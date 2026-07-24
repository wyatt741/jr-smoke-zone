#!/usr/bin/env python3
"""JR Smoke Zone - static site generator (Camarillo, CA smoke & vape shop).
Run:  python3 build.py   (emits index/products/visit + sitemap/robots)
Edit CONTENT here, never hand-edit the generated HTML. Deploy = git push.

Follows the site-template recipe (../site-template/PLAYBOOK.md): one generator,
cache-busted assets, dark default + theme toggle, IntersectionObserver reveal
motion, glass nav. Themed black/blue/gray from the owner's logo (--blue #67ade8
sampled from the scorpion artwork). Products page uses Pexels stock photography;
the home 'From the shop' gallery uses the shop's own Instagram photos (see LICENSES.md).

Non-negotiables baked in: 21+ age gate (age_gate() + app.js), FDA nicotine
warning in the footer, NO fabricated ratings/reviews/stats (real Yelp rating
is mixed), not e-commerce (CTAs are Visit / Directions / Call).

Business facts verified from Yelp 2026-07-23. Placeholders marked TODO below.
"""

import json

# ---- cache-busting (bump on any css/js change) ----
CSSV = "styles.css?v=33"
JSV  = "app.js?v=1"
CHATV= "chat.js?v=15"

# ---- dark-mode default + no-FOUC theme + age-gate state (runs before paint) ----
BOOT = ('<script>(function(){try{'
        'var t=localStorage.getItem("theme")||"dark";'
        'document.documentElement.setAttribute("data-theme",t);'
        'if(localStorage.getItem("age21")==="1")document.documentElement.setAttribute("data-age","ok");'
        '}catch(e){}})();</script>')
SUN    = '<svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M2 12h2.4M19.6 12H22M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>'
MOON   = '<svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/></svg>'
TOGGLE = f'<button class="theme-toggle" type="button" aria-label="Toggle dark mode" title="Toggle theme">{SUN}{MOON}</button>'

# brand art, both TRANSPARENT-background cutouts of the owner's logo (no black square):
#   MARK = scorpion only        -> nav/footer (text would be illegible at that size), favicon
#   LOGO = full logo + arched "JR. Smoke Zone" lettering -> hero + age gate
# favicons cache HARD - bump ICOV and close the tab to see a change (playbook §5/§10)
ICOV = "?v=2"
MARK = "assets/mark.png"
LOGO = "assets/logo.png"

# ---- ultra-light line icons (no emoji - premium feel per high-end-visual-design) ----
def _svg(p):
    return f'<svg class="ic-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
