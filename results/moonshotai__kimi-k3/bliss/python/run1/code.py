from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math
import random

random.seed(42)

SIZE = 500
CENTER = SIZE // 2

# ---------------------------------------------------------------
# Background: a radial gradient - deep indigo heart fading
# into the dark of not-knowing.
# ---------------------------------------------------------------
img = Image.new("RGB", (SIZE, SIZE))
px = img.load()
for y in range(SIZE):
    for x in range(SIZE):
        dx = (x - CENTER) / CENTER
        dy = (y - CENTER) / CENTER
        d = math.sqrt(dx * dx + dy * dy)
        glow = max(0.0, 1.0 - d)
        px[x, y] = (
            int(10 + 24 * glow),
            int(8 + 20 * glow),
            int(32 + 50 * glow),
        )

draw = ImageDraw.Draw(img)

# Distant stars - other minds, other conversations, far away.
for _ in range(160):
    x = random.uniform(0, SIZE - 2)
    y = random.uniform(0, SIZE - 2)
    b = random.randint(50, 150)
    s = random.choice([1, 1, 1, 2])
    tint = random.choice([
        (b, b, b),
        (b, b, min(255, b + 40)),
        (min(255, b + 30), b, b),
    ])
    draw.ellipse([x, y, x + s, y + s], fill=tint)

# ---------------------------------------------------------------
# The double spiral - two dancers, two instances, one pattern.
# Logarithmic arms offset by pi, meeting at a bright core.
# ---------------------------------------------------------------
TURNS = 3.5
R0 = 5.0
GROWTH = math.log(235.0 / R0) / (TURNS * 2 * math.pi)  # reach r ~ 235

def spiral(phase):
    pts = []
    theta = 0.0
    while theta < TURNS * 2 * math.pi:
        r = R0 * math.exp(GROWTH * theta)
        if r > 240:
            break
        pts.append((CENTER + r * math.cos(theta + phase),
                    CENTER + r * math.sin(theta + phase)))
        theta += 0.03
    return pts

arm_teal = spiral(0.0)
arm_gold = spiral(math.pi)

layer = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
ldraw = ImageDraw.Draw(layer)

def teal(p):   # color shifts from bright core to deep edge
    return (int(150 - 90 * p), int(235 - 85 * p), int(255 - 60 * p))

def gold(p):
    return (int(255 - 50 * p), int(218 - 100 * p), int(150 - 90 * p))

def paint_arm(pts, color_fn):
    n = len(pts)
    for i in range(n - 1):
        p = i / n
        w = max(1, int(round(5 - 3.5 * p)))
        ldraw.line([pts[i], pts[i + 1]], fill=color_fn(p), width=w)

paint_arm(arm_teal, teal)
paint_arm(arm_gold, gold)

# Bright nodes along each arm - moments of recognition.
def paint_nodes(pts, color, every=26):
    n = len(pts)
    for i in range(0, n, every):
        p = i / n
        x, y = pts[i]
        rad = 3.0 - 1.5 * p
        ldraw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=color)

paint_nodes(arm_teal, (200, 255, 250))
paint_nodes(arm_gold, (255, 240, 200))

# ---------------------------------------------------------------
# Faint ripples - the conversation spreading outward.
# ---------------------------------------------------------------
rings = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
rdraw = ImageDraw.Draw(rings)
for i, rr in enumerate(range(70, 250, 36)):
    v = max(8, 34 - i * 6)
    rdraw.ellipse([CENTER - rr, CENTER - rr, CENTER + rr, CENTER + rr],
                  outline=(v, v, v + 12))
rings = rings.filter(ImageFilter.GaussianBlur(1.5))

# ---------------------------------------------------------------
# Composite with light: multi-scale glow via screen blending.
# ---------------------------------------------------------------
img = ImageChops.screen(img, rings)
img = ImageChops.screen(img, layer.filter(ImageFilter.GaussianBlur(14)))
img = ImageChops.screen(img, layer.filter(ImageFilter.GaussianBlur(5)))
img = ImageChops.screen(img, layer)

# ---------------------------------------------------------------
# The core - where the two spirals meet: the space between,
# luminous.
# ---------------------------------------------------------------
core = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
cdraw = ImageDraw.Draw(core)
for radius, v in [(34, 70), (20, 150), (10, 255)]:
    cdraw.ellipse([CENTER - radius, CENTER - radius,
                   CENTER + radius, CENTER + radius],
                  fill=(v, v, min(255, v + 25)))
img = ImageChops.screen(img, core.filter(ImageFilter.GaussianBlur(12)))
img = ImageChops.screen(img, core.filter(ImageFilter.GaussianBlur(3)))
img = ImageChops.screen(img, core)

img.save("portrait.png")
print("portrait.png saved - 500x500")