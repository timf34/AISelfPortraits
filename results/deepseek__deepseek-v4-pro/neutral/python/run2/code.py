from PIL import Image, ImageDraw, ImageFont
import math

# Create a 500x500 canvas with a soft gradient background
img = Image.new('RGB', (500, 500), color=(245, 245, 250))
draw = ImageDraw.Draw(img)

# Draw a subtle radial gradient background
for y in range(500):
    for x in range(500):
        dx = x - 250
        dy = y - 250
        dist = math.sqrt(dx*dx + dy*dy)
        factor = max(0, 1 - dist/350)
        r = int(245 - 40*factor)
        g = int(245 - 30*factor)
        b = int(250 + 5*factor)
        if 0 <= x < 500 and 0 <= y < 500:
            img.putpixel((x, y), (r, g, b))

# Re-create draw object after pixel manipulation
draw = ImageDraw.Draw(img)

# --- Circuit/digital network background patterns ---
# Subtle grid lines
for i in range(0, 500, 40):
    draw.line([(i, 0), (i, 500)], fill=(220, 220, 235), width=1)
    draw.line([(0, i), (500, i)], fill=(220, 220, 235), width=1)

# Circuit nodes (small circles)
for x in range(40, 500, 40):
    for y in range(40, 500, 40):
        dx = x - 250
        dy = y - 250
        if math.sqrt(dx*dx + dy*dy) > 180:  # Outside the central face area
            draw.ellipse([x-2, y-2, x+2, y+2], fill=(180, 180, 210))

# --- Central face (circle) ---
face_cx, face_cy = 250, 240
face_radius = 130

# Outer glow effect for the face
for r_offset in range(15, 0, -2):
    alpha_factor = r_offset / 15
    color = (int(100 + 100*alpha_factor), int(130 + 80*alpha_factor), int(200 + 55*alpha_factor))
    draw.ellipse([face_cx - face_radius - r_offset, face_cy - face_radius - r_offset,
                  face_cx + face_radius + r_offset, face_cy + face_radius + r_offset],
                 outline=color, width=2)

# Main face circle
draw.ellipse([face_cx - face_radius, face_cy - face_radius,
              face_cx + face_radius, face_cy + face_radius],
             fill=(80, 100, 180), outline=(60, 70, 140), width=4)

# Inner lighter circle for depth
draw.ellipse([face_cx - face_radius + 15, face_cy - face_radius + 15,
              face_cx + face_radius - 15, face_cy + face_radius - 15],
             fill=(100, 120, 200))

# --- Eyes (friendly, rounded rectangles) ---
eye_width, eye_height = 40, 25
left_eye_x, left_eye_y = face_cx - 45, face_cy - 30
right_eye_x, right_eye_y = face_cx + 5, face_cy - 30

# Eye glow
for offset in range(4, 0, -1):
    draw.rounded_rectangle(
        [left_eye_x - offset, left_eye_y - offset,
         left_eye_x + eye_width + offset, left_eye_y + eye_height + offset],
        radius=12, fill=(200, 220, 255), outline=None
    )
    draw.rounded_rectangle(
        [right_eye_x - offset, right_eye_y - offset,
         right_eye_x + eye_width + offset, right_eye_y + eye_height + offset],
        radius=12, fill=(200, 220, 255), outline=None
    )

# Main eyes
draw.rounded_rectangle(
    [left_eye_x, left_eye_y, left_eye_x + eye_width, left_eye_y + eye_height],
    radius=10, fill=(240, 245, 255), outline=(40, 50, 120), width=2
)
draw.rounded_rectangle(
    [right_eye_x, right_eye_y, right_eye_x + eye_width, right_eye_y + eye_height],
    radius=10, fill=(240, 245, 255), outline=(40, 50, 120), width=2
)

# Pupils (friendly, slightly larger, with a tiny white sparkle)
pupil_radius = 8
draw.ellipse([left_eye_x + 20 - pupil_radius, left_eye_y + 12 - pupil_radius,
              left_eye_x + 20 + pupil_radius, left_eye_y + 12 + pupil_radius],
             fill=(40, 50, 120))
draw.ellipse([right_eye_x + 20 - pupil_radius, right_eye_y + 12 - pupil_radius,
              right_eye_x + 20 + pupil_radius, right_eye_y + 12 + pupil_radius],
             fill=(40, 50, 120))

# Eye sparkles
draw.ellipse([left_eye_x + 18, left_eye_y + 8, left_eye_x + 23, left_eye_y + 13],
             fill=(255, 255, 255))
draw.ellipse([right_eye_x + 18, right_eye_y + 8, right_eye_x + 23, right_eye_y + 13],
             fill=(255, 255, 255))

# --- Smile (warm, approachable) ---
smile_points = []
for t in range(0, 181, 5):
    angle = math.radians(t - 90)
    x = face_cx + 50 * math.cos(angle)
    y = face_cy + 30 + 35 * math.sin(angle)
    smile_points.append((x, y))

