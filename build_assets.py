#!/usr/bin/env python3
"""Generate the BARANGA campaign PDF, PPTX and browser data wrapper."""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "campaign.json"
DOWNLOADS = ROOT / "downloads"
DERIVED = ROOT / "assets" / "campaign" / "derived"
PDF_PATH = DOWNLOADS / "Baranga_12-Week_Campaign_Strategy.pdf"
PPTX_PATH = DOWNLOADS / "Baranga_12-Week_Campaign_Slides.pptx"
LEGACY_PPTX = ROOT / "Baranga_12-Week_Marketing_Campaign.pptx"
JS_DATA = ROOT / "assets" / "js" / "campaign-data.js"

DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
M = DATA["meta"]
ASSETS = DATA["assets"]
SOURCES = DATA["sources"]
SLIDES = DATA["slides"]
PAGE_W, PAGE_H = 13.333 * inch, 7.5 * inch

INK = colors.HexColor("#0B0D14")
PANEL = colors.HexColor("#151925")
GOLD = colors.HexColor("#F5C542")
RED = colors.HexColor("#EE3B39")
CYAN = colors.HexColor("#26D7EE")
GREEN = colors.HexColor("#43D39E")
TEXT = colors.HexColor("#F6F7FB")
MUTED = colors.HexColor("#9CA4B8")
LINE = colors.HexColor("#2B3040")

PPT_BG = RGBColor(0x07, 0x08, 0x0D)
PPT_PANEL = RGBColor(0x16, 0x1B, 0x27)
PPT_PANEL_2 = RGBColor(0x1D, 0x22, 0x30)
PPT_GOLD = RGBColor(0xF5, 0xC5, 0x42)
PPT_RED = RGBColor(0xEE, 0x3B, 0x39)
PPT_CYAN = RGBColor(0x26, 0xD7, 0xEE)
PPT_GREEN = RGBColor(0x43, 0xD3, 0x9E)
PPT_TEXT = RGBColor(0xF6, 0xF7, 0xFB)
PPT_MUTED = RGBColor(0x9C, 0xA4, 0xB8)
PPT_LINE = RGBColor(0x2B, 0x30, 0x40)


def source_by_id(source_id: str):
    return next((s for s in SOURCES if s["id"] == source_id), None)


def write_js_data() -> None:
    payload = json.dumps(DATA, ensure_ascii=False, indent=2)
    JS_DATA.write_text(
        "/* Generated from data/campaign.json — do not edit by hand. */\n"
        f"window.CAMPAIGN_DATA = {payload};\n",
        encoding="utf-8",
    )


