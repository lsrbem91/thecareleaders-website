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
/* Site search: a button in the header opens a search panel. The index (assets/search-index.json) is built from every public page and only loads the first time someone searches. */
document.addEventListener('DOMContentLoaded', function () {
  var inner = document.querySelector('.header-inner');
  if (!inner) return;
  var css = '.ss-btn{display:inline-flex;align-items:center;gap:6px;background:none;border:0;color:#0e2545;font:inherit;cursor:pointer;padding:8px;margin-left:auto;margin-right:4px}.ss-btn svg{width:20px;height:20px}.ss-btn span{font-size:15px}.ss-btn:focus-visible{outline:2px solid #008196;outline-offset:2px}' +
    '.ss-ov{position:fixed;inset:0;z-index:1000;background:rgba(14,37,69,.55);display:flex;justify-content:center;align-items:flex-start;padding:72px 16px 16px}.ss-ov[hidden]{display:none}' +
    '.ss-box{background:#fff;color:#0e2545;width:100%;max-width:720px;max-height:calc(100vh - 100px);display:flex;flex-direction:column;box-shadow:0 20px 50px rgba(14,37,69,.35)}' +
    '.ss-top{display:flex;gap:8px;align-items:center;padding:14px 16px;border-bottom:2px solid #008196}.ss-top input{flex:1;min-width:0;border:0;font:inherit;font-size:20px;color:#0e2545;background:transparent;padding:6px 0}.ss-top input:focus{outline:none}.ss-x{background:none;border:0;font:inherit;font-size:15px;color:#0e2545;cursor:pointer;padding:6px 8px;text-decoration:underline}' +
    '.ss-res{overflow:auto;padding:4px 0}.ss-res a{display:block;padding:12px 16px;color:#0e2545;text-decoration:none;border-bottom:1px solid #dae2e6}.ss-res a:hover,.ss-res a:focus,.ss-res a.on{background:#dae2e6;outline:none}.ss-res b{display:block;font-size:17px}.ss-res small{display:block;color:#008196;font-size:13px;margin:2px 0}.ss-res span{display:block;font-size:14px;line-height:1.45}.ss-res mark{background:#ffe2c2;color:inherit}.ss-msg{padding:16px;font-size:15px}' +
    '@media (max-width:1400px){.ss-btn span{display:none}.ss-btn{margin-right:0;padding:8px 6px}}' +
    '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .ss-btn{color:inherit}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>';
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'ss-btn'; btn.setAttribute('aria-label', 'Search the site'); btn.innerHTML = icon + '<span>Search</span>';
  var cta = inner.querySelector('.header-cta') || inner.querySelector('.nav-toggle');
  inner.insertBefore(btn, cta);
  var ov = document.createElement('div');
  ov.className = 'ss-ov'; ov.hidden = true; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Search the site');
  ov.innerHTML = '<div class="ss-box"><div class="ss-top">' + icon.replace('<svg', '<svg width="22" height="22"') + '<input type="search" placeholder="Search courses, programmes, keynotes and more" aria-label="Search" autocomplete="off"><button type="button" class="ss-x">Close</button></div><div class="ss-res" role="listbox" aria-live="polite"></div></div>';
  document.body.appendChild(ov);
  var input = ov.querySelector('input'), res = ov.querySelector('.ss-res'), idx = null, loading = null, last = null;
  function load() {
    if (idx || loading) return loading;
    loading = fetch('./assets/search-index.json?v=1').then(function (r) { return r.json(); }).then(function (j) {
      idx = j.map(function (p) { p._t = (p.t + ' ' + p.h1).toLowerCase(); p._h = (p.h + ' ' + p.s).toLowerCase(); p._d = p.d.toLowerCase(); p._b = p.b.toLowerCase(); return p; });
    }).catch(function () { res.innerHTML = '<p class="ss-msg">Search isn&#8217;t available right now. Try the menu, or email <a href="mailto:hello@thecareleaders.com">hello@thecareleaders.com</a>.</p>'; });
    return loading;
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function snip(p, terms) {
    var src = p.d && terms.some(function (t) { return p._d.indexOf(t) > -1; }) ? p.d : p.b, low = src.toLowerCase(), at = -1;
    terms.forEach(function (t) { var i = low.indexOf(t); if (i > -1 && (at < 0 || i < at)) at = i; });
    var start = Math.max(0, at - 60), out = (start ? '…' : '') + src.slice(start, start + 180) + (src.length > start + 180 ? '…' : '');
    out = esc(out);
    terms.forEach(function (t) { if (t.length > 1) out = out.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>'); });
    return out;
  }
  function run() {
    var q = input.value.trim().toLowerCase();
    if (q === last) return; last = q;
    if (q.length < 2) { res.innerHTML = ''; return; }
    if (!idx) { res.innerHTML = '<p class="ss-msg">Searching…</p>'; load().then(function () { last = null; run(); }); return; }
    var terms = q.split(/\s+/).filter(Boolean);
    var hits = idx.map(function (p) {
      var sc = 0, all = true;
      terms.forEach(function (t) {
        var s = 0;
        if (p._t.indexOf(t) > -1) s += 10;
        if (p._h.indexOf(t) > -1) s += 4;
        if (p._d.indexOf(t) > -1) s += 3;
        if (p._b.indexOf(t) > -1) s += 1;
        if (!s) all = false; sc += s;
      });
      if (p._t.indexOf(q) > -1) sc += 15;
      return { p: p, sc: all ? sc : 0 };
    }).filter(function (h) { return h.sc > 0; }).sort(function (a, b) { return b.sc - a.sc; }).slice(0, 12);
    if (!hits.length) { res.innerHTML = '<p class="ss-msg">Nothing found for &#8220;' + esc(input.value.trim()) + '&#8221;. Try a shorter word, or <a href="./contact.html">tell us what you&#8217;re looking for</a>.</p>'; return; }
    res.innerHTML = hits.map(function (h) {
      var p = h.p;
      return '<a role="option" href="./' + p.u + '"><b>' + esc(p.t || p.h1) + '</b>' + (p.s ? '<small>' + esc(p.s) + '</small>' : '') + '<span>' + snip(p, terms) + '</span></a>';
    }).join('');
  }
  var timer;
  input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 120); });
  function open() { ov.hidden = false; document.body.style.overflow = 'hidden'; input.focus(); load(); }
  function close() { ov.hidden = true; document.body.style.overflow = ''; btn.focus(); }
  btn.addEventListener('click', open);
  ov.querySelector('.ss-x').addEventListener('click', close);
  ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  ov.addEventListener('keydown', function (e) {
    var links = Array.prototype.slice.call(res.querySelectorAll('a[role=option]')), i = links.indexOf(document.activeElement);
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === 'ArrowDown' && links.length) { e.preventDefault(); (links[i + 1] || links[0]).focus(); }
    else if (e.key === 'ArrowUp' && links.length) { e.preventDefault(); if (i <= 0) input.focus(); else links[i - 1].focus(); }
    else if (e.key === 'Enter' && document.activeElement === input && links.length) { e.preventDefault(); location.href = links[0].href; }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && ov.hidden && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) { e.preventDefault(); open(); }
  });
});
/* On a course or programme page, every general "contact us" button carries that product,
   so the enquiry form opens with it already chosen. Menu links stay general. */
document.addEventListener('DOMContentLoaded', function () {
  var page = location.pathname.split('/').pop() || 'index.html';
  var src = document.querySelector('main a[href*="contact.html?topic="]');
  var q = src ? src.getAttribute('href').split('contact.html')[1] : page === 'programmes.html' ? '?topic=programme#enquire' : '';
  if (!q) return;
  document.querySelectorAll('a[href="./contact.html"], a[href="contact.html"]').forEach(function (a) {
    if (a.closest('.main-nav, .mobile-menu ul, .mm-sub, .fs-links')) return;
    a.setAttribute('href', './contact.html' + q);
  });
});
