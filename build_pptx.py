#!/usr/bin/env python3
"""Build Baranga — 12-Week Marketing & Promotion Campaign as a styled .pptx.

Mirrors the HTML deck (index.html). Dark/neon aesthetic, 16:9, speaker notes on
every slide. Run:  .venv/bin/python build_pptx.py
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

# ---------- design tokens ----------
BG      = "07070F"; PANEL  = "12122A"; PANEL2 = "171733"; LINE = "2A2A48"
TEXT    = "F4F4FB"; MUTED  = "9A9AB8"
CYAN    = "2FD6FF"; GOLD   = "F5C542"; RED    = "FF3B3B"; GREEN = "34D399"; MAGENTA = "FF4FD8"
UGY     = "FCD116"; UGR    = "D90000"
HEAD_FONT = "Archivo Black"; BODY_FONT = "Montserrat"

W, H = 13.333, 7.5
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
OUT    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Baranga_12-Week_Marketing_Campaign.pptx")

def C(hexstr): return RGBColor.from_string(hexstr.lstrip("#"))

def set_bg(slide, color=BG):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C(color)

def box(slide, x, y, w, h, fill=None, line=None, line_w=1.0, round_=True, shadow=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    if round_:
        try:
            shp.adjustments[0] = 0.055
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = C(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = C(line); shp.line.width = Pt(line_w)
    shp.shadow.inherit = shadow
    return shp

def txt(slide, x, y, w, h, content, size=16, color=TEXT, bold=False, font=BODY_FONT,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.0, wrap=True, autosize=None):
    """content: str, or list of paragraphs; each paragraph is str or list of (text, dict) runs."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if isinstance(content, str):
        content = [content]
    for pi, para in enumerate(content):
        p = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        if isinstance(para, str):
            para = [(para, {})]
        for t, style in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(style.get("size", size))
            r.font.bold = style.get("bold", bold)
            r.font.name = style.get("font", font)
            r.font.color.rgb = C(style.get("color", color))
    return tb

def pic(slide, path, x, y, w=None, h=None):
    kw = {}
    if w: kw["width"] = Inches(w)
    if h: kw["height"] = Inches(h)
    return slide.shapes.add_picture(path, Inches(x), Inches(y), **kw)

def kicker(slide, text, color=CYAN, x=0.55, y=0.32):
    txt(slide, x, y, 8, 0.3, [[("●  ", {"color": color, "size": 10}), (text.upper(), {"color": color, "size": 10, "bold": True})]],
        font=BODY_FONT).text_frame.paragraphs[0].line_spacing = 1.0
    # letterspacing via caps already; add thin accent line
    box(slide, x, y + 0.32, 1.6, 0.018, fill=color, round_=False)

def title(slide, runs, x=0.55, y=0.62, w=12.2, h=1.1):
    if isinstance(runs, str):
        runs = [[(runs, {})]]
    txt(slide, x, y, w, h, runs, size=30, color=TEXT, font=HEAD_FONT, bold=False, line_spacing=1.02)

def footer(slide, label, page):
    box(slide, 0.55, 7.06, 12.23, 0.012, fill=LINE, round_=False)
    txt(slide, 0.55, 7.12, 8, 0.28, [[("BARANGA", {"color": GOLD, "bold": True, "size": 8}),
                                      ("  —  " + label + "   ● ● ●  UG", {"color": MUTED, "size": 8})]])
    txt(slide, 11.6, 7.12, 1.2, 0.28, f"{page:02d} / 18", size=8, color=MUTED, align=PP_ALIGN.RIGHT)

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def panel(slide, x, y, w, h, accent=None, accent_side="left", fill=PANEL):
    box(slide, x, y, w, h, fill=fill, line=LINE, line_w=1.0)
    if accent:
        if accent_side == "left":
            box(slide, x, y + 0.12, 0.045, h - 0.24, fill=accent, round_=False)
        elif accent_side == "top":
            box(slide, x + 0.12, y, w - 0.24, 0.045, fill=accent, round_=False)

def chip(slide, x, y, w, text, color=TEXT, border=LINE):
    box(slide, x, y, w, 0.30, fill=PANEL2, line=border, line_w=1.0)
    txt(slide, x, y + 0.015, w, 0.27, text, size=8.5, color=color, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W), Inches(H)
blank = prs.slide_layouts[6]

def new_slide():
    s = prs.slides.add_slide(blank)
    set_bg(s)
    return s

# ============ SLIDE 1 — TITLE ============
s = new_slide()
# right image panel
pic(s, f"{ASSETS}/portrait-hero.jpg", 6.1, 0.0, w=7.24, h=7.5)
box(s, 6.1, 0.0, 0.06, 7.5, fill=CYAN, round_=False)
kicker(s, "12-Week Marketing & Promotion Campaign")
txt(s, 0.55, 1.05, 5.9, 2.6, [[("BARANGA", {"size": 88, "font": HEAD_FONT, "color": TEXT})]])
txt(s, 0.55, 3.35, 5.9, 0.35, "EMERGING UGANDAN AFRO-POP / RAP · HIP-HOP TRAP", size=11, color=CYAN, bold=True)
box(s, 0.55, 3.85, 0.9, 0.03, fill=GOLD, round_=False)
txt(s, 0.55, 4.05, 5.8, 0.5, [[("“You know it’s Baranga”", {"size": 17, "color": GOLD, "bold": True})]])
txt(s, 0.55, 4.75, 5.9, 1.15, [
    [("Presented by:  ", {"color": MUTED, "size": 10}), ("Campaign Engineer Studio × Baranga Team", {"size": 10})],
    [("Date:  ", {"color": MUTED, "size": 10}), ("November 2026 · Kampala, Uganda", {"size": 10})],
    [("Album cycle:  ", {"color": MUTED, "size": 10}), ("CHAPTERS I NEVER WROTE (8 May 2026)", {"size": 10})],
], line_spacing=1.35)
txt(s, 0.55, 6.35, 5.9, 0.3, "Spotify · Apple Music · YouTube · Shazam · IG / TikTok @_baranga", size=8, color=MUTED)
txt(s, 0.55, 6.72, 5.9, 0.3, "Portrait & cover art are AI-generated concept visuals. Facts: Spotify · Apple Music · Shazam · YouTube · NRG Radio UG.", size=6.5, color="5C5C78")
footer(s, "Title", 1)
notes(s, "Open with energy, not biography. One line: “This is Baranga — a Munyoro kid from western Uganda whose debut single SALO was written in high school, and whose single Badman is now everywhere on East African Gen Z feeds. In the next 12 weeks we turn that spark into a sustainable artist engine.” The deck is designed dark/neon on purpose — it reads like a music campaign, not a corporate review. Ground rules: every fact shown is from public sources; every number marked “~” is an approximate figure to be re-verified in Spotify for Artists before launch. Hold questions until slide 16 (metrics).")

# ============ SLIDE 2 — AGENDA ============
s = new_slide()
kicker(s, "Agenda")
title(s, [[("WHAT WE’LL ", {}), ("COVER", {"color": CYAN})]])
agenda = [
    ("01","Who is the Artist","Origin, name meaning & current momentum"),
    ("02","Campaign Objectives","SMART goals across awareness, streams & fan growth"),
    ("03","Audience Profile","Ugandan / East African Gen Z, 16–25"),
    ("04","Brand Archetypes","Outlaw × Everyman × Jester"),
    ("05","Competition Analysis","Peers, veterans & Baranga’s edge"),
    ("06","Positioning & Strategy","The statement, pillars & hashtags"),
    ("07","Visual Identity","Colors, type, imagery, do’s & don’ts"),
    ("08","12-Week Timeline & Calendar","Phases, weekly rhythm & daily themes"),
    ("09","Success Metrics & Next Steps","KPIs, tooling & launch checklist"),
]
for i,(n,t,d) in enumerate(agenda):
    y = 1.35 + i*0.55
    box(s, 0.55, y, 7.5, 0.48, fill=PANEL if i%2==0 else PANEL2, line=LINE, line_w=0.75)
    txt(s, 0.72, y+0.02, 0.75, 0.45, n, size=17, color=CYAN, font=HEAD_FONT, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 1.55, y+0.045, 6.4, 0.4, [[(t+"  ", {"bold": True, "size": 11.5}),("—  "+d, {"size": 8.5, "color": MUTED})]], anchor=MSO_ANCHOR.MIDDLE)
