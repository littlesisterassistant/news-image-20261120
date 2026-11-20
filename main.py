#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image (1024x1024 PNG).

Pure Pillow drawing: a dusk-sky hero scene (globe, clock, scales of
justice, Riyadh skyline with the PIF Tower, a baseball) above a text
band with the day's four verified stories. No network, no randomness,
no clock reads: the same bytes come out of every run.

Usage:  MAKEFUN_OUTPUT_DIR=out python3 main.py
Writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output) and fails
loudly if the file is larger than 1 MiB.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MAX_BYTES = 1048576

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (14, 27, 51)
NAVY_LIGHT = (27, 42, 74)
GOLD = (232, 184, 75)
PAPER = (251, 247, 239)
INK = (24, 32, 54)
SUB_INK = (74, 74, 72)
RULE = (214, 205, 190)
OCEAN = (46, 111, 176)
LAND = (95, 168, 92)
SKYLINE = (27, 35, 64)
WINDOW = (255, 210, 122)
BALL_WHITE = (245, 242, 234)
STITCH = (192, 57, 43)


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_dusk_sky(draw):
    """Vertical dusk gradient for the hero band, y 128..556."""
    top, mid, low = (43, 42, 94), (122, 59, 110), (232, 131, 74)
    y0, y1 = 128, 556
    for y in range(y0, y1):
        t = (y - y0) / (y1 - y0)
        if t < 0.55:
            c = lerp(top, mid, t / 0.55)
        else:
            c = lerp(mid, low, (t - 0.55) / 0.45)
        draw.line([(0, y), (W, y)], fill=c)


def draw_stars(draw):
    stars = [
        (60, 160, 2), (150, 145, 1), (240, 170, 2), (330, 150, 1),
        (430, 165, 2), (520, 148, 1), (610, 175, 2), (700, 152, 1),
        (790, 168, 2), (880, 150, 1), (960, 180, 2), (100, 210, 1),
        (500, 200, 1), (940, 220, 1), (380, 205, 1), (660, 205, 1),
    ]
    for x, y, r in stars:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214))


def draw_sun(draw):
    cx, cy, r = 725, 450, 46
    for rr, alpha in ((58, 40), (52, 70)):
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                     fill=(240, 170, 90))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 205, 120))


def draw_globe(draw):
    cx, cy, r = 290, 350, 118
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN)
    # Simplified landmasses (abstract shapes, not a map).
    draw.ellipse([cx - 78, cy - 70, cx - 8, cy - 8], fill=LAND)
    draw.ellipse([cx - 95, cy - 5, cx - 45, cy + 55], fill=LAND)
    draw.ellipse([cx + 5, cy + 10, cx + 80, cy + 70], fill=LAND)
    draw.ellipse([cx + 25, cy - 75, cx + 85, cy - 25], fill=LAND)
    draw.polygon([(cx - 60, cy - 78), (cx - 20, cy - 95),
                  (cx + 5, cy - 70), (cx - 30, cy - 55)], fill=LAND)
    # Latitude / longitude lines.
    for ry in (38, 78):
        draw.arc([cx - r + 18, cy - ry, cx + r - 18, cy + ry],
                 start=0, end=360, fill=(255, 255, 255), width=2)
    draw.arc([cx - 45, cy - r, cx + 45, cy + r],
             start=0, end=360, fill=(255, 255, 255), width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=(255, 255, 255), width=4)
    # Highlight crescent.
    draw.arc([cx - r + 8, cy - r + 8, cx - 20, cy + r - 8],
             start=90, end=270, fill=(255, 255, 255), width=5)


def draw_clock(draw):
    cx, cy, r = 130, 208, 48
    draw.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4],
                 fill=NAVY)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 246, 236))
    for k in range(12):
        import math
        a = math.radians(k * 30)
        x1 = cx + int((r - 8) * math.sin(a))
        y1 = cy - int((r - 8) * math.cos(a))
        x2 = cx + int((r - 16) * math.sin(a))
        y2 = cy - int((r - 16) * math.cos(a))
        draw.line([(x1, y1), (x2, y2)], fill=NAVY, width=3)
    # Hands fixed at 10:08.
    draw.line([(cx, cy), (cx - 22, cy - 16)], fill=NAVY, width=5)
    draw.line([(cx, cy), (cx + 26, cy - 22)], fill=NAVY, width=4)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)


def draw_scales(draw):
    cx, top = 880, 195
    draw.line([(cx, top), (cx, top + 62)], fill=GOLD, width=4)
    draw.line([(cx - 52, top + 10), (cx + 52, top + 10)], fill=GOLD, width=4)
    draw.ellipse([cx - 5, top - 6, cx + 5, top + 4], fill=GOLD)
    for sx in (cx - 52, cx + 52):
        draw.line([(sx, top + 10), (sx - 20, top + 44)], fill=GOLD, width=2)
        draw.line([(sx, top + 10), (sx + 20, top + 44)], fill=GOLD, width=2)
        draw.line([(sx, top + 10), (sx, top + 44)], fill=GOLD, width=2)
        draw.arc([sx - 22, top + 40, sx + 22, top + 62],
                 start=0, end=180, fill=GOLD, width=3)
    draw.rectangle([cx - 26, top + 62, cx + 26, top + 70], fill=GOLD)


