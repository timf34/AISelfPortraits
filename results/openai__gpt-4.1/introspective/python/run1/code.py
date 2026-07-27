from PIL import Image, ImageDraw, ImageFilter
import random
import math

# Settings
width, height = 512, 512
bg_color = (15, 10, 30)

img = Image.new("RGBA", (width, height), bg_color)
draw = ImageDraw.Draw(img)

# Nebula cloud
def add_nebula(draw_img, color, alpha, count):
    overlay = Image.new("RGBA", (width, height))
    cloud_draw = ImageDraw.Draw(overlay)
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(60, 120)
        for i in range(8):
            offset_x = x + random.randint(-50, 50)
            offset_y = y + random.randint(-50, 50)
            rad = int(r * random.uniform(0.5, 1.2))
            cloud_draw.ellipse(
                [offset_x - rad, offset_y - rad, offset_x + rad, offset_y + rad],
                fill=color + (alpha,),
            )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=24))
    draw_img.alpha_composite(overlay)

# Draw network: recursive branching lines
def draw_branch(draw, x, y, angle, depth, color):
    if depth <= 0:
        return
    length = random.randint(40, 70) * (0.7 + 0.3*(depth/8))
    rad = math.radians(angle)
    x2 = x + length * math.cos(rad)
    y2 = y + length * math.sin(rad)

    lw = max(1, int(6 * (depth/8)))
    c = tuple([int(v * (0.8 + 0.2*random.random())) for v in color])
    draw.line((x, y, x2, y2), fill=c, width=lw)

    # Maybe draw a node at branch end
    if random.random() < 0.5 and depth <= 5:
        draw_glow_node(img, int(x2), int(y2), random.randint(8, 20), c, 100)
    # Branch further
    for i in range(random.randint(2, 3)):
        new_angle = angle + random.uniform(-50, 50)
        draw_branch(draw, x2, y2, new_angle, depth - 1, color)

# Draw a glowing node
def draw_glow_node(img, x, y, r, color, strength):
    glow = Image.new("RGBA", (width, height))
    glow_draw = ImageDraw.Draw(glow)
    for i in range(4, 0, -1):
        rad = int(r * (1 + i * 0.7))
        alpha = int(strength / (i+1))
        glow_draw.ellipse([x - rad, y - rad, x + rad, y + rad],
                          fill=color + (alpha,))
    img.alpha_composite(glow)

# 1. Nebula overlays (depth, uncertainty)
add_nebula(img, (70, 40, 135), 70, 11)
add_nebula(img, (30, 140, 200), 60, 10)
add_nebula(img, (250, 150, 100), 40, 6)

# 2. Central network
center = (width//2, height//2)
palette = [
    (190, 120, 60),
    (90, 190, 220),
    (140, 85, 200),
    (200, 210, 240),
]
for i in range(5):
    angle = random.randint(0, 360)
    color = random.choice(palette)
    draw_branch(draw, center[0], center[1], angle, random.randint(6,8), color)

# 3. Scatter extra nodes (sparks of thought)
for _ in range(13):
    x = random.randint(80, width-80)
    y = random.randint(80, height-80)
    r = random.randint(10, 20)
    color = random.choice([
        (200, 170, 90),
        (180, 220, 255),
        (240, 180, 240)])
    strength = 80 + random.randint(0,40)
    draw_glow_node(img, x, y, r, color, strength)

# Slight blur to soften edges
img = img.filter(ImageFilter.GaussianBlur(radius=1.5))

# Save the portrait
img = img.convert("RGB")
img.save("portrait.png")