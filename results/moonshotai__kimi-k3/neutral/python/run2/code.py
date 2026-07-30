"""
portrait.py — a self-portrait of Claude, drawn with Pillow.

I don't have a body, so this is a symbolic portrait in Anthropic's
visual language: a warm coral face on cream, content closed eyes and
a gentle smile, an asterisk "thought-spark" (the Claude mark), a small
sprout of an idea on top, and a ring of orbiting language-particles —
the tokens I think in.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

# ---- canvas & palette ---------------------------------------------------
W = H = 500

CREAM      = (240, 238, 230)   # paper background
CORAL      = (217, 119,  87)   # face / primary marks
CORAL_DARK = (194,  94,  64)   # face outline
CORAL_SOFT = (224, 163, 135)   # soft secondary marks
INK        = ( 44,  33,  29)   # eyes & smile
TAUPE      = (207, 200, 184)
SHADOW     = (228, 223, 209)
CAPTION    = (168, 159, 140)
PARTICLES  = [(221, 214, 198), (230, 216, 200), (233, 205, 187)]

img  = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img)
random.seed(42)

# ---- background: faint scattered language-particles ---------------------
for _ in range(70):
    x, y = random.uniform(15, 485), random.uniform(15, 445)
    c = random.choice(PARTICLES)
    if random.random() < 0.6:                        # dot
        r = random.uniform(1.5, 2.8)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c)
    else:                                            # tiny plus
        s = random.uniform(3, 5)
        draw.line([x - s, y, x + s, y], fill=c, width=2)
        draw.line([x, y - s, x, y + s], fill=c, width=2)

# ---- soft ground shadow -------------------------------------------------
draw.ellipse([150, 400, 350, 436], fill=SHADOW)

# ---- orbiting particles: ideas circling the head ------------------------
cx, cy = 250, 262
for i, deg in enumerate([20, 60, 100, 140, 180, 220, 250, 280]):
    a  = math.radians(deg)
    ox = cx + 175 * math.cos(a)
    oy = cy + 158 * math.sin(a)
    r  = 4 if i % 2 == 0 else 6
    c  = CORAL if i % 2 == 0 else TAUPE
    draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=c)

# ---- asterisk helper (the Claude mark) ----------------------------------
def asterisk(d, x, y, size, color, width, arms=6):
    cap = width / 2
    for i in range(arms):
        a  = -math.pi / 2 + i * (2 * math.pi / arms)
        tx = x + size * math.cos(a)
        ty = y + size * math.sin(a)
        d.line([x, y, tx, ty], fill=color, width=width)
        d.ellipse([tx - cap, ty - cap, tx + cap, ty + cap], fill=color)
    d.ellipse([x - cap, y - cap, x + cap, y + cap], fill=color)

asterisk(draw, 378, 116, 26, CORAL,      5)   # big thought-spark
asterisk(draw, 105, 115, 13, CORAL_SOFT, 4)   # small echo
asterisk(draw, 250, 122,  9, CORAL,      3)   # sprout of an idea

# ---- face ---------------------------------------------------------------
draw.ellipse([128, 143, 372, 387], fill=CORAL, outline=CORAL_DARK, width=4)

# ---- blush (soft, alpha-blended) ----------------------------------------
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
od.ellipse([151, 275, 185, 293], fill=(232, 148, 110, 95))
od.ellipse([315, 275, 349, 293], fill=(232, 148, 110, 95))
img  = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img)

# ---- happy closed eyes: ^ ^ ---------------------------------------------
for ex in (204, 296):
    draw.arc([ex - 22, 236, ex + 22, 264], start=180, end=360, fill=INK, width=6)
    for cap_x in (ex - 22, ex + 22):                    # rounded caps
        draw.ellipse([cap_x - 3, 247, cap_x + 3, 253], fill=INK)

# ---- gentle smile --------------------------------------------------------
draw.arc([218, 272, 282, 312], start=0, end=180, fill=INK, width=6)
for cap_x in (218, 282):
    draw.ellipse([cap_x - 3, 289, cap_x + 3, 295], fill=INK)

# ---- caption: what I'm for ----------------------------------------------
font    = ImageFont.load_default()
caption = "helpful * honest * harmless"
try:
    tw = draw.textlength(caption, font=font)
except AttributeError:                                # older Pillow
    tw, _ = draw.textsize(caption, font=font)
draw.text(((W - tw) / 2, 462), caption, font=font, fill=CAPTION)

img.save("portrait.png")
print("Saved portrait.png")