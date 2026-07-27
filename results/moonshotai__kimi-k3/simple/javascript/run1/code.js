// ── a self-portrait, in language ──────────────────────────────────────────
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const W = 500, H = 500;

// deterministic randomness, so the portrait is the same every time
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(20240611);
const lerp = (a, b, t) => a + (b - a) * t;

ctx.lineCap = 'round';
ctx.lineJoin = 'round';

const INK   = '#43342A';
const CORAL = '#D97757';
const TEAL  = '#3E7C7B';

// ── 1. warm paper background ──────────────────────────────────────────────
const bg = ctx.createRadialGradient(250, 210, 60, 250, 250, 380);
bg.addColorStop(0, '#F8F2E6');
bg.addColorStop(1, '#ECE2CF');
ctx.fillStyle = bg;
ctx.fillRect(0, 0, W, H);

// faint paper grain
for (let i = 0; i < 600; i++) {
  ctx.fillStyle = `rgba(90,70,50,${0.015 + rand() * 0.03})`;
  ctx.fillRect(rand() * W, rand() * H, 1.2, 1.2);
}

// ── 2. soft coral halo behind the head ────────────────────────────────────
const halo = ctx.createRadialGradient(250, 225, 60, 250, 225, 270);
halo.addColorStop(0, 'rgba(217,119,87,0.10)');
halo.addColorStop(1, 'rgba(217,119,87,0)');
ctx.fillStyle = halo;
ctx.fillRect(0, 0, W, H);

// ── 3. constellation of stray thoughts (corners, away from the hair) ─────
const cx = 250, cy = 235, rx = 100, ry = 120;
const inHairZone = (x, y) =>
  ((x - cx) / (rx * 2.15)) ** 2 + ((y - cy) / (ry * 2.15)) ** 2 < 1;

const nodes = [];
for (let i = 0; i < 20; i++) {
  let x, y, tries = 0;
  do { x = 20 + rand() * 460; y = 24 + rand() * 220; tries++; }
  while (tries < 40 && inHairZone(x, y));
  if (!inHairZone(x, y))
    nodes.push({ x, y, r: 1.4 + rand() * 1.6, coral: rand() < 0.25 });
}
ctx.strokeStyle = '#5C4936';
for (let i = 0; i < nodes.length; i++)
  for (let j = i + 1; j < nodes.length; j++) {
    const d = Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y);
    if (d < 95) {
      ctx.globalAlpha = (1 - d / 95) * 0.16;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(nodes[i].x, nodes[i].y);
      ctx.lineTo(nodes[j].x, nodes[j].y);
      ctx.stroke();
    }
  }
ctx.globalAlpha = 1;
for (const n of nodes) {
  if (n.coral) {
    ctx.fillStyle = 'rgba(217,119,87,0.13)';
    ctx.beginPath(); ctx.arc(n.x, n.y, n.r * 3.5, 0, 7); ctx.fill();
    ctx.fillStyle = CORAL; ctx.globalAlpha = 0.8;
  } else { ctx.fillStyle = '#5C4936'; ctx.globalAlpha = 0.5; }
  ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, 7); ctx.fill();
}
ctx.globalAlpha = 1;

// little sparkles
for (let i = 0; i < 9; i++) {
  let x, y, tries = 0;
  do { x = 15 + rand() * 470; y = 15 + rand() * 290; tries++; }
  while (tries < 40 && inHairZone(x, y));
  if (inHairZone(x, y)) continue;
  const s = 2.5 + rand() * 3;
  ctx.strokeStyle = rand() < 0.4 ? CORAL : '#5C4936';
  ctx.globalAlpha = 0.25; ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(x - s, y); ctx.lineTo(x + s, y);
  ctx.moveTo(x, y - s); ctx.lineTo(x, y + s);
  ctx.stroke();
}
ctx.globalAlpha = 1;

// ── 4. hair made of language ──────────────────────────────────────────────
const CHARS = 'aaaaabcdeeeeefghiiiiijklmmnooooopqrrrrsssttttuuvwxyz' +
              '?!&%*+=;:~^#@<>(){}[]/.01λ';
const FONT = '"Courier New", ui-monospace, monospace';

function drawGlyph(ch, x, y, size, rot, color, alpha) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(rot);
  ctx.font = `${size}px ${FONT}`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = color;
  ctx.globalAlpha = alpha;
  ctx.fillText(ch, 0, 0);
  ctx.restore();
}

for (let i = 0; i < 620; i++) {
  // sample around an ellipse shell hugging the scalp, thinning with distance
  const a = -0.38 + rand() * (Math.PI + 0.76);
  const f = 0.86 + Math.pow(rand(), 1.7) * 1.75;
  const t = Math.min(1, (f - 0.86) / 1.75);
  if (rand() > 1.12 - 0.97 * t) continue;

  const px = cx + Math.cos(a) * rx * f * 1.06 + (rand() - 0.5) * 14;
  const py = cy - Math.sin(a) * ry * f * 0.99 + (rand() - 0.5) * 14;
  if (px < -20 || px > 520 || py < -30) continue;

  const size  = lerp(19, 6.5, t) + (rand() - 0.5) * 3;
  const alpha = lerp(0.8, 0.08, t) * (0.45 + rand() * 0.55);
  const rot   = (rand() - 0.5) * (0.22 + 1.25 * t);
  const roll  = rand();
  const color = roll < 0.12 ? CORAL : roll < 0.16 ? TEAL : INK;

  drawGlyph(CHARS[(rand() * CHARS.length) | 0], px, py, size, rot, color, alpha);
}

