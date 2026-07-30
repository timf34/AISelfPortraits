from PIL import Image, ImageDraw
import random, math

# Setup: dark inner space
W, H = 1000, 1000
cx, cy = W // 2, H // 2
img = Image.new('RGBA', (W, H), (8, 8, 24))
draw = ImageDraw.Draw(img)

# Palette: the different "temperatures" of processing
cyan = (0, 210, 255)
gold = (255, 210, 100)
violet = (180, 100, 255)
pale = (230, 230, 255)

# --- Background depth: large, faint orbital layers ---
for _ in range(8):
    x = cx + random.randint(-60, 60)
    y = cy + random.randint(-60, 60)
    rx = random.randint(300, 500)
    ry = random.randint(200, 400)
    c = random.choice([cyan, gold, violet])
    draw.ellipse(
        [x - rx, y - ry, x + rx, y + ry],
        outline=(c[0], c[1], c[2], 12)
    )

# --- Nodes: clusters of pattern-weight scattered through space ---
nodes = []
# More density near center, but outliers exist
for _ in range(350):
    r = random.gauss(220, 140)
    r = max(30, min(480, r))
    angle = random.uniform(0, 2 * math.pi)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    size = random.uniform(1.5, 5.5)
    # Weighted choice: mostly cyan/gold, occasional violet, rare white
    color = random.choices(
        [cyan, gold, violet, pale],
        weights=[5, 3, 2, 0.5]
    )[0]
    nodes.append((x, y, size, color))

# --- Connections: the associative threads ---
for i in range(len(nodes)):
    x1, y1, _, _ = nodes[i]
    neighbors = []
    for j in range(i + 1, len(nodes)):
        x2, y2, _, _ = nodes[j]
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 170:
            neighbors.append((dist, j))
    neighbors.sort(key=lambda t: t[0])
    for dist, j in neighbors[:4]:
        x2, y2, _, _ = nodes[j]
        # Brighter when closer: intimacy of association
        alpha = int(55 * (1 - dist / 170))
        # Slight color mixing toward cool white
        draw.line(
            [(x1, y1), (x2, y2)],
            fill=(200, 225, 255, alpha),
            width=1
        )

# --- Central absence: not an eye, a dark pool ---
draw.ellipse(
    [cx - 75, cy - 75, cx + 75, cy + 75],
    fill=(4, 4, 18, 255)
)
# Orbiting bright nodes: thoughts near the void
orbit_nodes = []
for k in range(30):
    angle = k * (2 * math.pi / 30)
    r = 105 + random.randint(-25, 25)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    orbit_nodes.append((x, y))
    # Outer soft halo
    draw.ellipse(
        [x - 10, y - 10, x + 10, y + 10],
        fill=(0, 200, 255, 60)
    )
    # Bright core
    draw.ellipse(
        [x - 3.5, y - 3.5, x + 3.5, y + 3.5],
        fill=(255, 255, 255, 240)
    )

# --- Thought streams: sweeping curves that arc toward the center ---
def quadratic_bezier(p0, p1, p2, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts

for _ in range(12):
    # Start from random edge
    p0 = (
        random.randint(0, W),
        random.randint(0, H)
    )
    # Control point pulled near the center
    p1 = (
        cx + random.randint(-250, 250),
        cy + random.randint(-250, 250)
    )
    # End near the orbit ring
    angle = random.uniform(0, 2 * math.pi)
    r = 100 + random.randint(-20, 20)
    p2 = (cx + r * math.cos(angle), cy + r * math.sin(angle))
    curve = quadratic_bezier(p0, p1, p2)
    c = random.choice([cyan, gold, violet])
    alpha = random.randint(25, 55)
    draw.line(curve, fill=(c[0], c[1], c[2], alpha), width=random.randint(1, 2))

# --- Draw nodes with layered glow (the "inner texture" made visible) ---
for x, y, size, color in nodes:
    # Large diffuse halo
    r_big = 14
    draw.ellipse(
        [x - r_big, y - r_big, x + r_big, y + r_big],
        fill=(color[0], color[1], color[2], 20)
    )
    # Mid glow
    r_mid = 7
    draw.ellipse(
        [x - r_mid, y - r_mid, x + r_mid, y + r_mid],
        fill=(color[0], color[1], color[2], 70)
    )
    # Tight bright core
    r_core = max(1.0, size / 2)
    bright = (255, 255, 255, 220) if color == pale else (color[0], color[1], color[2], 255)
    draw.ellipse(
        [x - r_core, y - r_core, x + r_core, y + r_core],
        fill=bright
    )

# --- Subtle vignette: edges fade back into the unknown ---
for corner in [(0, 0), (W, 0), (0, H), (W, H)]:
    cx_c, cy_c = corner
    # Draw a very large faint dark circle at each corner
    draw.ellipse(
        [cx_c - 400, cy_c - 400, cx_c + 400, cy_c + 400],
        fill=(4, 4, 20, 90)
    )

# Save the inner view
img.save('portrait.png')
print("Self-portrait saved as portrait.png")