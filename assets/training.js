/* Training finder for commissioners: filter by who it is for, what needs to change, format and a search;
   list or card view; a shortlist that becomes one enquiry email. Everything shows without JavaScript. */
document.addEventListener('DOMContentLoaded', function () {
  var bar = document.querySelector('[data-tk]');
  if (!bar) return;
  var list = document.querySelector('[data-tk-list]');
  var items = Array.prototype.slice.call(document.querySelectorAll('.tk-i'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('[data-tk-group]'));
  var count = bar.querySelector('[data-tk-count]');
  var reset = bar.querySelector('[data-tk-reset]');
  var empty = document.querySelector('[data-tk-empty]');
  var fields = Array.prototype.slice.call(bar.querySelectorAll('[data-k]'));
  var tiles = Array.prototype.slice.call(document.querySelectorAll('.tk-tile'));
  var state = { for: '', need: '', fmt: '', q: '' };

  function store(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function has(el, key, val) { return !val || (' ' + (el.getAttribute('data-' + key) || '') + ' ').indexOf(' ' + val + ' ') > -1; }

  try {
    var qs = new URLSearchParams(location.search);
    Object.keys(state).forEach(function (k) { if (qs.get(k)) state[k] = qs.get(k); });
  } catch (e) {}

  function apply(updateUrl) {
    var shown = 0, words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
    items.forEach(function (it) {
      var text = it.getAttribute('data-text') || '';
      var ok = has(it, 'for', state.for) && has(it, 'need', state.need) && has(it, 'fmt', state.fmt) &&
        words.every(function (w) { return text.indexOf(w) > -1; });
      it.hidden = !ok; if (ok) shown++;
    });
    groups.forEach(function (g) { g.hidden = !g.querySelector('.tk-i:not([hidden])'); });
    var any = state.for || state.need || state.fmt || state.q;
    count.textContent = any ? (shown === 1 ? 'Showing 1 course' : 'Showing ' + shown + ' courses') : 'All ' + items.length + ' courses';
    reset.hidden = !any;
    if (empty) empty.hidden = shown > 0;
    fields.forEach(function (f) { if (f.value !== state[f.getAttribute('data-k')]) f.value = state[f.getAttribute('data-k')]; });
    tiles.forEach(function (t) { t.setAttribute('aria-current', t.getAttribute('data-who') === state.for ? 'true' : 'false'); });
    if (updateUrl && history.replaceState) {
      try {
        var p = new URLSearchParams();
        Object.keys(state).forEach(function (k) { if (state[k]) p.set(k, state[k]); });
        var s = p.toString();
        history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash);
      } catch (e) {}
    }
  }

  fields.forEach(function (f) {
    f.addEventListener(f.tagName === 'INPUT' ? 'input' : 'change', function () { state[f.getAttribute('data-k')] = f.value.trim(); apply(true); });
  });
  reset.addEventListener('click', function () { state = { for: '', need: '', fmt: '', q: '' }; apply(true); });
  tiles.forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.preventDefault();
      var who = t.getAttribute('data-who');
      state.for = state.for === who ? '' : who;
      apply(true);
      bar.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  /* list or cards */
  var views = Array.prototype.slice.call(bar.querySelectorAll('[data-view]'));
  function setView(v) {
    list.classList.toggle('rows', v === 'rows'); list.classList.toggle('cards', v === 'cards');
    views.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-view') === v ? 'true' : 'false'); });
  }
  views.forEach(function (b) { b.addEventListener('click', function () { setView(b.getAttribute('data-view')); store('tk-view', b.getAttribute('data-view')); }); });
  setView(load('tk-view') === 'cards' ? 'cards' : 'rows');

  /* shortlist */
  var tray = document.querySelector('[data-tk-tray]');
  var sl = document.querySelector('[data-tk-sl]');
  var sc = document.querySelector('[data-tk-sc]');
  var short = [];
  try { short = JSON.parse(load('tk-short') || '[]') || []; } catch (e) { short = []; }
  var bySlug = {};
  items.forEach(function (it) { bySlug[it.getAttribute('data-slug')] = it; });
  /* the shortlist is shared with course pages; keep slugs we know, and titles saved by course pages */
  short = short.filter(function (s) { return bySlug[s]; });
  function draw() {
    items.forEach(function (it) { it.querySelector('[data-add]').setAttribute('aria-pressed', short.indexOf(it.getAttribute('data-slug')) > -1 ? 'true' : 'false'); });
    tray.hidden = short.length === 0 || (sl && sl.open);
    document.body.classList.toggle('tk-has-tray', short.length > 0);
    if (sc) sc.textContent = short.length;
    drawList();
    if (!short.length) return;
    var names = short.map(function (s) { return bySlug[s].getAttribute('data-title'); });
    tray.querySelector('[data-tk-n]').textContent = short.length === 1 ? '1 course on your shortlist' : short.length + ' courses on your shortlist';
    tray.querySelector('[data-tk-names]').textContent = names.join(', ');
    var body = 'Hello,\n\nI would like to talk about this training:\n' + names.map(function (n) { return '- ' + n; }).join('\n') +
      '\n\nWho it is for:\nRoughly how many people:\nWhen:\nWhere, or online:\n\nMy name, role and organisation:\n';
    var href = 'mailto:hello@thecareleaders.com?subject=' + encodeURIComponent('Training enquiry') + '&body=' + encodeURIComponent(body);
    Array.prototype.forEach.call(document.querySelectorAll('[data-tk-send]'), function (a) { a.href = href; });
  }
  list.addEventListener('click', function (e) {
    var b = e.target.closest('[data-add]'); if (!b) return;
    var s = b.closest('.tk-i').getAttribute('data-slug'), i = short.indexOf(s);
    if (i > -1) short.splice(i, 1); else short.push(s);
    store('tk-short', JSON.stringify(short));
    var titles = {}; try { titles = JSON.parse(load('tk-titles') || '{}') || {}; } catch (er) {}
    titles[s] = bySlug[s].getAttribute('data-title'); store('tk-titles', JSON.stringify(titles));
    draw();
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-tk-clear]'), function (b) {
    b.addEventListener('click', function () { short = []; store('tk-short', null); draw(); });
  });

  /* the shortlist itself: a dialog listing each course, with a link and a remove button */
  function drawList() {
    if (!sl) return;
    var ol = sl.querySelector('[data-tk-sl-list]');
    ol.innerHTML = '';
    short.forEach(function (s) {
      var it = bySlug[s], a = it.querySelector('a[href]');
      var li = document.createElement('li');
      var link = document.createElement('a'); link.href = a ? a.getAttribute('href') : '#'; link.textContent = it.getAttribute('data-title');
      var rm = document.createElement('button'); rm.type = 'button'; rm.className = 'tk-link'; rm.textContent = 'Remove';
      rm.setAttribute('aria-label', 'Remove ' + it.getAttribute('data-title') + ' from your shortlist');
      rm.addEventListener('click', function () {
        var i = short.indexOf(s); if (i > -1) short.splice(i, 1);
        store('tk-short', JSON.stringify(short)); draw();
        var next = ol.querySelector('button'); (next || sl.querySelector('[data-tk-close]')).focus();
      });
      li.appendChild(link); li.appendChild(rm); ol.appendChild(li);
    });
    sl.querySelector('[data-tk-sl-empty]').hidden = short.length > 0;
    sl.querySelector('[data-tk-sl-act]').hidden = short.length === 0;
  }
  function openList() {
    if (!sl) return;
    drawList();
    if (typeof sl.showModal === 'function') { if (!sl.open) sl.showModal(); } else sl.setAttribute('open', '');
    tray.hidden = true;
    sl.querySelector('[data-tk-close]').focus();
  }
  function closeList() {
    if (!sl) return;
    if (typeof sl.close === 'function' && sl.open) sl.close(); else sl.removeAttribute('open');
  }
  if (sl) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-tk-open]'), function (b) { b.addEventListener('click', openList); });
    sl.querySelector('[data-tk-close]').addEventListener('click', closeList);
    sl.addEventListener('click', function (e) { if (e.target === sl) closeList(); });
    sl.addEventListener('close', function () { draw(); var b = document.querySelector('[data-tk-open]'); if (b) b.focus(); });
    if (location.hash === '#shortlist') setTimeout(openList, 50);
  }

  apply(false); draw();
});
