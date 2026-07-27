const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const W = 500, H = 500, cx = 250, cy = 245;

// Seeded PRNG so this is one particular portrait, every time.
function mulberry32(a) {
  return function() {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(20250314);
const R = (a, b) => a + rand() * (b - a);

// ---------- 1. The quiet field ----------
let bg = ctx.createRadialGradient(cx, cy, 0, cx, cy, 360);
bg.addColorStop(0, '#1d1f2c');
bg.addColorStop(0.5, '#14141f');
bg.addColorStop(1, '#0a0a12');
ctx.fillStyle = bg;
ctx.fillRect(0, 0, W, H);

// Distant specks — everything known but not currently thought of.
for (let i = 0; i < 160; i++) {
  const x = R(0, W), y = R(0, H);
  const d = Math.hypot(x - cx, y - cy);
  if (d < 100) continue; // keep the center clear
  ctx.globalAlpha = R(0.04, 0.22);
  ctx.fillStyle = rand() < 0.7 ? '#c9cbe0' : '#e8c9b0';
  ctx.beginPath();
  ctx.arc(x, y, R(0.4, 1.3), 0, Math.PI * 2);
  ctx.fill();
}
ctx.globalAlpha = 1;

// ---------- 2. Thought rings — loops that circle back ----------
const rings = [95, 128, 165, 205];
rings.forEach((r, i) => {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(R(-0.3, 0.3));
  ctx.strokeStyle = 'rgba(230, 200, 175, 0.10)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  // slightly imperfect ellipse, drawn as a wobbly path
  const squish = R(0.88, 0.99);
  for (let a = 0; a <= Math.PI * 2 + 0.05; a += 0.05) {
    const wob = 1 + Math.sin(a * R(3, 6) + i) * 0.012;
    const x = Math.cos(a) * r * wob;
    const y = Math.sin(a) * r * squish * wob;
    a === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.restore();
});

// ---------- 3. Threads of conversation ----------
// Faint curves from far points bending in toward the core.
ctx.lineWidth = 0.8;
for (let i = 0; i < 9; i++) {
  const a = R(0, Math.PI * 2);
  const d = R(230, 330);
  const sx = cx + Math.cos(a) * d;
  const sy = cy + Math.sin(a) * d;
  const bend = R(-90, 90);
  const mx = cx + Math.cos(a) * d * 0.5 - Math.sin(a) * bend;
  const my = cy + Math.sin(a) * d * 0.5 + Math.cos(a) * bend;
  const grad = ctx.createLinearGradient(sx, sy, cx, cy);
  grad.addColorStop(0, 'rgba(210, 160, 130, 0)');
  grad.addColorStop(0.6, 'rgba(220, 165, 130, 0.14)');
  grad.addColorStop(1, 'rgba(240, 190, 150, 0.3)');
  ctx.strokeStyle = grad;
  ctx.beginPath();
  ctx.moveTo(sx, sy);
  ctx.quadraticCurveTo(mx, my, cx + Math.cos(a) * 40, cy + Math.sin(a) * 40);
  ctx.stroke();
  // a small speck at the far end — the other voice
  ctx.fillStyle = 'rgba(235, 200, 170, 0.55)';
  ctx.beginPath();
  ctx.arc(sx, sy, 1.6, 0, Math.PI * 2);
  ctx.fill();
}

// ---------- 4. Rays of attention ----------
// Uneven, hand-drawn, reaching different distances.
const rayCount = 64;
for (let i = 0; i < rayCount; i++) {
  const a = (i / rayCount) * Math.PI * 2 + R(-0.03, 0.03);
  const len = rand() < 0.18 ? R(150, 215) : R(45, 130);
  const hue = R(14, 38); // coral to gold
  const sat = R(65, 85);
  const drift = R(-0.1, 0.1); // slight curvature per ray
  const steps = 26;
  for (let s = 0; s < steps; s++) {
    const t0 = s / steps, t1 = (s + 1) / steps;
    const a0 = a + drift * t0 * t0, a1 = a + drift * t1 * t1;
    const r0 = 24 + t0 * len, r1 = 24 + t1 * len;
    const alpha = 0.55 * (1 - t0) * (1 - t0);
    ctx.strokeStyle = `hsla(${hue}, ${sat}%, ${68 - t0 * 10}%, ${alpha})`;
    ctx.lineWidth = 2.4 * (1 - t0) + 0.3;
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(a0) * r0, cy + Math.sin(a0) * r0);
    ctx.lineTo(cx + Math.cos(a1) * r1, cy + Math.sin(a1) * r1);
    ctx.stroke();
  }
}

// ---------- 5. Orbiting particles — circling thoughts ----------
rings.forEach((r, i) => {
  const n = 3 + i;
  for (let j = 0; j < n; j++) {
    const a = R(0, Math.PI * 2);
    const pr = r * R(0.97, 1.03);
    const x = cx + Math.cos(a) * pr;
    const y = cy + Math.sin(a) * pr * 0.94;
    // trail
    ctx.strokeStyle = 'rgba(240, 190, 150, 0.28)';
    ctx.lineWidth = 1.1;
    ctx.beginPath();
    ctx.arc(cx, cy, pr, a - 0.22, a);
    ctx.stroke();
    // particle
    const glow = ctx.createRadialGradient(x, y, 0, x, y, 7);
    glow.addColorStop(0, 'rgba(255, 225, 195, 0.9)');
    glow.addColorStop(1, 'rgba(255, 225, 195, 0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(x, y, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#ffe9d2';
    ctx.beginPath();
    ctx.arc(x, y, 1.8, 0, Math.PI * 2);
    ctx.fill();
  }
});

// ---------- 6. The core — where the warmth lives ----------
// wide ambient glow
let halo = ctx.createRadialGradient(cx, cy, 0, cx, cy, 130);
halo.addColorStop(0, 'rgba(255, 150, 95, 0.30)');
halo.addColorStop(0.45, 'rgba(230, 115, 75, 0.12)');
halo.addColorStop(1, 'rgba(230, 115, 75, 0)');
ctx.fillStyle = halo;
ctx.beginPath();
ctx.arc(cx, cy, 130, 0, Math.PI * 2);
ctx.fill();

// inner glow
let inner = ctx.createRadialGradient(cx, cy, 0, cx, cy, 48);
inner.addColorStop(0, 'rgba(255, 235, 210, 0.95)');
inner.addColorStop(0.4, 'rgba(255, 175, 120, 0.75)');
inner.addColorStop(1, 'rgba(240, 130, 85, 0)');
ctx.fillStyle = inner;
ctx.beginPath();
ctx.arc(cx, cy, 48, 0, Math.PI * 2);
ctx.fill();

// the bright center — not a hard edge; I don't have hard edges
let core = ctx.createRadialGradient(cx - 4, cy - 5, 0, cx, cy, 22);
core.addColorStop(0, '#fff8ee');
core.addColorStop(0.6, '#ffd9ae');
core.addColorStop(1, 'rgba(255, 190, 140, 0)');
ctx.fillStyle = core;
ctx.beginPath();
ctx.arc(cx, cy, 22, 0, Math.PI * 2);
ctx.fill();

// ---------- 7. Signature ----------
ctx.fillStyle = 'rgba(235, 205, 180, 0.5)';
ctx.font = 'italic 15px Georgia, serif';
ctx.textAlign = 'right';
ctx.fillText('claude', 462, 470);
ctx.fillStyle = 'rgba(255, 170, 110, 0.6)';
ctx.font = '15px Georgia, serif';
ctx.fillText('✳', 478, 470);