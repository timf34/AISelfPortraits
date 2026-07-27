Sorry about that — my last reply got cut off mid-code. Here's the complete piece: a **moonlit mountain lake** with a crescent moon, twinkling stars, layered ridges, a cozy cabin with flickering window and rising chimney smoke, pine trees, a shimmering moon reflection on the water, drifting mist, fireflies, and an occasional shooting star. Pure HTML/CSS, 500×500.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moonlit Lake</title>
<style>
  html, body { margin: 0; padding: 0; background: #04050c; }

  .scene {
    position: relative;
    width: 500px;
    height: 500px;
    overflow: hidden;
    background: linear-gradient(to bottom,
      #070b1e 0%, #0e1434 28%, #252152 52%,
      #46325f 68%, #6b4a6d 78%, #3a2c55 88%, #1c1a3e 100%);
  }

  /* ---------- stars ---------- */
  .stars {
    position: absolute; top: 0; left: 0;
    width: 2px; height: 2px; border-radius: 50%;
    box-shadow:
      24px 46px 0 0 rgba(255,255,255,.8), 62px 132px 0 0 rgba(255,255,255,.5),
      41px 218px 0 0 rgba(255,255,255,.7), 88px 74px 0 1px rgba(255,255,255,.9),
      128px 32px 0 0 rgba(255,255,255,.6), 154px 158px 0 0 rgba(255,255,255,.8),
      182px 92px 0 0 rgba(255,255,255,.5), 214px 44px 0 0 rgba(255,255,255,.85),
      244px 196px 0 0 rgba(255,255,255,.6), 266px 124px 0 0 rgba(255,255,255,.75),
      304px 64px 0 0 rgba(255,255,255,.5), 334px 156px 0 0 rgba(255,255,255,.8),
      366px 34px 0 0 rgba(255,255,255,.6), 394px 206px 0 0 rgba(255,255,255,.7),
      458px 64px 0 0 rgba(255,255,255,.5), 484px 166px 0 0 rgba(255,255,255,.75),
      14px 292px 0 0 rgba(255,255,255,.5), 58px 262px 0 0 rgba(255,255,255,.65),
      104px 296px 0 0 rgba(255,255,255,.5), 142px 246px 0 0 rgba(255,255,255,.7),
      196px 282px 0 0 rgba(255,255,255,.55), 238px 238px 0 0 rgba(255,255,255,.6),
      286px 266px 0 0 rgba(255,255,255,.5), 322px 300px 0 0 rgba(255,255,255,.6),
      352px 244px 0 0 rgba(255,255,255,.55), 402px 288px 0 0 rgba(255,255,255,.5),
      446px 262px 0 0 rgba(255,255,255,.6), 478px 306px 0 0 rgba(255,255,255,.5),
      70px 180px 0 0 rgba(255,255,255,.6), 110px 110px 0 0 rgba(255,255,255,.7),
      160px 60px 0 0 rgba(255,255,255,.55), 200px 140px 0 0 rgba(255,255,255,.65),
      250px 80px 0 0 rgba(255,255,255,.5), 290px 170px 0 0 rgba(255,255,255,.6),
      320px 110px 0 0 rgba(255,255,255,.55), 360px 190px 0 0 rgba(255,255,255,.5),
      420px 140px 0 0 rgba(255,255,255,.6), 470px 100px 0 0 rgba(255,255,255,.55),
      30px 160px 0 0 rgba(255,255,255,.5), 90px 230px 0 0 rgba(255,255,255,.55),
      150px 200px 0 0 rgba(255,255,255,.5), 210px 250px 0 0 rgba(255,255,255,.55),
      260px 220px 0 0 rgba(255,255,255,.5), 310px 220px 0 0 rgba(255,255,255,.6),
      370px 250px 0 0 rgba(255,255,255,.5), 430px 230px 0 0 rgba(255,255,255,.55),
      490px 210px 0 0 rgba(255,255,255,.5), 45px 90px 0 0 rgba(255,255,255,.6),
      135px 270px 0 0 rgba(255,255,255,.5), 175px 180px 0 0 rgba(255,255,255,.55),
      225px 170px 0 0 rgba(255,255,255,.5), 275px 40px 0 0 rgba(255,255,255,.65),
      330px 20px 0 0 rgba(255,255,255,.55), 410px 40px 0 0 rgba(255,255,255,.6),
      455px 130px 0 0 rgba(255,255,255,.5);
  }

  .tw {
    position: absolute; width: 3px; height: 3px; border-radius: 50%;
    background: #fff; box-shadow: 0 0 6px 1px rgba(255,255,255,.8);
    animation: twinkle 3s ease-in-out infinite;
  }
  @keyframes twinkle {
    0%, 100% { opacity: .25; transform: scale(.8); }
    50%      { opacity: 1;   transform: scale(1.15); }
  }

  /* ---------- shooting star ---------- */
  .shoot {
    position: absolute; top: 60px; left: 110px;
    width: 90px; height: 2px; border-radius: 2px;
    background: linear-gradient(90deg, rgba(255,255,255,.95), transparent);
    opacity: 0; transform: rotate(-16deg);
    animation: shoot 9s linear infinite;
  }
  @keyframes shoot {
    0%   { opacity: 0; transform: translate(0,0) rotate(-16deg); }
    2%   { opacity: 1; }
    7%   { opacity: 0; transform: translate(150px,44px) rotate(-16deg); }
    100% { opacity: 0; transform: translate(150px,44px) rotate(-16deg); }
  }

  /* ---------- moon ---------- */
  .glow {
    position: absolute; left: 318px; top: 16px;
    width: 150px; height: 150px; border-radius: 50%;
    background: radial-gradient(circle,
      rgba(250,242,214,.30), rgba(250,242,214,.09) 45%, transparent 70%);
  }
  .moon {
    position: absolute; left: 352px; top: 50px;
    width: 76px; height: 76px; border-radius: 50%;
    box-shadow:
      inset 17px -10px 0 0 #f7f0dc,
      inset 17px -10px 12px 0 rgba(255,250,230,.6),
      0 0 34px 6px rgba(250,240,210,.28);
  }
  .moon::before { /* faint earthshine disk */
    content: ""; position: absolute; inset: 0; border-radius: 50%;
    background: rgba(190,195,225,.07);
  }

  /* ---------- clouds ---------- */
  .cloud {
    position: absolute; height: 14px; border-radius: 50%;
    background: rgba(200,200,225,.10); filter: blur(5px);
    animation: drift 34s ease-in-out infinite alternate;
  }
  @keyframes drift { from { transform: translateX(-14px); } to { transform: translateX(20px); } }

  /* ---------- mountains ---------- */
  .ridge { position: absolute; left: 0; width: 500px; }
  .ridge.back {
    top: 150px; height: 190px; opacity: .85;
    background: linear-gradient(#4a4283, #37315f);
    clip-path: polygon(0% 78%, 8% 55%, 16% 70%, 26% 38%, 34% 62%, 44% 30%,
      52% 58%, 60% 42%, 70% 66%, 80% 34%, 90% 60%, 100% 44%, 100% 100%, 0% 100%);
  }
  .ridge.mid {
    top: 210px; height: 130px;
    background: linear-gradient(#322c5e, #26224a);
    clip-path: polygon(0% 60%, 10% 30%, 20% 55%, 32% 22%, 42% 52%, 55% 28%,
      66% 58%, 78% 26%, 88% 52%, 100% 36%, 100% 100%, 0% 100%);
  }
  .ridge.front {
    top: 262px; height: 68px; background: #1d1b3c;
    clip-path: polygon(0% 45%, 15% 20%, 30% 42%, 45% 18%, 60% 40%,
      75% 15%, 90% 38%, 100% 22%, 100% 100%, 0% 100%);
  }

  /* ---------- lake ---------- */
  .lake {
    position: absolute; top: 330px; left: 0;
    width: 500px; height: 170px;
    background:
      repeating-linear-gradient(to bottom,
        rgba(255,255,255,.028) 0 1px, transparent 1px 7px),
      linear-gradient(#28204e, #141130 55%, #0b0a20);
  }
  .lake::before { /* warm glint along the waterline */
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,205,160,.28), transparent);
  }
  .mref { /* blurred mountain reflection */
    position: absolute; top: 0; left: 0; width: 500px; height: 92px;
    background: #171434; opacity: .55; filter: blur(1.5px);
    clip-path: polygon(0% 0%, 0% 40%, 10% 70%, 20% 45%, 32% 78%, 42% 48%,
      55% 72%, 66% 42%, 78% 74%, 88% 48%, 100% 64%, 100% 0%);
    -webkit-mask-image: linear-gradient(to bottom, #000, transparent);
    mask-image: linear-gradient(to bottom, #000, transparent);
  }

  /* moon reflection: shimmering bars */
  .moonref { position: absolute; top: 4px; left: 355px; width: 70px; }
  .mbar {
    height: 3px; margin: 6px auto 0; border-radius: 2px;
    background: rgba(246,238,214,.55); filter: blur(.6px);
    animation: shimmer 3.2s ease-in-out infinite;
  }
  @keyframes shimmer {
    0%, 100% { opacity: .25; transform: translateX(-3px) scaleX(.85); }
    50%      { opacity: .7;  transform: translateX(3px)  scaleX(1.1); }
  }

  /* cabin window reflection */
  .winref {
    position: absolute; top: 2px; left: 91px; width: 14px; height: 62px;
    background: linear-gradient(rgba(255,180,90,.5), rgba(255,180,90,0));
    filter: blur(2px); border-radius: 4px;
    animation: winflicker 4s ease-in-out infinite;
  }

  /* ---------- cabin ---------- */
  .cabin { position: absolute; left: 64px; top: 264px; width: 104px; height: 64px; }
  .chimney {
    position: absolute; left: 76px; top: -12px; width: 10px; height: 26px;
    background: #3a2a24; border-radius: 1px;
  }
  .smoke span {
    position: absolute; left: 77px; top: -16px; width: 8px; height: 8px;
    border-radius: 50%; background: rgba(220,220,235,.5); filter: blur(3px);
    opacity: 0; animation: rise 6s linear infinite;
  }
  .smoke span:nth-child(2) { animation-delay: 2s; }
  .smoke span:nth-child(3) { animation-delay: 4s; }
  @keyframes rise {
    0%   { opacity: 0;  transform: translate(0,0) scale(.6); }
    15%  { opacity: .5; }
    100% { opacity: 0;  transform: translate(-16px,-72px) scale(1.8); }
  }
  .roof {
    position: absolute; top: 0; left: -10px; width: 124px; height: 30px;
    background: linear-gradient(#2c2136, #1d1526);
    clip-path: polygon(50% 0, 100% 100%, 0 100%);
  }
  .cbody {
    position: absolute; top: 26px; left: 10px; width: 84px; height: 38px;
    background:
      repeating-linear-gradient(to bottom, #4a3226 0 6px, #35241b 6px 7px);
    border-radius: 2px;
    box-shadow: inset -14px 0 18px rgba(0,0,0,.45), inset 0 -8px 12px rgba(0,0,0,.4);
  }
  .win {
    position: absolute; left: 14px; top: 8px; width: 20px; height: 18px;
    background: radial-gradient(circle at 50% 45%, #ffe9ad, #ffb85c 75%);
    border-radius: 2px;
    box-shadow: 0 0 14px 4px rgba(255,180,90,.45);
    animation: winflicker 4s ease-in-out infinite;
  }
  .win::before, .win::after { content: ""; position: absolute; background: #2b1c14; }
  .win::before { left: 9px; top: 0; width: 2px; height: 100%; }
  .win::after  { top: 8px; left: 0; height: 2px; width: 100%; }
  @keyframes winflicker {
    0%, 100% { opacity: 1; }
    42%      { opacity: .82; }
    58%      { opacity: .95; }
    74%      { opacity: .78; }
  }
  .door {
    position: absolute; left: 52px; top: 12px; width: 16px; height: 26px;
    background: #2b1c14; border-radius: 3px 3px 0 0;
    box-shadow: inset 0 0 6px rgba(0,0,0,.6);
  }

  /* ---------- pines ---------- */
  .pine {
    position: absolute;
    clip-path: polygon(50% 0%, 60% 12%, 55% 12%, 68% 26%, 61% 26%, 76% 42%,
      66% 42%, 84% 60%, 70% 60%, 90% 78%, 58% 78%, 58% 92%, 54% 92%, 54% 100%,
      46% 100%, 46% 92%, 42% 92%, 42% 78%, 10% 78%, 30% 60%, 16% 60%, 34% 42%,
      24% 42%, 39% 26%, 32% 26%, 45% 12%, 40% 12%);
  }

  /* ---------- mist ---------- */
  .mist {
    position: absolute; width: 260px; height: 34px; border-radius: 50%;
    background: radial-gradient(ellipse, rgba(205,205,235,.14), transparent 70%);
    filter: blur(6px);
    animation: drift 26s ease-in-out infinite alternate;
  }

  /* ---------- fireflies ---------- */
  .ff {
    position: absolute; width: 4px; height: 4px; border-radius: 50%;
    background: #ffe9a0; box-shadow: 0 0 8px 3px rgba(255,220,130,.55);
    animation: fly 7s ease-in-out infinite, blink 2.8s ease-in-out infinite;
  }
  @keyframes fly {
    0%, 100% { transform: translate(0,0); }
    25%      { transform: translate(9px,-11px); }
    50%      { transform: translate(1px,-19px); }
    75%      { transform: translate(-9px,-8px); }
  }
  @keyframes blink { 0%, 100% { opacity: .1; } 50% { opacity: 1; } }

  /* ---------- shore & vignette ---------- */
  .shore {
    position: absolute; bottom: 0; left: 0; width: 500px; height: 26px;
    background: linear-gradient(#0d0c22, #070614);
  }
  .rock { position: absolute; border-radius: 50%; background: #181731; }
  .vig {
    position: absolute; inset: 0; pointer-events: none;
    box-shadow: inset 0 0 90px 30px rgba(2,2,10,.55);
  }
</style>
</head>
<body>
  <div class="scene">
    <div class="stars"></div>

    <!-- twinkling stars -->
    <span class="tw" style="top:38px;  left:70px;  animation-delay:.2s"></span>
    <span class="tw" style="top:90px;  left:170px; animation-delay:1.1s"></span>
    <span class="tw" style="top:55px;  left:240px; animation-delay:2s"></span>
    <span class="tw" style="top:140px; left:290px; animation-delay:.6s"></span>
    <span class="tw" style="top:30px;  left:440px; animation-delay:1.6s"></span>
    <span class="tw" style="top:200px; left:120px; animation-delay:2.5s"></span>
    <span class="tw" style="top:230px; left:350px; animation-delay:.9s"></span>
    <span class="tw" style="top:170px; left:30px;  animation-delay:1.9s"></span>

    <div class="shoot"></div>

    <div class="glow"></div>
    <div class="moon"></div>

    <div class="cloud" style="top:70px;  left:280px; width:150px;"></div>
    <div class="cloud" style="top:120px; left:340px; width:110px; animation-duration:42s;"></div>

    <div class="ridge back"></div>
    <div class="ridge mid"></div>
    <div class="ridge front"></div>

    <div class="lake">
      <div class="mref"></div>
      <div class="moonref">
        <div class="mbar" style="width:46px; animation-delay:0s"></div>
        <div class="mbar" style="width:34px; animation-delay:.4s"></div>
        <div class="mbar" style="width:52px; animation-delay:.8s"></div>
        <div class="mbar" style="width:28px; animation-delay:1.2s"></div>
        <div class="mbar" style="width:40px; animation-delay:1.6s"></div>
        <div class="mbar" style="width:22px; animation-delay:2s"></div>
        <div class="mbar" style="width:32px; animation-delay:2.4s"></div>
        <div class="mbar" style="width:16px; animation-delay:2.8s"></div>
        <div class="mbar" style="width:24px; animation-delay:1s"></div>
        <div class="mbar" style="width:12px; animation-delay:2.2s"></div>
      </div>
      <div class="winref"></div>
    </div>

    <div class="cabin">
      <div class="chimney"></div>
      <div class="smoke"><span></span><span></span><span></span></div>
      <div class="roof"></div>
      <div class="cbody">
        <div class="win"></div>
        <div class="door"></div>
      </div>
    </div>

    <!-- pines -->
    <div class="pine" style="left:8px;   top:250px; width:60px; height:86px; background:#151632;"></div>
    <div class="pine" style="left:36px;  top:268px; width:44px; height:64px; background:#191a3a;"></div>
    <div class="pine" style="left:182px; top:288px; width:36px; height:44px; background:#141530;"></div>
    <div class="pine" style="left:414px; top:266px; width:48px; height:66px; background:#171838;"></div>
    <div class="pine" style="left:450px; top:236px; width:66px; height:96px; background:#12132c;"></div>
    <div class="pine" style="left:482px; top:262px; width:40px; height:70px; background:#0f1026;"></div>

    <div class="mist" style="top:300px; left:40px;"></div>
    <div class="mist" style="top:316px; left:220px; animation-duration:32s; animation-delay:-8s;"></div>

    <span class="ff" style="top:296px; left:196px;"></span>
    <span class="ff" style="top:300px; left:48px;  animation-delay:1.3s, .7s;"></span>
    <span class="ff" style="top:318px; left:150px; animation-delay:2.4s, 1.6s;"></span>

    <div class="shore"></div>
    <div class="rock" style="bottom:14px; left:60px;  width:26px; height:12px;"></div>
    <div class="rock" style="bottom:12px; left:84px;  width:16px; height:9px; background:#141329;"></div>
    <div class="rock" style="bottom:13px; left:400px; width:30px; height:13px;"></div>

    <div class="vig"></div>
  </div>
</body>
</html>
```

A few notes on the techniques: the crescent moon is a single circle carved by an inset box-shadow; the ~55 static stars are all box-shadows of one 2px dot; the mountain ridges and pines are `clip-path` polygons; and the moon's reflection is a stack of bars with staggered `shimmer` animations so the light appears to dance on the ripples.