pic(s, f"{ASSETS}/cover-badman.jpg", 8.35, 1.30, w=4.45, h=2.6)
pic(s, f"{ASSETS}/cover-chapters.jpg", 8.85, 3.45, w=3.45, h=1.9)
pic(s, f"{ASSETS}/landscape-western-uganda.jpg", 8.35, 4.95, w=4.45, h=1.55)
footer(s, "Agenda", 2)
notes(s, "Run this slide in under 40 seconds — it’s a map, not a story. Flag two slides to watch closely: 8 (positioning) and 12–15 (the calendar) — that’s where strategy becomes execution. Mention that every visual suggestion from the planning doc is baked into this deck’s design — the room is seeing the moodboard, not just reading about it.")

# ============ SLIDE 3 — WHO IS THE ARTIST 1/2 ============
s = new_slide()
kicker(s, "Who is the Artist · 1 of 2")
title(s, [[("FROM ", {}), ("WESTERN UGANDA", {"color": GOLD}), (" TO THE TIMELINE", {})]])
bullets = [
    ("BARANGA"," — Baranga Ferdinand, professionally BARANGA. Dynamic Ugandan Afro-pop & rap / hip-hop trap artist."),
    ("Career began 2023."," Debut single “SALO” (24 Aug 2024) — written and released while still in high school."),
    ("SALO"," is his first song built on a true personal story — widely understood to be about an affair; it launched the “real stories, real chapters” identity."),
    ("From western Uganda","; Munyoro heritage — self-described “Motorola by tribe” energy: tough, loud, proud."),
    ("The name “Baranga”"," fuses his hometown with the idea of “spreading the good news” — i.e. spreading good music."),
    ("Inspired by an uncle already in the music industry"," — music was the family business long before streaming."),
]
y = 1.5
for b, rest in bullets:
    txt(s, 0.7, y, 6.9, 0.72, [[("▸  ", {"color": GOLD, "size": 12}), (b, {"bold": True, "size": 11, "color": TEXT}), (rest, {"size": 10.5, "color": "D9D9EC"})]], line_spacing=1.12)
    y += 0.68
panel(s, 0.7, 5.6, 6.4, 0.95, accent=GOLD, fill=PANEL2)
txt(s, 0.95, 5.72, 6.0, 0.25, "SIGNATURE LINE", size=8, color=MUTED, bold=True)
txt(s, 0.95, 5.97, 6.0, 0.45, "“You know it’s Baranga.”", size=18, color=GOLD, bold=True, font=HEAD_FONT)
pic(s, f"{ASSETS}/landscape-western-uganda.jpg", 8.15, 1.45, w=4.6, h=4.35)
txt(s, 8.15, 5.9, 4.6, 0.5, "Western Uganda — Ruwenzori foothills & the lakes. Baranga’s roots: Munyoro country, now exporting sound to Kampala and beyond.", size=8.5, color=MUTED, align=PP_ALIGN.CENTER, line_spacing=1.15)
footer(s, "Who is the Artist", 3)
notes(s, "Tell the SALO story slowly — it’s the single most persuasive thing in the room. A teenager writes a song about a real affair, self-releases it, and it breaks through. That’s why positioning leans on authenticity rather than polish. Note the dual meaning of the name and repeat it: hometown + “spreading the good news.” If asked about the uncle, keep it warm and brief — music was in the family long before the streams. Avoid overclaiming listener numbers here; that lives on slide 4.")

# ============ SLIDE 4 — WHO IS THE ARTIST 2/2 ============
s = new_slide()
kicker(s, "Who is the Artist · 2 of 2")
title(s, [[("THE ", {}), ("CATALOGUE", {"color": CYAN}), (" & CURRENT STATUS", {})]])
pic(s, f"{ASSETS}/cover-badman.jpg", 0.55, 1.5, w=3.6, h=3.6)
stats = [("~4,042","Monthly listeners*"),("311K+","Badman streams*"),("~68K","YouTube visualizer*")]
for i,(n,d) in enumerate(stats):
    x = 0.55 + i*1.27
    box(s, x, 5.3, 1.12, 1.05, fill=PANEL2, line=LINE)
    txt(s, x, 5.42, 1.12, 0.5, n, size=17, color=GOLD, bold=True, align=PP_ALIGN.CENTER, font=HEAD_FONT)
    txt(s, x+0.04, 5.9, 1.04, 0.42, d, size=6, color=MUTED, align=PP_ALIGN.CENTER, line_spacing=1.1)
txt(s, 0.55, 6.42, 4.1, 0.4, "*Approximate public figures at research time. Re-verify in Spotify for Artists / YouTube Studio before launch.", size=6.5, color="5C5C78", line_spacing=1.15)
# right: table
panel(s, 4.6, 1.45, 8.2, 2.6)
txt(s, 4.85, 1.55, 7.7, 0.3, "KEY RELEASES", size=9, color=CYAN, bold=True)
rows = [
    ("SALO", "2024", "Debut single · 24 Aug 2024 · written in high school · true story"),
    ("Badman (feat. STANDO & Andrinah)", "2025", "Biggest hit — rel. 3 May 2025 · 5844655 Records DK · Gen Z chokehold · strong Shazam"),
    ("Party Riddim", "2025", "Feat. Ace Kaawa · dance/party record"),
    ("Do you? · Confirm", "2025", "Singles building the trap / Afro-pop lane"),
    ("CHAPTERS I NEVER WROTE", "2026", "7-track debut album · 8 May 2026"),
]
ty = 1.95
col_x = [4.85, 9.05, 9.85]
txt(s, col_x[0], ty, 4.1, 0.25, "RELEASE", size=7.5, color=MUTED, bold=True)
txt(s, col_x[1], ty, 0.8, 0.25, "YEAR", size=7.5, color=MUTED, bold=True)
txt(s, col_x[2], ty, 2.9, 0.25, "NOTES", size=7.5, color=MUTED, bold=True)
ty += 0.28
for r,y,n in rows:
    txt(s, col_x[0], ty, 4.1, 0.36, r, size=8, bold=True, color=TEXT, line_spacing=1.0)
    txt(s, col_x[1], ty, 0.8, 0.36, y, size=8, color=CYAN)
    txt(s, col_x[2], ty, 2.9, 0.36, n, size=7, color="D9D9EC", line_spacing=1.05)
    box(s, 4.85, ty+0.33, 7.7, 0.008, fill=LINE, round_=False)
    ty += 0.4
# tracklist
panel(s, 4.6, 4.25, 8.2, 1.75, fill=PANEL2)
txt(s, 4.85, 4.38, 7.7, 0.28, "ALBUM TRACKLIST — CHAPTERS I NEVER WROTE", size=9, color=CYAN, bold=True)
tracks = ["01 PARADISE (TUNGI)","02 WAGWUAN (MR FALLBACK & MELLAN KUNTA)","03 KAMPALA (DEEJAY KLVN)","04 LOST CAUSE (KRAVYNZ & KING AVO)","05 BREATHE (MR FALLBACK)","06 JAGERMEISTER (KING AVO)","07 FREAKY"]
tx, ty = 4.85, 4.78
for i, t in enumerate(tracks):
    wchip = 0.155 + 0.082*len(t)*0.62
    if tx + wchip > 12.6:
        tx = 4.85; ty += 0.42
    chip(s, tx, ty, wchip, t, color=(CYAN if i in (0,2) else TEXT), border=LINE)
    tx += wchip + 0.18
