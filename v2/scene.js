/*
 * Scena 3D di apertura: un oggetto per progetto, fatto di forme semplici.
 * Trascina per ruotarli, passa sopra per vedere il nome, clicca per entrare.
 * I progetti e i loro colori arrivano da window.PROJECTS (scritto in index.html).
 */
import * as THREE from './vendor/three.module.min.js';

const COLORS = { lime: 0xb6ff2e, magenta: 0xff2e93, violet: 0x6b2bff };
const BLACK = 0x000000, WHITE = 0xffffff;
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const canvas = document.getElementById('scene');
const stage = canvas && canvas.parentElement;
const label = document.getElementById('pointer-label');
const projects = window.PROJECTS || [];

/* ---------- mattoni ---------- */
function solid(geometry, color, edgeColor = BLACK) {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({ color, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 })));
  g.add(new THREE.LineSegments(new THREE.EdgesGeometry(geometry, 20), new THREE.LineBasicMaterial({ color: edgeColor })));
  return g;
}
function at(obj, x, y, z) { obj.position.set(x, y, z); return obj; }

/* ---------- gli oggetti ---------- */
const builders = {
  // Fragma: la plancia esagonale con le pedine
  fragma(accent) {
    const g = new THREE.Group();
    g.add(solid(new THREE.CylinderGeometry(1, 1, 0.16, 6), WHITE));
    g.add(at(solid(new THREE.CylinderGeometry(0.62, 0.62, 0.02, 6), accent), 0, 0.09, 0));
    [[0, 0], [0.42, 0.2], [-0.36, 0.3], [0.1, -0.45], [-0.5, -0.2]].forEach(([x, z]) => {
      g.add(at(solid(new THREE.ConeGeometry(0.09, 0.42, 6), BLACK, WHITE), x, 0.31, z));
    });
    g.rotation.x = 0.35;
    return g;
  },

  // Sound Morphology: la medusa di particelle
  'sound-morphology'(accent) {
    const g = new THREE.Group();
    const pts = [];
    for (let i = 0; i < 900; i++) {               // cupola
      const u = Math.random() * Math.PI * 2, v = Math.acos(Math.random());
      pts.push(Math.sin(v) * Math.cos(u) * 0.75, Math.cos(v) * 0.5 + 0.35, Math.sin(v) * Math.sin(u) * 0.75);
    }
    const strands = 9, per = 70;
    for (let s = 0; s < strands; s++) {            // tentacoli
      const a = (s / strands) * Math.PI * 2, r = 0.25 + (s % 3) * 0.16;
      for (let i = 0; i < per; i++) pts.push(Math.cos(a) * r, 0.35 - (i / per) * 1.5, Math.sin(a) * r);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
    const base = Float32Array.from(pts);
    const cloud = new THREE.Points(geo, new THREE.PointsMaterial({ color: accent, size: 3.2, sizeAttenuation: false }));
    g.add(cloud);
    g.userData.tick = (t) => {
      const p = geo.attributes.position.array;
      for (let i = 900 * 3; i < p.length; i += 3) {
        const depth = 0.35 - base[i + 1];
        p[i] = base[i] + Math.sin(t * 1.6 + depth * 4 + i) * 0.07 * depth;
        p[i + 2] = base[i + 2] + Math.cos(t * 1.3 + depth * 4 + i) * 0.07 * depth;
      }
      geo.attributes.position.needsUpdate = true;
      cloud.position.y = Math.sin(t * 0.9) * 0.06;
    };
    g.position.y = 0.25;
    return g;
  },

  // Futbol: una maglia
  futbol(accent) {
    const s = new THREE.Shape();
    [[-0.3, 0.8], [-0.95, 0.5], [-0.75, 0.05], [-0.48, 0.2], [-0.48, -0.85], [0.48, -0.85], [0.48, 0.2], [0.75, 0.05], [0.95, 0.5], [0.3, 0.8]]
      .forEach(([x, y], i) => (i ? s.lineTo(x, y) : s.moveTo(x, y)));
    s.quadraticCurveTo(0, 0.52, -0.3, 0.8);
    const g = new THREE.Group();
    g.add(at(solid(new THREE.ExtrudeGeometry(s, { depth: 0.14, bevelEnabled: false }), accent), 0, 0, -0.07));
    [-0.24, 0, 0.24].forEach((x) => g.add(at(solid(new THREE.BoxGeometry(0.1, 1.0, 0.16), BLACK, BLACK), x, -0.32, 0)));
    return g;
  },

  // Space Debris: la Terra e i detriti in orbita
  'space-debris'(accent) {
    const g = new THREE.Group();
    g.add(solid(new THREE.IcosahedronGeometry(0.62, 1), BLACK, WHITE));
    const ring = new THREE.Group();
    for (let i = 0; i < 46; i++) {
      const a = Math.random() * Math.PI * 2, r = 0.88 + Math.random() * 0.3, size = 0.035 + Math.random() * 0.06;
      const bit = solid(new THREE.BoxGeometry(size, size, size * (1 + Math.random() * 2)), i % 4 ? accent : WHITE);
      bit.rotation.set(Math.random() * 3, Math.random() * 3, 0);
      ring.add(at(bit, Math.cos(a) * r, (Math.random() - 0.5) * 0.16, Math.sin(a) * r));
    }
    ring.rotation.x = 0.45;
    g.add(ring);
    g.userData.tick = (t) => { ring.rotation.y = t * 0.35; };
    return g;
  },

  // EsploraMi: un telefono con il segnaposto
  esplorami(accent) {
    const g = new THREE.Group();
    g.add(solid(new THREE.BoxGeometry(0.86, 1.7, 0.1), BLACK, WHITE));
    g.add(at(solid(new THREE.BoxGeometry(0.74, 1.5, 0.02), accent), 0, 0, 0.055));
    [0.42, 0.22].forEach((y, i) => g.add(at(solid(new THREE.BoxGeometry(i ? 0.36 : 0.54, 0.06, 0.02), WHITE), i ? -0.09 : 0, -y - 0.1, 0.08)));
    const pin = new THREE.Group();
    pin.add(at(solid(new THREE.SphereGeometry(0.17, 12, 8), WHITE), 0, 0.2, 0));
    const tip = solid(new THREE.ConeGeometry(0.13, 0.3, 12), WHITE);
    tip.rotation.x = Math.PI;
    pin.add(at(tip, 0, -0.03, 0));
    g.add(at(pin, 0.02, 0.22, 0.22));
    g.userData.tick = (t) => { pin.position.y = 0.22 + Math.abs(Math.sin(t * 2)) * 0.12; };
    return g;
  },

  // Gestures: l'ascensore, con le porte che si aprono
  gestures(accent) {
    const g = new THREE.Group();
    const box = new THREE.BoxGeometry(1.3, 1.7, 0.7);
    g.add(new THREE.LineSegments(new THREE.EdgesGeometry(box), new THREE.LineBasicMaterial({ color: BLACK })));
    g.add(at(solid(new THREE.BoxGeometry(1.3, 0.04, 0.7), BLACK), 0, -0.85, 0));
    g.add(at(solid(new THREE.SphereGeometry(0.14, 12, 8), BLACK), -0.25, 0.25, -0.1));   // due persone
    g.add(at(solid(new THREE.CylinderGeometry(0.1, 0.14, 0.9, 10), BLACK), -0.25, -0.35, -0.1));
    g.add(at(solid(new THREE.SphereGeometry(0.14, 12, 8), WHITE), 0.28, 0.25, -0.1));
    g.add(at(solid(new THREE.CylinderGeometry(0.1, 0.14, 0.9, 10), WHITE), 0.28, -0.35, -0.1));
    const left = at(solid(new THREE.BoxGeometry(0.64, 1.66, 0.04), accent), -0.325, 0, 0.35);
    const right = at(solid(new THREE.BoxGeometry(0.64, 1.66, 0.04), accent), 0.325, 0, 0.35);
    g.add(left, right);
    g.userData.tick = (t, hot) => {
      const target = hot ? 0.58 : (Math.sin(t * 0.9) > 0.2 ? 0.5 : 0);
      g.userData.open = (g.userData.open || 0) + (target - (g.userData.open || 0)) * 0.08;
      left.position.x = -0.325 - g.userData.open;
      right.position.x = 0.325 + g.userData.open;
    };
    return g;
  },
};

/* ---------- scena ---------- */
function start() {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  } catch (err) {
    stage.classList.add('no-webgl');
    return;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, -50, 50);
  camera.position.set(0, 0, 10);

  const items = projects.filter((p) => builders[p.slug]).map((p, i) => {
    const pivot = new THREE.Group();          // posizione e scala
    const spin = new THREE.Group();           // rotazione comune
    const model = builders[p.slug](COLORS[p.accent] || BLACK);
    spin.add(model);
    pivot.add(spin);
    const hit = new THREE.Mesh(new THREE.SphereGeometry(1.15, 10, 8), new THREE.MeshBasicMaterial({ visible: false }));
    pivot.add(hit);
    scene.add(pivot);
    return { p, pivot, spin, model, hit, scale: 1, phase: i * 1.7 };
  });

  let W = 1, H = 1, unit = 1;
  function layout() {
    W = stage.clientWidth; H = stage.clientHeight;
    renderer.setSize(W, H, false);
    const cols = W / H > 1.15 ? 3 : 2, rows = Math.ceil(items.length / cols);
    // unità di mondo: ogni cella è larga 3; lascio spazio in basso per la frase
    const top = 0.09, bottom = W / H > 1.15 ? 0.25 : 0.34;
    const cellPx = Math.min(W / cols, (H * (1 - top - bottom)) / rows);
    unit = cellPx / 2.7;
    camera.left = -W / 2 / unit; camera.right = W / 2 / unit;
    camera.top = H / 2 / unit; camera.bottom = -H / 2 / unit;
    camera.updateProjectionMatrix();
    const cy = (H * (bottom - top)) / 2 / unit;       // centro dell'area utile
    items.forEach((it, i) => {
      const c = i % cols, r = Math.floor(i / cols);
      const spreadX = Math.min(W / cols / unit, 4.6);
      it.pivot.position.set((c - (cols - 1) / 2) * spreadX, cy + ((rows - 1) / 2 - r) * 2.7, 0);
    });
  }

  /* interazione */
  const ray = new THREE.Raycaster();
  const mouse = new THREE.Vector2(5, 5);
  let rotX = 0.3, rotY = 0.45, velX = 0, velY = 0;
  let drag = null, hot = null, moved = 0;

  function pick(e) {
    const r = canvas.getBoundingClientRect();
    mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(mouse, camera);
    const hits = ray.intersectObjects(items.map((it) => it.hit), false);
    return hits.length ? items.find((it) => it.hit === hits[0].object) : null;
  }
  function setHot(it, e) {
    hot = it;
    canvas.classList.toggle('is-hot', !!it);
    if (!label) return;
    if (it && e && e.pointerType === 'mouse') {
      label.dataset.accent = it.p.accent;
      label.innerHTML = '';
      label.append(it.p.title, Object.assign(document.createElement('small'), { textContent: it.p.type[document.documentElement.dataset.lang === 'en' ? 1 : 0] }));
      label.style.left = e.clientX + 'px';
      label.style.top = e.clientY + 'px';
      label.classList.add('is-on');
    } else label.classList.remove('is-on');
  }

  canvas.addEventListener('pointerdown', (e) => {
    drag = { x: e.clientX, y: e.clientY, target: pick(e) };
    moved = 0;
    if (e.pointerType === 'mouse') { canvas.setPointerCapture(e.pointerId); canvas.classList.add('is-dragging'); }
  });
  canvas.addEventListener('pointermove', (e) => {
    if (drag) {
      const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      moved += Math.abs(dx) + Math.abs(dy);
      drag.x = e.clientX; drag.y = e.clientY;
      velY = dx * 0.012;
      if (e.pointerType === 'mouse') velX = dy * 0.012;
      rotY += velY; rotX += velX;
      if (moved > 6) setHot(null);
    } else setHot(pick(e), e);
  });
  function release(e) {
    if (!drag) return;
    const target = drag.target;
    drag = null;
    canvas.classList.remove('is-dragging');
    if (e.type === 'pointerup' && moved < 8 && target && pick(e) === target) window.location.href = target.p.slug + '.html';
  }
  canvas.addEventListener('pointerup', release);
  canvas.addEventListener('pointercancel', release);
  canvas.addEventListener('pointerleave', () => { if (!drag) setHot(null); });

  /* ciclo */
  let running = true, visible = true;
  const clock = new THREE.Clock();
  function frame() {
    if (!running) return;
    requestAnimationFrame(frame);
    if (!visible) return;
    const t = reduce ? 0 : clock.getElapsedTime();
    if (!drag) {
      rotY += velY; rotX += velX;
      velY *= 0.94; velX *= 0.94;
      if (!reduce) rotY += 0.0022;
      rotX += (0.3 - rotX) * 0.01;                 // torna piano all'inclinazione di partenza
    }
    rotX = Math.max(-1.2, Math.min(1.2, rotX));
    items.forEach((it) => {
      it.spin.rotation.set(rotX, rotY + it.phase * 0.08, 0);
      const target = it === hot ? 1.22 : 1;
      it.scale += (target - it.scale) * 0.14;
      it.pivot.scale.setScalar(it.scale);
      if (!reduce) it.pivot.position.z = Math.sin(t * 0.8 + it.phase) * 0.05;
      if (it.model.userData.tick) it.model.userData.tick(t, it === hot);
    });
    renderer.render(scene, camera);
  }

  layout();
  window.addEventListener('resize', layout);
  if ('IntersectionObserver' in window) new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(stage);
  document.addEventListener('visibilitychange', () => { running = !document.hidden; if (running) frame(); });
  frame();
}

if (canvas && stage) start();
