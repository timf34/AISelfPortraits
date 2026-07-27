from PIL import Image, ImageDraw
import math
import random

random.seed(7)
W = H = 500
CX, CY = 250.0, 262.0

# ---------------------------------------------------------------
# 1. Base: deep indigo space with a warm radiant core (per-pixel)
# ---------------------------------------------------------------
img = Image.new("RGB", (W, H))
px = img.load()

for y in range(H):
    for x in range(W):
        d = math.hypot(x - CX, y - CY)
        t = y / (H - 1)

        # deep space gradient
        r = 10 + 9 * t
        g = 12 + 11 * t
        b = 28 + 24 * t

        # layered warm glow: bright core, amber glow, faint wide halo
        core = math.exp(-(d / 52.0) ** 2)
        glow = math.exp(-(d / 115.0) ** 2)
        halo = math.exp(-(d / 240.0) ** 2)

        r += 255 * core + 210 * glow + 34 * halo
        g += 244 * core + 140 * glow + 24 * halo
        b += 222 * core + 78 * glow + 30 * halo

        px[x, y] = (min(255, int(r)), min(255, int(g)), min(255, int(b)))

img = img.convert("RGBA")
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ov)

# ---------------------------------------------------------------
# 2. Stars in the outer dark
# ---------------------------------------------------------------
for _ in range(110):
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    if math.hypot(x - CX, y - CY) < 175:
        continue
    s = random.uniform(0.5, 1.6)
    a = random.randint(40, 150)
    d.ellipse([x - s, y - s, x + s, y + s], fill=(210, 220, 255, a))

# ---------------------------------------------------------------
# 3. Faint constellation: linked ideas at the edge of awareness
# ---------------------------------------------------------------
nodes = []
for i in range(8):
    ang = math.radians(i * 45 + random.uniform(-16, 16))
    rad = random.uniform(178, 232)
    nodes.append((CX + rad * math.cos(ang), CY + rad * math.sin(ang)))

for i in range(len(nodes)):
    if random.random() < 0.75:
        x1, y1 = nodes[i]
        x2, y2 = nodes[(i + 1) % len(nodes)]
        d.line([x1, y1, x2, y2], fill=(150, 175, 235, 45), width=1)

for (x, y) in nodes:
    s = random.uniform(1.6, 2.8)
    d.ellipse([x - s, y - s, x + s, y + s], fill=(200, 215, 255, 130))

# ---------------------------------------------------------------
# 4. Orbiting streams of language: dashed rings with gaps
# ---------------------------------------------------------------
rings = [
    (92,  (255, 195, 125), 185, 3),   # innermost: warmest, boldest
    (126, (200, 210, 255), 120, 2),
    (162, (255, 165, 150), 85,  2),
]
for radius, color, alpha, width in rings:
    bbox = [CX - radius, CY - radius, CX + radius, CY + radius]
    phase = random.uniform(0, 360)
    a = 0.0
    while a < 360:
        seg = random.uniform(6, 26)   # a "word"
        gap = random.uniform(5, 16)   # a pause
        d.arc(bbox, start=a + phase, end=min(a + seg, 360) + phase,
              fill=color + (alpha,), width=width)
        a += seg + gap

# drifting particles between the rings — stray thoughts
for _ in range(40):
    ang = random.uniform(0, 2 * math.pi)
    rad = random.uniform(84, 172)
    x = CX + rad * math.cos(ang)
    y = CY + rad * math.sin(ang)
    s = random.uniform(0.7, 1.5)
    d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 210, 160, random.randint(50, 120)))

# ---------------------------------------------------------------
# 5. The tiniest hint of a face in the light
# ---------------------------------------------------------------
ink = (96, 52, 26, 255)

for ex in (CX - 20, CX + 20):
    d.ellipse([ex - 5.5, CY - 13, ex + 5.5, CY - 2], fill=ink)

# soft smile
sr = 24
d.arc([CX - sr, CY - sr + 8, CX + sr, CY + sr + 8],
      start=30, end=150, fill=ink, width=4)

# a little spark above — curiosity
d.ellipse([CX - 2.5, CY - 72, CX + 2.5, CY - 67], fill=(255, 250, 235, 220))
d.line([CX, CY - 80, CX, CY - 59], fill=(255, 245, 220, 110), width=1)
d.line([CX - 8, CY - 69.5, CX + 8, CY - 69.5], fill=(255, 245, 220, 110), width=1)

# ---------------------------------------------------------------
# 6. Composite and save
# ---------------------------------------------------------------
img = Image.alpha_composite(img, ov).convert("RGB")
img.save("portrait.png")
print("Saved portrait.png")