txt(s, 4.6, 6.18, 8.2, 0.3, [[("@_baranga across platforms  ·  YouTube visualizers  ·  Peer collabs: STANDO · Andrinah · Ace Kaawa · King Avo · TUNGI · MR FALLBACK", {"size": 8.5, "color": MUTED})]])
footer(s, "Music & Momentum", 4)
notes(s, "Land three proof points, in this order: (1) Badman — a 2025 record out-streaming expectations with organic Shazam traction; (2) the album — CHAPTERS I NEVER WROTE dropped 8 May 2026 with seven chapters and star features, so this campaign rides an album cycle, not a one-off; (3) velocity — roughly 4K monthly listeners means headroom, not saturation. If challenged on the 311K figure, concede gracefully: public counters move; treat as order-of-magnitude and refresh in week 0. Close the loop: an artist mid-breakout, and the next 12 weeks decide whether the spike flattens or compounds.")

print("Slides 1–4 built")

# ============ SLIDE 5 — OBJECTIVES ============
s = new_slide()
kicker(s, "Campaign Objectives")
title(s, [[("FROM ", {}), ("SPARK", {"color": GOLD}), (" TO ", {}), ("SYSTEM", {"color": CYAN})]])
txt(s, 0.55, 1.32, 12, 0.35, "Overall goal: build sustainable momentum for BARANGA as the authentic Gen Z “Badman” voice over 12 weeks — measured, not vibes.", size=11, color=MUTED)
objectives = [
    ("01","Awareness ×2–3","Grow monthly listeners & video views 2–3× baseline by Week 12; Badman + one album deep cut trending on UG TikTok/Reels.", CYAN),
    ("02","Streams +50–100%","Lift Spotify streams & saves 50–100%+ over the window; album tracks compounding week-over-week.", GOLD),
    ("03","Audience +10–15K","Add 10–15K combined engaged followers (IG/TikTok/YT); 5K+ joining email/WhatsApp community.", MAGENTA),
    ("04","UGC Engine","Seed ≥500 user videos using #BarangaBadman; 3 recurring challenge formats; 20+ creator duets/stitches.", GREEN),
    ("05","Industry Openings","3+ playlist adds (editorial/indie UG & East Africa), 2+ radio interviews, 1 live showcase booked.", RED),
    ("06","Long-Term Engine","Repeatable content system + 2027 release calendar; management/label-ready campaign report.", UGY),
]
cw, ch, gap = 4.0, 1.95, 0.22
for i,(n,t,d,acc) in enumerate(objectives):
    col, row = i % 3, i // 3
    x, y = 0.55 + col*(cw+gap), 1.85 + row*(ch+0.28)
    panel(s, x, y, cw, ch, accent=acc)
    txt(s, x+0.22, y+0.14, cw-0.4, 0.35, n, size=14, color="3A3A5E", font=HEAD_FONT)
    txt(s, x+0.22, y+0.5, cw-0.4, 0.3, t, size=14, bold=True)
    txt(s, x+0.22, y+0.88, cw-0.4, 0.95, d, size=9, color=MUTED, line_spacing=1.18)
footer(s, "Objectives", 5)
notes(s, "Frame every objective as SMART on the whiteboard: each has a number, a deadline (end of Week 12) and a source of truth. Stress sequencing — awareness feeds streams, streams feed follows, follows feed UGC, UGC feeds industry leverage. If the room remembers one line: “We are not buying fame; we are compounding a fanbase that already exists.” Objectives 05 and 06 matter most to management — playlist adds and a booked showcase are the tangible wins that unlock the next conversation about touring or distribution.")

# ============ SLIDE 6 — AUDIENCE ============
s = new_slide()
kicker(s, "Audience Profile")
title(s, [[("GEN Z, ", {}), ("KAMPALA-FIRST", {"color": GOLD}), (", EAST-AFRICA-READY", {})]])
cols = [
    ("✓  WHAT THEY WANT", GREEN, ["Authentic, unpolished voices — not industry robots","Party records for 2AM in Kabalagala","Local flavor: Luganda/Runyoro inflections, Kampala slang","Relatable origin stories they can quote and share","A sound they can claim as “ours” before the world catches on"]),
    ("✕  WHAT’S MISSING", RED, ["Label-polished acts disconnected from the street","Generic Afrobeats clones with no Ugandan fingerprint","No recurring Baranga-style fan ritual or challenge culture","Few emerging acts with both streams and a story","East-African faces rare in global trap/Afro-pop playlists"]),
    ("⇄  HOW BARANGA FILLS IT", GOLD, ["High-school-to-Badman story = quote-tweet bait","True-story songwriting (SALO) builds parasocial trust","Badman energy + melodic hooks = TikTok-ready moments","Munyoro roots + Kampala hustle = two audiences, one artist","Meme-able identity: “You know it’s Baranga”"]),
]
for i,(h,acc,items) in enumerate(cols):
    x = 0.55 + i*4.13
    panel(s, x, 1.45, 3.9, 3.6, accent=acc, accent_side="top")
    txt(s, x+0.2, 1.6, 3.5, 0.3, h, size=11, bold=True, color=acc)
    yy = 2.1
    for it in items:
        txt(s, x+0.2, yy, 3.55, 0.62, [[("▸ ", {"color": GOLD}), (it, {"size": 8.5, "color": "D9D9EC"})]], line_spacing=1.15)
        yy += 0.585
chips = [("16–25 PRIMARY", CYAN),("URBAN KAMPALA + WESTERN UG", TEXT),("TIKTOK · REELS · SHORTS", TEXT),("SPOTIFY + AUDIOMACK", TEXT),("SECONDARY: 25–34 AFRO-POP", GOLD)]
cx = 0.55
for t, col in chips:
    w = 0.16 + 0.078*len(t)*0.92
    chip(s, cx, 5.25, w, t, color=col)
    cx += w + 0.18
pic(s, f"{ASSETS}/moodboard-genz.jpg", 0.55, 5.65, w=12.23, h=1.15)
footer(s, "Audience", 6)
notes(s, "Open the three columns left to right and pause on the middle one — “what’s missing.” That gap is the campaign’s reason to exist; Baranga is the bridge, not just another artist. If the room pushes back that the audience is “just TikTok kids,” widen the frame: primary is 16–25 heavy social, but the SALO angle travels to 25–34 too. Close with the moodboard image: “This is the energy we pour media into.”")

# ============ SLIDE 7 — ARCHETYPES ============
s = new_slide()
kicker(s, "Brand Archetypes")
title(s, [[("OUTLAW", {"color": RED}), (" × ", {"color": MUTED}), ("EVERYMAN", {"color": CYAN}), (" × ", {"color": MUTED}), ("JESTER", {"color": UGY})]])
panel(s, 0.55, 1.55, 4.35, 4.55, accent=RED, accent_side="top")
txt(s, 0.8, 1.75, 3.9, 0.3, "PRIMARY · OUTLAW / REBEL", size=9, bold=True, color="FF8A8A")
txt(s, 0.8, 2.15, 3.9, 0.7, "🕶️", size=44)
txt(s, 0.8, 2.85, 3.9, 0.35, "“The Badman”", size=17, bold=True)
txt(s, 0.8, 3.3, 3.85, 1.7, "Rules are suggestions. The walk, the snarl, the “Ayagala badman…” hook. Swagger without apology — the archetype behind the Badman single and its cover codes: smoke, neon, leather, red/blue.", size=9.5, color=MUTED, line_spacing=1.25)
chip(s, 0.8, 5.15, 1.15, "CONFIDENCE", color="FF8A8A", border=RED); chip(s, 2.05, 5.15, 1.1, "DEFIANCE", color="FF8A8A", border=RED); chip(s, 3.25, 5.15, 1.35, "INDEPENDENCE", color="FF8A8A", border=RED)
pic(s, f"{ASSETS}/portrait-hero.jpg", 5.15, 1.55, w=3.0, h=4.0)
txt(s, 5.15, 5.6, 3.0, 0.4, "The intersection: raw confidence, real story, party frequency.", size=8, color=MUTED, align=PP_ALIGN.CENTER, line_spacing=1.2)
panel(s, 8.45, 1.55, 4.33, 2.15, accent=CYAN, accent_side="top")
txt(s, 8.7, 1.72, 3.9, 0.28, "SECONDARY · EVERYMAN", size=9, bold=True, color=CYAN)
txt(s, 8.7, 2.02, 3.9, 0.5, "🤝", size=30)
txt(s, 8.7, 2.5, 3.9, 0.3, "“The High-School Kid Who Made It”", size=12, bold=True)
txt(s, 8.7, 2.85, 3.85, 1.0, "Relatable roots, family in the industry, breakout written in a classroom. Fans grew up with him — trust before fame.", size=8.5, color=MUTED, line_spacing=1.2)
panel(s, 8.45, 3.9, 4.33, 2.2, accent=UGY, accent_side="top")
txt(s, 8.7, 4.07, 3.9, 0.28, "TERTIARY · JESTER / LOVER", size=9, bold=True, color=UGY)
txt(s, 8.7, 4.37, 3.9, 0.5, "🎉", size=30)
txt(s, 8.7, 4.85, 3.9, 0.3, "“The Party Frequency”", size=12, bold=True)
txt(s, 8.7, 5.2, 3.85, 1.0, "Party Riddim, melodic hooks, romance records — the Jester’s humor and the Lover’s pull keep the catalogue re-listenable beyond the snarl.", size=8.5, color=MUTED, line_spacing=1.2)
footer(s, "Archetypes", 7)
notes(s, "Center portrait is the pivot: “Outlaw gets the click, Everyman gets the save, Jester gets the replay.” Kill the idea that Baranga is only the angry badman — the mix is what makes the persona sustainable for 12 weeks of content without fatigue. Ask the room which archetype the next single leads with — that answer sets the Week 9+ content ratio.")

