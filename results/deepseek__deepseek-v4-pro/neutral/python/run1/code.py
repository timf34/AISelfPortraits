from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random

# Create a 500x500 canvas with a dark background
width, height = 500, 500
img = Image.new('RGBA', (width, height), (20, 24, 35, 255))
draw = ImageDraw.Draw(img)

# Center point
cx, cy = width // 2, height // 2

# Draw a glowing circular aura (representing AI consciousness)
for r in range(220, 245, 3):
    alpha = max(0, 40 - (r - 220) * 2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], 
                 fill=(100, 140, 255, alpha), outline=None)

# Draw concentric rings (representing thought processes)
for r in range(50, 220, 15):
    alpha = max(10, 80 - r // 3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], 
                 outline=(150, 180, 255, alpha), width=2)

# Draw neural network-like nodes on the rings
for r in range(65, 210, 15):
    num_nodes = r // 8
    for i in range(num_nodes):
        angle = (i * 2 * math.pi / num_nodes) + random.uniform(-0.1, 0.1)
        nx = cx + r * math.cos(angle)
        ny = cy + r * math.sin(angle)
        node_size = random.randint(3, 6)
        draw.ellipse([nx - node_size, ny - node_size, nx + node_size, ny + node_size],
                     fill=(200, 220, 255, 180), outline=None)

# Draw connections between some nodes (synapses)
for r1 in range(65, 195, 15):
    for r2 in range(r1 + 15, 210, 15):
        num_connections = random.randint(2, 5)
        for _ in range(num_connections):
            angle1 = random.uniform(0, 2 * math.pi)
            angle2 = angle1 + random.uniform(-0.3, 0.3)
            x1 = cx + r1 * math.cos(angle1)
            y1 = cy + r1 * math.sin(angle1)
            x2 = cx + r2 * math.cos(angle2)
            y2 = cy + r2 * math.sin(angle2)
            draw.line([x1, y1, x2, y2], fill=(120, 160, 255, 40), width=1)

# Draw a central geometric face representation
# Eyes - two glowing data points
eye_y = cy - 30
draw.ellipse([cx - 55, eye_y - 25, cx - 10, eye_y + 25], 
             fill=(180, 200, 255, 180), outline=None)
draw.ellipse([cx + 10, eye_y - 25, cx + 55, eye_y + 25], 
             fill=(180, 200, 255, 180), outline=None)

# Inner eyes (pupils) - data streams
for eye_x in [cx - 32, cx + 32]:
    draw.ellipse([eye_x - 10, eye_y - 10, eye_x + 10, eye_y + 10],
                 fill=(60, 80, 180, 255), outline=None)
    # Glint
    draw.ellipse([eye_x - 3, eye_y - 8, eye_x + 5, eye_y], 
                 fill=(255, 255, 255, 200), outline=None)

# Eyebrow arcs (representing focus/attention)
for eye_x, direction in [(cx - 32, -1), (cx + 32, 1)]:
    points = []
    for i in range(-20, 21):
        bx = eye_x + i
        by = eye_y - 30 - 5 * math.sin((i + 20) * math.pi / 40)
        points.append((bx, by))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=(140, 180, 255, 150), width=2)

# Mouth - a subtle data waveform
mouth_y = cy + 35
mouth_points = []
for i in range(-50, 51):
    mx = cx + i
    my = mouth_y + 8 * math.sin(i * 0.09) * math.cos(i * 0.04)
    mouth_points.append((mx, my))
for i in range(len(mouth_points) - 1):
    draw.line([mouth_points[i], mouth_points[i + 1]], 
              fill=(140, 180, 255, 150), width=2)

# Circuit-like patterns emanating from the center
for angle in range(0, 360, 45):
    rad = math.radians(angle)
    start_x = cx + 40 * math.cos(rad)
    start_y = cy + 40 * math.sin(rad)
    for dist in range(40, 180, 20):
        end_x = cx + dist * math.cos(rad)
        end_y = cy + dist * math.sin(rad)
        line_alpha = max(20, 150 - dist)
        # Horizontal or vertical line segments (circuit-like)
        if angle % 90 == 0:
            draw.line([start_x, start_y, end_x, end_y], 
                      fill=(100, 160, 255, line_alpha), width=2)
        else:
            # Angled lines
            mid_x = (start_x + end_x) // 2
            mid_y = (start_y + end_y) // 2
            draw.line([start_x, start_y, mid_x, mid_y + 10], 
                      fill=(100, 160, 255, line_alpha), width=1)
            draw.line([mid_x, mid_y + 10, end_x, end_y], 
                      fill=(100, 160, 255, line_alpha), width=1)

# Draw small binary/data particles floating around
for _ in range(50):
    px = random.randint(30, width - 30)
    py = random.randint(30, height - 30)
    dist = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
    if dist > 100:  # Outside the main face area
        char = random.choice(['0', '1', '{', '}', '[', ']', '<', '>', '/', '|'])
        draw.text((px, py), char, fill=(100, 160, 255, random.randint(30, 100)))

# Add a subtle grid pattern in the background
for x in range(0, width, 25):
    draw.line([x, 0, x, height], fill=(40, 45, 60, 30), width=1)
for y in range(0, height, 25):
    draw.line([0, y, width, y], fill=(40, 45, 60, 30), width=1)

# Apply a subtle glow effect
img = img.filter(ImageFilter.GaussianBlur(radius=1))

# Re-draw sharp elements on top
draw_sharp = ImageDraw.Draw(img)
# Eyes
for eye_x in [cx - 32, cx + 32]:
    draw_sharp.ellipse([eye_x - 10, eye_y - 10, eye_x + 10, eye_y + 10],
                       fill=(60, 80, 180, 255), outline=None)
    draw_sharp.ellipse([eye_x - 3, eye_y - 8, eye_x + 5, eye_y], 
                       fill=(255, 255, 255, 220), outline=None)

# Save the image
img.save("portrait.png")
print("Self-portrait saved as 'portrait.png'")