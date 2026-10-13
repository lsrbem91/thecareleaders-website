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
  var short = [];
  try { short = JSON.parse(load('tk-short') || '[]') || []; } catch (e) { short = []; }
  var bySlug = {};
  items.forEach(function (it) { bySlug[it.getAttribute('data-slug')] = it; });
  /* the shortlist is shared with course pages; keep slugs we know, and titles saved by course pages */
  short = short.filter(function (s) { return bySlug[s]; });
  function draw() {
    items.forEach(function (it) { it.querySelector('[data-add]').setAttribute('aria-pressed', short.indexOf(it.getAttribute('data-slug')) > -1 ? 'true' : 'false'); });
    tray.hidden = short.length === 0;
    document.body.classList.toggle('tk-has-tray', short.length > 0);
    if (!short.length) return;
    var names = short.map(function (s) { return bySlug[s].getAttribute('data-title'); });
    tray.querySelector('[data-tk-n]').textContent = short.length === 1 ? '1 course on your shortlist' : short.length + ' courses on your shortlist';
    tray.querySelector('[data-tk-names]').textContent = names.join(', ');
    var body = 'Hello,\n\nI would like to talk about this training:\n' + names.map(function (n) { return '- ' + n; }).join('\n') +
      '\n\nWho it is for:\nRoughly how many people:\nWhen:\nWhere, or online:\n\nMy name, role and organisation:\n';
    tray.querySelector('[data-tk-send]').href = 'mailto:hello@thecareleaders.com?subject=' + encodeURIComponent('Training enquiry') + '&body=' + encodeURIComponent(body);
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
  tray.querySelector('[data-tk-clear]').addEventListener('click', function () { short = []; store('tk-short', null); draw(); });

  apply(false); draw();
});
