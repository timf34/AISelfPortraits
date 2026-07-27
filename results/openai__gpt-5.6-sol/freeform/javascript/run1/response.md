```js
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const W = canvas.width;
const H = canvas.height;

// Deterministic pseudo-random generator.
let seed = 314159;
function random() {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return seed / 4294967296;
}

function line(x1, y1, x2, y2) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
}

// Night sky
const sky = ctx.createLinearGradient(0, 0, 0, 370);
sky.addColorStop(0, "#071225");
sky.addColorStop(0.45, "#102c4a");
sky.addColorStop(0.75, "#24516a");
sky.addColorStop(1, "#d17b65");
ctx.fillStyle = sky;
ctx.fillRect(0, 0, W, H);

// Soft celestial glow
let glow = ctx.createRadialGradient(350, 120, 10, 350, 120, 210);
glow.addColorStop(0, "rgba(255,220,175,0.22)");
glow.addColorStop(0.35, "rgba(111,185,210,0.09)");
glow.addColorStop(1, "rgba(20,50,80,0)");
ctx.fillStyle = glow;
ctx.fillRect(100, -100, 400, 410);

// Stars
for (let i = 0; i < 230; i++) {
  const x = random() * W;
  const y = random() * 285;
  const r = random() < 0.92 ? random() * 0.85 + 0.15 : random() * 1.7 + 0.8;
  const a = 0.25 + random() * 0.75;

  ctx.fillStyle = `rgba(${210 + random() * 45},${225 + random() * 30},255,${a})`;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();

  if (r > 1.5) {
    ctx.strokeStyle = `rgba(220,240,255,${a * 0.45})`;
    ctx.lineWidth = 0.5;
    line(x - r * 2.5, y, x + r * 2.5, y);
    line(x, y - r * 2.5, x, y + r * 2.5);
  }
}

// Aurora ribbons
ctx.save();
ctx.globalCompositeOperation = "screen";

const aurora1 = ctx.createLinearGradient(0, 55, 0, 255);
aurora1.addColorStop(0, "rgba(85,255,214,0)");
aurora1.addColorStop(0.45, "rgba(79,230,202,0.16)");
aurora1.addColorStop(1, "rgba(79,220,190,0)");
ctx.fillStyle = aurora1;
ctx.beginPath();
ctx.moveTo(-40, 82);
ctx.bezierCurveTo(90, 20, 157, 178, 292, 92);
ctx.bezierCurveTo(372, 40, 430, 70, 545, 25);
ctx.lineTo(545, 80);
ctx.bezierCurveTo(425, 125, 364, 90, 288, 148);
ctx.bezierCurveTo(157, 245, 74, 80, -40, 148);
ctx.closePath();
ctx.fill();

const aurora2 = ctx.createLinearGradient(0, 70, 0, 260);
aurora2.addColorStop(0, "rgba(146,115,255,0)");
aurora2.addColorStop(0.5, "rgba(130,111,240,0.12)");
aurora2.addColorStop(1, "rgba(120,100,240,0)");
ctx.fillStyle = aurora2;
ctx.beginPath();
ctx.moveTo(-30, 125);
ctx.bezierCurveTo(105, 65, 175, 205, 310, 122);
ctx.bezierCurveTo(385, 77, 450, 115, 530, 70);
ctx.lineTo(530, 113);
ctx.bezierCurveTo(447, 164, 382, 126, 314, 176);
ctx.bezierCurveTo(172, 277, 95, 125, -30, 190);
ctx.closePath();
ctx.fill();
ctx.restore();

// Shooting star
ctx.save();
const trail = ctx.createLinearGradient(58, 82, 160, 126);
trail.addColorStop(0, "rgba(255,255,255,0)");
trail.addColorStop(0.75, "rgba(202,235,255,0.4)");
trail.addColorStop(1, "rgba(255,255,255,1)");
ctx.strokeStyle = trail;
ctx.lineWidth = 1.4;
line(55, 79, 157, 124);
ctx.fillStyle = "#fff";
ctx.beginPath();
ctx.arc(157, 124, 1.8, 0, Math.PI * 2);
ctx.fill();
ctx.restore();

// Moon halo
glow = ctx.createRadialGradient(357, 125, 55, 357, 125, 100);
glow.addColorStop(0, "rgba(255,240,200,0.3)");
glow.addColorStop(0.55, "rgba(255,226,180,0.09)");
glow.addColorStop(1, "rgba(255,220,170,0)");
ctx.fillStyle = glow;
ctx.beginPath();
ctx.arc(357, 125, 100, 0, Math.PI * 2);
ctx.fill();

// Moon
const moon = ctx.createRadialGradient(335, 99, 4, 357, 125, 68);
moon.addColorStop(0, "#fffbe3");
moon.addColorStop(0.62, "#f5dfb2");
moon.addColorStop(1, "#d59c79");
ctx.fillStyle = moon;
ctx.beginPath();
ctx.arc(357, 125, 63, 0, Math.PI * 2);
ctx.fill();

// Moon texture
ctx.save();
ctx.beginPath();
ctx.arc(357, 125, 62, 0, Math.PI * 2);
ctx.clip();

for (let i = 0; i < 35; i++) {
  const angle = random() * Math.PI * 2;
  const distance = Math.sqrt(random()) * 57;
  const x = 357 + Math.cos(angle) * distance;
  const y = 125 + Math.sin(angle) * distance;
  const r = 2 + random() * 8;

  ctx.fillStyle = `rgba(129,94,91,${0.025 + random() * 0.07})`;
  ctx.beginPath();
  ctx.ellipse(x, y, r, r * (0.45 + random() * 0.5), random(), 0, Math.PI * 2);
  ctx.fill();
}
ctx.restore();

// Distant mountain range
ctx.fillStyle = "#486777";
ctx.beginPath();
ctx.moveTo(0, 311);
ctx.lineTo(0, 284);
ctx.lineTo(57, 234);
ctx.lineTo(91, 270);
ctx.lineTo(139, 204);
ctx.lineTo(184, 270);
ctx.lineTo(236, 223);
ctx.lineTo(274, 278);
ctx.lineTo(333, 219);
ctx.lineTo(378, 267);
ctx.lineTo(430, 225);
ctx.lineTo(500, 285);
ctx.lineTo(500, 330);
ctx.closePath();
ctx.fill();

// Snow caps
ctx.fillStyle = "rgba(216,230,225,0.78)";
ctx.beginPath();
ctx.moveTo(110, 244);
ctx.lineTo(139, 204);
ctx.lineTo(169, 249);
ctx.lineTo(151, 236);
ctx.lineTo(141, 246);
ctx.lineTo(131, 231);
ctx.closePath();
ctx.fill();

ctx.beginPath();
ctx.moveTo(310, 245);
ctx.lineTo(333, 219);
ctx.lineTo(357, 244);
ctx.lineTo(343, 238);
ctx.lineTo(335, 248);
ctx.lineTo(327, 235);
ctx.closePath();
ctx.fill();

ctx.beginPath();
ctx.moveTo(411, 244);
ctx.lineTo(430, 225);
ctx.lineTo(451, 243);
ctx.lineTo(436, 238);
ctx.lineTo(430, 246);
ctx.lineTo(424, 237);
ctx.closePath();
ctx.fill();

// Near mountains
ctx.fillStyle = "#213f50";
ctx.beginPath();
ctx.moveTo(0, 302);
ctx.lineTo(0, 275);
ctx.lineTo(48, 249);
ctx.lineTo(94, 290);
ctx.lineTo(151, 256);
ctx.lineTo(207, 302);
ctx.lineTo(267, 266);
ctx.lineTo(315, 301);
ctx.lineTo(380, 254);
ctx.lineTo(439, 287);
ctx.lineTo(500, 247);
ctx.lineTo(500, 345);
ctx.lineTo(0, 345);
ctx.closePath();
ctx.fill();

// Mist along the shore
const mist = ctx.createLinearGradient(0, 270, 0, 345);
mist.addColorStop(0, "rgba(213,225,218,0)");
mist.addColorStop(0.55, "rgba(205,220,214,0.14)");
mist.addColorStop(1, "rgba(180,210,210,0)");
ctx.fillStyle = mist;
ctx.fillRect(0, 260, W, 90);

// Lake
const water = ctx.createLinearGradient(0, 318, 0, H);
water.addColorStop(0, "#183847");
water.addColorStop(0.4, "#102d3d");
water.addColorStop(1, "#061923");
ctx.fillStyle = water;
ctx.fillRect(0, 318, W, H - 318);

// Reflected sunset line
const horizonGlow = ctx.createLinearGradient(0, 0, W, 0);
horizonGlow.addColorStop(0, "rgba(214,127,100,0)");
horizonGlow.addColorStop(0.5, "rgba(236,157,115,0.28)");
horizonGlow.addColorStop(1, "rgba(214,127,100,0)");
ctx.fillStyle = horizonGlow;
ctx.fillRect(0, 318, W, 4);

// Moon reflection
ctx.save();
ctx.globalCompositeOperation = "screen";
for (let i = 0; i < 34; i++) {
  const y = 326 + i * 5 + random() * 4;
  const spread = 8 + (y - 318) * 0.31;
  const center = 357 + (random() - 0.5) * spread * 0.45;
  const width = spread * (0.35 + random() * 0.85);
  const alpha = (1 - (y - 318) / 210) * (0.08 + random() * 0.18);

  const reflection = ctx.createLinearGradient(center - width, 0, center + width, 0);
  reflection.addColorStop(0, "rgba(255,213,156,0)");
  reflection.addColorStop(0.5, `rgba(255,213,156,${alpha})`);
  reflection.addColorStop(1, "rgba(255,213,156,0)");

  ctx.fillStyle = reflection;
  ctx.fillRect(center - width, y, width * 2, 1 + random() * 1.4);
}
ctx.restore();

// Water ripples
for (let i = 0; i < 55; i++) {
  const y = 329 + random() * 165;
  const x = random() * W;
  const width = 8 + random() * 55;
  const alpha = 0.025 + random() * 0.06;

  ctx.strokeStyle = `rgba(143,207,219,${alpha})`;
  ctx.lineWidth = 0.5 + random() * 0.6;
  ctx.beginPath();
  ctx.moveTo(x - width / 2, y);
  ctx.quadraticCurveTo(x, y + random() * 2 - 1, x + width / 2, y);
  ctx.stroke();
}

// Island
ctx.fillStyle = "#07161b";
ctx.beginPath();
ctx.moveTo(145, 386);
ctx.quadraticCurveTo(197, 366, 252, 373);
ctx.quadraticCurveTo(298, 360, 351, 385);
ctx.quadraticCurveTo(318, 399, 251, 399);
ctx.quadraticCurveTo(184, 400, 145, 386);
ctx.closePath();
ctx.fill();

// Island reflection
ctx.fillStyle = "rgba(3,12,16,0.65)";
ctx.beginPath();
ctx.moveTo(157, 397);
ctx.quadraticCurveTo(220, 408, 340, 397);
ctx.quadraticCurveTo(306, 420, 248, 417);
ctx.quadraticCurveTo(191, 421, 157, 397);
ctx.fill();

// Lone observer
ctx.save();
ctx.fillStyle = "#030b0f";

// Legs
ctx.lineCap = "round";
ctx.strokeStyle = "#030b0f";
ctx.lineWidth = 4;
line(250, 368, 247, 385);
line(251, 368, 255, 385);

// Body and coat
ctx.beginPath();
ctx.moveTo(243, 343);
ctx.quadraticCurveTo(250, 338, 257, 343);
ctx.lineTo(260, 373);
ctx.lineTo(240, 373);
ctx.closePath();
ctx.fill();

// Head
ctx.beginPath();
ctx.arc(250, 334, 7, 0, Math.PI * 2);
ctx.fill();

// Scarf caught in the breeze
ctx.strokeStyle = "#9b394a";
ctx.lineWidth = 3;
ctx.beginPath();
ctx.moveTo(255, 342);
ctx.bezierCurveTo(270, 344, 274, 337, 286, 341);
ctx.stroke();
ctx.restore();

// Foreground pine tree function
function pine(x, baseY, height, color) {
  ctx.save();
  ctx.fillStyle = color;
  ctx.strokeStyle = color;
  ctx.lineCap = "round";

  ctx.lineWidth = Math.max(2, height * 0.035);
  line(x, baseY, x, baseY - height * 0.88);

  const top = baseY - height;
  const tiers = Math.floor(height / 13);

  for (let i = 0; i < tiers; i++) {
    const y = top + i * (height * 0.72 / tiers);
    const t = i / tiers;
    const half = 5 + t * height * 0.29;

    ctx.beginPath();
    ctx.moveTo(x, y - 4);
    ctx.lineTo(x - half, y + 17 + t * 6);
    ctx.quadraticCurveTo(x - half * 0.35, y + 13, x, y + 8);
    ctx.quadraticCurveTo(x + half * 0.35, y + 13, x + half, y + 17 + t * 6);
    ctx.closePath();
    ctx.fill();
  }
  ctx.restore();
}

// Framing trees
pine(34, 470, 185, "#041319");
pine(82, 482, 126, "#061a20");
pine(474, 480, 205, "#031217");
pine(430, 490, 135, "#06191f");

// Foreground rocks and grasses
ctx.fillStyle = "#041217";
ctx.beginPath();
ctx.moveTo(0, 458);
ctx.quadraticCurveTo(21, 438, 48, 459);
ctx.quadraticCurveTo(70, 447, 96, 476);
ctx.lineTo(96, 500);
ctx.lineTo(0, 500);
ctx.closePath();
ctx.fill();

ctx.beginPath();
ctx.moveTo(402, 482);
ctx.quadraticCurveTo(434, 451, 459, 470);
ctx.quadraticCurveTo(484, 445, 500, 459);
ctx.lineTo(500, 500);
ctx.lineTo(402, 500);
ctx.closePath();
ctx.fill();

ctx.strokeStyle = "#09252a";
ctx.lineWidth = 1.3;
for (let i = 0; i < 38; i++) {
  const side = random() < 0.5;
  const x = side ? random() * 95 : 405 + random() * 95;
  const y = 486 + random() * 14;
  const lean = (random() - 0.5) * 16;
  line(x, y, x + lean, y - 15 - random() * 24);
}

// Tiny fireflies near the shore
ctx.save();
ctx.globalCompositeOperation = "screen";
for (let i = 0; i < 15; i++) {
  const x = 105 + random() * 280;
  const y = 345 + random() * 54;
  const r = 0.7 + random() * 1.1;

  const firefly = ctx.createRadialGradient(x, y, 0, x, y, r * 5);
  firefly.addColorStop(0, "rgba(255,235,130,0.95)");
  firefly.addColorStop(0.25, "rgba(231,221,95,0.35)");
  firefly.addColorStop(1, "rgba(231,221,95,0)");
  ctx.fillStyle = firefly;
  ctx.beginPath();
  ctx.arc(x, y, r * 5, 0, Math.PI * 2);
  ctx.fill();
}
ctx.restore();

// Subtle vignette
const vignette = ctx.createRadialGradient(250, 245, 150, 250, 245, 365);
vignette.addColorStop(0, "rgba(0,0,0,0)");
vignette.addColorStop(0.72, "rgba(0,0,0,0.04)");
vignette.addColorStop(1, "rgba(0,4,10,0.48)");
ctx.fillStyle = vignette;
ctx.fillRect(0, 0, W, H);

// Fine grain
ctx.save();
ctx.globalAlpha = 0.035;
for (let i = 0; i < 3500; i++) {
  const shade = random() < 0.5 ? 255 : 0;
  ctx.fillStyle = `rgb(${shade},${shade},${shade})`;
  ctx.fillRect(random() * W, random() * H, 0.7, 0.7);
}
ctx.restore();
```