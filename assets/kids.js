/* Kid-level animated explainer (ko / en / zh). Text comes from data/medfl-data.js; the scene is a sketch with no experimental numbers.
   ?kids=5 opens step 5 directly, handy for presenters. */
(function () {
  'use strict';
  var SVGNS = 'http://www.w3.org/2000/svg';
  var X = [70, 186, 302, 418, 534, 650];
  var COMMON = [9, 10, 8, 10, 7, 9], RARE = [1, 1, 0, 1, 0, 1];

  function el(name, attrs, parent, text) {
    var e = document.createElementNS(SVGNS, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function diamond(cx, cy, size, attrs, parent) {
    var h = size / 2;
    attrs.d = 'M' + cx + ' ' + (cy - h) + 'L' + (cx + h) + ' ' + cy + 'L' + cx + ' ' + (cy + h) + 'L' + (cx - h) + ' ' + cy + 'Z';
    return el('path', attrs, parent);
  }

  function drawScene(svg, t) {
    var legend = el('g', { 'data-show': 's0' }, svg);
    el('rect', { x: 150, y: 22, width: 420, height: 92, rx: 14, fill: '#fff', stroke: '#9fb8aa', 'stroke-width': 2 }, legend);
    el('circle', { cx: 180, cy: 52, r: 9, fill: '#9a6a3c' }, legend);
    el('text', { x: 200, y: 58, 'font-size': 17, fill: '#152e32' }, legend, t.legend[0].replace(/^● /, ''));
    diamond(180, 88, 20, { fill: '#7b4fa6' }, legend);
    el('text', { x: 200, y: 94, 'font-size': 17, fill: '#152e32' }, legend, t.legend[1].replace(/^◆ /, ''));

    var server = el('g', { 'class': 'server', 'data-show': 's2 s3 s4 s5' }, svg);
    el('rect', { 'class': 'glow', x: 262, y: 14, width: 196, height: 84, rx: 18, fill: 'none', stroke: '#e09b35', 'stroke-width': 6 }, server);
    el('rect', { x: 268, y: 20, width: 184, height: 72, rx: 14, fill: '#173e40' }, server);
    el('text', { x: 360, y: 62, 'text-anchor': 'middle', fill: '#fff', 'font-size': 17, 'font-weight': 700 }, server, t.server);

    var fence = el('g', { 'data-show': 's1' }, svg);
    el('rect', { x: 10, y: 224, width: 700, height: 140, rx: 16, fill: 'none', stroke: '#e09b35', 'stroke-width': 3, 'stroke-dasharray': '9 7' }, fence);
    el('text', { x: 360, y: 214, 'text-anchor': 'middle', 'font-size': 16, 'font-weight': 700, fill: '#9a5b12' }, fence, t.stay);

    X.forEach(function (cx, i) {
      var b = el('g', { 'class': 'box' }, svg);
      el('rect', { x: cx - 50, y: 236, width: 100, height: 96, rx: 10, fill: '#fafbf8', stroke: '#9fb8aa', 'stroke-width': 2 }, b);
      el('text', { x: cx, y: 354, 'text-anchor': 'middle', 'font-size': 14, 'font-weight': 700, fill: '#173e40' }, b, t.box + ' ' + (i + 1));
      var n = 0, total = COMMON[i] + RARE[i];
      for (var r = 0; r < 3; r++) for (var c = 0; c < 4; c++) {
        if (n >= total) continue;
        var px = cx - 36 + c * 24, py = 258 + r * 26;
        if (n >= COMMON[i]) diamond(px, py, 18, { fill: '#7b4fa6', 'class': 'rare-dot' }, b);
        else el('circle', { cx: px, cy: py, r: 8, fill: '#9a6a3c' }, b);
        n++;
      }
      var note = el('g', { 'class': 'note n' + (i % 3), style: '--dx:' + (360 - cx) + 'px;--dy:-132px' }, svg);
      el('rect', { x: cx - 14, y: 192, width: 28, height: 36, rx: 3, fill: '#fffdf4', stroke: '#9a8a5a', 'stroke-width': 1.5 }, note);
      for (var l = 0; l < 3; l++) el('line', { x1: cx - 8, y1: 202 + l * 8, x2: cx + 8, y2: 202 + l * 8, stroke: '#9a8a5a', 'stroke-width': 1.5 }, note);
    });

    var robot = el('g', { 'class': 'robot', 'data-show': 's2 s3 s4 s5' }, svg);
    el('line', { x1: 32, y1: 0, x2: 32, y2: 10, stroke: '#173e40', 'stroke-width': 3 }, robot);
    el('circle', { cx: 32, cy: 0, r: 4, fill: '#e09b35' }, robot);
    el('rect', { x: 12, y: 10, width: 40, height: 30, rx: 9, fill: '#5f9f8c' }, robot);
    el('circle', { cx: 24, cy: 24, r: 4, fill: '#fff' }, robot);
    el('circle', { cx: 40, cy: 24, r: 4, fill: '#fff' }, robot);
    el('rect', { x: 18, y: 42, width: 28, height: 20, rx: 6, fill: '#3f7f6d' }, robot);

    var fog = el('g', { 'class': 'fog', 'data-show': 's4 s5' }, svg);
    [[120, 150, 34], [220, 120, 30], [330, 150, 38], [440, 125, 30], [560, 150, 36], [660, 175, 26], [60, 185, 24], [400, 180, 26], [280, 185, 24]].forEach(function (p) {
      el('circle', { cx: p[0], cy: p[1], r: p[2], fill: '#ffffff', opacity: 0.62 }, fog);
    });

    var mem = el('g', { 'data-show': 's5' }, svg);
    el('rect', { x: 470, y: 10, width: 240, height: 124, rx: 12, fill: '#fff', stroke: '#9fb8aa', 'stroke-width': 2 }, mem);
    el('text', { x: 486, y: 36, 'font-size': 15, 'font-weight': 700, fill: '#173e40' }, mem, t.memory);
    el('circle', { cx: 494, cy: 62, r: 8, fill: '#9a6a3c' }, mem);
    el('text', { x: 510, y: 67, 'font-size': 14, fill: '#152e32' }, mem, t.commonOk);
    diamond(494, 92, 18, { fill: '#7b4fa6', opacity: 0.3 }, mem);
    el('text', { x: 510, y: 97, 'font-size': 14, fill: '#152e32' }, mem, t.rareLost);
    el('text', { x: 486, y: 123, 'font-size': 12, fill: '#60766e' }, mem, t.illus);

    var fin = el('g', { 'data-show': 's6' }, svg);
    el('rect', { x: 150, y: 12, width: 420, height: 176, rx: 12, fill: '#fff', stroke: '#9fb8aa', 'stroke-width': 2 }, fin);
    el('text', { x: 170, y: 42, 'font-size': 17, 'font-weight': 700, fill: '#173e40' }, fin, t.tryT);
    t.tries.forEach(function (s, i) {
      el('rect', { x: 170, y: 56 + i * 34, width: 380, height: 26, rx: 13, fill: '#e6f2ec', stroke: '#7fb3a3' }, fin);
      el('text', { x: 184, y: 74 + i * 34, 'font-size': 14, fill: '#152e32' }, fin, s);
    });
    el('text', { x: 170, y: 176, 'font-size': 14, 'font-weight': 700, fill: '#8a4b0f' }, fin, t.checking);
  }

  function build(root) {
    var D = window.MEDFL_DATA;
    if (!D || !D.i18n) return;
    var lang = (document.documentElement.lang || 'ko').slice(0, 2);
    var t = (D.i18n[lang] || D.i18n.ko).kids;
    root.innerHTML = '';
    var stage = document.createElement('div');
    stage.className = 'kids-stage s0';
    stage.setAttribute('role', 'img');
    var svg = el('svg', { viewBox: '0 0 720 380', 'aria-hidden': 'true', focusable: 'false' });
    stage.appendChild(svg);
    drawScene(svg, t);
    var cap = document.createElement('p');
    cap.className = 'kids-caption';
    cap.setAttribute('aria-live', 'polite');
    var controls = document.createElement('div');
    controls.className = 'kids-controls';
    function button(label, cls) { var b = document.createElement('button'); b.type = 'button'; b.textContent = label; if (cls) b.className = cls; controls.appendChild(b); return b; }
    var prev = button(t.prev), play = button(t.play, 'primary'), next = button(t.next);
    var dots = document.createElement('div');
    dots.className = 'kids-dots';
    controls.appendChild(dots);
    var step = 0, timer = null, N = t.steps.length;
    var dotButtons = t.steps.map(function (s, i) {
      var d = document.createElement('button');
      d.type = 'button'; d.className = 'kids-dot';
      d.setAttribute('aria-label', t.stepOf + ' ' + (i + 1) + ': ' + s[0]);
      d.addEventListener('click', function () { stop(); go(i); });
      dots.appendChild(d);
      return d;
    });
    function go(i) {
      step = Math.max(0, Math.min(N - 1, i));
      stage.className = 'kids-stage s' + step;
      stage.setAttribute('aria-label', t.stage + ' — ' + t.steps[step][1]);
      cap.innerHTML = '';
      var b = document.createElement('b');
      b.textContent = (step + 1) + ' / ' + N + ' · ' + t.steps[step][0];
      cap.appendChild(b);
      cap.appendChild(document.createTextNode(t.steps[step][1]));
      dotButtons.forEach(function (d, k) { if (k === step) d.setAttribute('aria-current', 'step'); else d.removeAttribute('aria-current'); });
      prev.disabled = step === 0;
      next.disabled = step === N - 1;
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } play.textContent = t.play; }
    function start() {
      if (step === N - 1) go(0);
      play.textContent = t.pause;
      timer = setInterval(function () { if (step >= N - 1) { stop(); return; } go(step + 1); }, 5600);
    }
    play.addEventListener('click', function () { if (timer) stop(); else start(); });
    prev.addEventListener('click', function () { stop(); go(step - 1); });
    next.addEventListener('click', function () { stop(); go(step + 1); });
    root.appendChild(stage); root.appendChild(cap); root.appendChild(controls);
    var first = parseInt(new URLSearchParams(location.search).get('kids'), 10);
    go(isNaN(first) ? 0 : first - 1);
  }

  function init() { Array.prototype.forEach.call(document.querySelectorAll('.kids'), build); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
