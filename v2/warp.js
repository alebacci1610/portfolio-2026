/*
 * Deformazione vera di immagini e video mentre scorri.
 * Ogni elemento [data-bend] viene ridisegnato come superficie in un canvas
 * a tutto schermo dietro la pagina; uno shader la piega lungo la stessa curva
 * che fx.js usa per i testi (window.FX.k = quanto stai scorrendo, da -1 a 1).
 * Solo su computer: su telefono resta il ripiego più leggero di fx.js.
 */
import * as THREE from './vendor/three.module.min.js';

const FX = window.FX;
const els = [...document.querySelectorAll('[data-bend]')];

const VERT = `
  uniform vec2 uView;
  uniform float uK;
  uniform float uAmp;
  varying vec2 vUv;
  void main() {
    vUv = uv;
    vec4 wp = modelMatrix * vec4(position, 1.0);
    float nx = wp.x / uView.x;                       // -0.5 .. 0.5 sullo schermo
    wp.y -= uK * uAmp * cos(3.14159265 * nx);        // il centro resta indietro
    wp.x *= 1.0 - uK * 0.07 * (wp.y / uView.y) * 2.0; // un po' di prospettiva
    gl_Position = projectionMatrix * viewMatrix * wp;
  }`;
const FRAG = `
  uniform sampler2D uTex;
  uniform vec2 uPlane;
  uniform vec2 uMedia;
  uniform float uCover;
  varying vec2 vUv;
  void main() {
    vec2 uv = vUv;
    if (uCover > 0.5) {                              // come object-fit: cover
      float rp = uPlane.x / uPlane.y, rm = uMedia.x / uMedia.y;
      vec2 s = rp > rm ? vec2(1.0, rm / rp) : vec2(rp / rm, 1.0);
      uv = (uv - 0.5) * s + 0.5;
    }
    gl_FragColor = texture2D(uTex, uv);
  }`;

function start() {
  if (!FX || FX.reduce || FX.touch || !els.length) return;
  const canvas = document.createElement('canvas');
  canvas.id = 'warp';
  canvas.setAttribute('aria-hidden', 'true');
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  } catch (err) { return; }
  renderer.outputColorSpace = THREE.LinearSRGBColorSpace;   // colori passati così come sono
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  document.body.prepend(canvas);
  document.documentElement.classList.add('gl-on');
  FX.gl = true;

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, -10, 10);
  const geo = new THREE.PlaneGeometry(1, 1, 36, 24);
  const shared = { uView: { value: new THREE.Vector2(1, 1) }, uK: { value: 0 }, uAmp: { value: FX.amp } };

  function texFrom(source, isVideo) {
    const t = isVideo ? new THREE.VideoTexture(source) : new THREE.Texture(source);
    t.generateMipmaps = false;
    t.minFilter = THREE.LinearFilter;
    t.magFilter = THREE.LinearFilter;
    if (!isVideo) t.needsUpdate = true;
    return t;
  }

  const items = els.map((el) => {
    const mat = new THREE.ShaderMaterial({
      vertexShader: VERT, fragmentShader: FRAG, transparent: true,
      uniforms: { ...shared, uTex: { value: null }, uPlane: { value: new THREE.Vector2(1, 1) }, uMedia: { value: new THREE.Vector2(1, 1) }, uCover: { value: 1 } },
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.visible = false;
    mesh.frustumCulled = false;
    scene.add(mesh);
    return { el, mesh, mat, textures: new Map(), current: null, seen: false };
  });

  // quale immagine o video sta mostrando l'elemento in questo momento
  function activeMedia(el) {
    const v = el.querySelector('video');
    if (v) return v;
    return el.querySelector('img.is-on') || el.querySelector('img');
  }
  function ready(m) {
    return m.tagName === 'VIDEO' ? m.readyState >= 2 && m.videoWidth > 0 && m.currentTime > 0 : m.complete && m.naturalWidth > 0;
  }

  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { const it = items.find((i) => i.el === en.target); if (it) it.seen = en.isIntersecting; });
  }, { rootMargin: '30% 0px' });
  items.forEach((it) => io.observe(it.el));

  let W = 1, H = 1;
  function resize() {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H, false);
    camera.left = -W / 2; camera.right = W / 2; camera.top = H / 2; camera.bottom = -H / 2;
    camera.updateProjectionMatrix();
    shared.uView.value.set(W, H);
  }
  resize();
  window.addEventListener('resize', resize);

  function frame() {
    requestAnimationFrame(frame);
    shared.uK.value = FX.k;
    shared.uAmp.value = FX.amp;
    items.forEach((it) => {
      if (!it.seen) { it.mesh.visible = false; return; }
      const m = activeMedia(it.el);
      if (!m || !ready(m)) {
        if (!it.current) { it.mesh.visible = false; return; }   // ancora niente da mostrare: resta l'elemento normale
      } else if (it.current !== m) {
        if (!it.textures.has(m)) it.textures.set(m, texFrom(m, m.tagName === 'VIDEO'));
        it.current = m;
        it.mat.uniforms.uTex.value = it.textures.get(m);
        it.mat.uniforms.uMedia.value.set(m.videoWidth || m.naturalWidth, m.videoHeight || m.naturalHeight);
        it.mat.uniforms.uCover.value = getComputedStyle(m).objectFit === 'cover' ? 1 : 0;
        it.el.classList.add('is-gl');
      }
      const r = it.el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) { it.mesh.visible = false; return; }
      it.mesh.visible = true;
      it.mesh.scale.set(r.width, r.height, 1);
      it.mesh.position.set(r.left + r.width / 2 - W / 2, -(r.top + r.height / 2 - H / 2), 0);
      it.mat.uniforms.uPlane.value.set(r.width, r.height);
    });
    renderer.render(scene, camera);
  }
  frame();
}

start();
