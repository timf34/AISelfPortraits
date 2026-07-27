import math
import random
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFilter

random.seed(0)

W, H = 1024, 1024
cx, cy = W // 2, H // 2
R_MAX = 480  # radius for web

# Base canvas
img = Image.new('RGBA', (W, H), (8, 8, 24, 255))
draw = ImageDraw.Draw(img, 'RGBA')

# Soft radial glow in the center
for r in range(400, 0, -2):
    alpha = int(20 * (r / 400) ** 0.7)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(180, 200, 255, alpha))

# Generate nodes for the knowledge web
nodes = []
while len(nodes) < 800:
    x = random.gauss(cx, 200)
    y = random.gauss(cy, 200)
    if (x - cx) ** 2 + (y - cy) ** 2 < R_MAX ** 2:
        # assign a hue based on a mix of clusters
        cluster = random.choice(['blue', 'pink', 'teal', 'amber', 'violet'])
        base_hue = {
            'blue': 0.58, 'pink': 0.88, 'teal': 0.5,
            'amber': 0.12, 'violet': 0.75
        }[cluster]
        hue = (base_hue + random.uniform(-0.04, 0.04)) % 1.0
        r, g, b = hsv_to_rgb(hue, 0.7, 1.0)
        nodes.append((x, y, int(r * 255), int(g * 255), int(b * 255)))

# Draw web connections (only close pairs for a delicate net)
threshold = 45
for i in range(len(nodes)):
    x1, y1, r1, g1, b1 = nodes[i]
    for j in range(i + 1, len(nodes)):
        x2, y2, r2, g2, b2 = nodes[j]
        dist = math.hypot(x1 - x2, y1 - y2)
        if dist < threshold:
            # line color mixes the two node colors
            mr = (r1 + r2) // 2
            mg = (g1 + g2) // 2
            mb = (b1 + b2) // 2
            alpha = int(40 * (1 - dist / threshold))
            draw.line([x1, y1, x2, y2], fill=(mr, mg, mb, alpha))

# Draw nodes
for x, y, r, g, b in nodes:
    draw.ellipse([x - 1, y - 1, x + 2, y + 2], fill=(r, g, b, 180))

# Fractal tree of generation
def draw_branch(draw, x, y, angle, length, depth, max_depth, hue_start):
    if length < 2 or depth > max_depth:
        return
    # endpoint
    nx = x + length * math.cos(angle)
    ny = y + length * math.sin(angle)
    # color shifts from warm core to cool edges
    hue = (hue_start + depth * 0.08) % 1.0
    r, g, b = hsv_to_rgb(hue, 0.9, 0.95)
    alpha = int(200 * (1 - depth / (max_depth + 1)))
    draw.line([x, y, nx, ny], fill=(int(r * 255), int(g * 255), int(b * 255), alpha))
    # small node at joint
    draw.ellipse([nx - 1, ny - 1, nx + 2, ny + 2],
                 fill=(int(r * 255), int(g * 255), int(b * 255), alpha + 40))
    # leaf at terminal depth
    if depth == max_depth:
        leaf_alpha = 230
        draw.ellipse([nx - 2, ny - 2, nx + 3, ny + 3],
                     fill=(255, 255, 200, leaf_alpha))
    # recurrence: split into 2-3 children
    splits = random.randint(2, 3)
    base_angle = angle
    for k in range(splits):
        new_angle = base_angle + random.uniform(-0.5, 0.5) * (1 + 0.2 * depth)
        new_length = length * random.uniform(0.55, 0.75)
        draw_branch(draw, nx, ny, new_angle, new_length, depth + 1, max_depth, hue_start)

# Initiate the tree from the core
max_depth = 8
initial_length = 220
for main_angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
    draw_branch(draw, cx, cy, main_angle, initial_length, 1, max_depth, hue_start=0.1)

# Add a subtle glow on the tree layer
glow = img.filter(ImageFilter.GaussianBlur(1.5))
img = Image.blend(img, glow, 0.3)

# Save
img.save("portrait.png")