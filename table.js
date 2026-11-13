/*
 * Il tavolo: stampe da trascinare, lanciare e impilare.
 * - trascina: sposta la stampa (si solleva e si inclina col movimento)
 * - lancia: rilascia mentre ti muovi e la stampa scivola e rimbalza sui bordi
 * - clic senza trascinare: apre il progetto
 * - "Metti in ordine": allinea tutto alla griglia del tappetino
 * Più veloce lanci, più si allarga il nome stampato sul tappetino.
 */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;

  function css(name, el) {
    return parseFloat(getComputedStyle(el || root).getPropertyValue(name)) || 0;
  }

  /* ---------- righelli ---------- */
  function drawRulers(mat) {
    var old = mat.querySelectorAll('.ruler');
    for (var i = 0; i < old.length; i++) old[i].remove();
    var g = css('--grid'), e = css('--edge');
    var W = mat.clientWidth, H = mat.clientHeight;
    var NS = 'http://www.w3.org/2000/svg';

    function ruler(horizontal) {
      var len = horizontal ? W : H;
      var svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('class', 'ruler');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('width', horizontal ? W : e);
      svg.setAttribute('height', horizontal ? e : H);
      svg.style.left = '0'; svg.style.top = '0';
      var n = 0;
      for (var p = e; p < len; p += g, n++) {
        var major = n % 5 === 0;
        var l = document.createElementNS(NS, 'line');
        var t = major ? 12 : 6;
        if (horizontal) { l.setAttribute('x1', p + 0.5); l.setAttribute('x2', p + 0.5); l.setAttribute('y1', 0); l.setAttribute('y2', t); }
        else { l.setAttribute('y1', p + 0.5); l.setAttribute('y2', p + 0.5); l.setAttribute('x1', 0); l.setAttribute('x2', t); }
        svg.appendChild(l);
        if (major && n > 0) {
          var tx = document.createElementNS(NS, 'text');
          tx.textContent = n / 5;
          if (horizontal) { tx.setAttribute('x', p + 3); tx.setAttribute('y', 22); }
          else { tx.setAttribute('x', 3); tx.setAttribute('y', p + 12); }
          svg.appendChild(tx);
        }
      }
      mat.appendChild(svg);
    }
    ruler(true);
    ruler(false);
  }

  /* ---------- nome che si allarga ---------- */
  var boost = 0, boostTarget = 0, boostRaf = 0;
  function pushBoost(speed) {
    boostTarget = Math.min(40, speed * 8);
    if (!boostRaf && !reduce) boostRaf = requestAnimationFrame(tickBoost);
  }
  function tickBoost() {
    boost += (boostTarget - boost) * 0.18;
    boostTarget *= 0.93;
    root.style.setProperty('--boost', boost.toFixed(1));
    if (boost > 0.3 || boostTarget > 0.3) boostRaf = requestAnimationFrame(tickBoost);
    else { root.style.setProperty('--boost', '0'); boostRaf = 0; }
  }

  /* ---------- il tavolo ---------- */
  function Board(mat, opts) {
    this.mat = mat;
    this.opts = opts || {};
    this.key = 'tavolo:' + (this.opts.key || location.pathname);
    this.z = 10;
    this.mode = 'messy';
    this.items = [].map.call(mat.querySelectorAll('[data-drag]'), function (el) {
      return { el: el, x: 0, y: 0, r: 0, base: parseFloat(el.dataset.r || 0), vx: 0, vy: 0 };
    });
    this.bind();
  }

  Board.prototype.bounds = function (it) {
    var W = this.mat.clientWidth, H = this.mat.clientHeight;
    var w = it.el.offsetWidth, h = it.el.offsetHeight;
    return { minX: -w * 0.35, maxX: W - w * 0.65, minY: -h * 0.2, maxY: H - h * 0.55 };
  };

  Board.prototype.apply = function (it) {
    var s = it.el.style;
    s.setProperty('--x', it.x.toFixed(1) + 'px');
    s.setProperty('--y', it.y.toFixed(1) + 'px');
    s.setProperty('--r', it.r.toFixed(2) + 'deg');
  };

  Board.prototype.messyLayout = function () {
    var W = this.mat.clientWidth, H = this.mat.clientHeight;
    var e = css('--edge');
    this.items.forEach(function (it) {
      var w = it.el.offsetWidth, h = it.el.offsetHeight;
      var fx = parseFloat(it.el.dataset.mx || 0.5), fy = parseFloat(it.el.dataset.my || 0.5);
      it.x = e + fx * Math.max(0, W - w - e - 24);
      it.y = e + fy * Math.max(0, H - h - e - 64);
      it.r = it.base;
    });
  };

  Board.prototype.setMode = function (mode, animate) {
    this.mode = mode;
    var self = this;
    if (mode === 'tidy' && this.opts.tidy) this.opts.tidy(this);
    else {
      if (this.opts.beforeMessy) this.opts.beforeMessy(this);
      this.messyLayout();
    }
    this.items.forEach(function (it, i) {
      if (animate && !reduce) {
        it.el.classList.add('is-settling');
        it.el.style.transitionDelay = (i * 35) + 'ms';
      }
      self.apply(it);
    });
    if (animate && !reduce) {
      setTimeout(function () {
        self.items.forEach(function (it) { it.el.classList.remove('is-settling'); it.el.style.transitionDelay = ''; });
      }, 700 + this.items.length * 35);
    }
    if (this.opts.onMode) this.opts.onMode(mode);
    this.save();
  };

  Board.prototype.save = function () {
    try {
      sessionStorage.setItem(this.key, JSON.stringify({
        mode: this.mode, W: this.mat.clientWidth, H: this.mat.clientHeight,
        pos: this.items.map(function (it) { return [it.x, it.y, it.r, parseInt(it.el.style.zIndex || 0, 10)]; })
      }));
    } catch (e) { /* storage non disponibile */ }
  };

  Board.prototype.restore = function () {
    try {
      var d = JSON.parse(sessionStorage.getItem(this.key) || 'null');
      if (!d || d.pos.length !== this.items.length) return false;
      if (Math.abs(d.W - this.mat.clientWidth) > 40 || Math.abs(d.H - this.mat.clientHeight) > 120) return d.mode;
      var self = this;
      this.mode = d.mode;
      this.touched = true;
      if (d.mode === 'tidy' && this.opts.tidy) this.opts.tidy(this, true);
      this.items.forEach(function (it, i) {
        it.x = d.pos[i][0]; it.y = d.pos[i][1]; it.r = d.pos[i][2];
        if (d.pos[i][3]) { it.el.style.zIndex = d.pos[i][3]; self.z = Math.max(self.z, d.pos[i][3]); }
        self.apply(it);
      });
      if (this.opts.onMode) this.opts.onMode(d.mode);
      return true;
    } catch (e) { return false; }
  };

  Board.prototype.drop = function () {
    // un solo momento orchestrato: le stampe "cadono" sul tavolo
    if (reduce) return;
    this.items.forEach(function (it, i) {
      var el = it.el;
      el.style.setProperty('--s', '1.18');
      el.style.opacity = '0';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          el.style.transition = 'transform 0.6s cubic-bezier(0.3, 1.3, 0.5, 1), opacity 0.3s ease';
          el.style.transitionDelay = (120 + i * 70) + 'ms';
          el.style.setProperty('--s', '1');
          el.style.opacity = '1';
          setTimeout(function () { el.style.transition = ''; el.style.transitionDelay = ''; }, 900 + i * 70);
        });
      });
    });
  };

  Board.prototype.bind = function () {
    var self = this;
    this.items.forEach(function (it) {
      var el = it.el, start = null, last = null, raf = 0;

      el.addEventListener('dragstart', function (e) { e.preventDefault(); });

      el.addEventListener('pointerdown', function (e) {
        if (e.button !== 0) return;
        self.touched = true;
        cancelAnimationFrame(raf);
        el.setPointerCapture(e.pointerId);
        el.style.zIndex = ++self.z;
        el.classList.add('is-dragging');
        el.style.setProperty('--s', '1.04');
        start = { px: e.clientX, py: e.clientY, x: it.x, y: it.y, t: performance.now() };
        last = { px: e.clientX, py: e.clientY, t: start.t };
        it.vx = it.vy = 0;
      });

      el.addEventListener('pointermove', function (e) {
        if (!start) return;
        var now = performance.now(), dt = Math.max(1, now - last.t);
        var vx = (e.clientX - last.px) / dt, vy = (e.clientY - last.py) / dt;
        it.vx = it.vx * 0.6 + vx * 0.4;
        it.vy = it.vy * 0.6 + vy * 0.4;
        last = { px: e.clientX, py: e.clientY, t: now };
        it.x = start.x + (e.clientX - start.px);
        it.y = start.y + (e.clientY - start.py);
        if (!reduce) {
          var tilt = Math.max(-14, Math.min(14, it.vx * 6));
          it.r += ((it.base + tilt) - it.r) * 0.25;
          pushBoost(Math.hypot(it.vx, it.vy));
        }
        self.apply(it);
      });

      function end(e) {
        if (!start) return;
        if (e.type === 'pointercancel') {
          // il browser ha preso il gesto (es. scorrimento della pagina): rimetti la stampa dov'era
          it.x = start.x; it.y = start.y; it.r = it.base; start = null;
          el.classList.remove('is-dragging');
          el.style.setProperty('--s', '1');
          self.apply(it);
          return;
        }
        var moved = Math.hypot(e.clientX - start.px, e.clientY - start.py);
        var quick = performance.now() - start.t < 400;
        start = null;
        el.classList.remove('is-dragging');
        el.style.setProperty('--s', '1');
        if (moved < 6 && quick && el.href && e.type === 'pointerup') { self.open(el); return; }
        if (self.mode === 'tidy') { self.mode = 'messy'; if (self.opts.onMode) self.opts.onMode('messy'); }
        // se la stampa era ferma da un attimo, niente lancio
        if (performance.now() - last.t > 80) it.vx = it.vy = 0;
        self.fling(it, function (id) { raf = id; });
      }
      el.addEventListener('pointerup', end);
      el.addEventListener('pointercancel', end);

      // il clic "vero" lo gestiamo noi; da tastiera (Invio) apre normalmente
      el.addEventListener('click', function (e) {
        if (e.detail !== 0) e.preventDefault();
        else if (el.href) { e.preventDefault(); self.open(el); }
      });
    });
  };

  Board.prototype.fling = function (it, setRaf) {
    var self = this, prev = performance.now();
    if (reduce) { it.vx = it.vy = 0; }
    function step(now) {
      var dt = Math.min(32, now - prev); prev = now;
      var b = self.bounds(it);
      it.x += it.vx * dt; it.y += it.vy * dt;
      if (it.x < b.minX) { it.x = b.minX; it.vx = Math.abs(it.vx) * 0.5; }
      if (it.x > b.maxX) { it.x = b.maxX; it.vx = -Math.abs(it.vx) * 0.5; }
      if (it.y < b.minY) { it.y = b.minY; it.vy = Math.abs(it.vy) * 0.5; }
      if (it.y > b.maxY) { it.y = b.maxY; it.vy = -Math.abs(it.vy) * 0.5; }
      var f = Math.pow(0.995, dt);
      it.vx *= f; it.vy *= f;
      it.r += (it.base + it.vx * 4 - it.r) * 0.08;
      self.apply(it);
      if (Math.hypot(it.vx, it.vy) > 0.02) setRaf(requestAnimationFrame(step));
      else self.save();
    }
    setRaf(requestAnimationFrame(step));
  };

  // dopo un ridimensionamento: in ordine si ricalcola, sparpagliato si tiene tutto dentro il tavolo
  Board.prototype.refit = function () {
    if (this.mode === 'tidy' || !this.touched) { this.setMode(this.mode, false); return; }
    var self = this;
    this.items.forEach(function (it) {
      var b = self.bounds(it);
      it.x = Math.max(b.minX, Math.min(b.maxX, it.x));
      it.y = Math.max(b.minY, Math.min(b.maxY, it.y));
      self.apply(it);
    });
    this.save();
  };

  Board.prototype.open = function (el) {
    this.save();
    var img = el.querySelector('img');
    var go = function () { window.location.href = el.href; };
    if (img && 'startViewTransition' in document && !reduce) img.style.viewTransitionName = 'hero';
    go();
  };

  window.Tavolo = { Board: Board, drawRulers: drawRulers };

  /* ---------- striscia di schermate: trascina per scorrere ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    [].forEach.call(document.querySelectorAll('.phones'), function (strip) {
      var down = null;
      strip.addEventListener('pointerdown', function (e) {
        if (e.pointerType !== 'mouse') return;
        down = { x: e.clientX, left: strip.scrollLeft };
        strip.classList.add('is-dragging');
        strip.setPointerCapture(e.pointerId);
      });
      strip.addEventListener('pointermove', function (e) {
        if (down) strip.scrollLeft = down.left - (e.clientX - down.x);
      });
      function up() { down = null; strip.classList.remove('is-dragging'); }
      strip.addEventListener('pointerup', up);
      strip.addEventListener('pointercancel', up);
    });
  });
})();
