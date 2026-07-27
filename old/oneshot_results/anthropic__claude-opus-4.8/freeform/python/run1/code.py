from PIL import Image, ImageDraw
import math

W, H = 500, 500
img = Image.new("RGB", (W, H), (10, 10, 30))
draw = ImageDraw.Draw(img)

# Gradient sky
for y in range(H):
    t = y / H
    r = int(20 + t * 60)
    g = int(20 + t * 40)
    b = int(60 + t * 100)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Moon
draw.ellipse([380, 40, 460, 120], fill=(240, 240, 210))
draw.ellipse([395, 45, 475, 125], fill=(20, 30, 70))

# Stars
import random
random.seed(42)
for _ in range(120):
    x = random.randint(0, W)
    y = random.randint(0, 250)
    s = random.choice([1, 1, 2])
    b = random.randint(180, 255)
    draw.ellipse([x, y, x + s, y + s], fill=(b, b, b))

# Distant hills
def hill(base_y, color, amp, freq, phase):
    pts = [(0, H)]
    for x in range(0, W + 1, 5):
        y = base_y + amp * math.sin(x * freq + phase)
        pts.append((x, y))
    pts.append((W, H))
    draw.polygon(pts, fill=color)

hill(320, (40, 50, 70), 25, 0.012, 0)
hill(360, (30, 40, 55), 30, 0.015, 2)
hill(400, (20, 28, 40), 20, 0.02, 4)

# Reflection water
for y in range(430, H):
    t = (y - 430) / (H - 430)
    r = int(20 + t * 10)
    g = int(28 + t * 12)
    b = int(50 + t * 20)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Moon reflection
for i in range(15):
    yy = 435 + i * 4
    w = 30 - i
    draw.line([(420 - w, yy), (420 + w, yy)], fill=(200, 200, 180))

img.save("portrait.png")