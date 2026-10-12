/* Every page opens at the top. Browsers and embedded viewers can carry the previous scroll position across a navigation; this resets it unless the link points at a section (#anchor). */
(function () {
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
  function toTop() { if (!location.hash) { window.scrollTo(0, 0); document.documentElement.scrollTop = 0; document.body.scrollTop = 0; } }
  toTop();
  document.addEventListener('DOMContentLoaded', toTop);
  window.addEventListener('pageshow', toTop);
  window.addEventListener('load', function () { setTimeout(toTop, 0); });
})();
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.querySelector('.mobile-menu');
  if (!toggle || !menu) return;
  toggle.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
});
