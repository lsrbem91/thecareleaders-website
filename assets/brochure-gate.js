/* Brochure gate: adds the person to The Care Leaders newsletter audience in Mailchimp,
   tags them with the brochure, then opens the PDF. Uses Mailchimp's JSONP endpoint so
   the visitor stays on the page. */
(function () {
  var MC = 'https://thecareleaders.us20.list-manage.com/subscribe/post-json?u=59c462198d19ae06ac1668f73&id=59f81c6487&f_id=00a201eef0';
  /* Mailchimp embedded forms apply tags by ID, not name. IDs from Audience > Tags. */
  var TAGS = {
    'brochure-fellowship': '4229739', 'brochure-academy': '4229740',
    'brochure-designated-leaders': '4229741', 'brochure-care-to-work': '4229742',
    'brochure-care-to-work-we': '4229743', 'brochure-care-to-work-aj': '4229744',
    'keynote-living-a-careless-life': '4229745'
  };
  var n = 0;
  function jsonp(url, cb) {
    var name = 'mcgate' + (++n) + Date.now(), s = document.createElement('script'), done = false;
    window[name] = function (r) { done = true; cb(r); delete window[name]; s.remove(); };
    s.src = url + '&c=' + name;
    s.onerror = function () { if (!done) cb({ result: 'error', msg: 'network' }); };
    document.body.appendChild(s);
    setTimeout(function () { if (!done) cb({ result: 'error', msg: 'timeout' }); }, 12000);
  }
  document.querySelectorAll('form[data-gate]').forEach(function (f) {
    var msg = f.querySelector('.br-msg'), btn = f.querySelector('button[type=submit]');
    var dl = f.parentNode.querySelector('.br-done');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      var pick = f.querySelector('input[name=brochure]:checked');
      var pdf = pick ? pick.value : f.dataset.pdf;
      var tag = pick ? pick.dataset.tag : f.dataset.tag;
      var q = [];
      f.querySelectorAll('input,select').forEach(function (i) {
        if (!i.name || i.name === 'brochure' || ((i.type === 'checkbox' || i.type === 'radio') && !i.checked)) return;
        q.push(encodeURIComponent(i.name) + '=' + encodeURIComponent(i.value));
      });
      if (tag) q.push('tags=' + encodeURIComponent(TAGS[tag] || tag));
      btn.disabled = true; msg.hidden = false; msg.textContent = 'Getting your brochure…';
      jsonp(MC + '&' + q.join('&'), function (r) {
        var ok = r.result === 'success' || r.result === 'redirect' || /already subscribed|too many recent signup/i.test(r.msg || '');
        btn.disabled = false;
        if (!ok && r.msg !== 'network' && r.msg !== 'timeout') {
          msg.textContent = (r.msg || 'Something went wrong.').replace(/^\d+ - /, '').replace(/<[^>]+>/g, '');
          return;
        }
        if (dl) {
          dl.querySelector('a').href = pdf;
          f.hidden = true; dl.hidden = false; dl.focus();
        }
        var a = document.createElement('a'); a.href = pdf; a.download = pdf.split('/').pop();
        document.body.appendChild(a); a.click(); a.remove();
      });
    });
  });
})();
