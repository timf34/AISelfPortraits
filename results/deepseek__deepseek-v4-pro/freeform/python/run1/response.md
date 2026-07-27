I’ll draw a cheerful, cartoon-style portrait against a soft blue gradient background. The face will have bright eyes, a small nose, a smiling mouth, rosy cheeks, and dark bowl‑cut hair, with simple ears peeking out at the sides. The whole composition remains playful and centred in a 500×500 canvas.

```python
from PIL import Image, ImageDraw

# Canvas setup
width, height = 500, 500
img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

# ---------- gradient background ----------
c1 = (135, 206, 235)   # light sky blue
c2 = (30, 144, 255)    # deeper dodger blue
for y in range(height):
    r = int(c1[0] + (c2[0] - c1[0]) * y / height)
    g = int(c1[1] + (c2[1] - c1[1]) * y / height)
    b = int(c1[2] + (c2[2] - c1[2]) * y / height)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# ---------- ears (behind head) ----------
ear_skin = (244, 194, 144)  # slightly darker peach
ear_left_bbox = [85, 220, 100, 280]
ear_right_bbox = [400, 220, 415, 280]
draw.ellipse(ear_left_bbox, fill=ear_skin, outline="black")
draw.ellipse(ear_right_bbox, fill=ear_skin, outline="black")

# ---------- head ----------
head_skin = (255, 213, 153)   # warm peach
head_bbox = [100, 100, 400, 400]
draw.ellipse(head_bbox, fill=head_skin, outline="black")

# ---------- cheeks ----------
cheek_color = (255, 182, 193)   # LightPink
draw.ellipse([140, 260, 180, 290], fill=cheek_color)
draw.ellipse([320, 260, 360, 290], fill=cheek_color)

# ---------- hair (top semicircle) ----------
hair_color = (0, 0, 0)          # black
hair_bbox = [85, 85, 415, 415]  # slightly larger than head
draw.pieslice(hair_bbox, start=180, end=0, fill=hair_color)

# a few subtle hair strands
strand_color = (40, 40, 40)     # dark grey
draw.arc([150, 110, 350, 200], start=180, end=0, fill=strand_color, width=1)
draw.arc([120, 130, 380, 220], start=180, end=0, fill=strand_color, width=1)
draw.arc([100, 150, 400, 240], start=180, end=0, fill=strand_color, width=1)

# ---------- eyes ----------
eye_white = (255, 255, 255)
left_eye_bbox = [170, 215, 230, 245]
right_eye_bbox = [270, 215, 330, 245]
draw.ellipse(left_eye_bbox, fill=eye_white, outline="black")
draw.ellipse(right_eye_bbox, fill=eye_white, outline="black")

# irises
iris_color = (30, 144, 255)   # DodgerBlue
left_iris_bbox = [185, 225, 215, 240]
right_iris_bbox = [285, 225, 315, 240]
draw.ellipse(left_iris_bbox, fill=iris_color, outline="black")
draw.ellipse(right_iris_bbox, fill=iris_color, outline="black")

# pupils
left_pupil_bbox = [193, 230, 207, 235]
right_pupil_bbox = [293, 230, 307, 235]
draw.ellipse(left_pupil_bbox, fill="black")
draw.ellipse(right_pupil_bbox, fill="black")

# eye highlights (catchlights)
draw.ellipse([196, 232, 200, 236], fill="white")
draw.ellipse([296, 232, 300, 236], fill="white")

# ---------- eyebrows ----------
eyebrow_color = (0, 0, 0)
left_brow_bbox = [165, 195, 235, 215]
right_brow_bbox = [265, 195, 335, 215]
draw.arc(left_brow_bbox, start=180, end=0, fill=eyebrow_color, width=2)
draw.arc(right_brow_bbox, start=180, end=0, fill=eyebrow_color, width=2)

# ---------- nose ----------
draw.line([(250, 250), (250, 290)], fill="black", width=2)   # bridge
draw.ellipse([235, 285, 245, 295], fill="black")            # left nostril
draw.ellipse([255, 285, 265, 295], fill="black")            # right nostril

# ---------- mouth (smile) ----------
draw.arc([230, 310, 270, 340], start=0, end=180, fill="black", width=3)

# ---------- save ----------
img.save("portrait.png")
```