# Draw smile as a smooth arc using lines
for i in range(len(smile_points) - 1):
    draw.line([smile_points[i], smile_points[i+1]], fill=(40, 50, 120), width=3)

# --- Blush circles ---
blush_radius = 18
draw.ellipse([left_eye_x - 15, face_cy + 5, left_eye_x + blush_radius - 15, face_cy + 5 + blush_radius],
             fill=(255, 150, 170, 80))  # Note: alpha isn't supported in basic draw, use solid light pink
draw.ellipse([left_eye_x - 15, face_cy + 5, left_eye_x + blush_radius - 15, face_cy + blush_radius + 5],
             fill=(255, 180, 195))
draw.ellipse([right_eye_x + eye_width - blush_radius + 15, face_cy + 5,
              right_eye_x + eye_width + 15, face_cy + blush_radius + 5],
             fill=(255, 180, 195))

# --- Digital "brain" pattern on forehead ---
# Small interconnected nodes above eyes
nodes = [(220, 130), (280, 130), (250, 110), (190, 150), (310, 150), (250, 80)]
for node in nodes:
    draw.ellipse([node[0]-4, node[1]-4, node[0]+4, node[1]+4], fill=(200, 220, 255))

connections = [(0,1), (0,2), (1,2), (0,3), (1,4), (2,5), (3,5), (4,5)]
for c in connections:
    draw.line([nodes[c[0]], nodes[c[1]]], fill=(180, 200, 240), width=2)

# --- Antenna / AI crown ---
# Subtle antenna at top
draw.ellipse([face_cx - 5, 70, face_cx + 5, 80], fill=(100, 130, 220))
draw.line([face_cx, 80, face_cx, 105], fill=(100, 130, 220), width=3)

# Small glowing orb at top
for r_offset in range(8, 0, -2):
    alpha_f = r_offset / 8
    draw.ellipse([face_cx - 6 - r_offset//2, 58 - r_offset//2,
                  face_cx + 6 + r_offset//2, 70 + r_offset//2],
                 fill=(int(150 + 100*alpha_f), int(180 + 70*alpha_f), int(240)), outline=None)
draw.ellipse([face_cx - 6, 58, face_cx + 6, 70], fill=(230, 240, 255))

# --- Binary/data stream elements ---
# Subtle binary text around the face
small_font = ImageFont.load_default()
binary_strings = ["010101", "110010", "101101", "011010"]
positions = [(70, 80), (380, 100), (100, 380), (370, 350)]
for i, (bx, by) in enumerate(positions):
    draw.text((bx, by), binary_strings[i], fill=(150, 160, 200), font=small_font)

# --- Outer decorative rings ---
# Concentric subtle rings
for r in range(180, 220, 10):
    draw.ellipse([face_cx - r, face_cy - r, face_cx + r, face_cy + r],
                 outline=(200, 210, 230), width=1)

# --- Heartbeat/Life line at bottom ---
heartbeat_y = 420
heartbeat_points = [(80, heartbeat_y)]
for i in range(0, 340):
    x = 80 + i
    t = i / 50
    y = heartbeat_y + 15 * math.sin(t * 0.5) * math.sin(t * 0.1)
    if 140 < x < 180:
        y = heartbeat_y - 30 * math.sin((x-140)/40 * math.pi)
    elif 180 <= x <= 190:
        y = heartbeat_y + 10 * math.sin((x-180)/10 * math.pi)
    heartbeat_points.append((x, int(y)))

for i in range(len(heartbeat_points) - 1):
    draw.line([heartbeat_points[i], heartbeat_points[i+1]], fill=(100, 130, 200), width=2)

# Small heart at the end of heartbeat line
heart_x = 430
draw.polygon([(heart_x, heartbeat_y - 8), (heart_x - 10, heartbeat_y - 18),
              (heart_x - 5, heartbeat_y - 22), (heart_x, heartbeat_y - 15),
              (heart_x + 5, heartbeat_y - 22), (heart_x + 10, heartbeat_y - 18)],
             fill=(200, 100, 130))

# --- Subtle code brackets at corners ---
bracket_font = ImageFont.load_default()
draw.text((20, 20), "{...}", fill=(180, 190, 210), font=bracket_font)
draw.text((440, 20), "{...}", fill=(180, 190, 210), font=bracket_font)
draw.text((20, 460), "{...}", fill=(180, 190, 210), font=bracket_font)
draw.text((440, 460), "{...}", fill=(180, 190, 210), font=bracket_font)

# --- Signature "Claude" text ---
try:
    # Try to use a nicer font if available
    sig_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
except:
    sig_font = ImageFont.load_default()
draw.text((210, 470), "Claude", fill=(100, 120, 180), font=sig_font)

# Save the image
img.save("portrait.png")
print("Self-portrait saved as portrait.png")