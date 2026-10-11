/* Programme pages: tools library (filter + popup) and flip-book workbooks */
(function () {
  // ---- tools library
  var dataEl = document.getElementById('tl-data');
  if (dataEl) {
    var data = JSON.parse(dataEl.textContent);
    var dlg = document.getElementById('tl-dialog');
    var grid = document.querySelector('.tl-grid');
    var last = null;
    document.querySelectorAll('.tl-filter button').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('.tl-filter button').forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); });
        var g = b.dataset.g;
        grid.querySelectorAll('.tl-tool').forEach(function (t) { t.hidden = !(g === 'all' || t.dataset.g === g); });
      });
    });
    function open(id, btn) {
      var t = data[id]; if (!t) return;
      last = btn;
      dlg.querySelector('#tl-d-title').innerHTML = t.t;
      var g = dlg.querySelector('.tl-d-g'); g.textContent = t.g; g.className = 'tl-d-g g-' + t.g.toLowerCase();
      dlg.querySelector('.tl-d-d').innerHTML = t.d;
      dlg.querySelector('.tl-d-f').textContent = t.f;
      dlg.querySelector('.tl-d-a').textContent = t.a;
      dlg.querySelector('.tl-d-r').innerHTML = t.r;
      dlg.querySelector('.tl-d-rw').hidden = !t.r;
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    }
    function close() { if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); if (last) last.focus(); }
    grid.addEventListener('click', function (e) { var b = e.target.closest('.tl-tool'); if (b) open(b.dataset.id, b); });
    dlg.querySelector('.tl-close').addEventListener('click', close);
    dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });
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