# ============ SLIDE 8 — COMPETITION ============
s = new_slide()
kicker(s, "Competition Analysis")
title(s, [[("WHERE BARANGA ", {}), ("WINS", {"color": GOLD})]])
swot = [
    ("STRENGTHS", GREEN, ["True-story songwriting (SALO) — instant narrative credibility","Badman traction: 311K+ streams*, Shazam momentum, Gen Z pull","High-school origin = fresh, underexposed angle in UG hip-hop","Peer collab web: STANDO, Andrinah, Ace Kaawa, King Avo, MR FALLBACK, TUNGI","Hungry, available, visually distinct (streetwear + neon)"]),
    ("WEAKNESSES", RED, ["Small baseline (~4K monthly listeners*) — thin paid efficiency today","Low content volume / inconsistent posting cadence","No owned community asset (channel/list) yet","Limited live & TV/radio footprint vs. veterans","Single-hit risk if Badman momentum isn’t converted"]),
    ("OPPORTUNITIES", CYAN, ["Album cycle gives 7 tracks of content runway","Afro-trap + Afro-pop gap for authentic young UG voices","Short-form video underpriced in UG; first-mover on Badman challenge","NRG Radio UG & UG blogs actively cover emerging artists","Diaspora UG communities (London, Toronto, Dubai) as multipliers"]),
    ("THREATS", GOLD, ["Label-backed urban acts dominate playlists & shows","Viral fatigue — Badman may not re-chart without reinvention","Copycat challenges from better-resourced artists","Weak monetization turns momentum into burnout","Platform algorithm shifts (TikTok/IG reach volatility)"]),
]
for i,(h,acc,items) in enumerate(swot):
    x, y = (0.55 if i%2==0 else 6.9), (1.45 if i<2 else 4.05)
    panel(s, x, y, 6.0, 2.4, accent=acc, accent_side="top", fill=PANEL)
    txt(s, x+0.2, y+0.12, 5.6, 0.3, h, size=10, bold=True, color=acc)
    yy = y+0.48
    for it in items:
        txt(s, x+0.2, yy, 5.65, 0.4, [[("– ", {"color": MUTED}), (it, {"size": 7.5, "color": "D9D9EC"})]], line_spacing=1.05)
        yy += 0.37
footer(s, "Competition", 8)
notes(s, "Be honest in the weaknesses column — credibility with the artist’s team comes from not flinching. Then pivot to opportunities: the album cycle is a 12-week content goldmine. Closing line: “We can’t out-budget the majors; we out-authenticity them.” If pressed on King Avo or MR FALLBACK as ‘competition,’ reframe: feature partners first, competitors second — collabs are distribution in this market.")

# ============ SLIDE 9 — POSITIONING & STRATEGY ============
s = new_slide()
kicker(s, "Positioning & Strategy")
title(s, [[("OWN THE ", {}), ("“BADMAN”", {"color": GOLD}), (" LANE", {})]])
panel(s, 0.55, 1.35, 12.23, 1.15, accent=GOLD)
txt(s, 0.8, 1.45, 3.0, 0.25, "POSITIONING STATEMENT", size=8, color=MUTED, bold=True)
txt(s, 0.8, 1.73, 11.7, 0.72, [[("For ", {}), ("Ugandan & East African Gen Z (16–25)", {"bold": True, "color": TEXT}),
    (" who want music that feels ", {}), ("raw, local and theirs", {"bold": True, "color": TEXT}),
    (", BARANGA is the ", {}), ("emerging Afro-pop / rap artist", {"bold": True, "color": CYAN}),
    (" who turns ", {}), ("true-story, high-school-rooted songwriting", {"bold": True, "color": TEXT}),
    (" into ", {}), ("party-ready trap anthems", {"bold": True, "color": TEXT}),
    (" — unlike polished industry acts, his music was ", {}), ("written in the classroom, not a boardroom", {"bold": True, "color": GOLD}), (".  You know it’s Baranga.", {"bold": True, "color": GOLD})]],
    size=10.5, line_spacing=1.3)
pillars = [("🎥","CONTENT ENGINE","4–7 short-form/wk, non-negotiable", CYAN),
           ("📢","AMPLIFICATION","Boost winners, not guesses", CYAN),
           ("🤝","COMMUNITY","WhatsApp channel + weekly replies", CYAN),
           ("🎯","PAID (OPTIONAL)","Only proven creatives", GOLD),
           ("📰","EARNED","NRG, blogs, podcasts, radio", GOLD),
           ("🎨","VISUAL IDENTITY","Dark · neon · street · UG", GOLD)]
pw, gap = 1.87, 0.17
for i,(ic,t,d,acc) in enumerate(pillars):
    x = 0.55 + i*(pw+gap)
    panel(s, x, 2.75, pw, 2.15, fill=PANEL2)
    txt(s, x, 2.95, pw, 0.5, ic, size=24, align=PP_ALIGN.CENTER)
    txt(s, x+0.08, 3.5, pw-0.16, 0.3, t, size=8, bold=True, color=acc, align=PP_ALIGN.CENTER)
    txt(s, x+0.12, 3.82, pw-0.24, 0.95, d, size=7.5, color=MUTED, align=PP_ALIGN.CENTER, line_spacing=1.2)
txt(s, 0.55, 5.35, 4.0, 0.3, "FLOW", size=8, color=MUTED, bold=True)
flow = [("AWARENESS", CYAN),("→", MUTED),("ENGAGEMENT", MAGENTA),("→", MUTED),("CONVERSION", GOLD),("→", MUTED),("SUSTAIN", GREEN)]
fx = 1.35
for t, col in flow:
    w = 0.32 + 0.085*len(t)*0.9 if t != "→" else 0.35
    if t == "→":
        txt(s, fx, 5.32, 0.35, 0.3, "→", size=14, color=MUTED)
    else:
        chip(s, fx, 5.32, w, t, color=col)
    fx += w + 0.15
txt(s, 0.55, 5.95, 4.0, 0.3, "HASHTAGS", size=8, color=MUTED, bold=True)
chip(s, 1.35, 5.92, 1.75, "#BarangaBadman", color=CYAN)
chip(s, 3.25, 5.92, 2.35, "#ChaptersINeverWrote", color=TEXT)
chip(s, 5.75, 5.92, 2.15, "#YouKnowItsBaranga", color=GOLD)
footer(s, "Positioning & Strategy", 9)
notes(s, "Read the positioning statement aloud, verbatim — it’s written to be said. Then walk the six pillars left to right and land the operating rule: “Content engine is non-negotiable; paid only amplifies what organic proves.” The hashtags are the spine of the UGC program — every post in weeks 1–12 carries at least one. If questioned on the WhatsApp channel, remind them email fails for this demo — WhatsApp is where UG Gen Z lives.")

