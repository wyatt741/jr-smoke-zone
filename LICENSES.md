# Image provenance & licensing

Per playbook §4: provenance recorded for every image. Three sources are used here:
the **owner's logo**, the **shop's own Instagram photos**, and **Pexels stock** for the
product category imagery.

## Logo (owner-supplied)
| File | Source | Notes |
|------|--------|-------|
| `assets/logo.png` | Owner's logo artwork (`ITC Benguiat.pdf.pdf`, supplied by the owner via Wyatt) | Rasterized + trimmed to square. Full logo: scorpion + arched "JR. Smoke Zone" lettering. |
| `assets/mark.png` | Same source, scorpion cropped out of the full logo | Nav/footer brand mark. |
| `assets/favicon.ico` / `favicon.png` / `apple-touch-icon.png` | Generated from `mark.png` (Pillow) | 16/32/48 ico, 256 png, 180 full-bleed apple-touch. |

Brand blue `#67ade8` was colour-sampled from this artwork.

## Instagram photos (owner's own content)
Pulled 2026-07-23 from the shop's own public account
[@jrsmokezone](https://www.instagram.com/jrsmokezone/) via an Apify scraper, at
Wyatt's explicit direction. **Only posts authored by @jrsmokezone were used** —
posts by other accounts that merely tagged the shop were discarded.

| File | Post | Shows |
|------|------|-------|
| `assets/ig/Cj6NQc6goUQ.jpg` | [link](https://www.instagram.com/p/Cj6NQc6goUQ/) | Interior — cigar wall, lit ceiling |
| `assets/ig/DQXqPwjEghY.jpg` | [link](https://www.instagram.com/p/DQXqPwjEghY/) | Interior — shop floor |
| `assets/ig/DIfCAIIztcr.jpg` | [link](https://www.instagram.com/p/DIfCAIIztcr/) | 4/20 deals graphic |
| `assets/ig/DR0OKh2Eupc.jpg` | [link](https://www.instagram.com/p/DR0OKh2Eupc/) | Holiday giveaway boards |
| `assets/ig/DSG21OwES8q.jpg` | [link](https://www.instagram.com/p/DSG21OwES8q/) | In-store toy drive |
| `assets/ig/DXQFTVrj8Bo.jpg` | [link](https://www.instagram.com/p/DXQFTVrj8Bo/) | 4/20 celebration |

Each gallery tile links back to its source post.

### ✅ Owner sign-off — 2026-07-23
The shop owner has **explicitly approved** use of these images on this site
(confirmed to Wyatt, 2026-07-23). They are the shop's own published posts used for
the shop's own site.

Note for reference, not a blocker: two tiles are event flyers the shop published that
also feature partner businesses (JR Liquor Mart, P.S. Motorsports, Anderson
Technologies, Beachside Motorsports).

Still worth doing: swap in owner-supplied **hi-res originals** when available.
Instagram only serves low-res, so these are optimized to 720x900.

## Facts, not images
Business facts (address, hours, amenities, product categories) verified from Yelp
2026-07-23. Carried brands (Puffco, Zig-Zag, RAW, Elf Bar) are stated by the shop in
its own IG captions. Nothing invented.


## Pexels stock (product category imagery)
Added 2026-07-23 at Wyatt's request to fill out the Products page. All from
[Pexels](https://www.pexels.com), used under the [Pexels License](https://www.pexels.com/license/)
(free for commercial use, no attribution required, no resale of the unaltered image).
Each was downloaded, cropped to 5:4 and re-encoded at q82 — none are hotlinked.

| File | Pexels ID | Source |
|------|-----------|--------|
| `assets/products/vape.jpg` | 11587602 | https://www.pexels.com/photo/11587602/ |
| `assets/products/hookah.jpg` | 7518765 | https://www.pexels.com/photo/7518765/ |
| `assets/products/bong.jpg` | 8551077 | https://www.pexels.com/photo/8551077/ |
| `assets/products/cigar.jpg` | 10343917 | https://www.pexels.com/photo/10343917/ |
| `assets/products/papers.jpg` | 29474378 | https://www.pexels.com/photo/29474378/ |
| `assets/products/gear.jpg` | 19901864 | https://www.pexels.com/photo/19901864/ |
| `assets/products/apparel.jpg` | 581339 | https://www.pexels.com/photo/581339/ |

**Glass Pipes deliberately uses the shop's OWN interior photo**
(`assets/ig/Cj6NQc6goUQ.jpg`) rather than stock — it shows their actual product wall,
which is the thing reviewers single out. Real beats stock where real exists.

### Editorial rules applied when selecting
1. **Product-first, no people smoking.** Lifestyle shots of people mid-smoke were rejected.
2. **Nothing cannabis-implying.** Pexels results for "bong", "glass pipe" and "rolling
   papers" are dominated by cannabis imagery. JR Smoke Zone is a tobacco/vape retailer,
   not a dispensary, so every such image was rejected. The chosen water-pipe and papers
   shots contain no cannabis.
3. **Rejected a mis-tagged asset.** Pexels ID 6478094, titled "White and Red Glass Smoking
   Pipe" in search results, actually resolves to a photo of **fishing lures**. Caught on
   visual review and discarded.

### ⚠️ Known nits for the owner
- `vape.jpg` shows devices with a faintly visible **"Logic"** brand marking. Swap it if
  the shop does not carry Logic.
- These are **category/mood images, not the shop's actual inventory**. Replace with real
  shop photos when available — that is strictly better and the layout takes them as-is.
