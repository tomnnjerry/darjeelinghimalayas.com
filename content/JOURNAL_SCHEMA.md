# Journal ("Stories from the hills"): schema

Long reads at `/journal/<slug>/`, grouped by `category` at `/journal/topic/<category>/`. One JSON file per post in
`content/journal/<slug>.json`; the file name must equal the slug. All writing rules in [SCHEMA.md](SCHEMA.md) apply
(voice, banned words, no emoji, no exclamation marks, no full stop after headings, true facts only, prices indicative
in INR, "check current status before you travel" on anything that changes).

```json
{
  "slug": "toy-train-agony-point-and-the-loops",
  "title": "≤ 65 chars, no full stop",
  "category": "History | Trips | Seasons | Food | Treks | Budget | Culture | Wildlife | Practical",
  "date": "2026-09-14",
  "regions": ["darjeeling"],                       // land slugs from _plan.json; the first sets the colours
  "meta_description": "≤ 158 chars",
  "summary": "40–60 words, answer first",
  "wiki": "Darjeeling Himalayan Railway",          // exact English Wikipedia title for the lead photo, or ""
  "image_query": "Batasia Loop toy train Darjeeling",
  "key_takeaways": ["…", "…", "…", "…"],           // exactly 4, one sentence each
  "sections": [                                     // 5–8 sections, 1,050+ words in all
    {"heading": "≤ 55 chars", "paras": ["…"], "list": ["optional"],
     "table": {"head": ["…"], "rows": [["…"]]},     // at least one section has a table
     "links": [{"type": "place | journey | stay | guide | festival", "slug": "…"}]}   // optional, slugs must exist
  ],
  "related_places": ["place-slug"],
  "related_journeys": ["journey-slug"],
  "faqs": [{"q": "…", "a": "40–90 words"}]          // exactly 5
}
```

Validate with `python tools/check_journal.py`, then fetch photos with `python tools/fetch_images.py journal`.