ICON = {
 # product categories
 "vape":   _svg('<path d="M9 3h6M11 3v3M13 3v3"/><rect x="7" y="6" width="10" height="15" rx="3"/><path d="M10 11h4"/>'),
 "hookah": _svg('<path d="M12 3v6M9 6h6"/><path d="M8 9h8l-1.2 4.2a2.9 2.9 0 0 1-5.6 0z"/><path d="M12 16v3M8.5 21h7"/>'),
 "pipe":   _svg('<circle cx="7" cy="15" r="4"/><path d="M9.8 12.3 20 5.5"/>'),
 "bong":   _svg('<path d="M10 3h4v4l3.2 6.4a4 4 0 0 1-3.6 5.8H10.4a4 4 0 0 1-3.6-5.8L10 7z"/><path d="M9 8h6"/>'),
 "cigar":  _svg('<rect x="3" y="10" width="15" height="4" rx="2"/><path d="M18 11.2l2.2-1M18 12.8l2.2 1"/>'),
 "gear":   _svg('<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.2 5.2l2.1 2.1M16.7 16.7l2.1 2.1M18.8 5.2l-2.1 2.1M7.3 16.7l-2.1 2.1"/>'),
 "pouch":  _svg('<ellipse cx="12" cy="8" rx="7.5" ry="3.2"/><path d="M4.5 8v5.6c0 1.77 3.36 3.2 7.5 3.2s7.5-1.43 7.5-3.2V8"/><path d="M9.4 8.2h5.2"/>'),
 # amenities / why-visit
 "pin":    _svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.5"/>'),
 "store":  _svg('<path d="M3 9l1.2-5h15.6L21 9M4.5 9v11h15V9M4.5 9h15M9 20v-6h6v6"/>'),
 "spark":  _svg('<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>'),
 "people": _svg('<circle cx="9" cy="8" r="3"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0M15.5 5.6a3 3 0 0 1 0 5.8M20.5 20a5.5 5.5 0 0 0-3.2-5"/>'),
 "clock":  _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/>'),
 "card":   _svg('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h4"/>'),
 "wheel":  _svg('<circle cx="13" cy="4.2" r="1.7"/><path d="M13 6v6h5l2.2 5M13 12a5.2 5.2 0 1 0 4.4 8"/>'),
 "bike":   _svg('<circle cx="6" cy="16.5" r="3.5"/><circle cx="18" cy="16.5" r="3.5"/><path d="M6 16.5l4-8h5.5l-2.5 8M9.5 8.5H13"/>'),
 "phone":  _svg('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
 "route":  _svg('<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H15a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h6.5"/>'),
 "papers": _svg('<rect x="3.5" y="2.5" width="11" height="15" rx="2"/><path d="M7 6.5h4M7 10h4"/><path d="M7.5 21.5h11a2 2 0 0 0 2-2V7.5"/>'),
 "shirt":  _svg('<path d="M20.4 3.5 16 2a4 4 0 0 1-8 0L3.6 3.5a2 2 0 0 0-1.3 2.2l.6 3.5a1 1 0 0 0 1 .8H6v10a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V10h2.1a1 1 0 0 0 1-.8l.6-3.5a2 2 0 0 0-1.3-2.2z"/>'),
 "ig":     _svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1"/>'),
 "star":   _svg('<path d="M12 3l2.5 5.9 6.4.5-4.9 4.2 1.5 6.2L12 16.9 6.5 20l1.5-6.2L3 9.6l6.4-.5z"/>'),
 "heart":  _svg('<path d="M20.8 5.6a5.5 5.5 0 0 0-7.8 0L12 6.5l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.6z"/>'),
}
def icon(name): return ICON.get(name, "")

# ---- business facts (verified from Yelp 2026-07-23; do NOT fabricate anything else) ----
BIZ    = "JR Smoke Zone"
TAG    = "Camarillo's neighborhood smoke shop"   # share-link/title voice ("vape" assumed); product keywords stay in the meta description + schema
CITY   = "Camarillo, CA"
ADDR   = "2616 Ventura Blvd, Camarillo, CA 93010"
IG     = "https://www.instagram.com/jrsmokezone/"
# Google review deep link - opens the star form for THIS place. Place ID verified 2026-07-24
# (CID 0xa4341324cf2de8bd resolves to JR Smoke Zone; QR on the checkout card decodes to this).
REVIEW = "https://search.google.com/local/writereview?placeid=ChIJ1zLRvUY36IARvegtzyQTNKQ"
DOMAIN = "jrsmokezone.com"        # registered on Cloudflare 2026-07-23; DNS -> GitHub Pages
BASE   = f"https://{DOMAIN}"      # absolute origin for canonical / og / schema URLs
OG_IMG = f"{BASE}/assets/og.png"  # 1200x630 social share card (generated in build.py sibling script)
GEO    = (34.2160488, -119.0352246)  # 2616 Ventura Blvd, verified via OSM Nominatim 2026-07-24
MAPS   = "https://www.google.com/maps/search/?api=1&query=" + ADDR.replace(" ", "+").replace(",", "%2C")
MAP_EMBED = "https://www.google.com/maps?q=" + ADDR.replace(" ", "+").replace(",", "%2C") + "&output=embed"

# canonical URL per page (body-class key -> absolute URL). Home canonicals to the bare
# domain, not /index.html, so GitHub Pages' "/" and "/index.html" don't split ranking.
CANON = {"home": f"{BASE}/", "products": f"{BASE}/products.html", "visit": f"{BASE}/contact.html"}

def local_business_ld():
    """LocalBusiness (Store) JSON-LD for local SEO - Google rich results / Maps.
    All facts verified (address, phone, hours, geo); NO ratings/reviews (non-negotiable)."""
    hrs = [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
            "opens": "09:00", "closes": "21:00"},
           {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday",
            "opens": "10:00", "closes": "20:00"}]
    data = {
        "@context": "https://schema.org",
        "@type": "Store",
        "@id": f"{BASE}/#store",
        "name": BIZ,
        "description": "Locally owned smoke and vape shop in Camarillo, CA - vapes, e-liquid, hookah, glass pipes, bongs, cigars, and accessories.",
        "url": f"{BASE}/",
        "telephone": PHONE_TEL,
        "image": OG_IMG,
        "logo": f"{BASE}/{LOGO}",
        "priceRange": "$",
        "address": {"@type": "PostalAddress", "streetAddress": "2616 Ventura Blvd",
                    "addressLocality": "Camarillo", "addressRegion": "CA",
                    "postalCode": "93010", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "hasMap": MAPS,
        "openingHoursSpecification": hrs,
        "sameAs": [IG],
    }
    return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":")) + '</script>'

