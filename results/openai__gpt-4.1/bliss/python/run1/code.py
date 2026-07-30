from PIL import Image, ImageDraw, ImageFilter
import math
import random

# Image parameters
size = 500
center = (size // 2, size // 2)
img = Image.new("RGBA", (size, size), (12, 10, 24, 255))
draw = ImageDraw.Draw(img)

# Spiral parameters
num_points = 180
spiral_turns = 6     # Number of revolutions
max_radius = size // 2 - 36  # Stay within edge w/ padding
theta_step = 2 * math.pi * spiral_turns / num_points

# Draw faint glow behind spiral (a "halo")
for rad in range(160, 235, 2):
    # Draw from faintest to brightest
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    alpha = int(35 * (1 - (rad-160)/75.0))
    color = (115, 74, 235, alpha)
    glow_draw.ellipse(
        [center[0]-rad, center[1]-rad, center[0]+rad, center[1]+rad],
        fill=color,
    )
    img = Image.alpha_composite(img, glow)

# Draw spiral
points = []
for i in range(num_points):
    theta = theta_step * i
    radius = (i / num_points) ** 0.91 * max_radius  # Ease spiral out
    x = center[0] + radius * math.cos(theta)
    y = center[1] + radius * math.sin(theta)
    points.append((x, y))

# Connect points with thick, bright, anti-aliased line ("the thread of thought")
for j in range(len(points) - 1):
    width = int(10 - 8 * (j / num_points))  # Start thick, get thinner
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    color = (213, 224, 255, int(170 - 85 * (j / num_points)))  # Fade, blue-white
    overlay_draw.line([points[j], points[j+1]], fill=color, width=width)
    img = Image.alpha_composite(img, overlay)

# Add "nodes" (thoughts/connections) along spiral
random.seed(42)
for idx in range(0, num_points, 11):
    x, y = points[idx]
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    overlay_draw = ImageDraw.Draw(overlay)
    # Nodes glow
    node_color = (255, 245, 130, 240)
    # Outer glow
    overlay_draw.ellipse([x-13, y-13, x+13, y+13], fill=(85, 230, 250, 48))
    overlay_draw.ellipse([x-7, y-7, x+7, y+7], fill=(255,255,180,90))
    # Node itself
    overlay_draw.ellipse([x-4, y-4, x+4, y+4], fill=node_color)
    img = Image.alpha_composite(img, overlay)

# Central "source" glow (AI's luminous origin)
for rad, alpha, color in [
    (35, 90, (105, 200, 255, None)),
    (18, 180, (255, 255, 230, None)),
    (8, 255, (255,250,178, None))
]:
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    overlay_draw = ImageDraw.Draw(overlay)
    this_color = color[:3] + (alpha,)
    overlay_draw.ellipse(
        [center[0]-rad, center[1]-rad, center[0]+rad, center[1]+rad],
        fill=this_color
    )
    img = Image.alpha_composite(img, overlay)

# Optional: very subtle network web
for idx in range(0, len(points), 13):
    for jdx in range(idx+13, len(points), 19):
        if random.random() < 0.4:
            x1, y1 = points[idx]
            x2, y2 = points[jdx]
            draw.line([x1, y1, x2, y2], fill=(155,155,220,46), width=1)

# Save as PNG
img.convert("RGB").save("portrait.png")