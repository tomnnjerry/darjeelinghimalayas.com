"""Validate one land's content against content/SCHEMA.md.

Usage: python tools/check_region.py <land-slug> [--wiki]
--wiki also confirms every `wiki` title exists on English Wikipedia.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"
THEMES = {t["slug"] for t in json.loads((ROOT / "themes.json").read_text(encoding="utf-8"))}
PLAN = json.loads((ROOT / "_plan.json").read_text(encoding="utf-8"))
ALL_PLACES = {s for k, v in PLAN.items() if not k.startswith("_") for s in v["places"]}
KINDS = set("culture monastery viewpoint trek wildlife tea food rail craft adventure".split())
TIERS = {"Shoestring", "Value", "Comfort"}
BANNED = ["nestled", "breathtaking", "hidden gem", "paradise", "tapestry", "embark", "delve", "unleash",
          "vibrant", "bustling", "mesmeriz", "stunning", "magical", "heaven on earth", "feast for the eyes",
          "something for everyone", "whether you're", "look no further", "ultimate guide", "in this blog",
          "in conclusion", "unforgettable", "world-class", "seamless", "elevate", "immerse", "timeless",
          "boasts", "curated", "iconic", "pristine", "picturesque", "serene", "enchanting", "jewel", "!"]
errors, warns = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception as e:  # noqa: BLE001
        err(str(p), f"invalid JSON ({e})")
        return None


def months(where, v):
    if not (isinstance(v, list) and len(v) == 12 and all(x in (0, 1, 2) for x in v)):
        err(where, "best_months must be 12 ints of 0/1/2")


def faqs(where, v, n):
    if not isinstance(v, list) or len(v) != n:
        err(where, f"needs exactly {n} faqs (has {len(v) if isinstance(v, list) else 0})")
        return
    for f in v:
        if not f.get("q") or not f.get("a"):
            err(where, "faq missing q/a")


def heading(where, t):
    if t and t.rstrip().endswith("."):
        err(where, f"heading ends with full stop: {t!r}")
    if t and len(t) > 70:
        warns.append(f"{where}: heading over 70 chars: {t!r}")


def scan_banned(where, obj):
    text = json.dumps(obj, ensure_ascii=False).lower()
    for b in BANNED:
        if b in text:
            warns.append(f"{where}: banned word/phrase '{b}'")


def story(where, s):
    if not isinstance(s, dict) or not s.get("title") or len(s.get("paras", [])) < 2:
        err(where, "story needs a title and 2-3 paras")
    else:
        heading(where, s["title"])


def main():
    r = sys.argv[1]
    if r not in PLAN:
        sys.exit(f"unknown land {r}")
    base = ROOT / r
    planned = set(PLAN[r]["places"])
    wiki_titles = []
    reg = load(base / "region.json")
    places, stays, fests = {}, {}, {}
    for p in sorted((base / "places").glob("*.json")):
        d = load(p)
        if d:
            places[d["slug"]] = d
            if p.stem != d["slug"]:
                err(str(p), "file name must equal slug")
    for s in load(base / "stays.json") or []:
        stays[s["slug"]] = s
    for f in load(base / "festivals.json") or []:
        fests[f["slug"]] = f
    for s in sorted(planned - set(places)):
        err("plan", f"missing place file '{s}'")
    for s in sorted(set(places) - planned):
        err("plan", f"place '{s}' is not in _plan.json")

    if not reg:
        err("region", "region.json missing")
    else:
        months("region", reg.get("best_months"))
        faqs("region", reg.get("faqs"), 9)
        story("region story", reg.get("story"))
        if not reg.get("money"):
            err("region", "needs 'money'")
        if len(reg.get("highlights", [])) != 6:
            err("region", "needs 6 highlights")
        if len(reg.get("months", [])) != 12:
            err("region", "needs 12 months")
        for m in reg.get("months", []):
            for g in m.get("go", []):
                if g not in places:
                    err(f"region month {m.get('month')}", f"unknown place '{g}'")
            for e in m.get("events", []):
                if e not in fests:
                    err(f"region month {m.get('month')}", f"unknown festival '{e}'")
        wiki_titles.append(reg.get("wiki"))
        scan_banned("region", reg)

    exp_slugs = set()
    for slug, d in places.items():
        w = f"place {slug}"
        months(w, d.get("best_months"))
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("tagline"))
        story(w + " local_story", d.get("local_story"))
        if len(d.get("did_you_know", [])) != 3:
            err(w, "needs exactly 3 did_you_know")
        c = d.get("costs", [])
        if not (5 <= len(c) <= 7) or not all(isinstance(x, list) and len(x) == 2 for x in c):
            err(w, "costs must be 5-7 [item, amount] pairs")
        for t in d.get("themes", []):
            if t not in THEMES:
                err(w, f"unknown theme '{t}'")
        for n in d.get("nearby", []):
            if n not in planned:
                err(w, f"unknown nearby '{n}'")
        for s in d.get("stays", []):
            if s not in stays:
                err(w, f"unknown stay '{s}'")
        ex = d.get("experiences", [])
        if len(ex) != 4:
            err(w, f"needs 4 experiences (has {len(ex)})")
        for e in ex:
            heading(f"{w} exp", e.get("title"))
            faqs(f"{w} exp {e.get('slug')}", e.get("faqs"), 3)
            if e.get("kind") not in KINDS:
                err(f"{w} exp {e.get('slug')}", f"bad kind '{e.get('kind')}'")
            if e["slug"] in exp_slugs:
                err(w, f"duplicate experience slug {e['slug']}")
            exp_slugs.add(e["slug"])
            if e.get("wiki"):
                wiki_titles.append(e["wiki"])
        wiki_titles.append(d.get("wiki"))
        scan_banned(w, d)

    jcount, tiers = 0, {}
    for p in sorted((base / "journeys").glob("*.json")):
        d = load(p)
        if not d:
            continue
        jcount += 1
        w = f"journey {d.get('slug')}"
        months(w, d.get("best_months"))
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("title"))
        if d.get("tier") not in TIERS:
            err(w, f"bad tier '{d.get('tier')}'")
        tiers[d.get("tier")] = tiers.get(d.get("tier"), 0) + 1
        split = d.get("cost_split", [])
        if not (3 <= len(split) <= 6):
            err(w, "cost_split needs 3-6 lines")
        total_split = sum(x.get("inr", 0) for x in split)
        if total_split != d.get("price_from_inr"):
            err(w, f"cost_split sums to {total_split}, price is {d.get('price_from_inr')}")
        if len(d.get("save_money", [])) != 3:
            err(w, "needs 3 save_money tips")
        total = sum(s.get("nights", 0) for s in d.get("stops", []))
        if total != d.get("nights"):
            err(w, f"stop nights {total} != nights {d.get('nights')}")
        if len(d.get("days", [])) != d.get("nights", 0) + 1:
            err(w, "days must equal nights + 1")
        for s in d.get("stops", []):
            if s["place"] not in planned:
                err(w, f"unknown stop '{s['place']}'")
        for s in d.get("stays", []):
            if s not in stays:
                err(w, f"unknown stay '{s}'")
        for t in d.get("themes", []):
            if t not in THEMES:
                err(w, f"unknown theme '{t}'")
        scan_banned(w, d)

    for slug, s in stays.items():
        w = f"stay {slug}"
        faqs(w, s.get("faqs"), 3)
        if s.get("place") not in places:
            err(w, f"unknown place '{s.get('place')}'")
        if s.get("wiki"):
            wiki_titles.append(s["wiki"])
        scan_banned(w, s)

    gcount = 0
    for p in sorted((base / "guides").glob("*.json")):
        d = load(p)
        if not d:
            continue
        gcount += 1
        w = f"guide {d.get('slug')}"
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("title"))
        words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in d.get("sections", []))
        if words < 1000:
            warns.append(f"{w}: only {words} words")
        for s in d.get("sections", []):
            heading(w, s.get("heading"))
        for rp in d.get("related_places", []):
            if rp not in ALL_PLACES:
                err(w, f"unknown related place '{rp}'")
        scan_banned(w, d)

    for slug, f in fests.items():
        w = f"festival {slug}"
        faqs(w, f.get("faqs"), 4)
        if f.get("place") not in places:
            err(w, f"unknown place '{f.get('place')}'")
        if f.get("wiki"):
            wiki_titles.append(f["wiki"])
        scan_banned(w, f)

    routes = load(base / "routes.json") or []
    for rt in routes:
        w = f"route {rt.get('slug')}"
        faqs(w, rt.get("faqs"), 4)
        for k in ("from", "to"):
            if rt.get(k) not in ALL_PLACES:
                err(w, f"unknown {k} '{rt.get(k)}'")
        if rt.get("from") not in planned and rt.get("to") not in planned:
            err(w, "one end must be in this land")
        scan_banned(w, rt)

    # slugs must be unique across the whole site, not just this land
    own = {"route": {rt.get("slug") for rt in routes}, "stay": set(stays), "festival": set(fests),
           "experience": exp_slugs, "journey": {p.stem for p in (base / "journeys").glob("*.json")},
           "guide": {p.stem for p in (base / "guides").glob("*.json")}}
    for other in sorted(ROOT.iterdir()):
        if other == base or not (other / "places").is_dir():
            continue
        theirs = {"route": [x.get("slug") for x in load(other / "routes.json") or []],
                  "stay": [x.get("slug") for x in load(other / "stays.json") or []],
                  "festival": [x.get("slug") for x in load(other / "festivals.json") or []],
                  "experience": [e.get("slug") for p in (other / "places").glob("*.json")
                                 for e in (load(p) or {}).get("experiences", [])],
                  "journey": [p.stem for p in (other / "journeys").glob("*.json")],
                  "guide": [p.stem for p in (other / "guides").glob("*.json")]}
        for kind, slugs in theirs.items():
            for s in own[kind] & set(slugs):
                err(f"{kind} {s}", f"slug also used in {other.name}")

    if "--wiki" in sys.argv:
        titles = sorted({t for t in wiki_titles if t})
        for i in range(0, len(titles), 40):
            q = urllib.parse.urlencode({"action": "query", "titles": "|".join(titles[i:i + 40]),
                                        "redirects": 1, "format": "json", "formatversion": 2})
            req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q,
                                         headers={"User-Agent": "DarjeelingHimalayasBuild/1.0 (content check)"})
            data = json.load(urllib.request.urlopen(req, timeout=30))
            for pg in data["query"]["pages"]:
                if pg.get("missing"):
                    err("wiki", f"no Wikipedia article titled {pg['title']!r} (use '' or fix)")

    print(f"places={len(places)}/{len(planned)} experiences={len(exp_slugs)} stays={len(stays)} festivals={len(fests)} "
          f"routes={len(routes)} journeys={jcount} tiers={tiers} guides={gcount}")
    for w in warns:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
