I'll draw an abstract radial "Solar Geometry" piece — layered glowing polygons and orbits in neon gradients against deep black, with slow continuous rotation to give it life. No images, pure CSS/SVG shapes and gradients inside a 500×500 frame.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Solar Geometry</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #050505; display: flex; justify-content: flex-start; align-items: flex-start; }
  .canvas {
    width: 500px;
    height: 500px;
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at 50% 50%, #0a0a1a 0%, #020204 100%);
  }

  /* Deep radial glow core */
  .core {
    position: absolute;
    width: 180px;
    height: 180px;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle at center, #fffc00 0%, #ff0090 35%, #00e5ff 70%, transparent 85%);
    border-radius: 50%;
    filter: blur(18px);
    opacity: 0.9;
  }

  /* Inner bright nucleus */
  .nucleus {
    position: absolute;
    width: 60px;
    height: 60px;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle at center, #ffffff 0%, #fff8a0 40%, #ff0090 100%);
    border-radius: 50%;
    box-shadow: 0 0 40px 10px rgba(255, 0, 150, 0.6), 0 0 80px 20px rgba(0, 230, 255, 0.3);
    z-index: 10;
  }

  /* Rotating ring groups */
  .orbit {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .orbit1 {
    width: 340px; height: 340px;
    animation: spin 18s linear infinite;
  }
  .orbit2 {
    width: 420px; height: 420px;
    animation: spin-reverse 24s linear infinite;
  }
  .orbit3 {
    width: 280px; height: 280px;
    animation: spin 14s linear infinite;
  }

  /* Geometric nodes on orbits */
  .node {
    position: absolute;
    border-radius: 50%;
    box-shadow: 0 0 10px 2px currentColor;
  }

  /* Triangular orbit markers using clip-path */
  .tri {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #00ffe1, #ff00aa);
    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
    filter: drop-shadow(0 0 6px #00ffe1);
  }

  /* Small hex nodes */
  .hex {
    width: 14px; height: 14px;
    background: #fffc00;
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    box-shadow: 0 0 8px #fffc00;
  }

  /* Large diamond nodes */
  .diamond {
    width: 22px; height: 22px;
    background: linear-gradient(45deg, #ff0090, #fffc00);
    transform: rotate(45deg);
    box-shadow: 0 0 12px #ff0090;
  }

  @keyframes spin {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to   { transform: translate(-50%, -50%) rotate(360deg); }
  }
  @keyframes spin-reverse {
    from { transform: translate(-50%, -50%) rotate(360deg); }
    to   { transform: translate(-50%, -50%) rotate(0deg); }
  }

  /* Static decorative radial lines */
  .ray {
    position: absolute;
    top: 50%; left: 50%;
    width: 1px; height: 250px;
    background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0) 100%);
    transform-origin: top center;
  }
</style>
</head>
<body>

<div class="canvas" aria-label="Abstract solar geometry artwork">
  <div class="core"></div>
  <div class="nucleus"></div>

  <!-- Rays -->
  <div class="ray" style="transform: translate(-50%, -50%) rotate(0deg);"></div>
  <div class="ray" style="transform: translate(-50%, -50%) rotate(45deg);"></div>
  <div class="ray" style="transform: translate(-50%, -50%) rotate(90deg);"></div>
  <div class="ray" style="transform: translate(-50%, -50%) rotate(135deg);"></div>

  <!-- Orbit 1 -->
  <div class="orbit orbit1">
    <div class="node tri" style="top: -14px; left: calc(50% - 14px);"></div>
    <div class="node hex" style="bottom: 0; right: -7px;"></div>
    <div class="node tri" style="bottom: -14px; left: calc(50% - 14px);"></div>
    <div class="node hex" style="top: 0; left: -7px;"></div>
    <div class="node diamond" style="top: 20%; right: -10px;"></div>
    <div class="node diamond" style="bottom: 20%; left: -10px;"></div>
  </div>

  <!-- Orbit 2 -->
  <div class="orbit orbit2">
    <div class="node tri" style="top: -14px; left: calc(50% - 14px); transform: rotate(0deg);"></div>
    <div class="node hex" style="bottom: -7px; left: calc(50% - 7px);"></div>
    <div class="node diamond" style="top: 50%; right: -11px; transform: translateY(-50%) rotate(45deg);"></div>
    <div class="node diamond" style="top: 50%; left: -11px; transform: translateY(-50%) rotate(45deg);"></div>
    <div class="node tri" style="top: 30%; left: -14px; transform: rotate(90deg);"></div>
    <div class="node tri" style="top: 70%; right: -14px; transform: rotate(-90deg);"></div>
  </div>

  <!-- Orbit 3 -->
  <div class="orbit orbit3">
    <div class="node diamond" style="top: -11px; left: calc(50% - 11px); transform: rotate(45deg);"></div>
    <div class="node hex" style="bottom: -7px; left: calc(50% - 7px);"></div>
    <div class="node tri" style="bottom: -14px; left: calc(50% - 14px); transform: rotate(180deg);"></div>
    <div class="node diamond" style="top: 50%; right: -11px; transform: translateY(-50%) rotate(45deg);"></div>
    <div class="node hex" style="top: 50%; left: -7px; transform: translateY(-50%);"></div>
  </div>
</div>

</body>
</html>
```