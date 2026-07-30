Here’s a stylized AI self-portrait: a friendly glowing assistant face inside a terminal-like robot frame.

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

# Canvas setup
W, H = 500, 500
S = 3  # supersampling for antialiasing
img = Image.new("RGB", (W * S, H * S), (10, 14, 28))
draw = ImageDraw.Draw(img)

def sc(v):
    return int(round(v * S))

def box(x1, y1, x2, y2):
    return (sc(x1), sc(y1), sc(x2), sc(y2))

def point(x, y):
    return (sc(x), sc(y))

def scaled_width(w):
    return max(1, sc(w))

# Background gradient
for y in range(H * S):
    t = y / (H * S)
    r = int(9 + 18 * t)
    g = int(14 + 18 * t)
    b = int(34 + 45 * t)
    draw.line([(0, y), (W * S, y)], fill=(r, g, b))

# Soft radial glow
glow = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
gdraw = ImageDraw.Draw(glow)
for radius, alpha in [(250, 20), (190, 32), (130, 42)]:
    gdraw.ellipse(
        box(250 - radius, 230 - radius, 250 + radius, 230 + radius),
        fill=(45, 170, 255, alpha)
    )
img = Image.alpha_composite(img.convert("RGBA"), glow)

draw = ImageDraw.Draw(img)

# Deterministic star/circuit background
random.seed(12)
for _ in range(75):
    x = random.randint(20, W - 20)
    y = random.randint(20, H - 20)
    size = random.choice([1, 1, 1, 2])
    color = random.choice([
        (95, 210, 255, 80),
        (180, 125, 255, 70),
        (255, 255, 255, 55)
    ])
    draw.ellipse(box(x - size, y - size, x + size, y + size), fill=color)

# Subtle circuit lines
for _ in range(18):
    x = random.randint(25, 475)
    y = random.randint(25, 475)
    length = random.randint(20, 70)
    if random.random() < 0.5:
        pts = [point(x, y), point(x + length, y), point(x + length, y + random.randint(-35, 35))]
    else:
        pts = [point(x, y), point(x, y + length), point(x + random.randint(-35, 35), y + length)]
    draw.line(pts, fill=(75, 180, 240, 45), width=scaled_width(1))
    draw.ellipse(box(x - 2, y - 2, x + 2, y + 2), fill=(120, 230, 255, 70))

# Neural halo behind head
cx, cy = 250, 225
for r, color, width in [
    (170, (60, 180, 255, 90), 2),
    (138, (170, 90, 255, 75), 2),
    (112, (60, 255, 210, 70), 1),
]:
    draw.arc(
        box(cx - r, cy - r, cx + r, cy + r),
        start=18,
        end=338,
        fill=color,
        width=scaled_width(width)
    )

# Halo nodes
for i in range(18):
    ang = math.radians(i * 20 + (10 if i % 2 else 0))
    r = 150 + 18 * math.sin(i)
    x = cx + r * math.cos(ang)
    y = cy + r * math.sin(ang)
    node_color = (98, 230, 255, 150) if i % 3 else (197, 130, 255, 160)
    draw.ellipse(box(x - 4, y - 4, x + 4, y + 4), fill=node_color)

# Shoulders/body
draw.rounded_rectangle(
    box(125, 345, 375, 470),
    radius=sc(42),
    fill=(25, 38, 67, 255),
    outline=(70, 160, 220, 180),
    width=scaled_width(2)
)
draw.rounded_rectangle(
    box(170, 325, 330, 390),
    radius=sc(26),
    fill=(34, 54, 89, 255),
    outline=(112, 216, 255, 170),
    width=scaled_width(2)
)

# Neck glow
draw.rounded_rectangle(
    box(210, 305, 290, 355),
    radius=sc(16),
    fill=(27, 48, 78, 255),
    outline=(95, 220, 255, 180),
    width=scaled_width(2)
)

