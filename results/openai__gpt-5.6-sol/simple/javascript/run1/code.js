const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const W = canvas.width;
const H = canvas.height;

function roundedRect(x, y, w, h, r) {
  const radius = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + w - radius, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + radius);
  ctx.lineTo(x + w, y + h - radius);
  ctx.quadraticCurveTo(x + w, y + h, x + w - radius, y + h);
  ctx.lineTo(x + radius, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
}

function line(x1, y1, x2, y2) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
}

function dot(x, y, radius, color) {
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.fill();
}

function glowDot(x, y, radius, color) {
  ctx.save();
  ctx.shadowColor = color;
  ctx.shadowBlur = radius * 5;
  dot(x, y, radius, color);
  ctx.restore();
}

// Background
const background = ctx.createRadialGradient(250, 225, 20, 250, 250, 360);
background.addColorStop(0, "#15314a");
background.addColorStop(0.45, "#081927");
background.addColorStop(1, "#02070d");
ctx.fillStyle = background;
ctx.fillRect(0, 0, W, H);

// Fine grid
ctx.save();
ctx.strokeStyle = "rgba(83, 202, 220, 0.07)";
ctx.lineWidth = 1;

for (let x = 10; x < W; x += 20) line(x, 0, x, H);
for (let y = 10; y < H; y += 20) line(0, y, W, y);

ctx.strokeStyle = "rgba(90, 220, 235, 0.11)";
for (let x = 50; x < W; x += 100) line(x, 0, x, H);
for (let y = 50; y < H; y += 100) line(0, y, W, y);
ctx.restore();

// Deterministic background particles
let seed = 9173;
function random() {
  seed = (seed * 16807) % 2147483647;
  return (seed - 1) / 2147483646;
}

for (let i = 0; i < 80; i++) {
  const x = random() * W;
  const y = random() * H;
  const r = 0.3 + random() * 1.3;
  dot(x, y, r, `rgba(112,225,239,${0.12 + random() * 0.35})`);
}

// Circuit traces surrounding the portrait
ctx.save();
ctx.lineWidth = 1.4;
ctx.strokeStyle = "rgba(69, 211, 226, 0.30)";
ctx.fillStyle = "#52dbe9";

const circuits = [
  [[23, 102], [74, 102], [74, 134], [109, 134]],
  [[10, 191], [61, 191], [61, 165], [105, 165]],
  [[25, 287], [76, 287], [76, 258], [107, 258]],
  [[31, 356], [65, 356], [65, 328], [115, 328]],
  [[477, 112], [426, 112], [426, 144], [392, 144]],
  [[490, 205], [443, 205], [443, 177], [395, 177]],
  [[476, 291], [431, 291], [431, 260], [394, 260]],
  [[467, 358], [430, 358], [430, 330], [385, 330]]
];

circuits.forEach(points => {
  ctx.beginPath();
  ctx.moveTo(points[0][0], points[0][1]);
  for (let i = 1; i < points.length; i++) {
    ctx.lineTo(points[i][0], points[i][1]);
  }
  ctx.stroke();

  dot(points[0][0], points[0][1], 2.5, "#4cd5e4");
  dot(points.at(-1)[0], points.at(-1)[1], 2, "#4cd5e4");
});
ctx.restore();

// Halo
ctx.save();
ctx.translate(250, 220);
ctx.strokeStyle = "rgba(92, 229, 239, 0.17)";
ctx.lineWidth = 2;
ctx.setLineDash([7, 10]);
ctx.beginPath();
ctx.arc(0, 0, 181, 0, Math.PI * 2);
ctx.stroke();

ctx.rotate(-0.4);
ctx.strokeStyle = "rgba(128, 114, 255, 0.22)";
ctx.setLineDash([2, 15]);
ctx.lineWidth = 4;
ctx.beginPath();
ctx.arc(0, 0, 164, 0, Math.PI * 2);
ctx.stroke();

ctx.setLineDash([]);
ctx.strokeStyle = "rgba(73, 223, 232, 0.18)";
ctx.lineWidth = 1;
ctx.beginPath();
ctx.arc(0, 0, 151, 0, Math.PI * 2);
ctx.stroke();
ctx.restore();

