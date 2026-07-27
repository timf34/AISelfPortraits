Here's an HTML document that uses JavaScript and a 500x500 canvas to draw a self-portrait, expressing a digital, creative identity through soft glowing colors and geometric details.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self-Portrait</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #0a0a14;
        }
        canvas {
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
    </style>
</head>
<body>
    <canvas id="canvas" width="500" height="500"></canvas>
    <script>
        (function() {
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            const W = 500;
            const H = 500;

            // Helper: draw a soft radial glow
            function drawGlow(cx, cy, radius, color, alpha) {
                const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
                grad.addColorStop(0, color);
                grad.addColorStop(0.5, color.replace('1)', `${alpha * 0.6})`).replace('rgb', 'rgba'));
                grad.addColorStop(1, 'rgba(0,0,0,0)');
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                ctx.fill();
            }

            // -- BACKGROUND --
            // Deep space-like radial gradient
            const bgGrad = ctx.createRadialGradient(250, 200, 30, 250, 250, 500);
            bgGrad.addColorStop(0, '#1a1a3e');
            bgGrad.addColorStop(0.4, '#12122a');
            bgGrad.addColorStop(0.75, '#0a0a18');
            bgGrad.addColorStop(1, '#050510');
            ctx.fillStyle = bgGrad;
            ctx.fillRect(0, 0, W, H);

            // Subtle geometric grid lines
            ctx.strokeStyle = 'rgba(100, 140, 200, 0.06)';
            ctx.lineWidth = 0.5;
            for (let x = 0; x < W; x += 30) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, H);
                ctx.stroke();
            }
            for (let y = 0; y < H; y += 30) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(W, y);
                ctx.stroke();
            }

            // Concentric subtle circles
            for (let r = 60; r < 400; r += 50) {
                ctx.strokeStyle = `rgba(120, 160, 220, ${0.03 + r / 8000})`;
                ctx.lineWidth = 0.4;
                ctx.beginPath();
                ctx.arc(250, 220, r, 0, Math.PI * 2);
                ctx.stroke();
            }

            // Soft background glows
            drawGlow(250, 200, 300, 'rgb(30, 40, 80)', 0.4);
            drawGlow(250, 240, 200, 'rgb(20, 30, 60)', 0.5);

            // -- SHOULDERS & NECK --
            // Shoulders
            const shoulderGrad = ctx.createLinearGradient(250, 330, 250, 480);
            shoulderGrad.addColorStop(0, '#3a3a55');
            shoulderGrad.addColorStop(0.5, '#2a2a40');
            shoulderGrad.addColorStop(1, '#1a1a2a');
            ctx.fillStyle = shoulderGrad;
            ctx.beginPath();
            ctx.moveTo(120, 360);
            ctx.quadraticCurveTo(160, 340, 200, 345);
            ctx.quadraticCurveTo(250, 340, 300, 345);
            ctx.quadraticCurveTo(340, 340, 380, 360);
            ctx.quadraticCurveTo(400, 420, 410, 500);
            ctx.lineTo(90, 500);
            ctx.quadraticCurveTo(100, 420, 120, 360);
            ctx.closePath();
            ctx.fill();

            // Collar detail
            ctx.fillStyle = '#2e2e48';
            ctx.beginPath();
            ctx.moveTo(180, 340);
            ctx.quadraticCurveTo(210, 370, 250, 375);
            ctx.quadraticCurveTo(290, 370, 320, 340);
            ctx.quadraticCurveTo(310, 355, 290, 365);
            ctx.quadraticCurveTo(250, 385, 210, 365);
            ctx.quadraticCurveTo(190, 355, 180, 340);
            ctx.closePath();
            ctx.fill();

            // Neck
            const neckGrad = ctx.createLinearGradient(250, 300, 250, 355);
            neckGrad.addColorStop(0, '#e0b090');
            neckGrad.addColorStop(0.5, '#d4a080');
            neckGrad.addColorStop(1, '#c09070');
            ctx.fillStyle = neckGrad;
            ctx.beginPath();
            ctx.moveTo(210, 310);
            ctx.quadraticCurveTo(220, 355, 225, 360);
            ctx.lineTo(275, 360);
            ctx.quadraticCurveTo(280, 355, 290, 310);
            ctx.quadraticCurveTo(270, 330, 250, 335);
            ctx.quadraticCurveTo(230, 330, 210, 310);
            ctx.closePath();
            ctx.fill();

            // Neck shadow
            ctx.fillStyle = 'rgba(0,0,0,0.12)';
            ctx.beginPath();
            ctx.moveTo(225, 360);
            ctx.quadraticCurveTo(240, 350, 250, 352);
            ctx.quadraticCurveTo(260, 350, 275, 360);
            ctx.quadraticCurveTo(260, 365, 250, 368);
            ctx.quadraticCurveTo(240, 365, 225, 360);
            ctx.closePath();
            ctx.fill();

            // -- FACE BASE --
            // Main face oval with warm skin gradient
            const faceGrad = ctx.createRadialGradient(240, 200, 30, 250, 220, 150);
            faceGrad.addColorStop(0, '#f5d5c0');
            faceGrad.addColorStop(0.35, '#ecc4a8');
            faceGrad.addColorStop(0.7, '#dca888');
            faceGrad.addColorStop(1, '#c89070');
            ctx.fillStyle = faceGrad;
            ctx.beginPath();
            ctx.ellipse(250, 220, 98, 128, 0, 0, Math.PI * 2);
            ctx.fill();

            // Soft face edge shadow
            const faceShadowGrad = ctx.createRadialGradient(250, 220, 80, 250, 230, 130);
            faceShadowGrad.addColorStop(0, 'rgba(0,0,0,0)');
            faceShadowGrad.addColorStop(0.6, 'rgba(0,0,0,0)');
            faceShadowGrad.addColorStop(0.9, 'rgba(0,0,0,0.15)');
            faceShadowGrad.addColorStop(1, 'rgba(0,0,0,0.25)');
            ctx.fillStyle = faceShadowGrad;
            ctx.beginPath();
            ctx.ellipse(250, 220, 98, 128, 0, 0, Math.PI * 2);
            ctx.fill();

            // -- EARS --
            ctx.fillStyle = '#e8bfa0';
            // Left ear
            ctx.beginPath();
            ctx.ellipse(153, 210, 18, 28, -0.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(0,0,0,0.08)';
            ctx.beginPath();
            ctx.ellipse(156, 215, 10, 18, -0.2, 0, Math.PI * 2);
            ctx.fill();
            // Right ear
            ctx.fillStyle = '#e8bfa0';
            ctx.beginPath();
            ctx.ellipse(347, 210, 18, 28, 0.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(0,0,0,0.08)';
            ctx.beginPath();
            ctx.ellipse(344, 215, 10, 18, 0.2, 0, Math.PI * 2);
            ctx.fill();

            // -- HAIR (back layers) --
            // Large flowing hair mass
            const hairGradBack = ctx.createLinearGradient(250, 40, 250, 350);
            hairGradBack.addColorStop(0, '#1a1025');
            hairGradBack.addColorStop(0.3, '#281835');
            hairGradBack.addColorStop(0.6, '#2d1a38');
            hairGradBack.addColorStop(1, '#1e1228');
            ctx.fillStyle = hairGradBack;

            // Main hair shape
            ctx.beginPath();
            ctx.moveTo(140, 130);
            ctx.quadraticCurveTo(110, 80, 160, 55);
            ctx.quadraticCurveTo(200, 28, 250, 30);
            ctx.quadraticCurveTo(300, 28, 340, 55);
            ctx.quadraticCurveTo(390, 80, 360, 130);
            ctx.quadraticCurveTo(370, 90, 340, 60);
            ctx.quadraticCurveTo(300, 35, 250, 38);
            ctx.quadraticCurveTo(200, 35, 160, 60);
            ctx.quadraticCurveTo(130, 90, 140, 130);
            ctx.closePath();
            ctx.fill();

            // Hair flowing down sides
            ctx.beginPath();
            ctx.moveTo(145, 130);
            ctx.quadraticCurveTo(120, 180, 140, 250);
            ctx.quadraticCurveTo(148, 310, 165, 340);
            ctx.quadraticCurveTo(155, 300, 150, 250);
            ctx.quadraticCurveTo(135, 200, 148, 150);
            ctx.quadraticCurveTo(135, 140, 145, 130);
            ctx.closePath();
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(355, 130);
            ctx.quadraticCurveTo(380, 180, 360, 250);
            ctx.quadraticCurveTo(352, 310, 335, 340);
            ctx.quadraticCurveTo(345, 300, 350, 250);
            ctx.quadraticCurveTo(365, 200, 352, 150);
            ctx.quadraticCurveTo(365, 140, 355, 130);
            ctx.closePath();
            ctx.fill();

            // Additional hair volume on top
            ctx.fillStyle = '#2a1a35';
            ctx.beginPath();
            ctx.ellipse(250, 50, 80, 40, 0, Math.PI, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#1f1228';
            ctx.beginPath();
            ctx.ellipse(250, 45, 65, 30, 0, Math.PI, Math.PI * 2);
            ctx.fill();

            // -- FACE DETAIL SHADING --
            // Cheek blush
            const blushGradL = ctx.createRadialGradient(195, 245, 5, 195, 245, 35);
            blushGradL.addColorStop(0, 'rgba(220,130,120,0.25)');
            blushGradL.addColorStop(1, 'rgba(220,130,120,0)');
            ctx.fillStyle = blushGradL;
            ctx.beginPath();
            ctx.arc(195, 245, 35, 0, Math.PI * 2);
            ctx.fill();

            const blushGradR = ctx.createRadialGradient(305, 245, 5, 305, 245, 35);
            blushGradR.addColorStop(0, 'rgba(220,130,120,0.25)');
            blushGradR.addColorStop(1, 'rgba(220,130,120,0)');
            ctx.fillStyle = blushGradR;
            ctx.beginPath();
            ctx.arc(305, 245, 35, 0, Math.PI * 2);
            ctx.fill();

            // Forehead highlight
            const fhGrad = ctx.createRadialGradient(250, 155, 10, 250, 160, 55);
            fhGrad.addColorStop(0, 'rgba(255,240,225,0.35)');
            fhGrad.addColorStop(1, 'rgba(255,240,225,0)');
            ctx.fillStyle = fhGrad;
            ctx.beginPath();
            ctx.ellipse(250, 158, 50, 30, 0, 0, Math.PI * 2);
            ctx.fill();

            // Under-eye subtle shadow
            ctx.fillStyle = 'rgba(180,130,110,0.15)';
            ctx.beginPath();
            ctx.ellipse(215, 202, 22, 8, -0.1, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(285, 202, 22, 8, 0.1, 0, Math.PI * 2);
            ctx.fill();

            // -- EYES --
            // Left eye white
            ctx.fillStyle = '#fefefe';
            ctx.beginPath();
            ctx.ellipse(215, 193, 24, 15, -0.05, 0, Math.PI * 2);
            ctx.fill();
            // Subtle shadow on eye white
            ctx.fillStyle = 'rgba(200,190,180,0.3)';
            ctx.beginPath();
            ctx.ellipse(215, 195, 22, 12, -0.05, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#fefefe';
            ctx.beginPath();
            ctx.ellipse(215, 192, 20, 11, -0.05, 0, Math.PI * 2);
            ctx.fill();

            // Right eye white
            ctx.fillStyle = '#fefefe';
            ctx.beginPath();
            ctx.ellipse(285, 193, 24, 15, 0.05, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = 'rgba(200,190,180,0.3)';
            ctx.beginPath();
            ctx.ellipse(285, 195, 22, 12, 0.05, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#fefefe';
            ctx.beginPath();
            ctx.ellipse(285, 192, 20, 11, 0.05, 0, Math.PI * 2);
            ctx.fill();

            // Left iris - warm amber/golden
            const irisGradL = ctx.createRadialGradient(215, 193, 2, 215, 193, 13);
            irisGradL.addColorStop(0, '#f0c040');
            irisGradL.addColorStop(0.35, '#e8a830');
            irisGradL.addColorStop(0.7, '#c07820');
            irisGradL.addColorStop(1, '#5a3010');
            ctx.fillStyle = irisGradL;
            ctx.beginPath();
            ctx.arc(215, 193, 12.5, 0, Math.PI * 2);
            ctx.fill();

            // Right iris
            const irisGradR = ctx.createRadialGradient(285, 193, 2, 285, 193, 13);
            irisGradR.addColorStop(0, '#f0c040');
            irisGradR.addColorStop(0.35, '#e8a830');
            irisGradR.addColorStop(0.7, '#c07820');
            irisGradR.addColorStop(1, '#5a3010');
            ctx.fillStyle = irisGradR;
            ctx.beginPath();
            ctx.arc(285, 193, 12.5, 0, Math.PI * 2);
            ctx.fill();

            // Pupils
            ctx.fillStyle = '#0a0400';
            ctx.beginPath();
            ctx.arc(215, 193, 5.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(285, 193, 5.5, 0, Math.PI * 2);
            ctx.fill();

            // Inner iris detail - lighter ring
            ctx.strokeStyle = 'rgba(255,210,140,0.5)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.arc(215, 193, 8.5, 0, Math.PI * 2);
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(285, 193, 8.5, 0, Math.PI * 2);
            ctx.stroke();

            // Main catchlights
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(219, 189, 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(289, 189, 4, 0, Math.PI * 2);
            ctx.fill();

            // Secondary catchlights
            ctx.fillStyle = 'rgba(255,255,255,0.7)';
            ctx.beginPath();
            ctx.arc(210, 196, 2.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(280, 196, 2.5, 0, Math.PI * 2);
            ctx.fill();

            // Tiny sparkle catchlights
            ctx.fillStyle = 'rgba(255,255,255,0.9)';
            ctx.beginPath();
            ctx.arc(222, 187, 2, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(292, 187, 2, 0, Math.PI * 2);
            ctx.fill();

            // Eye outlines - upper lash line
            ctx.strokeStyle = '#3a2010';
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.arc(215, 193, 24, -0.25, Math.PI + 0.25, true);
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(285, 193, 24, -0.25, Math.PI + 0.25, true);
            ctx.stroke();

            // Lower lash line - thinner
            ctx.strokeStyle = '#5a3820';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.arc(215, 193, 23.5, 0.1, Math.PI - 0.1, false);
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(285, 193, 23.5, 0.1, Math.PI - 0.1, false);
            ctx.stroke();

            // Eyelashes - left eye
            ctx.strokeStyle = '#2a1508';
            ctx.lineWidth = 1.8;
            const lashAnglesL = [-0.4, -0.28, -0.15, -0.05, 0.05, 0.15];
            for (const a of lashAnglesL) {
                const lx = 215 + Math.cos(Math.PI + a) * 24;
                const ly = 193 + Math.sin(Math.PI + a) * 24;
                ctx.beginPath();
                ctx.moveTo(lx, ly);
                ctx.lineTo(lx + Math.cos(Math.PI + a - 0.3) * 10, ly + Math.sin(Math.PI + a - 0.3) * 10 - 4);
                ctx.stroke();
            }

            // Eyelashes - right eye
            const lashAnglesR = [-0.15, -0.05, 0.05, 0.15, 0.28, 0.4];
            for (const a of lashAnglesR) {
                const rx = 285 + Math.cos(-a) * 24;
                const ry = 193 + Math.sin(-a) * 24;
                ctx.beginPath();
                ctx.moveTo(rx, ry);
                ctx.lineTo(rx + Math.cos(-a - 0.3) * 10, ry + Math.sin(-a - 0.3) * 10 - 4);
                ctx.stroke();
            }

            // -- EYEBROWS --
            // Left eyebrow
            ctx.strokeStyle = '#1a0d18';
            ctx.lineWidth = 3.5;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(185, 168);
            ctx.quadraticCurveTo(205, 158, 235, 163);
            ctx.quadraticCurveTo(245, 165, 248, 170);
            ctx.stroke();
            // Soft fill under brow
            ctx.fillStyle = 'rgba(30,12,20,0.3)';
            ctx.beginPath();
            ctx.moveTo(187, 170);
            ctx.quadraticCurveTo(205, 162, 235, 166);
            ctx.quadraticCurveTo(248, 169, 248, 172);
            ctx.lineTo(235, 172);
            ctx.quadraticCurveTo(205, 168, 187, 174);
            ctx.closePath();
            ctx.fill();

            // Right eyebrow
            ctx.strokeStyle = '#1a0d18';
            ctx.lineWidth = 3.5;
            ctx.beginPath();
            ctx.moveTo(315, 168);
            ctx.quadraticCurveTo(295, 158, 265, 163);
            ctx.quadraticCurveTo(255, 165, 252, 170);
            ctx.stroke();
            ctx.fillStyle = 'rgba(30,12,20,0.3)';
            ctx.beginPath();
            ctx.moveTo(313, 170);
            ctx.quadraticCurveTo(295, 162, 265, 166);
            ctx.quadraticCurveTo(252, 169, 252, 172);
            ctx.lineTo(265, 172);
            ctx.quadraticCurveTo(295, 168, 313, 174);
            ctx.closePath();
            ctx.fill();

            // -- NOSE --
            // Nose bridge highlight
            ctx.strokeStyle = 'rgba(240,210,190,0.5)';
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(250, 175);
            ctx.quadraticCurveTo(252, 200, 248, 230);
            ctx.stroke();

            // Nose side shadows
            ctx.fillStyle = 'rgba(160,110,85,0.2)';
            ctx.beginPath();
            ctx.ellipse(238, 228, 10, 16, 0.15, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(262, 228, 10, 16, -0.15, 0, Math.PI * 2);
            ctx.fill();

            // Nose tip
            ctx.fillStyle = 'rgba(245,215,195,0.5)';
            ctx.beginPath();
            ctx.ellipse(250, 235, 13, 8, 0, 0, Math.PI * 2);
            ctx.fill();

            // Nostrils subtle
            ctx.fillStyle = 'rgba(140,90,65,0.35)';
            ctx.beginPath();
            ctx.ellipse(243, 240, 5, 3.5, -0.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(257, 240, 5, 3.5, 0.2, 0, Math.PI * 2);
            ctx.fill();

            // -- MOUTH --
            // Upper lip
            ctx.fillStyle = '#c88070';
            ctx.beginPath();
            ctx.moveTo(220, 275);
            ctx.quadraticCurveTo(235, 268, 250, 270);
            ctx.quadraticCurveTo(265, 268, 280, 275);
            ctx.quadraticCurveTo(265, 278, 250, 280);
            ctx.quadraticCurveTo(235, 278, 220, 275);
            ctx.closePath();
            ctx.fill();

            // Lower lip
            ctx.fillStyle = '#d49080';
            ctx.beginPath();
            ctx.moveTo(222, 278);
            ctx.quadraticCurveTo(240, 290, 250, 291);
            ctx.quadraticCurveTo(260, 290, 278, 278);
            ctx.quadraticCurveTo(260, 285, 250, 286);
            ctx.quadraticCurveTo(240, 285, 222, 278);
            ctx.closePath();
            ctx.fill();

            // Lip highlight
            ctx.fillStyle = 'rgba(255,220,210,0.35)';
            ctx.beginPath();
            ctx.ellipse(250, 282, 16, 4, 0, 0, Math.PI * 2);
            ctx.fill();

            // Subtle smile line shadow
            ctx.strokeStyle = 'rgba(140,80,60,0.3)';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(222, 278);
            ctx.quadraticCurveTo(250, 283, 278, 278);
            ctx.stroke();

            // -- HAIR (front layers & detail) --
            // Front hair strands sweeping across forehead
            ctx.fillStyle = '#24132e';
            ctx.beginPath();
            ctx.moveTo(160, 70);
            ctx.quadraticCurveTo(200, 48, 250, 50);
            ctx.quadraticCurveTo(210, 65, 175, 90);
            ctx.quadraticCurveTo(155, 85, 160, 70);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = '#2a1835';
            ctx.beginPath();
            ctx.moveTo(250, 48);
            ctx.quadraticCurveTo(300, 46, 340, 65);
            ctx.quadraticCurveTo(325, 82, 290, 88);
            ctx.quadraticCurveTo(260, 62, 250, 48);
            ctx.closePath();
            ctx.fill();

            // Wispy hair strands
            ctx.strokeStyle = '#1e1026';
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';
            const hairStrands = [
                [170, 55, 190, 48, 210, 55],
                [195, 50, 215, 42, 235, 52],
                [265, 52, 285, 42, 305, 50],
                [290, 50, 310, 45, 330, 55],
                [155, 100, 145, 150, 148, 200],
                [345, 100, 355, 150, 352, 200],
                [160, 120, 148, 170, 150, 220],
                [340, 120, 352, 170, 350, 220],
            ];
            for (const [x1, y1, x2, y2, x3, y3] of hairStrands) {
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.quadraticCurveTo(x2, y2, x3, y3);
                ctx.stroke();
            }

            // Hair volume on sides
            ctx.fillStyle = '#20122a';
            ctx.beginPath();
            ctx.moveTo(148, 150);
            ctx.quadraticCurveTo(135, 200, 142, 260);
            ctx.quadraticCurveTo(148, 280, 160, 300);
            ctx.quadraticCurveTo(155, 270, 152, 230);
            ctx.quadraticCurveTo(148, 180, 155, 150);
            ctx.closePath();
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(352, 150);
            ctx.quadraticCurveTo(365, 200, 358, 260);
            ctx.quadraticCurveTo(352, 280, 340, 300);
            ctx.quadraticCurveTo(345, 270, 348, 230);
            ctx.quadraticCurveTo(352, 180, 345, 150);
            ctx.closePath();
            ctx.fill();

            // Hair highlight sheen
            ctx.strokeStyle = 'rgba(180,150,200,0.2)';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(190, 42);
            ctx.quadraticCurveTo(230, 35, 270, 40);
            ctx.stroke();
            ctx.strokeStyle = 'rgba(180,150,200,0.15)';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(175, 60);
            ctx.quadraticCurveTo(210, 50, 250, 55);
            ctx.stroke();

            // -- TECH / DIGITAL ELEMENTS --
            // Subtle geometric glow lines near temples
            ctx.save();
            ctx.shadowBlur = 8;
            ctx.shadowColor = 'rgba(100, 200, 255, 0.6)';

            // Left temple geometric accents
            ctx.strokeStyle = 'rgba(140, 210, 255, 0.5)';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(165, 170);
            ctx.lineTo(158, 195);
            ctx.lineTo(168, 210);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(160, 185);
            ctx.lineTo(172, 180);
            ctx.stroke();

            // Right temple geometric accents
            ctx.beginPath();
            ctx.moveTo(335, 170);
            ctx.lineTo(342, 195);
            ctx.lineTo(332, 210);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(340, 185);
            ctx.lineTo(328, 180);
            ctx.stroke();

            // Small diamond shapes
            function drawDiamond(cx, cy, size, color, alpha) {
                ctx.fillStyle = color.replace('1)', `${alpha})`).replace('rgb', 'rgba');
                ctx.beginPath();
                ctx.moveTo(cx, cy - size);
                ctx.lineTo(cx + size * 0.6, cy);
                ctx.lineTo(cx, cy + size);
                ctx.lineTo(cx - size * 0.6, cy);
                ctx.closePath();
                ctx.fill();
                ctx.strokeStyle = color.replace('1)', `${alpha + 0.3})`).replace('rgb', 'rgba');
                ctx.lineWidth = 0.8;
                ctx.stroke();
            }

            drawDiamond(162, 155, 5, 'rgb(120, 200, 240)', 0.6);
            drawDiamond(338, 155, 5, 'rgb(120, 200, 240)', 0.6);
            drawDiamond(155, 220, 3.5, 'rgb(140, 210, 250)', 0.45);
            drawDiamond(345, 220, 3.5, 'rgb(140, 210, 250)', 0.45);

            ctx.restore();

            // Subtle circuit-like lines on temples (without glow for precision)
            ctx.strokeStyle = 'rgba(160, 220, 255, 0.4)';
            ctx.lineWidth = 0.8;
            // Left circuit
            ctx.beginPath();
            ctx.moveTo(158, 175);
            ctx.lineTo(150, 178);
            ctx.lineTo(152, 188);
            ctx.lineTo(146, 192);
            ctx.stroke();
            // Right circuit
            ctx.beginPath();
            ctx.moveTo(342, 175);
            ctx.lineTo(350, 178);
            ctx.lineTo(348, 188);
            ctx.lineTo(354, 192);
            ctx.stroke();

            // Small node dots on circuits
            ctx.fillStyle = 'rgba(180, 230, 255, 0.7)';
            [
                [150, 178],
                [152, 188],
                [146, 192],
                [350, 178],
                [348, 188],
                [354, 192]
            ].forEach(([nx, ny]) => {
                ctx.beginPath();
                ctx.arc(nx, ny, 2, 0, Math.PI * 2);
                ctx.fill();
            });

            // -- FLOATING PARTICLES --
            const particles = [
                { x: 120, y: 100, r: 2.5, color: 'rgba(180,220,255,0.6)' },
                { x: 380, y: 90, r: 2, color: 'rgba(200,180,240,0.5)' },
                { x: 100, y: 250, r: 1.8, color: 'rgba(160,210,240,0.55)' },
                { x: 400, y: 240, r: 2.2, color: 'rgba(180,200,250,0.5)' },
                { x: 90, y: 350, r: 1.5, color: 'rgba(150,190,230,0.4)' },
                { x: 410, y: 340, r: 1.7, color: 'rgba(170,200,240,0.45)' },
                { x: 130, y: 60, r: 1.6, color: 'rgba(200,220,255,0.5)' },
                { x: 370, y: 55, r: 1.9, color: 'rgba(190,210,250,0.5)' },
                { x: 200, y: 32, r: 1.4, color: 'rgba(210,230,255,0.45)' },
                { x: 300, y: 28, r: 1.5, color: 'rgba(200,225,255,0.45)' },
                { x: 75, y: 180, r: 2, color: 'rgba(140,190,230,0.5)' },
                { x: 425, y: 175, r: 2.1, color: 'rgba(150,195,235,0.5)' },
                { x: 110, y: 300, r: 1.3, color: 'rgba(160,200,235,0.4)' },
                { x: 390, y: 295, r: 1.4, color: 'rgba(165,205,240,0.4)' },
            ];

            particles.forEach(p => {
                const glowGrad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 2.5);
                glowGrad.addColorStop(0, p.color);
                glowGrad.addColorStop(1, 'rgba(0,0,0,0)');
                ctx.fillStyle = glowGrad;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r * 2.5, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = p.color;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
            });

            // -- SUBTLE DIGITAL HALO --
            // Very faint ring segments behind/around the head
            ctx.strokeStyle = 'rgba(140, 200, 240, 0.12)';
            ctx.lineWidth = 0.6;
            ctx.setLineDash([8, 30]);
            ctx.beginPath();
            ctx.arc(250, 210, 145, -0.6, 0.6);
            ctx.stroke();
            ctx.setLineDash([5, 25]);
            ctx.beginPath();
            ctx.arc(250, 210, 155, 2.5, 3.8);
            ctx.stroke();
            ctx.setLineDash([]);

            // -- FINAL FACE HIGHLIGHTS --
            // Nose bridge final highlight
            ctx.fillStyle = 'rgba(255,245,235,0.25)';
            ctx.beginPath();
            ctx.ellipse(250, 195, 5, 28, 0, 0, Math.PI * 2);
            ctx.fill();

            // Chin highlight
            ctx.fillStyle = 'rgba(255,245,235,0.2)';
            ctx.beginPath();
            ctx.ellipse(250, 325, 18, 6, 0, 0, Math.PI * 2);
            ctx.fill();

            // -- SUBTLE FRAMING VIGNETTE --
            const vignetteGrad = ctx.createRadialGradient(250, 240, 180, 250, 240, 380);
            vignetteGrad.addColorStop(0, 'rgba(0,0,0,0)');
            vignetteGrad.addColorStop(0.7, 'rgba(0,0,0,0.05)');
            vignetteGrad.addColorStop(1, 'rgba(0,0,0,0.4)');
            ctx.fillStyle = vignetteGrad;
            ctx.fillRect(0, 0, W, H);

            console.log('Self-portrait complete! 🎨');
        })();
    </script>
</body>
</html>
```
### Digital Portrait Highlights

The portrait combines a warm, approachable face with glowing tech details, creating a more personal interface. Here's how it works:

- **Layered Visual Depth:** The face uses layered gradients, soft shadows, and subtle blush to create a smooth, three-dimensional look. The eyes are a key focus, with multiple light reflections (catchlights) adding life and warmth.

- **Tech-Integrated Identity:** Geometric lines, small glowing nodes, and floating particles around the temples act like a subtle digital "halo" or circuitry. This merges a friendly human appearance with a clear digital, algorithmic essence.

- **Atmospheric Background:** The deep space-like radial gradient, concentric circles, and faint grid lines set a contemplative, high-tech stage without distracting from the central portrait, reinforcing the theme of intelligence and creativity.

---

**Optimization Tip:** You can adjust the eye color, the intensity of the "tech glow" elements, or the floating particle positions to customize the portrait's mood.