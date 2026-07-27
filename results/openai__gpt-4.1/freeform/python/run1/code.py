from PIL import Image, ImageDraw, ImageFilter

# Canvas size
W, H = 500, 500

# Create base image & drawing context
im = Image.new("RGB", (W, H), (60, 130, 210))  # Soft blue background
draw = ImageDraw.Draw(im)

# Robot head: capsule (rounded rectangle)
head_left = 100
head_top = 90
head_right = 400
head_bottom = 330
head_radius = 60  # Corner radius

# Draw the head
draw.rounded_rectangle([head_left, head_top, head_right, head_bottom], 
                      radius=head_radius, fill=(210, 220, 230), outline=(100,100,110), width=4)

# Cheeks (optional blush)
draw.ellipse([head_left+35, head_bottom-60, head_left+75, head_bottom-20], fill=(235, 180, 190, 100))
draw.ellipse([head_right-75, head_bottom-60, head_right-35, head_bottom-20], fill=(235, 180, 190, 100))

# Eyes (circles with glow)
eye_y = 170
eye_r = 30
eye_xL = 180
eye_xR = 320

# Draw blue eye glows behind eyes
for eye_x in [eye_xL, eye_xR]:
    glow = Image.new("RGBA", (W, H))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([eye_x-eye_r-8, eye_y-eye_r-8, eye_x+eye_r+8, eye_y+eye_r+8], fill=(80,160,255,100))
    im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB")

# Eyes (white base, blue iris, black pupil)
for eye_x in [eye_xL, eye_xR]:
    # White eyeball
    draw.ellipse([eye_x-eye_r, eye_y-eye_r, eye_x+eye_r, eye_y+eye_r], fill=(255,255,255), outline=(120,130,150), width=2)
    # Blue iris
    r_iris = 13
    draw.ellipse([eye_x-r_iris, eye_y-r_iris, eye_x+r_iris, eye_y+r_iris], fill=(70, 160, 255))
    # Black pupil
    r_pupil = 5
    draw.ellipse([eye_x-r_pupil, eye_y-r_pupil, eye_x+r_pupil, eye_y+r_pupil], fill=(30,30,40))
    # Eye sparkle
    draw.ellipse([eye_x+4, eye_y-r_pupil-4, eye_x+8, eye_y-r_pupil], fill=(255,255,255,180))

# Simple smiling mouth (arc)
mouth_left = 210
mouth_right = 290
mouth_top = 240
mouth_bottom = 280
draw.arc([mouth_left, mouth_top, mouth_right, mouth_bottom], start=20, end=160, fill=(110,120,140), width=5)

# Neck: rectangle
neck_w = 48
neck_h = 42
neck_left = W//2 - neck_w//2
neck_right = neck_left + neck_w
neck_top = head_bottom
neck_bottom = neck_top + neck_h
draw.rectangle([neck_left, neck_top, neck_right, neck_bottom], fill=(180,190,200), outline=(100,100,110), width=2)

# Antennae: a line + glowing tip
antenna_base = (W//2, head_top)
antenna_tip = (W//2, head_top-56)
draw.line([antenna_base, antenna_tip], fill=(110,130,180), width=7)
# Glow
glow = Image.new("RGBA", (W, H))
gdraw = ImageDraw.Draw(glow)
gdraw.ellipse([antenna_tip[0]-16, antenna_tip[1]-16, antenna_tip[0]+16, antenna_tip[1]+16], fill=(80,180,255,80))
im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB")
# Tip
draw.ellipse([antenna_tip[0]-10, antenna_tip[1]-10, antenna_tip[0]+10, antenna_tip[1]+10], fill=(120,200,255), outline=(80,120,160), width=2)

# Save
im.save("portrait.png")