# ============ SLIDE 10 — VISUAL IDENTITY ============
s = new_slide()
kicker(s, "Visual Identity Guidelines")
title(s, [[("DARK. ", {}), ("NEON.", {"color": CYAN}), (" UNMISTAKABLY ", {}), ("UG.", {"color": GOLD})]])
txt(s, 0.55, 1.4, 5.0, 0.28, "CORE PALETTE", size=9, bold=True, color=MUTED)
swatches = [("Void Black","#07070F · base","07070F"),("Deep Navy","#12122A · panels","12122A"),("Electric Blue","#2FD6FF · energy","2FD6FF"),("Gold","#F5C542 · premium","F5C542"),
            ("UG Yellow","#FCD116 · flag","FCD116"),("UG Red","#D90000 · flag","D90000"),("Neon Pink","#FF4FD8 · pop","FF4FD8"),("Street Green","#34D399 · go","34D399")]
for i,(n,d,hexv) in enumerate(swatches):
    x, y = 0.55 + (i%4)*1.62, (1.75 if i<4 else 3.0)
    box(s, x, y, 1.45, 0.85, fill=hexv, line=LINE, round_=True)
    txt(s, x, y+0.92, 1.45, 0.25, n, size=8, bold=True)
    txt(s, x, y+1.13, 1.45, 0.22, d, size=6.5, color=MUTED)
panel(s, 0.55, 4.75, 6.4, 1.85, fill=PANEL2)
txt(s, 0.8, 4.88, 6.0, 0.25, "TYPOGRAPHY", size=8, color=CYAN, bold=True)
txt(s, 0.8, 5.18, 6.0, 0.35, "ARCHIVO BLACK / MONTSERRAT", size=16, font=HEAD_FONT)
txt(s, 0.8, 5.6, 6.0, 0.9, "Headings: heavy display sans, uppercase, tight leading. Body: Montserrat 400/600. Accents: letterspaced all-caps kickers. No serif. No thin weights on dark.", size=8.5, color=MUTED, line_spacing=1.25)
panel(s, 7.2, 1.4, 2.55, 3.15, accent=GREEN, accent_side="top")
txt(s, 7.4, 1.55, 2.2, 0.28, "DO", size=10, bold=True, color=GREEN)
dos = ["Raw, candid BTS & rehearsal moments","Luganda / Runyoro flavor in captions","UGC-first formats; fan reposts over polish","Album art & wordmark on everything","Neon-on-black contrast; bold type"]
yy = 1.98
for d in dos:
    txt(s, 7.4, yy, 2.2, 0.5, [[("✓ ", {"color": GREEN, "bold": True}), (d, {"size": 7, "color": "D9D9EC"})]], line_spacing=1.1)
    yy += 0.5
panel(s, 9.95, 1.4, 2.55, 3.15, accent=RED, accent_side="top")
txt(s, 10.15, 1.55, 2.2, 0.28, "DON’T", size=10, bold=True, color="FF8A8A")
donts = ["Overly polished corporate stock","Generic “African” tropes / safari clichés","Busy layouts — one message per frame","Unverified stream claims in creative","Inconsistent wordmark casing (“baranga” ✗)"]
yy = 1.98
for d in donts:
    txt(s, 10.15, yy, 2.2, 0.5, [[("✕ ", {"color": RED, "bold": True}), (d, {"size": 7, "color": "D9D9EC"})]], line_spacing=1.1)
    yy += 0.5
pic(s, f"{ASSETS}/cover-chapters.jpg", 7.2, 4.75, w=5.3, h=1.7)
footer(s, "Visual Identity", 10)
notes(s, "Hand this slide to whoever designs — it’s the spec, not inspiration. Non-negotiables: void-black base, one neon accent per composition, Archivo Black for anything under three words. The do/don’t split matters because emerging artists lose identity through inconsistency, not bad taste. The QR belongs on slide 17 — keep identity clean here; functionality lives later.")

# ============ SLIDE 11 — TIMELINE OVERVIEW ============
s = new_slide()
kicker(s, "12-Week Timeline Overview")
title(s, [[("THREE ", {}), ("PHASES", {"color": CYAN}), (", ONE ", {}), ("ARC", {"color": GOLD})]])
phases = [
    ("WEEKS 1–4","FOUNDATION & AWARENESS", CYAN, "#14263B",
     "Launch the Badman challenge, origin series & UGC seeding. Lock identity, ship consistently, get into every UG Gen Z feed daily.",
     ["W1: Launch — challenge video + dance tutorial + album trailer","W2: Origin series — SALO, name meaning, Munyoro pride","W3: UGC seed — duets, stitches, first boost on winner","W4: Deep-cut teasers + mid-phase community poll"],
     "GOAL: BE EVERYWHERE, FAST"),
    ("WEEKS 5–8","ENGAGEMENT & GROWTH", MAGENTA, "#2B1430",
     "Convert viewers to fans: duets, lives, BTS, breakdowns, collaborations and first paid support on proven creatives.",
     ["W5: Fan duets, Q&A lives, lyric breakdowns","W6: Peak challenges + collab shoutouts (STANDO / Ace Kaawa)","W7: Paid on winners + heavy playlist push","W8: Testimonials + “fills the gap” + mid-campaign review"],
     "GOAL: VIEWS → FANBASE"),
    ("WEEKS 9–12","AMPLIFY · CONVERT · SUSTAIN", GOLD, "#2C2410",
     "Scale what worked, ask for the save/follow/stream, stack social proof, and leave behind a system — not a spike.",
     ["W9: Scale top content + hard CTAs + radio lives","W10: Collab pushes + fan campaigns + media features","W11: Social-proof recaps + community join pushes","W12: Recap video + finale challenge + sustain roadmap"],
     "GOAL: MAKE IT STICK"),
]
for i,(wk,name,acc,fill,desc,items,goal) in enumerate(phases):
    x = 0.55 + i*4.18
    panel(s, x, 1.45, 3.95, 4.75, fill=fill)
    txt(s, x+0.25, 1.62, 3.45, 0.45, wk, size=22, font=HEAD_FONT, color=acc)
    txt(s, x+0.25, 2.1, 3.45, 0.3, name, size=9.5, bold=True, color=TEXT)
    txt(s, x+0.25, 2.48, 3.45, 1.0, desc, size=8, color=MUTED, line_spacing=1.22)
    yy = 3.5
    for it in items:
        txt(s, x+0.25, yy, 3.45, 0.42, [[("▸ ", {"color": acc}), (it, {"size": 7.5, "color": "DCDCEC"})]], line_spacing=1.12)
        yy += 0.42
    box(s, x+0.25, 5.45, 3.45, 0.28, fill="0B0B1A", line=acc, line_w=0.75)
    txt(s, x+0.25, 5.485, 3.45, 0.22, goal, size=7, bold=True, color=acc, align=PP_ALIGN.CENTER)
footer(s, "Timeline", 11)
notes(s, "Draw the arc in the air: attention → affection → action. Foundation (be seen), Engagement (be felt), Amplify/Convert/Sustain (be chosen, then be kept). Emphasize paid media appears only in phase 2, only on creatives already winning organically — the discipline that keeps the budget honest. The weekly grid follows on slides 12–15.")

