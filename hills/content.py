"""In-memory catalogue built from content/*.json.

Every page on the site is rendered from this catalogue. In DEBUG the catalogue
reloads when any content file changes, so writers see edits on refresh.
"""
import json
import re
from collections import OrderedDict
from pathlib import Path

from django.conf import settings
from django.urls import reverse

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MONTH_SHORT = [m[:3] for m in MONTHS]
REGION_ORDER = ["darjeeling", "kurseong-mirik", "kalimpong", "singalila", "gangtok", "north-sikkim", "west-sikkim", "dooars"]
# The order of "The Climb" on the home page: lowest land first.
CLIMB_ORDER = ["dooars", "kalimpong", "kurseong-mirik", "gangtok", "darjeeling", "west-sikkim", "singalila", "north-sikkim"]
# Each land wears the colours it is known for.
# ground = dark sections, accent = highlights and buttons on dark, ink = accent text on light, tint = light wash
LANDS = {
    "darjeeling": {"palette": "Steam-engine blue and Kanchenjunga dawn", "ground": "#1C2E5A", "ground2": "#27407A",
                   "accent": "#F4A3A0", "ink": "#A8343A", "tint": "#E8ECF6", "alt": 2042, "glyph": "train"},
    "kurseong-mirik": {"palette": "Mirik lake teal and Sittong orange", "ground": "#0D4146", "ground2": "#145459",
                       "accent": "#F5A04A", "ink": "#9A4D0B", "tint": "#E0F0EF", "alt": 1458, "glyph": "tea"},
    "kalimpong": {"palette": "Monastery maroon and orchid", "ground": "#4B1229", "ground2": "#5E1C36",
                  "accent": "#EE9AD2", "ink": "#97296F", "tint": "#F7E6EF", "alt": 1247, "glyph": "orchid"},
    "singalila": {"palette": "Rhododendron red and ridge slate", "ground": "#23263B", "ground2": "#2F3350",
                  "accent": "#F0596B", "ink": "#B0233A", "tint": "#ECEBF3", "alt": 3636, "glyph": "ridge"},
    "gangtok": {"palette": "Tsomgo turquoise and prayer-flag yellow", "ground": "#0A3F4C", "ground2": "#0F5262",
                "accent": "#F6CB3A", "ink": "#7A5D00", "tint": "#DFF1F3", "alt": 1650, "glyph": "flags"},
    "north-sikkim": {"palette": "Glacier ice and primula violet", "ground": "#2A1F4A", "ground2": "#382C5E",
                     "accent": "#A9DCF5", "ink": "#2A6688", "tint": "#ECE8F6", "alt": 5183, "glyph": "glacier"},
    "west-sikkim": {"palette": "Butter-lamp ochre and cardamom green", "ground": "#4A2709", "ground2": "#5D3410",
                    "accent": "#A6DC8E", "ink": "#2E6A21", "tint": "#F8EEDC", "alt": 2150, "glyph": "chorten"},
    "dooars": {"palette": "Sal forest green and elephant-grass gold", "ground": "#143421", "ground2": "#1C4430",
               "accent": "#E3C65A", "ink": "#6F5C0C", "tint": "#E4EFE3", "alt": 120, "glyph": "rhino"},
}

# Shiny gradients per land: `grad` = ground (dark, 3 stops), `foil` = metallic accent (light → mid → deep).
GRADIENTS = {
    "darjeeling": {"grad": ("#101B3D", "#1F3570", "#3A4F94"), "foil": ("#FFE1DB", "#F4A3A0", "#D9636A")},
    "kurseong-mirik": {"grad": ("#06292D", "#0E4F55", "#17767A"), "foil": ("#FFE2B8", "#F5A04A", "#CC6E14")},
    "kalimpong": {"grad": ("#2E0717", "#5E1534", "#86274E"), "foil": ("#FFE0F3", "#EE9AD2", "#C3559F")},
    "singalila": {"grad": ("#14162A", "#2A2E4D", "#463E66"), "foil": ("#FFD0D5", "#F0596B", "#C42C44")},
    "gangtok": {"grad": ("#04252E", "#0A4C5C", "#11798A"), "foil": ("#FFF3B0", "#F6CB3A", "#C99A0A")},
    "north-sikkim": {"grad": ("#170F2E", "#33265C", "#4B3A82"), "foil": ("#EAF8FF", "#A9DCF5", "#5FA8D0")},
    "west-sikkim": {"grad": ("#2C1504", "#5E3410", "#8A4F18"), "foil": ("#EEFFE2", "#A6DC8E", "#5FA548")},
    "dooars": {"grad": ("#0A1F12", "#18452B", "#2A6A3E"), "foil": ("#FFF4BE", "#E3C65A", "#B3921E")},
}
for _slug, _g in GRADIENTS.items():
    LANDS[_slug].update(_g)

