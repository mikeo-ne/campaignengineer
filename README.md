# campaignengineer

**BARANGA — 12-Week Marketing & Promotion Campaign** (emerging Ugandan Afro-Pop / Rap artist).

## Deliverables

| File | What it is |
|---|---|
| `index.html` | Self-contained interactive HTML slide deck — dark/neon design, 18 slides, keyboard nav (←/→, N = speaker notes, F = fullscreen, P = print/PDF). Best viewed served over HTTP. |
| `Baranga_12-Week_Marketing_Campaign.pptx` | PowerPoint build (16:9) mirroring the deck, with **speaker notes on every slide**. Open in PowerPoint or import into Google Slides. |
| `assets/` | AI-generated concept artwork (stylized portrait, Badman + CHAPTERS I NEVER WROTE cover concepts, western Uganda landscape, Gen Z Kampala moodboard, closing neon). Not official photography. |
| `build_pptx.py` | Regenerates the `.pptx` from scratch. |

## View the deck

```bash
python3 -m http.server 8080
# open http://localhost:8080/
```

`Ctrl/Cmd + P` saves the HTML deck to PDF (one 16:9 slide per page).

## Rebuild the PowerPoint

```bash
python3 -m venv .venv
.venv/bin/pip install python-pptx pillow
.venv/bin/python build_pptx.py
```

## Fact sources

Spotify · Apple Music · Shazam · YouTube · Musixmatch · Audiomack · NRG Radio UG interviews ·
official releases: **SALO** (24 Aug 2024), **Badman** (feat. STANDO & Andrinah, 3 May 2025, 5844655 Records DK),
**Party Riddim** (feat. Ace Kaawa, 2025), **CHAPTERS I NEVER WROTE** (7 tracks, 8 May 2026).
Figures marked “~” are public approximations — refresh in Spotify for Artists / YouTube Studio during Week 0.
