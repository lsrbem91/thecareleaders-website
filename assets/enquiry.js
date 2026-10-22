/* One enquiry form for the whole site. Posts to Web3Forms, which emails hello@thecareleaders.com.
   The topic choice shows that topic's questions. The subject line and the JSON block at the end of the
   email are what the Power Automate flow on hello@ reads to send the right automatic reply. */
var ENQ_OPTIONS = {"Consultancy": ["Transformation and service design", "Participation and co-production", "Employment and pathways", "Not sure yet"], "Fostering, with Why Care": [], "A programme": ["The Designated Leaders Programme", "The Care Leaders Academy", "Care to Work", "The Care Leaders Fellowship", "The NVR Programme", "Mentors Who Care"], "Training for my team": ["Behind the Behaviour", "Trauma, Attachment and Transitions", "Living a Careless Life", "Supporting Boys in Care", "Tools for Schools", "Two Timetables: When School Meets Social Care", "Raising Aspirations", "NVR Essentials", "The Practice Toolkit", "Care Not Custody", "A Guide to Good Recording", "Language that Lifts", "Working Alongside Lived Experience", "Power to Lead", "Corporate Parenting in Practice", "Leading Care Leavers at Work", "Be the First Yes", "The Person Behind the File", "Co-producing your Care Leaver Local Offer", "Not sure yet, help me choose"], "A keynote or conference workshop": ["Living a Careless Life", "Just Say Yes", "The Power of the Profile", "Tools for Schools", "Lived Experience Leadership", "From Care Leaver to Care Leader", "Be the First Yes", "Not sure yet, help me choose"], "Something else": []};
var KEYNOTE = 'A keynote or conference workshop', TRAINING = 'Training for my team';
var DONE = {
  'Consultancy': 'Luke or one of our consultants will be in touch to suggest a first conversation about your service.',
  'Fostering, with Why Care': 'We&#8217;ll be in touch to suggest a first conversation with the Why Care team.',
  'A programme': 'We&#8217;ll send you the programme details and suggest a short call.',
  'Training for my team': 'We&#8217;ll check Luke&#8217;s diary for your date and email you his availability, the fee and what&#8217;s included.',
  'A keynote or conference workshop': 'We&#8217;ll check Luke&#8217;s diary for your date and email you his availability, the fee and the talk we&#8217;d recommend for your audience.',
  'Something else': 'We&#8217;ll read your message and get back to you.'
};
document.addEventListener('DOMContentLoaded', function () {
  var forms = document.querySelectorAll('form[data-enquiry]');
  if (!forms.length) return;
  var qs = {}; try { qs = Object.fromEntries(new URLSearchParams(location.search)); } catch (e) {}
  forms.forEach(function (f) {
    var topic = f.querySelector('[name=topic]'), msg = f.querySelector('[name=message]');
    var itemWrap = f.querySelector('[data-item-wrap]'), item = f.querySelector('[name=item]');
    var itemLabel = f.querySelector('[data-item-label]'), msgLabel = f.querySelector('[data-msg-label]');
    function show(sec, on) { var el = f.querySelector('[data-sec=' + sec + ']'); if (!el) return; el.hidden = !on; el.disabled = !on; }
    function sync() {
      var t = topic.value, it = item.value;
      var ev = t === KEYNOTE || t === TRAINING;
      show('keynote', ev);
      var ses = f.querySelector('[name=session]'); if (ses) { var sl = ses.closest('label'); sl.hidden = t !== KEYNOTE; ses.disabled = t !== KEYNOTE; }
      var leg = f.querySelector('[data-sec=keynote] legend'); if (leg) leg.textContent = t === TRAINING ? 'About your training' : 'About your event';
      var tod = f.querySelector('[name=time_of_day]');
      if (tod) {
        var tl = tod.closest('label'), hint = f.querySelector('[data-tr-hint]');
        if (!hint) { hint = document.createElement('p'); hint.setAttribute('data-tr-hint', ''); hint.className = 'enq-hint'; hint.style.cssText = 'margin:0 0 14px;font-size:15px;line-height:1.5'; hint.textContent = 'Face to face, every course runs for 6 hours, usually 10am to 4pm. Online, it is a 2-hour live session. Up to 60 people.'; tl.parentNode.parentNode.insertBefore(hint, tl.parentNode.nextSibling); }
        if (t === TRAINING) { tl.hidden = true; tod.value = 'Full day'; hint.hidden = false; }
        else { tl.hidden = false; hint.hidden = true; }
      }
      show('fellowship', it === 'The Care Leaders Fellowship');
      itemLabel.textContent = t === KEYNOTE ? 'Which talk are you interested in?' : t === TRAINING ? 'Which course?' : 'Which one?';
      msgLabel.textContent = t === KEYNOTE ? 'Tell us about your event and what you want people to leave with' : t === TRAINING ? 'Tell us about your team and what you want them to leave with' : 'Tell us what you need';
    }
    function fillItems(keep) {
      var list = ENQ_OPTIONS[topic.value] || [];
      item.innerHTML = '<option value="">Choose one</option>' + list.map(function (o) { return '<option>' + o.replace(/</g, '&lt;') + '</option>'; }).join('');
      itemWrap.hidden = !list.length; item.required = !!list.length; item.disabled = !list.length;
      if (keep && list.indexOf(keep) > -1) item.value = keep;
      sync();
    }
    topic.addEventListener('change', function () { fillItems(''); });
    item.addEventListener('change', sync);
    if (qs.topic === 'keynote') topic.value = KEYNOTE;
    if (qs.topic === 'training' || f.getAttribute('data-topic') === 'training') topic.value = TRAINING;
    if (qs.topic === 'programme') topic.value = 'A programme';
    if (qs.topic === 'programme' && qs.course === 'NVR Advanced') qs.course = 'The NVR Programme';
    fillItems(qs.talk || qs.course || f.getAttribute('data-item') || '');
    if (qs.about && msg && !msg.value) { msg.value = 'About: ' + qs.about + '\n\n'; if (!topic.value) { topic.value = 'Training for my team'; fillItems(qs.about); } }
    document.addEventListener('enq:talk', function (e) { topic.value = KEYNOTE; fillItems(e.detail || ''); });
    var status = f.querySelector('[data-status]'), btn = f.querySelector('button[type=submit]');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      var data = new FormData(f), t = data.get('topic') || 'Something else';
      var page = location.pathname.split('/').pop() || 'index.html';
      var name = (data.get('name') || '').trim();
      var rec = { topic: t, item: data.get('item') || '', first_name: name.split(/\s+/)[0], name: name, role: data.get('role') || '',
        organisation: data.get('organisation') || '', email: (data.get('email') || '').trim(), phone: data.get('phone') || '', page: page };
      ['event_date', 'time_of_day', 'format', 'venue', 'session', 'audience', 'numbers', 'mobile', 'fel_ask'].forEach(function (k) { if (data.has(k)) rec[k] = data.get(k); });
      data.set('subject', 'Website enquiry | ' + t + ' | ' + (rec.item || '-') + ' | ' + name.replace(/\|/g, '') + ' | ' + rec.email);
      data.set('page', page);
      data.set('zz_flow_data', 'FLOWDATA' + btoa(unescape(encodeURIComponent(JSON.stringify(rec)))) + 'ENDFLOWDATA');
      btn.disabled = true; btn.textContent = 'Sending…'; status.textContent = ''; status.className = 'enq-status';
      fetch('https://api.web3forms.com/submit', { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.success, j: j }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error(res.j && res.j.message);
          f.reset(); f.hidden = true;
          var done = f.parentNode.querySelector('[data-done]'), line = done.querySelector('[data-done-line]');
          if (line && DONE[t]) line.innerHTML = DONE[t] + ' We reply within 3 working days.';
          done.hidden = false; done.focus();
        })
        .catch(function () {
          btn.disabled = false; btn.textContent = 'Send enquiry';
          status.className = 'enq-status enq-err';
          status.innerHTML = 'Sorry, that didn&#8217;t send. Please email <a href="mailto:hello@thecareleaders.com">hello@thecareleaders.com</a>.';
        });
    });
  });
});
