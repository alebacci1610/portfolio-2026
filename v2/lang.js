/*
 * Selettore lingua IT / EN
 * --------------------------------------------------------------
 * Ogni testo bilingue è scritto due volte nell'HTML:
 *   <span lang="it">Progetti</span><span lang="en">Projects</span>
 * lang.css nasconde la versione che non serve.
 *
 * Questo file va caricato nel <head> (senza defer) così la lingua
 * è decisa prima che la pagina venga disegnata, senza "sfarfallii".
 *
 * Alla prima visita: italiano se il browser è in italiano, altrimenti inglese.
 * Poi il sito ricorda l'ultima scelta del visitatore.
 */
(function () {
  var KEY = 'portfolio-lang';
  var root = document.documentElement;

  function saved() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function save(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) { /* storage non disponibile */ }
  }

  function detect() {
    var s = saved();
    if (s === 'it' || s === 'en') return s;
    var nav = (navigator.languages && navigator.languages[0]) || navigator.language || '';
    return nav.toLowerCase().indexOf('it') === 0 ? 'it' : 'en';
  }

  function apply(lang) {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang);
    var buttons = document.querySelectorAll('[data-set-lang]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute('aria-pressed', buttons[i].getAttribute('data-set-lang') === lang ? 'true' : 'false');
    }
  }

  // Subito, prima del rendering
  apply(detect());

  // Quando la pagina è pronta, collega i pulsanti
  document.addEventListener('DOMContentLoaded', function () {
    apply(root.getAttribute('data-lang'));
    document.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-set-lang]') : null;
      if (!btn) return;
      var lang = btn.getAttribute('data-set-lang');
      save(lang);
      apply(lang);
    });
  });
})();
