# Darjeeling Himalayas: content schema and house rules

Darjeeling Himalayas (darjeelinghimalayas.com) plans honest-priced, locally rooted trips in eight lands of the
Darjeeling and Sikkim Himalaya and the Dooars below them:
Darjeeling & Ghoom (`darjeeling`), Kurseong, Mirik & the tea valleys (`kurseong-mirik`), Kalimpong, Lava & Lolegaon
(`kalimpong`), Sandakphu & the Singalila Ridge (`singalila`), Gangtok & East Sikkim (`gangtok`), North Sikkim
(`north-sikkim`), Pelling, Yuksom & South Sikkim (`west-sikkim`), the Dooars & Siliguri (`dooars`).

Byline: "Darjeeling Himalayas Hill Desk". Voice: a well-read local friend. Warm, exact, first person plural ("we"),
never salesy. We tell the story of a place (who lived there, what the name means, what happened there, what people
eat and grow) and then the hard facts: how to get there, what it costs, when to go.
Audience: Indian families, couples, students and solo travellers, and international backpackers, who want a good trip
WITHOUT luxury prices. Shared jeeps, the toy train, homestays, government lodges, trekkers' huts, small family hotels.

All content is JSON, UTF-8, under `content/<land>/`. The JSON must parse (no comments, no trailing commas).
Slugs are lowercase-hyphenated ASCII and unique within their type across the WHOLE site (prefix experiences,
journeys, guides, stays, festivals and routes with a place or land word, e.g. `darjeeling-batasia-loop-dawn`).
PLACE SLUGS ARE FIXED in `content/_plan.json`: create exactly those place files, no others.

## Story rules (the point of this site)

- Every place has a `local_story`: the real history or lore of that place, told as a story with names, years and
  specifics. Examples of the kind of thing we want: the meaning of the name in Lepcha, Nepali or Tibetan; who built
  the monastery and when; the tea garden's planter history; the Tibetan refugees who settled after 1959; the Lepcha
  legend of Mount Kanchenjunga as guardian; the toy train's Agony Point; Tagore's stays at Mungpoo; the old Silk Route
  through Zuluk and Nathu La; Kalimpong's wool trade with Lhasa. TRUE things only. If a story is folklore, say so
  ("Lepcha elders tell…", "the local story is…"). Never invent a person, a quote, a date or a legend.
- `did_you_know`: 3 lesser-known, checkable facts per place (each ≤ 35 words). Specific: numbers, years, names.
- When you are not sure of a fact, leave it out, or put it in the region's `to_confirm` list with a short note.
- Never invent reviews, awards, statistics, star ratings, founders, staff names, client counts or "since 19xx".

## Writing rules (strict)

- Headings and titles: no full stop at the end; short, one line on desktop (≤ 60 characters).
- Plain and specific: numbers over adjectives (km, hours, metres, ₹, months, °C).
- BANNED words/phrases: nestled, breathtaking, hidden gem, paradise, tapestry, embark, delve, unleash, vibrant,
  bustling, mesmerizing, stunning, magical, heaven on earth, a feast for the eyes, something for everyone,
  whether you're, look no further, ultimate guide, in this blog, in conclusion, unforgettable, world-class,
  seamless, curated, elevate, immerse, timeless, jewel, iconic, boasts, queen of the hills (max once per land),
  offbeat (max once per file), pristine, picturesque, serene, enchanting.
- No emoji. No exclamation marks.
- Facts that change (permits, Protected Area Permits, Inner Line Permits, road openings, landslides, toy train
  services, park closures, festival dates, fees, fares): state the rule as you understand it and add
  "check current status before you travel". North Sikkim roads (NH10, Chungthang, Lachen, Gurudongmar) and the
  Teesta valley roads have had long closures since the October 2023 Teesta flood: always flag them.
- Prices are INDICATIVE, in INR, realistic for budget and mid-range travel in 2025–26. Write money as "₹1,800".
  Shared jeep seats, homestay rates with meals, government lodge rates, guide fees, permit fees, safari fees.
  Never pretend precision: "₹250–350 a seat", "about ₹2,000 per person with dinner and breakfast".