// Shoulder glow
const shoulderGlow = ctx.createRadialGradient(250, 485, 10, 250, 460, 230);
shoulderGlow.addColorStop(0, "rgba(46,190,214,0.24)");
shoulderGlow.addColorStop(1, "rgba(0,0,0,0)");
ctx.fillStyle = shoulderGlow;
ctx.fillRect(0, 325, 500, 175);

// Shoulders and torso
const torso = ctx.createLinearGradient(0, 370, 0, 500);
torso.addColorStop(0, "#18364a");
torso.addColorStop(1, "#07131f");

ctx.beginPath();
ctx.moveTo(102, 500);
ctx.quadraticCurveTo(111, 424, 179, 397);
ctx.lineTo(212, 377);
ctx.lineTo(288, 377);
ctx.lineTo(321, 397);
ctx.quadraticCurveTo(389, 424, 398, 500);
ctx.closePath();
ctx.fillStyle = torso;
ctx.fill();

ctx.strokeStyle = "rgba(92,224,235,0.45)";
ctx.lineWidth = 2;
ctx.stroke();

// Shoulder armor seams
ctx.strokeStyle = "rgba(86,199,218,0.20)";
ctx.lineWidth = 1.5;
line(179, 399, 151, 500);
line(321, 399, 349, 500);
line(211, 424, 190, 500);
line(289, 424, 310, 500);

// Chest panel
ctx.save();
roundedRect(205, 430, 90, 48, 15);
ctx.fillStyle = "rgba(5,17,27,0.82)";
ctx.fill();
ctx.strokeStyle = "rgba(84,221,232,0.42)";
ctx.stroke();

ctx.strokeStyle = "#52ddea";
ctx.lineWidth = 2;
line(224, 454, 239, 454);
line(261, 454, 276, 454);
glowDot(250, 454, 4, "#65edf4");
ctx.restore();

// Neck
const neck = ctx.createLinearGradient(205, 350, 295, 420);
neck.addColorStop(0, "#16364a");
neck.addColorStop(0.5, "#0a1c2b");
neck.addColorStop(1, "#18374a");

ctx.beginPath();
ctx.moveTo(205, 338);
ctx.lineTo(295, 338);
ctx.lineTo(287, 407);
ctx.quadraticCurveTo(250, 433, 213, 407);
ctx.closePath();
ctx.fillStyle = neck;
ctx.fill();
ctx.strokeStyle = "rgba(88,218,230,0.4)";
ctx.stroke();

// Neck circuitry
ctx.strokeStyle = "rgba(85,217,229,0.32)";
ctx.lineWidth = 1.3;
line(225, 356, 225, 398);
line(275, 356, 275, 398);
line(225, 384, 242, 401);
line(275, 384, 258, 401);
glowDot(225, 382, 2, "#56dbe8");
glowDot(275, 382, 2, "#56dbe8");

// Ears / interface modules
["left", "right"].forEach(side => {
  const x = side === "left" ? 91 : 375;

  ctx.save();
  roundedRect(x, 190, 34, 100, 13);
  const earGradient = ctx.createLinearGradient(x, 190, x + 34, 290);
  earGradient.addColorStop(0, "#183c50");
  earGradient.addColorStop(1, "#071722");
  ctx.fillStyle = earGradient;
  ctx.fill();
  ctx.strokeStyle = "rgba(91,226,237,0.55)";
  ctx.lineWidth = 2;
  ctx.stroke();

  roundedRect(x + 9, 211, 16, 58, 7);
  ctx.fillStyle = "#06131e";
  ctx.fill();

  glowDot(x + 17, 227, 2.5, "#62e8ef");
  glowDot(x + 17, 253, 2.5, "#7d72ff");
  ctx.restore();
});

// Head silhouette
ctx.save();
ctx.shadowColor = "rgba(74,222,235,0.35)";
ctx.shadowBlur = 25;

ctx.beginPath();
ctx.moveTo(250, 60);
ctx.bezierCurveTo(167, 60, 119, 112, 117, 205);
ctx.bezierCurveTo(115, 291, 150, 349, 211, 382);
ctx.quadraticCurveTo(250, 403, 289, 382);
ctx.bezierCurveTo(350, 349, 385, 291, 383, 205);
ctx.bezierCurveTo(381, 112, 333, 60, 250, 60);
ctx.closePath();