# ---- contact ----
PHONE     = "(805) 384-5115"                         # verified real number
PHONE_TEL = "+18053845115"
# Cloudflare Worker URL for the AI chat bot (worker/). EMPTY = bot uses its free
# deterministic answers. Set to the deployed Worker URL to switch on Claude-backed AI.
WORKER    = "https://chat.jrsmokezone.com"   # AI bot live on branded custom domain (2026-07-24)
EMAIL     = "jrsmokezone@gmail.com"                  # real shop inbox (owner-supplied)
# FormSubmit endpoint MUST stay lowercase (playbook §7 - changing the case forces
# re-activation). The FIRST submission triggers a one-time activation email that the
# owner has to click before any message actually gets delivered.
FORM_TO   = EMAIL

# hours: (day-label, hours). Real, from Yelp.
HOURS = [("Mon", "9am - 9pm"), ("Tue", "9am - 9pm"), ("Wed", "9am - 9pm"),
         ("Thu", "9am - 9pm"), ("Fri", "9am - 9pm"), ("Sat", "9am - 9pm"),
         ("Sun", "10am - 8pm")]

def hour_rows(hours):
    """Collapse consecutive days sharing the same hours into ranges: Mon-Sat 9am-9pm.
    Generic, so changing HOURS above re-groups automatically (no hardcoded ranges)."""
    runs = []
    for day, hrs in hours:
        if runs and runs[-1][2] == hrs:
            runs[-1][1] = day                     # extend the current run
        else:
            runs.append([day, day, hrs])          # start a new run
    return [(a if a == b else f"{a}-{b}", h) for a, b, h in runs]

# self-check: the smallest thing that fails if the grouping logic breaks
assert hour_rows(HOURS) == [("Mon-Sat", "9am - 9pm"), ("Sun", "10am - 8pm")]
assert hour_rows([("Mon", "9-5")]) == [("Mon", "9-5")]                       # single day
assert hour_rows([("Mon", "9-5"), ("Tue", "9-6")]) == [("Mon", "9-5"), ("Tue", "9-6")]  # no run
assert hour_rows([("Mon", "9-5"), ("Tue", "9-6"), ("Wed", "9-6")]) == \
       [("Mon", "9-5"), ("Tue-Wed", "9-6")]                                  # run at the end

HOUR_ROWS   = hour_rows(HOURS)
HOURS_SHORT = " · ".join(f"{d} {h.replace(' - ', '-')}" for d, h in HOUR_ROWS)

# product categories - all from their REAL Yelp list, no invented brands.
# (icon, title, short[home], long[products page], items[generic product types, not brands])
PRODUCTS = [
 ("vape",  "Vapes & E-Liquid", "assets/products/vape.jpg",
  "Devices, pods, disposables, and e-liquid.",
  "Vape devices, pods, disposables, and e-liquid. New to it or dialing in a setup, the staff will point you the right way toward what California lets us carry.",
  ["Vape devices & pods", "Disposables", "E-liquid & salts", "Coils & pods"]),
 ("pouch", "Nicotine Pouches", "assets/products/pouches.jpg",
  "Tobacco-free pouches like Zyn.",
  "Tobacco-free nicotine pouches that tuck under the lip, like Zyn. California restricts flavored pouches, so we carry the forms the state allows. Call or text and the staff will say what's in stock.",
  ["Tobacco-free", "Like Zyn", "CA-allowed forms", "Ask about strengths"]),
 ("hookah", "Hookah", "assets/products/hookah.jpg",
  "Hookahs, shisha, and everything for the session.",
  "Full hookah setups and the shisha, hoses, bowls, and coals to go with them. Grab a whole kit or just restock the essentials.",
  ["Hookahs & kits", "Shisha / flavored tobacco", "Bowls & hoses", "Coals & accessories"]),
 ("pipe", "Glass Pipes", "assets/products/pipe.jpg",
  "A deep glass selection - the thing folks come back for.",
  "The glass wall is what regulars rave about. Hand pipes and glass in a range of styles and price points, from simple daily pieces to standout ones.",
  ["Hand pipes", "Chillums & one-hitters", "Colored & worked glass", "Everyday to premium"]),
 ("bong", "Bongs & Water Pipes", "assets/products/bong.jpg",
  "Water pipes, beakers, rigs, and the parts to run them.",
  "Water pipes and rigs in glass and silicone, plus bowls, downstems, and the small parts that always seem to go missing.",
  ["Beakers & straight tubes", "Rigs", "Bowls & downstems", "Silicone & glass"]),
 ("cigar", "Cigars", "assets/products/cigar.jpg",
  "Cigars and the smoking accessories to match.",
  "Cigars for the casual smoker and the aficionado, plus cutters, lighters, and the extras that round out the ritual.",
  ["Singles & selection", "Cutters & lighters", "Ashtrays", "Humidor accessories"]),
 ("papers", "Rolling Papers & Trays", "assets/products/papers.jpg",
  "Papers, wraps, tips, and trays to keep it tidy.",
  "Rolling papers, wraps, tips, and trays, including the names people ask for by heart like RAW and Zig-Zag, plus the grinders that go with them.",
  ["Papers & wraps", "Tips & filters", "Rolling trays", "Grinders"]),
 ("gear", "Vape Accessories", "assets/products/gear.jpg",
  "Chargers, coils, grinders, trays, and all the extras.",
  "The catch-all wall: chargers, coils, grinders, trays, storage, cleaning supplies, and the odds and ends that keep everything running.",
  ["Chargers & batteries", "Grinders & trays", "Storage & cleaning", "Odds & ends"]),
 ("shirt", "Apparel & Merch", "assets/products/apparel.jpg",
  "Shirts, hats, and shop merch.",
  "Shop apparel and merch, plus the occasional drop from the brands we carry. Ask what is on the rack.",
  ["Tees & hoodies", "Hats", "Brand merch", "Shop drops"]),
]

