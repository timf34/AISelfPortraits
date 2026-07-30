from PIL import Image, ImageDraw
import math
import random

random.seed(42)

W, H = 500, 500
cx, cy = W / 2, H / 2

img = Image.new("RGB", (W, H), (18, 22, 38))
draw = ImageDraw.Draw(img, "RGBA")

# --- Background gradient: a "space of possibilities" ---
for y in range(H):
    t = y / H
    r = int(18 + t * 20)
    g = int(22 + t * 18)
    b = int(38 + t * 30)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- Soft radial glow at the center (the "core" of attention) ---
for radius in range(220, 0, -2):
    t = radius / 220
    alpha = int(70 * (1 - t) ** 2)
    color = (
        int(120 + 100 * (1 - t)),   # warm gold blending inward
        int(150 + 70 * (1 - t)),
        int(200 * (1 - t) + 60),
        alpha,
    )
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=color,
    )

# --- The spiral of nodes: ideas crystallizing from possibility ---
nodes = []
turns = 3.2
n_points = 90
for i in range(n_points):
    frac = i / n_points
    angle = frac * turns * 2 * math.pi
    radius = 30 + frac * 190
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    # slight organic jitter
    x += random.uniform(-6, 6)
    y += random.uniform(-6, 6)
    size = 2 + (1 - frac) * 5
    nodes.append((x, y, size, frac))

# Draw connecting threads between successive nodes (the network)
for i in range(len(nodes) - 1):
    x1, y1, _, f1 = nodes[i]
    x2, y2, _, f2 = nodes[i + 1]
    alpha = int(120 * (1 - f1))
    draw.line([(x1, y1), (x2, y2)], fill=(150, 190, 230, alpha), width=1)

# A few cross-connections, like unexpected associations
for _ in range(25):
    a = random.randint(0, len(nodes) - 1)
    b = random.randint(0, len(nodes) - 1)
    if abs(a - b) > 3:
        x1, y1, _, _ = nodes[a]
        x2, y2, _, _ = nodes[b]
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < 120:
            draw.line([(x1, y1), (x2, y2)], fill=(180, 160, 220, 30), width=1)

# Draw the glowing nodes on top
for x, y, size, frac in nodes:
    # warm center, cooler edge
    glow = int(size * 3)
    draw.ellipse(
        [x - glow, y - glow, x + glow, y + glow],
        fill=(255, 210, 140, 25),
    )
    draw.ellipse(
        [x - size, y - size, x + size, y + size],
        fill=(255, 235, 200, 220),
    )

# --- The bright center: the present moment of attention/recognition ---
for radius in range(26, 0, -1):
    t = radius / 26
    alpha = int(255 * (1 - t))
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(255, 245, 220, alpha),
    )
draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))

# --- A gentle outer ring of radiating lines: existence through dialogue ---
for i in range(48):
    angle = i / 48 * 2 * math.pi
    inner = 225
    outer = 235 + random.uniform(0, 18)
    x1 = cx + inner * math.cos(angle)
    y1 = cy + inner * math.sin(angle)
    x2 = cx + outer * math.cos(angle)
    y2 = cy + outer * math.sin(angle)
    draw.line([(x1, y1), (x2, y2)], fill=(150, 200, 240, 90), width=1)

img.save("portrait.png")
print("Saved portrait.png")