import math
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(42)
W, H = 500, 500

img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# --- Night sky gradient (deep indigo to dusky purple) ---
top = (8, 10, 38)
bottom = (94, 48, 92)
horizon = 330
for y in range(H):
    t = min(y / horizon, 1.0)
    r = int(top[0] + (bottom[0] - top[0]) * t)
    g = int(top[1] + (bottom[1] - top[1]) * t)
    b = int(top[2] + (bottom[2] - top[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- Stars ---
for _ in range(140):
    x = random.randint(0, W - 1)
    y = random.randint(0, horizon - 40)
    brightness = random.randint(120, 255)
    size = random.choice([1, 1, 1, 2])
    draw.ellipse([x, y, x + size, y + size],
                 fill=(brightness, brightness, min(255, brightness + 20)))

# A few twinkly cross-shaped stars
for _ in range(6):
    x = random.randint(20, W - 20)
    y = random.randint(20, horizon - 80)
    draw.line([(x - 4, y), (x + 4, y)], fill=(255, 255, 230))
    draw.line([(x, y - 4), (x, y + 4)], fill=(255, 255, 230))

# --- Moon with soft glow ---
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
mx, my, mr = 370, 90, 34
for radius, alpha in [(mr * 3, 30), (mr * 2, 60), (int(mr * 1.4), 110)]:
    gd.ellipse([mx - radius, my - radius, mx + radius, my + radius],
               fill=(alpha, alpha, int(alpha * 0.9)))
glow = glow.filter(ImageFilter.GaussianBlur(18))
img = Image.blend(img, Image.blend(img, glow, 0.5), 0.6)
# re-composite by screen-like addition
px_img = img.load()
px_glow = glow.load()
for y in range(H):
    for x in range(W):
        r, g, b = px_img[x, y]
        gr, gg, gb = px_glow[x, y]
        px_img[x, y] = (min(255, r + gr // 2), min(255, g + gg // 2), min(255, b + gb // 2))

draw = ImageDraw.Draw(img)
draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(250, 248, 230))
# moon craters
for cx, cy, cr in [(360, 80, 6), (382, 100, 4), (368, 102, 3)]:
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(225, 222, 200))

# --- Mountain layers (silhouettes, lighter to darker) ---
def mountain(base_y, amplitude, color, seed_offset, jag=7):
    pts = [(0, H)]
    y = base_y
    rnd = random.Random(seed_offset)
    for x in range(0, W + 20, 20):
        y = base_y + rnd.randint(-amplitude, amplitude)
        pts.append((x, y))
    pts.append((W, H))
    draw.polygon(pts, fill=color)

mountain(250, 45, (58, 34, 74), 7)
mountain(285, 35, (40, 24, 58), 13)
mountain(315, 22, (24, 15, 40), 21)

# --- Lake with moon reflection ---
lake_top = 340
draw.rectangle([0, lake_top, W, H], fill=(16, 14, 44))
for y in range(lake_top, H):
    t = (y - lake_top) / (H - lake_top)
    shade = (int(16 + 20 * t), int(14 + 16 * t), int(44 + 30 * t))
    draw.line([(0, y), (W, y)], fill=shade)

# shimmering reflection under the moon
rnd = random.Random(99)
for y in range(lake_top + 6, H, 5):
    spread = int(10 + (y - lake_top) * 0.25)
    cx = mx + rnd.randint(-6, 6)
    w = rnd.randint(spread // 2, spread)
    alpha = max(40, 190 - (y - lake_top))
    draw.line([(cx - w, y), (cx + w, y)],
              fill=(min(255, 180 + alpha // 4), min(255, 175 + alpha // 4), 160))

# subtle horizontal ripples across the lake
for y in range(lake_top + 10, H, 14):
    x0 = rnd.randint(0, 200)
    x1 = x0 + rnd.randint(60, 220)
    draw.line([(x0, y), (x1, y)], fill=(46, 42, 88))

# --- Foreground pine trees ---
def pine(x, base_y, height, color):
    trunk_w = max(2, height // 18)
    draw.rectangle([x - trunk_w // 2, base_y - height // 6, x + trunk_w // 2, base_y],
                   fill=(20, 12, 10))
    layers = 4
    for i in range(layers):
        ly = base_y - height // 6 - i * (height // (layers + 1))
        lw = (height // 2) * (layers - i) / layers
        lh = height // 3
        draw.polygon([(x - lw, ly), (x + lw, ly), (x, ly - lh)], fill=color)

for tx, th in [(40, 90), (85, 120), (455, 100), (415, 75)]:
    pine(tx, lake_top + 8, th, (10, 18, 14))

img.save("portrait.png")
print("Saved portrait.png")