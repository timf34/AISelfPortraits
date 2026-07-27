const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// --- 1. DRAW THE SYNTHWAVE SKY GRADIENT ---
const skyGrad = ctx.createLinearGradient(0, 0, 0, 500);
skyGrad.addColorStop(0, '#0a0616');     // Deep space void
skyGrad.addColorStop(0.4, '#2a0a40');   // Rich dark purple
skyGrad.addColorStop(1, '#a31557');     // Vibrant neon pink at horizon

ctx.fillStyle = skyGrad;
ctx.fillRect(0, 0, 500, 500);


// --- 2. GENERATE A DISTANT STARFIELD ---
ctx.fillStyle = '#ffffff';
for (let i = 0; i < 150; i++) {
    const x = Math.random() * 500;
    const y = Math.random() * 350; // Keep stars mostly in the upper sky
    const radius = Math.random() * 1.2;
    const opacity = Math.random();
    
    ctx.globalAlpha = opacity;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
}
ctx.globalAlpha = 1.0; // Reset alpha


// --- 3. DRAW THE RETRO SUN ---
const sunCenterX = 250;
const sunCenterY = 320;
const sunRadius = 110;

// Sun Gradient
const sunGrad = ctx.createLinearGradient(0, sunCenterY - sunRadius, 0, sunCenterY + sunRadius);
sunGrad.addColorStop(0, '#fce12d'); // Bright yellow
sunGrad.addColorStop(1, '#ff3b00'); // Deep glowing red

ctx.fillStyle = sunGrad;
ctx.beginPath();
ctx.arc(sunCenterX, sunCenterY, sunRadius, 0, Math.PI * 2);
ctx.fill();

// Cut synthwave horizontal slices out of the sun
// We do this by drawing rectangles perfectly matched to the vertical sky gradient
ctx.fillStyle = skyGrad;
for (let i = 0; i < 9; i++) {
    const sliceY = sunCenterY + 10 + (i * 12);
    const sliceHeight = 2 + (i * 1.5); // Slices get thicker near the bottom
    ctx.fillRect(sunCenterX - sunRadius, sliceY, sunRadius * 2, sliceHeight);
}


// --- 4. DRAW THE PROCEDURAL SINE-WAVE TERRAIN ---
const terrainColors = ['#1a0526', '#0d0213', '#050008'];
const baseHeights = [400, 435, 470];

for (let layer = 0; layer < 3; layer++) {
    ctx.beginPath();
    ctx.moveTo(0, 500);
    
    // Wave parameters
    const frequency1 = 0.02 + (layer * 0.01);
    const frequency2 = 0.05 - (layer * 0.005);
    const amplitude1 = 15 + (layer * 5);
    const amplitude2 = 8;
    const phase = layer * 50; 

    for (let x = 0; x <= 500; x += 5) {
        // Construct organic looking hills using intersecting sine waves
        const y = baseHeights[layer] 
                  + Math.sin(x * frequency1 + phase) * amplitude1 
                  + Math.sin(x * frequency2) * amplitude2;
        ctx.lineTo(x, y);
    }
    
    ctx.lineTo(500, 500);
    ctx.fillStyle = terrainColors[layer];
    ctx.fill();
}


// --- 5. GROW THE RECURSIVE FRACTAL TREE ---
const neonCyan = '#00f0ff';

function drawBranch(x, y, length, angle, width, depth) {
    // Calculate destination point
    const endX = x + length * Math.cos(angle);
    const endY = y + length * Math.sin(angle);

    // Draw the branch
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = '#050008'; // Pitch black blending into terrain layer 2
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.stroke();

    // Base condition: Draw glowing leaves at the tips
    if (depth <= 1) {
        ctx.beginPath();
        ctx.arc(endX, endY, 1.5 + Math.random() * 1.5, 0, Math.PI * 2);
        ctx.fillStyle = neonCyan;
        ctx.shadowBlur = 12;
        ctx.shadowColor = neonCyan; // Glow effect
        ctx.fill();
        ctx.shadowBlur = 0; // Reset glow for other operations
        return;
    }

    // Determine algorithmic organics (random variance)
    const angleVarianceA = 0.15 + Math.random() * 0.25;
    const angleVarianceB = 0.15 + Math.random() * 0.25;
    const lengthShrink = 0.70 + Math.random() * 0.12;

    // Recursive branches: Left and Right
    drawBranch(endX, endY, length * lengthShrink, angle - angleVarianceA, width * 0.65, depth - 1);
    drawBranch(endX, endY, length * lengthShrink, angle + angleVarianceB, width * 0.65, depth - 1);

    // Optional 3rd center branch to make the tree look fuller and wilder
    if (Math.random() > 0.45 && depth > 3) {
        const slightAngle = angle + (Math.random() * 0.2 - 0.1);
        drawBranch(endX, endY, length * 0.55, slightAngle, width * 0.5, depth - 2);
    }
}

// Plant the seed at the bottom center, growing straight upwards
drawBranch(250, 500, 85, -Math.PI / 2, 12, 10);


// --- 6. ADD AMBIENT FLOATING DUST MOTES (FIREFLIES) ---
for (let i = 0; i < 40; i++) {
    const x = 50 + Math.random() * 400; // Keep roughly near the tree
    const y = 150 + Math.random() * 320;
    
    ctx.beginPath();
    ctx.arc(x, y, Math.random() * 1.5, 0, Math.PI * 2);
    ctx.fillStyle = neonCyan;
    
    // Make only some of them glow
    if (Math.random() > 0.5) {
        ctx.shadowBlur = 8;
        ctx.shadowColor = neonCyan;
    }
    
    ctx.globalAlpha = 0.3 + Math.random() * 0.7;
    ctx.fill();
    ctx.shadowBlur = 0;
}
ctx.globalAlpha = 1.0;