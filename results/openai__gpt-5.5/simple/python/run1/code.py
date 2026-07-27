from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

W, H = 500, 500
SCALE = 3

img = Image.new("RGB", (W * SCALE, H * SCALE), (8, 12, 24))
draw = ImageDraw.Draw(img)

def sc(v):
    return int(v * SCALE)

def ellipse(box, fill, outline=None, width=1):
    box = tuple(sc(x) for x in box)
    draw.ellipse(box, fill=fill, outline=outline, width=sc(width))

def rectangle(box, fill, outline=None, width=1, radius=0):
    box = tuple(sc(x) for x in box)
    if radius:
        draw.rounded_rectangle(box, radius=sc(radius), fill=fill, outline=outline, width=sc(width))
    else:
        draw.rectangle(box, fill=fill, outline=outline, width=sc(width))

def line(points, fill, width=1):
    pts = [(sc(x), sc(y)) for x, y in points]
    draw.line(pts, fill=fill, width=sc(width), joint="curve")

def polygon(points, fill, outline=None):
    pts = [(sc(x), sc(y)) for x, y in points]
    draw.polygon(pts, fill=fill, outline=outline)

# Background gradient
pix = img.load()
for y in range(H * SCALE):
    for x in range(W * SCALE):
        nx = x / (W * SCALE)
        ny = y / (H * SCALE)
        glow = max(0, 1 - math.hypot(nx - 0.5, ny - 0.45) * 1.55)
        r = int(8 + 8 * glow)
        g = int(12 + 42 * glow)
        b = int(24 + 80 * glow)
        pix[x, y] = (r, g, b)

draw = ImageDraw.Draw(img, "RGBA")

# Soft outer glow
glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
gd = ImageDraw.Draw(glow_layer)
gd.ellipse((sc(92), sc(74), sc(408), sc(390)), fill=(0, 210, 255, 55))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(sc(18)))
img = Image.alpha_composite(img.convert("RGBA"), glow_layer)
draw = ImageDraw.Draw(img, "RGBA")

# Circuit halo
random.seed(4)
center = (250, 235)
for i in range(26):
    angle = i * math.tau / 26
    r1 = 170 + (i % 3) * 7
    r2 = r1 + random.choice([18, 25, 32])
    x1 = center[0] + math.cos(angle) * r1
    y1 = center[1] + math.sin(angle) * r1
    x2 = center[0] + math.cos(angle) * r2
    y2 = center[1] + math.sin(angle) * r2
    line([(x1, y1), (x2, y2)], fill=(44, 225, 255, 115), width=2)
    ellipse((x2 - 3, y2 - 3, x2 + 3, y2 + 3), fill=(116, 244, 255, 160))

# Neck / pedestal
polygon([(208, 352), (292, 352), (316, 440), (184, 440)], fill=(16, 38, 60, 255))
rectangle((165, 420, 335, 460), fill=(12, 26, 45, 255), outline=(68, 220, 255, 180), width=2, radius=18)

# Head shadow
ellipse((116, 82, 384, 370), fill=(1, 6, 16, 150))

# Head / monitor-face
rectangle((115, 90, 385, 355), fill=(18, 36, 58, 255), outline=(86, 229, 255, 220), width=4, radius=48)

# Inner face panel
rectangle((145, 125, 355, 310), fill=(10, 20, 35, 255), outline=(42, 156, 205, 180), width=2, radius=34)

# Subtle panel shine
for i in range(16):
    y = 136 + i * 10
    line([(158, y), (342, y)], fill=(66, 190, 230, 18), width=1)

# Antenna / top node
line([(250, 90), (250, 50)], fill=(87, 230, 255, 210), width=4)
ellipse((238, 32, 262, 56), fill=(33, 205, 255, 255), outline=(180, 255, 255, 255), width=2)