# ============ SLIDE 12 — CALENDAR OVERVIEW ============
s = new_slide()
kicker(s, "12-Week Content Calendar · Overview")
title(s, [[("THE ", {}), ("WEEKLY RHYTHM", {"color": CYAN})]])
panel(s, 0.55, 1.4, 6.3, 4.35)
txt(s, 0.8, 1.52, 5.8, 0.28, "STANDING WEEKLY CADENCE (CUSTOMIZE TO SHOOT DATES)", size=8, color=CYAN, bold=True)
tbl_rows = [
    ("SLOT","FREQUENCY","OWNER"),
    ("Short-form video (TikTok / Reels / Shorts)","4–7× / week","Content lead + artist"),
    ("Stories (BTS, polls, reposts)","3–5× / day","Artist + community mgr"),
    ("Long-form (YouTube / Live / interview)","1–2× / week","Video lead"),
    ("Playlist pitch + blog/radio outreach","1× / week · Fri","Promo lead"),
    ("Community reply session (“Baranga answers”)","1× / week · Sun","Community mgr"),
    ("Metrics review + calendar tweak","Bi-weekly · Fri","Whole team · 30 min"),
]
ty = 1.92
for j,(a,b,c_) in enumerate(tbl_rows):
    if j == 0:
        txt(s, 0.8, ty, 3.4, 0.25, a, size=7.5, color=MUTED, bold=True)
        txt(s, 4.0, ty, 1.35, 0.25, b, size=7.5, color=MUTED, bold=True)
        txt(s, 5.35, ty, 1.5, 0.25, c_, size=7.5, color=MUTED, bold=True)
        box(s, 0.8, ty+0.24, 6.0, 0.012, fill=CYAN, round_=False)
        ty += 0.35
        continue
    txt(s, 0.8, ty, 3.25, 0.45, a, size=7.5, bold=(j==1), color=TEXT, line_spacing=1.05)
    txt(s, 4.0, ty, 1.3, 0.45, b, size=7.5, color=GOLD, bold=True, line_spacing=1.05)
    txt(s, 5.35, ty, 1.55, 0.45, c_, size=7, color=MUTED, line_spacing=1.1)
    box(s, 0.8, ty+0.4, 6.0, 0.008, fill=LINE, round_=False)
    ty += 0.52
txt(s, 0.8, 5.62, 5.9, 0.3, "Daily stand-up: 15-min morning batch (“what ships today?”) + evening community sweep. Friday = numbers, not feelings.", size=8, color=MUTED, line_spacing=1.2)
phase_cards = [
    ("WEEKS 1–4 · FOUNDATION", CYAN, "Launch challenge · origin series · UGC seeding · deep-cut teasers (KAMPALA, PARADISE) · mid-phase poll. Theme: “You know it’s Baranga.”"),
    ("WEEKS 5–8 · ENGAGEMENT", MAGENTA, "Fan duets · BTS · lyric breakdowns · peak challenges · collab shoutouts · paid on winners · “fills the gap”. Theme: “Baranga is for us.”"),
    ("WEEKS 9–12 · AMPLIFY", GOLD, "Scale winners · streaming CTAs · lives & radio · fan campaigns · social-proof recaps · finale + 2027 roadmap. Theme: “You knew it.”"),
]
for i,(t,acc,d) in enumerate(phase_cards):
    y = 1.4 + i*1.55
    panel(s, 7.15, y, 5.6, 1.35, accent=acc)
    txt(s, 7.4, y+0.12, 5.1, 0.28, t, size=9, bold=True, color=acc)
    txt(s, 7.4, y+0.42, 5.1, 0.85, d, size=8, color="DCDCEC", line_spacing=1.25)
footer(s, "Calendar Overview", 12)
notes(s, "This is the operational heartbeat — hand it out as a one-pager. Walk the cadence table first, then the three phase themes. These are working rhythms, not commandments: if a challenge underperforms in week 2, the format gets cut by week 3. The three taglines map 1:1 to the phases — “You know it’s Baranga” (awareness), “Baranga is for us” (belonging), “You knew it” (vindication). Print the calendar appendix (slides 13–15) before the meeting.")

print("Slides 5–12 built")

# ============ SLIDES 13–15 — DETAILED CALENDAR ============
def calendar_slide(page, kicker_txt, runs, weeks):
    s = new_slide()
    kicker(s, kicker_txt)
    title(s, runs)
    cw, gap = 3.0, 0.14
    for i,(wk,tag,items,hook) in enumerate(weeks):
        x = 0.55 + i*(cw+gap)
        panel(s, x, 1.42, cw, 4.6, fill=PANEL)
        txt(s, x+0.16, 1.52, cw-0.32, 0.3, wk, size=10, bold=True, color=CYAN, font=HEAD_FONT)
        txt(s, x+0.16, 1.8, cw-0.32, 0.22, tag.upper(), size=6.5, bold=True, color=MUTED)
        yy = 2.1
        for day, body in items:
            txt(s, x+0.16, yy, cw-0.32, 0.52, [[(day+" ", {"bold": True, "color": TEXT, "size": 7}), (body, {"color": "D5D5E8", "size": 7})]], line_spacing=1.12)
            yy += 0.475
        box(s, x+0.16, 5.32, cw-0.32, 0.008, fill=GOLD, round_=False)
        txt(s, x+0.16, 5.4, cw-0.32, 0.55, hook, size=6.5, color=GOLD, line_spacing=1.15, anchor=MSO_ANCHOR.TOP)
    footer(s, kicker_txt.split("·")[-1].strip().title(), page)
    return s

s13 = calendar_slide(13, "Detailed Calendar · Weeks 1–4 · Foundation",
    [[("FOUNDATION ", {}), ("& ", {"color": MUTED}), ("AWARENESS", {"color": GOLD})]],
    [("WEEK 1 — LAUNCH","Go time",[
        ("Mon:","“You know it’s Baranga” intro + pinned post everywhere"),
        ("Tue:","#BarangaBadman dance challenge launch (60–90s tutorial)"),
        ("Wed:","CHAPTERS I NEVER WROTE album trailer (15–30s)"),
        ("Thu:","Fan challenge reposts + artist comment-everywhere sweep"),
        ("Fri:","Soft playlist submissions + NRG Radio UG press blast"),
        ("Wknd:","Hashtag blast; first WhatsApp Channel community poll")],
     "“High school to Badman — you know it’s Baranga 🔥 Link in bio #BarangaBadman”"),
     ("WEEK 2 — ORIGIN SERIES","The story",[
        ("Ep 1:","High-school story — writing SALO in class (B-roll + talking head)"),
        ("Ep 2:","“Baranga means…” — name meaning + hometown reveal"),
        ("Ep 3:","SALO true-story clip — what really happened (tasteful)"),
        ("Ep 4:","Munyoro pride — roots, family, uncle in the industry"),
        ("Also:","Radio clip shares + NRG interview snippets cut vertical")],
     "“Everyone asked where Badman came from. Ep 1: a classroom in western Uganda.”"),
     ("WEEK 3 — UGC SEED","The people",[
        ("Prompt:","Duet/stitch “Do your Badman verse” + lyric-challenge template"),
        ("Outreach:","DM 50 micro-creators (5K–100K) w/ pre-cleared audio + brief"),
        ("Feature:","Early fan-feature carousel — 10 fan covers/duets officially reposted"),
        ("Boost:","First paid push (UGX 100–150K) on week-1 winner post"),
        ("Media:","Red Pepper, Sqoop, UG blogs — pitch the origin story")],
     "“I don’t need you to sing it right. I need you to feel it — duet me.”"),
     ("WEEK 4 — DEEP CUTS","Album push",[
        ("Teases:","KAMPALA (DEEJAY KLVN) + PARADISE (TUNGI) — 20s visual snippets"),
        ("Recap:","“The first 21 days of Badman” mid-phase reel"),
        ("Poll:","“Which chapter hits hardest?” — WhatsApp + IG Stories"),
        ("Playlist:","Re-pitch with refreshed streaming proof"),
        ("Review:","Bi-weekly metrics review #1 — lock week 5–8 priorities")],
     "“KAMPALA is the chapter nobody saw coming. Midnight drops soon.”")])
notes(s13, "Week 1 is non-negotiable shipping discipline — if content slips here, nothing else matters. Week 2 is the heart: the origin series is what no competitor can copy. Watch UGC quality in week 3, not quantity — one great stitch beats 50 lazy ones. The week-4 poll is data disguised as engagement: the winning ‘chapter’ becomes the serviced single for weeks 5–8. Budget guardrail: boost only the single best post of the week.")

