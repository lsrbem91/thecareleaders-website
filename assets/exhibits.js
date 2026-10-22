/* Case study exhibits: open a piece of work and page through it (22 Oct 2026) */
(function () {
  var cards = [].slice.call(document.querySelectorAll('.ex-card'));
  if (cards.length) {
    var dlg = document.createElement('dialog'); dlg.className = 'ex-dlg'; dlg.setAttribute('aria-label', 'Work viewer');
    dlg.innerHTML = '<div class="ex-top"><div><span class="ex-dt"></span><strong class="ex-dn"></strong></div><span class="ex-ct" aria-live="polite"></span><button type="button" class="ex-x" aria-label="Close">&#215;</button></div>' +
      '<div class="ex-stage"><button type="button" class="ex-pv" aria-label="Previous page">&#8592;</button><div class="ex-slide"></div><button type="button" class="ex-nx" aria-label="Next page">&#8594;</button></div>' +
      '<p class="ex-cap"></p><div class="ex-thumbs" role="tablist" aria-label="Pages"></div>';
    document.body.appendChild(dlg);
    var stage = dlg.querySelector('.ex-slide'), cap = dlg.querySelector('.ex-cap'), ct = dlg.querySelector('.ex-ct'), th = dlg.querySelector('.ex-thumbs');
    var slides = [], cur = 0, id = '', opener = null;
    function show(i) {
      cur = (i + slides.length) % slides.length;
      stage.innerHTML = ''; var n = slides[cur].cloneNode(true); stage.appendChild(n);
      cap.textContent = slides[cur].getAttribute('data-cap') || '';
      ct.textContent = 'Page ' + (cur + 1) + ' of ' + slides.length;
      [].forEach.call(th.children, function (b, k) { b.setAttribute('aria-selected', k === cur ? 'true' : 'false'); if (k === cur) b.scrollIntoView({ block: 'nearest', inline: 'center' }); });
      if (history.replaceState) history.replaceState(null, '', '#ex-' + id + '-' + (cur + 1));
    }
    function open(key, page, from) {
      var t = document.getElementById('ex-' + key); if (!t) return;
      id = key; opener = from || null;
      var sec = (from && from.closest('.ex-sec')) || document.querySelector('.ex-sec');
      if (sec) { var cs = getComputedStyle(sec); ['--exa', '--exb', '--exl'].forEach(function (v) { var x = cs.getPropertyValue(v); if (x) dlg.style.setProperty(v, x.trim()); }); }
      slides = [].slice.call(t.content.querySelectorAll('.ex-s'));
      dlg.querySelector('.ex-dt').textContent = t.getAttribute('data-type') || '';
      dlg.querySelector('.ex-dn').textContent = t.getAttribute('data-title') || '';
      th.innerHTML = '';
      slides.forEach(function (s, k) {
        var b = document.createElement('button'); b.type = 'button'; b.setAttribute('role', 'tab'); b.setAttribute('aria-label', 'Page ' + (k + 1) + ': ' + (s.getAttribute('data-cap') || ''));
        var im = s.querySelector('img'); if (im) { var x = document.createElement('img'); x.src = im.getAttribute('src'); x.alt = ''; b.appendChild(x); } else { b.textContent = k + 1; b.className = 'ex-tn'; }
        b.addEventListener('click', function () { show(k); }); th.appendChild(b);
      });
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
      document.documentElement.classList.add('ex-lock');
      show(page || 0);
    }
    function close() { if (dlg.open) dlg.close(); }
    dlg.addEventListener('close', function () { document.documentElement.classList.remove('ex-lock'); if (history.replaceState) history.replaceState(null, '', location.pathname + location.search + '#see-the-work'); if (opener) opener.focus(); });
    dlg.querySelector('.ex-x').addEventListener('click', close);
    dlg.querySelector('.ex-pv').addEventListener('click', function () { show(cur - 1); });
    dlg.querySelector('.ex-nx').addEventListener('click', function () { show(cur + 1); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) close(); });
    dlg.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1); } });
    var x0 = null; stage.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); x0 = null; });
    cards.forEach(function (c) { c.addEventListener('click', function () { open(c.getAttribute('data-ex'), 0, c); }); });
    var m = location.hash.match(/^#ex-([a-z0-9-]+)-(\d+)$/);
    if (m) open(m[1], parseInt(m[2], 10) - 1, document.querySelector('.ex-card[data-ex="' + m[1] + '"]'));
  }
  /* letter explorers */
  [].forEach.call(document.querySelectorAll('[data-dw]'), function (w) {
    var tabs = [].slice.call(w.querySelectorAll('[role="tab"]'));
    function sel(t) { tabs.forEach(function (x) { var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute('aria-controls')).hidden = !on; }); }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { sel(t); });
      t.addEventListener('keydown', function (e) { var d = { ArrowRight: 1, ArrowLeft: -1 }[e.key]; if (d) { e.preventDefault(); var n = tabs[(i + d + tabs.length) % tabs.length]; sel(n); n.focus(); } });
    });
  });
  /* shuffle a commitment */
  [].forEach.call(document.querySelectorAll('[data-shuffle]'), function (box) {
    var items = [].slice.call(box.querySelectorAll('li')), out = box.querySelector('.cm-out'), btn = box.querySelector('.cm-btn'), k = 0;
    function show() { out.classList.remove('in'); void out.offsetWidth; out.textContent = items[k].textContent; out.classList.add('in'); box.querySelector('.cm-n').textContent = (k + 1) + ' of ' + items.length; }
    btn.addEventListener('click', function () { k = (k + 1) % items.length; show(); }); show();
  });
  /* feedback bars grow when seen */
  var fb = document.querySelector('[data-fbc]');
  if (fb) { if ('IntersectionObserver' in window) { var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { fb.classList.add('on'); io.disconnect(); } }, { threshold: .3 }); io.observe(fb); } else fb.classList.add('on'); }
})();
