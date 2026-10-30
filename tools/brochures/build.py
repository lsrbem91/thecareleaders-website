"""Build a Care Leaders Learning course brochure from a course data file.

Usage: python3 tools/brochures/build.py courses/nvr-essentials.json [out_dir]

One template for every training course, built on the TCL Learning design system:
Crossten only (Black headlines, Semibold labels, Light body), the Learning palette,
hand-cut strips, boxes and hexagons, and the 22 TCLL pictograms with their fixed meanings.
No icon fonts, no drawn icons, no grey, no rounded corners.

Page order (navigation strip on every inner page):
 Cover · Problem · Who it's for · Outcomes · The course (2 pages) · Formats and fees
 · Included · Online showcase and toolkit (if the course has one) · Book

Design rule: no CSS shadows, filters, masks or opacity. They export as soft masks
that the iPhone PDF viewer draws as dark boxes. Shapes are pre-tinted PNGs.
"""
import html, json, os, sys, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent
A = SITE / 'assets'
K = HERE / 'assets'
e = lambda s: html.escape(s, quote=True)

def strip(text, shape='ribbon', col='fuchsia', cls=''):
    return f'<span class="strip {shape} {cls}" style="background-image:url({K}/strips/{shape}-{col}.png)">{e(text)}</span>'
def picto(n, cls='pic'):
    return f'<img class="{cls}" src="{K}/picto/p{int(n):02d}.png" alt="">'
def box(col):
    return f'background-image:url({K}/strips/box-{col}.png)'

NAV = [('problem', 'The problem'), ('who', "Who it's for"), ('outcomes', 'Outcomes'), ('course', 'The course'),
       ('formats', 'Formats and fees'), ('included', 'Included'), ('online', 'Online course'), ('book', 'Book')]

def nav(cur, has_online, dark):
    items = [n for n in NAV if has_online or n[0] != 'online']
    out = []
    for k, t in items:
        if k == cur:
            out.append(strip(t, 'angled', 'apple' if dark else 'fuchsia', 'navon'))
        else:
            out.append(f'<span class="navi">{e(t)}</span>')
    return f'<nav class="nav"><img class="bm" src="{K}/brandmark.png" alt="">{"".join(out)}</nav>'

def page(inner, cls, sec=None, c=None, n=None):
    dark = 'dark' in cls
    top = nav(sec, bool(c.get('toolkit')), dark) if sec else ''
    foot = f'<div class="foot"><span>{e(c["name"])} · Course brochure · careleaderslearning.com</span><span>{n}</span></div>' if n else ''
    return f'<section class="pg {cls}">{top}{inner}{foot}</section>'