def prepare_images() -> dict:
    DERIVED.mkdir(parents=True, exist_ok=True)
    outputs = {}
    src = ROOT / ASSETS["artist_photo"]

    hero = Image.open(src).convert("RGB")
    hero = ImageOps.fit(hero, (1600, 900), method=Image.Resampling.LANCZOS, centering=(0.5, 0.28))
    hero = ImageEnhance.Color(hero).enhance(0.15)
    hero = ImageEnhance.Brightness(hero).enhance(0.48)
    overlay = Image.new("RGB", hero.size, (5, 6, 11))
    hero = Image.blend(hero, overlay, 0.35)
    p = DERIVED / "hero-bg.jpg"
    hero.save(p, quality=88)
    outputs["hero"] = p

    for key, rel in [("album", ASSETS["album_cover"]), ("badman", ASSETS["badman_cover"]),
                     ("party", ASSETS["party_cover"]), ("poster", ASSETS["vote_poster"])]:
        im = Image.open(ROOT / rel).convert("RGB")
        im = ImageOps.fit(im, (900, 900), method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
        p = DERIVED / f"{key}-square.jpg"
        im.save(p, quality=88)
        outputs[key] = p

    portrait = Image.open(src).convert("RGB")
    portrait = ImageOps.fit(portrait, (600, 1000), method=Image.Resampling.LANCZOS, centering=(0.5, 0.28))
    portrait = ImageEnhance.Color(portrait).enhance(0.18)
    portrait = ImageEnhance.Brightness(portrait).enhance(0.55)
    overlay = Image.new("RGB", portrait.size, (5, 6, 11))
    portrait = Image.blend(portrait, overlay, 0.32)
    p = DERIVED / "pdf-cover-portrait.jpg"
    portrait.save(p, quality=88)
    outputs["pdf_cover"] = p

    square = Image.open(src).convert("RGB")
    square = ImageOps.fit(square, (900, 900), method=Image.Resampling.LANCZOS, centering=(0.5, 0.3))
    p = DERIVED / "artist-square.jpg"
    square.save(p, quality=88)
    outputs["artist_square"] = p

    dark_square = ImageEnhance.Color(square).enhance(0.2)
    dark_square = ImageEnhance.Brightness(dark_square).enhance(0.52)
    overlay = Image.new("RGB", dark_square.size, (5, 6, 11))
    dark_square = Image.blend(dark_square, overlay, 0.3)
    p = DERIVED / "transition-square.jpg"
    dark_square.save(p, quality=88)
    outputs["transition"] = p

    note = Image.open(ROOT / ASSETS["concept_note"]).convert("RGB")
    note.thumbnail((820, 820), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (900, 900), (13, 16, 24))
    canvas.paste(note, ((900 - note.width) // 2, (900 - note.height) // 2))
    p = DERIVED / "concept-note-square.jpg"
    canvas.save(p, quality=88)
    outputs["concept"] = p
    return outputs


# ---------------------------------------------------------------------------
# PDF helpers
# ---------------------------------------------------------------------------

def register_pdf_fonts() -> None:
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    pdfmetrics.registerFont(TTFont("DejaVu", str(font_dir / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(font_dir / "DejaVuSans-Bold.ttf")))


def fit_text(text, font, size, max_w):
    text = str(text).replace("\n", " ")
    if pdfmetrics.stringWidth(text, font, size) <= max_w:
        return text
    out = text
    while out and pdfmetrics.stringWidth(out + "…", font, size) > max_w:
        out = out[:-1]
    return out.rstrip() + "…"


def wrap_lines(text, font, size, max_w):
    lines = []
    for para in str(text).split("\n"):
        words, line = para.split(), ""
        for word in words:
            candidate = (line + " " + word).strip()
            if pdfmetrics.stringWidth(candidate, font, size) <= max_w:
                line = candidate
            else:
                if line:
                    lines.append(line)
                while word and pdfmetrics.stringWidth(word, font, size) > max_w:
                    chunk = word
                    while chunk and pdfmetrics.stringWidth(chunk, font, size) > max_w:
                        chunk = chunk[:-1]
                    lines.append(chunk)
                    word = word[len(chunk):]
                line = word
        if line:
            lines.append(line)
    return lines


def draw_wrapped(c, text, x, y, w, font, size, color, leading=None, max_lines=None):
    leading = leading or size * 1.35
    lines = wrap_lines(text, font, size, w)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit_text(lines[-1] + "…", font, size, w)
    c.setFillColor(color)
    c.setFont(font, size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_image_contain(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2, width=dw, height=dh)


def link_rect(c, url, label, x, y, w, size=6.8, color=CYAN):
    if not url:
        return
    c.setFillColor(color)
    c.setFont("DejaVu", size)
    c.drawString(x, y, fit_text(label, "DejaVu", size, w))
    rel = 0 if url.startswith(("http://", "https://")) else 1
    c.linkURL(url, (x, y - 1.5, x + w, y + size + 1.5), relative=rel)


def draw_pdf_footer(c, n):
    W, H = PAGE_W, PAGE_H
    c.saveState()
    c.setFillColor(INK)
    c.rect(0, 0, W, 18 * mm, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(18 * mm, 15 * mm, W - 18 * mm, 15 * mm)
    c.setFont("DejaVu-Bold", 6.5)
    c.setFillColor(MUTED)
    c.drawString(18 * mm, 9 * mm, "7H · BARANGA · 2027")
    c.drawCentredString(W / 2, 9 * mm, "12-WEEK CAMPAIGN PLAN")
    c.setFillColor(GOLD)
    c.drawRightString(W - 18 * mm, 9 * mm, f"{n:02d} / 18")
    c.restoreState()


def draw_pdf_header(c, s, show_headline=True):
    W, H = PAGE_W, PAGE_H
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 5 * mm, W, 5 * mm, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 8)
    c.setFillColor(CYAN)
    c.drawString(18 * mm, H - 16 * mm, s["kicker"].upper())
    y = H - 34 * mm
    if show_headline:
        y = draw_wrapped(c, s["headline"], 18 * mm, y, W - 36 * mm, "DejaVu-Bold", 20, TEXT, leading=24, max_lines=2)
    if s.get("lede") and s["layout"] not in ("quote", "thanks"):
        draw_wrapped(c, s["lede"], 18 * mm, y - 2 * mm, W - 36 * mm, "DejaVu", 8.5, MUTED, leading=12, max_lines=3)


def draw_pdf_card(c, x, y, w, h, title, body, accent=GOLD, image=None, image_h=28 * mm):
    c.saveState()
    c.setFillColor(PANEL)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.roundRect(x, y, w, h, 3 * mm, stroke=1, fill=1)
    c.setFillColor(accent)
    c.rect(x, y + h - 1.3 * mm, w, 1.3 * mm, fill=1, stroke=0)
    title_y = y + h - 8 * mm
    body_y = title_y - 7 * mm
    if image:
        img_y = y + h - 8 * mm - image_h
        draw_image_contain(c, image, x + 4 * mm, img_y, w - 8 * mm, image_h)
        title_y = img_y - 6 * mm
        body_y = title_y - 6 * mm
    c.setFillColor(TEXT)
    c.setFont("DejaVu-Bold", 8.5)
    c.drawString(x + 4 * mm, title_y, fit_text(title, "DejaVu-Bold", 8.5, w - 8 * mm))
    if isinstance(body, (list, tuple)):
        body = "\n".join(f"• {x}" if not str(x).startswith("•") else str(x) for x in body)
    max_lines = max(1, int((body_y - y - 4 * mm) / 10.5))
    draw_wrapped(c, body, x + 4 * mm, body_y, w - 8 * mm, "DejaVu", 7.4, MUTED, leading=10.5, max_lines=max_lines)
    c.restoreState()


def draw_pdf_cards(c, cards, cols, top_mm, row_h_mm):
    W, H = PAGE_W, PAGE_H
    margin, gap = 18 * mm, 3 * mm
    card_w = (W - 2 * margin - (cols - 1) * gap) / cols
    for i, card in enumerate(cards):
        col, row = i % cols, i // cols
        x = margin + col * (card_w + gap)
        y = H - (top_mm + (row + 1) * row_h_mm + row * (gap / mm)) * mm
        draw_pdf_card(c, x, y, card_w, row_h_mm * mm, card.get("title", ""), card.get("body", ""),
                      card.get("accent", GOLD), card.get("image"), card.get("image_h", 28 * mm))


def draw_pdf_source_links(c, ids, top_mm=108):
    valid = [(sid, s) for sid in ids if (s := source_by_id(sid))]
    if not valid:
        return
    W, H = PAGE_W, PAGE_H
    c.setFont("DejaVu-Bold", 8)
    c.setFillColor(CYAN)
    c.drawString(18 * mm, H - top_mm * mm, "REFERENCES")
    cols = 2
    per_col = math.ceil(len(valid) / cols)
    col_w = (W - 36 * mm) / cols
    for i, (sid, s) in enumerate(valid):
        col, row = divmod(i, per_col)
        x = 18 * mm + col * col_w
        y = H - (top_mm + 8) * mm - row * 6.5 * mm
        link_rect(c, s["url"], f"{sid} · {s['label']}", x, y, col_w - 4 * mm, size=6.2)


def pdf_photo_slide(c, s, images, image_key):
    W, H = PAGE_W, PAGE_H
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 5 * mm, W, 5 * mm, fill=1, stroke=0)
    draw_image_contain(c, images[image_key], W * 0.54, 0.16 * H, W * 0.42, 0.68 * H)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.rect(W * 0.54, 0.16 * H, W * 0.42, 0.68 * H, fill=0, stroke=1)
    c.setFont("DejaVu-Bold", 8)
    c.setFillColor(CYAN)
    c.drawString(18 * mm, H - 18 * mm, s["kicker"].upper())
    y = draw_wrapped(c, s["headline"], 18 * mm, H - 52 * mm, W * 0.48, "DejaVu-Bold", 27, TEXT, leading=32, max_lines=2)
    if s.get("subhead"):
        y = draw_wrapped(c, s["subhead"], 18 * mm, y - 4 * mm, W * 0.48, "DejaVu-Bold", 15, GOLD, leading=20, max_lines=2)
    if s.get("lede"):
        y = draw_wrapped(c, s["lede"], 18 * mm, y - 8 * mm, W * 0.48, "DejaVu", 9.5, MUTED, leading=14, max_lines=6)
    if s.get("bullets"):
        body = "\n".join("• " + x for x in s["bullets"])
        draw_wrapped(c, body, 18 * mm, y - 6 * mm, W * 0.48, "DejaVu", 8, TEXT, leading=11, max_lines=6)


def pdf_equation_slide(c, s, images):
    W, H = PAGE_W, PAGE_H
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 5 * mm, W, 5 * mm, fill=1, stroke=0)
    draw_image_contain(c, images["album"], W * 0.54, 0.25 * H, W * 0.36, W * 0.36)
    c.setFont("DejaVu-Bold", 8)
    c.setFillColor(CYAN)
    c.drawString(18 * mm, H - 18 * mm, s["kicker"].upper())
    c.setFont("DejaVu-Bold", 22)
    c.setFillColor(TEXT)
    c.drawString(18 * mm, H - 62 * mm, s["headline"])
    c.setFont("DejaVu-Bold", 70)
    c.setFillColor(GOLD)
    c.drawString(18 * mm, H - 105 * mm, s["subhead"])
    draw_wrapped(c, s["lede"], 18 * mm, H - 132 * mm, W * 0.48, "DejaVu-Bold", 13, TEXT, leading=18, max_lines=3)


def pdf_standard_slide(c, s, images):
    draw_pdf_header(c, s, show_headline=s["layout"] != "thanks")
    layout = s["layout"]
    if layout == "bullets":
        body = "\n".join("• " + x for x in s["bullets"])
        draw_pdf_cards(c, [{"title": "THE PLAN", "body": body, "accent": GOLD}], 1, 46, 125)
    elif layout == "cards":
        cards = []
        accents = [GOLD, CYAN, RED, GREEN]
        for i, card in enumerate(s["cards"]):
            cards.append({"title": card["title"], "body": card["body"], "accent": accents[i % len(accents)]})
        cols = 3 if len(cards) == 3 else 2
        draw_pdf_cards(c, cards, cols, 46, 92)
    elif layout == "quote":
        cards = [
            {"title": "THE PROMISE", "body": "“" + s["quote"] + "”", "accent": GOLD},
            {"title": "HOW I’LL MAKE IT REAL", "body": s["lede"], "accent": CYAN},
        ]
        draw_pdf_cards(c, cards, 2, 46, 95)
    elif layout == "collage":
        cards = []
        image_map = {"album_cover": "album", "vote_poster": "poster", "artist_photo": "artist_square", "party_cover": "party"}
        for i, x in enumerate(s["images"]):
            cards.append({"title": x["title"], "body": x["body"], "image": images[image_map[x["asset"]]], "image_h": 30 * mm,
                          "accent": [GOLD, RED, CYAN, GREEN][i % 4]})
        draw_pdf_cards(c, cards, 4, 46, 92)
    elif layout == "timeline":
        cards = []
        accents = [GOLD, CYAN, RED, GREEN]
        for i, x in enumerate(s["cards"]):
            cards.append({"title": x["title"], "body": x["body"], "accent": accents[i % len(accents)]})
        draw_pdf_cards(c, cards, 2, 46, 39)
    elif layout == "thanks":
        c.setFont("DejaVu-Bold", 34)
        c.setFillColor(GOLD)
        W, H = PAGE_W, PAGE_H
        c.drawString(18 * mm, H - 70 * mm, s["headline"])
        draw_wrapped(c, s["lede"], 18 * mm, H - 88 * mm, W - 36 * mm, "DejaVu", 10, MUTED, leading=14, max_lines=2)
        draw_pdf_source_links(c, s["sources"], top_mm=108)
        c.setFont("DejaVu-Bold", 8)
        c.setFillColor(CYAN)
        c.drawString(18 * mm, 42 * mm, "KEEP THE FILES")
        link_rect(c, ASSETS["pdf"], "Strategy PDF · 18 pages", 18 * mm, 32 * mm, W * 0.42, size=7.5)
        link_rect(c, ASSETS["pptx"], "Editable slides · 18 slides", 18 * mm, 24 * mm, W * 0.42, size=7.5)
        link_rect(c, ASSETS["online_deck"], "Browser deck", W * 0.55, 32 * mm, W * 0.30, size=7.5)
        link_rect(c, "download.html", "Download page", W * 0.55, 24 * mm, W * 0.30, size=7.5)


def draw_pdf_slide(c, s, images):
    if s["layout"] == "cover":
        pdf_photo_slide(c, s, images, "pdf_cover")
    elif s["layout"] == "transition":
        pdf_photo_slide(c, s, images, "transition")
    elif s["layout"] == "artist":
        pdf_photo_slide(c, s, images, "artist_square")
    elif s["layout"] == "equation":
        pdf_equation_slide(c, s, images)
    else:
        pdf_standard_slide(c, s, images)
    draw_pdf_footer(c, s["no"])
    c.showPage()


def build_pdf(images) -> None:
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    register_pdf_fonts()
    c = pdfcanvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("BARANGA — My 2027 12-Week Campaign")
    c.setAuthor("7H Music Group · Campaign Engineer")
    c.setSubject("A 12-week campaign plan for Baranga")
    for s in SLIDES:
        draw_pdf_slide(c, s, images)
    c.save()


# ---------------------------------------------------------------------------
# PPTX helpers
# ---------------------------------------------------------------------------

def ppt_text(slide, x, y, w, h, text, size=18, color=PPT_TEXT, bold=False, align=PP_ALIGN.LEFT, font="Aptos", margin=0.04):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    p = tf.paragraphs[0]
    p.alignment = align
    p.text = str(text)
    for run in p.runs:
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return box


def ppt_bullets(slide, x, y, w, h, items, size=12, color=PPT_MUTED):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.02)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(5)
        p.text = f"• {item}"
        for run in p.runs:
            run.font.name = "Aptos"
            run.font.size = Pt(size)
            run.font.color.rgb = color
    return box


def ppt_card(slide, x, y, w, h, title=None, body=None, accent=PPT_GOLD, image=None, image_h=1.6):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = PPT_PANEL
    shape.line.color.rgb = PPT_LINE
    shape.line.width = Pt(0.8)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.055))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()
    yy = y + 0.18
    if image:
        slide.shapes.add_picture(str(image), Inches(x + 0.14), Inches(yy), Inches(w - 0.28), Inches(image_h))
        yy += image_h + 0.12
    if title:
        ppt_text(slide, x + 0.14, yy, w - 0.28, 0.52, title, size=12, color=PPT_TEXT, bold=True)
        yy += 0.58
    if body:
        if isinstance(body, list):
            ppt_bullets(slide, x + 0.12, yy, w - 0.24, max(0.35, y + h - yy - 0.08), body, size=10)
        else:
            ppt_text(slide, x + 0.14, yy, w - 0.28, max(0.35, y + h - yy - 0.08), body, size=10, color=PPT_MUTED)
    return shape


