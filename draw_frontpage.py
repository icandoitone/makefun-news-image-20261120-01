#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

A newspaper front page, 1024x1024, drawn with PIL only. All facts were
verified against Reuters, BBC, CNN, Le Monde and the India Meteorological
Department on the morning of 20 November 2026 (UTC).

Layout budget (1024 tall): masthead 0-166, lead 180-452, middle 468-736,
lower 752-932, footer rule 944, footer text 952-1012.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
NAVY = (16, 38, 74)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GREY = (90, 88, 82)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 17)
    draw.text((x, y), text, font=f, fill=color)
    return y + 24


def headline(draw, x, y, text, size, max_w, leading=None):
    f = font(SERIF, size)
    leading = leading or int(size * 1.12)
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


# ---------------------------------------------------------------- flags
def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    stripe = h / 13
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=(178, 34, 52))
    canton_w, canton_h = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + canton_w, y + canton_h], fill=NAVY)
    for r in range(5):
        for c in range(6):
            cx = x + 8 + c * (canton_w - 12) / 5
            cy = y + 7 + r * (canton_h - 12) / 4
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)

    def star(cx, cy, r):
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.4
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=(255, 222, 0))

    star(x + w * 0.22, y + h * 0.28, 13)
    for dx, dy in [(0.42, 0.12), (0.52, 0.28), (0.52, 0.48), (0.42, 0.62)]:
        star(x + w * dx, y + h * dy, 5)


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    third = h / 3
    draw.rectangle([x, y, x + w, y + third], fill=(255, 255, 255))
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=(213, 0, 50))


