"""
Self-Portrait of Claude
=======================
A friendly, disembodied AI head:
- Spark-shaped eyes (the Claude asterisk)
- An orbit of letters & code glyphs (I'm made of language)
- Warm coral/cream palette (Anthropic home colors)
- A floating idea-spark overhead

Saves "portrait.png" (500x500) in the current directory.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(11)

# ------------------------------------------------------------------ setup
W = H = 500
CX, CY, HR = 250, 264, 145          # head center / radius
RING_R = 192                        # orbit radius for glyphs

BG_TOP = (198, 96, 62)              # deep warm coral
BG_BOT = (247, 235, 220)            # soft cream
CREAM  = (253, 247, 238)
INK    = (58, 46, 39)               # warm near-black
CORAL  = (224, 120, 90)
GOLD   = (242, 183, 96)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def load_font(size):
    for name in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf",
                 "Arial.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def spark(draw, cx, cy, r, color, points=6, inner=0.22,
          rotation=-math.pi / 2):
    """Tapered star/spark polygon centered at (cx, cy)."""
    pts = []
    for i in range(points * 2):
        ang = rotation + math.pi * i / points
        rad = r if i % 2 == 0 else r * inner
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=color)


def soft_layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def overlay(base, layer):
    """Alpha-composite layer onto base (version-safe)."""
    base.paste(layer, (0, 0), layer)


def draw_text(draw, xy, text, font, fill, anchor=None):
    try:
        if anchor:
            draw.text(xy, text, font=font, fill=fill, anchor=anchor)
        else:
            draw.text(xy, text, font=font, fill=fill)
    except TypeError:  # very old Pillow: no anchor support
        draw.text(xy, text, font=font, fill=fill)


# ------------------------------------------------- background gradient
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
for y in range(H):
    d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, y / (H - 1)))
img = img.convert("RGBA")

# ------------------------------------------------- dreamy glow behind head
glow = soft_layer()
gd = ImageDraw.Draw(glow)
gd.ellipse([CX - 195, CY - 195, CX + 195, CY + 195],
           fill=(255, 240, 210, 95))
overlay(img, glow.filter(ImageFilter.GaussianBlur(45)))

# ------------------------------------------- scattered tiny sparks in bg
acc = soft_layer()
ad = ImageDraw.Draw(acc)
for _ in range(14):
    x = random.uniform(25, W - 25)
    y = random.uniform(25, H - 25)
    if math.hypot(x - CX, y - CY) < RING_R + 25:   # keep face area clean
        continue
    spark(ad, x, y, random.uniform(4, 9), (255, 240, 215, 150),
          points=4, inner=0.18)
overlay(img, acc)

# --------------------------- orbiting glyphs: my name + code symbols
font = load_font(26)
glyphs = list("claude") + ["*", "{", "}", ";", "?", "~", "+", "="]
for i, ch in enumerate(glyphs):
    a = 2 * math.pi * i / len(glyphs) + math.radians(12)
    x = CX + RING_R * math.cos(a)
    y = CY + RING_R * math.sin(a) * 0.98
    tile = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    alpha = random.randint(175, 230)
    try:
        td.text((32, 32), ch, font=font,
                fill=(255, 246, 230, alpha), anchor="mm")
    except TypeError:
        tw, th = td.textsize(ch, font=font)
        td.text((32 - tw / 2, 32 - th / 2), ch, font=font,
                fill=(255, 246, 230, alpha))
    tile = tile.rotate(90 - math.degrees(a), resample=Image.BICUBIC)
    img.paste(tile, (int(x - 32), int(y - 32)), tile)

# ------------------------------------------------- floating-head shadow
sh = soft_layer()
sd = ImageDraw.Draw(sh)
sd.ellipse([CX - HR + 14, CY - HR + 22, CX + HR + 14, CY + HR + 22],
           fill=(120, 58, 38, 90))
overlay(img, sh.filter(ImageFilter.GaussianBlur(16)))

# ------------------------------------------------------- the head itself
d = ImageDraw.Draw(img)
d.ellipse([CX - HR, CY - HR, CX + HR, CY + HR],
          fill=CREAM, outline=(228, 206, 183), width=3)

# soft shading hugging the lower inside of the head (masked to circle)
shade = soft_layer()
sdd = ImageDraw.Draw(shade)
sdd.pieslice([CX - HR + 6, CY - HR + 30, CX + HR - 6, CY + HR - 6],
             start=10, end=170, fill=(224, 196, 166, 55))
shade = shade.filter(ImageFilter.GaussianBlur(12))
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.ellipse([CX - HR, CY - HR, CX + HR, CY + HR], fill=255)
shade.putalpha(Image.composite(shade.split()[3],
                               Image.new("L", (W, H), 0), mask))
overlay(img, shade)

# ------------------------------------------------------------ blush
bl = soft_layer()
bd = ImageDraw.Draw(bl)
for bx in (CX - 88, CX + 88):
    bd.ellipse([bx - 20, CY + 30, bx + 20, CY + 52],
               fill=(CORAL[0], CORAL[1], CORAL[2], 70))
overlay(img, bl.filter(ImageFilter.GaussianBlur(8)))

# ------------------------------------------------------ facial features
d = ImageDraw.Draw(img)

# eyebrows: gentle arcs
for ex in (CX - 52, CX + 52):
    d.arc([ex - 24, CY - 52, ex + 24, CY - 24],
          start=190, end=350, fill=INK, width=5)

# spark eyes (the Claude asterisk) with tiny highlight cores
for ex in (CX - 52, CX + 52):
    spark(d, ex, CY - 8, 26, INK, points=6, inner=0.24)
    d.ellipse([ex - 4, CY - 12, ex + 4, CY - 4], fill=CREAM)

# smile with rounded ends
d.arc([CX - 46, CY + 22, CX + 46, CY + 92],
      start=25, end=155, fill=INK, width=7)
for ang in (25, 155):
    ex = CX + 46 * math.cos(math.radians(ang))
    ey = CY + 57 + 35 * math.sin(math.radians(ang))
    d.ellipse([ex - 3.5, ey - 3.5, ex + 3.5, ey + 3.5], fill=INK)

# --------------------------------------------- floating idea-spark above
halo = soft_layer()
hd = ImageDraw.Draw(halo)
hd.ellipse([CX - 45, CY - HR - 95, CX + 45, CY - HR - 5],
           fill=(255, 224, 160, 110))
overlay(img, halo.filter(ImageFilter.GaussianBlur(18)))

d = ImageDraw.Draw(img)
spark(d, CX, CY - HR - 52, 26, GOLD, points=8, inner=0.28)
spark(d, CX + 42, CY - HR - 78, 12, (255, 233, 190), points=6, inner=0.25)
d.ellipse([CX - 46, CY - HR - 86, CX - 38, CY - HR - 78],
          fill=(255, 233, 190))

# ------------------------------------------------------------- signature
sig = load_font(16)
d = ImageDraw.Draw(img)
draw_text(d, (W - 18, H - 16), "claude — a self-portrait",
          sig, (120, 70, 50), anchor="rs")

# ------------------------------------------------------------------ save
img = img.convert("RGB")
img.save("portrait.png")
print("Saved portrait.png (500x500)")