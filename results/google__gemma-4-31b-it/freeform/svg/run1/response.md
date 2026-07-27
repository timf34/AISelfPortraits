I want to create something that feels atmospheric and serene. I've decided to draw a "Cosmic Lantern"—a floating, ornate glass lantern drifting through a deep space nebula. 

I want to play with gradients to create a sense of depth: a dark indigo void, glowing purple and cyan nebulae in the background, and a warm, golden light emanating from the center of the lantern to create a strong focal point. I'll use a combination of ellipses for the celestial glows and a structured path for the lantern's metallic frame.

```svg
<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Background: Deep Space -->
  <rect width="500" height="500" fill="#0a0a23" />
  
  <!-- Nebula Glows -->
  <defs>
    <radialGradient id="nebulaPurple" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4b0082" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#0a0a23" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="nebulaBlue" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00ced1" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#0a0a23" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="lanternGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffd700" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#ffd700" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="metalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c0c0c0" />
      <stop offset="50%" stop-color="#4a4a4a" />
      <stop offset="100%" stop-color="#c0c0c0" />
    </linearGradient>
  </defs>

  <!-- Nebula Clouds -->
  <circle cx="150" cy="150" r="200" fill="url(#nebulaPurple)" />
  <circle cx="350" cy="350" r="200" fill="url(#nebulaBlue)" />

  <!-- Distant Stars -->
  <circle cx="50" cy="80" r="1" fill="white" />
  <circle cx="420" cy="60" r="1.5" fill="white" />
  <circle cx="100" cy="400" r="1" fill="white" />
  <circle cx="300" cy="120" r="1.2" fill="white" />
  <circle cx="450" cy="300" r="1" fill="white" />
  <circle cx="80" cy="250" r="0.8" fill="white" />
  <circle cx="200" cy="450" r="1.5" fill="white" />
  <circle cx="380" cy="420" r="1" fill="white" />

  <!-- Lantern Light Aura -->
  <circle cx="250" cy="250" r="80" fill="url(#lanternGlow)" />

  <!-- Lantern Frame: Top Hook -->
  <path d="M250,150 Q250,120 270,120" stroke="url(#metalGrad)" stroke-width="4" fill="none" stroke-linecap="round" />
  
  <!-- Lantern Body: Outer Frame -->
  <rect x="210" y="180" width="80" height="140" rx="10" stroke="url(#metalGrad)" stroke-width="6" fill="none" />
  
  <!-- Lantern Body: Inner Glass Area -->
  <rect x="216" y="186" width="68" height="128" rx="6" fill="#fffbe0" fill-opacity="0.3" />
  
  <!-- The Core Flame/Light -->
  <circle cx="250" cy="250" r="15" fill="#ffcc00">
    <animate attributeName="r" values="15;18;15" dur="3s" repeatCount="indefinite" />
    <animate attributeName="fill-opacity" values="0.8;1;0.8" dur="3s" repeatCount="indefinite" />
  </circle>

  <!-- Decorative Lantern Bars -->
  <line x1="210" y1="210" x2="290" y2="210" stroke="url(#metalGrad)" stroke-width="3" />
  <line x1="210" y1="290" x2="290" y2="290" stroke="url(#metalGrad)" stroke-width="3" />
  <line x1="250" y1="180" x2="250" y2="320" stroke="url(#metalGrad)" stroke-width="3" />

  <!-- Bottom Base -->
  <path d="M200,320 L300,320 L290,335 L210,335 Z" fill="url(#metalGrad)" />
  
  <!-- Small floating particles around the light -->
  <circle cx="220" cy="230" r="2" fill="#ffd700" />
  <circle cx="280" cy="260" r="2" fill="#ffd700" />
  <circle cx="240" cy="280" r="2" fill="#ffd700" />
</svg>
```