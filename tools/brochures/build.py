"""Build a Care Leaders Learning course brochure from a course data file.

Usage: python3 tools/brochures/build.py courses/nvr-essentials.json [out_dir]

One template for every training course. Show, don't tell: each page leads with
a graphic, a big number or a short headline, with detail underneath.
Sections (shown in the navigation strip on every inner page):
 Problem · Who · Outcomes · The day · Formats and fees · Included · Online course · Book

Design rule: no CSS shadows, filters, masks or opacity. They export as soft masks
that the iPhone PDF viewer draws as dark boxes.
"""
import html, json, os, sys, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent
A = SITE / 'assets'
e = lambda s: html.escape(s, quote=True)

ICONS = {
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'group': '<path d="M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 11a3 3 0 1 0 0-6M18 14c2 .8 3 3 3 6"/>',
 'pound': '<path d="M16 6.5A3.5 3.5 0 0 0 9.5 8v4.5c0 3-1 5.5-3 7.5h11M6.5 12.5h7"/>',
 'gift': '<path d="M4 11h16v9H4zM3 7h18v4H3zM12 7v13M12 7c-1.5-3-5-3.5-5-1s3 1 5 1c2 0 5 1.5 5-1s-3.5-2-5 1"/>',
 'home': '<path d="M3 11l9-7 9 7M5 9.5V20h5v-6h4v6h5V9.5"/>',
 'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 'hands': '<path d="M7 11a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM2.5 20c0-2.8 2-5 4.5-5s4.5 2.2 4.5 5M16.5 13a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM13 20c0-2.2 1.6-4 3.5-4s3.5 1.8 3.5 4"/>',
 'clipboard': '<path d="M8 4h8v3H8zM6 5.5H5v15h14v-15h-1M8.5 12l2 2 4-4.5"/>',
 'room': '<path d="M3 4h18v11H3zM12 15v5M8 20h8M7 8h6M7 11h9"/>',
 'laptop': '<path d="M5 5h14v10H5zM2 19h20l-2-4H4z"/>',
 'book': '<path d="M4 4.5h6a2 2 0 0 1 2 2V20a2 2 0 0 0-2-2H4zM20 4.5h-6a2 2 0 0 0-2 2V20a2 2 0 0 1 2-2h6z"/>',
 'play': '<path d="M3 5h18v14H3zM10 9v6l5-3z"/>',
 'award': '<path d="M12 14a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM8.5 13l-1.5 8 5-3 5 3-1.5-8"/>',
 'tag': '<path d="M3 3h8l10 10-8 8L3 11zM7.5 7.5h.01M10 16l6-6"/>',
 'cross': '<path d="M6 6l12 12M18 6L6 18"/>',
 'tick': '<path d="M4 12.5l5 5L20 6.5"/>',
}
def ico(name, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

NAV = [('problem', 'Problem'), ('who', "Who it's for"), ('outcomes', 'Outcomes'), ('day', 'The course'),
       ('formats', 'Formats and fees'), ('included', 'Included'), ('online', 'Online course'), ('book', 'Book')]

def nav(cur, has_online):
    items = [n for n in NAV if has_online or n[0] != 'online']
    return '<nav class="nav">' + ''.join(f'<span class="{"on" if k == cur else ""}">{e(t)}</span>' for k, t in items) + '</nav>'

def page(inner, cls='', sec=None, c=None, n=None):
    top = nav(sec, bool(c.get('toolkit'))) if sec else ''
    foot = f'<div class="foot"><span>{e(c["name"])} · Course brochure</span><span>{n}</span></div>' if n else ''
    return f'<section class="pg {cls}">{top}{inner}{foot}<div class="bar"><i></i><i></i><i></i><i></i></div></section>'

def build(c):
    acc = c['accent']; name = c['name']; P = []
    num = lambda: len(P) + 1
    hs = c['headline'].split('. ', 1)
    head = f'{e(hs[0])}.<br><span class="lime">{e(hs[1])}</span>' if len(hs) == 2 else e(c['headline'])

    # 1 Cover: the whole offer at a glance
    glance = ''.join(f'<div class="gl">{ico(i)}<b>{e(big)}</b><span>{e(lab)}</span><small>{e(sm)}</small></div>' for i, big, lab, sm in c['glance'])
    P.append(page(f'''
      <img class="logo" src="{A}/img/tcll/tcll-logo-white.png" alt="The Care Leaders Learning">
      <p class="tagr">Course brochure</p>
      <div class="cov"><span class="cat">{e(c['category'])}</span>
        <h1 class="cname">{e(name)}</h1><p class="hl">{head}</p><p class="intro">{e(c['intro'])}</p></div>
      <img class="covimg" src="{A}/img/tcll/{c['cover_image']}" alt="">
      <div class="glance">{glance}</div>''', 'dark cover', c=c))

    # 2 Problem: before and after
    pr = c['problem']
    wo = ''.join(f'<li>{ico("cross", "mk")}{e(x)}</li>' for x in pr['without'])
    wi = ''.join(f'<li>{ico("tick", "mk")}{e(x)}</li>' for x in pr['with'])
    P.append(page(f'''
      <div class="scene"><p class="s1">{e(pr['scene'])}</p><p class="s2">{e(pr['question'])}</p></div>
      <div class="ba"><div class="b bad"><p class="bh">Without a shared approach</p><ul>{wo}</ul></div>
        <div class="arrow"></div>
        <div class="b good"><p class="bh">After {e(name)}</p><ul>{wi}</ul></div></div>
      <div class="pnotes"><p><b>Why it matters.</b> {e(pr['standards'])}</p><p><b>Evidence.</b> {e(pr['evidence'])}</p></div>''',
      'light', 'problem', c, num()))

    # 3 Who
    groups = ''.join(f'<div class="wt">{ico(i)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in c['audience']['groups'])
    notes = ''.join(f'<span>{ico("tick", "mk")}{e(x)}</span>' for x in c['audience']['notes'])
    P.append(page(f'''<h2 class="ph">Who it's for</h2>
      <div class="wts">{groups}</div><div class="chips">{notes}</div>''', 'bed', 'who', c, num()))

    # 4 Outcomes
    outs = ''.join(f'<div class="ot"><span class="on">{i}</span><h3>{e(h)}</h3><p>{e(d)}</p></div>' for i, (h, d) in enumerate(c['outcomes'], 1))
    P.append(page(f'''<h2 class="ph">By the end of the day, people can</h2><div class="ots">{outs}</div>''', 'light', 'outcomes', c, num()))

    # 5 The day: timeline
    parts = c['parts']; half = len(parts) // 2
    def blk(i, p):
        return f'<div class="tb"><span class="tn">{i}</span><h3>{e(p["title"])}</h3><p class="ts">{e(p["theory"])}</p><p class="lv">{ico("gift", "mk")}{e(p["leave"])}</p></div>'
    am = ''.join(blk(i + 1, p) for i, p in enumerate(parts[:half]))
    pm = ''.join(blk(i + 1 + half, p) for i, p in enumerate(parts[half:]))
    P.append(page(f'''<h2 class="ph">The day at a glance</h2>
      <div class="tl"><div class="tt"><span>10am</span><span>Lunch</span><span>4pm</span></div>
        <div class="trow"><div class="half"><p class="hl2">Morning</p><div class="tbs">{am}</div></div>
        <div class="lunch">Lunch</div>
        <div class="half"><p class="hl2">Afternoon</p><div class="tbs">{pm}</div></div></div></div>
      <p class="tln">{ico("gift", "mk")} = what people leave with, ready to use on their next shift.</p>''', 'bed', 'day', c, num()))

    # 6 Story, Theory, Action grid
    rows = ''.join(f'''<div class="gr"><div class="gp"><span class="tn">{i}</span>{e(p["title"])}</div>
        <div class="gs">{e(p["story"])}</div><div class="gt">{e(p["theory"])}</div><div class="ga">{e(p["action"])}</div></div>'''
        for i, p in enumerate(parts, 1))
    P.append(page(f'''<h2 class="ph">How every part works</h2>
      <div class="grid"><div class="gh"><div></div>
        <div><img src="{A}/img/tcll/icon-story-speech.png" alt="">Story<small>A moment from care</small></div>
        <div><img src="{A}/img/tcll/icon-theory-triangle.png" alt="">Theory<small>The thinking behind it</small></div>
        <div><img src="{A}/img/tcll/icon-action-chevrons.png" alt="">Action<small>What people practise</small></div></div>{rows}</div>
      <p class="tln">{e(c['story_line'])}</p>''', 'light', 'day', c, num()))

    # 7 Formats and fees
    def fmt(f):
        pts = ''.join(f'<li>{ico("tick", "mk")}{e(x)}</li>' for x in f['points'])
        return f'''<div class="fc">{ico(f['icon'], 'fic')}<p class="fl">{e(f['label'])}</p>
          <p class="flen">{e(f['length'])}<small>{e(f['time'])}</small></p>
          <p class="fee">{e(f['fee'])}<small>{e(f['fee_note'])}</small></p><ul>{pts}</ul></div>'''
    P.append(page(f'''<h2 class="ph">Face to face or live online</h2>
      <div class="fcs">{''.join(fmt(f) for f in c['formats'])}</div>
      <p class="fnote">{ico("group", "mk")}{e(c['fees_note'])}</p>''', 'bed', 'formats', c, num()))

    # 8 Included
    gets = ''.join(f'<div class="gi">{ico(i)}<b>{e(t)}</b><span>{e(s)}</span><p>{e(d)}</p></div>' for i, t, s, d in c['gets'])
    P.append(page(f'''<h2 class="ph">Every delegate gets</h2><p class="phs">Face to face or online. Included in the fee.</p>
      <div class="gis">{gets}</div>''', 'dark inner', 'included', c, num()))

    # 9 Online course and toolkit
    tk = c.get('toolkit')
    if tk:
        path = ''.join(f'<li><span>{i}</span>{e(s)}</li>' for i, s in enumerate(tk['sections'], 1))
        tools = ''.join(f'<div class="tool"><span>{i:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i, (a, b) in enumerate(tk['tools'], 1))
        P.append(page(f'''<div class="tkh"><div><span class="cat">{e(tk['kind'])}</span><h2 class="ph">{e(tk['name'])}</h2>
          <p class="phs">{e(tk['intro'])}</p></div>
          <div class="screen"><div class="sbar"><i></i><i></i><i></i></div><ol class="path">{path}</ol></div></div>
          <p class="lbl">{len(tk['tools'])} interactive tools inside</p><div class="tools">{tools}</div>''', 'light', 'online', c, num()))

    # 10 Book
    rel = ''.join(f'<div><b>{e(a)}</b> {e(b)}</div>' for a, b in c.get('related', []))
    steps = [('Get in touch', 'Your date, format and numbers'), ('Get your fee', 'We hold the date for 14 days'),
             ('Confirm by email', 'Your booking is secured'), ('Plan it together', 'A short call, shaped to your service')]
    st = ''.join(f'<div class="st"><span>{i}</span><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(steps, 1))
    P.append(page(f'''<h2 class="ph">Book {e(name)} in four steps</h2>
      <div class="sts">{st}</div>
      <p class="mail">hello@thecareleaders.com</p>
      <div class="who2"><img src="{A}/img/brand/luke-speaking.jpg" alt="Luke Rodgers BEM">
        <div><p class="lbl">Designed and led by</p><h3>Luke Rodgers BEM</h3>
        <p>From care leaver to care leader. Luke went into care at 10 and has spent his career inside children's services as a consultant, trainer, keynote speaker and national engagement lead. He led the national engagement on England's new fostering standards, was a Knowledge Equity Fellow at Saïd Business School, University of Oxford, and was awarded the British Empire Medal in 2018.</p></div>
        <div class="rel"><p class="lbl">Often booked with</p>{rel}</div></div>
      <p class="legal">Gold, Dual Perspective Leadership Award, iESE Public Sector Transformation Awards 2026 · Children &amp; Young People Now Workforce Development Award 2023 · The Care Leaders Ltd, company number 10782615 · thecareleaders.com</p>''',
      'dark back', 'book', c))

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