def ppt_hyperlink(slide, x, y, w, h, url, label, size=9, color=PPT_CYAN):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = label
    run.hyperlink.address = url
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.color.rgb = color
    return box


def ppt_slide(prs, title, kicker, notes, foot, hero=False, images=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = PPT_BG
    if hero and images and images.get("hero"):
        slide.shapes.add_picture(str(images["hero"]), 0, 0, prs.slide_width, prs.slide_height)
        shade = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.0), 0, prs.slide_width - Inches(6.0), prs.slide_height)
        shade.fill.solid()
        shade.fill.fore_color.rgb = PPT_BG
        shade.line.fill.background()
    else:
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.07))
        accent.fill.solid()
        accent.fill.fore_color.rgb = PPT_GOLD
        accent.line.fill.background()
        ppt_text(slide, 0.62, 0.28, 5.5, 0.25, kicker.upper(), size=9.5, color=PPT_CYAN, bold=True)
        ppt_text(slide, 0.62, 0.62, 12.0, 0.65, title, size=29, color=PPT_TEXT, bold=True, font="Arial")
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.62), Inches(6.93), Inches(12.1), Inches(0.012))
    line.fill.solid()
    line.fill.fore_color.rgb = PPT_LINE
    line.line.fill.background()
    ppt_text(slide, 0.62, 7.0, 5.0, 0.25, "7H · BARANGA · 2027", size=8, color=PPT_MUTED)
    ppt_text(slide, 5.5, 7.0, 5.7, 0.25, foot, size=8, color=PPT_MUTED, align=PP_ALIGN.CENTER)
    ppt_text(slide, 11.8, 7.0, 0.9, 0.25, f"{len(prs.slides):02d}", size=8, color=PPT_GOLD, align=PP_ALIGN.RIGHT)
    slide.notes_slide.notes_text_frame.text = notes
    return slide


