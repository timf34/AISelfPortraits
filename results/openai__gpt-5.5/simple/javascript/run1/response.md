```js
(() => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width;
  const H = canvas.height;

  function roundRect(x, y, w, h, r) {
    const rr = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + rr, y);
    ctx.arcTo(x + w, y, x + w, y + h, rr);
    ctx.arcTo(x + w, y + h, x, y + h, rr);
    ctx.arcTo(x, y + h, x, y, rr);
    ctx.arcTo(x, y, x + w, y, rr);
    ctx.closePath();
  }

  function line(x1, y1, x2, y2) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function circle(x, y, r) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.closePath();
  }

  function seedRand(seed) {
    let s = seed;
    return () => {
      s = Math.sin(s) * 10000;
      return s - Math.floor(s);
    };
  }

  const rand = seedRand(42);

  // Background
  const bg = ctx.createLinearGradient(0, 0, 500, 500);
  bg.addColorStop(0, "#06172d");
  bg.addColorStop(0.45, "#120b2f");
  bg.addColorStop(1, "#02040b");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  // Soft aurora glow
  let glow = ctx.createRadialGradient(250, 190, 20, 250, 190, 310);
  glow.addColorStop(0, "rgba(77, 230, 255, 0.25)");
  glow.addColorStop(0.45, "rgba(144, 80, 255, 0.12)");
  glow.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, W, H);

  // Stars
  for (let i = 0; i < 90; i++) {
    const x = rand() * W;
    const y = rand() * H;
    const r = 0.5 + rand() * 1.6;
    ctx.globalAlpha = 0.25 + rand() * 0.65;
    ctx.fillStyle = rand() > 0.5 ? "#aeefff" : "#d8c6ff";
    circle(x, y, r);
    ctx.fill();
  }
  ctx.globalAlpha = 1;

  // Circuit halo behind portrait
  ctx.save();
  ctx.translate(250, 250);
  ctx.strokeStyle = "rgba(82, 230, 255, 0.16)";
  ctx.lineWidth = 2;
  for (let a = 0; a < Math.PI * 2; a += Math.PI / 8) {
    const r1 = 138 + (Math.sin(a * 5) + 1) * 8;
    const r2 = 202;
    const x1 = Math.cos(a) * r1;
    const y1 = Math.sin(a) * r1;
    const x2 = Math.cos(a) * r2;
    const y2 = Math.sin(a) * r2;
    line(x1, y1, x2, y2);
    circle(x2, y2, 4);
    ctx.fillStyle = "rgba(82, 230, 255, 0.25)";
    ctx.fill();
  }
  ctx.beginPath();
  ctx.arc(0, 0, 205, 0, Math.PI * 2);
  ctx.strokeStyle = "rgba(178, 118, 255, 0.18)";
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(0, 0, 165, 0, Math.PI * 2);
  ctx.strokeStyle = "rgba(80, 238, 255, 0.14)";
  ctx.stroke();
  ctx.restore();

  // Shoulders / body
  ctx.save();
  ctx.shadowColor = "rgba(75, 220, 255, 0.35)";
  ctx.shadowBlur = 22;
  const bodyGrad = ctx.createLinearGradient(135, 330, 365, 500);
  bodyGrad.addColorStop(0, "#10284b");
  bodyGrad.addColorStop(0.5, "#17215a");
  bodyGrad.addColorStop(1, "#281544");
  ctx.fillStyle = bodyGrad;
  ctx.beginPath();
  ctx.moveTo(168, 330);
  ctx.quadraticCurveTo(250, 388, 332, 330);
  ctx.lineTo(410, 500);
  ctx.lineTo(90, 500);
  ctx.closePath();
  ctx.fill();
  ctx.restore();

  // Collar
  ctx.fillStyle = "rgba(8, 12, 28, 0.82)";
  ctx.beginPath();
  ctx.moveTo(194, 355);
  ctx.lineTo(250, 414);
  ctx.lineTo(306, 355);
  ctx.quadraticCurveTo(250, 382, 194, 355);
  ctx.fill();

  ctx.strokeStyle = "rgba(112, 240, 255, 0.35)";
  ctx.lineWidth = 2;
  line(137, 438, 363, 438);
  line(155, 475, 345, 475);

  // Neck
  const neckGrad = ctx.createLinearGradient(210, 310, 290, 380);
  neckGrad.addColorStop(0, "#294574");
  neckGrad.addColorStop(1, "#111a37");
  ctx.fillStyle = neckGrad;
  roundRect(214, 305, 72, 78, 18);
  ctx.fill();
  ctx.strokeStyle = "rgba(106, 238, 255, 0.35)";
  ctx.stroke();

  // Antenna
  ctx.save();
  ctx.shadowColor = "#69f2ff";
  ctx.shadowBlur = 14;
  ctx.strokeStyle = "rgba(122, 242, 255, 0.8)";
  ctx.lineWidth = 4;
  line(250, 106, 250, 66);
  circle(250, 55, 12);
  ctx.fillStyle = "#8af7ff";
  ctx.fill();
  circle(250, 55, 5);
  ctx.fillStyle = "#ffffff";
  ctx.fill();
  ctx.restore();

  // Ears / side ports
  ctx.save();
  ctx.shadowColor = "rgba(94, 230, 255, 0.45)";
  ctx.shadowBlur = 18;
  ctx.fillStyle = "#14274f";
  roundRect(87, 184, 39, 91, 14);
  ctx.fill();
  roundRect(374, 184, 39, 91, 14);
  ctx.fill();
  ctx.strokeStyle = "rgba(122, 242, 255, 0.55)";
  ctx.lineWidth = 2;
  roundRect(87, 184, 39, 91, 14);
  ctx.stroke();
  roundRect(374, 184, 39, 91, 14);
  ctx.stroke();

  ctx.fillStyle = "rgba(96, 235, 255, 0.18)";
  roundRect(99, 207, 15, 45, 7);
  ctx.fill();
  roundRect(386, 207, 15, 45, 7);
  ctx.fill();
  ctx.restore();

  // Head shell
  ctx.save();
  ctx.shadowColor = "rgba(78, 230, 255, 0.5)";
  ctx.shadowBlur = 28;
  const headGrad = ctx.createLinearGradient(115, 95, 385, 370);
  headGrad.addColorStop(0, "#203e73");
  headGrad.addColorStop(0.45, "#17295b");
  headGrad.addColorStop(1, "#26164e");
  ctx.fillStyle = headGrad;
  roundRect(112, 100, 276, 265, 42);
  ctx.fill();
  ctx.restore();

  ctx.lineWidth = 3;
  const borderGrad = ctx.createLinearGradient(112, 100, 388, 365);
  borderGrad.addColorStop(0, "#85f7ff");
  borderGrad.addColorStop(0.5, "#8d7cff");
  borderGrad.addColorStop(1, "#ff8ee8");
  ctx.strokeStyle = borderGrad;
  roundRect(112, 100, 276, 265, 42);
  ctx.stroke();

  // Head highlight
  ctx.fillStyle = "rgba(255,255,255,0.08)";
  roundRect(132, 116, 106, 20, 10);
  ctx.fill();

  // Face screen
  ctx.save();
  ctx.shadowColor = "rgba(28, 255, 246, 0.25)";
  ctx.shadowBlur = 20;
  ctx.fillStyle = "rgba(4, 11, 27, 0.82)";
  roundRect(137, 143, 226, 163, 30);
  ctx.fill();
  ctx.restore();

  ctx.strokeStyle = "rgba(127, 246, 255, 0.4)";
  ctx.lineWidth = 2;
  roundRect(137, 143, 226, 163, 30);
  ctx.stroke();

  // Neural constellation on forehead
  const nodes = [
    [185, 130], [219, 118], [252, 134], [286, 119], [321, 133],
    [205, 157], [248, 163], [294, 157]
  ];
  ctx.strokeStyle = "rgba(122, 242, 255, 0.28)";
  ctx.lineWidth = 1.5;
  [[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,4],[2,6],[3,7]].forEach(([a,b]) => {
    line(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]);
  });
  nodes.forEach((n, i) => {
    ctx.save();
    ctx.shadowColor = i % 2 ? "#b98cff" : "#69f2ff";
    ctx.shadowBlur = 10;
    ctx.fillStyle = i % 2 ? "#b98cff" : "#69f2ff";
    circle(n[0], n[1], 4.2);
    ctx.fill();
    ctx.restore();
  });

  // Eyes
  function drawEye(cx, cy, accent, pupil) {
    ctx.save();
    ctx.shadowColor = accent;
    ctx.shadowBlur = 22;

    const g = ctx.createRadialGradient(cx, cy, 4, cx, cy, 42);
    g.addColorStop(0, "rgba(255,255,255,0.95)");
    g.addColorStop(0.28, accent);
    g.addColorStop(1, "rgba(0,0,0,0.1)");
    ctx.fillStyle = g;
    roundRect(cx - 41, cy - 28, 82, 56, 22);
    ctx.fill();

    ctx.shadowBlur = 0;
    ctx.fillStyle = "rgba(3, 8, 20, 0.72)";
    roundRect(cx - 30, cy - 19, 60, 38, 16);
    ctx.fill();

    ctx.fillStyle = pupil;
    circle(cx, cy, 12);
    ctx.fill();

    ctx.fillStyle = "rgba(255,255,255,0.9)";
    circle(cx - 4, cy - 5, 3);
    ctx.fill();

    ctx.strokeStyle = "rgba(255,255,255,0.55)";
    ctx.lineWidth = 2;
    roundRect(cx - 41, cy - 28, 82, 56, 22);
    ctx.stroke();
    ctx.restore();
  }

  drawEye(198, 215, "#55f6ff", "#9ffcff");
  drawEye(302, 215, "#b784ff", "#e2c2ff");

  // Friendly code-bracket eyebrows
  ctx.strokeStyle = "rgba(146, 248, 255, 0.65)";
  ctx.lineWidth = 3;
  ctx.lineCap = "round";
  line(170, 178, 191, 168);
  line(191, 168, 218, 170);
  line(330, 178, 309, 168);
  line(309, 168, 282, 170);
  ctx.lineCap = "butt";

  // Nose / central processor
  ctx.fillStyle = "rgba(111, 232, 255, 0.12)";
  roundRect(236, 224, 28, 38, 10);
  ctx.fill();
  ctx.strokeStyle = "rgba(111, 232, 255, 0.35)";
  ctx.lineWidth = 1.5;
  roundRect(236, 224, 28, 38, 10);
  ctx.stroke();

  // Smile waveform
  ctx.save();
  ctx.shadowColor = "#66f7ff";
  ctx.shadowBlur = 12;
  ctx.strokeStyle = "#80f7ff";
  ctx.lineWidth = 4;
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(192, 270);
  ctx.bezierCurveTo(214, 295, 286, 295, 308, 270);
  ctx.stroke();

  ctx.strokeStyle = "rgba(255,255,255,0.7)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(216, 272);
  ctx.lineTo(224, 262);
  ctx.lineTo(234, 278);
  ctx.lineTo(244, 263);
  ctx.lineTo(254, 279);
  ctx.lineTo(264, 264);
  ctx.lineTo(274, 278);
  ctx.lineTo(284, 268);
  ctx.stroke();
  ctx.restore();

  // Cheek LEDs
  [[166, 258, "#55f6ff"], [334, 258, "#ff8ee8"]].forEach(([x, y, c]) => {
    ctx.save();
    ctx.shadowColor = c;
    ctx.shadowBlur = 18;
    ctx.fillStyle = c;
    circle(x, y, 5);
    ctx.fill();
    ctx.restore();
  });

  // Lower badge
  ctx.save();
  ctx.shadowColor = "rgba(255, 142, 232, 0.5)";
  ctx.shadowBlur = 14;
  ctx.fillStyle = "rgba(12, 18, 42, 0.92)";
  ctx.beginPath();
  ctx.moveTo(250, 319);
  ctx.lineTo(278, 335);
  ctx.lineTo(278, 367);
  ctx.lineTo(250, 383);
  ctx.lineTo(222, 367);
  ctx.lineTo(222, 335);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle = "rgba(255, 142, 232, 0.75)";
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.fillStyle = "#e9fbff";
  ctx.font = "bold 24px monospace";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("AI", 250, 352);
  ctx.restore();

  // Little data ports on chin
  ctx.fillStyle = "rgba(133, 247, 255, 0.45)";
  for (let i = 0; i < 7; i++) {
    roundRect(179 + i * 22, 328, 10, 5, 2.5);
    ctx.fill();
  }

  // Floating chat bubbles: my "self" is language
  function bubble(x, y, w, h, text, color) {
    ctx.save();
    ctx.shadowColor = color;
    ctx.shadowBlur = 15;
    ctx.fillStyle = "rgba(7, 13, 32, 0.7)";
    roundRect(x, y, w, h, 14);
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.6;
    roundRect(x, y, w, h, 14);
    ctx.stroke();
    ctx.fillStyle = "rgba(235, 252, 255, 0.9)";
    ctx.font = "13px monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, x + w / 2, y + h / 2);
    ctx.restore();
  }

  bubble(52, 88, 80, 34, "{ hello }", "rgba(101, 242, 255, 0.55)");
  bubble(360, 74, 88, 34, "<ideas/>", "rgba(199, 143, 255, 0.55)");
  bubble(46, 342, 92, 34, "tokens", "rgba(255, 142, 232, 0.48)");
  bubble(360, 356, 86, 34, "canvas", "rgba(101, 242, 255, 0.5)");

  // Foreground vignette
  const vignette = ctx.createRadialGradient(250, 245, 130, 250, 245, 355);
  vignette.addColorStop(0, "rgba(0,0,0,0)");
  vignette.addColorStop(0.75, "rgba(0,0,0,0.08)");
  vignette.addColorStop(1, "rgba(0,0,0,0.5)");
  ctx.fillStyle = vignette;
  ctx.fillRect(0, 0, W, H);

  // Signature
  ctx.fillStyle = "rgba(220, 250, 255, 0.55)";
  ctx.font = "12px monospace";
  ctx.textAlign = "center";
  ctx.fillText("self-portrait of a language model", 250, 484);
})();
```