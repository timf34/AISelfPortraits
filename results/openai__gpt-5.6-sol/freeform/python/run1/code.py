from PIL import Image, ImageDraw, ImageFilter
import random
import math

# Render at higher resolution for smoother edges
SCALE = 3
W = H = 500
SIZE = (W * SCALE, H * SCALE)

def sc(value):
    return int(round(value * SCALE))

def box(coords):
    return tuple(sc(v) for v in coords)

def points(coords):
    return [(sc(x), sc(y)) for x, y in coords]

def add_glow(base, center, radius, color, strength=180):
    """Add a soft radial glow."""
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    px = layer.load()
    cx, cy = sc(center[0]), sc(center[1])
    r = sc(radius)

    x0 = max(0, cx - r)
    x1 = min(SIZE[0], cx + r)
    y0 = max(0, cy - r)
    y1 = min(SIZE[1], cy + r)

    for y in range(y0, y1):
        for x in range(x0, x1):
            distance = math.hypot(x - cx, y - cy) / r
            if distance < 1:
                alpha = int(strength * (1 - distance) ** 2)
                px[x, y] = (*color, alpha)

    return Image.alpha_composite(base, layer)

# ---------------------------------------------------------------------
# Background gradient
# ---------------------------------------------------------------------
image = Image.new("RGBA", SIZE, (0, 0, 0, 255))
draw = ImageDraw.Draw(image)

top_color = (10, 15, 42)
bottom_color = (67, 39, 72)

for y in range(SIZE[1]):
    t = y / (SIZE[1] - 1)
    # Slightly nonlinear transition for a deeper upper sky
    t2 = t ** 1.25
    color = tuple(
        int(top_color[i] * (1 - t2) + bottom_color[i] * t2)
        for i in range(3)
    )
    draw.line((0, y, SIZE[0], y), fill=color + (255,))

# Subtle ambient glow behind the portrait
image = add_glow(image, (250, 245), 225, (98, 69, 125), 85)

# ---------------------------------------------------------------------
# Arched observatory window
# ---------------------------------------------------------------------
outer_mask = Image.new("L", SIZE, 0)
om = ImageDraw.Draw(outer_mask)
om.ellipse(box((46, 12, 454, 420)), fill=255)
om.rectangle(box((46, 215, 454, 472)), fill=255)

# Gold frame gradient
frame = Image.new("RGBA", SIZE, (0, 0, 0, 0))
fd = ImageDraw.Draw(frame)
for y in range(sc(12), sc(473)):
    t = (y - sc(12)) / sc(461)
    color = (
        int(210 - 55 * t),
        int(159 - 52 * t),
        int(91 - 35 * t),
        255
    )
    fd.line((0, y, SIZE[0], y), fill=color)

image.paste(frame, (0, 0), outer_mask)

inner_mask = Image.new("L", SIZE, 0)
im = ImageDraw.Draw(inner_mask)
im.ellipse(box((65, 31, 435, 401)), fill=255)
im.rectangle(box((65, 216, 435, 456)), fill=255)

# Interior night sky
window_sky = Image.new("RGBA", SIZE, (0, 0, 0, 0))
ws = ImageDraw.Draw(window_sky)

for y in range(SIZE[1]):
    logical_y = y / SCALE
    t = max(0, min(1, logical_y / 470))
    color = (
        int(5 + 19 * t),
        int(12 + 19 * t),
        int(34 + 39 * t),
        255
    )
    ws.line((0, y, SIZE[0], y), fill=color)

# Stars
random.seed(21)
for _ in range(170):
    x = random.uniform(70, 430)
    y = random.uniform(38, 365)
    r = random.choice([0.35, 0.45, 0.6, 0.8, 1.1])
    brightness = random.randint(145, 245)
    tint = random.choice([
        (brightness, brightness, brightness),
        (brightness, brightness, min(255, brightness + 20)),
        (min(255, brightness + 18), brightness, int(brightness * 0.78))
    ])
    ws.ellipse(box((x-r, y-r, x+r, y+r)), fill=tint + (random.randint(130, 230),))