def build(c):
    acc = c['accent']; name = c['name']; P = []
    num = lambda: len(P) + 1
    hs = c['headline'].split('. ', 1)
    head = f'{e(hs[0])}. <span class="apple">{e(hs[1])}</span>' if len(hs) == 2 else e(c['headline'])

    # 1 Cover
    glance = ''.join(f'<div class="gl{" wide" if g[4:] else ""}" style="{box("indigo")}"><b>{e(g[1])}</b><span>{e(g[2])}</span><small>{e(g[3])}</small></div>'
                     for g in c['glance'])
    P.append(page(f'''
      <img class="logo" src="{A}/img/tcll/tcll-logo-white.png" alt="The Care Leaders Learning">
      <div class="cov">{strip(c['category'], 'ribbon', 'apple', 'cat')}
        <h1>{e(name)}</h1><p class="hl">{head}</p><p class="intro">{e(c['intro'])}</p></div>
      <img class="covimg" src="{A}/img/tcll/{c['cover_image']}" alt="">
      <div class="glance">{glance}</div>''', 'dark cover', c=c))

    # 2 Problem
    pr = c['problem']
    wo = ''.join(f'<li>{e(x)}</li>' for x in pr['without'])
    wi = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in pr['with'])
    P.append(page(f'''
      <div class="scene" style="{box('navy')}">{picto(14, 'pic scpic')}<p class="s1">{e(pr['scene'])}</p><p class="s2">{e(pr['question'])}</p></div>
      <div class="ba">
        <div class="b bad" style="{box('white')}">{strip('Without a shared approach', 'angled', 'red', 'bh')}<ul>{wo}</ul></div>
        {picto(22, 'pic mid')}
        <div class="b good" style="{box('white')}">{strip(f'After {name}', 'angled', 'midgreen', 'bh dk')}<ul>{wi}</ul></div></div>
      <div class="pnotes"><p><span class="k">Why it matters.</span> {e(pr['standards'])}</p><p><span class="k">The evidence.</span> {e(pr['evidence'])}</p></div>''',
      'bed-red', 'problem', c, num()))

    # 3 Who
    pics = [19, 4, 13, 15]
    groups = ''.join(f'<div class="wt" style="{box("white")}">{picto(pics[k % 4])}<h3>{e(t)}</h3><p>{e(d)}</p></div>'
                     for k, (_, t, d) in enumerate(c['audience']['groups']))
    notes = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in c['audience']['notes'])
    P.append(page(f'''<h2>Who it's for</h2>
      <div class="wts">{groups}</div><ul class="chips">{notes}</ul>''', 'bed-purple', 'who', c, num()))

    # 4 Outcomes (objectives role: indigo)
    cols = ['indigo', 'purple', 'indigo', 'purple', 'indigo', 'purple']
    outs = ''.join(f'<div class="ot" style="{box(cols[i - 1])}"><span class="on">{i}</span><h3>{e(h)}</h3><p>{e(d)}</p></div>'
                   for i, (h, d) in enumerate(c['outcomes'], 1))
    P.append(page(f'''<h2>By the end of the day, people can</h2><div class="ots">{outs}</div>''', 'light', 'outcomes', c, num()))

    # 5 The day at a glance
    parts = c['parts']; half = len(parts) // 2
    pcols = ['fuchsia', 'purple', 'teal', 'indigo']
    def blk(i, p):
        return f'''<div class="tb" style="{box(pcols[(i - 1) % 4])}"><span class="tn">{i}</span><h3>{e(p["title"])}</h3>
          <p class="ts">{e(p["theory"])}</p>{strip(p["leave"], "ribbon", "apple", "lv")}</div>'''
    am = ''.join(blk(i + 1, p) for i, p in enumerate(parts[:half]))
    pm = ''.join(blk(i + 1 + half, p) for i, p in enumerate(parts[half:]))
    P.append(page(f'''<h2>The day: {len(parts)} parts, 10am to 4pm</h2>
      <div class="ruler" style="background-image:url({K}/strips/arrowlong-navy.png)"><span>10am</span><span>Morning</span><span>Lunch</span><span>Afternoon</span><span>4pm</span></div>
      <div class="trow"><div class="tbs">{am}</div><div class="lunch" style="{box('midgreen')}">Lunch</div><div class="tbs">{pm}</div></div>
      <p class="tln">{strip('You leave with', 'ribbon', 'apple', 'mini')} a tool ready to use on your next shift.</p>''', 'light', 'course', c, num()))

    # 6 Story, Theory, Action
    rows = ''.join(f'''<div class="gr"><div class="gp" style="{box(pcols[(i - 1) % 4])}"><span class="tn">{i}</span>{e(p["title"])}</div>
        <div class="gc gs">{e(p["story"])}</div><div class="gc gt">{e(p["theory"])}</div><div class="gc ga">{e(p["action"])}</div></div>'''
        for i, p in enumerate(parts, 1))
    P.append(page(f'''<h2>Every part: a story, the theory, then practice</h2>
      <div class="grid"><div class="gh"><div></div>
        <div>{picto(18, 'pic sm')}{strip('Story', 'ribbon', 'fuchsia', 'gh1')}<small>A moment from care</small></div>
        <div>{picto(6, 'pic sm')}{strip('Theory', 'ribbon', 'purple', 'gh1')}<small>The thinking behind it</small></div>
        <div>{picto(17, 'pic sm')}{strip('Action', 'ribbon', 'midgreen', 'gh1 dk')}<small>What people practise</small></div></div>{rows}</div>
      <p class="tln">{e(c['story_line'])}</p>''', 'light', 'course', c, num()))

    # 7 Formats and fees
    imgs = [f'{A}/img/tcll/blocks/block-5.webp', f'{A}/img/tcll/blocks/block-3.webp']
    def fmt(k, f):
        pts = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in f['points'])
        return f'''<div class="fc" style="{box('white')}"><img class="fimg" src="{imgs[k % 2]}" alt="">
          {strip(f['label'], 'angled', 'teal', 'fl')}
          <p class="flen">{e(f['length'])}</p><p class="ftime">{e(f['time'])}</p>
          <p class="fee">{e(f['fee'])} <span>{e(f['fee_note'])}</span></p><ul>{pts}</ul></div>'''
    P.append(page(f'''<h2>Face to face or live online</h2>
      <div class="fcs">{''.join(fmt(k, f) for k, f in enumerate(c['formats']))}</div>
      <p class="fnote">{picto(12, 'pic xs')}{e(c['fees_note'])}</p>''', 'bed-blue', 'formats', c, num()))

    # 8 Included
    gp = [20, 5, 8, 1, 16]
    gets = ''.join(f'<div class="gi" style="{box("indigo")}">{picto(gp[k % 5])}<b>{e(t)}</b>{strip(s, "angled", "apple", "gs2")}<p>{e(d)}</p></div>'
                   for k, (_, t, s, d) in enumerate(c['gets']))
    P.append(page(f'''<h2>What every delegate gets</h2><p class="sub">Face to face or online. All included in the fee.</p>
      <div class="gis">{gets}</div>''', 'dark', 'included', c, num()))

    # 9 Online showcase: devices and workbook
    sh = c.get('showcase')
    if sh:
        S = f'{K}/showcase'; lb = sh['labels']
        P.append(page(f'''<div class="shh"><h2>{e(sh['title'])}</h2><p class="sub">{e(sh['sub'])}</p></div>
          <img class="shl" src="{S}/{sh['laptop']}" alt=""><img class="shp" src="{S}/{sh['phone']}" alt="">
          <img class="shw1" src="{S}/{sh['workbook'][0]}" alt=""><img class="shw2" src="{S}/{sh['workbook'][1]}" alt="">
          <div class="shlb s1">{strip(lb[0], 'angled', 'purple')}</div><div class="shlb s2">{strip(lb[1], 'angled', 'teal')}</div>
          <div class="shlb s3">{strip(lb[2], 'angled', 'fuchsia')}</div>''', 'bed-purple', 'online', c, num()))

    # 10 Online course and toolkit
    tk = c.get('toolkit')
    if tk:
        hc = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']
        path = ''.join(f'<li><span class="hx" style="background-image:url({K}/strips/hex-{hc[(i - 1) % 5]}.png)">{i}</span>{e(s)}</li>'
                       for i, s in enumerate(tk['sections'], 1))
        tools = ''.join(f'<div class="tool" style="{box("white")}"><span>{i:02d}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>'
                        for i, (a, b) in enumerate(tk['tools'], 1))
        P.append(page(f'''<div class="tkh"><div>{strip(tk['kind'], 'ribbon', 'fuchsia', 'cat')}<h2>{e(tk['name'])}</h2>
            <p class="sub">{e(tk['intro'])}</p></div><ol class="path">{path}</ol></div>
          <p class="lbl">{picto(9, 'pic xs')}{len(tk['tools'])} interactive tools inside</p><div class="tools">{tools}</div>''', 'bed-green', 'online', c, num()))

    # 10 Book
    scol = ['apple', 'midgreen', 'teal', 'brightpurple']
    steps = [('Get in touch', 'Your date, format and numbers'), ('Get your fee', 'We hold the date for 14 days'),
             ('Confirm by email', 'Your booking is secured'), ('Plan it together', 'A short call, shaped to your service')]
    st = ''.join(f'<div class="st {"dk" if scol[i] in ("apple", "midgreen") else ""}" style="background-image:url({K}/strips/arrow-{scol[i]}.png)"><span>{i + 1}</span><b>{e(a)}</b><p>{e(b)}</p></div>'
                 for i, (a, b) in enumerate(steps))
    rel = ''.join(f'<p><span class="k">{e(a)}.</span> {e(b)}</p>' for a, b in c.get('related', []))
    P.append(page(f'''<h2>Book {e(name)} in four steps</h2>
      <div class="sts">{st}</div>
      {strip('hello@thecareleaders.com', 'ribbon', 'apple', 'mail')}
      <div class="who2"><img src="{A}/img/brand/luke-speaking.jpg" alt="Luke Rodgers BEM">
        <div>{strip('Designed and led by', 'angled', 'purple', 'mini')}<h3>Luke Rodgers BEM</h3>
        <p>From care leaver to care leader. Luke went into care at 10 and has spent his career inside children's services as a consultant, trainer, keynote speaker and national engagement lead. He led the national engagement on England's new fostering standards, was a Knowledge Equity Fellow at Saïd Business School, University of Oxford, and was awarded the British Empire Medal in 2018.</p></div>
        <div class="rel">{strip('Often booked with', 'angled', 'purple', 'mini')}{rel}</div></div>
      <p class="legal">Gold, Dual Perspective Leadership Award, iESE Public Sector Transformation Awards 2026 · Children &amp; Young People Now Workforce Development Award 2023 · The Care Leaders Ltd, company number 10782615 · thecareleaders.com</p>''',
      'dark', 'book', c))

    css = (HERE / 'brochure.css').read_text().replace('{ACC}', acc).replace('{A}', str(A)).replace('{K}', str(K))
    return f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{e(name)}: course brochure</title><style>{css}</style></head><body>{"".join(P)}</body></html>'

if __name__ == '__main__':
    src = pathlib.Path(sys.argv[1]); src = src if src.is_absolute() else (HERE / src if (HERE / src).exists() else src)
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else SITE / 'assets/docs/brochures'
    c = json.loads(src.read_text())
    h = out / f"{c['slug']}.html"; h.write_text(build(c))
    pdf = out / f"{c['slug']}.pdf"
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{h}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.pdf({{path:'{pdf}',width:'1280px',height:'720px',printBackground:true,margin:{{top:0,right:0,bottom:0,left:0}}}});
await b.close()}})();"""
    subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
    print(pdf)