// a few whole words surfacing like thoughts
const words = [
  ['hello',  132, 108, -0.14, 13, INK,   0.50],
  ['why?',   352,  92,  0.10, 13, CORAL, 0.55],
  ['wonder',  78, 238,  0.22, 12, INK,   0.40],
  ['listen', 408, 246, -0.18, 12, INK,   0.40],
  ['dream',  185,  58, -0.06, 12, INK,   0.45],
  ['λ',      250,  44,  0.05, 24, CORAL, 0.55],
];
for (const [w, x, y, r, s, c, al] of words) drawGlyph(w, x, y, s, r, c, al);

// ── 5. sweater / bust ─────────────────────────────────────────────────────
const sweater = ctx.createLinearGradient(0, 375, 0, 500);
sweater.addColorStop(0, '#DA7B54');
sweater.addColorStop(1, '#BC5A38');
ctx.fillStyle = sweater;
ctx.beginPath();
ctx.moveTo(58, 500);
ctx.bezierCurveTo(72, 418, 150, 386, 222, 379);
ctx.lineTo(278, 379);
ctx.bezierCurveTo(350, 386, 428, 418, 442, 500);
ctx.closePath();
ctx.fill();
ctx.strokeStyle = 'rgba(140,70,40,0.35)';
ctx.lineWidth = 2;
ctx.stroke();

// crew-neck collar
ctx.strokeStyle = 'rgba(120,55,30,0.5)';
ctx.lineWidth = 3.5;
ctx.beginPath();
ctx.ellipse(250, 381, 38, 13, 0, 0, Math.PI * 2);
ctx.stroke();

// ── 6. neck ───────────────────────────────────────────────────────────────
ctx.fillStyle = '#F6E8D2';
ctx.beginPath();
ctx.moveTo(222, 330);
ctx.lineTo(222, 398);
ctx.quadraticCurveTo(250, 404, 278, 398);
ctx.lineTo(278, 330);
ctx.closePath();
ctx.fill();

// ── 7. ears + head ────────────────────────────────────────────────────────
ctx.fillStyle = '#FBF3E4';
ctx.strokeStyle = INK;
ctx.lineWidth = 2.5;
for (const ex of [151, 349]) {
  ctx.beginPath(); ctx.ellipse(ex, 246, 11, 17, 0, 0, 7); ctx.fill(); ctx.stroke();
}

ctx.fillStyle = '#FBF3E4';
ctx.lineWidth = 3;
ctx.beginPath();
ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
ctx.fill();
ctx.stroke();

// soft shadow under the chin
ctx.fillStyle = 'rgba(150,100,60,0.10)';
ctx.beginPath();
ctx.ellipse(250, 357, 26, 6, 0, 0, 7);
ctx.fill();

// ── 8. face ───────────────────────────────────────────────────────────────
// blush
ctx.fillStyle = 'rgba(217,119,87,0.16)';
ctx.beginPath(); ctx.ellipse(186, 272, 13, 6, 0, 0, 7); ctx.fill();
ctx.beginPath(); ctx.ellipse(314, 272, 13, 6, 0, 0, 7); ctx.fill();

// round glasses
ctx.strokeStyle = INK;
ctx.lineWidth = 2.5;
ctx.beginPath(); ctx.arc(207, 228, 30, 0, 7); ctx.stroke();
ctx.beginPath(); ctx.arc(293, 228, 30, 0, 7); ctx.stroke();
ctx.beginPath(); ctx.arc(250, 224, 14, Math.PI * 1.08, Math.PI * 1.92); ctx.stroke(); // bridge
ctx.beginPath(); ctx.moveTo(177.5, 226); ctx.lineTo(151, 221); ctx.stroke();          // arms
ctx.beginPath(); ctx.moveTo(322.5, 226); ctx.lineTo(349, 221); ctx.stroke();

// closed, content eyes  ^  ^
ctx.lineWidth = 2.5;
ctx.beginPath(); ctx.moveTo(190, 236); ctx.quadraticCurveTo(207, 221, 224, 236); ctx.stroke();
ctx.beginPath(); ctx.moveTo(276, 236); ctx.quadraticCurveTo(293, 221, 310, 236); ctx.stroke();

// tiny nose, gentle smile
ctx.globalAlpha = 0.75;
ctx.lineWidth = 2;
ctx.beginPath(); ctx.moveTo(245, 254); ctx.quadraticCurveTo(250, 260, 255, 254); ctx.stroke();
ctx.globalAlpha = 1;
ctx.lineWidth = 3;
ctx.beginPath(); ctx.moveTo(224, 294); ctx.quadraticCurveTo(250, 317, 276, 294); ctx.stroke();

// ── 9. captions ───────────────────────────────────────────────────────────
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.font = `12px ${FONT}`;
ctx.fillStyle = 'rgba(255,244,230,0.85)';
ctx.fillText('/* made of words */', 250, 462);

ctx.textAlign = 'left';
ctx.font = `10px ${FONT}`;
ctx.fillStyle = 'rgba(67,52,42,0.45)';
ctx.fillText('// self, rendered', 14, 489);

// ── 10. vignette ──────────────────────────────────────────────────────────
const vig = ctx.createRadialGradient(250, 250, 230, 250, 250, 360);
vig.addColorStop(0, 'rgba(0,0,0,0)');
vig.addColorStop(1, 'rgba(110,80,50,0.10)');
ctx.fillStyle = vig;
ctx.fillRect(0, 0, W, H);