I'll draw a serene nighttime scene — a crescent moon over rolling hills with a reflection in water, some stars, and a shooting star. I like the calm mood and the chance to use gradients and simple shapes.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Moonlit Night</title>
<style>
  html, body { margin: 0; padding: 0; }
  #scene {
    position: relative;
    width: 500px;
    height: 500px;
    overflow: hidden;
    background: linear-gradient(#0b1a3a 0%, #15294d 40%, #2a4066 60%, #1a2b4a 100%);
  }

  /* Stars */
  .star {
    position: absolute;
    background: #fff;
    border-radius: 50%;
    animation: twinkle 3s infinite ease-in-out;
  }
  @keyframes twinkle {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
  }

  /* Moon */
  #moon {
    position: absolute;
    top: 55px;
    left: 340px;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: #f7f3d8;
    box-shadow: 0 0 40px 15px rgba(247,243,216,0.4);
  }
  #moon::after {
    content: "";
    position: absolute;
    top: -8px;
    left: 22px;
    width: 78px;
    height: 78px;
    border-radius: 50%;
    background: #15294d;
  }

  /* Shooting star */
  #shooting {
    position: absolute;
    top: 90px;
    left: 60px;
    width: 90px;
    height: 2px;
    background: linear-gradient(90deg, rgba(255,255,255,0), #fff);
    transform: rotate(20deg);
    border-radius: 2px;
    animation: shoot 6s infinite ease-in;
    opacity: 0;
  }
  @keyframes shoot {
    0% { transform: translate(0,0) rotate(20deg); opacity: 0; }
    8% { opacity: 1; }
    18% { transform: translate(180px,65px) rotate(20deg); opacity: 0; }
    100% { opacity: 0; }
  }

  /* Water */
  #water {
    position: absolute;
    bottom: 0;
    width: 500px;
    height: 160px;
    background: linear-gradient(#1e3a63, #0a1830);
  }
  #moonReflect {
    position: absolute;
    top: 8px;
    left: 375px;
    width: 30px;
    height: 130px;
    background: linear-gradient(rgba(247,243,216,0.5), rgba(247,243,216,0));
    filter: blur(4px);
  }

  /* Hills */
  .hill {
    position: absolute;
    border-radius: 50% 50% 0 0;
  }
  #hill1 {
    bottom: 160px;
    left: -60px;
    width: 320px;
    height: 130px;
    background: #14203a;
  }
  #hill2 {
    bottom: 160px;
    left: 200px;
    width: 400px;
    height: 170px;
    background: #0e1830;
  }
</style>
</head>
<body>
<div id="scene">
  <div id="moon"></div>
  <div id="shooting"></div>
  <div class="hill" id="hill2"></div>
  <div class="hill" id="hill1"></div>
  <div id="water">
    <div id="moonReflect"></div>
  </div>
</div>
<script>
  const scene = document.getElementById('scene');
  for (let i = 0; i < 70; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = Math.random() * 2 + 1;
    s.style.width = size + 'px';
    s.style.height = size + 'px';
    s.style.left = Math.random() * 500 + 'px';
    s.style.top = Math.random() * 300 + 'px';
    s.style.animationDelay = Math.random() * 3 + 's';
    scene.appendChild(s);
  }
</script>
</body>
</html>
```