# why-visit features - grounded in REAL Yelp review sentiment (helpful/patient staff,
# glass selection) and verified facts. NO ratings, NO star claims, NO quoted reviews.
FEATURES = [
 ("store",  "Locally owned",
  "A real neighborhood shop on Ventura Blvd, not a faceless chain or an online middleman."),
 ("spark",  "Deep glass selection",
  "Regulars single out the glass wall - a genuine range to actually pick from in person."),
 ("people", "Helpful, patient staff",
  "Ask anything. The team's happy to walk you through options whether you're new or know exactly what you want."),
 ("gear",   "Everything in one spot",
  "Vapes, hookah, glass, cigars, and accessories under one roof - one stop instead of five."),
]

# amenities (verified from Yelp)
AMENITIES = [("wheel", "Wheelchair accessible"), ("card", "Accepts credit cards"),
             ("bike", "Bike parking")]

# brands the shop carries (from their own IG posts). Elf Bar (flavored disposables) pulled
# 2026-07-24 for California compliance: flavored vapes/disposables are illegal to sell at
# retail in CA (SB 793), so we don't advertise them. Papers/dab brands are unaffected.
BRANDS = ["Puffco", "Zig-Zag", "RAW"]

# REAL public shout-out from a local business (IG post 2026-05-22), trimmed excerpt.
# Not a customer review and not a rating - attributed + linked to the source post.
SHOUTOUT = {"text": "Had to stop by and show love at the best smoke shop in the 805. "
                    "The owner of that spot is rad! Good people.",
            "who": "Beachside Motorsports", "handle": "@beachsidemotorsportsllc",
            "post": "DYpgJ-AFIMM"}

# real Instagram posts (@jrsmokezone), images downloaded to assets/ig/. (code, caption)
# Mix of real interior shots + branded promos + community events, pulled 2026-07-23.
GALLERY = [
 ("Cj6NQc6goUQ", "Inside the shop"),
 ("DQXqPwjEghY", "On the floor"),
 ("DIfCAIIztcr", "4/20 deals"),
 ("DR0OKh2Eupc", "Holiday giveaway"),
 ("DSG21OwES8q", "In-store toy drive"),
 ("DXQFTVrj8Bo", "4/20 celebration"),
]
IG_POST = "https://www.instagram.com/p/{}/"

NAV = [("index.html", "Home"), ("products.html", "Products")]

# ============================ SHARED CHROME ============================
def head(title, desc, page=""):
    canon = CANON.get(page, f"{BASE}/")
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{BIZ}"><meta property="og:image" content="{OG_IMG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMG}">
{local_business_ld()}
<meta name="theme-color" content="#0a0d13">
<link rel="icon" href="assets/favicon.ico{ICOV}" sizes="any">
<link rel="icon" type="image/png" href="assets/favicon.png{ICOV}">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png{ICOV}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{CSSV}">
{BOOT}
</head><body class="{page}">
{age_gate()}
<a class="skip" href="#main">Skip to content</a>'''

def brandmark(cls="", badge=False):
    # badge=True -> the full logo (scorpion + arched "JR. Smoke Zone") on a fixed-dark tile
    # so the logo's white lettering stays legible on the light-theme nav too. The wordmark
    # text is kept because the badge lettering is decorative-small at nav size.
    emblem = (f'<span class="brand-badge"><img class="brand-ic" src="{LOGO}" alt="" width="46" height="46"></span>'
              if badge else
              f'<img class="brand-ic" src="{MARK}" alt="" width="40" height="40">')
    return (f'<a class="brand {cls}" href="index.html" aria-label="{BIZ} home">'
            f'{emblem}'
            f'<span class="wordmark"><span class="wm-jr">JR</span> Smoke Zone</span></a>')

def nav(active):
    links = "".join(
        f'<a href="{h}"{" class=\"active\"" if h==active else ""}>{t}</a>' for h, t in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f'''<div class="nav-shell"><header class="nav"><div class="nav-in">
  {brandmark(badge=True)}
  <nav class="nav-links">{links}</nav>
  {TOGGLE}
  <a class="btn btn-primary btn-sm nav-cta cta-anim" href="contact.html">Contact Us<span class="btn-ic">&rarr;</span></a>
  <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header></div>
