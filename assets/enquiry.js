/* Enquiry form: posts to Web3Forms, which emails hello@thecareleaders.com. Works without page reloads;
   falls back to a plain email link if the service can't be reached. */
document.addEventListener('DOMContentLoaded', function () {
  var forms = document.querySelectorAll('form[data-enquiry]');
  if (!forms.length) return;
  var qs = {}; try { qs = Object.fromEntries(new URLSearchParams(location.search)); } catch (e) {}
  forms.forEach(function (f) {
    var topic = f.querySelector('[name=topic]'), msg = f.querySelector('[name=message]');
    if (qs.about && msg && !msg.value) { msg.value = 'About: ' + qs.about + '\n\n'; if (topic && !topic.value) topic.value = 'Training for my team'; }
    var status = f.querySelector('[data-status]'), btn = f.querySelector('button[type=submit]');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      var data = new FormData(f);
      data.set('subject', 'Website enquiry: ' + (data.get('topic') || 'General') + ' (' + (data.get('name') || '') + ')');
      data.set('page', location.pathname.split('/').pop() || 'index.html');
      btn.disabled = true; btn.textContent = 'Sending…'; status.textContent = ''; status.className = 'enq-status';
      fetch('https://api.web3forms.com/submit', { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.success, j: j }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error(res.j && res.j.message);
          f.reset(); f.hidden = true;
          var done = f.parentNode.querySelector('[data-done]'); done.hidden = false; done.focus();
        })
        .catch(function () {
          btn.disabled = false; btn.textContent = 'Send enquiry';
          status.className = 'enq-status enq-err';
          status.innerHTML = 'Sorry, that didn&#8217;t send. Please email <a href="mailto:hello@thecareleaders.com">hello@thecareleaders.com</a> or call 0800 233 5597.';
        });
    });
  });
});