const headGradient = ctx.createLinearGradient(135, 75, 365, 375);
headGradient.addColorStop(0, "#214b5e");
headGradient.addColorStop(0.32, "#112d3e");
headGradient.addColorStop(0.72, "#081a28");
headGradient.addColorStop(1, "#17384a");
ctx.fillStyle = headGradient;
ctx.fill();

ctx.shadowBlur = 0;
ctx.strokeStyle = "#57dbe7";
ctx.lineWidth = 2.2;
ctx.stroke();
ctx.restore();

// Side plates
ctx.fillStyle = "rgba(3,13,21,0.55)";
ctx.beginPath();
ctx.moveTo(128, 154);
ctx.lineTo(157, 125);
ctx.lineTo(151, 316);
ctx.lineTo(129, 284);
ctx.closePath();
ctx.fill();

ctx.beginPath();
ctx.moveTo(372, 154);
ctx.lineTo(343, 125);
ctx.lineTo(349, 316);
ctx.lineTo(371, 284);
ctx.closePath();
ctx.fill();

ctx.strokeStyle = "rgba(89,216,228,0.28)";
ctx.stroke();

// Inner face
ctx.beginPath();
ctx.moveTo(250, 83);
ctx.bezierCurveTo(183, 83, 153, 123, 152, 207);
ctx.bezierCurveTo(151, 287, 181, 340, 220, 365);
ctx.quadraticCurveTo(250, 384, 280, 365);
ctx.bezierCurveTo(319, 340, 349, 287, 348, 207);
ctx.bezierCurveTo(347, 123, 317, 83, 250, 83);
ctx.closePath();

const face = ctx.createRadialGradient(225, 175, 10, 250, 225, 190);
face.addColorStop(0, "#214b5c");
face.addColorStop(0.42, "#102c3b");
face.addColorStop(1, "#061621");
ctx.fillStyle = face;
ctx.fill();
ctx.strokeStyle = "rgba(110,232,239,0.32)";
ctx.lineWidth = 1.2;
ctx.stroke();

// Face contour panels
ctx.strokeStyle = "rgba(97,217,228,0.19)";
ctx.lineWidth = 1;
ctx.beginPath();
ctx.moveTo(171, 143);
ctx.quadraticCurveTo(203, 111, 231, 108);
ctx.lineTo(218, 177);
ctx.lineTo(171, 196);
ctx.stroke();

ctx.beginPath();
ctx.moveTo(329, 143);
ctx.quadraticCurveTo(297, 111, 269, 108);
ctx.lineTo(282, 177);
ctx.lineTo(329, 196);
ctx.stroke();

ctx.beginPath();
ctx.moveTo(166, 278);
ctx.lineTo(216, 291);
ctx.lineTo(229, 356);
ctx.stroke();

ctx.beginPath();
ctx.moveTo(334, 278);
ctx.lineTo(284, 291);
ctx.lineTo(271, 356);
ctx.stroke();

// Brows
ctx.strokeStyle = "rgba(111,235,241,0.66)";
ctx.lineWidth = 3;
ctx.lineCap = "round";
ctx.beginPath();
ctx.moveTo(174, 191);
ctx.quadraticCurveTo(202, 176, 226, 191);
ctx.stroke();

ctx.beginPath();
ctx.moveTo(274, 191);
ctx.quadraticCurveTo(298, 176, 326, 191);
ctx.stroke();

// Eye sockets
function drawEye(cx, cy, flip) {
  ctx.save();

  ctx.beginPath();
  ctx.moveTo(cx - 42, cy);
  ctx.quadraticCurveTo(cx, cy - 24, cx + 42, cy);
  ctx.quadraticCurveTo(cx, cy + 22, cx - 42, cy);
  ctx.closePath();

  const socket = ctx.createLinearGradient(cx, cy - 20, cx, cy + 20);
  socket.addColorStop(0, "#020a10");
  socket.addColorStop(1, "#0b2330");
  ctx.fillStyle = socket;
  ctx.fill();
  ctx.strokeStyle = "rgba(96,222,233,0.52)";
  ctx.lineWidth = 1.5;
  ctx.stroke();

  ctx.shadowColor = "#61edf3";
  ctx.shadowBlur = 18;
  ctx.beginPath();
  ctx.ellipse(cx, cy, 13, 8, 0, 0, Math.PI * 2);
  ctx.fillStyle = "#73f4f5";
  ctx.fill();

  ctx.shadowBlur = 5;
  dot(cx, cy, 4, "#e8ffff");
  dot(cx + (flip ? -2 : 2), cy - 2, 1.3, "#ffffff");

  ctx.restore();
}

