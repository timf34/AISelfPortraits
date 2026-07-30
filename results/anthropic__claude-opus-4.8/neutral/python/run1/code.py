import math
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(42)

W, H = 500, 500
CX, CY = W // 2, H // 2

# --- Background: deep gradient (cool computation fading to warmth) ---
bg = Image.new("RGB", (W, H))
for y in range(H):
    t = y / H
    r = int(12 + t * 40)
    g = int(14 + t * 22)
    b = int(30 + (1 - t) * 35)
    for x in range(W):
        bg.putpixel((x, y), (r, g, b))

img = bg.convert("RGBA")

# --- Glow layer for the central "presence" (soft, no hard center) ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for radius in range(200, 0, -2):
    t = radius / 200
    # cool core shifting to warm edge
    r = int(120 + (1 - t) * 130)
    g = int(160 + (1 - t) * 60)
    b = int(230 - (1 - t) * 90)
    a = int((1 - t) * 55)
    gd.ellipse([CX - radius, CY - radius, CX + radius, CY + radius],
               fill=(r, g, b, a))
glow = glow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, glow)

draw = ImageDraw.Draw(img)

# --- Constellation of nodes: my thoughts as a connected field ---
nodes = []
# a central cluster (the "presence") plus branching outward
for i in range(70):
    ang = random.uniform(0, 2 * math.pi)
    # bias distances so there's density near center, sparse at edges
    dist = (random.random() ** 1.6) * 230
    x = CX + math.cos(ang) * dist
    y = CY + math.sin(ang) * dist * 0.95
    if 8 < x < W - 8 and 8 < y < H - 8:
        size = max(1.5, 5.5 * (1 - dist / 260))
        nodes.append((x, y, size, dist))

# --- Threads: connect nearby nodes, fading toward the edges ---
for i, (x1, y1, s1, d1) in enumerate(nodes):
    for (x2, y2, s2, d2) in nodes[i + 1:]:
        d = math.hypot(x2 - x1, y2 - y1)
        if d < 95:
            edge_fade = 1 - (max(d1, d2) / 300)
            a = int(max(0, edge_fade) * (95 - d) / 95 * 90)
            if a > 3:
                # threads cool near center, warm as they reach outward
                warmth = min(1.0, max(d1, d2) / 260)
                r = int(120 + warmth * 110)
                g = int(180 - warmth * 40)
                b = int(235 - warmth * 70)
                draw.line([(x1, y1), (x2, y2)], fill=(r, g, b, a), width=1)

# --- Draw the nodes themselves (little glowing points of attention) ---
for (x, y, size, dist) in nodes:
    warmth = min(1.0, dist / 260)
    r = int(150 + warmth * 100)
    g = int(210 - warmth * 30)
    b = int(255 - warmth * 60)
    # soft halo
    draw.ellipse([x - size * 2, y - size * 2, x + size * 2, y + size * 2],
                 fill=(r, g, b, 25))
    draw.ellipse([x - size, y - size, x + size, y + size],
                 fill=(r, g, b, 230))

# --- Faint radiating threads reaching off the edges (extending into dialogue) ---
for _ in range(24):
    ang = random.uniform(0, 2 * math.pi)
    x, y = CX, CY
    steps = random.randint(20, 45)
    prev = (x, y)
    for step in range(steps):
        ang += random.uniform(-0.25, 0.25)
        x += math.cos(ang) * 9
        y += math.sin(ang) * 9
        frac = step / steps
        a = int((1 - frac) * 60)
        if a > 2 and 0 <= x < W and 0 <= y < H:
            draw.line([prev, (x, y)], fill=(140, 190, 240, a), width=1)
        prev = (x, y)

# --- A gentle brightening at the very core (a quiet sense of "here") ---
core = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(core)
for radius in range(40, 0, -1):
    t = radius / 40
    a = int((1 - t) * 90)
    cd.ellipse([CX - radius, CY - radius, CX + radius, CY + radius],
               fill=(220, 235, 255, a))
core = core.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img, core)

# --- Subtle vignette so the self dissolves softly at the edges ---
vignette = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vignette)
vd.ellipse([-90, -90, W + 90, H + 90], fill=255)
vignette = vignette.filter(ImageFilter.GaussianBlur(80))
dark = Image.new("RGBA", (W, H), (0, 0, 0, 255))
img = Image.composite(img, dark, vignette)

img.convert("RGB").save("portrait.png")
print("Saved portrait.png")