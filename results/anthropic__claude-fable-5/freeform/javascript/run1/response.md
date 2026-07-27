I'd like to draw a twilight mountain lake — layered silhouette ridges fading into a warm horizon, a glowing moon with its shimmering reflection stretched across the water, stars, pines, birds, and a few fireflies. It's a scene built entirely from gradients and simple math, which is what makes procedural canvas art fun: atmosphere out of sines and alpha.

I'll use a seeded random generator so the scene is reproducible, sum-of-sines for natural-looking mountain ridges, and horizontal streaks for the classic "moonglade" reflection on water.

```js
const ctx = document.getElementById('canvas').getContext('2d');
const W = 500, H = 500, HORIZON = 320;

// Seeded PRNG (mulberry32) for reproducible art
function mulberry32(a) {
  return function() {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(20240613);

// ---------- SKY ----------
const sky = ctx.createLinearGradient(0, 0, 0, HORIZON);
sky.addColorStop(0.00, '#0a0d2e');
sky.addColorStop(0.45, '#372a63');
sky.addColorStop(0.72, '#7c3f6d');
sky.addColorStop(0.90, '#c96a55');
sky.addColorStop(1.00, '#f0a05f');
ctx.fillStyle = sky;
ctx.fillRect(0, 0, W, HORIZON);

// ---------- STARS ----------
for (let i = 0; i < 150; i++) {
  const x = rand() * W;
  const y = rand() * 250;
  const fade = 1 - y / 280;               // stars fade near horizon glow
  const a = (0.25 + rand() * 0.75) * fade;
  const r = rand() < 0.12 ? 1.4 : 0.7;
  ctx.fillStyle = `rgba(255,245,225,${a.toFixed(3)})`;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}

// ---------- MOON ----------
const mx = 355, my = 105, mr = 34;
const glow = ctx.createRadialGradient(mx, my, mr * 0.4, mx, my, mr * 3.4);
glow.addColorStop(0, 'rgba(255,240,210,0.55)');
glow.addColorStop(0.4, 'rgba(255,220,180,0.16)');
glow.addColorStop(1, 'rgba(255,220,180,0)');
ctx.fillStyle = glow;
ctx.fillRect(mx - mr * 3.4, my - mr * 3.4, mr * 6.8, mr * 6.8);

const moon = ctx.createRadialGradient(mx - 10, my - 10, 4, mx, my, mr);
moon.addColorStop(0, '#fffdf2');
moon.addColorStop(1, '#f3d9a8');
ctx.fillStyle = moon;
ctx.beginPath();
ctx.arc(mx, my, mr, 0, Math.PI * 2);
ctx.fill();
// faint craters
ctx.fillStyle = 'rgba(210,180,140,0.35)';
[[ -8, -4, 6 ], [ 10, 8, 4.5 ], [ 2, 14, 3 ], [ -14, 12, 3.5 ]].forEach(([dx, dy, r]) => {
  ctx.beginPath();
  ctx.arc(mx + dx, my + dy, r, 0, Math.PI * 2);
  ctx.fill();
});

// ---------- MOUNTAINS (layered ridges via sum of sines) ----------
function makeRidge(base, amp, roughness) {
  const p = [rand() * 9, rand() * 9, rand() * 9];
  const f = [0.006 + rand() * 0.004, 0.015 + rand() * 0.01, 0.045 * roughness];
  const ys = [];
  for (let x = 0; x <= W; x++) {
    const n = 0.55 * Math.sin(x * f[0] + p[0])
            + 0.30 * Math.sin(x * f[1] + p[1])
            + 0.15 * Math.sin(x * f[2] + p[2]);
    ys.push(base - amp * (0.5 + 0.5 * n));
  }
  return ys;
}
function fillRidge(ys, bottom, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(0, ys[0]);
  for (let x = 1; x <= W; x++) ctx.lineTo(x, ys[x]);
  ctx.lineTo(W, bottom);
  ctx.lineTo(0, bottom);
  ctx.closePath();
  ctx.fill();
}
const layers = [
  { base: 275, amp: 85, rough: 0.8, color: '#8a4f70' },
  { base: 295, amp: 90, rough: 1.0, color: '#5d3560' },
  { base: 315, amp: 80, rough: 1.2, color: '#3a2350' },
  { base: 322, amp: 55, rough: 1.4, color: '#221640' },
];
const ridgeData = layers.map(L => makeRidge(L.base, L.amp, L.rough));
layers.forEach((L, i) => fillRidge(ridgeData[i], HORIZON, L.color));

// mist band hugging the horizon
const mist = ctx.createLinearGradient(0, 285, 0, HORIZON);
mist.addColorStop(0, 'rgba(240,170,110,0)');
mist.addColorStop(1, 'rgba(240,170,110,0.28)');
ctx.fillStyle = mist;
ctx.fillRect(0, 285, W, HORIZON - 285);

// ---------- BIRDS ----------
ctx.strokeStyle = 'rgba(20,12,35,0.85)';
ctx.lineWidth = 1.4;
ctx.lineCap = 'round';
[[95, 130, 8], [125, 118, 6], [150, 140, 7], [418, 175, 6], [443, 163, 5]].forEach(([bx, by, s]) => {
  ctx.beginPath();
  ctx.moveTo(bx - s, by);
  ctx.quadraticCurveTo(bx - s / 2, by - s * 0.8, bx, by);
  ctx.quadraticCurveTo(bx + s / 2, by - s * 0.8, bx + s, by);
  ctx.stroke();
});

// ---------- WATER ----------
const water = ctx.createLinearGradient(0, HORIZON, 0, H);
water.addColorStop(0.00, '#d8794f');
water.addColorStop(0.12, '#7c3a58');
water.addColorStop(0.40, '#2c1c4a');
water.addColorStop(1.00, '#0b0d28');
ctx.fillStyle = water;
ctx.fillRect(0, HORIZON, W, H - HORIZON);

// faint mirrored mountains
ctx.save();
ctx.globalAlpha = 0.22;
ctx.translate(0, HORIZON * 2);
ctx.scale(1, -1);
layers.forEach((L, i) => fillRidge(ridgeData[i], HORIZON, L.color));
ctx.restore();

// horizontal ripple lines
for (let i = 0; i < 55; i++) {
  const y = HORIZON + 4 + rand() * (H - HORIZON - 10);
  const depth = (y - HORIZON) / (H - HORIZON);
  const len = 15 + rand() * (30 + depth * 130);
  const x = rand() * (W - len);
  ctx.strokeStyle = `rgba(190,150,200,${(0.05 + rand() * 0.08).toFixed(3)})`;
  ctx.lineWidth = 0.8 + depth * 1.2;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + len, y);
  ctx.stroke();
}

// moonglade — shimmering reflection column
for (let i = 0; i < 60; i++) {
  const y = HORIZON + 3 + rand() * (H - HORIZON - 20);
  const depth = (y - HORIZON) / (H - HORIZON);
  const spread = 8 + depth * 55;
  const len = 6 + rand() * spread;
  const x = mx + (rand() - 0.5) * spread * 1.6 - len / 2;
  ctx.strokeStyle = `rgba(255,225,175,${(0.10 + rand() * 0.28 * (1 - depth * 0.5)).toFixed(3)})`;
  ctx.lineWidth = 1 + rand() * 1.6;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + len, y);
  ctx.stroke();
}

// ---------- FOREGROUND BANK & PINES ----------
ctx.fillStyle = '#0a081e';
ctx.beginPath();
ctx.moveTo(0, 500);
ctx.lineTo(0, 425);
ctx.bezierCurveTo(90, 448, 160, 470, 250, 478);
ctx.bezierCurveTo(350, 486, 430, 468, 500, 448);
ctx.lineTo(500, 500);
ctx.closePath();
ctx.fill();

function pine(x, baseY, h) {
  ctx.fillStyle = '#0a081e';
  ctx.fillRect(x - h * 0.03, baseY - h * 0.18, h * 0.06, h * 0.2);
  for (let t = 0; t < 3; t++) {
    const w = h * (0.42 - t * 0.10);
    const top = baseY - h * (0.42 + t * 0.29);
    const bot = baseY - h * (0.12 + t * 0.24);
    ctx.beginPath();
    ctx.moveTo(x, top);
    ctx.lineTo(x - w, bot);
    ctx.lineTo(x + w, bot);
    ctx.closePath();
    ctx.fill();
  }
}
pine(30, 452, 95);
pine(68, 462, 70);
pine(105, 472, 52);
pine(462, 470, 88);
pine(425, 478, 60);

// ---------- FIREFLIES ----------
for (let i = 0; i < 14; i++) {
  const x = rand() * W;
  const y = 430 + rand() * 60;
  const r = 1 + rand() * 1.5;
  const g = ctx.createRadialGradient(x, y, 0, x, y, r * 5);
  g.addColorStop(0, 'rgba(220,255,150,0.9)');
  g.addColorStop(0.3, 'rgba(190,240,110,0.35)');
  g.addColorStop(1, 'rgba(190,240,110,0)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(x, y, r * 5, 0, Math.PI * 2);
  ctx.fill();
}

// ---------- VIGNETTE ----------
const vig = ctx.createRadialGradient(W / 2, H / 2, 200, W / 2, H / 2, 380);
vig.addColorStop(0, 'rgba(0,0,0,0)');
vig.addColorStop(1, 'rgba(5,0,20,0.35)');
ctx.fillStyle = vig;
ctx.fillRect(0, 0, W, H);
```

The scene layers from back to front: a warm-to-indigo sky gradient, stars that fade near the horizon glow, a cratered moon with soft radiance, four mountain ridges that get darker and rougher as they approach (cheap atmospheric perspective), then water with a faint mirrored world, drifting ripple strokes, and a moonglade that widens and disperses toward the viewer — just like real reflections do. A dark bank with pines and a scattering of fireflies anchors the foreground, and a subtle vignette pulls the eye to the center.