KINDS = OrderedDict([
    ("viewpoint", ("Viewpoints", "Kanchenjunga at dawn and the valleys below", "Where to stand, how early to leave and what it costs to get there. Clear mornings come mostly from October to early December and in March and April.")),
    ("monastery", ("Monasteries", "Gompas, prayer halls and butter lamps", "Working monasteries first, sights second. Go at prayer time, walk clockwise, ask before you photograph inside.")),
    ("culture", ("Culture and history", "Old bazaars, bungalows and the people who keep them", "Stories told on site: the Raj hill station, the Silk Route trade, the Lepcha, Bhutia and Gorkha homes of these hills.")),
    ("tea", ("Tea", "Gardens, factories and the first flush", "Walk the plucking paths, see a factory at work and taste the flushes side by side, often for the price of a cup.")),
    ("rail", ("Toy train", "The Darjeeling Himalayan Railway", "Joyrides, loops and the full climb from the plains on the two-foot line.")),
    ("trek", ("Treks and walks", "Ridges, forests and village trails", "Graded by hours, height gained and terrain, with homestays and lodges at the end of the day.")),
    ("wildlife", ("Wildlife and birds", "Rhinos, red pandas and hornbills", "Safaris in the Dooars and forest walks in the hills, timed to the season and the park rules.")),
    ("food", ("Food", "Momos, thukpa, sel roti and chhurpi", "Kitchens, markets and tea shops where locals eat, for less than a hotel lunch.")),
    ("craft", ("Crafts", "Weavers, carvers and nurseries", "Thangka painters, carpet weavers, paper makers and orchid growers in their own workshops.")),
    ("adventure", ("Adventure", "Rafting, paragliding and high roads", "Active days with licensed operators, graded honestly and priced plainly.")),
])

_cache = {"stamp": None, "cat": None}


def clean_author(a):
    """Commons 'Artist' fields often carry a timestamp, a caption or a whole citation: keep just the name."""
    a = re.sub(r"\s+", " ", a or "").strip()
    a = re.sub(r"\s*\d{4}-\d{2}-\d{2}.*$", "", a)          # '... 2010-09-21 12:41:53 This is a cropped ...'
    a = re.sub(r"\s*\((based on|after|from)\b.*$", "", a, flags=re.I)
    m = re.match(r"(.{10,80}?\))\.\s", a)                   # 'Saleur, Louis (1861-1889). Photographe ...'
    if m:
        a = m.group(1)
    if len(a) > 80:
        a = a[:77].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return a or "Unknown author"


def _read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _stamp(root):
    return max((p.stat().st_mtime for p in root.rglob("*.json")), default=0)


def catalogue():
    root = Path(settings.CONTENT_DIR)
    if _cache["cat"] is None or settings.DEBUG:
        stamp = _stamp(root)
        if stamp != _cache["stamp"]:
            _cache["cat"] = Catalogue(root)
            _cache["stamp"] = stamp
    return _cache["cat"]


def month_bar(best):
    """[{'m': 'Jan', 'v': 2}, ...] for the 12-month strip."""
    best = best or [0] * 12
    return [{"m": MONTH_SHORT[i], "full": MONTHS[i], "v": best[i] if i < len(best) else 0} for i in range(12)]