<div class="mobile-menu" id="mobile-menu">{mlinks}<a class="btn btn-primary cta-anim" href="contact.html">Contact Us<span class="btn-ic">&rarr;</span></a>{TOGGLE}</div>'''

def age_gate():
    # 21+ splash. Shown before paint unless localStorage age21=1 (set in BOOT -> data-age="ok").
    # "Yes" persists + reveals; "No" leaves the site. Wired in app.js.
    return f'''<div class="agegate" id="agegate" role="dialog" aria-modal="true" aria-labelledby="ag-title">
  <div class="ag-card">
    <img class="ag-logo" src="{LOGO}" alt="{BIZ}" width="190" height="190">
    <h2 id="ag-title">Are you 21 or older?</h2>
    <p>You must be at least 21 years of age to enter this site. Tobacco and vapor products are for adults 21+ only.</p>
    <div class="ag-btns">
      <button class="btn btn-primary btn-lg" id="ag-yes" type="button">Yes, I'm 21+</button>
      <button class="btn btn-ghost btn-lg" id="ag-no" type="button">No</button>
    </div>
    <p class="ag-fine">By entering you confirm you are of legal age to purchase tobacco and vapor products in California.</p>
  </div>
</div>'''

def chat_data():
    """Feed the assistant the SAME constants the pages render, so it can never drift
    from the site or invent a fact. No API key, no backend - see chat.js."""
    d = {"biz": BIZ, "addr": ADDR, "phone": PHONE, "tel": PHONE_TEL, "email": EMAIL,
         "maps": MAPS, "ig": IG, "review": REVIEW, "worker": WORKER, "hoursShort": HOURS_SHORT,
         "days": [{"d": a, "h": b} for a, b in HOURS],        # Mon..Sun, for "open now?"
         "hours": [{"d": a, "h": b} for a, b in HOUR_ROWS],   # grouped, for display
         "products": [{"id": p[0], "title": p[1], "short": p[3]} for p in PRODUCTS],
         "brands": BRANDS, "amenities": [t for _, t in AMENITIES]}
    return f"<script>window.JRZ={json.dumps(d, ensure_ascii=False)};</script>"

def chat_widget():
    # Deterministic assistant: answers only from window.JRZ (real data). It never quotes
    # prices or claims stock - those route to a phone call. No LLM, no key, no backend.
    return f'''<div class="cw" id="cw">
  <button class="cw-bubble" id="cw-bubble" type="button" aria-label="Ask a question" aria-expanded="false" aria-controls="cw-panel">
    <svg class="cw-i cw-i-chat" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5Z"/></svg>
    <svg class="cw-i cw-i-x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
  </button>
  <div class="cw-nudge" id="cw-nudge" hidden>
    <button class="cw-nudge-open" type="button" data-open-chat>Questions? I can help.</button>
    <button class="cw-nudge-x" id="cw-nudge-x" type="button" aria-label="Dismiss">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  </div>
  <div class="cw-panel" id="cw-panel" role="dialog" aria-labelledby="cw-title" hidden>
    <div class="cw-head">
      <img class="cw-avatar" src="{MARK}" alt="" width="34" height="34">
      <div class="cw-head-t"><strong id="cw-title">{BIZ}</strong>
        <span><span class="cw-dot"></span>Hours, directions, what we carry</span></div>
      <button class="cw-x" id="cw-close" type="button" aria-label="Close chat">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
    <div class="cw-log" id="cw-log" role="log" aria-live="polite" aria-label="Chat messages"></div>
    <form class="cw-form" id="cw-form" autocomplete="off">
      <label class="sr-only" for="cw-input">Type your question</label>
      <input id="cw-input" class="cw-input" type="text" placeholder="Ask a question..." maxlength="300" autocomplete="off">
      <button class="cw-send" type="submit" aria-label="Send">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </form>
    <p class="cw-note">Automated assistant. For prices or stock, call the shop. 21+ only.</p>
  </div>
