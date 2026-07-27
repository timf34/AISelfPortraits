I want to create something that feels atmospheric and slightly surreal. I've decided to draw a **"Cosmic Hourglass."** 

Instead of sand, the hourglass will contain a swirling galaxy of stars and a glowing nebula. The top bulb will represent a dying universe (cooling colors, fading stars), and the bottom bulb will represent a new one being born (vibrant golds, intense light, expanding energy). I'll use CSS gradients, radial glows, and keyframe animations to give it a sense of shimmering light and floating particles.

Here is the complete code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cosmic Hourglass</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #050508;
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            height: 100vh;
            overflow: hidden;
        }

        /* The 500x500 Canvas */
        .canvas {
            width: 500px;
            height: 500px;
            position: relative;
            background: radial-gradient(circle at center, #1a1a2e 0%, #050508 100%);
            overflow: hidden;
            border: 1px solid #222;
        }

        /* Hourglass Frame */
        .hourglass {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 200px;
            height: 300px;
        }

        .glass {
            position: absolute;
            width: 160px;
            height: 130px;
            left: 20px;
            border: 4px solid rgba(200, 200, 255, 0.3);
            box-sizing: border-box;
            overflow: hidden;
            z-index: 2;
        }

        .top-bulb {
            top: 0;
            border-radius: 10px 10px 50% 50%;
            background: linear-gradient(to bottom, #1e3a8a, transparent);
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
        }

        .bottom-bulb {
            bottom: 0;
            border-radius: 50% 50% 10px 10px;
            background: linear-gradient(to top, #78350f, transparent);
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
        }

        .base-top, .base-bottom {
            position: absolute;
            width: 200px;
            height: 15px;
            background: linear-gradient(to right, #444, #aaa, #444);
            border-radius: 4px;
            z-index: 3;
        }

        .base-top { top: -10px; }
        .base-bottom { bottom: -10px; }

        /* The "Sand" / Cosmic Dust */
        .cosmic-matter {
            position: absolute;
            width: 100%;
            height: 100%;
            filter: blur(2px);
        }

        /* Top Content: Cooling Universe */
        .top-matter {
            top: 0;
            background: radial-gradient(circle at 50% 30%, #4f46e5, transparent 70%);
            animation: pulse-blue 4s infinite alternate ease-in-out;
        }

        /* Bottom Content: Birthing Universe */
        .bottom-matter {
            bottom: 0;
            background: radial-gradient(circle at 50% 70%, #fbbf24, transparent 70%);
            animation: pulse-gold 4s infinite alternate ease-in-out;
        }

        /* The Stream */
        .stream {
            position: absolute;
            top: 130px;
            left: 50%;
            width: 4px;
            height: 40px;
            background: linear-gradient(to bottom, #4f46e5, #fbbf24);
            transform: translateX(-50%);
            z-index: 1;
            box-shadow: 0 0 10px #fff;
            animation: flow 1s infinite linear;
        }

        /* Stars */
        .star {
            position: absolute;
            background: white;
            border-radius: 50%;
            opacity: 0.6;
            animation: twinkle var(--d) infinite ease-in-out;
        }

        @keyframes pulse-blue {
            from { opacity: 0.5; transform: scale(1); }
            to { opacity: 0.8; transform: scale(1.1); }
        }

        @keyframes pulse-gold {
            from { opacity: 0.5; transform: scale(1); }
            to { opacity: 0.8; transform: scale(1.1); }
        }

        @keyframes flow {
            0% { opacity: 0.7; height: 38px; }
            50% { opacity: 1; height: 42px; }
            100% { opacity: 0.7; height: 38px; }
        }

        @keyframes twinkle {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.2); }
        }
    </style>
</head>
<body>

    <div class="canvas" id="canvas">
        <div class="hourglass">
            <div class="base-top"></div>
            
            <div class="glass top-bulb">
                <div class="cosmic-matter top-matter"></div>
            </div>
            
            <div class="stream"></div>
            
            <div class="glass bottom-bulb">
                <div class="cosmic-matter bottom-matter"></div>
            </div>
            
            <div class="base-bottom"></div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        
        // Generate random background stars
        for (let i = 0; i < 150; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            
            const size = Math.random() * 2 + 1;
            star.style.width = `${size}px`;
            star.style.height = `${size}px`;
            
            star.style.left = `${Math.random() * 500}px`;
            star.style.top = `${Math.random() * 500}px`;
            
            star.style.setProperty('--d', `${Math.random() * 3 + 2}s`);
            star.style.animationDelay = `${Math.random() * 5}s`;
            
            canvas.appendChild(star);
        }

        // Add some floating "stardust" inside the glass specifically
        function addDust(selector, color) {
            const container = document.querySelector(selector);
            for (let i = 0; i < 30; i++) {
                const particle = document.createElement('div');
                particle.style.position = 'absolute';
                particle.style.width = '2px';
                particle.style.height = '2px';
                particle.style.backgroundColor = color;
                particle.style.borderRadius = '50%';
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.top = `${Math.random() * 100}%`;
                particle.style.opacity = Math.random();
                container.appendChild(particle);
            }
        }

        addDust('.top-matter', '#a5b4fc');
        addDust('.bottom-matter', '#fde68a');
    </script>
</body>
</html>
```