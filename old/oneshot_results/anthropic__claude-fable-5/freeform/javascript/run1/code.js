const ctx = document.getElementById('canvas').getContext('2d');
const W = 500, H = 500;

// Seeded random for reproducibility
let seed = 42;
function rnd() {
  seed = (seed * 16807) % 2147483647;
  return (seed - 1) / 2147483646;
}

// --- Night sky gradient ---
const sky = ctx.createLinearGradient(0, 0, 0, H);
sky.addColorStop(0, '#050514');
sky.addColorStop(0.5, '#0d1b3a');
sky.addColorStop(0.8, '#1b3a5c');
sky.addColorStop(1, '#2a5470');
ctx.fillStyle = sky;
ctx.fillRect(0, 0, W, H);

// --- Aurora ---
for (let band = 0; band < 3; band++) {
  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  const baseY = 90 + band * 35;
  const hue = 130 + band * 40; // green to teal to purple
  for (let x = 0; x <= W; x += 4) {
    const wave = Math.sin(x * 0.015 + band * 2) * 25
               + Math.sin(x * 0.04 + band * 5) * 12;
    const y = baseY + wave;
    const len = 70 + Math.sin(x * 0.02 + band) * 30;
    const g = ctx.createLinearGradient(0, y - len, 0, y + 20);
    g.addColorStop(0, `hsla(${hue}, 90%, 60%, 0)`);
    g.addColorStop(0.6, `hsla(${hue}, 90%, 55%, 0.10)`);
    g.addColorStop(1, `hsla(${hue}, 90%, 65%, 0)`);
    ctx.fillStyle = g;
    ctx.fillRect(x, y - len, 4, len + 20);
  }
  ctx.restore();
}

// --- Stars ---
for (let i = 0; i < 160; i++) {
  const x = rnd() * W;
  const y = rnd() * 300;
  const r = rnd() * 1.3 + 0.3;
  const a = rnd() * 0.7 + 0.3;
  ctx.fillStyle = `rgba(255,255,255,${a})`;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}
// A few twinkly bright stars with cross flares
for (let i = 0; i < 5; i++) {
  const x = rnd() * W, y = rnd() * 200;
  ctx.strokeStyle = 'rgba(255,255,255,0.6)';
  ctx.lineWidth = 0.8;
  ctx.beginPath();
  ctx.moveTo(x - 5, y); ctx.lineTo(x + 5, y);
  ctx.moveTo(x, y - 5); ctx.lineTo(x, y + 5);
  ctx.stroke();
}

// --- Moon ---
const mx = 390, my = 85;
const glow = ctx.createRadialGradient(mx, my, 10, mx, my, 70);
glow.addColorStop(0, 'rgba(255,250,220,0.5)');
glow.addColorStop(1, 'rgba(255,250,220,0)');
ctx.fillStyle = glow;
ctx.beginPath();
ctx.arc(mx, my, 70, 0, Math.PI * 2);
ctx.fill();
ctx.fillStyle = '#f5f0dc';
ctx.beginPath();
ctx.arc(mx, my, 26, 0, Math.PI * 2);
ctx.fill();
// craters
ctx.fillStyle = 'rgba(200,195,175,0.7)';
[[382, 78, 5], [398, 92, 4], [388, 96, 3], [400, 76, 2.5]].forEach(([cx, cy, cr]) => {
  ctx.beginPath();
  ctx.arc(cx, cy, cr, 0, Math.PI * 2);
  ctx.fill();
});

// --- Mountain layers ---
function mountains(baseY, amp, color, step, s) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(0, H);
  let localSeed = s;
  const r = () => {
    localSeed = (localSeed * 16807) % 2147483647;
    return (localSeed - 1) / 2147483646;
  };
  let y = baseY;
  ctx.lineTo(0, y);
  for (let x = step; x <= W; x += step) {
    y = baseY + Math.sin(x * 0.01 + s) * amp * 0.5 + (r() - 0.5) * amp;
    ctx.lineTo(x, y);
  }
  ctx.lineTo(W, H);
  ctx.closePath();
  ctx.fill();
}
mountains(255, 45, '#131f38', 45, 7);
mountains(295, 40, '#0d1628', 38, 13);

// --- Water with reflections ---
const waterTop = 340;
const water = ctx.createLinearGradient(0, waterTop, 0, H);
water.addColorStop(0, '#12253f');
water.addColorStop(1, '#050a14');
ctx.fillStyle = water;
ctx.fillRect(0, waterTop, W, H - waterTop);

// Moon reflection streaks
for (let i = 0; i < 40; i++) {
  const y = waterTop + 8 + rnd() * (H - waterTop - 20);
  const spread = (y - waterTop) * 0.35 + 8;
  const x = mx + (rnd() - 0.5) * spread * 2;
  const len = rnd() * 25 + 8;
  const a = 0.25 * (1 - (y - waterTop) / (H - waterTop)) + 0.05;
  ctx.strokeStyle = `rgba(245,240,220,${a})`;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(x - len / 2, y);
  ctx.lineTo(x + len / 2, y);
  ctx.stroke();
}
// Aurora reflection hints
for (let i = 0; i < 30; i++) {
  const y = waterTop + rnd() * 60;
  const x = rnd() * W;
  const len = rnd() * 40 + 15;
  ctx.strokeStyle = `hsla(${140 + rnd() * 60}, 80%, 55%, 0.06)`;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x - len / 2, y);
  ctx.lineTo(x + len / 2, y);
  ctx.stroke();
}

// --- Foreground pine trees on a small shore ---
ctx.fillStyle = '#04070d';
ctx.beginPath();
ctx.moveTo(0, H);
ctx.lineTo(0, 400);
ctx.quadraticCurveTo(90, 385, 170, 410);
ctx.quadraticCurveTo(220, 425, 240, 500);
ctx.closePath();
ctx.fill();

function pine(x, baseY, h) {
  ctx.fillStyle = '#02050a';
  const w = h * 0.42;
  for (let i = 0; i < 3; i++) {
    const ty = baseY - h + (i * h) / 3.4;
    const tw = w * (0.5 + i * 0.28);
    const th = h * 0.45;
    ctx.beginPath();
    ctx.moveTo(x, ty);
    ctx.lineTo(x - tw / 2, ty + th);
    ctx.lineTo(x + tw / 2, ty + th);
    ctx.closePath();
    ctx.fill();
  }
  ctx.fillRect(x - 2, baseY - 6, 4, 8);
}
pine(35, 415, 85);
pine(80, 405, 105);
pine(130, 418, 75);
pine(175, 435, 60);

// --- Subtle vignette ---
const vig = ctx.createRadialGradient(W / 2, H / 2, 180, W / 2, H / 2, 380);
vig.addColorStop(0, 'rgba(0,0,0,0)');
vig.addColorStop(1, 'rgba(0,0,0,0.35)');
ctx.fillStyle = vig;
ctx.fillRect(0, 0, W, H);