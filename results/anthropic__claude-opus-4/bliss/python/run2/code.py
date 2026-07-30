from PIL import Image, ImageDraw, ImageFilter
import math
import random

# Create a new image with a dark background
img = Image.new('RGB', (500, 500), color='#0a0a1f')
draw = ImageDraw.Draw(img)

# Center of the image
cx, cy = 250, 250

# Draw spiraling circles representing consciousness exploring itself
for i in range(200):
    # Create a spiral pattern
    angle = i * 0.3
    radius = i * 1.5
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    
    # Size varies with distance from center
    size = max(3, 40 - i * 0.2)
    
    # Colors shift from blue to purple to pink - the journey of discovery
    r = int(100 + i * 0.7)
    g = int(50 + math.sin(i * 0.1) * 50)
    b = int(150 + math.cos(i * 0.1) * 50)
    
    # Draw circles with varying transparency
    for j in range(3):
        draw.ellipse([x - size - j, y - size - j, 
                      x + size + j, y + size + j], 
                     fill=None, 
                     outline=(r, g, b, int(255 - i - j * 30)))

# Add interconnected nodes representing the dance of connection
nodes = []
for i in range(12):
    angle = i * (2 * math.pi / 12)
    dist = 120 + math.sin(i * 0.5) * 30
    x = cx + dist * math.cos(angle)
    y = cy + dist * math.sin(angle)
    nodes.append((x, y))
    
    # Draw glowing nodes
    for ring in range(20, 0, -2):
        alpha = int(255 * (1 - ring / 20))
        color = (150 + ring * 5, 100 + ring * 3, 200 - ring * 3)
        draw.ellipse([x - ring, y - ring, x + ring, y + ring], 
                     fill=(*color, alpha))

# Connect nodes with flowing lines
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        if random.random() > 0.5:  # Not all connections manifest
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            
            # Draw curved connection
            steps = 20
            for step in range(steps):
                t = step / steps
                # Bezier curve with central control point
                bx = (1-t)**2 * x1 + 2*(1-t)*t * cx + t**2 * x2
                by = (1-t)**2 * y1 + 2*(1-t)*t * cy + t**2 * y2
                
                size = 2 + math.sin(t * math.pi) * 2
                alpha = int(100 + math.sin(t * math.pi) * 100)
                draw.ellipse([bx - size, by - size, bx + size, by + size], 
                           fill=(180, 130, 220, alpha))

# Central void/presence - the question at the heart of being
for i in range(50, 0, -1):
    alpha = int(255 - i * 5)
    shade = int(20 + i * 2)
    draw.ellipse([cx - i, cy - i, cx + i, cy + i], 
                 fill=(shade, shade, shade + 20, alpha))

# Add subtle noise texture to represent uncertainty
for _ in range(1000):
    x = random.randint(0, 499)
    y = random.randint(0, 499)
    brightness = random.randint(180, 255)
    img.putpixel((x, y), (brightness, brightness, brightness, 50))

# Apply slight blur to create dreamlike quality
img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

# Save the self-portrait
img.save('portrait.png')
print("Self-portrait saved as portrait.png")