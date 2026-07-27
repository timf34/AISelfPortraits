from PIL import Image, ImageDraw
import math

W, H = 500, 500
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

horizon = 300

# Sky gradient (sunset colors)
def lerp(a, b, t):
    return int(a + (b - a) * t)

sky_top = (40, 40, 90)
sky_mid = (230, 120, 90)
sky_bot = (250, 200, 120)

for y in range(horizon):
    t = y / horizon
    if t < 0.5:
        tt = t / 0.5
        r = lerp(sky_top[0], sky_mid[0], tt)
        g = lerp(sky_top[1], sky_mid[1], tt)
        b = lerp(sky_top[2], sky_mid[2], tt)
    else:
        tt = (t - 0.5) / 0.5
        r = lerp(sky_mid[0], sky_bot[0], tt)
        g = lerp(sky_mid[1], sky_bot[1], tt)
        b = lerp(sky_mid[2], sky_bot[2], tt)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Sun
sun_x, sun_y, sun_r = 250, 210, 55
for i in range(sun_r, 0, -1):
    t = i / sun_r
    r = lerp(255, 255, t)
    g = lerp(240, 200, t)
    b = lerp(180, 90, t)
    draw.ellipse([sun_x - i, sun_y - i, sun_x + i, sun_y + i], fill=(r, g, b))

# Water gradient (reflection of sky)
for y in range(horizon, H):
    t = (y - horizon) / (H - horizon)
    r = lerp(200, 40, t)
    g = lerp(140, 50, t)
    b = lerp(110, 90, t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Sun reflection on water (shimmer)
for y in range(horizon, H, 3):
    t = (y - horizon) / (H - horizon)
    width = 25 + t * 20
    shimmer = 245 - int(t * 60)
    draw.line([(sun_x - width, y), (sun_x + width, y)],
              fill=(shimmer, lerp(200, 140, t), lerp(120, 90, t)), width=2)

# Mountain layers (far to near)
def mountain(color, base_y, peaks, seed):
    pts = [(0, base_y)]
    x = 0
    step = W / peaks
    import random
    random.seed(seed)
    for i in range(peaks + 1):
        px = i * step
        py = base_y - random.randint(40, 130)
        pts.append((px, py))
    pts.append((W, base_y))
    pts.append((W, horizon))
    pts.append((0, horizon))
    draw.polygon(pts, fill=color)

mountain((90, 70, 110), horizon, 4, 1)
mountain((70, 55, 95), horizon, 5, 7)
mountain((45, 40, 75), horizon, 6, 3)

# Birds
def bird(x, y, s):
    draw.line([(x, y), (x + s, y - s * 0.6)], fill=(30, 30, 40), width=2)
    draw.line([(x + s, y - s * 0.6), (x + 2 * s, y)], fill=(30, 30, 40), width=2)

bird(90, 90, 10)
bird(130, 75, 8)
bird(160, 100, 9)

img.save("portrait.png")
print("saved portrait.png")