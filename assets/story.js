/* Our story: interactive timeline (22 Oct 2026) */
(function () {
  var root = document.querySelector('.st-line'); if (!root) return;
  var items = Array.prototype.slice.call(root.querySelectorAll('.st-i'));
  var toast = document.querySelector('.st-toast'), tt;
  function open(li, on) {
    var b = li.querySelector('.st-btn'), d = li.querySelector('.st-d');
    b.setAttribute('aria-expanded', on ? 'true' : 'false'); d.hidden = !on; li.classList.toggle('st-open', on);
  }
  items.forEach(function (li) {
    li.querySelector('.st-btn').addEventListener('click', function () { open(li, li.querySelector('.st-d').hidden); });
  });
  /* filter by part of the story */
  var fb = Array.prototype.slice.call(document.querySelectorAll('.st-filter button'));
  fb.forEach(function (b) {
    b.addEventListener('click', function () {
      var era = b.getAttribute('data-era');
      fb.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      items.forEach(function (li) { li.hidden = !(era === 'all' || li.getAttribute('data-era') === era); });
      fill();
    });
  });
  /* jump to a year */
  Array.prototype.slice.call(document.querySelectorAll('.st-years a')).forEach(function (a) {
    a.addEventListener('click', function (e) {
      var t = document.getElementById(a.getAttribute('href').slice(1)); if (!t) return;
      e.preventDefault();
      if (t.hidden && fb[0]) fb[0].click();
      t.classList.add('st-in'); t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (history.replaceState) history.replaceState(null, '', '#' + t.id);
    });
  });
  /* progress rail */
  var wrap = document.querySelector('.st-wrap'), bar = document.querySelector('.st-fill');
  function fill() {
    if (!wrap || !bar) return;
    var r = wrap.getBoundingClientRect(), h = r.height, seen = Math.min(Math.max(window.innerHeight * 0.6 - r.top, 0), h);
    bar.style.height = (h ? seen / h * 100 : 0) + '%';
  }
  window.addEventListener('scroll', fill, { passive: true }); window.addEventListener('resize', fill); fill();
  /* reveal as you scroll */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduce) {
    root.classList.add('st-anim');
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('st-in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -10% 0px' });
    items.forEach(function (li) { io.observe(li); });
  }
  /* share a moment */
  function say(t) { if (!toast) return; toast.textContent = t; toast.hidden = false; clearTimeout(tt); tt = setTimeout(function () { toast.hidden = true; }, 2600); }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('.st-share'); if (!b) return;
    var url = location.href.split('#')[0] + '#' + b.getAttribute('data-share'), title = b.getAttribute('data-title') + ': The Care Leaders story';
    if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); return; }
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(url).then(function () { say('Link copied. Paste it anywhere to share this moment.'); }, function () { say(url); }); }
    else say(url);
  });
  /* open a shared moment */
  var id = location.hash.slice(1), li = id && document.getElementById(id);
  if (li && li.classList.contains('st-i')) { open(li, true); li.classList.add('st-in'); setTimeout(function () { li.scrollIntoView({ block: 'center' }); }, 60); }
})();