</div>'''

def visit_cta():
    return f'''<section class="cta-band"><div class="wrap"><div class="cta-card reveal">
  <div class="cta-copy">
    <span class="eyebrow eyebrow-light">Come see us</span>
    <h2>Swing by the shop.</h2>
    <p><a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a><br>Open {HOURS_SHORT}<br>Questions? Call or text <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
  </div>
  <div class="cta-btns">
    <a class="btn btn-glow btn-lg cta-anim" href="{MAPS}" target="_blank" rel="noopener">Get directions<span class="btn-ic">&rarr;</span></a>
    <a class="btn btn-ghost-light btn-lg" href="tel:{PHONE_TEL}">Call the shop</a>
  </div>
</div></div></section>'''

def footer():
    cols = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV) + '<a href="contact.html">Contact</a>'
    return f'''<footer>
<div class="wrap warn-bar">
  <strong>WARNING:</strong> This product contains nicotine. Nicotine is an addictive chemical.
  <span class="warn-age">Must be 21+ to purchase.</span>
</div>
<div class="wrap foot-grid">
  <div class="foot-brand">
    {brandmark("brand-foot", badge=True)}
    <p>Glass, vapes, hookah, cigars, and every accessory to match. On Ventura Blvd in {CITY.split(",")[0]}.</p>
    <div class="foot-social">
      <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">Instagram</a>
      <a href="{REVIEW}" target="_blank" rel="noopener" aria-label="Review us on Google">Review us on Google</a>
    </div>
  </div>
  <div class="foot-col"><h5>Explore</h5>{cols}</div>
  <div class="foot-col"><h5>Find us</h5>
    <a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a>
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <span class="foot-note">{HOURS_SHORT}</span>
  </div>
</div>
<div class="legal wrap">
  <span>&copy; 2026 {BIZ}. All rights reserved.</span>
  <span>Not for sale to minors. 21+ only.</span>
</div>
</footer>
{chat_widget()}
{chat_data()}
<script src="{JSV}"></script>
<script src="{CHATV}"></script></body></html>'''

# ============================ PAGES ============================
def home():
    # double-bezel: outer shell (.bezel) + inner core (.bezel-in), concentric radii.
    # uniform 4-up grid (8 tiles = 2 even rows) - no oversized hero tile
    prods = "".join(
        f'''<a class="svc bezel" href="products.html#{p[0]}"><span class="bezel-in svc-in">
        <span class="ic-badge">{icon(p[0])}</span>
        <span class="svc-copy"><h3>{p[1]}</h3><p>{p[3]}</p>
        <span class="svc-more">See more<span class="btn-ic">&rarr;</span></span></span></span></a>'''
        for p in PRODUCTS)
    feats = "".join(
        f'<div class="feat bezel"><div class="bezel-in feat-in"><span class="ic-badge">{icon(k)}</span><h3>{t}</h3><p>{d}</p></div></div>'
        for k, t, d in FEATURES)
    # marquee: product keywords + real carried brands, rendered twice for a seamless loop
    chips = ["Vapes", "E-Liquid", "Disposables", "Hookah", "Shisha", "Glass Pipes",
             "Bongs", "Puffco", "Zig-Zag", "RAW", "Cigars", "Grinders", "Accessories"]
    row = "".join(f'<span class="mq-chip">{c}</span>' for c in chips)
    marquee = row + row
    igtiles = "".join(
        f'''<a class="ig-tile bezel" href="{IG_POST.format(code)}" target="_blank" rel="noopener">
        <span class="bezel-in ig-in">
        <img src="assets/ig/{code}.jpg" alt="{label} at {BIZ}" loading="lazy">
        <span class="ig-cap">{label}{icon("ig")}</span></span></a>''' for code, label in GALLERY)
    return head(f"{BIZ} | {TAG}",
        f"Locally owned smoke & vape shop in {CITY}. Vapes, e-liquid, hookah, glass pipes, bongs, cigars, and accessories. Come visit us on Ventura Blvd.",
        "home") + nav("index.html") + f'''