- Stays: REAL properties only, that you are confident exist and operate: government lodges (WBTDC, WBFDC, GTA,
  Sikkim Tourism), trekkers' huts, well-known family-run hotels and guesthouses, long-running homestays you
  are sure of, and heritage budget hotels. If unsure, describe the homestay VILLAGE (e.g. "the homestays of
  Sillery Gaon") in `where_to_stay` instead of naming a property. Do not invent amenities or prices.
- `best_months` is ALWAYS an array of 12 integers, Jan..Dec: 2 = best, 1 = good, 0 = avoid/closed.
- `wiki` = the EXACT title of an existing English Wikipedia article about that thing (used to fetch photos with
  credits). Use "" if none exists. Do not guess; small villages often have no article.
- `image_query` = 3–6 words that would find a real photo of exactly that subject on Wikimedia Commons
  (e.g. "Batasia Loop Darjeeling train", "Rumtek Monastery Sikkim").
- FAQs: real questions travellers search for; answers 40–90 words, answer first, specific.
- `name_local`: the place name in Nepali Devanagari (e.g. "दार्जिलिङ") ONLY if you are confident; else "".

## Files to write for each land `<r>`

### 1. `content/<r>/region.json`
```json
{
  "slug": "darjeeling", "name": "Darjeeling & Ghoom", "short": "Darjeeling", "country": "India",
  "state": "West Bengal | Sikkim",
  "tagline": "≤ 8 words",
  "meta_description": "≤ 158 chars",
  "summary": "40–60 word answer-first summary",
  "story": {"title": "≤ 60 chars", "paras": ["70–120 words", "…", "…"]},       // 3 paras: the land's story
  "intro": ["para (60–110 words)", "para", "para"],
  "facts": [["Best months", "Oct – Dec · Mar – May"], ["Gateway", "NJP / Bagdogra"], ["From Siliguri", "≈ 65 km · 3 h"], ["Altitude", "…"], ["Languages", "…"], ["Permits", "…"], ["Daily budget", "₹1,800–3,000 pp"]],
  "best_months": [1,1,2,2,2,0,0,0,1,2,2,2],
  "highlights": [{"title": "…", "text": "35–60 words"}],          // exactly 6
  "getting_there": "90–150 words (NJP, Bagdogra, Siliguri jeep stands, shared and reserved jeep fares)",
  "permits": "60–120 words, or '' if none apply",
  "money": "80–130 words: what a day really costs here, shoestring vs comfortable, where people overspend",
  "wiki": "Darjeeling",
  "lat": 27.04, "lng": 88.26,
  "months": [                                                      // exactly 12, Jan..Dec
    {"month": "January", "rating": 1, "weather": "Darjeeling 2–9 °C, dry, clear mornings", "summary": "60–100 words",
     "go": ["place-slug", "place-slug", "place-slug"], "events": ["festival-slug"], "tip": "one sentence"}
  ],
  "faqs": [{"q": "…", "a": "…"}],                                   // exactly 9
  "to_confirm": ["short notes on facts you were not sure of (may be empty)"]
}
```

### 2. `content/<r>/places/<place-slug>.json` (every place in _plan.json for your land)
```json
{
  "slug": "ghoom", "name": "Ghoom", "name_local": "घुम", "region": "darjeeling",
  "kind": "town | village | hill station | viewpoint | tea garden | lake | national park | forest village | pass | valley | monastery town | river town | trek stop | market town",
  "wiki": "Ghum, India", "image_query": "Ghoom railway station Darjeeling",
  "lat": 26.99, "lng": 88.25, "altitude_m": 2258,
  "tagline": "≤ 70 chars",
  "meta_description": "≤ 158 chars",
  "summary": "40–60 word answer-first summary",
  "local_story": {"title": "≤ 60 chars", "paras": ["70–120 words", "…"]},   // 2–3 paras, TRUE
  "did_you_know": ["≤ 35 words", "…", "…"],                                  // exactly 3
  "intro": ["para 70–120 words", "para"],
  "facts": [["Best months", "…"], ["Nights we suggest", "1–2"], ["From Siliguri", "≈ 60 km · 2.5 h"], ["Altitude", "2,258 m"], ["Known for", "…"], ["Network", "Jio/Airtel good in town"]],
  "best_months": [1,1,2,2,2,0,0,0,1,2,2,2],
  "nights": "1–2",
  "costs": [["Shared jeep from Siliguri", "₹200–250 a seat"], ["Homestay with dinner and breakfast", "₹1,500–2,200 pp"], ["Momos and tea", "₹80–150"], ["…", "…"]],   // 5–7 rows, indicative
  "highlights": [{"title": "…", "text": "35–60 words"}],          // 5–6
  "how_to_reach": [{"mode": "Shared jeep", "text": "…"}, {"mode": "Toy train", "text": "…"}, {"mode": "Reserved car", "text": "…"}],   // 2–4 real options
  "where_to_stay": "70–120 words naming areas, homestay villages and real budget properties",
  "stays": ["stay-slug"],                                         // slugs from your stays.json in this place (may be [])
  "tips": ["one sentence", "…"],                                   // 5
  "themes": ["toy-train", "monasteries"],                          // from THEMES below, 2–5
  "nearby": ["place-slug"],                                        // 2–4 other places in YOUR land
  "experiences": [                                                 // exactly 4
    {"slug": "ghoom-yiga-choeling-morning-prayers", "title": "≤ 55 chars",
     "kind": "culture | monastery | viewpoint | trek | wildlife | tea | food | rail | craft | adventure",
     "duration": "1.5 hours", "best_time": "6–7 am, Oct–May", "cost": "Free · donation welcome | ₹… ",
     "image_query": "Yiga Choeling monastery Ghoom", "wiki": "Ghoom Monastery",
     "summary": "35–55 words", "body": ["para 70–120 words", "para", "para"],
     "good_for": ["couples", "families", "solo", "students", "photographers", "seniors", "first-timers"],
     "faqs": [{"q": "…", "a": "…"}]}                                // exactly 3
  ],
  "faqs": [{"q": "…", "a": "…"}]                                    // exactly 9
}
```

### 3. `content/<r>/journeys/<journey-slug>.json` (12 per land; slug ends with "-<N>n")
```json
{
  "slug": "darjeeling-toy-train-and-tea-4n", "title": "≤ 50 chars", "region": "darjeeling",
  "nights": 4, "themes": ["toy-train", "tea-country"],
  "tier": "Shoestring | Value | Comfort",
  "travel_mode": "Shared jeeps | Reserved car | On foot | Mixed",
  "stops": [{"place": "darjeeling", "nights": 3}, {"place": "lamahatta", "nights": 1}],   // own-land places; nights sum = nights
  "start": "NJP railway station or Bagdogra airport", "end": "NJP railway station or Bagdogra airport",
  "price_from_inr": 14500,
  "cost_split": [{"item": "Jeeps, toy train and transfers", "inr": 4000}, {"item": "Homestays, 4 nights with dinner and breakfast", "inr": 7600},
                 {"item": "Lunches, tea and snacks", "inr": 1900}, {"item": "Entry fees, permits and guide", "inr": 1000}],   // 3–6 lines; inr sums EXACTLY to price_from_inr
  "best_months": [1,1,2,2,2,0,0,0,1,2,2,2],
  "pace": "Easy | Balanced | Active", "max_altitude_m": 2590,
  "meta_description": "≤ 158 chars including 'N nights' and the price",
  "summary": "40–60 words", "intro": ["para 70–120 words", "para"],
  "highlights": ["…"],                                                          // 5
  "days": [{"day": 1, "title": "≤ 45 chars", "place": "darjeeling", "overnight": "Darjeeling", "drive": "≈ 70 km · 3 h by shared jeep or ''", "text": "70–130 words", "meals": "Dinner", "spend": "₹350 jeep seat + ₹150 lunch"}],  // days = nights + 1
  "stays": ["stay-slug"],                                                       // may be []
  "includes": ["…"], "excludes": ["…"],
  "save_money": ["one sentence money-saving tip", "…", "…"],                   // 3
  "good_to_know": ["…"],
  "faqs": [{"q": "…", "a": "…"}]                                                // exactly 9
}
```
Price is per person, twin sharing, Indian nationals, from NJP/Bagdogra back to NJP/Bagdogra, round to ₹500.
Tiers: Shoestring ≈ ₹1,500–2,500 per person per day; Value ≈ ₹2,500–4,000; Comfort ≈ ₹4,000–6,500.
Mix the tiers across your 12 (at least 3 of each). Lengths from 2 to 9 nights. Cross-land journeys are not
allowed in your folder (stops must be your own land's places).

### 4. `content/<r>/stays.json` — array, 4–8 real properties
```json
[{"slug": "darjeeling-dekeling-hotel", "name": "Dekeling Hotel", "place": "darjeeling",
  "kind": "homestay | guesthouse | government lodge | trekkers' hut | budget hotel | heritage hotel | forest bungalow | hostel | tea garden homestay | camp",
  "price_band": "₹2,000–3,500 a room (indicative)",
  "wiki": "", "image_query": "Dekeling Hotel Darjeeling",
  "summary": "35–55 words", "body": ["para 70–110 words", "para"],
  "why": ["one line", "one line", "one line"], "best_for": ["couples", "…"],
  "website": "official URL only if certain, else ''",
  "faqs": [{"q": "…", "a": "…"}]}]                                                // exactly 3
```

### 5. `content/<r>/guides/<guide-slug>.json` (10 per land)
```json
{"slug": "darjeeling-on-a-budget", "title": "≤ 60 chars", "region": "darjeeling",
 "category": "planning | seasons | stays | culture | food | wildlife | practical | treks | budget | history",
 "meta_description": "≤ 158 chars", "summary": "40–60 words answer-first",
 "sections": [{"heading": "≤ 50 chars", "paras": ["…"], "list": ["optional"], "table": {"head": ["…"], "rows": [["…"]]}}],
 "related_places": ["place-slug"],
 "faqs": [{"q": "…", "a": "…"}]}                                                 // exactly 9
```
Guides: 1,100–1,600 words of body across 5–8 sections; use a table in at least one section. Every land needs at
least: one budget guide (what things cost), one history/story guide, one best-time guide, one getting-there guide,
one food guide.

### 6. `content/<r>/festivals.json` — array, 2–4 REAL recurring festivals or fairs
```json
[{"slug": "ghoom-losar", "name": "Losar at Ghoom", "place": "ghoom", "wiki": "Losar",
  "image_query": "Losar cham dance monastery", "when": "Feb–Mar, Tibetan New Year (lunar calendar)", "month_nums": [2, 3],
  "summary": "35–55 words", "body": ["para 70–110 words", "para", "para"], "tips": ["…", "…", "…"],
  "faqs": [{"q": "…", "a": "…"}]}]                                                // exactly 4
```

### 7. `content/<r>/routes.json` — array, 4–6 routes
```json
[{"slug": "siliguri-to-darjeeling", "from": "siliguri", "to": "darjeeling", "distance_km": 65,
  "summary": "35–55 words",
  "options": [{"mode": "Shared jeep", "time": "3–3.5 h", "fare": "₹250–350 a seat", "text": "50–90 words"},
              {"mode": "Reserved car", "time": "3 h", "fare": "₹3,000–4,000 a car", "text": "…"},
              {"mode": "Toy train", "time": "7–8 h", "fare": "…", "text": "…"}],
  "stops_on_way": ["…"], "tip": "one sentence",
  "faqs": [{"q": "…", "a": "…"}]}]                                                // exactly 4
```
`from` and `to` may be ANY place slug in `_plan.json` (e.g. `siliguri`, `gangtok`), but at least one end must be in
your land.

## THEMES (use these slugs only)
tea-country, toy-train, treks, homestays, monasteries, kanchenjunga-views, wildlife-birds, family-trips,
budget-honeymoons, solo-backpacking, snow-and-passes, food-trails, festivals, photography, long-weekends, off-season

## Cross-references
Every slug you reference (places, stays, festivals in `events`, journey stops, nearby) must exist in your own land's
files, except route ends, which may be any place in `_plan.json`. Run
`python tools/check_region.py <land>` until it prints OK, then `python tools/check_region.py <land> --wiki`.
