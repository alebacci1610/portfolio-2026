/*
 * Effetti del sito.
 *  1. [data-bend]      immagini e video che si curvano e si inclinano mentre scorri
 *  2. [data-swap]      lettere dei titoli che cambiano carattere vicino al mouse
 *  3. [data-scramble]  etichette che si rimescolano e si ricompongono
 *  4. video e sequenze di immagini che partono solo quando sono visibili
 *  5. filtri dei progetti, striscia di schermate da trascinare
 * Con "riduci animazioni" attivo nel sistema, 1-3 restano fermi.
 */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var touch = window.matchMedia('(hover: none)').matches;
  var $$ = function (sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); };

  /* insieme degli elementi attualmente visibili, per non lavorare su tutta la pagina */
  function watch(els, margin) {
    var seen = new Set();
    if (!('IntersectionObserver' in window)) { els.forEach(function (e) { seen.add(e); }); return seen; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) seen.add(en.target); else seen.delete(en.target); });
    }, { rootMargin: margin || '20% 0px' });
    els.forEach(function (e) { io.observe(e); });
    return seen;
  }

  /* ---------- 1. curvatura allo scroll ---------- */
  function initBend() {
    var els = $$('[data-bend]');
    if (!els.length || reduce) return;
    var visible = watch(els);
    var lastY = window.scrollY, lastT = performance.now(), vel = 0, k = 0, dirty = false;

    function frame(now) {
      var dt = Math.max(8, now - lastT);
      var y = window.scrollY;
      var v = (y - lastY) / dt;                 // px per millisecondo
      lastY = y; lastT = now;
      vel += (v - vel) * 0.25;
      var target = Math.max(-1, Math.min(1, vel / 3.2));
      k += (target - k) * 0.14;

      if (Math.abs(k) > 0.004) {
        dirty = true;
        var vw = window.innerWidth;
        visible.forEach(function (el) {
          var w = el.offsetWidth, h = el.offsetHeight;
          if (!w || !h) return;
          var c = k * Math.min(h * 0.11, 70);    // quanto si incurvano i bordi
          var tE = Math.max(c, 0), tM = Math.max(-c, 0);
          var bE = h - Math.max(-c, 0), bM = h - Math.max(c, 0);
          el.style.clipPath = 'path("M0,' + tE.toFixed(1) + ' Q' + (w / 2) + ',' + (2 * tM - tE).toFixed(1) + ' ' + w + ',' + tE.toFixed(1) +
            ' L' + w + ',' + bE.toFixed(1) + ' Q' + (w / 2) + ',' + (2 * bM - bE).toFixed(1) + ' 0,' + bE.toFixed(1) + ' Z")';
          // chi sta a sinistra si gira da una parte, chi sta a destra dall'altra
          var r = el.getBoundingClientRect();
          var side = ((r.left + w / 2) - vw / 2) / (vw / 2);
          el.style.transform = 'perspective(1400px) rotateX(' + (-k * 9).toFixed(2) + 'deg) rotateY(' + (-side * Math.abs(k) * 10).toFixed(2) + 'deg) scale(' + (1 - Math.abs(k) * 0.035).toFixed(4) + ')';
        });
      } else if (dirty) {
        dirty = false; k = 0;
        els.forEach(function (el) { el.style.clipPath = ''; el.style.transform = ''; });
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* ---------- 2. lettere che cambiano carattere ---------- */
  function splitLetters(el) {
    var text = el.textContent;
    el.setAttribute('aria-label', text);
    el.textContent = '';
    text.split(' ').forEach(function (word, i, all) {
      var w = document.createElement('span');
      w.className = 'w';
      w.setAttribute('aria-hidden', 'true');
      for (var j = 0; j < word.length; j++) {
        var c = document.createElement('span');
        c.className = 'ch';
        c.textContent = word[j];
        w.appendChild(c);
      }
      el.appendChild(w);
      if (i < all.length - 1) el.appendChild(document.createTextNode(' '));
    });
  }

  function initSwap() {
    var hosts = [];
    $$('[data-swap]').forEach(function (el) {
      var leaves = $$('[lang]', el);
      (leaves.length ? leaves : [el]).forEach(function (leaf) { splitLetters(leaf); hosts.push(leaf); });
    });
    if (!hosts.length || reduce) return;
    var visible = watch(hosts, '0px');

    if (touch) {
      // senza mouse: ogni tanto qualche lettera cambia da sola
      setInterval(function () {
        visible.forEach(function (h) {
          var chars = $$('.ch', h);
          if (!chars.length) return;
          chars.forEach(function (c) { if (Math.random() < 0.5) c.classList.remove('alt'); });
          for (var n = 0; n < Math.max(1, chars.length / 12); n++) chars[Math.floor(Math.random() * chars.length)].classList.add('alt');
        });
      }, 900);
      return;
    }

    var px = -9999, py = -9999, queued = false;
    function update() {
      queued = false;
      visible.forEach(function (h) {
        var r = h.getBoundingClientRect();
        var size = parseFloat(getComputedStyle(h).fontSize) || 40;
        var reach = Math.max(46, size * 0.75);
        var near = px > r.left - reach && px < r.right + reach && py > r.top - reach && py < r.bottom + reach;
        $$('.ch', h).forEach(function (c) {
          if (!near) { c.classList.remove('alt'); return; }
          var b = c.getBoundingClientRect();
          var d = Math.hypot(px - (b.left + b.width / 2), py - (b.top + b.height / 2));
          c.classList.toggle('alt', d < reach);
        });
      });
    }
    window.addEventListener('pointermove', function (e) {
      px = e.clientX; py = e.clientY;
      if (!queued) { queued = true; requestAnimationFrame(update); }
    }, { passive: true });
    document.addEventListener('pointerleave', function () { px = py = -9999; update(); });
  }

  /* ---------- 3. etichette che si rimescolano ---------- */
  var GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  function scramble(el) {
    if (el._busy || reduce) return;
    var final = el._final || (el._final = el.textContent);
    el._busy = true;
    var start = performance.now(), dur = 420 + final.length * 14;
    (function tick(now) {
      var p = Math.min(1, (now - start) / dur);
      var done = Math.floor(p * final.length), out = '';
      for (var i = 0; i < final.length; i++) {
        var ch = final[i];
        out += (i < done || ch === ' ' || ch === ',' || ch === '.') ? ch : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      }
      el.textContent = out;
      if (p < 1) requestAnimationFrame(tick); else { el.textContent = final; el._busy = false; }
    })(start);
  }

  function initScramble() {
    var leaves = [];
    $$('[data-scramble]').forEach(function (el) {
      var inner = $$('[lang]', el);
      (inner.length ? inner : [el]).forEach(function (l) { if (!l.children.length) leaves.push(l); });
      el.addEventListener('mouseenter', function () { (inner.length ? inner : [el]).forEach(function (l) { if (!l.children.length) scramble(l); }); });
    });
    if (!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { scramble(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.6 });
    leaves.forEach(function (l) { io.observe(l); });
  }

  /* ---------- 4. video e sequenze solo quando visibili ---------- */
  function initMedia() {
    var vids = $$('video[data-auto]');
    var decks = $$('[data-slides]');
    if (!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var el = en.target;
        if (el.tagName === 'VIDEO') {
          if (en.isIntersecting) { var p = el.play(); if (p && p.catch) p.catch(function () {}); }
          else el.pause();
        } else el._on = en.isIntersecting;
      });
    }, { threshold: 0.25 });
    vids.forEach(function (v) { v.muted = true; io.observe(v); });
    decks.forEach(function (d) {
      var imgs = $$('img', d), i = 0;
      if (imgs.length < 2) return;
      io.observe(d);
      setInterval(function () {
        if (!d._on || reduce) return;
        imgs[i].classList.remove('is-on');
        i = (i + 1) % imgs.length;
        imgs[i].classList.add('is-on');
      }, 2400);
    });
  }

  /* ---------- 5. filtri e striscia di schermate ---------- */
  function initFilters() {
    var buttons = $$('.filters button');
    var works = $$('.work');
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        buttons.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        works.forEach(function (w) { w.hidden = !(f === 'all' || w.getAttribute('data-type') === f); });
      });
    });
  }

  function initStrips() {
    $$('.phones').forEach(function (strip) {
      var down = null;
      strip.addEventListener('pointerdown', function (e) {
        if (e.pointerType !== 'mouse') return;
        down = { x: e.clientX, left: strip.scrollLeft };
        strip.classList.add('is-dragging');
        strip.setPointerCapture(e.pointerId);
      });
      strip.addEventListener('pointermove', function (e) { if (down) strip.scrollLeft = down.left - (e.clientX - down.x); });
      function up() { down = null; strip.classList.remove('is-dragging'); }
      strip.addEventListener('pointerup', up);
      strip.addEventListener('pointercancel', up);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initSwap();
    initScramble();
    initBend();
    initMedia();
    initFilters();
    initStrips();
  });
})();
