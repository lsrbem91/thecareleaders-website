/* Training finder: filter course cards by who they are for and how they are delivered. All cards show until a choice is made. */
document.addEventListener('DOMContentLoaded', function () {
  var root = document.querySelector('[data-tf]');
  if (!root) return;
  var state = { aud: 'all', fmt: 'all' };
  var cards = Array.prototype.slice.call(document.querySelectorAll('.tl-card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('[data-tf-group]'));
  var count = document.querySelector('[data-tf-count]');
  var empty = document.querySelector('[data-tf-empty]');
  function has(card, key, val) { return val === 'all' || (' ' + (card.getAttribute('data-' + key) || '') + ' ').indexOf(' ' + val + ' ') > -1; }
  function apply() {
    var shown = 0;
    cards.forEach(function (c) { var ok = has(c, 'aud', state.aud) && has(c, 'fmt', state.fmt); c.hidden = !ok; if (ok) shown++; });
    groups.forEach(function (g) { g.hidden = !g.querySelector('.tl-card:not([hidden])'); });
    if (count) count.textContent = shown === 1 ? '1 course' : shown + ' courses';
    if (empty) empty.hidden = shown > 0;
    root.querySelectorAll('.tf-chip').forEach(function (b) {
      var k = b.hasAttribute('data-aud') ? 'aud' : 'fmt';
      b.setAttribute('aria-pressed', b.getAttribute('data-' + k) === state[k] ? 'true' : 'false');
    });
  }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('.tf-chip');
    if (b) { var k = b.hasAttribute('data-aud') ? 'aud' : 'fmt'; state[k] = b.getAttribute('data-' + k); apply(); }
    if (e.target.closest('[data-tf-reset]')) { state = { aud: 'all', fmt: 'all' }; apply(); }
  });
  apply();
});
