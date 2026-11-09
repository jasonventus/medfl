/* Shared MedFL components (homepages + explain.html). Text comes from data/medfl-data.js (window.MEDFL_DATA). */
(function () {
  'use strict';
  var D = window.MEDFL_DATA || {};
  var doc = document.documentElement;
  doc.classList.add('js');
  var NS = 'http://www.w3.org/2000/svg';

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
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- one federated round with six clients: images never move, only parameters / protected updates travel ---- */
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
      var mk = svg('marker', { id: m[0], viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto' }, defs);
      svg('path', { d: 'M0 0L10 5L0 10z', fill: m[1] }, mk);
    });
    var down = svg('g', { 'class': 'flr-down' }, s), up = svg('g', { 'class': 'flr-up' }, s), st = svg('g', { 'class': 'flr-p2' }, s);
    CL.forEach(function (c, i) {
      var cx = c[0] + 110, top = i < 3, cy = top ? 100 : 300, sx = SX[i % 3], sy = top ? 158 : 242;
      svg('line', { x1: sx, y1: sy, x2: cx, y2: cy, 'marker-end': 'url(#flr-m-down)' }, down);
      svg('line', { x1: cx, y1: cy, x2: sx, y2: sy, 'marker-end': 'url(#flr-m-up)' }, up);
      svg('line', { x1: cx + 18, y1: cy, x2: sx + 18, y2: sy, 'marker-end': 'url(#flr-m-p2)' }, st);
    });
    var srv = svg('g', { 'class': 'flr-server' }, s);
    svg('rect', { 'class': 'flr-glow', x: 244, y: 152, width: 232, height: 96, rx: 18 }, srv);
    svg('rect', { x: 250, y: 158, width: 220, height: 84, rx: 14 }, srv);
    svg('text', { x: 360, y: 192, 'text-anchor': 'middle', 'class': 'flr-t1' }, srv, t.server);
    svg('text', { x: 360, y: 220, 'text-anchor': 'middle', 'class': 'flr-agg' }, srv, t.agg);
    svg('text', { x: 240, y: 186, 'text-anchor': 'end', 'class': 'flr-lab flr-lab-down' }, s, t.down);
    svg('text', { x: 240, y: 186, 'text-anchor': 'end', 'class': 'flr-lab flr-lab-up' }, s, t.up);
    svg('text', { x: 240, y: 214, 'text-anchor': 'end', 'class': 'flr-lab flr-lab-p2' }, s, t.stats);
    CL.forEach(function (c, i) {
      var g = svg('g', { 'class': 'flr-client' }, s), x = c[0], y = c[1];
      svg('rect', { 'class': 'flr-box', x: x, y: y, width: 220, height: 84, rx: 12 }, g);
      svg('text', { x: x + 12, y: y + 24, 'class': 'flr-t2' }, g, t.client + ' ' + (i + 1));
      svg('rect', { x: x + 176, y: y + 8, width: 30, height: 24, rx: 3, fill: '#e9d6c3', stroke: '#9a7b5f' }, g);
      svg('rect', { x: x + 170, y: y + 13, width: 30, height: 24, rx: 3, fill: '#f4e7d9', stroke: '#9a7b5f' }, g);
      svg('circle', { cx: x + 185, cy: y + 25, r: 6, fill: '#8a5a3c' }, g);
      svg('text', { x: x + 12, y: y + 45, 'class': 'flr-t3' }, g, '▣ ' + t.local);
      var dp = svg('g', { 'class': 'flr-dp' }, g);
      svg('rect', { x: x + 8, y: y + 54, width: 204, height: 24, rx: 6 }, dp);
      svg('text', { x: x + 16, y: y + 71, 'class': 'flr-t4' }, dp, t.dp1 + ' · ' + t.dp2);
    });
    var cap = html('div', 'flr-cap', mount);
    cap.setAttribute('role', 'status'); cap.setAttribute('aria-live', 'polite');
    var bar = html('div', 'flr-controls', mount);
    var stepBtns = t.steps.map(function (name, i) {
      var b = html('button', 'flr-step', bar, (i + 1) + '. ' + name);
      b.type = 'button';
      b.addEventListener('click', function () { stop(); go(i); });
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
      cap.innerHTML = '';
      html('b', '', cap, (step + 1) + '. ' + t.titles[step]);
      html('span', '', cap, t.copies[step]);
      stepBtns.forEach(function (b, k) { b.setAttribute('aria-pressed', k === step ? 'true' : 'false'); });
      prev.disabled = step === 0; next.disabled = step === 3;
    }
    function stop() { if (mount._timer) { clearInterval(mount._timer); mount._timer = null; } play.textContent = t.play; }
    play.addEventListener('click', function () {
      if (mount._timer) { stop(); return; }
      if (step === 3) go(0);
      play.textContent = t.pause;
      mount._timer = setInterval(function () { if (step >= 3) { stop(); return; } go(step + 1); }, reduce ? 6000 : 3800);
    });
    prev.addEventListener('click', function () { stop(); go(step - 1); });
    next.addEventListener('click', function () { stop(); go(step + 1); });
    box.addEventListener('change', function () { p2 = box.checked; mount.setAttribute('data-p2', p2 ? '1' : '0'); if (p2 && step !== 2) { stop(); go(2); } else go(step); });
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
    var r = html('input', '', row); r.type = 'range'; r.min = 0; r.max = 100; r.step = 10; r.value = v; r.id = id;
    html('span', '', row, t.high);
    var out = html('output', '', row); out.setAttribute('for', id);
    var sig = html('div', 'nz-signals', mount);
    [['common', 24], ['rare', 4]].forEach(function (k) {
      var b = html('div', 'nz-box ' + k[0], sig);
      html('h4', '', b, t[k[0]]);
      var plot = html('div', 'nz-plot', b); plot.setAttribute('aria-hidden', 'true');
      var dots = html('div', 'nz-dots', plot);
      for (var i = 0; i < k[1]; i++) html('i', 'nz-dot', dots);
      html('div', 'nz-fog', plot);
    });
    var mean = html('p', 'nz-meaning', mount); mean.setAttribute('role', 'status'); mean.setAttribute('aria-live', 'polite');
    html('p', 'nz-note', mount, t.note);
    function render() {
      v = +r.value; mount.setAttribute('data-v', v);
      out.textContent = v + '/100';
      r.setAttribute('aria-valuetext', t.unit + ' ' + v + '/100');
      mount.style.setProperty('--nzfog', (0.04 + v * 0.0075).toFixed(3));
      mean.textContent = t.states[v < 30 ? 0 : v < 70 ? 1 : 2];
    }
    r.addEventListener('input', render);
    render();
  }

  /* ---- page behaviour: view tabs, version switch, language links that keep the current section ---- */
  function tabs() {
    var btns = document.querySelectorAll('[data-view]');
    if (!btns.length) return;
    function show(id) {
      btns.forEach(function (b) {
        var on = b.getAttribute('data-view') === id;
        b.setAttribute('aria-selected', on ? 'true' : 'false');
        var p = document.getElementById(b.getAttribute('data-view'));
        if (p) p.hidden = !on;
      });
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-view')); }); });
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
