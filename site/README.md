# 7H Campaign Engineer

A small, local-first website for building artist campaign plans for **7H Music Group**. The first working plan is a **2027, 12-week campaign for Baranga**, prepared for review on 25 Nov 2026.

The figures on the objectives and budget pages are what I’ll work toward in the campaign window; I’ll measure them as the work happens.

## What’s here

| Path | What it is |
|---|---|
| `index.html` | The campaign homepage: the 18-slide order, the plan, a reusable builder, downloads and references. |
| `presentation.html` | The live 18-slide browser deck with speaker notes, keyboard navigation, fullscreen and print support. |
| `download.html` | Download page for the PDF and editable PowerPoint. |
| `downloads/Baranga_12-Week_Campaign_Strategy.pdf` | The 18-page printable version of the assignment. |
| `downloads/Baranga_12-Week_Campaign_Slides.pptx` | The editable 16:9 PowerPoint with 18 slides and speaker notes. |
| `Baranga_12-Week_Marketing_Campaign.pptx` | Root-level compatibility copy of the same deck. |
| `RESEARCH.md` | Working notes, platform facts and references. |
| `data/campaign.json` | The single source of truth for the site, PDF and slides. |
| `briefs/` | The supplied 7H brief and concept note. |
| `assets/` | Local CSS, JavaScript, icons and supplied 7H/rights-holder artwork. |
| `build_assets.py` | Regenerates `assets/js/campaign-data.js`, the PDF, the PPTX and the root-level PowerPoint copy from `data/campaign.json`. |

## Slide order

The deck follows the required 18-slide assignment order:

1. Title / one job
2. Objectives
3. “BUT FIRST...”
4. Audience profile
5. Biggest end benefit
6. “SO... WHO IS BARANGA ...ACTUALLY?”
7. Brand archetype
8. Identity equation
9. Brand signature
10. Competitors
11. Strengths / weaknesses
12. “HOW DO WE BEAT THEM?”
13. Positioning / strategy
14. Tactics
15. Playlist tactics
16. Timeline · Weeks 1–6
17. Timeline · Weeks 7–12
18. Thank you

See [`RESEARCH.md#assignment-slide-order`](RESEARCH.md#assignment-slide-order) for the working note.

## Run it locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build_assets.py
python3 -m http.server 8080 --bind 0.0.0.0
```

Then open `index.html`, `presentation.html` or `download.html` from the local server. The site uses local CSS, JavaScript, SVG icons and supplied artwork — no CDN, external font, analytics or backend is required.

## Before launch

I’ll set the exact 12-week dates, campaign owner, budget currency, audio clearances, venue/ticketing terms and Week 0 private DSP baselines with the team before launch. “2027” is the campaign heading.

Supplied artwork belongs to the respective rights holders and is used for this internal campaign.