# A few decorative four-point stars
for x, y, size in [(132, 109, 4), (355, 91, 3), (389, 176, 4), (104, 222, 3)]:
    ws.polygon(points([
        (x, y-size), (x+0.8, y-0.8), (x+size, y),
        (x+0.8, y+0.8), (x, y+size), (x-0.8, y+0.8),
        (x-size, y), (x-0.8, y-0.8)
    ]), fill=(245, 221, 174, 220))

# Crescent moon
ws.ellipse(box((337, 70, 388, 121)), fill=(255, 229, 166, 255))
ws.ellipse(box((350, 61, 397, 108)), fill=(8, 15, 40, 255))

# Distant mountains
ws.polygon(points([
    (65, 346), (111, 288), (143, 319), (190, 260),
    (230, 316), (280, 273), (324, 318), (369, 267),
    (435, 338), (435, 456), (65, 456)
]), fill=(27, 33, 61, 255))

ws.polygon(points([
    (65, 378), (118, 332), (163, 365), (218, 306),
    (268, 363), (319, 327), (370, 370), (435, 325),
    (435, 456), (65, 456)
]), fill=(38, 39, 67, 255))

# Mist bands
mist = Image.new("RGBA", SIZE, (0, 0, 0, 0))
md = ImageDraw.Draw(mist)
md.ellipse(box((42, 333, 345, 405)), fill=(130, 111, 147, 35))
md.ellipse(box((194, 354, 469, 421)), fill=(154, 126, 154, 29))
mist = mist.filter(ImageFilter.GaussianBlur(sc(10)))
window_sky = Image.alpha_composite(window_sky, mist)

image.paste(window_sky, (0, 0), inner_mask)
draw = ImageDraw.Draw(image)

# Inner frame highlight
draw.arc(box((59, 25, 441, 407)), 180, 360,
         fill=(245, 205, 130, 220), width=sc(3))
draw.line(points([(59, 215), (59, 457), (441, 457), (441, 215)]),
          fill=(108, 73, 53, 255), width=sc(5))

# Window mullions
draw.line(points([(250, 33), (250, 456)]),
          fill=(95, 69, 67, 175), width=sc(4))
draw.line(points([(66, 217), (434, 217)]),
          fill=(95, 69, 67, 175), width=sc(4))
draw.line(points([(68, 220), (432, 220)]),
          fill=(230, 177, 104, 90), width=sc(1))

# ---------------------------------------------------------------------
# Portrait silhouette and clothing
# ---------------------------------------------------------------------
# Shoulder shadow
shadow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse(box((113, 356, 387, 530)), fill=(0, 0, 0, 150))
shadow = shadow.filter(ImageFilter.GaussianBlur(sc(10)))
image = Image.alpha_composite(image, shadow)
draw = ImageDraw.Draw(image)

# Coat / shoulders
draw.polygon(points([
    (127, 500), (135, 412), (164, 374), (209, 353),
    (250, 367), (291, 353), (336, 374), (365, 412),
    (373, 500)
]), fill=(24, 50, 73, 255))

# Coat edge lighting
draw.line(points([(164, 375), (140, 416), (133, 500)]),
          fill=(71, 107, 120, 255), width=sc(4))
draw.line(points([(336, 375), (360, 416), (367, 500)]),
          fill=(70, 98, 113, 230), width=sc(4))

# Lapels
draw.polygon(points([
    (165, 375), (210, 352), (250, 404), (203, 389), (188, 430)
]), fill=(35, 69, 92, 255))
draw.polygon(points([
    (335, 375), (290, 352), (250, 404), (297, 389), (312, 430)
]), fill=(31, 63, 86, 255))

draw.line(points([(210, 354), (250, 404), (290, 354)]),
          fill=(100, 129, 132, 190), width=sc(2))

# Neck
draw.rounded_rectangle(box((218, 291, 282, 377)), radius=sc(23),
                       fill=(160, 105, 93, 255))