def best_range(best):
    """'Oct – Mar' style label from a 12-int array (rating 2 = best)."""
    if not best:
        return ""
    good = {i for i, v in enumerate(best) if v == 2} or {i for i, v in enumerate(best) if v >= 1}
    if not good:
        return ""
    if len(good) == 12:
        return "All year"
    runs = []  # runs on a circular calendar, e.g. Oct..Mar
    for i in range(12):
        if i in good and (i - 1) % 12 not in good:
            run, j = [i], (i + 1) % 12
            while j in good:
                run.append(j)
                j = (j + 1) % 12
            runs.append(run)
    labels = []
    for run in runs:
        labels.append(MONTH_SHORT[run[0]] if len(run) == 1 else f"{MONTH_SHORT[run[0]]} – {MONTH_SHORT[run[-1]]}")
    return " · ".join(labels)


class Catalogue:
    def __init__(self, root):
        self.root = root
        self.themes = OrderedDict((t["slug"], t) for t in _read(root / "themes.json"))
        img_file = root / "images.json"
        self.images = _read(img_file) if img_file.exists() else {}
        for recs in self.images.values():
            for rec in recs:
                rec["author"] = clean_author(rec.get("author"))
        self.regions = OrderedDict()
        self.places = OrderedDict()
        self.experiences = OrderedDict()
        self.journeys = OrderedDict()
        self.stays = OrderedDict()
        self.guides = OrderedDict()
        self.festivals = OrderedDict()
        self.routes = OrderedDict()
        for slug in REGION_ORDER:
            base = root / slug
            if (base / "region.json").exists():
                self._load_region(slug, base)
        self.posts = OrderedDict()
        for p in (root / "journal").glob("*.json") if (root / "journal").exists() else []:
            d = _read(p)
            d["url"] = reverse("post", args=[d["slug"]])
            self.posts[d["slug"]] = d
        self.posts = OrderedDict(sorted(self.posts.items(), key=lambda kv: kv[1].get("date", ""), reverse=True))
        self._link()
        self._link_posts()

    # ---------- loading ----------
    def _load_region(self, slug, base):
        r = _read(base / "region.json")
        r["slug"] = slug
        pal = LANDS[slug]
        r.update(pal)
        r["pigment"], r["deep"] = pal["accent"], pal["ink"]
        r["url"] = reverse("region", args=[slug])
        r["places"], r["journeys"], r["stays"], r["guides"], r["festivals"], r["routes"] = [], [], [], [], [], []
        self.regions[slug] = r
        for p in sorted((base / "places").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("place", args=[slug, d["slug"]])
            self.places[d["slug"]] = d
            r["places"].append(d)
            for e in d.get("experiences", []):
                e["place"] = d["slug"]
                e["region"] = slug
                e["url"] = reverse("experience", args=[slug, d["slug"], e["slug"]])
                self.experiences[e["slug"]] = e
        for p in sorted((base / "journeys").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("journey", args=[d["slug"]])
            self.journeys[d["slug"]] = d
            r["journeys"].append(d)
        for name, store, key, view in (("stays.json", self.stays, "stays", "stay"),
                                       ("festivals.json", self.festivals, "festivals", "festival"),
                                       ("routes.json", self.routes, "routes", "route")):
            f = base / name
            for d in (_read(f) if f.exists() else []):
                d["region"] = slug
                d["url"] = reverse(view, args=[d["slug"]])
                store[d["slug"]] = d
                r[key].append(d)
        for p in sorted((base / "guides").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("guide", args=[d["slug"]])
            self.guides[d["slug"]] = d
            r["guides"].append(d)

    def _imgs(self, *keys):
        for k in keys:
            if self.images.get(k):
                return self.images[k]
        return []

    def _link(self):
        # drop routes whose places do not exist (yet)
        for slug in [s for s, rt in self.routes.items() if rt.get("from") not in self.places or rt.get("to") not in self.places]:
            dead = self.routes.pop(slug)
            self.regions[dead["region"]]["routes"].remove(dead)
        for r in self.regions.values():
            r["images"] = self._imgs(f"region:{r['slug']}") or [
                i for p in r["places"][:6] for i in self._imgs(f"place:{p['slug']}")[:1]]
            r["best_label"] = best_range(r.get("best_months"))
            r["bar"] = month_bar(r.get("best_months"))
        for p in self.places.values():
            p["region_obj"] = self.regions[p["region"]]
            p["images"] = self._imgs(f"place:{p['slug']}")
            p["best_label"] = best_range(p.get("best_months"))
            p["bar"] = month_bar(p.get("best_months"))
            p["nearby_objs"] = [self.places[s] for s in p.get("nearby", []) if s in self.places]
            p["stay_objs"] = [self.stays[s] for s in p.get("stays", []) if s in self.stays]
            p["journey_objs"] = [j for j in self.journeys.values()
                                 if any(s["place"] == p["slug"] for s in j.get("stops", []))]
            p["festival_objs"] = [f for f in self.festivals.values() if f.get("place") == p["slug"]]
            p["route_objs"] = [rt for rt in self.routes.values() if p["slug"] in (rt.get("from"), rt.get("to"))]
        for r in self.regions.values():
            # the places most journeys stop at lead menus and supply the land's lead photos
            r["top_places"] = sorted(r["places"], key=lambda p: (-len(p["journey_objs"]), p["name"]))
            r["images"] = self._imgs(f"region:{r['slug']}") or [
                i for p in r["top_places"][:6] for i in p["images"][:1]]
        for e in self.experiences.values():
            place = self.places[e["place"]]
            e["place_obj"] = place
            e["region_obj"] = place["region_obj"]
            e["images"] = self._imgs(f"exp:{e['slug']}") or place["images"][1:] or place["images"]
            e["themes"] = place.get("themes", [])
        for s in self.stays.values():
            place = self.places.get(s.get("place"))
            s["place_obj"] = place
            s["region_obj"] = self.regions[s["region"]]
            s["images"] = self._imgs(f"stay:{s['slug']}") or (place["images"] if place else [])
            s["journey_objs"] = [j for j in self.journeys.values() if s["slug"] in j.get("stays", [])]
        for j in self.journeys.values():
            j["region_obj"] = self.regions[j["region"]]
            stops = [dict(st, obj=self.places[st["place"]]) for st in j.get("stops", []) if st["place"] in self.places]
            j["stop_objs"] = stops
            j["images"] = self._imgs(f"journey:{j['slug']}") or [
                i for st in stops for i in st["obj"]["images"][:1]]
            j["stay_objs"] = [self.stays[s] for s in j.get("stays", []) if s in self.stays]
            j["best_label"] = best_range(j.get("best_months"))
            j["bar"] = month_bar(j.get("best_months"))
            j["days_count"] = j.get("nights", 0) + 1
            j["per_day"] = int(round(j.get("price_from_inr", 0) / max(j["days_count"], 1) / 50.0) * 50)
            total = sum(x.get("inr", 0) for x in j.get("cost_split", [])) or 1
            for x in j.get("cost_split", []):
                x["pct"] = round(100 * x.get("inr", 0) / total, 1)
            for d in j.get("days", []):
                d["place_obj"] = self.places.get(d.get("place"))
        for r in self.regions.values():
            js = r["journeys"]
            r["price_from"] = min((j.get("price_from_inr", 0) for j in js), default=0)
            r["per_day_from"] = min((j["per_day"] for j in js), default=0)
            r["max_alt"] = max((p.get("altitude_m") or 0 for p in r["places"]), default=0)
            r["min_alt"] = min((p.get("altitude_m") or 0 for p in r["places"] if p.get("altitude_m")), default=0)
        self.facts = [{"text": t, "place": p} for p in self.places.values() for t in p.get("did_you_know", [])]
        for g in self.guides.values():
            g["region_obj"] = self.regions[g["region"]]
            rel = [self.places[s] for s in g.get("related_places", []) if s in self.places]
            g["related_objs"] = rel
            g["images"] = self._imgs(f"guide:{g['slug']}") or [i for p in rel for i in p["images"][:1]] or g["region_obj"]["images"]
            words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in g.get("sections", []))
            g["read_min"] = max(3, round(words / 220))
            for s in g.get("sections", []):
                s["anchor"] = re.sub(r"[^a-z0-9]+", "-", s.get("heading", "").lower()).strip("-")
        for f in self.festivals.values():
            place = self.places.get(f.get("place"))
            f["place_obj"] = place
            f["region_obj"] = self.regions[f["region"]]
            f["images"] = self._imgs(f"fest:{f['slug']}") or (place["images"] if place else [])
        for rt in self.routes.values():
            rt["from_obj"] = self.places.get(rt.get("from"))
            rt["to_obj"] = self.places.get(rt.get("to"))
            rt["region_obj"] = self.regions[rt["region"]]
            rt["images"] = (rt["to_obj"] or {}).get("images", []) + (rt["from_obj"] or {}).get("images", [])[:1]
        for t in self.themes.values():
            t["url"] = reverse("theme", args=[t["slug"]])

    def _link_posts(self):
        from datetime import date
        for d in self.posts.values():
            d["region_objs"] = [self.regions[r] for r in d.get("regions", []) if r in self.regions]
            d["journey_objs"] = [self.journeys[j] for j in d.get("related_journeys", []) if j in self.journeys]
            d["place_objs"] = [self.places[x] for x in d.get("related_places", []) if x in self.places]
            d["images"] = (self._imgs(f"blog:{d['slug']}") or [i for x in d["place_objs"] for i in x["images"][:1]])
            words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in d.get("sections", []))
            d["read_min"] = max(3, round(words / 220))
            d["cat_slug"] = re.sub(r"[^a-z0-9]+", "-", d.get("category", "").lower()).strip("-")
            try:
                d["date_obj"] = date.fromisoformat(d.get("date", ""))
            except ValueError:
                d["date_obj"] = None
            land = d["region_objs"][0]["slug"] if d["region_objs"] else None
            d["land"] = land
            stores = {"journey": self.journeys, "place": self.places, "stay": self.stays, "guide": self.guides, "festival": self.festivals}
            for sec in d.get("sections", []):
                sec["anchor"] = re.sub(r"[^a-z0-9]+", "-", sec.get("heading", "").lower()).strip("-")
                objs = []
                for ln in sec.get("links", []):
                    o = stores.get(ln.get("type"), {}).get(ln.get("slug"))
                    if o:
                        objs.append({"type": ln["type"], "title": o.get("title") or o.get("name"), "url": o["url"],
                                     "img": (o.get("images") or [None])[0]})
                sec["link_objs"] = objs
        self.post_categories = OrderedDict()
        for d in self.posts.values():
            self.post_categories.setdefault(d["cat_slug"], {"slug": d["cat_slug"], "name": d.get("category"), "posts": []})["posts"].append(d)

    # ---------- queries ----------
    def theme_items(self, theme, region=None):
        def ok(x):
            return region is None or x.get("region") == region
        places = [p for p in self.places.values() if theme in p.get("themes", []) and ok(p)]
        journeys = [j for j in self.journeys.values() if theme in j.get("themes", []) and ok(j)]
        place_slugs = {p["slug"] for p in places}
        stays = [s for s in self.stays.values() if s.get("place") in place_slugs and ok(s)]
        experiences = [e for e in self.experiences.values() if e["place"] in place_slugs and ok(e)]
        return {"places": places, "journeys": journeys, "stays": stays, "experiences": experiences}

    def region_theme_pairs(self):
        """(region, theme) pairs with enough content to deserve a page."""
        out = []
        for r in self.regions:
            for t in self.themes:
                items = self.theme_items(t, r)
                if len(items["places"]) >= 2 and (items["journeys"] or len(items["places"]) >= 3):
                    out.append((r, t))
        return out

    def region_kind_pairs(self):
        """(region, kind) pairs with at least 3 experiences."""
        out = []
        for r in self.regions:
            for k in KINDS:
                if sum(1 for e in self.experiences.values() if e["region"] == r and e.get("kind") == k) >= 3:
                    out.append((r, k))
        return out

    def counts(self):
        return {
            "regions": len(self.regions), "places": len(self.places), "experiences": len(self.experiences),
            "journeys": len(self.journeys), "stays": len(self.stays), "guides": len(self.guides),
            "festivals": len(self.festivals), "routes": len(self.routes), "themes": len(self.themes),
            "posts": len(self.posts),
        }

    def all_images(self):
        seen, out = set(), []
        for key, recs in self.images.items():
            for rec in recs:
                if rec["file"] not in seen:
                    seen.add(rec["file"])
                    out.append(dict(rec, used_for=key))
        return out
