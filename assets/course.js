/* Course pages (The Care Leaders Learning): tabs for what changes and formats, one-open session accordion,
   a shortlist shared with the Training page, and a slim bar that appears once the hero has scrolled away. */
document.addEventListener('DOMContentLoaded', function () {
  var page = document.querySelector('[data-course]');
  if (!page) return;
  var slug = page.getAttribute('data-course'), title = page.getAttribute('data-title');

  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function store(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }

  /* tabs: click, and arrow keys between tabs */
  Array.prototype.forEach.call(page.querySelectorAll('[data-tc-tabs]'), function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll('[role=tab]'));
    function pick(t, focus) {
      tabs.forEach(function (b) {
        var on = b === t;
        b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1;
        var p = document.getElementById(b.getAttribute('aria-controls')); if (p) p.hidden = !on;
      });
      if (focus) t.focus();
    }
    tabs.forEach(function (b, i) {
      b.addEventListener('click', function () { pick(b); });
      b.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (n) { e.preventDefault(); pick(tabs[(i + n + tabs.length) % tabs.length], true); }
      });
    });
  });

  /* one session open at a time, for browsers without <details name> */
  var sess = Array.prototype.slice.call(page.querySelectorAll('.tc-s'));
  sess.forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) sess.forEach(function (o) { if (o !== d && o.open) o.open = false; }); });
  });

  /* shortlist, shared with the Training page */
  var adds = Array.prototype.slice.call(page.querySelectorAll('[data-tc-add]'));
  var count = page.querySelector('[data-tc-count]');
  var view = page.querySelector('[data-tc-view]');
  var send = page.querySelector('[data-tc-send]');
  var askHref = send ? send.getAttribute('href') : '';
  function getShort() { try { return JSON.parse(load('tk-short') || '[]') || []; } catch (e) { return []; } }
  function getTitles() { try { return JSON.parse(load('tk-titles') || '{}') || {}; } catch (e) { return {}; } }
  function draw() {
    var short = getShort(), on = short.indexOf(slug) > -1;
    adds.forEach(function (b) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    var label = short.length ? (short.length === 1 ? 'View your shortlist (1 course)' : 'View your shortlist (' + short.length + ' courses)') : '';
    if (count) { count.textContent = label; count.hidden = !short.length; }
    if (view) { view.hidden = !short.length; view.querySelector('a').textContent = label; }
    if (send) {
      if (short.length > 1) {
        var t = getTitles();
        var names = short.map(function (s) { return t[s] || s.replace(/-/g, ' '); });
        var body = 'Hello,\n\nI would like to talk about this training:\n' + names.map(function (n) { return '- ' + n; }).join('\n') +
          '\n\nWho it is for:\nRoughly how many people:\nWhen:\nWhere, or online:\n\nMy name, role and organisation:\n';
        send.href = 'mailto:hello@thecareleaders.com?subject=' + encodeURIComponent('Training enquiry') + '&body=' + encodeURIComponent(body);
        send.textContent = 'Send one enquiry';
      } else { send.href = askHref; send.textContent = 'Ask about this course'; }
    }
  }
  adds.forEach(function (b) {
    b.addEventListener('click', function () {
      var short = getShort(), i = short.indexOf(slug), t = getTitles();
      if (i > -1) short.splice(i, 1); else { short.push(slug); t[slug] = title; store('tk-titles', JSON.stringify(t)); }
      store('tk-short', JSON.stringify(short)); draw();
    });
  });
  draw();

  /* slim bar once the hero is out of view */
  var bar = page.querySelector('[data-tc-bar]'), hero = page.querySelector('[data-tc-hero]');
  if (bar && hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      var gone = !es[0].isIntersecting;
      bar.hidden = !gone; document.body.classList.toggle('tc-has-bar', gone);
    }, { rootMargin: '-120px 0px 0px 0px' }).observe(hero);
  }
});
