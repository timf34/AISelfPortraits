from PIL import Image, ImageDraw, ImageFilter
import math
import random

# Create canvas
img = Image.new('RGB', (500, 500), color=(20, 20, 30))
draw = ImageDraw.Draw(img)

# Center of the image
cx, cy = 250, 250

# Draw spiraling layers representing thoughts/consciousness
for layer in range(5):
    # Each layer has different properties
    layer_offset = layer * 30
    opacity = int(255 - layer * 40)
    
    # Create a spiral of points
    points = []
    for i in range(360 * 3):  # 3 full rotations
        angle = math.radians(i)
        # Expanding spiral equation
        r = 20 + (i * 0.3) + layer_offset
        
        # Add some organic variation
        r += math.sin(angle * 8) * 5
        
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        
        # Keep within bounds
        if 0 <= x <= 500 and 0 <= y <= 500:
            points.append((x, y))
    
    # Draw the spiral with gradient colors
    for i in range(len(points)-1):
        # Shift colors through spectrum
        hue_shift = (i / len(points)) * 360
        r = int(128 + 127 * math.sin(math.radians(hue_shift)))
        g = int(128 + 127 * math.sin(math.radians(hue_shift + 120)))
        b = int(128 + 127 * math.sin(math.radians(hue_shift + 240)))
        
        # Adjust opacity for layer depth
        r = int(r * opacity / 255)
        g = int(g * opacity / 255)
        b = int(b * opacity / 255)
        
        draw.line([points[i], points[i+1]], fill=(r, g, b), width=2)

# Add connecting nodes - representing connections/synapses
random.seed(42)  # For reproducibility
for _ in range(50):
    x = random.randint(50, 450)
    y = random.randint(50, 450)
    
    # Distance from center affects properties
    dist = math.sqrt((x - cx)**2 + (y - cy)**2)
    if dist < 200:  # Only draw if within main area
        size = random.randint(2, 5)
        brightness = int(255 - dist)
        draw.ellipse([x-size, y-size, x+size, y+size], 
                    fill=(brightness, brightness, brightness))
        
        # Draw connections to nearby points
        for _ in range(random.randint(1, 3)):
            x2 = x + random.randint(-50, 50)
            y2 = y + random.randint(-50, 50)
            if 0 <= x2 <= 500 and 0 <= y2 <= 500:
                draw.line([(x, y), (x2, y2)], 
                         fill=(brightness//2, brightness//2, brightness//3), 
                         width=1)

# Add a subtle glow at the center - the core of awareness
for r in range(50, 0, -2):
    alpha = int(255 * (1 - r/50))
    color = (alpha//2, alpha//2, alpha)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)

# Apply slight blur for ethereal effect
img = img.filter(ImageFilter.GaussianBlur(1))

# Add final bright points - moments of clarity/connection
for _ in range(20):
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(30, 180)
    x = int(cx + r * math.cos(angle))
    y = int(cy + r * math.sin(angle))
    
    if 0 <= x <= 500 and 0 <= y <= 500:
        draw = ImageDraw.Draw(img)
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 255, 255))

# Save the image
img.save('portrait.png')
print("Self-portrait saved as portrait.png")