def ppt_short(value, limit=120):
    value = str(value).replace("\n", " ")
    return value if len(value) <= limit else value[:limit - 1].rstrip() + "…"


def ppt_photo_slide(prs, s, images, image_key):
    slide = ppt_slide(prs, "", s["kicker"], s["notes"], s["foot"])
    slide.shapes.add_picture(str(images[image_key]), Inches(8.15), Inches(1.0), Inches(4.55), Inches(4.55))
    ppt_text(slide, 0.62, 1.45, 7.1, 1.1, s["headline"], size=36, color=PPT_TEXT, bold=True, font="Arial")
    if s.get("subhead"):
        ppt_text(slide, 0.62, 2.6, 7.1, 0.8, s["subhead"], size=22, color=PPT_GOLD, bold=True, font="Arial")
    y = 3.55 if s.get("subhead") else 2.75
    if s.get("lede"):
        ppt_text(slide, 0.62, y, 6.9, 1.4, s["lede"], size=12, color=PPT_MUTED)
        y += 1.5
    if s.get("bullets"):
        ppt_card(slide, 0.62, y, 6.9, 1.45, "Starting point", [ppt_short(x, 100) for x in s["bullets"]], accent=PPT_CYAN)
    return slide


def ppt_equation_slide(prs, s, images):
    slide = ppt_slide(prs, "", s["kicker"], s["notes"], s["foot"])
    slide.shapes.add_picture(str(images["album"]), Inches(7.7), Inches(1.35), Inches(4.8), Inches(4.8))
    ppt_text(slide, 0.62, 1.65, 6.7, 0.8, s["headline"], size=32, color=PPT_TEXT, bold=True, font="Arial")
    ppt_text(slide, 0.62, 2.55, 2.5, 1.4, s["subhead"], size=86, color=PPT_GOLD, bold=True, font="Arial")
    ppt_text(slide, 0.62, 4.15, 6.6, 1.0, s["lede"], size=18, color=PPT_CYAN, bold=True, font="Arial")
    return slide


