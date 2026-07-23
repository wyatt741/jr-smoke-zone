# JR Smoke Zone — website kickoff prompt

> Paste everything below the line as the FIRST message in a new session dedicated to
> this project (working dir `~/Documents/Claude/jr-smoke-zone/`). It's self-contained:
> template decision first, then every verified business fact, then the guardrails.

---

Build a marketing website for **JR Smoke Zone**, a locally owned smoke & vape shop in
Camarillo, CA. This is a **demo I'll show the owner** (a friend of mine) to win the job —
the walk-in-with-a-finished-demo play. It is a local-presence / "come visit us" brochure
site, **not e-commerce** (age + payment-processor rules make online vape sales impractical).

## STEP 1 — pick the template/approach FIRST, before writing anything

Decide and tell me the plan before building. Options:

- **Option A (recommended): clone my proven `bwraps` / `anderson-it` generator.** One
  `build.py` emits static HTML/CSS/JS — dark-mode default, glass nav, contact form,
  IntersectionObserver reveal motion, cache-busted assets. It's already dark and
  product-grid shaped, and a **partial port already exists in this folder** (see "Current
  state" below). Reskinned graphite + neon-green.
- **Option B: adopt an HTML5 UP template** from `~/Documents/Claude/html5up-templates/`.
  Best dark fits for a smoke shop: **Dimension** (dark, minimal, premium modal one-pager),
  **Massively** or **Stellar** (dark scroll), **Forty** (bold photo tiles — best *once real
  product photos exist*).

**My recommendation: Option A.** The engine already does everything a smoke-shop brochure
needs and keeps deploy = `git push`. Use HTML5 UP only if the owner wants a totally
different look. Confirm the pick, then proceed.

## Business facts — REAL, verified from Yelp 2026-07-23 (do NOT fabricate anything else)

- **Name:** JR Smoke Zone
- **Type:** Locally owned smoke & vape shop (Vape Shop / Tobacco Shop / Smoke Shop)
- **Address:** 2616 Ventura Blvd, Camarillo, CA 93010
- **Hours:** Mon–Sat 9:00 AM – 9:00 PM · Sun 10:00 AM – 8:00 PM
- **Products (verbatim from their Yelp "About"):** "a range of products including hookah,
  e-Liquid, glass pipes, cigars, bongs, vape accessories & much more!"
- **Amenities (Yelp):** Wheelchair accessible · Accepts credit cards · Bike parking
- **Instagram:** https://www.instagram.com/jrsmokezone/  (age-gated to logged-out viewers)
- **Product categories to feature** (all from their real list — no invented brands):
  Vapes & E-Liquid · Hookah · Glass Pipes · Bongs & Water Pipes · Cigars · Vape Accessories
- **Real review sentiment** (context only, don't quote as testimonials yet): reviewers
  repeatedly praise the **staff being helpful/patient** and the **glass selection**; the
  overall Yelp rating is **mixed** (some 1-star complaints). So feature **no rating badge
  and no star claims** until the owner supplies genuine ones.

## Placeholders — owner / I must provide before launch (leave clearly marked TODO)

- **Phone number** — Yelp hides it, IG is gated. I'll get it from my buddy.
- **Email / FormSubmit inbox** — needed to activate the contact form.
- **Real photos** — interior, product walls, glass. From the owner (don't scrape IG/Yelp).
- **Custom domain** — placeholder `jrsmokezone.com` in sitemap for now.
- **Logo / brand colors** — none yet; using a text wordmark + graphite/neon-green default.

## Smoke-shop requirements — non-negotiable

1. **21+ age gate** — full-screen splash on first visit ("Are you 21 or older?"), remembers
   via localStorage, "No" leaves the site. Legally required framing for CA tobacco/vape.
2. **FDA nicotine warning** in the footer: *"WARNING: This product contains nicotine.
   Nicotine is an addictive chemical."* plus a "Must be 21+ to purchase" line.
3. **No fabricated reviews, ratings, or stats** (my standing rule; doubly important here
   because the real rating is mixed).
4. **No photos yet** → typographic + neon, icon-driven design that looks intentional with
   zero images. Build it so real photos drop in later without a redesign.
5. **Not e-commerce** — no cart, no online sales. CTAs are "Visit us / Directions / Call."

## Design direction

- Dark default (graphite near-black, green-tinted) + **neon green accent**; light-mode toggle.
- Fonts: Bricolage Grotesque (display) + Plus Jakarta Sans (body).
- Line icons (no emoji), reveal-on-scroll motion, refined per the **high-end-visual-design**
  skill. Distinct from bwraps' pink identity.

## Pages (lean v1)

Home · Products · Visit (address + hours + map + amenities + call). Add About/Gallery only
once there's real content/photos.

## My conventions (carry from bwraps / anderson-it)

- Edit content in `build.py` only; never hand-edit generated HTML. Run `python3 build.py`.
- Real content only. Concise voice, no em dashes. Playful/local tone fits this brand.
- Preview: `python3 -m http.server 8777 --directory .` → Browser pane (navigate, then
  screenshot immediately; pane is flaky on scroll).
- Deploy: `git push origin main` → GitHub Pages (repo goes public → no secrets/emails in
  tracked files; gitignore `docs/`).
- Save generated outputs to OneDrive Documents if any; back up before overwriting live files.

## Current state of this folder

**Empty except for this file** — clean slate, deliberately. A partial Option-A port was
built during scoping and then wiped so the template choice starts unbiased. If you pick
Option A, clone the engine fresh from `~/Documents/Claude/bwraps/` (`build.py`, `styles.css`,
`app.js`) and reskin — do NOT copy bwraps' pink palette, real photos, or print-shop content.

## First actions for you (the new session)

1. State the template pick (A or B) in one line.
2. Scaffold it: if A, clone the bwraps engine and strip it to the smoke-shop content above;
   if B, copy the chosen HTML5 UP template folder in.
3. Build the 21+ age gate, nicotine footer, and icon-driven Products; preview; screenshot.
4. Give me back the short **owner TODO list** (phone, email, photos, domain, logo).