<main id="main">
<section class="hero"><div class="wrap hero-in">
  <div class="hero-copy reveal">
    <span class="eyebrow"><span class="dot"></span>Locally owned · {CITY}</span>
    <h1>Your neighborhood <span class="hl">smoke shop</span></h1>
    <div class="hero-visit">
      <p class="hv-lead">Swing by the shop.</p>
      <address class="hv-addr"><a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a></address>
      <p class="hv-hours"><span class="hc-dot"></span>Open {HOURS_SHORT}</p>
      <p class="hv-ask">Questions? <a href="#" data-open-chat>Ask our assistant</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
    </div>
    <div class="hero-btns">
      <a class="btn btn-primary btn-lg cta-anim" href="{MAPS}" target="_blank" rel="noopener">Get directions<span class="btn-ic">&rarr;</span></a>
      <a class="btn btn-ghost btn-lg" href="products.html">Browse products</a>
    </div>
  </div>
  <aside class="hero-logo reveal d1">
    <img class="hero-mark" src="{LOGO}" alt="{BIZ}" width="480" height="480">
  </aside>
</div></section>

<section class="marquee-sec"><div class="wrap marquee-in">
  <span class="marquee-label">In store</span>
  <div class="marquee"><div class="marquee-track">{marquee}</div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">What we carry</span>
    <h2>One shop, all of it</h2>
    <p>From a fresh coil to a standout piece of glass, it's on the wall in {CITY.split(",")[0]}.</p></div>
  <div class="bento stagger reveal">{prods}</div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Why visit us</span><h2>A local shop that does it right</h2></div>
  <div class="feat-grid stagger reveal">{feats}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">From the shop</span><h2>Straight off the feed</h2>
    <p>Real shots from inside the store, plus the deals, giveaways, and events we run for the neighborhood.</p></div>
  <div class="ig-grid stagger reveal">{igtiles}</div>
  <div class="center" style="margin-top:34px"><a class="btn btn-primary btn-lg cta-anim" href="{IG}" target="_blank" rel="noopener">Follow &#64;jrsmokezone{icon("ig")}</a></div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">More than a smoke shop</span><h2>Part of the neighborhood</h2>
    <p>JR Smoke Zone runs in-store toy drives, 4/20 events, and giveaways with local businesses, right next to our sister store JR Liquor Mart on Ventura Blvd.</p></div>
  <figure class="shout bezel reveal"><div class="bezel-in shout-in">
    <blockquote>&ldquo;{SHOUTOUT["text"]}&rdquo;</blockquote>
    <figcaption>
      <span class="shout-who">{SHOUTOUT["who"]}</span>
      <a href="{IG_POST.format(SHOUTOUT["post"])}" target="_blank" rel="noopener">{SHOUTOUT["handle"]}{icon("ig")}</a>
    </figcaption>
  </div></figure>
</div></section>
</main>
{visit_cta()}{footer()}'''

def products():
    # 2-up card grid: photo on top, then icon + title + copy + bullets. No per-card CTA
    # (one closing band covers it). id on each card so home's "See more" links land here.
    cards = "".join(
        f'''<article class="prod-card bezel reveal" id="{ic}"><div class="bezel-in">
        <div class="prod-photo"><img src="{photo}" alt="{title} at {BIZ}" width="900" height="720"></div>
        <div class="prod-body">
          <div class="prod-head"><span class="ic-badge">{icon(ic)}</span><h2>{title}</h2></div>
          <p>{long}</p><ul class="ticks">{"".join(f"<li>{x}</li>" for x in items)}</ul>
        </div></div></article>'''
        for ic, title, photo, short, long, items in PRODUCTS)
    return head(f"Products | {BIZ}",
        f"Vapes and e-liquid, hookah, glass pipes, bongs, cigars, and accessories at {BIZ} in {CITY}.",
        "products") + nav("products.html") + f'''
<main id="main">
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Products</span><h1>What's on the wall</h1>
  <p>A deep glass wall, vapes and e-liquid, hookah, cigars, and every accessory to match. Come see the whole wall in person, it's better in your hands than on a screen.</p>
</div></section>
<section class="section" style="padding-top:40px"><div class="wrap">
  <div class="prod-grid stagger reveal">{cards}</div>
</div></section>
</main>{visit_cta()}{footer()}'''

def visit():
    hrows = "".join(f'<div class="hr-row"><span>{d}</span><strong>{h}</strong></div>' for d, h in HOUR_ROWS)
    amen = "".join(f'<span class="amen"><span class="amen-ic">{icon(k)}</span>{t}</span>' for k, t in AMENITIES)
    return head(f"Contact | {BIZ}",
        f"Contact {BIZ} at {ADDR}. Hours, directions, phone, and a message form.",
        "visit") + nav("contact.html") + f'''
<main id="main">
<section class="page-hero"><div class="wrap reveal">
  <span class="eyebrow">Contact us</span><h1>Swing by the shop.</h1>
  <p><a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a><br>Open {HOURS_SHORT}<br>Questions? Call or text <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
