Sorry about that — my reply got cut off before the block finished. Here is the complete, self-contained code: an aurora borealis over a mountain lake, with a procedurally generated sky rendered offscreen so it can be flipped and wobbled into the water reflection, plus moonlight glitter, mist, and foreground pine silhouettes.

```javascript
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const W = 500, H = 500, HORIZON = 350;

// ---------- deterministic RNG (stable composition every run) ----------
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(20240613);

// ---------- offscreen "sky" canvas (everything above the horizon, so it can be reflected) ----------
const off = document.createElement('canvas');
off.width = W;
off.height = HORIZON;
const octx = off.getContext('2d');

// night sky gradient
const sky = octx.createLinearGradient(0, 0, 0, HORIZON);
sky.addColorStop(0.00, '#03040f');
sky.addColorStop(0.35, '#0a1230');
sky.addColorStop(0.62, '#14264d');
sky.addColorStop(0.85, '#1d3a63');
sky.addColorStop(1.00, '#2a5583');
octx.fillStyle = sky;
octx.fillRect(0, 0, W, HORIZON);

// faint stars
for (let i = 0; i < 230; i++) {
  const x = rand() * W;
  const y = rand() * HORIZON * 0.92;
  const r = 0.2 + rand() * 1.1;
  const a = 0.2 + rand() * 0.6;
  octx.fillStyle = 'rgba(255,255,255,' + a.toFixed(2) + ')';
  octx.beginPath();
  octx.arc(x, y, r, 0, Math.PI * 2);
  octx.fill();
}

// bright stars with glow, a few with sparkle crosses
for (let i = 0; i < 16; i++) {
  const x = rand() * W;
  const y = rand() * HORIZON * 0.7;
  const r = 1 + rand() * 1.3;
  const g = octx.createRadialGradient(x, y, 0, x, y, r * 5);
  g.addColorStop(0, 'rgba(255,255,255,0.9)');
  g.addColorStop(0.35, 'rgba(190,215,255,0.3)');
  g.addColorStop(1, 'rgba(190,215,255,0)');
  octx.fillStyle = g;
  octx.beginPath(); octx.arc(x, y, r * 5, 0, Math.PI * 2); octx.fill();
  octx.fillStyle = 'rgba(255,255,255,0.95)';
  octx.beginPath(); octx.arc(x, y, r, 0, Math.PI * 2); octx.fill();
  if (i % 3 === 0) {
    const L = r * 6;
    octx.strokeStyle = 'rgba(255,255,255,0.45)';
    octx.lineWidth = 0.7;
    octx.beginPath();
    octx.moveTo(x - L, y); octx.lineTo(x + L, y);
    octx.moveTo(x, y - L); octx.lineTo(x, y + L);
    octx.stroke();
  }
}

// shooting star
{
  const sx = 80, sy = 56, ex = 205, ey = 116;
  const g = octx.createLinearGradient(sx, sy, ex, ey);
  g.addColorStop(0, 'rgba(255,255,255,0)');
  g.addColorStop(0.7, 'rgba(200,225,255,0.5)');
  g.addColorStop(1, 'rgba(255,255,255,0.9)');
  octx.strokeStyle = g;
  octx.lineWidth = 1.6;
  octx.lineCap = 'round';
  octx.beginPath(); octx.moveTo(sx, sy); octx.lineTo(ex, ey); octx.stroke();
  const hg = octx.createRadialGradient(ex, ey, 0, ex, ey, 6);
  hg.addColorStop(0, 'rgba(255,255,255,0.95)');
  hg.addColorStop(1, 'rgba(255,255,255,0)');
  octx.fillStyle = hg;
  octx.beginPath(); octx.arc(ex, ey, 6, 0, Math.PI * 2); octx.fill();
}

// ---------- aurora borealis: vertical curtain strips, additive glow ----------
function aurora(c, opts) {
  const { yBase, amp, k, thick, hue, hue2, phase, alpha } = opts;
  c.save();
  c.globalCompositeOperation = 'lighter';
  for (let x = 0; x <= W; x += 2) {
    const t = x / W;
    const yc = yBase
      + Math.sin(t * k + phase) * amp
      + Math.sin(t * k * 2.3 + phase * 1.7) * amp * 0.35;
    const th = thick * (0.65 + 0.35 * Math.sin(t * 7 + phase * 2));
    const a = alpha * (0.45 + 0.55 * (0.5 + 0.5 * Math.sin(t * 5.2 + phase * 3.1)));
    const hh = hue + (hue2 - hue) * (0.5 + 0.5 * Math.sin(t * 3 + phase));
    const g = c.createLinearGradient(0, yc - th, 0, yc);
    g.addColorStop(0, 'hsla(' + hh + ',95%,60%,0)');
    g.addColorStop(0.75, 'hsla(' + hh + ',95%,62%,' + (a * 0.5).toFixed(3) + ')');
    g.addColorStop(1, 'hsla(' + hh + ',95%,68%,' + a.toFixed(3) + ')');
    c.fillStyle = g;
    c.fillRect(x, yc - th, 2, th);
    // bright lower edge of the curtain
    c.fillStyle = 'hsla(' + hh + ',100%,75%,' + (a * 0.55).toFixed(3) + ')';
    c.fillRect(x, yc - 2, 2, 2);
  }
  c.restore();
}
aurora(octx, { yBase: 150, amp: 34, k: 6.5, thick: 95, hue: 140, hue2: 165, phase: 0.6, alpha: 0.16 });
aurora(octx, { yBase: 192, amp: 26, k: 8.0, thick: 68, hue: 155, hue2: 190, phase: 2.4, alpha: 0.13 });
aurora(octx, { yBase: 102, amp: 20, k: 5.0, thick: 52, hue: 262, hue2: 285, phase: 4.2, alpha: 0.10 });

// ---------- moon with glow and craters ----------
const MX = 378, MY = 92, MR = 24;
{
  const g = octx.createRadialGradient(MX, MY, MR * 0.4, MX, MY, MR * 5);
  g.addColorStop(0, 'rgba(220,235,255,0.35)');
  g.addColorStop(0.4, 'rgba(180,210,255,0.12)');
  g.addColorStop(1, 'rgba(180,210,255,0)');
  octx.fillStyle = g;
  octx.beginPath(); octx.arc(MX, MY, MR * 5, 0, Math.PI * 2); octx.fill();

  const mb = octx.createRadialGradient(MX - 8, MY - 8, 2, MX, MY, MR);
  mb.addColorStop(0, '#ffffff');
  mb.addColorStop(0.6, '#e8eef7');
  mb.addColorStop(1, '#b9c6da');
  octx.fillStyle = mb;
  octx.beginPath(); octx.arc(MX, MY, MR, 0, Math.PI * 2); octx.fill();

  octx.fillStyle = 'rgba(150,165,190,0.35)';
  const craters = [[-7, -3, 4.5], [6, 7, 3.5], [3, -9, 2.6], [-2, 10, 2.2], [10, -4, 2]];
  for (const [dx, dy, r] of craters) {
    octx.beginPath(); octx.arc(MX + dx, MY + dy, r, 0, Math.PI * 2); octx.fill();
  }
}

// ---------- procedural mountain ridges ----------
function ridgePoints(baseY, minH, maxH, seg, seed) {
  const r = mulberry32(seed);
  const pts = [];
  const n = Math.ceil(W / seg) + 2;
  for (let i = -1; i <= n; i++) {
    pts.push([i * seg, baseY - minH - r() * (maxH - minH)]);
  }
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [x1, y1] = pts[i], [x2, y2] = pts[i + 1];
    out.push([x1, y1]);
    out.push([(x1 + x2) / 2, (y1 + y2) / 2 + (r() - 0.5) * seg * 0.9]);
  }
  out.push(pts[pts.length - 1]);
  return out;
}
function drawRange(c, baseY, minH, maxH, seg, color, seed) {
  const pts = ridgePoints(baseY, minH, maxH, seg, seed);
  c.fillStyle = color;
  c.beginPath();
  c.moveTo(-seg, baseY + 2);
  for (const [x, y] of pts) c.lineTo(x, y);
  c.lineTo(W + seg, baseY + 2);
  c.closePath();
  c.fill();
  return pts;
}
function snowCaps(c, pts, baseY) {
  c.fillStyle = 'rgba(205,220,245,0.35)';
  for (let i = 1; i < pts.length - 1; i++) {
    const [x, y] = pts[i];
    const h = baseY - y;
    if (y < pts[i - 1][1] && y <= pts[i + 1][1] && h > 60) {
      const s = Math.min(14, h * 0.18);
      c.beginPath();
      c.moveTo(x, y);
      c.lineTo(x - s, y + s * 1.2);
      c.lineTo(x - s * 0.3, y + s * 0.9);
      c.lineTo(x + s * 0.25, y + s * 1.25);
      c.lineTo(x + s, y + s * 1.1);
      c.closePath();
      c.fill();
    }
  }
}
const farPts = drawRange(octx, HORIZON, 70, 170, 64, '#16294a', 7);
snowCaps(octx, farPts, HORIZON);
drawRange(octx, HORIZON, 30, 92, 48, '#0b1830', 23);

// ---------- little pine trees (used on shore + foreground) ----------
function pine(c, x, y, h, color) {
  c.fillStyle = color;
  c.fillRect(x - h * 0.04, y - h * 0.12, h * 0.08, h * 0.12);
  for (let i = 0; i < 3; i++) {
    const ty = y - h * 0.1 - h * 0.28 * i;
    const tw = h * 0.5 * (1 - i * 0.26);
    const th = h * 0.34;
    c.beginPath();
    c.moveTo(x, ty - th);
    c.lineTo(x - tw / 2, ty);
    c.lineTo(x + tw / 2, ty);
    c.closePath();
    c.fill();
  }
}
// far-shore treeline (will reflect in the water automatically)
{
  const tr = mulberry32(99);
  for (let x = -5; x < W + 5; x += 6 + tr() * 10) {
    pine(octx, x, HORIZON + 2, 12 + tr() * 20, '#081222');
  }
}

// ================= compose the main canvas =================
ctx.drawImage(off, 0, 0);

// lake base
const lake = ctx.createLinearGradient(0, HORIZON, 0, H);
lake.addColorStop(0, '#16304f');
lake.addColorStop(0.3, '#0e2138');
lake.addColorStop(1, '#050b18');
ctx.fillStyle = lake;
ctx.fillRect(0, HORIZON, W, H - HORIZON);

// reflection: draw the sky canvas back in flipped horizontal slices, wobbled
ctx.save();
ctx.globalAlpha = 0.5;
for (let y = 0; y < H - HORIZON; y += 2) {
  const srcY = HORIZON - y - 2;
  const dx = Math.sin(y * 0.18) * (y / (H - HORIZON)) * 5;
  ctx.drawImage(off, 0, srcY, W, 2, dx, HORIZON + y, W, 2);
}
ctx.restore();

// water tint, deeper with depth
const tint = ctx.createLinearGradient(0, HORIZON, 0, H);
tint.addColorStop(0, 'rgba(20,45,80,0.12)');
tint.addColorStop(1, 'rgba(4,10,24,0.55)');
ctx.fillStyle = tint;
ctx.fillRect(0, HORIZON, W, H - HORIZON);

// soft aurora glow bleeding into the water near shore
{
  const ag = ctx.createLinearGradient(0, HORIZON, 0, HORIZON + 90);
  ag.addColorStop(0, 'rgba(90,240,170,0.08)');
  ag.addColorStop(1, 'rgba(90,240,170,0)');
  ctx.fillStyle = ag;
  ctx.fillRect(50, HORIZON, 260, 90);
}

// shoreline highlight
ctx.fillStyle = 'rgba(140,185,230,0.15)';
ctx.fillRect(0, HORIZON - 1, W, 1.5);

// squashed moon-glow on the water
{
  ctx.save();
  ctx.translate(MX, HORIZON + 8);
  ctx.scale(1, 0.35);
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 46);
  g.addColorStop(0, 'rgba(210,230,255,0.20)');
  g.addColorStop(1, 'rgba(210,230,255,0)');
  ctx.fillStyle = g;
  ctx.beginPath(); ctx.arc(0, 0, 46, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}

// moonlight glitter path
{
  const gr = mulberry32(777);
  for (let i = 0; i < 90; i++) {
    const y = HORIZON + 6 + gr() * (H - HORIZON - 12);
    const spread = 6 + (y - HORIZON) * 0.35;
    const x = MX + (gr() - 0.5) * spread * 2;
    const len = 3 + gr() * 14 * ((y - HORIZON) / 150 + 0.3);
    const a = 0.05 + gr() * 0.22 * (1 - (y - HORIZON) / 200);
    ctx.strokeStyle = 'rgba(215,232,255,' + a.toFixed(3) + ')';
    ctx.lineWidth = 1 + gr() * 1.2;
    ctx.beginPath();
    ctx.moveTo(x - len / 2, y);
    ctx.lineTo(x + len / 2, y);
    ctx.stroke();
  }
}

// faint ripples
for (let i = 0; i < 26; i++) {
  const y = HORIZON + 4 + rand() * (H - HORIZON - 8);
  const x0 = rand() * W * 0.7;
  const len = 30 + rand() * 120;
  const a = 0.03 + rand() * 0.07;
  ctx.strokeStyle = 'rgba(160,195,235,' + a.toFixed(3) + ')';
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x0 + len, y); ctx.stroke();
}

// low mist bands over the water
for (const [mx, mw, my] of [[40, 280, 372], [150, 260, 396]]) {
  const g = ctx.createLinearGradient(mx, 0, mx + mw, 0);
  g.addColorStop(0, 'rgba(180,200,230,0)');
  g.addColorStop(0.5, 'rgba(180,200,230,0.10)');
  g.addColorStop(1, 'rgba(180,200,230,0)');
  ctx.fillStyle = g;
  ctx.fillRect(mx, my, mw, 7);
}

// ---------- foreground: dark hills + pine silhouettes ----------
ctx.fillStyle = '#030711';
// left hill
ctx.beginPath();
ctx.moveTo(0, H);
ctx.lineTo(0, 430);
ctx.quadraticCurveTo(90, 405, 170, 452);
ctx.quadraticCurveTo(210, 475, 240, H);
ctx.closePath();
ctx.fill();
// right hill
ctx.beginPath();
ctx.moveTo(W, H);
ctx.lineTo(W, 445);
ctx.quadraticCurveTo(430, 420, 370, 460);
ctx.quadraticCurveTo(340, 480, 320, H);
ctx.closePath();
ctx.fill();

// foreground pines on the hills
pine(ctx, 30, 448, 55, '#02050d');
pine(ctx, 62, 456, 42, '#02050d');
pine(ctx, 100, 466, 60, '#02050d');
pine(ctx, 145, 480, 38, '#02050d');
pine(ctx, 462, 462, 50, '#02050d');
pine(ctx, 425, 474, 38, '#02050d');
pine(ctx, 392, 484, 30, '#02050d');

// ---------- vignette ----------
const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 0.75);
vg.addColorStop(0, 'rgba(0,0,0,0)');
vg.addColorStop(1, 'rgba(0,0,0,0.45)');
ctx.fillStyle = vg;
ctx.fillRect(0, 0, W, H);
```