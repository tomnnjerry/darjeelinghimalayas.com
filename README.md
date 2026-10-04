# Darjeeling Himalayas (darjeelinghimalayas.com)

Django site for honest-priced, locally rooted trips in eight lands of the Darjeeling and Sikkim Himalaya and the
Dooars below them. Shared jeeps, the toy train, homestays, government lodges and trekkers' huts, priced for Indian
families, couples, students and backpackers rather than luxury travel. Every page is rendered from JSON in `content/`.
Photos come from Wikimedia Commons with author, licence and source link. Maps are drawn on the server as SVG from
Natural Earth outlines: no map API, no API key, no tiles.

Each land wears its own palette and gradient, set once in `hills/content.py → LANDS / GRADIENTS` and applied to any
element with `data-land` (styles in `static/css/hillcart.css`). Each land has its own drawn icon (`hills/icons.py`,
`{% icon "train" %}`). The home page's "Climb" orders the lands from the Dooars (≈ 120 m) to North Sikkim.

| Land | Slug | Palette |
|---|---|---|
| Darjeeling & Ghoom | `darjeeling` | Steam-engine blue and Kanchenjunga dawn |
| Kurseong, Mirik & the tea valleys | `kurseong-mirik` | Mirik lake teal and Sittong orange |
| Kalimpong, Lava & Lolegaon | `kalimpong` | Monastery maroon and orchid |
| Sandakphu & the Singalila Ridge | `singalila` | Rhododendron red and ridge slate |
| Gangtok & East Sikkim | `gangtok` | Tsomgo turquoise and prayer-flag yellow |
| North Sikkim: Lachung & Lachen | `north-sikkim` | Glacier ice and primula violet |
| Pelling, Yuksom & South Sikkim | `west-sikkim` | Butter-lamp ochre and cardamom green |
| The Dooars & Siliguri | `dooars` | Sal forest green and elephant-grass gold |

## Run it

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Enquiries, call-back requests and newsletter sign-ups land in the database: `/admin/` after `python manage.py createsuperuser`.

## Commands

```bash
python tools/check_region.py gangtok --wiki   # validate one land (counts, slugs, FAQs, banned words, Wikipedia titles)
python tools/check_journal.py                 # validate journal posts
python tools/fetch_images.py                  # credited Commons photos into content/images.json (incremental; --force; OVERRIDES for hand picks)
python tools/contact_sheet.py place: sheet.jpg  # contact sheet of lead photos, to eyeball the set
python tools/build_outlines.py                # rebuild map outlines (Natural Earth, India's view of borders)
python tools/smoke.py                         # render every URL in the sitemap (set DJANGO_DEBUG=0 for speed)
```

Pages render without photos until `tools/fetch_images.py` has been run (it needs network access to Wikipedia and
Commons and takes a while; it is incremental, so it can be stopped and resumed).

## Page types

| Page | URL | Source |
|---|---|---|
| Land hub / month / style / experience kind | `/hills/<land>/`, `…/seasons/<month>/`, `…/styles/<style>/`, `…/experiences/<kind>/` | `content/<land>/region.json` + generated |
| Place / experience | `/hills/<land>/<place>/`, `…/<place>/<experience>/` | `content/<land>/places/*.json` |
| Trip, stay, guide, festival, route | `/trips/…`, `/stays/…`, `/guides/…`, `/festivals/…`, `/routes/…` | `content/<land>/…` |
| Journal ("Stories from the hills") | `/journal/`, `/journal/<slug>/`, `/journal/topic/<topic>/` | `content/journal/*.json` |
| Styles, seasons | `/styles/…`, `/seasons/` | `content/themes.json` |
| Tools | `/tools/jeep-fares/`, `/tools/budget/`, `/tools/season-finder/`, `/tools/permits/`, `/tools/hill-words/` | templates + catalogue |
| Policies | `/policies/<slug>/` | `hills/policies.py` |
| Company | `/about/`, `/how-we-work/`, `/contact/`, `/faq/`, `/plan/` | templates |
| Utility | `/search.json`, `/sitemap.xml`, `/sitemap/`, `/robots.txt`, `/llms.txt`, `/photo-credits/` | |

Content rules: [content/SCHEMA.md](content/SCHEMA.md), [content/JOURNAL_SCHEMA.md](content/JOURNAL_SCHEMA.md).
Place slugs are fixed in [content/_plan.json](content/_plan.json).

## Conversion features

- Floating call-to-action on every page (plan online + contact menu) and a three-button dock on phones.
- Mega menus: lands in their own colours with top places, trips by style and length, experiences, planning.
- Site search (press `/`), loading a small JSON index on first use.
- Hero finder (land + month) that pre-fills the enquiry form.
- Three-step enquiry wizard with progress bar and contact preference; quick forms on trips, places and articles;
  call-back form on the contact page; newsletter in the footer.
- Sticky price-and-dates bar on trip pages; mid-article call-to-action on long reads.
- `dataLayer` events on every CTA click, form submit, wizard step, search and lead (`generate_lead`); set `DH_GA4` to load GA4.

## Before launch

1. Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=0`. Contact details default to `hello@darjeelinghimalayas.com`, +91 99546 34102
   and the same number on WhatsApp; override with `DH_EMAIL`, `DH_PHONE`, `DH_WHATSAPP` (digits with country code),
   `DH_ADDRESS` (shown in the footer and on About and Contact once set) and optional `DH_GA4`.
2. Fill the `[BRACKETED]` legal details in `hills/policies.py` (legal name, registered address, registration and GST
   numbers, courts' city, payment gateway). Add real founder and office details to `templates/hills/about.html` if wanted.
3. Have a lawyer review `hills/policies.py` (refunds, payments, booking terms, privacy under India's DPDP Act, cookies).
   If you enable GA4, add a consent banner and list its cookies in the cookie policy.
4. Review every region's `to_confirm` list, and re-check permits, road status (North Sikkim and the Teesta valley since
   the October 2023 flood), toy train services, park closures and fares close to launch.
5. Review prices in trip files and the planning ranges in `templates/hills/tool_budget.html`.
6. Run `python tools/fetch_images.py`, spot-check photos with `tools/contact_sheet.py`, pin better ones via `OVERRIDES`.
7. `python manage.py collectstatic`; serve with gunicorn behind HTTPS (`whitenoise` is used automatically if installed;
   set `DH_HASHED_STATIC=1` for hashed file names).
8. Submit `/sitemap.xml` to Google Search Console and Bing Webmaster Tools.
