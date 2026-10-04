"""Fast first pass: one lead photo per place, using batched Wikipedia/Commons requests.

Usage: python tools/fetch_leads.py [--force]

fetch_images.py asks Wikimedia several questions per place, which is slow when the API rate-limits. This script asks
the same question for up to 50 places at once (Wikipedia's lead image for each article, then Commons metadata for all
those files), so a whole site gets lead photos in a handful of requests. Places without an article fall back to one
Commons search each. Run fetch_images.py afterwards for the extra photos; it keeps what is already there.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import commons  # noqa: E402
from fetch_images import BAD_TITLE, CONTENT, OUT, REGIONS, clean, landscape_first, read  # noqa: E402


def lead_files(wikis):
    """{wiki title as written: 'File:...'} for the articles that have a lead image."""
    out = {}
    for i in range(0, len(wikis), 40):
        chunk = wikis[i:i + 40]
        data = commons._get(commons.WIKI_API, {"action": "query", "titles": "|".join(chunk), "redirects": 1,
                                               "prop": "pageimages", "piprop": "name", "pilimit": 50})
        q = data.get("query", {})
        alias = {}  # as written -> resolved title
        for m in q.get("normalized", []) + q.get("redirects", []):
            alias[m["from"]] = m["to"]
        by_title = {p["title"]: p.get("pageimage") for p in q.get("pages", [])}
        for w in chunk:
            t = w
            for _ in range(3):
                t = alias.get(t, t)
            if by_title.get(t):
                out[w] = "File:" + by_title[t].replace("_", " ")
    return out


def main():
    force = "--force" in sys.argv
    images = read(OUT) if OUT.exists() else {}
    places = []
    for land in REGIONS:
        for p in sorted((CONTENT / land / "places").glob("*.json")):
            d = read(p)
            if force or not images.get(f"place:{d['slug']}"):
                places.append(d)
    print(f"{len(places)} places need a lead photo", flush=True)
    wikis = sorted({d["wiki"] for d in places if d.get("wiki")})
    files = lead_files(wikis)
    print(f"{len(files)} of {len(wikis)} articles have a lead image", flush=True)
    recs = {r["file"]: r for r in commons.file_info(sorted(set(files.values())))}
    got = 0
    for d in places:
        f = files.get(d.get("wiki"))
        rec = recs.get(f) if f else None
        if rec and not BAD_TITLE.search(rec["file"]):
            images[f"place:{d['slug']}"] = [rec]
            got += 1
    OUT.write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{got} places got a photo from their article", flush=True)
    missing = [d for d in places if not images.get(f"place:{d['slug']}")]
    for n, d in enumerate(missing, 1):  # no article, or its lead image is a map or too small: search Commons
        words = (d.get("image_query") or d["name"]).split()
        queries = [" ".join(words), " ".join(words[:3]), f"{d['name']} {d.get('region', '')}".strip()]
        found = []
        for q in dict.fromkeys(queries):  # specific first, then looser: tiny villages rarely match a long phrase
            found = landscape_first(clean(commons.search_images(q, 3)))[:3]
            if found:
                break
        if found:
            images[f"place:{d['slug']}"] = found
            print(f"  {n}/{len(missing)} {d['slug']}: search found {len(found)}", flush=True)
        else:
            print(f"  {n}/{len(missing)} {d['slug']}: nothing", flush=True)
        if n % 5 == 0:
            OUT.write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
    OUT.write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
    have = sum(1 for k, v in images.items() if k.startswith("place:") and v)
    print(f"done: {have} places have photos", flush=True)


if __name__ == "__main__":
    main()