draw.ellipse(box((219, 327, 281, 378)), fill=(177, 119, 99, 255))

# Hair mass behind head
draw.ellipse(box((174, 126, 326, 310)), fill=(23, 20, 35, 255))
draw.polygon(points([
    (178, 205), (164, 296), (190, 345), (215, 282),
    (285, 282), (310, 345), (336, 296), (322, 198)
]), fill=(22, 19, 33, 255))

# Ears
draw.ellipse(box((179, 213, 205, 260)), fill=(172, 112, 98, 255))
draw.ellipse(box((295, 213, 321, 260)), fill=(172, 112, 98, 255))

# Face
draw.ellipse(box((190, 143, 310, 307)), fill=(185, 125, 106, 255))

# Warm lower-face lighting from the held sun
face_light = Image.new("RGBA", SIZE, (0, 0, 0, 0))
fld = ImageDraw.Draw(face_light)
fld.ellipse(box((196, 224, 304, 326)), fill=(255, 180, 99, 48))
face_light = face_light.filter(ImageFilter.GaussianBlur(sc(14)))
image = Image.alpha_composite(image, face_light)
draw = ImageDraw.Draw(image)

# Hair cap and locks
draw.pieslice(box((176, 121, 324, 249)), 180, 360, fill=(27, 22, 38, 255))
draw.polygon(points([
    (180, 196), (203, 139), (213, 203), (231, 140),
    (245, 197), (265, 137), (278, 200), (302, 151),
    (322, 215), (307, 150), (191, 145)
]), fill=(27, 22, 38, 255))

# Brows
draw.arc(box((208, 206, 239, 224)), 195, 338,
         fill=(65, 42, 49, 255), width=sc(3))
draw.arc(box((261, 206, 292, 224)), 202, 345,
         fill=(65, 42, 49, 255), width=sc(3))

# Closed eyes
draw.arc(box((208, 218, 239, 238)), 5, 175,
         fill=(54, 39, 47, 255), width=sc(2))
draw.arc(box((261, 218, 292, 238)), 5, 175,
         fill=(54, 39, 47, 255), width=sc(2))

# Nose and mouth
draw.line(points([(250, 224), (245, 258), (253, 260)]),
          fill=(133, 82, 78, 210), width=sc(2))
draw.arc(box((232, 265, 268, 286)), 12, 168,
         fill=(104, 57, 67, 255), width=sc(2))

# Freckles
for x, y in [(216, 245), (224, 248), (232, 246),
             (268, 246), (276, 248), (284, 244)]:
    draw.ellipse(box((x-1, y-1, x+1, y+1)),
                 fill=(117, 70, 67, 150))

# ---------------------------------------------------------------------
# Hands and miniature sun
# ---------------------------------------------------------------------
# Sun glow behind hands
image = add_glow(image, (250, 361), 92, (255, 154, 54), 180)
image = add_glow(image, (250, 361), 48, (255, 214, 105), 190)
draw = ImageDraw.Draw(image)

# Forearms
draw.rounded_rectangle(box((172, 375, 222, 458)), radius=sc(21),
                       fill=(32, 65, 87, 255))
draw.rounded_rectangle(box((278, 375, 328, 458)), radius=sc(21),
                       fill=(32, 65, 87, 255))

# Hands, cupped around the light
draw.ellipse(box((184, 345, 241, 393)), fill=(190, 128, 103, 255))
draw.ellipse(box((259, 345, 316, 393)), fill=(190, 128, 103, 255))

# Shape the palms with coat overlays
draw.polygon(points([
    (174, 388), (191, 358), (222, 381), (229, 418), (184, 420)
]), fill=(34, 68, 89, 255))
draw.polygon(points([
    (326, 388), (309, 358), (278, 381), (271, 418), (316, 420)
]), fill=(34, 68, 89, 255))

# Fingers
for offset in [0, 7, 14]:
    draw.arc(box((191 + offset, 349 - offset * 0.12,
                  239 + offset * 0.15, 383 + offset * 0.08)),
             200, 327, fill=(225, 163, 119, 240), width=sc(2))