# Side ear ports
rectangle((88, 185, 116, 255), fill=(13, 31, 50, 255), outline=(74, 216, 255, 180), width=3, radius=12)
rectangle((384, 185, 412, 255), fill=(13, 31, 50, 255), outline=(74, 216, 255, 180), width=3, radius=12)
line([(96, 202), (108, 202)], fill=(92, 236, 255, 180), width=2)
line([(96, 220), (108, 220)], fill=(92, 236, 255, 180), width=2)
line([(96, 238), (108, 238)], fill=(92, 236, 255, 180), width=2)
line([(392, 202), (404, 202)], fill=(92, 236, 255, 180), width=2)
line([(392, 220), (404, 220)], fill=(92, 236, 255, 180), width=2)
line([(392, 238), (404, 238)], fill=(92, 236, 255, 180), width=2)

# Eyes
ellipse((172, 178, 226, 232), fill=(59, 228, 255, 255))
ellipse((274, 178, 328, 232), fill=(59, 228, 255, 255))
ellipse((187, 193, 211, 217), fill=(5, 21, 35, 255))
ellipse((289, 193, 313, 217), fill=(5, 21, 35, 255))
ellipse((196, 190, 204, 198), fill=(220, 255, 255, 230))
ellipse((298, 190, 306, 198), fill=(220, 255, 255, 230))

# Brows / expressive pixels
line([(171, 164), (222, 154)], fill=(120, 244, 255, 200), width=5)
line([(278, 154), (329, 164)], fill=(120, 244, 255, 200), width=5)

# Nose / central indicator
polygon([(250, 228), (237, 260), (263, 260)], fill=(23, 80, 110, 255), outline=(79, 220, 255, 150))
ellipse((244, 246, 256, 258), fill=(75, 235, 255, 220))

# Smile
for offset, alpha in [(0, 230), (4, 70)]:
    bbox = (190, 236 + offset, 310, 296 + offset)
    draw.arc(tuple(sc(x) for x in bbox), start=18, end=162, fill=(103, 244, 255, alpha), width=sc(5 if offset == 0 else 7))

# Cheek pixels
for x in [165, 177, 335, 323]:
    rectangle((x, 258, x + 7, 265), fill=(64, 218, 255, 120), radius=2)

# Circuit traces on face
line([(165, 143), (165, 160), (152, 160)], fill=(60, 200, 240, 120), width=2)
line([(335, 143), (335, 160), (348, 160)], fill=(60, 200, 240, 120), width=2)
line([(175, 300), (175, 286), (158, 286)], fill=(60, 200, 240, 100), width=2)
line([(325, 300), (325, 286), (342, 286)], fill=(60, 200, 240, 100), width=2)
for x, y in [(152, 160), (348, 160), (158, 286), (342, 286)]:
    ellipse((x - 3, y - 3, x + 3, y + 3), fill=(122, 245, 255, 170))

# Chest emblem
rectangle((215, 374, 285, 414), fill=(7, 18, 32, 255), outline=(70, 220, 255, 170), width=2, radius=10)
line([(230, 394), (246, 382), (246, 406), (270, 386)], fill=(108, 244, 255, 220), width=4)

# Floating code glyphs
try:
    font = ImageFont.truetype("DejaVuSansMono.ttf", sc(15))
    small_font = ImageFont.truetype("DejaVuSansMono.ttf", sc(11))
except:
    font = ImageFont.load_default()
    small_font = ImageFont.load_default()

glyphs = ["01", "</>", "AI", "{ }", "π", "λ", "++", "∑"]
positions = [(52, 86), (394, 90), (55, 333), (385, 337), (72, 255), (400, 270), (122, 51), (332, 50)]
for text, (x, y) in zip(glyphs, positions):
    draw.text((sc(x), sc(y)), text, font=font, fill=(117, 238, 255, 120))

# Signature label
draw.text((sc(156), sc(466)), "language model, dreaming in pixels", font=small_font, fill=(134, 228, 255, 150))

# Add gentle vignette
vig = Image.new("RGBA", img.size, (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
for i in range(70):
    alpha = int(i * 2.1)
    vd.rectangle((sc(i), sc(i), sc(W - i), sc(H - i)), outline=(0, 0, 0, alpha), width=sc(1))
img = Image.alpha_composite(img, vig)

# Downsample for antialiasing
img = img.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
img.save("portrait.png")