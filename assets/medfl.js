/* Shared MedFL components (homepages + explain.html). Text comes from data/medfl-data.js (window.MEDFL_DATA). */
(function () {
  'use strict';
  var D = window.MEDFL_DATA || {};
  var doc = document.documentElement;
  doc.classList.add('js');
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function lang() { var l = (doc.getAttribute('lang') || 'ko').slice(0, 2); return D.i18n && D.i18n[l] ? l : 'ko'; }
  function svg(tag, attrs, parent, text) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function html(tag, cls, parent, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  // pause CSS animations while a widget is off screen (saves CPU on long pages)
  function watch(el, root) {
    if (el._io) el._io.disconnect();
    if (!('IntersectionObserver' in window)) return;
    el._io = new IntersectionObserver(function (es) { es.forEach(function (e) { root.classList.toggle('is-off', !e.isIntersecting); }); });
    el._io.observe(el);
  }

  /* ---- one federated round with six clients: images never move; only parameters / protected updates travel ---- */
  var CL = [[10, 16], [250, 16], [490, 16], [10, 300], [250, 300], [490, 300]];
  var SX = [310, 360, 410];
  function round(mount, l) {
    if (!mount || !D.i18n) return;
    var t = D.i18n[l || lang()].round;
    if (mount._timer) { clearInterval(mount._timer); mount._timer = null; }
    var step = +(mount.getAttribute('data-step') || 0), p2 = mount.getAttribute('data-p2') === '1';
    mount.innerHTML = '';
    mount.classList.add('flr');
    html('p', 'flr-tag', mount, t.tag);
    var stage = html('div', 'flr-stage', mount);
    var s = svg('svg', { viewBox: '0 0 720 400', role: 'img', 'aria-label': t.aria }, stage);
    var defs = svg('defs', {}, s);
    [['flr-m-down', '#2f6f5f'], ['flr-m-up', '#c9661c'], ['flr-m-p2', '#7b4fa6']].forEach(function (m) {
      var mk = svg('marker', { id: m[0], viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto' }, defs);
      svg('path', { d: 'M0 0L10 5L0 10z', fill: m[1] }, mk);
    });
    var down = svg('g', { 'class': 'flr-down' }, s), up = svg('g', { 'class': 'flr-up' }, s), st = svg('g', { 'class': 'flr-p2' }, s);
    var toks = svg('g', { 'class': 'flr-toks' }, s);
    CL.forEach(function (c, i) {
      var cx = c[0] + 110, top = i < 3, cy = top ? 100 : 300, sx = SX[i % 3], sy = top ? 158 : 242;
      svg('line', { x1: sx, y1: sy, x2: cx, y2: cy, 'marker-end': 'url(#flr-m-down)' }, down);
      svg('line', { x1: cx, y1: cy, x2: sx, y2: sy, 'marker-end': 'url(#flr-m-up)' }, up);
      svg('line', { x1: cx + 18, y1: cy, x2: sx + 18, y2: sy, 'marker-end': 'url(#flr-m-p2)' }, st);
      // travelling tokens: model card (down), sealed update (up), noisy class statistics (P2, once)
      var a = svg('g', { 'class': 'flr-tok flr-tok-down', style: '--x0:' + sx + 'px;--y0:' + sy + 'px;--x1:' + cx + 'px;--y1:' + cy + 'px;--i:' + i }, toks);
      svg('rect', { x: -10, y: -7, width: 20, height: 14, rx: 3 }, a);
      [-3, 0, 3].forEach(function (y) { svg('line', { x1: -6, y1: y, x2: 6, y2: y }, a); });
      var b = svg('g', { 'class': 'flr-tok flr-tok-up', style: '--x0:' + cx + 'px;--y0:' + cy + 'px;--x1:' + sx + 'px;--y1:' + sy + 'px;--i:' + i }, toks);
      svg('rect', { x: -10, y: -7, width: 20, height: 14, rx: 3 }, b);
      svg('path', { d: 'M-10 -6L0 2L10 -6' }, b);
      var q = svg('g', { 'class': 'flr-tok flr-tok-p2', style: '--x0:' + (cx + 18) + 'px;--y0:' + cy + 'px;--x1:' + (sx + 18) + 'px;--y1:' + sy + 'px;--i:' + i }, toks);
      svg('path', { d: 'M0 -8L8 0L0 8L-8 0Z' }, q);
    });
    var srv = svg('g', { 'class': 'flr-server' }, s);
    svg('rect', { 'class': 'flr-ripple', x: 250, y: 158, width: 220, height: 84, rx: 14 }, srv);
    svg('rect', { 'class': 'flr-glow', x: 244, y: 152, width: 232, height: 96, rx: 18 }, srv);
    svg('rect', { 'class': 'flr-core', x: 250, y: 158, width: 220, height: 84, rx: 14 }, srv);
    var model = svg('g', { 'class': 'flr-model' }, srv);
    [0, 1, 2].forEach(function (k) { svg('rect', { x: 266 + k * 4, y: 170 + k * 5, width: 22, height: 15, rx: 3 }, model); });
    svg('text', { x: 360, y: 192, 'text-anchor': 'middle', 'class': 'flr-t1' }, srv, t.server);
    svg('text', { x: 360, y: 214, 'text-anchor': 'middle', 'class': 'flr-agg' }, srv, t.agg);
    svg('text', { x: 360, y: 232, 'text-anchor': 'middle', 'class': 'flr-agg2' }, srv, t.agg2);
    svg('text', { x: 240, y: 186, 'text-anchor': 'end', 'class': 'flr-lab flr-lab-down' }, s, t.down);
    svg('text', { x: 240, y: 186, 'text-anchor': 'end', 'class': 'flr-lab flr-lab-up' }, s, t.up);
    svg('text', { x: 240, y: 212, 'text-anchor': 'end', 'class': 'flr-lab flr-lab-p2' }, s, t.stats);
    CL.forEach(function (c, i) {
      var g = svg('g', { 'class': 'flr-client', style: '--i:' + i }, s), x = c[0], y = c[1];
      svg('rect', { 'class': 'flr-shadow', x: x + 2, y: y + 3, width: 220, height: 84, rx: 12 }, g);
      svg('rect', { 'class': 'flr-box', x: x, y: y, width: 220, height: 84, rx: 12 }, g);
      svg('text', { x: x + 12, y: y + 22, 'class': 'flr-t2' }, g, t.client + ' ' + (i + 1));
      svg('text', { x: x + 12, y: y + 40, 'class': 'flr-t3' }, g, '▣ ' + t.local);
      svg('rect', { x: x + 176, y: y + 8, width: 30, height: 24, rx: 3, fill: '#e9d6c3', stroke: '#9a7b5f' }, g);
      svg('rect', { x: x + 170, y: y + 13, width: 30, height: 24, rx: 3, fill: '#f4e7d9', stroke: '#9a7b5f' }, g);
      svg('circle', { 'class': 'flr-lesion', cx: x + 185, cy: y + 25, r: 6, fill: '#8a5a3c' }, g);
      var dp = svg('g', { 'class': 'flr-dp' }, g);
      svg('rect', { x: x + 8, y: y + 48, width: 204, height: 22, rx: 6 }, dp);
      svg('text', { x: x + 16, y: y + 63, 'class': 'flr-t4' }, dp, t.dp1 + ' · ' + t.dp2);
      [[196, 54], [203, 60], [197, 65]].forEach(function (p, k) { svg('circle', { 'class': 'flr-spark', cx: x + p[0], cy: y + p[1], r: 1.8, style: '--k:' + k }, dp); });
      var pg = svg('g', { 'class': 'flr-prog' }, g);
      svg('rect', { x: x + 8, y: y + 75, width: 204, height: 4, rx: 2, fill: '#dfe9e3' }, pg);
      svg('rect', { 'class': 'flr-prog-fill', x: x + 8, y: y + 75, width: 204, height: 4, rx: 2 }, pg);
    });
    var meter = html('div', 'flr-meter', mount); meter.setAttribute('aria-hidden', 'true');
    var fill = html('span', '', meter);
    var cap = html('div', 'flr-cap', mount);
    cap.setAttribute('role', 'status'); cap.setAttribute('aria-live', 'polite');
    var bar = html('div', 'flr-controls', mount);
    var stepBtns = t.steps.map(function (name, i) {
      var b = html('button', 'flr-step', bar, (i + 1) + '. ' + name);
      b.type = 'button';
      b.addEventListener('click', function () { stop(); go(i); });
      b.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!k) return;
        e.preventDefault(); stop(); go(step + k); stepBtns[step].focus();
      });
      return b;
    });
    var bar2 = html('div', 'flr-controls', mount);
    var prev = html('button', '', bar2, t.prev), play = html('button', 'primary', bar2, t.play), next = html('button', '', bar2, t.next);
    [prev, play, next].forEach(function (b) { b.type = 'button'; });
    var lab = html('label', 'flr-p2toggle', bar2), box = html('input', '', lab);
    box.type = 'checkbox'; box.checked = p2;
    lab.appendChild(document.createTextNode(' ' + t.p2));
    function go(i) {
      step = Math.max(0, Math.min(3, i));
      mount.setAttribute('data-step', step);
      stage.className = 'flr-stage st' + (step + 1) + (p2 ? ' p2' : '');
      fill.style.width = (step + 1) * 25 + '%';
      cap.innerHTML = '';
      html('b', '', cap, (step + 1) + '. ' + t.titles[step]);
      html('span', '', cap, t.copies[step]);
      cap.classList.remove('flr-in'); void cap.offsetWidth; cap.classList.add('flr-in');
      stepBtns.forEach(function (b, k) { b.setAttribute('aria-pressed', k === step ? 'true' : 'false'); });
      prev.disabled = step === 0; next.disabled = step === 3;
    }
    function stop() { if (mount._timer) { clearInterval(mount._timer); mount._timer = null; } play.textContent = t.play; }
    play.addEventListener('click', function () {
      if (mount._timer) { stop(); return; }
      if (step === 3) go(0);
      play.textContent = t.pause;
      mount._timer = setInterval(function () { if (step >= 3) { stop(); return; } go(step + 1); }, reduce ? 6000 : 4200);
    });
    prev.addEventListener('click', function () { stop(); go(step - 1); });
    next.addEventListener('click', function () { stop(); go(step + 1); });
    box.addEventListener('change', function () {
      p2 = box.checked; mount.setAttribute('data-p2', p2 ? '1' : '0');
      if (p2 && step < 2) { stop(); go(2); } else go(step);
    });
    watch(stage, mount);
    go(step);
  }

  /* ---- concept noise slider (from explain.html): a visual overlay only, no DP, no model, no real ε ---- */
  function noise(mount, l) {
    if (!mount || !D.i18n) return;
    var t = D.i18n[l || lang()].noise, v = +(mount.getAttribute('data-v') || 40);
    var id = 'nz-' + Math.random().toString(36).slice(2, 7);
    mount.innerHTML = '';
    mount.classList.add('nz');
    html('p', 'nz-tag', mount, t.tag);
    var lab = html('label', 'nz-label', mount, t.label); lab.setAttribute('for', id);
    var row = html('div', 'nz-row', mount);
    html('span', '', row, t.low);
    var r = html('input', '', row); r.type = 'range'; r.min = 0; r.max = 100; r.step = 5; r.value = v; r.id = id;
    html('span', '', row, t.high);
    var out = html('output', '', row); out.setAttribute('for', id);
    var sig = html('div', 'nz-signals', mount);
    [['common', 24], ['rare', 4]].forEach(function (k) {
      var b = html('div', 'nz-box ' + k[0], sig);
      html('h4', '', b, t[k[0]]);
      var plot = html('div', 'nz-plot', b); plot.setAttribute('aria-hidden', 'true');
      var dots = html('div', 'nz-dots', plot);
      for (var i = 0; i < k[1]; i++) { var d = html('i', 'nz-dot', dots); d.style.setProperty('--k', i % 7); }
      html('div', 'nz-fog', plot);
    });
    var mean = html('p', 'nz-meaning', mount); mean.setAttribute('role', 'status'); mean.setAttribute('aria-live', 'polite');
    html('p', 'nz-note', mount, t.note);
    var last = -1;
    function render() {
      v = +r.value; mount.setAttribute('data-v', v);
      out.textContent = v + '/100';
      r.setAttribute('aria-valuetext', t.unit + ' ' + v + '/100');
      r.style.setProperty('--nzp', v + '%');
      mount.style.setProperty('--nzfog', (0.04 + v * 0.0075).toFixed(3));
      mount.style.setProperty('--nzj', (v / 100 * 2.4).toFixed(2) + 'px');
      var s = v < 30 ? 0 : v < 70 ? 1 : 2;
      if (s !== last) { mean.textContent = t.states[s]; last = s; }
    }
    r.addEventListener('input', render);
    watch(sig, mount);
    render();
  }

  /* ---- page behaviour: view tabs, version switch, language links that keep the current section ---- */
  function tabs() {
    var btns = Array.prototype.slice.call(document.querySelectorAll('[data-view]'));
    if (!btns.length) return;
    function show(id, focus) {
      btns.forEach(function (b) {
        var on = b.getAttribute('data-view') === id;
        b.setAttribute('aria-selected', on ? 'true' : 'false');
        b.tabIndex = on ? 0 : -1;
        if (on && focus) b.focus();
        var p = document.getElementById(b.getAttribute('data-view'));
        if (p) p.hidden = !on;
      });
    }
    btns.forEach(function (b, i) {
      b.addEventListener('click', function () { show(b.getAttribute('data-view')); });
      b.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!k) return;
        e.preventDefault();
        show(btns[(i + k + btns.length) % btns.length].getAttribute('data-view'), true);
      });
    });
    show(location.hash === '#view-b' ? 'view-b' : 'view-a');
  }
  function versions() {
    var btns = document.querySelectorAll('[data-ver]');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var orig = b.getAttribute('data-ver') === 'orig';
        doc.classList.toggle('ver-orig', orig);
        btns.forEach(function (x) { x.setAttribute('aria-pressed', (x.getAttribute('data-ver') === 'orig') === orig ? 'true' : 'false'); });
      });
    });
  }
  function current() {
    var secs = document.querySelectorAll('main section[id]'), id = '';
    for (var i = 0; i < secs.length; i++) if (secs[i].getBoundingClientRect().top < 160) id = secs[i].id;
    return id;
  }
  function langLinks() {
    document.querySelectorAll('a[data-lang-link]').forEach(function (a) {
      a.addEventListener('click', function () {
        var id = current();
        a.setAttribute('href', a.getAttribute('href').split('#')[0] + (id && id !== 'what' ? '#' + id : ''));
      });
    });
  }

  window.MedFLDemo = { round: round, noise: noise };
  function init() {
    document.querySelectorAll('[data-flr]').forEach(function (m) { round(m); });
    document.querySelectorAll('[data-noise]').forEach(function (m) { noise(m); });
    tabs(); versions(); langLinks();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
