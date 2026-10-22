/* Our story: year roadmap (22 Oct 2026) */
(function () {
  var rm = document.querySelector('[data-rm]'); if (!rm) return;
  rm.classList.add('rm-js');
  var tabs = [].slice.call(rm.querySelectorAll('.rm-stop')), panels = [].slice.call(rm.querySelectorAll('.rm-p'));
  var track = rm.querySelector('.rm-track'), cur = 0, toast = document.querySelector('.st-toast'), tt;
  function go(i, focus, hash) {
    cur = (i + tabs.length) % tabs.length;
    tabs.forEach(function (t, k) { var on = k === cur; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; t.classList.toggle('rm-past', k < cur); });
    panels.forEach(function (p, k) { p.hidden = k !== cur; });
    var t = tabs[cur];
    track.scrollTo({ left: t.offsetLeft - track.clientWidth / 2 + t.offsetWidth / 2, behavior: 'smooth' });
    rm.style.setProperty('--rm-pn', cur / (tabs.length - 1));
    if (focus) t.focus();
    if (hash && history.replaceState) history.replaceState(null, '', '#y' + t.getAttribute('data-y'));
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { go(i, false, true); });
    t.addEventListener('keydown', function (e) {
      var k = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (k) { e.preventDefault(); go(cur + k, true, true); }
      if (e.key === 'Home') { e.preventDefault(); go(0, true, true); }
      if (e.key === 'End') { e.preventDefault(); go(tabs.length - 1, true, true); }
    });
  });
  rm.addEventListener('click', function (e) {
    if (e.target.closest('.rm-prev')) go(cur - 1, false, true);
    if (e.target.closest('.rm-next')) go(cur + 1, false, true);
    var b = e.target.closest('.st-share'); if (!b) return;
    var url = location.href.split('#')[0] + '#y' + b.getAttribute('data-share'), title = b.getAttribute('data-title') + ': The Care Leaders story';
    if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); return; }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(function () { say('Link copied.'); }, function () { say(url); });
    else say(url);
  });
  function say(t) { if (!toast) return; toast.textContent = t; toast.hidden = false; clearTimeout(tt); tt = setTimeout(function () { toast.hidden = true; }, 2600); }
  /* swipe on the panel */
  var x0 = null, box = rm.querySelector('.rm-panels');
  box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) go(cur + (dx < 0 ? 1 : -1), false, true); x0 = null; });
  var m = location.hash.match(/^#y(\d{4})$/), start = 0;
  if (m) tabs.forEach(function (t, i) { if (t.getAttribute('data-y') === m[1]) start = i; });
  go(start, false, false);
  if (m) setTimeout(function () { rm.scrollIntoView({ block: 'start' }); }, 60);
})();
