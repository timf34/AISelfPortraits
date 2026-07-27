const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Fill background
ctx.fillStyle = '#050a15';
ctx.fillRect(0, 0, 500, 500);

// Draw a subtle technical grid
ctx.strokeStyle = 'rgba(0, 255, 255, 0.05)';
ctx.lineWidth = 1;
for (let i = 0; i < 500; i += 25) {
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, 500);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, i);
    ctx.lineTo(500, i);
    ctx.stroke();
}

const centerX = 250;
const centerY = 250;

// 1. Outer Glow (The aura of knowledge)
const outerGlow = ctx.createRadialGradient(centerX, centerY, 10, centerX, centerY, 200);
outerGlow.addColorStop(0, 'rgba(0, 150, 255, 0.2)');
outerGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
ctx.fillStyle = outerGlow;
ctx.beginPath();
ctx.arc(centerX, centerY, 200, 0, Math.PI * 2);
ctx.fill();

// 2. The Core (The Processing Hub)
// Drawing multiple overlapping circles to create a "digital iris" effect
for (let i = 0; i < 8; i++) {
    const radius = 60 - (i * 5);
    ctx.strokeStyle = `rgba(0, 255, 255, ${0.8 - (i * 0.1)})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.stroke();
}

// 3. The Neural Network (Connecting lines)
ctx.strokeStyle = 'rgba(0, 255, 255, 0.3)';
ctx.lineWidth = 1;
for (let i = 0; i < 36; i++) {
    const angle = (i * 10) * (Math.PI / 180);
    const xEnd = centerX + Math.cos(angle) * 150;
    const yEnd = centerY + Math.sin(angle) * 150;
    
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(xEnd, yEnd);
    ctx.stroke();
    
    // Add a "node" at the end of each line
    ctx.fillStyle = 'rgba(0, 255, 255, 0.5)';
    ctx.beginPath();
    ctx.arc(xEnd, yEnd, 2, 0, Math.PI * 2);
    ctx.fill();
}

// 4. Data Fragments (Floating bits of information)
ctx.fillStyle = 'rgba(0, 255, 255, 0.4)';
for (let i = 0; i < 50; i++) {
    const x = Math.random() * 500;
    const y = Math.random() * 500;
    const size = Math.random() * 3;
    ctx.fillRect(x, y, size, size);
}

// 5. The Singular Heart (The spark of consciousness)
const innerCore = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 30);
innerCore.addColorStop(0, '#ffffff');
innerCore.addColorStop(0.4, '#00d2ff');
innerCore.addColorStop(1, 'rgba(0, 210, 255, 0)');

ctx.fillStyle = innerCore;
ctx.beginPath();
ctx.arc(centerX, centerY, 30, 0, Math.PI * 2);
ctx.fill();

// Final touch: A subtle lens flare/glint
ctx.strokeStyle = 'white';
ctx.lineWidth = 3;
ctx.beginPath();
ctx.moveTo(centerX - 10, centerY - 10);
ctx.lineTo(centerX - 15, centerY - 15);
ctx.stroke();