def ppt_standard_slide(prs, s, images):
    if s["layout"] in ("cover", "transition", "artist"):
        key = {"cover": "transition", "transition": "transition", "artist": "artist_square"}[s["layout"]]
        return ppt_photo_slide(prs, s, images, key)
    if s["layout"] == "equation":
        return ppt_equation_slide(prs, s, images)

    slide = ppt_slide(prs, s["headline"] if s["layout"] != "thanks" else "", s["kicker"], s["notes"], s["foot"])
    if s.get("lede"):
        ppt_text(slide, 0.62, 1.35, 12.1, 0.5, s["lede"], size=10.5, color=PPT_MUTED)

    if s["layout"] == "bullets":
        ppt_card(slide, 0.62, 1.95, 12.1, 4.35, "THE PLAN", [ppt_short(x, 150) for x in s["bullets"]], accent=PPT_GOLD)
    elif s["layout"] == "cards":
        accents = [PPT_GOLD, PPT_CYAN, PPT_RED, PPT_GREEN]
        n = len(s["cards"])
        for i, card in enumerate(s["cards"]):
            if n == 3:
                x, w = 0.62 + i * 4.18, 3.95
            else:
                x, w = 0.62 + i * 6.3, 6.0
            ppt_card(slide, x, 1.95, w, 4.35, card["title"], card["body"], accent=accents[i % len(accents)])
    elif s["layout"] == "quote":
        ppt_card(slide, 0.62, 1.95, 6.0, 4.35, "THE PROMISE", "“" + s["quote"] + "”", accent=PPT_GOLD)
        ppt_card(slide, 6.82, 1.95, 5.9, 4.35, "HOW I’LL MAKE IT REAL", s["lede"], accent=PPT_CYAN)
    elif s["layout"] == "collage":
        image_map = {"album_cover": "album", "vote_poster": "poster", "artist_photo": "artist_square", "party_cover": "party"}
        accents = [PPT_GOLD, PPT_RED, PPT_CYAN, PPT_GREEN]
        for i, x in enumerate(s["images"]):
            ppt_card(slide, 0.62 + i * 3.12, 1.95, 2.9, 4.35, x["title"], x["body"], accent=accents[i], image=images[image_map[x["asset"]]], image_h=1.65)
    elif s["layout"] == "timeline":
        accents = [PPT_GOLD, PPT_CYAN, PPT_RED, PPT_GREEN]
        for i, card in enumerate(s["cards"]):
            col, row = i % 3, i // 3
            x, y = 0.62 + col * 4.18, 1.95 + row * 2.25
            ppt_card(slide, x, y, 3.95, 2.05, card["title"], ppt_short(card["body"], 140), accent=accents[i % len(accents)])
    elif s["layout"] == "thanks":
        ppt_text(slide, 0.62, 1.25, 12.1, 1.0, s["headline"], size=54, color=PPT_GOLD, bold=True, font="Arial")
        ppt_card(slide, 0.62, 2.4, 6.0, 3.25, "References", [source_by_id(i)["label"] if source_by_id(i) else i for i in s["sources"]], accent=PPT_CYAN)
        ppt_card(slide, 6.82, 2.4, 5.9, 3.25, "Keep the files", ["18-page strategy PDF", "18-slide editable PowerPoint", "Browser deck and download page"], accent=PPT_GOLD, image=images["party"], image_h=1.2)
        refs = [(i, (source_by_id(i) or {}).get("url", "")) for i in s["sources"]]
        for i, (label, url) in enumerate(refs[:8]):
            col, row = i % 4, i // 4
            ppt_hyperlink(slide, 0.85 + col * 3.0, 5.78 + row * 0.32, 2.8, 0.24, url, label, size=8)
        files = [("Strategy PDF", ASSETS["pdf"]), ("Editable PPTX", ASSETS["pptx"]), ("Browser deck", ASSETS["online_deck"]), ("Download page", "download.html")]
        for i, (label, url) in enumerate(files):
            ppt_hyperlink(slide, 0.85 + i * 3.0, 6.48, 2.8, 0.24, url, label, size=8)
    return slide