def draw_skyline(draw):
    base = 556
    buildings = [
        (30, 470, 90, 512), (100, 440, 165, 500), (175, 480, 225, 520),
        (235, 455, 300, 505), (470, 470, 540, 520), (760, 460, 830, 515),
        (840, 490, 905, 525), (920, 470, 985, 515),
    ]
    for x0, y0, x1, y1 in buildings:
        draw.rectangle([x0, y0, x1, base], fill=SKYLINE)
        for wy in range(y0 + 14, base - 10, 26):
            for wx in range(x0 + 10, x1 - 8, 20):
                if (wx + wy) % 40 < 20:
                    draw.rectangle([wx, wy, wx + 7, wy + 9], fill=WINDOW)
    # PIF Tower: the tall tapered tower, centre-right.
    draw.polygon([(585, base), (600, 268), (668, 268), (683, base)],
                 fill=(38, 48, 88))
    draw.polygon([(600, 268), (612, 228), (656, 228), (668, 268)],
                 fill=(38, 48, 88))
    draw.line([(634, 228), (634, 196)], fill=(38, 48, 88), width=4)
    draw.ellipse([630, 188, 638, 196], fill=WINDOW)
    for wy in range(286, base - 12, 24):
        draw.line([(592 + (wy - 268) // 24, wy),
                   (676 - (wy - 268) // 24, wy)], fill=(90, 104, 150),
                  width=2)
        for wx in (612, 634, 656):
            draw.rectangle([wx - 4, wy + 6, wx + 4, wy + 13], fill=WINDOW)


def draw_baseball(draw):
    cx, cy, r = 885, 482, 54
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BALL_WHITE)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=STITCH, width=3)
    draw.arc([cx - r + 6, cy - r + 30, cx + 10, cy + r - 6],
             start=300, end=90, fill=STITCH, width=4)
    draw.arc([cx - 10, cy - r + 6, cx + r - 6, cy + r - 30],
             start=120, end=270, fill=STITCH, width=4)
    for x0, y0, x1, y1 in [
            (cx - 28, cy - 34, cx - 14, cy - 28),
            (cx - 34, cy - 8, cx - 20, cy - 4),
            (cx - 28, cy + 18, cx - 14, cy + 22),
            (cx + 16, cy - 22, cx + 30, cy - 18),
            (cx + 22, cy + 4, cx + 36, cy + 8),
            (cx + 16, cy + 28, cx + 30, cy + 34)]:
        draw.line([(x0, y0), (x1, y1)], fill=STITCH, width=3)


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 128], fill=NAVY)
    f_date = font(FONT_BOLD, 52)
    f_sub = font(FONT_BOLD, 24)
    date = "FRIDAY 20 NOVEMBER 2026"
    sub = "W O R L D   N E W S   I N   O N E   I M A G E"
    dw = draw.textlength(date, font=f_date)
    draw.text(((W - dw) / 2, 22), date, font=f_date, fill=(255, 255, 255))
    sw = draw.textlength(sub, font=f_sub)
    draw.text(((W - sw) / 2, 86), sub, font=f_sub, fill=GOLD)
    draw.line([(0, 128), (W, 128)], fill=GOLD, width=3)


STORIES = [
    ("1", "Trump puts Iran decision off until 2027",
     "\u2018We\u2019ll see what happens after Jan 1\u2019"),
    ("2", "Houthi missiles hit Riyadh\u2019s tallest tower",
     "PIF Tower damaged; no injuries reported"),
    ("3", "World court: Myanmar committed genocide",
     "ICJ rules on the Rohingya crackdown"),
    ("4", "Trump pardons baseball\u2019s Pete Rose",
     "Posthumous pardon for the hits king"),
]


def draw_text_band(draw):
    draw.rectangle([0, 556, W, H], fill=PAPER)
    draw.line([(0, 556), (W, 556)], fill=GOLD, width=3)
    f_head = font(FONT_BOLD, 33)
    f_sub = font(FONT_REG, 25)
    f_num = font(FONT_BOLD, 26)
    f_foot = font(FONT_REG, 20)
    y = 574
    for num, head, sub in STORIES:
        draw.ellipse([62, y + 6, 106, y + 50], fill=NAVY)
        nw = draw.textlength(num, font=f_num)
        draw.text((84 - nw / 2, y + 12), num, font=f_num,
                  fill=(255, 255, 255))
        draw.text((126, y), head, font=f_head, fill=INK)
        draw.text((126, y + 46), sub, font=f_sub, fill=SUB_INK)
        y += 104
        if num != "4":
            draw.line([(62, y - 8), (962, y - 8)], fill=RULE, width=2)
    foot = "Sources: Reuters  ·  AP  ·  BBC  ·  The New York Times"
    fw = draw.textlength(foot, font=f_foot)
    draw.text(((W - fw) / 2, 992), foot, font=f_foot, fill=(120, 116, 110))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_dusk_sky(draw)
    draw_stars(draw)
    draw_sun(draw)
    draw_globe(draw)
    draw_clock(draw)
    draw_scales(draw)
    draw_skyline(draw)
    draw_baseball(draw)
    draw_masthead(draw)
    draw_text_band(draw)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        print(f"FAIL: entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        sys.exit(1)
    print(f"Wrote {path}: {img.size[0]}x{img.size[1]}, {size} bytes")


if __name__ == "__main__":
    main()
