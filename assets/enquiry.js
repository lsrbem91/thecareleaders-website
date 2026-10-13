/* Enquiry form: posts to Web3Forms, which emails hello@thecareleaders.com. Works without page reloads;
   falls back to a plain email link if the service can't be reached. */
var ENQ_OPTIONS = {"Consultancy": ["Transformation and service design", "Participation and co-production", "Employment and pathways", "Not sure yet"], "Fostering, with Why Care": [], "A programme": ["The Designated Leaders Programme", "The Care Leaders Academy", "Care to Work", "The Care Leaders Fellowship", "The NVR Programme"], "Training for my team": ["The Journey Through Care", "Behind the Behaviour", "Trauma, Attachment and Transitions", "Living a Careless Life", "Supporting Boys in Care", "Tools for Schools", "Two Timetables: When School Meets Social Care", "Raising Aspirations", "NVR Essentials", "NVR Advanced", "The Practice Toolkit", "Care Not Custody", "A guide to good recording", "From Case Note to Letter", "Language that Lifts", "Profiles that Find the Right Home", "Participation that Changes Decisions", "Working Alongside Lived Experience", "How to be a Mentor", "Power to Lead", "Story, Theory, Action: The Facilitator Programme", "Ready for Inspection: Hearing Children’s Lived Experience", "Corporate Parenting in Practice", "Leading Care Leavers at Work", "Be the First Yes", "The Person Behind the File", "Co-producing your Care Leaver Local Offer", "Not sure yet, help me choose"], "A keynote or conference workshop": ["Living a Careless Life", "Just Say Yes", "The Power of the Profile", "Tools for Schools", "Lived Experience Leadership", "From Care Leaver to Care Leader", "Be the First Yes", "Not sure yet, help me choose"], "Something else": []};
document.addEventListener('DOMContentLoaded', function () {
  var forms = document.querySelectorAll('form[data-enquiry]');
  if (!forms.length) return;
  var qs = {}; try { qs = Object.fromEntries(new URLSearchParams(location.search)); } catch (e) {}
  forms.forEach(function (f) {
    var topic = f.querySelector('[name=topic]'), msg = f.querySelector('[name=message]');
    var itemWrap = f.querySelector('[data-item-wrap]'), item = f.querySelector('[name=item]');
    function fillItems(keep) {
      var list = ENQ_OPTIONS[topic.value] || [];
      item.innerHTML = '<option value="">Choose one</option>' + list.map(function (o) { return '<option>' + o.replace(/</g, '&lt;') + '</option>'; }).join('');
      itemWrap.hidden = !list.length; item.required = !!list.length;
      if (keep && list.indexOf(keep) > -1) item.value = keep;
    }
    topic.addEventListener('change', function () { fillItems(''); });
    fillItems(f.getAttribute('data-item') || '');
    if (qs.about && msg && !msg.value) { msg.value = 'About: ' + qs.about + '\n\n'; if (topic && !topic.value) { topic.value = 'Training for my team'; fillItems(qs.about); } }
    var status = f.querySelector('[data-status]'), btn = f.querySelector('button[type=submit]');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      var data = new FormData(f);
      /* the subject carries topic, name and email so the Power Automate flow on hello@ can send the right auto-reply */
      data.set('subject', 'Website enquiry | ' + (data.get('topic') || 'Something else') + ' | ' + (data.get('item') || '-') + ' | ' + (data.get('name') || '').replace(/\|/g, '') + ' | ' + (data.get('email') || '').trim());
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