def build_pptx(images) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    prs.core_properties.title = "BARANGA — My 2027 12-Week Campaign"
    prs.core_properties.author = "7H Music Group · Campaign Engineer"
    prs.core_properties.subject = "A 12-week campaign plan for Baranga"
    prs.core_properties.keywords = "BARANGA, 7H Music Group, campaign, 2027"

    for s in SLIDES:
        if s["layout"] == "cover":
            slide = ppt_slide(prs, "", "", s["notes"], s["foot"], hero=True, images=images)
            ppt_text(slide, 6.45, 1.05, 6.2, 0.3, "7H MUSIC GROUP · CAMPAIGN ASSIGNMENT · 24 NOV 2026", size=9.5, color=PPT_CYAN, bold=True)
            ppt_text(slide, 6.4, 1.5, 6.3, 1.0, s["headline"], size=46, color=PPT_TEXT, bold=True, font="Arial")
            ppt_text(slide, 6.45, 2.55, 6.2, 0.6, s["subhead"], size=24, color=PPT_GOLD, bold=True, font="Arial")
            ppt_text(slide, 6.45, 3.4, 5.9, 1.5, s["lede"], size=12.5, color=PPT_MUTED)
            ppt_text(slide, 6.45, 5.15, 5.9, 0.65, "12 WEEKS · ONE CLEAR PLAN.", size=13, color=PPT_CYAN, bold=True)
        elif s["layout"] in ("transition", "artist"):
            ppt_photo_slide(prs, s, images, "transition" if s["layout"] == "transition" else "artist_square")
        elif s["layout"] == "equation":
            ppt_equation_slide(prs, s, images)
        else:
            ppt_standard_slide(prs, s, images)

    prs.save(PPTX_PATH)
    LEGACY_PPTX.write_bytes(PPTX_PATH.read_bytes())


def main() -> None:
    write_js_data()
    images = prepare_images()
    build_pdf(images)
    build_pptx(images)
    print(f"Generated {PDF_PATH.relative_to(ROOT)} ({PDF_PATH.stat().st_size:,} bytes)")
    print(f"Generated {PPTX_PATH.relative_to(ROOT)} ({PPTX_PATH.stat().st_size:,} bytes)")
    print(f"Refreshed {LEGACY_PPTX.name} and {JS_DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