s14 = calendar_slide(14, "Detailed Calendar · Weeks 5–8 · Engagement",
    [[("ENGAGEMENT ", {}), ("& ", {"color": MUTED}), ("GROWTH", {"color": GOLD})]],
    [("WEEK 5 — FANS FIRST","Closeness",[
        ("Recap:","Fan duet/stitch roundup #2 — bigger, glossier, fan-credited"),
        ("Live:","IG/TikTok Live Q&A — 45–60 min, promo’d 3 days ahead"),
        ("BTS:","Studio session footage (tracking SALO vocals)"),
        ("Breakdowns:","1 verse/day for the KAMPALA & Badman bars"),
        ("Community:","First “fans only” voice note from Baranga (WhatsApp)")],
     "“Ask me anything — no PR filter, no manager on the line.”"),
     ("WEEK 6 — PEAK CHALLENGE","Momentum",[
        ("Push:","Peak challenge — STANDO clip duet + Ace Kaawa shoutout tree"),
        ("Formats:","“Day-in-the-life” + “rate my outfit” streetwear reels"),
        ("Shoutouts:","Peer collab tags (STANDO, Ace Kaawa, King Avo) — reciprocity"),
        ("Listen:","Stream-party for the W4 poll-winning album track"),
        ("UGC:","Mid-campaign creator leaderboard — public shoutout")],
     "“STANDO gave me the nod. King Avo ran the chorus. We’re just getting started.”"),
     ("WEEK 7 — PAID PUSH","Amplify",[
        ("Ads:","UG + diaspora lookalikes on week 1–6 winning creatives only"),
        ("Seeding:","20 mid-tier UG creators get merch + brief"),
        ("Playlist:","Heavy pitch week — resubmit Badman + KAMPALA w/ proof pack"),
        ("Radio:","NRG Radio UG interview airing + podcast booking push"),
        ("Geo:","Kampala, Mbarara, Fort Portal, London, Toronto")],
     "“The whole city can hear it from here. Kampala → the world.”"),
     ("WEEK 8 — PROOF & PIVOT","Mid-review",[
        ("Fans:","“What Badman means to me” — 3–4 fan testimonial videos"),
        ("Doc:","“Baranga fills the gap” — 90s editorial mini-doc"),
        ("Report:","Mid-campaign: streams, listeners, followers, UGC vs targets"),
        ("Optimize:","Kill flat formats, double winners, re-cut captions"),
        ("Review:","Bi-weekly metrics review #2 — reset week 9–12 if needed")],
     "“Two months ago nobody knew the name. Today the blogs are learning it.”")])
notes(s14, "Weeks 5–8 is where vanity becomes community. The live Q&A is the highest-trust hour of the campaign — protect it from scripts. In week 7, paid exists only to pour fuel on organic fire; if an ad outperforms organic, ask why the content team didn’t make it first. Week 8 is the honesty checkpoint: if targets are missed, reset them here — never in week 11 under pressure.")

s15 = calendar_slide(15, "Detailed Calendar · Weeks 9–12 · Amplify",
    [[("AMPLIFY · CONVERT · SUSTAIN", {})]][0] and [[("AMPLIFY · CONVERT · ", {}), ("SUSTAIN", {"color": GOLD})]],
    [("WEEK 9 — SCALE WINNERS","Push",[
        ("Scale:","Top-3 creatives re-cut with fresh hooks"),
        ("CTAs:","Save · follow · stream Badman + album deep cuts — everywhere"),
        ("Lives:","Radio lives + IG/TikTok Live run — 2× this week"),
        ("Anthem:","“Badman is for us” fan-anthem reel — fans as chorus"),
        ("Playlist:","Re-pitch with updated social-proof numbers")],
     "“Save it. Stream it. It’s already in the taxi playlist.”"),
     ("WEEK 10 — COLLAB PUSH","Network",[
        ("Collabs:","STANDO, Andrinah, Ace Kaawa, King Avo — joint posts + stories"),
        ("Fan push:","#YouKnowItsBaranga — best fan story featured officially"),
        ("Media:","1 long-form interview (NRG/podcast) + 2 blog features"),
        ("Community:","“Badman army” broadcast — coordinate listening sessions")],
     "“This is what happens when Kampala raps together.”"),
     ("WEEK 11 — SOCIAL PROOF","Convert",[
        ("Recap:","“X fans, Y videos, Z streams — you did this”"),
        ("CTAs:","Pre-save next single + follow @_baranga push"),
        ("Community:","Drive WhatsApp/Discord to the 5K milestone"),
        ("Shows:","Booking outreach with fresh metrics pack (mgmt/venues)"),
        ("Review:","Bi-weekly metrics review #3 — final stretch lock")],
     "“Numbers don’t lie. Check the streams — then join the army.”"),
     ("WEEK 12 — FINALE","Land it",[
        ("Recap:","Big recap video — 12 weeks in 90 seconds, the receipts"),
        ("Thanks:","Thank-you post + finale challenge — one last #BarangaBadman wave"),
        ("Roadmap:","2027 sustain reveal (next single + tour hint)"),
        ("Report:","Full campaign report teaser for management/labels"),
        ("Debrief:","Post-campaign review + evergreen content bank handover")],
     "“You knew it. Now 2027 begins. — You know it’s Baranga.”")])
notes(s15, "Week 9 is the “ask” phase — after eight weeks of giving, it’s fair to explicitly request saves, follows and streams, and fans will respond. Week 10 leans on the collab web as distribution; every partner post is a mini-launch. Week 11 converts attention into owned audience; the 5K WhatsApp milestone outlives the algorithm. Close week 12 with gratitude, not noise — the recap video is the case study for labels and venues.")

# ============ SLIDE 16 — METRICS ============
s = new_slide()
kicker(s, "Success Metrics & Tracking")
title(s, [[("IF IT ISN’T ", {}), ("MEASURED", {"color": CYAN}), (", IT DIDN’T ", {}), ("HAPPEN", {"color": GOLD})]])
panel(s, 0.55, 1.4, 6.5, 4.6)
txt(s, 0.8, 1.52, 6.0, 0.28, "KPI TARGETS — BASELINE → WEEK 12", size=8, color=CYAN, bold=True)
kpi_rows = [("METRIC","BASELINE*","TARGET (W12)","SOURCE"),
    ("Spotify monthly listeners","~4,042","8–12K (2–3×)","Spotify for Artists"),
    ("Badman + album streams / 28d","311K+ cumulative","+50–100% WoW","Spotify for Artists"),
    ("Followers added (IG/TikTok/YT)","—","+10–15K","Native analytics"),
    ("#BarangaBadman UGC videos","0","≥ 500 tagged posts","TikTok / IG tags"),
    ("Playlist adds (editorial/indie)","—","≥ 3 incl. 1 UG editorial","SubmitHub / direct"),
    ("Radio / interview slots","—","≥ 2 (NRG Radio UG)","Booking log"),
    ("Live show / showcase booked","—","≥ 1 (Kampala + western UG)","Venue LOI / poster"),
    ("WhatsApp / Discord community","0","≥ 5,000 members","Channel analytics")]
ty = 1.92
for j,(a,b,c_,d) in enumerate(kpi_rows):
    if j == 0:
        for x,t,w in [(0.8,a,2.3),(3.1,b,1.15),(4.25,c_,1.15),(5.4,d,1.5)]:
            txt(s, x, ty, w, 0.22, t, size=6.5, bold=True, color=MUTED)
        box(s, 0.8, ty+0.22, 6.0, 0.012, fill=CYAN, round_=False)
        ty += 0.32; continue
    txt(s, 0.8, ty, 2.3, 0.35, a, size=7.5, color=TEXT, line_spacing=1.05)
    txt(s, 3.1, ty, 1.15, 0.35, b, size=7, color=MUTED, line_spacing=1.05)
    txt(s, 4.25, ty, 1.15, 0.35, c_, size=7.5, bold=True, color=GOLD, line_spacing=1.05)
    txt(s, 5.4, ty, 1.5, 0.35, d, size=6.5, color=MUTED, line_spacing=1.1)
    box(s, 0.8, ty+0.33, 6.0, 0.008, fill=LINE, round_=False)
    ty += 0.42
