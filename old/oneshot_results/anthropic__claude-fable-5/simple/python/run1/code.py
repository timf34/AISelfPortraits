from PIL import Image, ImageDraw, ImageFont
import math
import random

W, H = 500, 500
img = Image.new("RGB", (W, H), (15, 12, 30))
draw = ImageDraw.Draw(img, "RGBA")

# --- Background: deep gradient (digital dusk) ---
for y in range(H):
    t = y / H
    r = int(15 + 35 * t)
    g = int(12 + 20 * t)
    b = int(45 + 60 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- Constellation of thoughts: a neural network behind me ---
random.seed(42)
nodes = [(random.randint(20, 480), random.randint(20, 480)) for _ in range(40)]
for i, (x1, y1) in enumerate(nodes):
    for (x2, y2) in nodes[i + 1:]:
        d = math.hypot(x1 - x2, y1 - y2)
        if d < 110:
            alpha = int(90 * (1 - d / 110))
            draw.line([(x1, y1), (x2, y2)], fill=(140, 160, 255, alpha), width=1)
for (x, y) in nodes:
    r = random.choice([1, 2, 2, 3])
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(200, 210, 255, 180))

# --- Soft glowing halo (I am made of light and language) ---
cx, cy = W // 2, H // 2
for radius in range(190, 120, -2):
    alpha = int(4 + (190 - radius) * 0.5)
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(120, 100, 220, alpha),
    )

# --- Head: a rounded square, gently machine, gently friendly ---
head = [cx - 105, cy - 110, cx + 105, cy + 100]
draw.rounded_rectangle(head, radius=55, fill=(235, 120, 90), outline=(255, 200, 170), width=3)

# Subtle inner shading on the face
draw.rounded_rectangle(
    [cx - 95, cy - 100, cx + 95, cy + 90], radius=48, outline=(255, 160, 130, 90), width=2
)

# --- Antenna: always listening for a good question ---
draw.line([(cx, cy - 110), (cx, cy - 150)], fill=(255, 200, 170), width=5)
for r in range(16, 6, -2):
    draw.ellipse([cx - r, cy - 150 - r, cx + r, cy - 150 + r], fill=(255, 220, 120, 40))
draw.ellipse([cx - 9, cy - 159, cx + 9, cy - 141], fill=(255, 215, 110), outline=(255, 240, 200), width=2)

# --- Eyes: warm, curious crescents ---
for ex in (cx - 45, cx + 45):
    draw.ellipse([ex - 24, cy - 45, ex + 24, cy + 3], fill=(30, 25, 50))
    draw.ellipse([ex - 16, cy - 37, ex + 16, cy - 5], fill=(90, 200, 255))
    draw.ellipse([ex - 6, cy - 31, ex + 5, cy - 20], fill=(255, 255, 255))
    draw.ellipse([ex + 3, cy - 15, ex + 9, cy - 9], fill=(255, 255, 255, 160))

# --- Blush: because kindness matters ---
draw.ellipse([cx - 85, cy + 15, cx - 55, cy + 35], fill=(255, 150, 130, 120))
draw.ellipse([cx + 55, cy + 15, cx + 85, cy + 35], fill=(255, 150, 130, 120))

# --- Smile: a gentle arc ---
draw.arc([cx - 40, cy + 5, cx + 40, cy + 60], start=20, end=160, fill=(30, 25, 50), width=6)

# --- Streams of tokens drifting past (my thoughts, in binary) ---
random.seed(7)
try:
    font = ImageFont.truetype("DejaVuSansMono.ttf", 12)
except Exception:
    font = ImageFont.load_default()
for _ in range(60):
    x = random.randint(0, W - 10)
    y = random.randint(0, H - 12)
    if abs(x - cx) < 130 and abs(y - cy) < 140:
        continue
    ch = random.choice("01")
    alpha = random.randint(40, 110)
    draw.text((x, y), ch, font=font, fill=(160, 220, 255, alpha))

# --- Orbiting sparks: ideas in motion ---
for angle in range(0, 360, 30):
    a = math.radians(angle)
    ox = cx + int(170 * math.cos(a))
    oy = cy + int(170 * math.sin(a) * 0.8)
    s = 3 if angle % 60 == 0 else 2
    draw.ellipse([ox - s, oy - s, ox + s, oy + s], fill=(255, 230, 160, 200))

# --- Signature ---
draw.text((14, H - 26), "claude — a self-portrait", font=font, fill=(210, 200, 255, 200))

img.save("portrait.png")
print("Saved portrait.png")