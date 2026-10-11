/* Programme pages: tools library, flip-books, brochure gate, explorers. Guarded so it runs once. */
if (!window.__tclProg) { window.__tclProg = true;
/* Programme pages: tools library (filter + popup) and flip-book workbooks */
(function () {
  // ---- tools library: filter + side panel
  var dataEl = document.getElementById('tl-data');
  if (dataEl) {
    var data = JSON.parse(dataEl.textContent);
    var grid = document.querySelector('.tl-grid'), panel = document.querySelector('.tl-panel');
    document.querySelectorAll('.tl-filter button').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('.tl-filter button').forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); });
        var g = b.dataset.g;
        grid.querySelectorAll('.tl-tool').forEach(function (t) { t.hidden = !(g === 'all' || t.dataset.g === g); });
      });
    });
    function show(id, btn) {
      var t = data[id]; if (!t) return;
      grid.querySelectorAll('.tl-tool').forEach(function (x) { x.setAttribute('aria-pressed', x === btn); });
      var g = panel.querySelector('.tl-p-g'); g.textContent = t.g; g.className = 'tl-p-g g-' + t.g.toLowerCase();
      panel.querySelector('.tl-p-t').innerHTML = t.t;
      panel.querySelector('.tl-p-d').innerHTML = t.d;
      panel.querySelector('.tl-p-f').textContent = t.f;
      panel.querySelector('.tl-p-a').textContent = t.a;
      panel.querySelector('.tl-p-r').innerHTML = t.r;
      panel.querySelector('.tl-p-rw').hidden = !t.r;
      panel.classList.remove('flash'); void panel.offsetWidth; panel.classList.add('flash');
      if (window.matchMedia('(max-width:1000px)').matches) panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    grid.addEventListener('click', function (e) { var b = e.target.closest('.tl-tool'); if (b) show(b.dataset.id, b); });
  }

  // ---- flip books
  document.querySelectorAll('.fb').forEach(function (fb) {
    var tabs = fb.querySelectorAll('.fb-tabs [role=tab]');
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t); });
        fb.querySelectorAll('.fb-book').forEach(function (bk) { bk.hidden = bk.dataset.book !== t.dataset.book; });
      });
    });
    fb.querySelectorAll('.fb-book').forEach(function (bk) {
      var pages = bk.querySelectorAll('.fb-page'), i = 0, n = pages.length;
      var count = bk.querySelector('.fb-count'), prev = bk.querySelector('.fb-prev'), next = bk.querySelector('.fb-next');
      function show() {
        pages.forEach(function (p, j) { p.classList.toggle('turned', j < i); });
        count.textContent = (i + 1) + ' / ' + n;
        prev.disabled = i === 0; next.disabled = i === n - 1;
      }
      next.addEventListener('click', function () { if (i < n - 1) { i++; show(); } });
      prev.addEventListener('click', function () { if (i > 0) { i--; show(); } });
      bk.querySelector('.fb-stage').addEventListener('click', function (e) {
        var r = this.getBoundingClientRect();
        if (e.clientX - r.left > r.width / 2) next.click(); else prev.click();
      });
      show();
    });
  });
})();
/* brochure gate: posts to Mailchimp once the landing page is approved */
document.querySelectorAll('form[data-mailchimp=pending]').forEach(function (f) {
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var m = f.querySelector('.br-msg') || f.appendChild(Object.assign(document.createElement('p'), { className: 'br-msg', role: 'status' }));
    m.textContent = 'Thank you. The brochure download is being set up. Email hello@thecareleaders.com and we will send it to you.';
  });
});
/* explorers (tabs + panel) and strand switches */
document.querySelectorAll('[data-xp]').forEach(function (x) {
  var tabs = x.querySelectorAll('[data-xp-tab]');
  function pick(t, focus) {
    tabs.forEach(function (b) { var on = b === t; b.setAttribute('aria-selected', on); b.tabIndex = on ? 0 : -1; });
    x.querySelectorAll('[data-xp-panel]').forEach(function (p) {
      var on = p.dataset.xpPanel === t.dataset.xpTab; p.hidden = !on;
      if (on) { p.classList.remove('flash'); void p.offsetWidth; p.classList.add('flash'); }
    });
    if (focus) t.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { pick(t); });
    t.addEventListener('keydown', function (e) {
      var k = e.key, j = -1;
      if (k === 'ArrowDown' || k === 'ArrowRight') j = (i + 1) % tabs.length;
      if (k === 'ArrowUp' || k === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
      if (j > -1) { e.preventDefault(); pick(tabs[j], true); }
    });
  });
});

}
