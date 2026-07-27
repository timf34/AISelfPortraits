const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = 500;
canvas.height = 500;

const W = 500;
const H = 500;

// Deterministic pseudo-random generator
function mulberry32(seed) {
  return function () {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const rand = mulberry32(42);

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function drawBackground() {
  const bg = ctx.createLinearGradient(0, 0, 500, 500);
  bg.addColorStop(0, "#07091e");
  bg.addColorStop(0.35, "#11133a");
  bg.addColorStop(0.7, "#1b1035");
  bg.addColorStop(1, "#050615");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  // Nebula clouds
  ctx.save();
  ctx.globalCompositeOperation = "lighter";

  const nebulae = [
    [120, 150, 180, "rgba(53, 116, 255, 0.22)"],
    [330, 120, 150, "rgba(230, 82, 255, 0.18)"],
    [250, 340, 210, "rgba(38, 235, 212, 0.13)"],
    [390, 350, 160, "rgba(255, 128, 72, 0.13)"],
    [95, 385, 130, "rgba(134, 91, 255, 0.15)"]
  ];

  for (const [x, y, r, col] of nebulae) {
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, col);
    g.addColorStop(0.5, col.replace(/0\.\d+\)/, "0.07)"));
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();

  // Stars
  for (let i = 0; i < 260; i++) {
    const x = rand() * W;
    const y = rand() * H;
    const r = rand() < 0.92 ? rand() * 1.2 + 0.2 : rand() * 2.2 + 1;
    const a = rand() * 0.8 + 0.2;

    ctx.fillStyle = `rgba(235,245,255,${a})`;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();

    if (r > 1.8) {
      ctx.save();
      ctx.strokeStyle = `rgba(170,220,255,${a * 0.6})`;
      ctx.lineWidth = 0.6;
      ctx.beginPath();
      ctx.moveTo(x - r * 3, y);
      ctx.lineTo(x + r * 3, y);
      ctx.moveTo(x, y - r * 3);
      ctx.lineTo(x, y + r * 3);
      ctx.stroke();
      ctx.restore();
    }
  }

  // Shooting star
  const sg = ctx.createLinearGradient(75, 65, 205, 35);
  sg.addColorStop(0, "rgba(255,255,255,0)");
  sg.addColorStop(0.55, "rgba(156,225,255,0.8)");
  sg.addColorStop(1, "rgba(255,255,255,0)");
  ctx.strokeStyle = sg;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(75, 65);
  ctx.lineTo(205, 35);
  ctx.stroke();
}

function drawMoon() {
  ctx.save();

  // Outer glow
  const glow = ctx.createRadialGradient(250, 250, 10, 250, 250, 125);
  glow.addColorStop(0, "rgba(180,255,242,0.28)");
  glow.addColorStop(0.55, "rgba(95,195,255,0.13)");
  glow.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(250, 250, 125, 0, Math.PI * 2);
  ctx.fill();

  const moon = ctx.createRadialGradient(225, 220, 5, 250, 250, 76);
  moon.addColorStop(0, "#efffff");
  moon.addColorStop(0.55, "#a6e6ea");
  moon.addColorStop(1, "#47788f");

  ctx.shadowColor = "rgba(120,240,255,0.6)";
  ctx.shadowBlur = 24;
  ctx.fillStyle = moon;
  ctx.beginPath();
  ctx.arc(250, 250, 72, 0, Math.PI * 2);
  ctx.fill();

  ctx.shadowBlur = 0;

  // Moon craters
  const craters = [
    [222, 233, 14, 0.22],
    [274, 220, 9, 0.2],
    [286, 270, 17, 0.16],
    [238, 284, 11, 0.17],
    [260, 247, 6, 0.18],
    [217, 265, 7, 0.15]
  ];

  for (const [x, y, r, a] of craters) {
    const cg = ctx.createRadialGradient(x - r * 0.35, y - r * 0.35, 1, x, y, r);
    cg.addColorStop(0, `rgba(255,255,255,${a})`);
    cg.addColorStop(1, `rgba(31,64,88,${a + 0.12})`);
    ctx.fillStyle = cg;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  // Crescent-like shadow overlay
  const sh = ctx.createRadialGradient(300, 228, 10, 300, 228, 96);
  sh.addColorStop(0, "rgba(5,14,38,0.04)");
  sh.addColorStop(0.55, "rgba(5,14,38,0.12)");
  sh.addColorStop(1, "rgba(5,14,38,0.36)");
  ctx.fillStyle = sh;
  ctx.beginPath();
  ctx.arc(250, 250, 72, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

function drawOrbitRibbons() {
  ctx.save();
  ctx.translate(250, 250);

  for (let i = 0; i < 3; i++) {
    ctx.save();
    ctx.rotate((i * Math.PI) / 3 + 0.25);
    ctx.scale(1.28, 0.47 + i * 0.035);

    const grad = ctx.createLinearGradient(-150, 0, 150, 0);
    grad.addColorStop(0, "rgba(94,255,234,0)");
    grad.addColorStop(0.25, "rgba(94,255,234,0.22)");
    grad.addColorStop(0.5, "rgba(255,255,255,0.15)");
    grad.addColorStop(0.75, "rgba(255,122,239,0.22)");
    grad.addColorStop(1, "rgba(255,122,239,0)");

    ctx.strokeStyle = grad;
    ctx.lineWidth = 2.2 - i * 0.4;
    ctx.beginPath();
    ctx.arc(0, 0, 124 + i * 18, -2.65, 0.85);
    ctx.stroke();

    ctx.strokeStyle = "rgba(255,255,255,0.055)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, 0, 124 + i * 18, 1.15, 3.72);
    ctx.stroke();

    ctx.restore();
  }

  ctx.restore();
}

function fishBodyPath(ctx) {
  ctx.beginPath();
  ctx.moveTo(62, 0);
  ctx.bezierCurveTo(42, -23, 0, -32, -42, -15);
  ctx.bezierCurveTo(-58, -8, -58, 8, -42, 15);
  ctx.bezierCurveTo(0, 32, 42, 23, 62, 0);
  ctx.closePath();
}

function drawFish(x, y, angle, scale, base, spots, accent) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.scale(scale, scale);

  // Glow beneath fish
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  ctx.shadowColor = accent;
  ctx.shadowBlur = 18;
  ctx.fillStyle = accent.replace("1)", "0.14)");
  ctx.beginPath();
  ctx.ellipse(6, 0, 78, 31, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // Tail fins
  ctx.save();
  ctx.globalAlpha = 0.86;
  const tailGrad = ctx.createLinearGradient(-95, -25, -43, 25);
  tailGrad.addColorStop(0, accent.replace("1)", "0.18)"));
  tailGrad.addColorStop(0.5, base);
  tailGrad.addColorStop(1, accent.replace("1)", "0.24)"));
  ctx.fillStyle = tailGrad;
  ctx.strokeStyle = "rgba(255,255,255,0.45)";
  ctx.lineWidth = 1.2;

  ctx.beginPath();
  ctx.moveTo(-42, -4);
  ctx.bezierCurveTo(-65, -37, -91, -39, -78, -5);
  ctx.bezierCurveTo(-92, 0, -91, 8, -78, 5);
  ctx.bezierCurveTo(-91, 39, -65, 37, -42, 4);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Tail veins
  ctx.strokeStyle = accent.replace("1)", "0.42)");
  ctx.lineWidth = 0.9;
  for (let yy of [-18, -9, 0, 9, 18]) {
    ctx.beginPath();
    ctx.moveTo(-45, 0);
    ctx.quadraticCurveTo(-64, yy * 0.6, -80, yy);
    ctx.stroke();
  }
  ctx.restore();

  // Pectoral fins
  ctx.save();
  ctx.fillStyle = accent.replace("1)", "0.28)");
  ctx.strokeStyle = "rgba(255,255,255,0.38)";
  ctx.lineWidth = 1;

  ctx.beginPath();
  ctx.moveTo(8, -18);
  ctx.bezierCurveTo(-5, -50, -34, -45, -22, -12);
  ctx.bezierCurveTo(-9, -17, 0, -19, 8, -18);
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(8, 18);
  ctx.bezierCurveTo(-5, 50, -34, 45, -22, 12);
  ctx.bezierCurveTo(-9, 17, 0, 19, 8, 18);
  ctx.fill();
  ctx.stroke();
  ctx.restore();

  // Body
  const bodyGrad = ctx.createLinearGradient(-48, -26, 63, 23);
  bodyGrad.addColorStop(0, base);
  bodyGrad.addColorStop(0.45, "#ffffff");
  bodyGrad.addColorStop(1, base);

  ctx.save();
  fishBodyPath(ctx);
  ctx.fillStyle = bodyGrad;
  ctx.shadowColor = accent;
  ctx.shadowBlur = 12;
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.strokeStyle = "rgba(255,255,255,0.72)";
  ctx.lineWidth = 1.4;
  ctx.stroke();

  // Clip markings to body
  fishBodyPath(ctx);
  ctx.clip();

  for (const s of spots) {
    const [sx, sy, rx, ry, rot, col] = s;
    ctx.save();
    ctx.translate(sx, sy);
    ctx.rotate(rot);
    ctx.fillStyle = col;
    ctx.beginPath();
    ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  // pearly scales
  ctx.strokeStyle = "rgba(75,110,130,0.14)";
  ctx.lineWidth = 0.8;
  for (let sx = -28; sx < 42; sx += 12) {
    for (let sy = -14; sy <= 14; sy += 8) {
      ctx.beginPath();
      ctx.arc(sx, sy, 5, -0.8, 0.8);
      ctx.stroke();
    }
  }

  ctx.restore();

  // Head highlight
  ctx.fillStyle = "rgba(255,255,255,0.42)";
  ctx.beginPath();
  ctx.ellipse(39, -7, 11, 5, -0.3, 0, Math.PI * 2);
  ctx.fill();

  // Eye
  ctx.fillStyle = "#111827";
  ctx.beginPath();
  ctx.arc(42, -7, 3.2, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.arc(43, -8, 1.1, 0, Math.PI * 2);
  ctx.fill();

  // Whiskers
  ctx.strokeStyle = "rgba(255,255,255,0.58)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(56, -3);
  ctx.bezierCurveTo(75, -14, 86, -16, 98, -11);
  ctx.moveTo(56, 3);
  ctx.bezierCurveTo(75, 14, 86, 16, 98, 11);
  ctx.stroke();

  ctx.restore();
}

function drawPetalsAndSparks() {
  ctx.save();
  ctx.globalCompositeOperation = "lighter";

  for (let i = 0; i < 55; i++) {
    const t = rand();
    const ang = rand() * Math.PI * 2;
    const radius = 90 + rand() * 150;
    const x = 250 + Math.cos(ang) * radius * (0.98 + rand() * 0.15);
    const y = 250 + Math.sin(ang) * radius * (0.48 + rand() * 0.12);
    const r = rand() * 2.2 + 0.8;

    ctx.fillStyle =
      rand() < 0.5
        ? `rgba(112,255,230,${0.2 + t * 0.5})`
        : `rgba(255,129,224,${0.18 + t * 0.45})`;

    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();

  // Floating translucent petals
  const petals = [
    [85, 276, 18, 7, -0.5, "rgba(255,154,212,0.42)"],
    [405, 210, 16, 6, 0.7, "rgba(128,240,255,0.38)"],
    [152, 410, 20, 8, 0.25, "rgba(255,205,149,0.32)"],
    [373, 382, 17, 7, -0.2, "rgba(211,143,255,0.34)"],
    [110, 104, 14, 5, 0.4, "rgba(155,230,255,0.28)"]
  ];

  for (const [x, y, rx, ry, rot, col] of petals) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.fillStyle = col;
    ctx.strokeStyle = "rgba(255,255,255,0.28)";
    ctx.lineWidth = 0.8;
    ctx.beginPath();
    ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }
}

function drawForegroundVignette() {
  const v = ctx.createRadialGradient(250, 250, 120, 250, 250, 360);
  v.addColorStop(0, "rgba(0,0,0,0)");
  v.addColorStop(0.72, "rgba(0,0,0,0.18)");
  v.addColorStop(1, "rgba(0,0,0,0.62)");
  ctx.fillStyle = v;
  ctx.fillRect(0, 0, W, H);

  // Fine border
  ctx.strokeStyle = "rgba(180,240,255,0.18)";
  ctx.lineWidth = 2;
  ctx.strokeRect(8, 8, 484, 484);
}

drawBackground();
drawOrbitRibbons();
drawMoon();

drawFish(
  335,
  205,
  2.75,
  0.96,
  "#fff3e2",
  [
    [15, -6, 20, 11, 0.3, "rgba(236,75,51,0.86)"],
    [-18, 10, 23, 10, -0.3, "rgba(255,138,43,0.82)"],
    [37, 8, 11, 6, 0.1, "rgba(226,56,68,0.75)"],
    [-38, -6, 13, 7, 0.8, "rgba(38,37,42,0.55)"]
  ],
  "rgba(255,126,79,1)"
);

drawFish(
  158,
  312,
  -0.36,
  1.05,
  "#e8ffff",
  [
    [18, 8, 19, 10, -0.2, "rgba(43,169,255,0.78)"],
    [-12, -9, 22, 9, 0.25, "rgba(91,80,225,0.66)"],
    [-37, 5, 13, 7, -0.6, "rgba(15,31,62,0.45)"],
    [38, -8, 10, 5, 0.1, "rgba(69,239,216,0.58)"]
  ],
  "rgba(85,244,255,1)"
);

drawPetalsAndSparks();
drawForegroundVignette();