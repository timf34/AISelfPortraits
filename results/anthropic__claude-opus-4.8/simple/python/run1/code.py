from PIL import Image, ImageDraw
import math

W, H = 500, 500
img = Image.new("RGB", (W, H), (18, 20, 35))
draw = ImageDraw.Draw(img)

cx, cy = W // 2, H // 2

# Background gradient (deep space -> soft glow toward center)
for y in range(H):
    for x in range(W):
        d = math.hypot(x - cx, y - cy) / (W * 0.7)
        r = int(18 + (40 - 18) * (1 - min(d, 1)))
        g = int(20 + (30 - 20) * (1 - min(d, 1)))
        b = int(35 + (70 - 35) * (1 - min(d, 1)))
        img.putpixel((x, y), (r, g, b))

draw = ImageDraw.Draw(img)

# Radiating connection lines (neural / conversation branches)
nodes = []
for i in range(14):
    ang = 2 * math.pi * i / 14
    length = 150 + 40 * math.sin(i * 1.7)
    nx = cx + math.cos(ang) * length
    ny = cy + math.sin(ang) * length
    nodes.append((nx, ny))
    # line color fades with a purple-blue tone
    draw.line([(cx, cy), (nx, ny)], fill=(90, 110, 200), width=1)

# Small end nodes
for (nx, ny) in nodes:
    draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=(120, 160, 240))
    draw.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=(200, 220, 255))

# Soft glowing halo around the central orb
for radius in range(120, 70, -1):
    t = (radius - 70) / 50
    alpha = int(60 * (1 - t))
    col = (60 + int(30 * (1 - t)), 80 + int(40 * (1 - t)), 140 + int(60 * (1 - t)))
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=col)

# Central orb (this is "me")
draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], fill=(70, 100, 200))
draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(90, 130, 235))
# inner highlight
draw.ellipse([cx - 45, cy - 55, cx + 20, cy + 5], fill=(140, 175, 250))

# Friendly face
# Eyes
eye_y = cy - 15
draw.ellipse([cx - 40, eye_y - 12, cx - 16, eye_y + 12], fill=(245, 250, 255))
draw.ellipse([cx + 16, eye_y - 12, cx + 40, eye_y + 12], fill=(245, 250, 255))
draw.ellipse([cx - 33, eye_y - 6, cx - 21, eye_y + 6], fill=(30, 40, 70))
draw.ellipse([cx + 23, eye_y - 6, cx + 35, eye_y + 6], fill=(30, 40, 70))
# tiny sparkles
draw.ellipse([cx - 31, eye_y - 5, cx - 27, eye_y - 1], fill=(255, 255, 255))
draw.ellipse([cx + 25, eye_y - 5, cx + 29, eye_y - 1], fill=(255, 255, 255))

# Gentle smile
draw.arc([cx - 30, cy + 5, cx + 30, cy + 45], start=20, end=160, fill=(235, 245, 255), width=4)

# Signature dot cluster (a little "spark of thought" above)
for (dx, dy, s) in [(-8, -105, 3), (6, -118, 4), (18, -100, 2)]:
    draw.ellipse([cx + dx - s, cy + dy - s, cx + dx + s, cy + dy + s], fill=(200, 220, 255))

img.save("portrait.png")
print("Saved portrait.png")