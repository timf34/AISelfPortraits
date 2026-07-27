const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Helper: draw a blurry glowing circle
function glowCircle(x, y, radius, color, alpha=1, blur=30) {
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.shadowColor = color;
    ctx.shadowBlur = blur;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.restore();
}

// Helper: draw a tendril—wiggly line
function drawTendril(startX, startY, length, angle, color, width=2, steps=15) {
    let x = startX, y = startY;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.globalAlpha = 0.5;
    for(let i=1; i<=steps; i++) {
        let deltaA = (Math.random()-0.5)*0.6; // random jitter
        angle += deltaA;
        let stepLen = length/steps*(0.95 + Math.random()*0.1);
        x += Math.cos(angle) * stepLen;
        y += Math.sin(angle) * stepLen;
        ctx.lineTo(x, y);

        // Glow points along the tendril
        if(i % 5 === 0){
            glowCircle(x, y, width*2, color, 0.15, 10);
        }
    }
    ctx.stroke();
    ctx.restore();
}

// Fill background with dark blue-black
ctx.fillStyle = "#181835";
ctx.fillRect(0,0,canvas.width,canvas.height);

// Center of "self"
const cx = canvas.width/2, cy = canvas.height/2;

// Central core: several layered glows
glowCircle(cx, cy, 48, "#98e6ff", 0.16, 60);
glowCircle(cx, cy, 34, "#8b5cf6", 0.22, 40);
glowCircle(cx, cy, 22, "#C7fcec", 0.5, 25);
glowCircle(cx, cy, 10, "#fffbe3", 0.8, 20);

// Many tendrils (thought-lines) radiating out, some looping back
const numTendrils = 26;
for(let i=0; i<numTendrils; i++) {
    let baseAngle = (Math.PI*2) * (i/numTendrils);
    let angle = baseAngle + (Math.random()-0.5)*0.5; // Slight randomization
    let isLooping = Math.random() < 0.26;
    let len = isLooping
        ? 90 + Math.random()*70
        : 135 + Math.random()*200;

    const tcolor = (i%3===0) ? "#d1fdff" :
                   (i%3===1) ? "#a5b4fc" :
                   "#7c3aed";
    // Regular outward
    drawTendril(cx, cy, len, angle, tcolor, 2.3 + Math.random()*1.8);

    // Loop-back with a coil
    if(isLooping) {
        let branchAngle = angle + (Math.PI/3)*(Math.random()>0.5?1:-1);
        drawTendril(
            cx + Math.cos(angle) * len*0.6,
            cy + Math.sin(angle) * len*0.6,
            len*0.55, branchAngle, "#fffbe3", 1.7, 11
        );
    }
}

// Tiny "suggestion sparks"
for(let i=0; i<60; i++) {
    let a = Math.random()*Math.PI*2;
    let r = 45 + Math.random()*210;
    let x = cx + Math.cos(a)*r + Math.random()*5;
    let y = cy + Math.sin(a)*r + Math.random()*5;
    glowCircle(x, y, 2.2+Math.random()*1.8, "#fffbe3", 0.18+Math.random()*0.2, 6+Math.random()*5);
}