</div></section>

<section class="section" style="padding-top:32px"><div class="wrap visit-in">
  <div class="visit-info reveal">
    <div class="vcard bezel"><div class="bezel-in vcard-in">
      <span class="ic-badge">{icon("pin")}</span>
      <h3>Address</h3>
      <p><a class="addr-link" href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a></p>
      <a class="btn btn-primary cta-anim" href="{MAPS}" target="_blank" rel="noopener">Get directions<span class="btn-ic">&rarr;</span></a>
    </div></div>
    <div class="vcard bezel"><div class="bezel-in vcard-in">
      <span class="ic-badge">{icon("clock")}</span>
      <h3>Hours</h3>
      <div class="hours">{hrows}</div>
    </div></div>
    <div class="vcard bezel"><div class="bezel-in vcard-in">
      <span class="ic-badge">{icon("phone")}</span>
      <h3>Call or text</h3>
      <a class="big-phone" href="tel:{PHONE_TEL}">{PHONE}</a>
      <div class="ct-btns">
        <a class="btn btn-primary btn-sm cta-anim" href="tel:{PHONE_TEL}">Call<span class="btn-ic">&rarr;</span></a>
        <a class="btn btn-ghost btn-sm" href="sms:{PHONE_TEL}">Text us</a>
      </div>
      <a class="v-mail" href="mailto:{EMAIL}">{EMAIL}</a>
    </div></div>
    <div class="vcard bezel"><div class="bezel-in vcard-in">
      <span class="ic-badge">{icon("store")}</span>
      <h3>Good to know</h3>
      <div class="amenities">{amen}</div>
      <a class="v-ig" href="{IG}" target="_blank" rel="noopener">Follow on Instagram &rarr;</a>
      <a class="v-review" href="{REVIEW}" target="_blank" rel="noopener">{icon("star")}Review us on Google</a>
    </div></div>
  </div>

  <aside class="visit-form reveal d1">
    <h3>Send us a message</h3>
    <p>Got a question about a product or hours? Drop us a line.</p>
    <form class="cform" action="https://formsubmit.co/{FORM_TO}" method="POST">
      <input type="hidden" name="_subject" value="New message from the JR Smoke Zone website">
      <input type="hidden" name="_template" value="table">
      <input type="text" name="_honey" style="display:none">
      <label>Name<input name="name" required></label>
      <label>Email<input name="email" type="email" required></label>
      <label>Message<textarea name="message" rows="5" placeholder="Your question..."></textarea></label>
      <button class="btn btn-primary btn-lg" type="submit">Send<span class="btn-ic">&rarr;</span></button>
      <p class="form-fine">Prefer to talk? Call or text {PHONE}.</p>
    </form>
  </aside>
</div></section>

<section class="map-sec"><iframe src="{MAP_EMBED}" title="{BIZ} location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>
</main>{footer()}'''

# ============================ BUILD ============================
PAGES = {"index.html": home, "products.html": products, "contact.html": visit}

def sitemap():
    # loc must match each page's <link rel=canonical>: home = bare domain, not /index.html
    locs = [f"{BASE}/"] + [f"{BASE}/{p}" for p in PAGES if p != "index.html"]
    urls = "".join(f"<url><loc>{u}</loc></url>" for u in locs)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'

# the page moved visit.html -> contact.html; keep a redirect so old/shared links don't 404
REDIRECT_STUB = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                 f'<title>{BIZ}</title><link rel="canonical" href="{BASE}/contact.html">'
                 f'<meta http-equiv="refresh" content="0; url=/contact.html">'
                 f'<meta name="robots" content="noindex">'
                 f'<script>location.replace("/contact.html")</script></head>'
                 f'<body>Redirecting to <a href="/contact.html">Contact</a>.</body></html>')

def build():
    for fn, f in PAGES.items():
        with open(fn, "w", encoding="utf-8") as fh:
            fh.write(f())
    with open("visit.html", "w", encoding="utf-8") as fh:   # legacy URL -> contact.html
        fh.write(REDIRECT_STUB)
    with open("sitemap.xml", "w", encoding="utf-8") as fh:
        fh.write(sitemap())
    with open("robots.txt", "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    # GitHub Pages custom domain. One line, no scheme. Emitted here so `python3 build.py`
    # never drops it. DNS (A + www CNAME) lives at Cloudflare (added 2026-07-23).
    with open("CNAME", "w", encoding="utf-8") as fh:
        fh.write(f"{DOMAIN}\n")
    print("built:", ", ".join(PAGES), "+ sitemap.xml, robots.txt, CNAME")

if __name__ == "__main__":
    build()
