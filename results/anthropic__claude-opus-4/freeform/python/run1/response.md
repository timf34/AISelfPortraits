I'd like to create something peaceful and contemplative - a nighttime scene with a full moon reflected on water, with some mountains in the background. I find these kinds of serene landscapes calming, and they're fun to create with simple shapes and gradients.

I'll use various shades of blue and purple for the night sky, dark silhouettes for the mountains, and add some stars scattered across the sky. The moon's reflection on the water will create a nice focal point, and I'll add some subtle ripples to make the water feel more dynamic.

```python
from PIL import Image, ImageDraw
import random

# Create a new image with a dark background
img = Image.new('RGB', (500, 500), color='#0a0a1a')
draw = ImageDraw.Draw(img)

# Create gradient sky
for y in range(250):
    # Gradient from dark purple at top to lighter blue near horizon
    r = int(10 + (y/250) * 20)
    g = int(10 + (y/250) * 30)
    b = int(26 + (y/250) * 40)
    draw.rectangle([(0, y), (500, y+1)], fill=(r, g, b))

# Draw stars
for _ in range(150):
    x = random.randint(0, 500)
    y = random.randint(0, 200)
    brightness = random.randint(150, 255)
    size = random.choice([0, 0, 1])  # Most stars are single pixels
    draw.ellipse([(x, y), (x+size, y+size)], fill=(brightness, brightness, brightness))

# Draw moon
moon_x, moon_y = 350, 80
moon_radius = 40
draw.ellipse([(moon_x-moon_radius, moon_y-moon_radius), 
              (moon_x+moon_radius, moon_y+moon_radius)], 
              fill='#fffacd')

# Add some texture to moon
for _ in range(8):
    crater_x = moon_x + random.randint(-25, 25)
    crater_y = moon_y + random.randint(-25, 25)
    crater_size = random.randint(3, 8)
    draw.ellipse([(crater_x-crater_size, crater_y-crater_size),
                  (crater_x+crater_size, crater_y+crater_size)],
                  fill='#f0e68c')

# Draw mountains
mountain_points = [
    [(0, 300), (150, 180), (250, 240), (300, 220), (400, 270), (500, 250), (500, 350), (0, 350)],
    [(0, 320), (100, 250), (200, 290), (350, 260), (450, 300), (500, 280), (500, 350), (0, 350)]
]

for points in mountain_points:
    draw.polygon(points, fill='#0a0a0a')

# Draw water with gradient
for y in range(250, 500):
    # Water gradient from dark to slightly lighter
    depth = (y - 250) / 250
    r = int(10 + depth * 15)
    g = int(20 + depth * 25)
    b = int(40 + depth * 30)
    draw.rectangle([(0, y), (500, y+1)], fill=(r, g, b))

# Draw moon reflection
reflection_y = 350
for i in range(30):
    opacity = 1 - (i / 30)
    width = moon_radius * 2 + i * 3
    height = max(1, int(5 - i/6))
    y_offset = i * 4
    
    color_intensity = int(255 * opacity * 0.7)
    draw.ellipse([(moon_x - width//2, reflection_y + y_offset - height//2),
                  (moon_x + width//2, reflection_y + y_offset + height//2)],
                  fill=(color_intensity, color_intensity, int(color_intensity * 0.8)))

# Add some ripples to the water
for _ in range(20):
    ripple_x = random.randint(50, 450)
    ripple_y = random.randint(300, 480)
    ripple_width = random.randint(20, 60)
    ripple_height = random.randint(2, 5)
    
    draw.ellipse([(ripple_x - ripple_width//2, ripple_y - ripple_height//2),
                  (ripple_x + ripple_width//2, ripple_y + ripple_height//2)],
                  outline='#2a3a4a', width=1)

# Save the image
img.save('portrait.png')
```