# ---------------------------------------------------------------- build
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- masthead
hline(d, 0, W, 6, width=6)
d.text((W // 2, 16), "THE WORLD TODAY", font=font(SERIF, 66),
       fill=INK, anchor="ma")
d.text((W // 2, 92), "FRIDAY  20  NOVEMBER  2026",
       font=font(SANS_B, 26), fill=NAVY, anchor="ma")
hline(d, 24, W - 24, 132, width=3)
d.text((24, 140), "ONE DAY  •  ONE PAGE  •  THE WORLD",
       font=font(SANS_B, 15), fill=GREY)
d.text((W - 24, 140), "No. 325", font=font(SANS_B, 15), fill=GREY, anchor="ra")
hline(d, 24, W - 24, 166, width=1)

# --- lead story: trilateral summit
y = 180
y = kicker(d, 24, y, "SHENZHEN, CHINA  •  A FIRST IN DIPLOMACY")
y = headline(d, 24, y, "TRUMP, XI AND PUTIN MEET AT LAST",
             40, 620, leading=46)
y = headline(d, 24, y, "First three-way summit ends with a joint peace declaration",
             21, 620, leading=26)
y += 6
y = para(d, 24, y,
         "The leaders of the United States, China and Russia sat down "
         "together for the first time, in Shenzhen, and issued a joint "
         "peace declaration after talks on nuclear risks, energy security "
         "and the world's wars. The APEC summit goes on.",
         font(SANS, 18), 620, 24)
# flags illustration, right of lead
fx, fy, fw, fh = 680, 190, 96, 64
flag_us(d, fx, fy, fw, fh)
d.text((fx + fw // 2, fy + fh + 8), "UNITED STATES", font=font(SANS_B, 13),
       fill=INK, anchor="ma")
flag_cn(d, fx + 110, fy, fw, fh)
d.text((fx + 110 + fw // 2, fy + fh + 8), "CHINA", font=font(SANS_B, 13),
       fill=INK, anchor="ma")
flag_ru(d, fx + 220, fy, fw, fh)
d.text((fx + 220 + fw // 2, fy + fh + 8), "RUSSIA", font=font(SANS_B, 13),
       fill=INK, anchor="ma")
# globe arc under the flags
d.ellipse([700, 300, 980, 440], outline=TEAL, width=4)
d.arc([700, 300, 980, 440], 180, 360, fill=TEAL, width=4)
d.arc([720, 330, 960, 410], 200, 340, fill=TEAL, width=2)
for gx, gy in [(760, 330), (830, 312), (900, 330)]:
    d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=TEAL)
d.text((840, 372), "SHENZHEN", font=font(SANS_B, 16), fill=TEAL, anchor="ma")
d.text((840, 396), "APEC summit", font=font(SANS, 15), fill=GREY, anchor="ma")
hline(d, 24, W - 24, 452, width=2)

# --- middle row: ICJ (left) and cyclone (right)
my = 468
kicker(d, 24, my, "THE HAGUE  •  WORLD COURT")
headline(d, 24, my + 26, "MYANMAR GUILTY OF GENOCIDE",
         27, 460, leading=31)
para(d, 24, my + 92,
     "The International Court of Justice ruled, 9-6, that Myanmar "
     "committed genocide against the Rohingya in 2017 - the first time "
     "the court has found a state guilty of genocide. It ordered "
     "reparations and the safe return of refugees.",
     font(SANS, 17), 460, 23)
# scales of justice
sx, sy = 250, my + 196
d.line([(sx, sy), (sx, sy + 56)], fill=INK, width=4)
d.line([(sx - 52, sy + 6), (sx + 52, sy + 6)], fill=INK, width=4)
for dx in (-52, 52):
    d.line([(sx + dx, sy + 6), (sx + dx, sy + 30)], fill=INK, width=2)
    d.arc([sx + dx - 22, sy + 26, sx + dx + 22, sy + 56], 0, 180, fill=INK, width=2)
    d.line([(sx + dx - 22, sy + 41), (sx + dx + 22, sy + 41)], fill=INK, width=2)
d.line([(sx - 26, sy + 56), (sx + 26, sy + 56)], fill=INK, width=4)
# right column
kicker(d, 524, my, "INDIA  •  LANDFALL TODAY")
headline(d, 524, my + 26, "CYCLONE AKVAN HITS ODISHA",
         27, 452, leading=31)
para(d, 524, my + 92,
     "Severe Cyclone Akvan is due ashore near Gopalpur around noon, "
     "with winds of 100 km/h and heavy rain. More than 100,000 people "
     "have been moved to shelters along the Odisha and Andhra coasts.",
     font(SANS, 17), 452, 23)
# cyclone spiral
cx, cy = 760, my + 212
for r in range(40, 8, -8):
    start = 200 - r * 4
    d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 300,
          fill=TEAL, width=5)
d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
d.line([(524, my), (524, my + 252)], fill=GREY, width=1)
hline(d, 24, W - 24, 736, width=2)

# --- lower row: Kyiv (left) and Anthropic (right)
ly = 752
kicker(d, 24, ly, "KYIV  •  WAR IN UKRAINE")
headline(d, 24, ly + 26, "DRONES DAMAGE TWO EMBASSIES",
         25, 460, leading=29)
para(d, 24, ly + 88,
     "A day-long Russian drone raid on Kyiv killed one person and "
     "damaged the Austrian and Dutch embassies and St Volodymyr's "
     "Cathedral. The EU will summon Russia's ambassador.",
     font(SANS, 17), 460, 23)
kicker(d, 524, ly, "WALL STREET  •  MARKETS")
headline(d, 524, ly + 26, "ANTHROPIC'S RECORD DEBUT",
         25, 452, leading=29)
para(d, 524, ly + 88,
     "Shares in AI firm Anthropic opened at $111.50 on Nasdaq, 34% "
     "above their $83 offer price, and closed at $97.17 - the biggest "
     "stock market debut ever, raising over $100 billion.",
     font(SANS, 17), 452, 23)
d.line([(524, ly), (524, ly + 180)], fill=GREY, width=1)

# --- footer
hline(d, 24, W - 24, 944, width=2)
para(d, 24, 952,
     "SPORT: Henry Nicholls' unbeaten 113 puts New Zealand 243-5 on day "
     "one against India in Wellington.",
     font(SANS_B, 16), 976, 22)
para(d, 24, 976,
     "Also today: World Children's Day  •  APEC talks continue  •  "
     "COP31 in Turkiye.",
     font(SANS, 15), 640, 20)
d.text((W - 24, H - 22), "Sources: Reuters, BBC, CNN, Le Monde, IMD",
       font=font(SANS, 13), fill=GREY, anchor="rb")

img.save("/home/hatch/workspace/makefun-news-image-20261120/entry.png",
         optimize=True)
print("saved")
