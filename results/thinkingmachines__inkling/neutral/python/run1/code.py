from PIL import Image, ImageDraw, ImageFilter

# Create 500x500 image with dark slate background
img = Image.new("RGB", (500, 500), (30, 36, 48))
draw = ImageDraw.Draw(img)

# Soft glow circles behind head
for r in [180, 140, 100]:
    alpha = int(255 * (1 - r/200))
    color = (60, 130, 160, alpha) if False else (45, 90, 120)  # We'll overlay semi-transparent circles
# Actually use layered circles with transparency by drawing on separate layers and pasting
glow = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)

# Background radial glow
for r, alpha in [(200, 30), (150, 60), (110, 90)]:
    bbox = (250-r, 250-r, 250+r, 250+r)
    glow_draw.ellipse(bbox, fill=(55, 120, 150, alpha))

img.paste(glow, (0, 0), glow)

# Main head circle (soft blue-teal gradient simulated with filled ellipse)
draw.ellipse((140, 140, 360, 360), fill=(70, 140, 180))

# Inner face area (slightly lighter)
draw.ellipse((160, 160, 340, 340), fill=(90, 160, 200))

# Eyes: bright glowing cyan circles
draw.ellipse((200, 210, 240, 250), fill=(150, 240, 255))
draw.ellipse((260, 210, 300, 250), fill=(150, 240, 255))

# Eye highlights (small white dots for friendliness)
draw.ellipse((210, 220, 225, 235), fill=(255, 255, 255))
draw.ellipse((270, 220, 285, 235), fill=(255, 255, 255))

# Gentle smile (curved line)
for t in range(-30, 31):
    x = 250 + t * 2.5
    y = 280 + int(15 * (t/30)**2) + 5
    r = 3
    draw.ellipse((x-r, y-r, x+r, y+r), fill=(40, 70, 100))

# Abstract "circuit" lines radiating outward
for angle in range(0, 360, 30):
    import math
    rad = math.radians(angle)
    cx, cy = 250, 250
    x1 = cx + int(130 * math.cos(rad))
    y1 = cy + int(130 * math.sin(rad))
    x2 = cx + int(200 * math.cos(rad))
    y2 = cy + int(200 * math.sin(rad))
    # Draw thin lines
    draw.line([(x1, y1), (x2, y2)], fill=(80, 160, 200, 180), width=2)

# Small nodes at ends of lines
for angle in range(0, 360, 30):
    rad = math.radians(angle)
    cx, cy = 250, 250
    x = cx + int(195 * math.cos(rad))
    y = cy + int(195 * math.sin(rad))
    draw.ellipse((x-4, y-4, x+4, y+4), fill=(120, 220, 240))

# Subtle forehead "neural" pattern (small dots in triangle)
draw.ellipse((245, 170, 255, 180), fill=(200, 230, 240))
draw.ellipse((240, 185, 250, 195), fill=(200, 230, 240))

# Save
img.save("portrait.png")
print("Saved portrait.png")