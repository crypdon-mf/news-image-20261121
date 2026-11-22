#!/usr/bin/env python3
"""Generate the 21 Nov 2026 world-news front page (1024x1024 PNG).

Drawn entirely with Pillow shapes + DejaVu text. No network, fully
deterministic. Stories verified against world news wires for 21 Nov 2026:
GTA VI's record $3.79bn first day, the AI stock sell-off, Anthropic's
$2tn debut, the ICJ's Myanmar genocide ruling, the El Chapo Isidro
capture in Mexico, the Kryvyi Rih missile strike, and COP31 overtime.

Layout: a masthead with the date, a lead illustration of a Vice City
sunset skyline for the GTA VI story with its headline and deck, then a
grid of six panels (two rows of three), each with a small drawn
illustration, a kicker, a headline and a one-line deck, and a footer
strip of three further items. The lead is the day's biggest story by
scale and reach, so it gets the full-width art and the largest headline;
the six panels cover one story per field (economy, technology, justice,
crime, conflict, climate) so the page reads as a world summary rather
than a single-topic poster. Each panel illustration is a small drawn
scene for its story (a falling chart, a blue chip, scales, a badge, a
city under fire, a melting globe), so the page carries its meaning
visually and not only in words. Every headline and deck is hand-wrapped
with wrap_text so nothing is clipped or truncated at the image edges.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREY = (90, 90, 90)
MARGIN = 28

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, y, text, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
y = 18
centered(d, y, "THE WORLD IN ONE DAY", font(FSB, 58), INK)
y = 84
d.line([(MARGIN, 96), (W - MARGIN, 96)], fill=INK, width=3)
centered(d, 104, "S A T U R D A Y   2 1   N O V E M B E R   2 0 2 6", font(FB, 24), RED)
d.line([(MARGIN, 140), (W - MARGIN, 140)], fill=INK, width=2)

# ---------------------------------------------------------------- lead: GTA VI
LX, LY, LW, LH = MARGIN, 154, W - 2 * MARGIN, 308
# illustration: Vice City sunset (left ~55%)
ix, iy, iw, ih = LX, LY, 530, LH
bands = [(255, 126, 182), (247, 120, 160), (214, 96, 150), (150, 80, 170),
         (110, 60, 160), (70, 45, 140)]
for i, col in enumerate(bands):
    y0 = iy + i * ih // len(bands)
    y1 = iy + (i + 1) * ih // len(bands)
    d.rectangle([ix, y0, ix + iw, y1], fill=col)
# sun
d.ellipse([ix + 300, iy + 28, ix + 420, iy + 148], fill=(255, 214, 130))
d.ellipse([ix + 312, iy + 40, ix + 408, iy + 136], fill=(255, 232, 170))
# skyline silhouettes
random.seed(21)
bx = ix
while bx < ix + iw - 30:
    bw = random.randint(34, 64)
    bh = random.randint(70, 170)
    by = iy + ih - 58 - bh
    d.rectangle([bx, by, bx + bw, iy + ih - 58], fill=(40, 20, 70))
    for wy in range(by + 10, iy + ih - 66, 16):
        for wx in range(bx + 6, bx + bw - 6, 14):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 220, 120))
    bx += bw + 4
# water + reflection
d.rectangle([ix, iy + ih - 58, ix + iw, iy + ih], fill=(38, 28, 96))
for k in range(6):
    yy = iy + ih - 50 + k * 9
    d.line([(ix + 20 + k * 30, yy), (ix + 180 + k * 40, yy)], fill=(255, 150, 200), width=2)
# palm trees
def palm(px, py, s):
    d.line([(px, py), (px + 4, py - 46 * s)], fill=(30, 20, 50), width=5)
    for ang in (-70, -35, 0, 35, 70):
        a = math.radians(ang - 90)
        ex = px + 4 + math.cos(a) * 34 * s
        ey = py - 46 * s + math.sin(a) * 20 * s
        d.line([(px + 4, py - 46 * s), (ex, ey)], fill=(20, 90, 50), width=4)

palm(ix + 60, iy + ih - 58, 1.0)
palm(ix + 480, iy + ih - 58, 0.8)
# lead text (right)
tx = ix + iw + 22
tw = LX + LW - tx
d.text((tx, LY + 6), "CULTURE  •  GAMING", font=font(FB, 20), fill=RED)
yy = text_block(d, tx, LY + 38, ["GTA VI TAKES", "$3.79BN", "IN A DAY"], font(FB, 58), INK, 62)
deck = wrap(d, "Rockstar's sequel is the biggest entertainment launch in history — 32.5m copies sold before release.", font(FR, 23), tw)
text_block(d, tx, yy + 12, deck, font(FR, 23), INK, 30)
d.line([(LX, LY + LH + 14), (W - MARGIN, LY + LH + 14)], fill=INK, width=2)

# ---------------------------------------------------------------- secondary grid
def panel(x, y, w, h, kicker, kcolor, headline, deck, draw_art):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(200, 195, 180), width=1)
    art_h = 108
    draw_art(x + 1, y + 1, w - 2, art_h)
    d.text((x + 12, y + art_h + 10), kicker, font=font(FB, 16), fill=kcolor)
    hl = wrap(d, headline, font(FB, 24), w - 24)
    yy = text_block(d, x + 12, y + art_h + 32, hl[:2], font(FB, 24), INK, 28)
    dk = wrap(d, deck, font(FR, 17), w - 24)
    text_block(d, x + 12, yy + 4, dk[:1], font(FR, 17), GREY, 20)


def art_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for gy in range(4):
        yy = y + 12 + gy * 24
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(235, 235, 235), width=1)
    # falling line chart
    pts = []
    n = 9
    for i in range(n):
        px = x + 14 + i * (w - 28) // (n - 1)
        py = y + 14 + int(i * (h - 34) / (n - 1) * 0.9) + (6 if i % 3 == 0 else 0)
        pts.append((px, py))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    d.text((x + w - 52, y + h - 26), "-3.7%", font=font(FB, 22), fill=RED)


def art_anthropic(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 248))
    # rising bars
    bars = [22, 34, 30, 46, 58, 74]
    bw = (w - 40) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 18 + i * bw
        d.rectangle([bx, y + h - 12 - bh, bx + bw - 8, y + h - 12], fill=NAVY)
    # rising arrow
    d.line([(x + 16, y + h - 40), (x + w - 20, y + 14)], fill=(0, 140, 70), width=4)
    d.polygon([(x + w - 20, y + 14), (x + w - 40, y + 16), (x + w - 22, y + 32)], fill=(0, 140, 70))
    d.text((x + 14, y + 8), "$2tn", font=font(FB, 26), fill=NAVY)


def art_court(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    cx = x + w // 2
    d.polygon([(cx - 90, y + 22), (cx + 90, y + 22), (cx, y + 2)], fill=(120, 110, 95))
    for i in range(4):
        px = cx - 78 + i * 52
        d.rectangle([px, y + 26, px + 16, y + 82], fill=(250, 248, 240))
    d.rectangle([cx - 96, y + 82, cx + 96, y + 92], fill=(120, 110, 95))
    # scales of justice
    d.line([(cx, y + 96), (cx, y + 104)], fill=INK, width=2)


def art_badge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 84))
    cx, cy = x + w // 2, y + h // 2 + 4
    # five-point star badge
    pts = []
    for i in range(10):
        r = 40 if i % 2 == 0 else 17
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(212, 175, 55), outline=(255, 230, 140))
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(24, 44, 84))
    d.text((cx - 6, cy - 8), "$", font=font(FB, 16), fill=(212, 175, 55))


def art_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 214, 230))
    # skyline
    random.seed(11)
    bx = x + 8
    while bx < x + w - 24:
        bw = random.randint(22, 40)
        bh = random.randint(28, 62)
        d.rectangle([bx, y + h - 18 - bh, bx + bw, y + h - 18], fill=(60, 70, 90))
        bx += bw + 5
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(90, 90, 90))
    # smoke plume
    for sx, sy, r in [(x + w - 70, y + 22, 14), (x + w - 52, y + 12, 18), (x + w - 84, y + 14, 11)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))
    # Ukrainian flag
    fx, fy = x + 16, y + 14
    d.rectangle([fx, fy, fx + 52, fy + 13], fill=(0, 91, 187))
    d.rectangle([fx, fy + 13, fx + 52, fy + 26], fill=(255, 213, 0))
    d.line([(fx, fy), (fx, fy + 62)], fill=INK, width=3)


def art_climate(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 214))
    # globe
    cx, cy, r = x + w // 2, y + h // 2 + 6, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 220))
    d.ellipse([cx - 24, cy - 18, cx - 2, cy + 4], fill=(70, 170, 90))
    d.ellipse([cx + 4, cy + 8, cx + 26, cy + 28], fill=(70, 170, 90))
    d.ellipse([cx - 30, cy - 34, cx + 30, cy + 34], outline=(30, 90, 140), width=3)
    # sun
    d.ellipse([x + w - 46, y + 10, x + w - 16, y + 40], fill=(255, 200, 60))


GX, GY = MARGIN, 478
PW = (W - 2 * MARGIN - 2 * 16) // 3
PH = 222
panels = [
    ("MARKETS", RED, "AI sell-off hits world markets",
     "S&P 500 -3.7%; Nikkei -5.06%.", art_markets),
    ("ANTHROPIC", NAVY, "Anthropic debuts at $2 trillion",
     "Biggest debut in history.", art_anthropic),
    ("THE HAGUE", (90, 70, 20), "Myanmar guilty of Rohingya genocide",
     "First state found guilty.", art_court),
    ("MEXICO", (24, 44, 84), "FBI's most-wanted cartel boss seized",
     "Captured in Sinaloa.", art_badge),
    ("UKRAINE", (0, 91, 187), "Missile hits Zelenskyy's hometown",
     "Two killed, 60 hurt.", art_ukraine),
    ("CLIMATE", (0, 110, 60), "COP31 talks run past deadline",
     "Stalled in Antalya.", art_climate),
]
for i, (kick, kc, hl, dk, art) in enumerate(panels):
    px = GX + (i % 3) * (PW + 16)
    py = GY + (i // 3) * (PH + 16)
    panel(px, py, PW, PH, kick, kc, hl, dk, art)

# ---------------------------------------------------------------- footer
d.line([(MARGIN, 952), (W - MARGIN, 952)], fill=INK, width=1)
foot = ("ALSO IN THE NEWS  —  Brazil: dengue cut 69% by bacteria-carrying mosquitoes  •  "
        "700,000 displaced in southern Ethiopia  •  UN agrees to keep working on AI weapons rules")
fl = wrap(d, foot, font(FR, 17), W - 2 * MARGIN)
text_block(d, MARGIN, 962, fl, font(FR, 17), GREY, 22)

img.save("entry.png", "PNG")
print("saved entry.png")