for offset in [0, 7, 14]:
    draw.arc(box((261 - offset * 0.15, 349 - offset * 0.12,
                  309 - offset, 383 + offset * 0.08)),
             213, 340, fill=(225, 163, 119, 240), width=sc(2))

# Rays around tiny sun
for angle in range(0, 360, 30):
    a = math.radians(angle)
    inner = 27
    outer = 35 if angle % 60 == 0 else 31
    x1 = 250 + math.cos(a) * inner
    y1 = 361 + math.sin(a) * inner
    x2 = 250 + math.cos(a) * outer
    y2 = 361 + math.sin(a) * outer
    draw.line(points([(x1, y1), (x2, y2)]),
              fill=(255, 214, 113, 210), width=sc(2))

# Sun disk
draw.ellipse(box((228, 339, 272, 383)), fill=(255, 184, 54, 255))
draw.ellipse(box((234, 345, 266, 377)), fill=(255, 225, 116, 255))
draw.ellipse(box((241, 350, 259, 368)), fill=(255, 248, 190, 255))

# Tiny orbit line and planet
draw.arc(box((217, 348, 283, 376)), 185, 535,
         fill=(255, 225, 164, 180), width=sc(1))
draw.ellipse(box((278, 355, 283, 360)), fill=(255, 190, 92, 255))

# Coat buttons
for y in [431, 466]:
    draw.ellipse(box((246, y-4, 254, y+4)), fill=(187, 143, 82, 255))
    draw.ellipse(box((248, y-2, 252, y+2)), fill=(240, 196, 115, 180))

# ---------------------------------------------------------------------
# Foreground plants
# ---------------------------------------------------------------------
plant = Image.new("RGBA", SIZE, (0, 0, 0, 0))
pd = ImageDraw.Draw(plant)

# Stems
pd.line(points([(37, 500), (76, 363), (104, 306)]),
        fill=(35, 79, 70, 255), width=sc(4))
pd.line(points([(20, 500), (35, 397), (18, 347)]),
        fill=(35, 79, 70, 255), width=sc(4))
pd.line(points([(463, 500), (428, 365), (401, 306)]),
        fill=(35, 79, 70, 255), width=sc(4))
pd.line(points([(483, 500), (466, 400), (484, 345)]),
        fill=(35, 79, 70, 255), width=sc(4))

def leaf(draw_obj, cx, cy, rx, ry, angle, color):
    temp = Image.new("RGBA", (sc(rx * 3), sc(ry * 3)), (0, 0, 0, 0))
    td = ImageDraw.Draw(temp)
    td.ellipse((sc(rx * 0.5), sc(ry * 0.5),
                sc(rx * 2.5), sc(ry * 2.5)), fill=color)
    temp = temp.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    plant.alpha_composite(
        temp,
        (sc(cx) - temp.width // 2, sc(cy) - temp.height // 2)
    )

for args in [
    (49, 430, 11, 28, -37), (61, 392, 11, 27, 31),
    (79, 353, 10, 26, -43), (93, 326, 9, 23, 38),
    (28, 415, 10, 25, -45), (22, 371, 9, 23, 28),
    (451, 429, 11, 28, 37), (439, 392, 11, 27, -31),
    (421, 353, 10, 26, 43), (407, 326, 9, 23, -38),
    (472, 414, 10, 25, 45), (479, 370, 9, 23, -28)
]:
    leaf(pd, *args, color=(41, 91, 77, 255))

image = Image.alpha_composite(image, plant)

# Fine grain for a soft printed texture
random.seed(9)
grain = Image.new("RGBA", SIZE, (0, 0, 0, 0))
gp = grain.load()
for _ in range(26000):
    x = random.randrange(SIZE[0])
    y = random.randrange(SIZE[1])
    shade = random.choice([255, 230, 30])
    gp[x, y] = (shade, shade, shade, random.randint(2, 8))
image = Image.alpha_composite(image, grain)

# Downsample and save
image = image.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
image.save("portrait.png", quality=95)