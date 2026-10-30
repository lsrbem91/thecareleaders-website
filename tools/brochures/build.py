"""Build a Care Leaders Learning course brochure from a course data file.

Usage: python3 tools/brochures/build.py courses/nvr-essentials.json [out_dir]

One template for every training course. Page order:
 1 Cover  2 The problem it solves  3 Who it's for  4 Learning outcomes
 5-6 The course in detail  7 How you can run it (with fees)
 8 What every delegate gets  9 The online course and toolkit (if the course has one)
 10 Who delivers it and how to book

Design rule: no CSS shadows, filters, masks or opacity. They export as soft masks
that the iPhone PDF viewer draws as dark boxes.
"""
import html, json, os, sys, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent
A = SITE / 'assets'
e = lambda s: html.escape(s, quote=True)

def page(inner, cls='', n=None, name=''):
    foot = f'<div class="foot"><span>{e(name)} · Course brochure</span><span>{n}</span></div>' if n else ''
    return f'<section class="pg {cls}">{inner}{foot}<div class="bar"><i></i><i></i><i></i><i></i></div></section>'

def build(c):
    acc = c['accent']; name = c['name']; P = []
    eyebrow = lambda t: f'<p class="eb"><b></b>{e(t)}</p>'
    hs = c['headline'].split('. ', 1)
    head = f'{e(hs[0])}.<span class="lime"> {e(hs[1])}</span>' if len(hs) == 2 else e(c['headline'])

    # 1 Cover
    facts = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in c['facts'])
    P.append(page(f'''
      <img class="logo" src="{A}/img/tcll/tcll-logo-white.png" alt="The Care Leaders Learning">
      <p class="tagr">Course brochure</p>
      <div class="cov">
        <span class="cat">{e(c['category'])}</span>
        <h2 class="cname">{e(name)}</h2>
        <h1>{head}</h1>
        <p class="intro">{e(c['intro'])}</p>
      </div>
      <img class="covimg" src="{A}/img/tcll/{c['cover_image']}" alt="">
      <dl class="facts">{facts}</dl>''', 'dark cover'))

    # 2 Problem
    pr = c['problem']
    tags = ''.join(f'<span class="tag">{e(t)}</span>' for t in pr['helps_with'])
    body = ''.join(f'<p>{e(b)}</p>' for b in pr['body'])
    P.append(page(f'''
      <div class="col2">
        <div>{eyebrow('The problem it solves')}
          <p class="big">{e(pr['lead'])}</p>{body}
          <p class="lbl">Helps with</p><div class="tags">{tags}</div>
        </div>
        <aside class="evid"><img src="{A}/img/tcll/icon-theory-triangle.png" alt="">
          <h3>{e(pr['evidence_title'])}</h3><p>{e(pr['evidence'])}</p></aside>
      </div>''', 'light', 2, name))

    # 3 Who it's for
    groups = ''.join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in c['audience']['groups'])
    notes = ''.join(f'<li><img src="{A}/img/tcll/tick.png" alt="">{e(x)}</li>' for x in c['audience']['notes'])
    P.append(page(f'''{eyebrow("Who it's for")}<h2>Who it's for.</h2>
      <div class="who"><div class="cards4">{groups}</div><ul class="ticks">{notes}</ul></div>''', 'bed', 3, name))

    # 4 Outcomes
    outs = ''.join(f'<li><span>{i}</span><p>{e(o)}</p></li>' for i, o in enumerate(c['outcomes'], 1))
    P.append(page(f'''{eyebrow('Learning outcomes')}<h2>By the end of the course, people will be able to:</h2>
      <ol class="outs">{outs}</ol>''', 'light', 4, name))

    # 5-6 Course in detail, two parts per page
    def part(i, p):
        return f'''<article class="part"><div class="ph"><span class="pn">{i}</span><div><h3>{e(p['title'])}</h3><p class="when">{e(p['when'])}</p></div></div>
          <div class="sta"><img src="{A}/img/tcll/icon-story-speech.png" alt=""><p><b>Story.</b> {e(p['story'])}</p></div>
          <div class="sta"><img src="{A}/img/tcll/icon-theory-triangle.png" alt=""><p><b>Theory.</b> {e(p['theory'])}</p></div>
          <div class="sta"><img src="{A}/img/tcll/icon-action-chevrons.png" alt=""><p><b>Action.</b> {e(p['action'])}</p></div>
          <p class="leave"><b>You leave with</b> {e(p['leave'])}</p></article>'''
    parts = c['parts']
    for k in range(0, len(parts), 2):
        intro = f'<p class="sub">{e(c["story_line"])}</p>' if k == 0 else '<p class="sub">Every part runs Story, Theory, Action: a moment from the story, the thinking behind it, then something people practise.</p>'
        title = 'The course in detail.' if k == 0 else 'The course in detail, continued.'
        P.append(page(f'''{eyebrow('The course')}<h2>{title}</h2>{intro}
          <div class="parts">{''.join(part(k + j + 1, p) for j, p in enumerate(parts[k:k + 2]))}</div>''', 'light', len(P) + 1, name))

    # 7 How you can run it
    def fmt(f):
        rows = ''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in f['rows'])
        return f'''<article class="fmt"><p class="fl">{e(f['label'])}</p><p class="flen">{e(f['length'])}</p>
          <p class="fee">{e(f['fee'])} <small>{e(f['fee_note'])}</small></p><p>{e(f['desc'])}</p><dl>{rows}</dl></article>'''
    P.append(page(f'''{eyebrow('How you can run it')}<h2>Face to face or live online.</h2>
      <div class="fmts">{''.join(fmt(f) for f in c['formats'])}</div><p class="fnote">{e(c['fees_note'])}</p>''', 'bed', len(P) + 1, name))

    # 8 What every delegate gets
    tk = c.get('toolkit')
    online = f"{tk['name']}, our {tk['kind'].lower()}" if tk else 'The online course'
    gets = [
        ('A workbook for life', 'Every delegate gets their own workbook, with the stories, the tools and space to plan. Theirs to keep forever.'),
        ('The recording, for 12 months', 'A recording of the session, so people can catch up or go back over a part.'),
        (f"{tk['name']}, for 12 months" if tk else 'The online course, for 12 months', f"{online} on The Care Leaders Online, covering the same ground in more depth." ),
        ('A certificate of completion', 'For each delegate, to keep for their own development record.'),
        ('50% off The Care Leaders Online', "Half price on an individual annual membership for their first 12 months: on-demand courses, talks from speakers across the country and practice tools."),
    ]
    g = ''.join(f'<div class="get"><img src="{A}/img/tcll/tick.png" alt=""><div><h3>{e(a)}</h3><p>{e(b)}</p></div></div>' for a, b in gets)
    P.append(page(f'''<div class="col2 w">
        <div>{eyebrow('Included for every delegate')}<h2>Every delegate gets more than the day.</h2>
          <p class="sub">Face to face or online, the same package comes with every course.</p>
          <img class="sideimg" src="{A}/img/tcll/{c['side_image']}" alt=""></div>
        <div class="gets">{g}</div></div>''', 'dark inner', len(P) + 1, name))

    # 9 Toolkit
    if tk:
        secs = ''.join(f'<li><span>{i:02d}</span>{e(s)}</li>' for i, s in enumerate(tk['sections'], 1))
        tools = ''.join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in tk['tools'])
        P.append(page(f'''{eyebrow(tk['kind'])}<h2>{e(tk['name'])}: the online course and its tools.</h2>
          <p class="sub wide">{e(tk['intro'])}</p>
          <div class="tk"><div class="secs"><p class="lbl">The course, section by section</p><ol>{secs}</ol></div>
          <div><p class="lbl">The tools inside it</p><ul class="tools">{tools}</ul></div></div>''', 'light', len(P) + 1, name))

    # 10 Who delivers + booking
    rel = ''.join(f'<div><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in c.get('related', []))
    P.append(page(f'''
      <div class="col2 w">
        <div><img class="logo2" src="{A}/img/tcll/tcll-logo-white.png" alt="The Care Leaders Learning">
          {eyebrow('Who designs and delivers it')}<h2>From care leaver to care leader.</h2>
          <p class="bio">Every course is designed by Luke Rodgers BEM and follows the same Story, Theory, Action approach. Luke went into care at 10, and has spent his career since inside children's services as a consultant, trainer, keynote speaker and national engagement lead. He led the national engagement on England's new fostering standards, was a Knowledge Equity Fellow at Saïd Business School, University of Oxford, and was awarded the British Empire Medal in 2018.</p>
          <p class="bio">Courses are delivered by people with lived experience of care and professional experience of children's services.</p>
        </div>
        <div>{eyebrow('How to book')}<h2>Bring {e(name)} to your team.</h2>
          <ol class="steps"><li><b>Get in touch</b> with your date, format and roughly how many people.</li>
            <li><b>We send your fee and hold the date</b> for 14 days.</li>
            <li><b>Confirm by email</b> to secure the booking.</li>
            <li><b>We plan it with you</b> on a short call, shaped around your service.</li></ol>
          <p class="mail">hello@thecareleaders.com</p>
          {f'<div class="rel"><p class="lbl">Often booked with</p>{rel}</div>' if rel else ''}
        </div></div>
      <p class="legal">Gold, Dual Perspective Leadership Award, iESE Public Sector Transformation Awards 2026 · Children &amp; Young People Now Workforce Development Award 2023 · The Care Leaders Ltd, company number 10782615 · thecareleaders.com</p>''', 'dark back'))

    css = (HERE / 'brochure.css').read_text().replace('{ACC}', acc).replace('{A}', str(A))
    return f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{e(name)}: course brochure</title><style>{css}</style></head><body>{"".join(P)}</body></html>'

if __name__ == '__main__':
    src = pathlib.Path(sys.argv[1]); src = src if src.is_absolute() else (HERE / src if (HERE / src).exists() else src)
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else SITE / 'assets/docs/brochures'
    c = json.loads(src.read_text())
    h = out / f"{c['slug']}.html"; h.write_text(build(c))
    pdf = out / f"{c['slug']}.pdf"
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{h}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.pdf({{path:'{pdf}',width:'1280px',height:'720px',printBackground:true,margin:{{top:0,right:0,bottom:0,left:0}}}});
await b.close()}})();"""
    subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
    print(pdf)