txt(s, 0.8, 5.85, 6.1, 0.35, "*Public approximations at research time — refresh all baselines in Week 0. 12-week window: Dec 2026 → Feb 2027.", size=6.5, color="5C5C78", line_spacing=1.15)
panel(s, 7.3, 1.4, 5.5, 2.15, fill=PANEL2)
txt(s, 7.55, 1.52, 5.0, 0.25, "GROWTH CURVE (ILLUSTRATIVE)", size=8, color=CYAN, bold=True)
from pptx.util import Pt as _Pt
from lxml import etree
# simple line chart via freeform: use an arc of connected lines (polyline) through chevrons
pts = [(7.6,3.05),(8.45,2.98),(9.3,2.82),(10.15,2.5),(11.0,2.1),(11.85,1.78),(12.55,1.58)]
for k in range(len(pts)-1):
    x1,y1 = pts[k]; x2,y2 = pts[k+1]
    ln = s.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = C(CYAN); ln.line.width = Pt(2.5)
box(s, 7.6, 1.95, 4.9, 0.006, fill=LINE, round_=False)
txt(s, 7.55, 3.15, 5.0, 0.25, "Baseline ~4K → target 8–12K monthly listeners (2–3×)", size=7, color=MUTED)
panel(s, 7.3, 3.75, 5.5, 1.15)
txt(s, 7.55, 3.85, 5.0, 0.25, "TOOLSTACK", size=8, color=CYAN, bold=True)
chip(s, 7.55, 4.22, 1.6, "Spotify for Artists", color=CYAN)
chip(s, 9.3, 4.22, 1.45, "YouTube Studio")
chip(s, 10.9, 4.22, 1.75, "IG / TikTok Insights")
chip(s, 7.55, 4.62, 1.7, "Metricool / Sprout", color=GOLD)
chip(s, 9.4, 4.62, 1.55, "SubmitHub")
chip(s, 11.1, 4.62, 1.55, "GA4 · UTM links", color=GREEN)
panel(s, 7.3, 5.1, 5.5, 0.9, accent=RED)
txt(s, 7.55, 5.2, 5.0, 0.25, "RED FLAGS", size=8, bold=True, color="FF8A8A")
txt(s, 7.55, 5.46, 5.1, 0.5, "Boosting flat creatives “because we paid” · chasing vanity followers over saves · skipping Friday reviews in weeks 5–11.", size=7.5, color="D9D9EC", line_spacing=1.2)
footer(s, "Metrics", 16)
notes(s, "Set the rule: metrics are reviewed Friday, decisions made Friday — never mid-week on emotion. The illustrative curve is not a promise; it’s the expected shape if the engine holds: flat weeks 1–2 (seeding), inflection at week 3 (UGC), compounding from week 6. If actuals beat target, bank learnings for 2027; if they miss, diagnose in this order: hook quality → posting cadence → CTA clarity → paid efficiency. Red flags are behaviors, not metrics — call them out by name in every review.")

# ============ SLIDE 17 — NEXT STEPS ============
s = new_slide()
kicker(s, "Next Steps & Call to Action")
title(s, [[("LET’S ", {}), ("SHIP IT", {"color": GOLD})]])
steps = ["Lock budget, channels & asset list (W0 — this week)",
         "Build the full calendar in Notion / Google Sheets — assign owners",
         "Shoot & edit Week 1 assets: intro, dance tutorial, album trailer",
         "Set up tracking: Spotify for Artists, dashboards, UTM links",
         "Align with Baranga & management — availability, approvals, fit checks",
         "Launch Week 1 — target: first full week of December 2026"]
for i, st in enumerate(steps):
    y = 1.5 + i*0.78
    box(s, 0.55, y, 7.5, 0.66, fill=PANEL if i%2==0 else PANEL2, line=LINE)
    box(s, 0.75, y+0.13, 0.42, 0.42, fill="0B2A1A", line=GREEN, line_w=1.5)
    txt(s, 0.75, y+0.135, 0.42, 0.4, "✓", size=18, bold=True, color=GREEN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 1.4, y+0.05, 6.5, 0.55, st, size=10.5, color="E8E8F5", anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15)
panel(s, 8.35, 1.5, 4.4, 1.9, fill=PANEL2)
txt(s, 8.55, 1.62, 4.0, 0.25, "COUNTDOWN TO LAUNCH", size=8, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
txt(s, 8.35, 1.95, 4.4, 0.95, [[("T–7 ", {"font": HEAD_FONT, "size": 54, "color": CYAN}), ("DAYS", {"size": 16, "color": MUTED, "bold": True})]], align=PP_ALIGN.CENTER)
txt(s, 8.55, 2.95, 4.0, 0.3, "Week 0 starts when budget & assets are signed off", size=7.5, color=MUTED, align=PP_ALIGN.CENTER)
panel(s, 8.35, 3.6, 4.4, 2.4, fill=PANEL2)
txt(s, 8.55, 3.72, 4.0, 0.25, "SCAN → STREAM", size=8, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
# QR-ish placeholder drawn with rectangles
import random
random.seed(42)
qx, qy, cell = 9.85, 4.08, 0.085
for r in range(9):
    for c_ in range(9):
        corner = (r<3 and c_<3) or (r<3 and c_>5) or (r>5 and c_<3)
        if corner:
            continue
        if random.random() > 0.52:
            box(s, qx+c_*cell, qy+r*cell, cell*0.92, cell*0.92, fill=TEXT, round_=False)
for fx_, fy_ in [(0,0),(6,0),(0,6)]:
    box(s, qx+fx_*cell, qy+fy_*cell, cell*3, cell*3, fill=TEXT, round_=False)
    box(s, qx+(fx_+0.7)*cell, qy+(fy_+0.7)*cell, cell*1.6, cell*1.6, fill="0D0D1F", round_=False)
    box(s, qx+(fx_+1.15)*cell, qy+(fy_+1.15)*cell, cell*0.7, cell*0.7, fill=TEXT, round_=False)
txt(s, 8.55, 4.95, 4.0, 0.35, "open.spotify.com — search “Baranga”\n@_baranga everywhere", size=8, color="D9D9EC", align=PP_ALIGN.CENTER, line_spacing=1.3)
footer(s, "Next Steps", 17)
notes(s, "Close with energy. The ask is explicit: sign-off on budget and launch date, and artist commitment to the weekly cadence — without the artist posting, none of this runs. Assign owners in the room. The QR is a live placeholder — generate the final Spotify QR in Spotify for Artists once the campaign URL is confirmed. End on: “Week 1 is either a launch or a missed window. Let’s pick launch.”")

# ============ SLIDE 18 — THANK YOU ============
s = new_slide()
pic(s, f"{ASSETS}/closing-neon.jpg", 0, 0, w=W, h=H)
box(s, 0, 4.6, W, 2.9, fill="020208")
# soften band
txt(s, 0.7, 5.0, 6.0, 0.3, "THANK YOU", size=10, bold=True, color=GOLD)
txt(s, 0.7, 5.3, 11.9, 1.15, [[("Let’s make them ", {}), ("know it’s Baranga.", {"color": GOLD})]], size=38, font=HEAD_FONT, line_spacing=1.0)
txt(s, 0.7, 6.55, 11.9, 0.3, "Spotify · Apple Music · YouTube · Shazam — search “Baranga”   |   @_baranga on IG / TikTok   |   #BarangaBadman", size=10, color=TEXT, bold=True)
txt(s, 0.7, 6.95, 12.0, 0.5, "Credits & sources: Spotify · Apple Music · Shazam · YouTube · Musixmatch · Audiomack · NRG Radio UG · official releases (SALO, Badman, Party Riddim, CHAPTERS I NEVER WROTE). Deck artwork (portrait, covers, neon) is AI-generated concept art. 12 weeks · Dec 2026 → Feb 2027 · Kampala × Western Uganda.", size=6.5, color="B9B9D4", line_spacing=1.25)
notes(s, "Leave the neon image up after you stop talking — it does the closing for you. If asked for the single most important thing: “Protect the Friday metrics review and the Sunday reply session — everything else is execution.” If asked about next steps beyond 12 weeks: 2027 single cycle, live showcase in Kampala + western Uganda, and a label/distribution conversation backed by this report. Thank the artist and management by name if they’re in the room.")

prs.save(OUT)
print("Saved", OUT, "with", len(prs.slides._sldIdLst), "slides")
