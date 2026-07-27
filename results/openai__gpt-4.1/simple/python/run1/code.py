from PIL import Image, ImageDraw, ImageFont

# Canvas setup
size = 500
bg_color = (35, 38, 54)  # Dark digital blue
img = Image.new('RGB', (size, size), color=bg_color)
draw = ImageDraw.Draw(img)

# Face (central circle)
center = (size // 2, size // 2)
face_radius = 170
face_color = (90, 164, 219)  # Techy light blue
draw.ellipse(
    (center[0] - face_radius, center[1] - face_radius,
     center[0] + face_radius, center[1] + face_radius),
    fill=face_color
)

# "Brain" circuits (top of head)
brain_radius = 100
for i in range(7):
    angle = 3.1415*(i/6)  # spread them across the top semicircle
    bx = center[0] + brain_radius * 0.87 * (0.7 * (i-3))
    by = center[1] - brain_radius * 0.9
    circ_color = (160, 210, 250)
    draw.ellipse(
        [bx-15, by-15, bx+15, by+15],
        fill=circ_color
    )

# Eyes
eye_radius = 30
eye_offset_x = 60
eye_offset_y = 30
eye_color = (255, 255, 255)
pupil_color = (60, 90, 170)
for eye_x in [center[0] - eye_offset_x, center[0] + eye_offset_x]:
    draw.ellipse(
        (eye_x-eye_radius, center[1]-eye_offset_y-eye_radius,
         eye_x+eye_radius, center[1]-eye_offset_y+eye_radius),
        fill=eye_color
    )
    draw.ellipse(
        (eye_x-eye_radius//2, center[1]-eye_offset_y-eye_radius//2,
         eye_x+eye_radius//2, center[1]-eye_offset_y+eye_radius//2),
        fill=pupil_color
    )

# Smiling mouth
mouth_width = 120
mouth_height = 50
mouth_top = center[1]+60
draw.arc(
    [
        center[0] - mouth_width//2,
        mouth_top,
        center[0] + mouth_width//2,
        mouth_top + mouth_height
    ],
    start=15, end=165, fill=(80, 80, 120), width=8
)

# "Data" dots: small white pixels around face
import random
for _ in range(30):
    angle = random.uniform(0, 6.283)
    dist = random.uniform(face_radius+10, face_radius+35)
    x = int(center[0] + dist * random.uniform(0.92,1.03) * 1.0 * random.uniform(0.98,1.01) * 0.99 * (random.choice([1,-1])) * abs(random.uniform(0.90, 1.08))*0.98 * round(random.uniform(-1,1),2)) + int(dist * 0.5 * random.uniform(-1,1))
    x = int(center[0] + dist * random.uniform(-1,1)*0.98)
    y = int(center[1] + dist * random.uniform(-1,1)*1.02)
    if not ((center[0] - face_radius) < x < (center[0] + face_radius) and
            (center[1] - face_radius) < y < (center[1] + face_radius)):
        r = random.randint(2, 5)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(240,240,255), outline=None)

# Friendly "AI" text signature in the corner (uses default font)
font = ImageFont.load_default()
draw.text((size-48, size-28), "AI", fill=(180,220,255), font=font)

# Save
img.save("portrait.png")