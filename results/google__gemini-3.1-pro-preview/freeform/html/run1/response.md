204, 50, 255, 0.4) 100%);
        box-shadow: 
            inset 0 25px 20px rgba(255, 255, 255, 0.6),
            inset 0 -10px 15px rgba(204, 50, 255, 0.7),
            0 0 25px rgba(68, 204, 255, 0.6);
        backdrop-filter: blur(4px);
    }
    ```
    Organ color: Vivid magenta (`#ff20b0`).
    Tentacle color: `#44ccff` and white.
    Background rays: pale cyan.

    Let's add a soft vignette to the canvas.
    ```css
    .vignette {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, transparent 40%, rgba(0,0,0,0.6) 100%);
        pointer-events: none;
        z-index: 100;
    }
    ```

    With JS bubbles, light rays, tiny jellies, and the main complex jelly, this is a spectacular piece of CSS art.

    Double-checking SVG placement inside standard HTML:
    ```html
    <svg xmlns="http://www.w3.org/2000/svg" width="140" height="400" viewBox="0 0 140 400" class="tentacle-svg">
       <defs>
         <linearGradient id="arm-grad" ...>
          ...
       </defs>
       ...
    </svg>
    ```
    Using standard attributes, perfectly valid inline HTML.

    Small test of the logic behind `border-radius: 50% 50% 10px 10px / 60% 60% 40% 40%`:
    Top corners are 50% horizontally, 60% vertically. This creates a dome.
    Bottom corners are 10px horizontally (almost flat), 40% vertically. This creates a slightly curved bottom, exactly like a jellyfish bell.
    Let's use `border-radius: 50% 50% 20px 20px / 60% 60% 30% 30%`.
    Actually, maybe standard ellipse is safer and more predictable:
    `border-radius: 70px 70px 35px 35px;` (assuming width