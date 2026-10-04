# Tales of Luxury (talesofluxury.com)

Django site for a private luxury travel company working in seven lands: Nepal (Nº 01), Rajasthan (02), Ladakh (03),
North East India (04), Kerala (05), Goa (06) and UP & Bihar (07). About 1,050 pages, all rendered from JSON in
`content/`. Every photo comes from Wikimedia Commons with author, licence and source link. Maps are drawn on the server
as SVG from Natural Earth outlines: no map API, no API key, no tiles.

Design system: **The Folio** (Bodoni Moda + Archivo, arch photo frames, ledger rows, route ribbon, numbered tales).
Each land wears its own shiny gradient and metallic foil, set once in `tales/content.py → LANDS / GRADIENTS` and applied
to any element with `data-land` (styles in `static/css/folio-v3.css`). Each land also has its own drawn icon (`tales/icons.py`,
`{% icon "rajasthan" %}`). The site never shows inventory counts.

| Land | Palette | Ground | Accent |
|---|---|---|---|
| Nepal | Himalayan indigo and rhododendron | #1B2354 | #F27384 |
| Rajasthan | Pink City and saffron | #6A1B4D | #F4A23B |
| Ladakh | Pangong blue and prayer-flag yellow | #0E3B4C | #F2C230 |
| North East | Tea garden and orchid | #22381A | #E58BB6 |
| Kerala | Backwater green and kasavu gold | #06433A | #E2C27A |
| Goa | Azulejo blue and laterite | #0F3672 | #F99A72 |
| UP & Bihar | Ganga dusk and marigold | #4D1F08 | #F5A912 |

Design canvas: https://claude.ai/artifact/2eh7xmaj4DBRw4W97aaEqP

## Run it

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Enquiries, call-back requests and newsletter sign-ups land in the database: `/admin/` after `python manage.py createsuperuser`.

## Commands

```bash
python tools/check_region.py rajasthan --wiki   # validate one land (counts, slugs, FAQs, banned words, Wikipedia titles)
python tools/check_journal.py                    # validate Journal posts
python tools/fetch_images.py                     # credited Commons photos for new content (incremental; --force; OVERRIDES dict for hand picks)
python tools/contact_sheet.py place: sheet.jpg   # contact sheet of lead photos, to eyeball the set
python tools/build_outlines.py                   # rebuild map outlines (Natural Earth, India's view of borders)
python tools/smoke.py                            # render every URL in the sitemap (set DJANGO_DEBUG=0 for speed)
```

## Page types

| Page | URL | Source |
|---|---|---|
| Land hub / month / style / experience kind | `/lands/<land>/`, `…/seasons/<month>/`, `…/styles/<style>/`, `…/experiences/<kind>/` | `content/<land>/region.json` + generated |
| Place / experience | `/lands/<land>/<place>/`, `…/<place>/<experience>/` | `content/<land>/places/*.json` |
| Journey, stay, guide, festival, route | `/journeys/…`, `/stays/…`, `/guides/…`, `/festivals/…`, `/routes/…` | `content/<land>/…` |
| Journal (30 posts, by topic) | `/journal/`, `/journal/<slug>/`, `/journal/topic/<topic>/` | `content/journal/*.json` |
| Styles, seasons, tools | `/styles/…`, `/seasons/`, `/tools/…` | `content/themes.json` |
| Policies | `/policies/<slug>/` | `tales/policies.py` |
| Company | `/about/`, `/how-we-work/`, `/contact/`, `/faq/`, `/plan/` | templates |
| Utility | `/search.json`, `/sitemap.xml`, `/sitemap/`, `/robots.txt`, `/llms.txt`, `/photo-credits/` | |

Content rules: [content/SCHEMA.md](content/SCHEMA.md), [content/JOURNAL_SCHEMA.md](content/JOURNAL_SCHEMA.md).

## Conversion features

- Floating call-to-action on every page (plan online + contact menu) and a three-button dock on phones.
- Utility bar with phone, WhatsApp and email; "Plan my journey" button in the header.
- Mega menus: lands in their own colours with top places, journeys by style and length, experiences, planning.
- Site search (press `/`), loading a small JSON index on first use.
- Hero finder (land + month) that pre-fills the enquiry form.
- Three-step enquiry wizard with progress bar and contact preference; quick forms on journeys, places, articles and the
  footer band; call-back form on the contact page; newsletter in the footer.
- Sticky price-and-dates bar on journey pages; mid-article call-to-action and a once-per-visit planning prompt on long reads.
- Trust strip (no payment to start, itemised quote, one planner, change anything) and full policy set.
- `dataLayer` events on every CTA click, form submit, wizard step, search and lead (`generate_lead`); set `TOL_GA4` to load GA4.

## Before launch

1. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `TOL_EMAIL`, `TOL_PHONE`, `TOL_WHATSAPP` (digits with country code), optional `TOL_GA4`.
   Phone and WhatsApp buttons appear automatically once these are set.
2. Replace every `[BRACKETED]` placeholder: `tol/settings.py → SITE`, `templates/tales/about.html`, `contact.html`,
   the footer trust row in `base.html`, and all values in `tales/policies.py`.
3. Have a lawyer review `tales/policies.py` (refunds, payments, booking terms, privacy under India's DPDP Act, cookies).
   If you enable GA4, add a consent banner and list its cookies in the cookie policy.
4. Confirm service promises match how you work ("replies within one working day", "one planner", "no payment to start").
5. Review prices in journey files and the planning ranges in `templates/tales/tool_budget.html`.
6. Spot-check photos with `tools/contact_sheet.py`; pin better ones via `OVERRIDES` in `tools/fetch_images.py`.
7. `python manage.py collectstatic`; serve with gunicorn behind HTTPS (`whitenoise` is used automatically if installed).
8. Submit `/sitemap.xml` to Google Search Console and Bing Webmaster Tools.
