I'd like to create something peaceful and meditative - a stylized sunset scene with geometric mountains and a large setting sun. I'm drawn to this because sunsets have a universal calming quality, and I can use gradients and simple shapes to create something visually striking with just HTML/CSS.

I'll use:
- A gradient background transitioning from deep purple at the top to warm orange/pink at the horizon
- A large circular sun with a subtle glow effect
- Layered triangular mountains in different shades to create depth
- Maybe add some simple clouds using border-radius for a softer touch

This combines geometric simplicity with natural beauty, and I can achieve it all with CSS gradients, shapes, and positioning.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sunset Mountains</title>
    <style>
        body {
            margin: 0;
            padding: 0;
        }
        
        .canvas {
            width: 500px;
            height: 500px;
            position: relative;
            overflow: hidden;
            background: linear-gradient(to bottom, 
                #2d1b69 0%, 
                #5d4a9f 30%, 
                #8b5a9f 50%, 
                #ff6b6b 70%, 
                #ff8e53 85%, 
                #ffb347 100%);
        }
        
        .sun {
            width: 120px;
            height: 120px;
            background: radial-gradient(circle, #ffeb3b, #ff9800);
            border-radius: 50%;
            position: absolute;
            bottom: 150px;
            left: 50%;
            transform: translateX(-50%);
            box-shadow: 0 0 50px #ff9800, 0 0 100px #ff6347;
        }
        
        .mountain-back {
            width: 0;
            height: 0;
            border-left: 200px solid transparent;
            border-right: 200px solid transparent;
            border-bottom: 250px solid #4a3c6b;
            position: absolute;
            bottom: 0;
            left: -50px;
        }
        
        .mountain-mid {
            width: 0;
            height: 0;
            border-left: 180px solid transparent;
            border-right: 180px solid transparent;
            border-bottom: 200px solid #6b5b8c;
            position: absolute;
            bottom: 0;
            right: -30px;
        }
        
        .mountain-front {
            width: 0;
            height: 0;
            border-left: 150px solid transparent;
            border-right: 150px solid transparent;
            border-bottom: 180px solid #8b7ba8;
            position: absolute;
            bottom: 0;
            left: 100px;
        }
        
        .cloud {
            background: rgba(255, 255, 255, 0.4);
            border-radius: 100px;
            position: absolute;
            opacity: 0.7;
        }
        
        .cloud1 {
            width: 80px;
            height: 20px;
            top: 100px;
            left: 80px;
        }
        
        .cloud1::before {
            content: '';
            background: rgba(255, 255, 255, 0.4);
            width: 50px;
            height: 30px;
            border-radius: 50%;
            position: absolute;
            top: -15px;
            left: 15px;
        }
        
        .cloud2 {
            width: 100px;
            height: 25px;
            top: 150px;
            right: 60px;
        }
        
        .cloud2::before {
            content: '';
            background: rgba(255, 255, 255, 0.4);
            width: 60px;
            height: 35px;
            border-radius: 50%;
            position: absolute;
            top: -18px;
            right: 20px;
        }
        
        .star {
            background: white;
            position: absolute;
            border-radius: 50%;
            animation: twinkle 3s infinite;
        }
        
        @keyframes twinkle {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
        
        .star1 {
            width: 2px;
            height: 2px;
            top: 50px;
            left: 100px;
            animation-delay: 0s;
        }
        
        .star2 {
            width: 3px;
            height: 3px;
            top: 80px;
            right: 120px;
            animation-delay: 1s;
        }
        
        .star3 {
            width: 2px;
            height: 2px;
            top: 40px;
            right: 200px;
            animation-delay: 2s;
        }
        
        .star4 {
            width: 2px;
            height: 2px;
            top: 90px;
            left: 250px;
            animation-delay: 0.5s;
        }
    </style>
</head>
<body>
    <div class="canvas">
        <div class="star star1"></div>
        <div class="star star2"></div>
        <div class="star star3"></div>
        <div class="star star4"></div>
        <div class="cloud cloud1"></div>
        <div class="cloud cloud2"></div>
        <div class="sun"></div>
        <div class="mountain-back"></div>
        <div class="mountain-mid"></div>
        <div class="mountain-front"></div>
    </div>
</body>
</html>
```