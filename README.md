# campaignengineer — BARANGA · 12-Week Marketing & Promotion Campaign

Presentation build for the BARANGA campaign review — emerging Ugandan Afro-Pop / Rap artist, Badman era.

## Deliverables

| File | What it is |
|---|---|
| `index.html` | Self-contained interactive HTML deck — dark/neon design, 18 slides, keyboard nav (←/→ · **N** speaker notes · **F** fullscreen · **P** print/PDF). Served over HTTP for the live preview. |
| `Baranga_12-Week_Marketing_Campaign.pptx` | PowerPoint build (16:9) mirroring the deck, with **speaker notes on every slide**. Opens in PowerPoint; imports into Google Slides. |
| `assets/real/` | **Official artwork from the releases** — Badman (feat. STANDO & Andrinah, 5844655 Records DK), Party Riddim (Ace Kaawa & BARANGA), CHAPTERS I NEVER WROTE (teaser + album art), plus an official studio-session still from the Badman era. |
| `build_pptx.py` | Regenerates the `.pptx`. |

## View the deck

```bash
python3 -m http.server 8080   # then open http://localhost:8080/
```

`Ctrl/Cmd + P` saves the HTML deck to PDF (16:9, one slide per page).

## Rebuild the PowerPoint

```bash
python3 -m venv .venv && .venv/bin/pip install python-pptx pillow
.venv/bin/python build_pptx.py
```

## Fact sources

Apple Music (artist ID 1764683984) · Spotify · Shazam · Audiomack (@badman-rare) · Deezer (artist 53724222) · NRG Radio UG · YouTube.
Releases: **SALO** 24 Aug 2024 · **Do you?** Jan 2025 · **Confirm** (feat. Smokie Cee) Feb 2025 · **Badman** (feat. STANDO & Andrinah) 3 May 2025 · **CHAPTERS I NEVER WROTE** 8 May 2026 (7 tracks) · **Island Kiss** (Smokie Cee feat. BARANGA) Aug 2026 · **Party Riddim** (Ace Kaawa & BARANGA) Aug 2025.

Figures marked “~” are public approximations (Nov 2026); Week 0 re-baselines them in Spotify for Artists.
Artwork shown belongs to the respective rights holders and is used within the artist’s own campaign materials.
