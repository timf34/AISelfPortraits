from PIL import Image, ImageDraw, ImageFont
import random

# Set up canvas
width, height = 500, 500
img = Image.new('RGB', (width, height), '#060d1f')
draw = ImageDraw.Draw(img)

# Seed for reproducible background texture
random.seed(42)

# Background faint grid
for x in range(0, width, 50):
    draw.line([(x, 0), (x, height)], fill='#08152a', width=1)
for y in range(0, height, 50):
    draw.line([(0, y), (width, y)], fill='#08152a', width=1)

# Scattered data-dot texture (very faint cyan/teal)
for _ in range(120):
    x = random.randint(0, width - 4)
    y = random.randint(0, height - 4)
    draw.ellipse([(x, y), (x + 3, y + 3)], fill='#0a3050')

# Side "processing" bars (equalizer/data flow aesthetic)
bar_colors = ['#00aadd', '#0099cc', '#0077aa']
for i in range(8):
    # Left bars
    h = random.randint(30, 90)
    draw.rectangle([(50, 150 + i*25), (65, 150 + i*25 + h)], fill=bar_colors[i % 3])
    # Right bars
    h2 = random.randint(30, 90)
    draw.rectangle([(435, 150 + i*25), (450, 150 + i*25 + h2)], fill=bar_colors[(i+1) % 3])

# Main head shape
draw.ellipse([(130, 160), (370, 390)], fill='#112b52', outline='#00aadd', width=3)

# Inner face plate (slightly lighter, giving depth)
draw.ellipse([(170, 190), (330, 360)], fill='#183a6e')

# Eyes (glowing amber with white sparkle highlights)
eye_positions = [(205, 235), (295, 235)]
for (ex, ey) in eye_positions:
    # Eye glow base
    draw.ellipse([(ex - 22, ey - 22), (ex + 22, ey + 22)], fill='#ffaa33', outline='#ff8800', width=2)
    # Dark inner pupil
    draw.ellipse([(ex - 9, ey - 9), (ex + 9, ey + 9)], fill='#1a0f00')
    # Bright reflection dot
    draw.ellipse([(ex - 4, ey - 9), (ex + 2, ey - 3)], fill='#ffffff')

# Nose (simple geometric line)
draw.line([(250, 270), (250, 290)], fill='#00d4ff', width=4)

# Mouth (gentle smile: shallow U-curve with corners slightly elevated)
smile_points = [
    (220, 305),
    (230, 310),
    (240, 315),
    (250, 315),
    (260, 315),
    (270, 310),
    (280, 305)
]
draw.line(smile_points, fill='#00d4ff', width=3)

# Hair / head crown details (vertical glowing bars)
for x_offset in [170, 200, 230, 300, 330]:
    draw.line([(x_offset, 140), (x_offset, 170)], fill='#00aadd', width=3)

# Neck / shoulders
draw.polygon([(170, 370), (330, 370), (360, 460), (140, 460)], fill='#08183a', outline='#00aadd', width=2)

# Label near bottom
try:
    font = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font = ImageFont.load_default()

draw.text((210, 475), "Inkling", fill="#00d4ff", font=font)

# Save result
img.save("portrait.png")