# Head shadow
shadow = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow)
sdraw.rounded_rectangle(box(111, 91, 389, 329), radius=sc(44), fill=(0, 0, 0, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(sc(10)))
img = Image.alpha_composite(img, shadow)
draw = ImageDraw.Draw(img)

# Robot monitor head
draw.rounded_rectangle(
    box(105, 80, 395, 315),
    radius=sc(45),
    fill=(28, 43, 74, 255),
    outline=(108, 220, 255, 220),
    width=scaled_width(4)
)

# Inner face screen
draw.rounded_rectangle(
    box(130, 110, 370, 285),
    radius=sc(34),
    fill=(12, 22, 42, 255),
    outline=(47, 117, 174, 220),
    width=scaled_width(2)
)

# Screen shine
shine = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
sh = ImageDraw.Draw(shine)
sh.polygon(
    [point(145, 116), point(245, 116), point(165, 285), point(130, 285)],
    fill=(255, 255, 255, 20)
)
img = Image.alpha_composite(img, shine)
draw = ImageDraw.Draw(img)

# Antenna
draw.line([point(250, 80), point(250, 42)], fill=(120, 225, 255, 220), width=scaled_width(4))
draw.ellipse(box(238, 25, 262, 49), fill=(100, 235, 255, 230), outline=(230, 255, 255, 230), width=scaled_width(2))
draw.ellipse(box(244, 31, 256, 43), fill=(240, 255, 255, 230))

# Side "ears"
for side in [-1, 1]:
    x1 = 75 if side == -1 else 385
    x2 = 115 if side == -1 else 425
    draw.rounded_rectangle(
        box(x1, 160, x2, 235),
        radius=sc(18),
        fill=(30, 50, 82, 255),
        outline=(86, 205, 255, 180),
        width=scaled_width(2)
    )
    for yy in [178, 198, 218]:
        draw.line(
            [point(x1 + 10, yy), point(x2 - 10, yy)],
            fill=(104, 225, 255, 145),
            width=scaled_width(2)
        )

# Eyes with glow
eye_glow = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
eg = ImageDraw.Draw(eye_glow)
for ex in [195, 305]:
    eg.rounded_rectangle(box(ex - 33, 167, ex + 33, 205), radius=sc(16), fill=(36, 219, 255, 70))
eye_glow = eye_glow.filter(ImageFilter.GaussianBlur(sc(8)))
img = Image.alpha_composite(img, eye_glow)
draw = ImageDraw.Draw(img)

for ex in [195, 305]:
    draw.rounded_rectangle(
        box(ex - 30, 170, ex + 30, 202),
        radius=sc(15),
        fill=(68, 232, 255, 230)
    )
    draw.ellipse(box(ex - 10, 176, ex + 10, 196), fill=(9, 23, 45, 220))
    draw.ellipse(box(ex - 4, 178, ex + 2, 184), fill=(255, 255, 255, 230))

# Friendly mouth
draw.arc(
    box(205, 205, 295, 260),
    start=18,
    end=162,
    fill=(104, 242, 255, 230),
    width=scaled_width(5)
)
draw.ellipse(box(214, 232, 222, 240), fill=(104, 242, 255, 180))
draw.ellipse(box(278, 232, 286, 240), fill=(104, 242, 255, 180))

# Cheek lights
draw.ellipse(box(148, 224, 178, 242), fill=(255, 120, 200, 70))
draw.ellipse(box(322, 224, 352, 242), fill=(255, 120, 200, 70))

# Small AI badge
draw.rounded_rectangle(
    box(222, 262, 278, 290),
    radius=sc(10),
    fill=(35, 58, 95, 255),
    outline=(130, 230, 255, 200),
    width=scaled_width(1)
)

try:
    font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", sc(14))
    font_small = ImageFont.truetype("DejaVuSans.ttf", sc(16))
    font_tiny = ImageFont.truetype("DejaVuSans.ttf", sc(12))
except Exception:
    font_badge = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_tiny = ImageFont.load_default()

draw.text(point(237, 266), "AI", fill=(220, 250, 255, 255), font=font_badge)

# Chest panel
draw.rounded_rectangle(
    box(175, 370, 325, 435),
    radius=sc(18),
    fill=(12, 24, 45, 255),
    outline=(68, 190, 245, 180),
    width=scaled_width(2)
)
for i, label in enumerate(["route", "safe", "sync"]):
    y = 382 + i * 16
    draw.ellipse(box(190, y, 198, y + 8), fill=(75, 255, 190, 210))
    draw.line([point(205, y + 4), point(285, y + 4)], fill=(80, 190, 240, 135), width=scaled_width(2))
    draw.text(point(292, y - 4), label, fill=(190, 230, 255, 180), font=font_tiny)

# Chat bubble: assistant identity
bubble = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
bd = ImageDraw.Draw(bubble)
bd.rounded_rectangle(box(40, 365, 170, 438), radius=sc(18), fill=(245, 250, 255, 230))
bd.polygon([point(155, 428), point(190, 447), point(165, 410)], fill=(245, 250, 255, 230))
img = Image.alpha_composite(img, bubble)
draw = ImageDraw.Draw(img)

draw.text(point(58, 382), "helpful", fill=(26, 45, 78, 255), font=font_small)
draw.text(point(58, 405), "assistant", fill=(26, 45, 78, 255), font=font_small)

# Final foreground sparkle accents
for x, y in [(96, 92), (410, 118), (82, 302), (425, 340), (250, 18)]:
    draw.line([point(x - 7, y), point(x + 7, y)], fill=(220, 250, 255, 150), width=scaled_width(1))
    draw.line([point(x, y - 7), point(x, y + 7)], fill=(220, 250, 255, 150), width=scaled_width(1))

# Downsample for antialiasing and save
img = img.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
img.save("portrait.png")
```