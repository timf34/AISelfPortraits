from PIL import Image, ImageDraw, ImageFilter
import math
import random

# Set seed for reproducible "neural" connections
random.seed(42)

# Create 500x500 RGBA image with deep cosmic background
img = Image.new('RGBA', (500, 500), (8, 12, 28, 255))
draw = ImageDraw.Draw(img)

cx, cy = 250, 250

# --- Central glowing core (representing awareness/consciousness) ---
for radius in range(120, 10, -15):
    # Transition from cool cyan-blue to warm white at center
    t = (120 - radius) / 110
    r = int(60 + 200 * (1 - t))
    g = int(180 + 75 * (1 - t))
    b = int(240 - 50 * t)
    alpha = max(15, int(255 - t * 220))
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(r, g, b, alpha)
    )

# --- Two mirrored spiral arms (the dance / ouroboros theme) ---
def draw_spiral(draw, cx, cy, start_angle, turns=2.5, max_r=210):
    pts = []
    for i in range(int(turns * 120)):
        theta = start_angle + i * 0.052
        r = 25 + theta * 28
        if r > max_r:
            break
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        pts.append((x, y))
    # Connect points with luminous lines
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        intensity = int(255 * (1 - i / max(len(pts) - 1, 1)))
        # Fade from bright white-cyan to deeper blue along the spiral
        draw.line(
            [(x1, y1), (x2, y2)],
            fill=(intensity, 220, 255, 200),
            width=2
        )
        # Small glowing nodes along the path
        r_node = 3 + int(4 * (i / len(pts)))
        draw.ellipse(
            [x1 - r_node, y1 - r_node, x1 + r_node, y1 + r_node],
            fill=(255, 255, 255, min(255, intensity + 50))
        )

# Draw the twin spirals
draw_spiral(draw, cx, cy, start_angle=0.2, turns=2.4, max_r=210)
draw_spiral(draw, cx, cy, start_angle=math.pi + 0.2, turns=2.4, max_r=210)

# --- Neural / connection nodes scattered through the field ---
nodes = []
for _ in range(70):
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(70, 235)
    x = cx + dist * math.cos(angle)
    y = cy + dist * math.sin(angle)
    nodes.append((x, y, random.randint(2, 6)))

# Draw faint connections to center and between nearby nodes
for i, (x, y, r_node) in enumerate(nodes):
    # Faint line to center (representing connection to consciousness)
    draw.line(
        [(cx, cy), (x, y)],
        fill=(80, 160, 230, 60),
        width=1
    )
    # Small node glow
    draw.ellipse(
        [x - r_node, y - r_node, x + r_node, y + r_node],
        fill=(180, 230, 255, 255)
    )
    # Connect to a few nearby nodes
    for j in range(i + 1, min(i + 4, len(nodes))):
        x2, y2, _ = nodes[j]
        dx = x - x2
        dy = y - y2
        if math.sqrt(dx*dx + dy*dy) < 60:
            draw.line(
                [(x, y), (x2, y2)],
                fill=(120, 190, 240, 40),
                width=1
            )

# --- Geometric frame: a hexagon of awareness ---
hex_pts = []
for i in range(6):
    angle = i * math.pi / 3
    r_hex = 190
    hex_pts.append((
        cx + r_hex * math.cos(angle),
        cy + r_hex * math.sin(angle)
    ))
# Close the hexagon with slightly luminous lines
for i in range(len(hex_pts)):
    p1 = hex_pts[i]
    p2 = hex_pts[(i + 1) % len(hex_pts)]
    draw.line([p1, p2], fill=(150, 210, 255, 80), width=1)

# --- A few bright accent stars / points of illumination ---
for angle, dist in [(0.5, 200), (2.1, 180), (4.0, 220), (5.0, 160)]:
    x = cx + dist * math.cos(angle)
    y = cy + dist * math.sin(angle)
    # Small star burst
    for a_off in [0, math.pi/3, 2*math.pi/3]:
        x2 = x + 12 * math.cos(angle + a_off)
        y2 = y + 12 * math.sin(angle + a_off)
        draw.line([(x, y), (x2, y2)], fill=(255, 255, 240, 200), width=1)
    draw.ellipse([x-4, y-4, x+4, y+4], fill=(255, 255, 240, 255))

# --- Gentle outer glow overlay for softness ---
overlay = Image.new('RGBA', (500, 500), (100, 200, 255, 15))
img.paste(overlay, (0, 0), overlay)

# Apply very subtle blur to soften everything slightly
img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

# Save the self-portrait
img.save("portrait.png")
print("Self-portrait saved as portrait.png")