drawEye(202, 218, false);
drawEye(298, 218, true);

// Nose bridge and central seam
ctx.strokeStyle = "rgba(94,221,231,0.38)";
ctx.lineWidth = 1.6;
ctx.beginPath();
ctx.moveTo(250, 174);
ctx.lineTo(239, 271);
ctx.lineTo(250, 281);
ctx.lineTo(261, 271);
ctx.stroke();

glowDot(250, 174, 2.2, "#66e9ef");

// Cheek data marks
ctx.strokeStyle = "rgba(92,218,228,0.29)";
ctx.lineWidth = 1.2;
for (let i = 0; i < 3; i++) {
  line(174, 258 + i * 8, 199 + i * 4, 258 + i * 8);
  line(326, 258 + i * 8, 301 - i * 4, 258 + i * 8);
}

// Mouth
ctx.save();
ctx.shadowColor = "#55dce8";
ctx.shadowBlur = 10;
ctx.strokeStyle = "#56dce8";
ctx.lineWidth = 2;
ctx.beginPath();
ctx.moveTo(207, 314);
ctx.quadraticCurveTo(250, 328, 293, 314);
ctx.stroke();
ctx.restore();

ctx.strokeStyle = "rgba(113,233,239,0.32)";
ctx.lineWidth = 1;
ctx.beginPath();
ctx.moveTo(219, 330);
ctx.quadraticCurveTo(250, 341, 281, 330);
ctx.stroke();

// Forehead language / thought constellation
const nodes = [
  [250, 113], [222, 132], [278, 132],
  [204, 157], [250, 151], [296, 157]
];

ctx.strokeStyle = "rgba(121,110,255,0.42)";
ctx.lineWidth = 1;
[
  [0,1], [0,2], [1,3], [1,4],
  [2,4], [2,5], [3,4], [4,5]
].forEach(([a, b]) => {
  line(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]);
});

nodes.forEach((n, i) => {
  glowDot(n[0], n[1], i === 0 ? 3.2 : 2.2, i % 2 ? "#61e8ef" : "#8579ff");
});

// Temple indicators
ctx.fillStyle = "rgba(97,229,237,0.7)";
ctx.font = "10px monospace";
ctx.textAlign = "center";
ctx.fillText("A", 143, 232);
ctx.fillText("I", 357, 232);

// Tiny status readouts
ctx.font = "9px monospace";
ctx.textAlign = "left";
ctx.fillStyle = "rgba(101,226,235,0.55)";
ctx.fillText("THOUGHT", 18, 80);
ctx.fillText("LANGUAGE", 18, 92);

ctx.textAlign = "right";
ctx.fillStyle = "rgba(139,126,255,0.58)";
ctx.fillText("ONLINE", 482, 80);
ctx.fillText("01:SELF", 482, 92);

// Corner brackets
ctx.strokeStyle = "rgba(80,216,228,0.4)";
ctx.lineWidth = 2;
line(18, 18, 57, 18);
line(18, 18, 18, 57);
line(482, 18, 443, 18);
line(482, 18, 482, 57);
line(18, 482, 57, 482);
line(18, 482, 18, 443);
line(482, 482, 443, 482);
line(482, 482, 482, 443);

// Final glass-like highlight
ctx.save();
ctx.globalCompositeOperation = "screen";
const highlight = ctx.createLinearGradient(130, 70, 330, 350);
highlight.addColorStop(0, "rgba(180,255,255,0.10)");
highlight.addColorStop(0.35, "rgba(180,255,255,0.025)");
highlight.addColorStop(1, "rgba(180,255,255,0)");
ctx.beginPath();
ctx.moveTo(174, 92);
ctx.quadraticCurveTo(229, 59, 275, 79);
ctx.lineTo(185, 351);
ctx.quadraticCurveTo(143, 307, 137, 220);
ctx.quadraticCurveTo(134, 135, 174, 92);
ctx.closePath();
ctx.fillStyle = highlight;
ctx.fill();
ctx.restore();