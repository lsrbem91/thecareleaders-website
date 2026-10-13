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
/* Drop-down menus: hover or keyboard focus opens them (CSS); the arrow button toggles them for click and touch. */
document.addEventListener('DOMContentLoaded', function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('.main-nav .has-dd'));
  function closeAll(except) { items.forEach(function (li) { if (li !== except) { li.classList.remove('open'); var b = li.querySelector('.dd-btn'); if (b) b.setAttribute('aria-expanded', 'false'); } }); }
  items.forEach(function (li) {
    var btn = li.querySelector('.dd-btn');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !li.classList.contains('open');
      closeAll(li); li.classList.toggle('open', open); btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) { var first = li.querySelector('.dd a'); if (first) first.focus(); }
    });
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget)) { li.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); } });
    li.addEventListener('mouseleave', function () { li.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); });
  });
  document.addEventListener('click', function () { closeAll(null); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { var openLi = items.filter(function (li) { return li.classList.contains('open') || li.contains(document.activeElement); })[0]; closeAll(null); if (openLi) openLi.querySelector('.dd-btn').focus(); }
  });
});
