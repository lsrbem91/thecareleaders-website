"""Keynote brochure in Luke Speaks branding (an alternative to the Care Leaders Learning version).

  python3 tools/brochures/lsbrochure.py [out_dir]  -> keynotes-brochure-luke-speaks.pdf

Luke Speaks colours: fresh orange, teal, navy, plum, on cream and blue beds. Cut shapes only, no circles.
Same content as the keynotes brochure in catalogue.py (TALKS, bio, fees), so the two stay in step.
"""
import html, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build import opt, K, A, HERE, e
from catalogue import TALKS, BIO, SPEAK, WHY

LOGO = A / 'img/logos/luke-speaks.png'
B = A / 'img/brand'
COLS = ['or', 'te', 'pl', 'na']

def tag(text, col='or', cls=''):
    return f'<span class="tag {col} {cls}">{e(text)}</span>'

NAV = [('talks', 'The keynotes'), ('get', 'What you get'), ('luke', 'About Luke'), ('fees', 'Fees'), ('book', 'Book')]
def page(inner, cls, sec=None, n=None, t=None):
    nav = ''
    if sec:
        items = ''.join(tag(x, 'pl', 'on') if k == sec else f'<span class="ni">{e(x)}</span>' for k, x in NAV)
        nav = f'<nav class="nav"><img class="nl" src="{LOGO}" alt="Luke Speaks">{items}</nav>'
    foot = f'<div class="foot"><span>Keynotes with Luke Rodgers BEM · Luke Speaks · thecareleaders.com/keynotes</span><span>{n}</span></div>' if n else ''
    toc = f' data-toc="{e(t)}" data-n="{n}"' if t else ''
    return f'<section class="pg {cls}"{toc}>{nav}{inner}{foot}</section>'

def build():
    P = []
    num = lambda: len(P) + 1
    # Cover
    P.append(f'''<section class="pg cream cover"><img class="clogo" src="{LOGO}" alt="Luke Speaks">
      <div class="cov">{tag('Keynotes and conference workshops', 'te')}<h1>Keynotes with Luke Rodgers BEM</h1>
        <p class="hl">From care leaver. <span>To care leader.</span></p>
        <p class="intro">Story-led keynotes for conferences, staff days and boards: stories of care from Luke&#8217;s lived experience, the theory behind them and tools your audience can use the next day.</p></div>
      <div class="cph cut"><img src="{opt(B / 'luke-lga-wide.jpg', 900)}" alt="Luke Rodgers BEM speaking"></div>
      <img class="shape s-bub" src="{B / 'bubble-orange.png'}" alt="">
      <div class="cstats">
        <div class="cs na cut"><b>In person or online</b><span>keynotes of up to 90 minutes</span></div>
        <div class="cs or cut"><b>{len(TALKS)}</b><span>keynotes, or one built for your audience</span></div>
        <div class="cs te cut"><b>4,000+</b><span>delegates since 2024</span></div></div></section>''')
    P.append('')
    # Audience matrix
    rows = ''.join(f'<li class="cut"><span class="ma">{e(aud)}</span><span class="mar"></span><b>{e(t)}</b></li>' for t, _, _, aud, _, _, _ in TALKS)
    P.append(page(f'''<h2>Find the keynote for your audience</h2>
      <div class="mx"><ol class="mxl">{rows}</ol>
        <div class="mxc pl cut"><img class="mxi" src="{B / 'bubble-orange.png'}" alt=""><h3>Don&#8217;t see your audience here?</h3>
          <p>Tell us your conference theme, who&#8217;s coming and what you want them to leave with, and we&#8217;ll shape a custom keynote around them. It follows the same approach as every other talk, with the recording, the on-demand course and the workbook included.</p></div></div>''',
      'blue', 'talks', num(), 'Find the keynote for your audience'))
    # Talks
    beds = ['white', 'cream', 'blue']
    shapes = ['bubble-orange', 'crown-orange', 'bolt-navy', 'flower-teal', 'arrow-teal', 'squiggle-orange', 'tri-teal']
    for i, (t, tl, who, aud, para, outs, _) in enumerate(TALKS):
        col = COLS[i % 4]
        lis = ''.join(f'<li><span class="tk"></span>{e(x)}</li>' for x in outs)
        five = ''
        if t == 'Lived Experience Leadership':
            fs = [('Storytelling', 'Sharing their experience safely, on their own terms.'), ('Skills', 'Recognising and building the skills their experience has given them.'),
                  ('Strategies', 'Helping shape plans, services and decisions.'), ('Scaling', 'Leading pieces of work, such as training staff or running projects.'),
                  ('Succession', 'Mentoring and bringing the next young people through.')]
            five = '<ol class="five">' + ''.join(f'<li><span class="fn {COLS[k % 4]} cut">{k + 1}</span><b>{e(a)}.</b> {e(b)}</li>' for k, (a, b) in enumerate(fs)) + '</ol>'
        flag = tag('Flagship talk', 'or', 'flag') if i == 0 else ''
        P.append(page(f'''<div class="kn{' fv' if five else ''}"><div class="knl">{tag('For ' + who[0].lower() + who[1:], col)}
            <h2>{e(t)}</h2><p class="knt">{e(tl)}</p>{flag}<p class="knp">{e(para)}</p>{five}</div>
          <div class="knr"><div class="kno na cut"><h3>By the end, delegates will</h3><ul>{lis}</ul></div>
            <div class="knf"><p><b>Length</b> 45 to 90 minutes</p><p><b>Format</b> Keynote or conference workshop, in person or online</p>
            <p><b>Comes with</b> The recording and an on-demand course for 12 months, plus a workbook to keep</p></div></div></div>
          <img class="shape s-talk" src="{B / (shapes[i % 7] + '.png')}" alt="">''', beds[i % 3], 'talks', num(), t))
    # More than a keynote
    four = [('Before the day', 'A planning call', ['A 30-minute planning call', 'The keynote shaped around your audience and theme', 'A title and blurb for your programme, plus Luke\'s photo and bio']),
            ('On the day', 'The keynote', ['A keynote of up to 90 minutes', 'Time for questions and discussion', 'The slides, to share with delegates']),
            ('On the day', 'A workbook for every delegate', ['Print-ready or digital', 'Activities for individuals and teams', 'Theirs to keep']),
            ('After the day', 'The recording and course', ['The full keynote recorded', 'An on-demand course on The Care Leaders Online', '12 months\' access for every delegate'])]
    g = ''.join(f'<div class="g4 {COLS[k]} cut"><span class="gw">{e(w)}</span><h3>{e(t)}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in pts)}</ul></div>' for k, (w, t, pts) in enumerate(four))
    P.append(page(f'<h2>More than a keynote</h2><p class="sub">Every booking, in person or online, comes with the same four things.</p><div class="g4s">{g}</div>',
                  'cream', 'get', num(), 'More than a keynote: what every booking includes'))
    # Course online
    S = K / 'showcase'; sl = 'tools-for-schools'
    P.append(page(f'''<h2>The keynote course on any device</h2>{tag('Free for 12 months: the recording and the course', 'or', 'big')}
      <p class="shn">Shown: Tools for Schools. Every keynote has its own on-demand course on The Care Leaders Online, and a workbook.</p>
      <img class="shl" src="{opt(S / f'{sl}-laptop.png', 1300)}" alt=""><img class="shp" src="{opt(S / f'{sl}-phone.png', 800)}" alt="">
      <img class="shw1" src="{S}/{sl}-workbook-cover.jpg" alt=""><img class="shw2" src="{S}/{sl}-workbook-page.jpg" alt="">
      <div class="shb b1">{tag('The course home on a laptop', 'pl')}</div><div class="shb b2">{tag('Every tool works on a phone', 'te')}</div>
      <div class="shb b3">{tag('The workbook, theirs to keep', 'na')}</div>''', 'blue', 'get', num(), 'The keynote course on any device'))
    # How every talk works
    sta = [('or', 'Story', 'A real moment from care, told from the young person\'s side.'), ('te', 'Theory', 'The thinking that explains it, with honest evidence.'),
           ('pl', 'Action', 'Something to practise and use at work the next day.')]
    rows = ''.join(f'<div class="st3 {c} cut"><b>{t}</b><p>{x}</p></div>' for c, t, x in sta)
    P.append(page(f'''<h2>How every keynote works</h2><p class="sub">Every talk follows the same three steps, whatever the audience.</p>
      <div class="st3s">{rows}</div><img class="shape s-st" src="{B / 'arrow-teal.png'}" alt="">''', 'white', 'get', num(), 'How every keynote works: Story, Theory, Action'))
    # About Luke
    paras = ''.join(f'<p>{e(x)}</p>' for x in BIO)
    stats = ''.join(f'<div class="ps {COLS[k]} cut"><b>{e(a)}</b><span>{e(b)}</span></div>' for k, (a, b) in enumerate(SPEAK))
    P.append(page(f'''<div class="ab"><div class="abp cut"><img src="{opt(B / 'luke-lga-podium.jpg', 700)}" alt="Luke Rodgers BEM"></div>
      <div class="abt">{tag('Your speaker', 'te')}<h2>Luke Rodgers BEM</h2>{paras}</div>
      <div class="abs">{stats}<blockquote class="na cut">&#8220;You demand bravery and humanity in equal measure.&#8221;<cite>Maggie Atkinson, former Children&#8217;s Commissioner for England</cite></blockquote></div></div>''',
      'cream', 'luke', num(), 'Your speaker: Luke Rodgers BEM'))
    # Why Luke
    us = ''.join(f'<div class="us white cut"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for _, t, x in WHY['usps'])
    aw = ''.join(f'<div class="aw"><img src="{A}/img/{img}" alt="{e(a)}"><b>{e(a)}</b><span>{e(b)}</span></div>' for img, a, b in WHY['awards'])
    wst = ''.join(f'<div class="ws {["or", "te"][k]} cut"><b>{e(a)}</b><span>{e(b)}</span></div>' for k, (a, b) in enumerate(WHY['stats']))
    P.append(page(f'''<h2>Why book Luke</h2><p class="sub">Keynotes from someone who has lived in care and has led services.</p>
      <div class="wg"><div class="uss">{us}</div><div class="aws white cut">{tag('Award winning', 'pl')}{aw}</div></div><div class="wss">{wst}</div>''',
      'blue', 'luke', num(), 'Why book Luke'))
    # Fees
    def fee(col, label, fee_, note, pts, img):
        li = ''.join(f'<li><span class="tk"></span>{e(x)}</li>' for x in pts)
        return f'''<div class="fc white cut"><div class="fi cut"><img src="{opt(B / img, 600)}" alt=""></div>{tag(label, col)}
          <p class="fl">Keynote of up to 90 minutes</p><p class="fee">{fee_} <span>{note}</span></p><ul>{li}</ul></div>'''
    P.append(page(f'''<h2>Fees for every keynote</h2><div class="fcs">
      {fee('or', 'In person', '£4,950', '+ VAT + travel expenses', ['A planning call before the day', 'A workbook for every delegate', 'The recording and course for 12 months'], 'luke-stage.jpg')}
      {fee('te', 'Live online', '£2,490', '+ VAT', ['A planning call before the day', 'Questions in the chat and live Q&A', 'The recording and course for 12 months'], 'luke-room.jpg')}</div>
      <p class="fnote">Keynotes and conference workshops are contracted and invoiced by Luke Speaks Ltd, powered by The Care Leaders. If Luke is free, we hold your date for 14 days.</p>''',
      'cream', 'fees', num(), 'Fees for every keynote'))
    # Book
    steps = [('Tell us about your event', 'The date, your audience and the talk'), ('Get availability and a fee', 'We hold the date for 14 days'),
             ('Confirm by email', 'And send a purchase order if you use them'), ('Before the day', 'A planning call and a checklist')]
    st = ''.join(f'<div class="bs {COLS[k]} cut"><span>{k + 1}</span><b>{e(a)}</b><p>{e(b)}</p></div>' for k, (a, b) in enumerate(steps))
    P.append(page(f'''<h2>Book Luke in 4 steps</h2><div class="bss">{st}</div>{tag('hello@thecareleaders.com', 'or', 'mail')}
      <img class="shape s-bk" src="{B / 'bubble-teal.png'}" alt="">
      <p class="legal">Gold, Dual Perspective Leadership Award, iESE Public Sector Transformation Awards 2026 · Children &amp; Young People Now Workforce Development Award 2023 · Luke Speaks Ltd, company number 15452230 · thecareleaders.com/keynotes</p>''',
      'white', 'book'))
    # Contents
    items = [(m.group(2), html.unescape(m.group(1))) for pg in P for m in [re.search(r'data-toc="([^"]+)" data-n="(\d+)"', pg)] if m]
    lis = ''.join(f'<li><span class="cn {COLS[i % 4]} cut">{n}</span>{e(t)}</li>' for i, (n, t) in enumerate(items))
    P[1] = page(f'<h2>Contents</h2><ol class="toc">{lis}</ol>', 'white', None, 2)
    return P

CSS = '''
@font-face{font-family:CB;src:url({A}/fonts/crossten-black.woff2)}
@font-face{font-family:CS;src:url({A}/fonts/crossten-semibold.woff2)}
@font-face{font-family:CL;src:url({A}/fonts/crossten-light.woff2)}
@page{size:1280px 720px;margin:0}
*{box-sizing:border-box;margin:0;padding:0}ul,ol{list-style:none}
body{font-family:CL,sans-serif;color:#0e2545;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h1,h2,h3{font-family:CB;font-weight:400;color:#4e2b53}b{font-family:CS;font-weight:400}
.pg{width:1280px;height:720px;position:relative;overflow:hidden;padding:96px 60px 50px;break-after:page}
.white{background:#fff}.cream{background:#f6efe4}.blue{background:#dae2e6}
.or{background:#fbab1e;color:#2a1830}.te{background:#008196;color:#fff}.pl{background:#4e2b53;color:#fff}.na{background:#0e2545;color:#fff}
.or h3{color:#2a1830}.te h3,.pl h3,.na h3{color:#fff}
.cut{clip-path:polygon(0 2%,100% 0,99% 100%,1% 98%)}
h2{font-size:48px;line-height:1.05;margin-bottom:22px}.sub{font-size:20px;margin:-10px 0 26px}
.tag{display:inline-block;font:400 15px CS;padding:7px 16px 8px;clip-path:polygon(0 0,100% 6%,97% 100%,2% 92%)}
.nav{position:absolute;left:60px;right:60px;top:24px;display:flex;align-items:center;gap:20px}
.nl{height:38px;margin-right:8px}.ni{font:400 14px CS;color:#4e2b53}.tag.on{font-size:14px;padding:6px 14px 7px}
.foot{position:absolute;left:60px;right:60px;bottom:20px;display:flex;justify-content:space-between;font:400 12px CS;color:#4e2b53}
.shape{position:absolute;pointer-events:none}
/* cover */
.cover{padding:0}.clogo{position:absolute;left:60px;top:44px;height:92px}
.cov{position:absolute;left:60px;top:170px;width:600px}.cov .tag{margin-bottom:16px}
.cover h1{font-size:68px;line-height:.98;margin-bottom:14px}
.hl{font-family:CB;font-size:32px;color:#0e2545;margin-bottom:14px}.hl span{color:#008196}
.intro{font-size:19px;line-height:1.5}
.cph{position:absolute;right:0;top:0;width:520px;height:560px;clip-path:polygon(12% 0,100% 0,100% 100%,0 96%)}.cph img{width:100%;height:100%;object-fit:cover}
.s-bub{left:610px;top:40px;width:120px}
.cstats{position:absolute;left:60px;right:60px;bottom:34px;display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:16px}
.cs{padding:16px 22px 18px}.cs b{display:block;font-family:CB;font-size:36px;line-height:1.05}.cs span{font:400 16px CS}
/* contents */
.toc{columns:2;column-gap:60px}.toc li{display:flex;gap:14px;align-items:center;font:400 18px CS;color:#4e2b53;margin-bottom:12px;break-inside:avoid}
.cn{flex:0 0 38px;height:34px;display:grid;place-items:center;font:400 15px CB}
/* matrix */
.mx{display:grid;grid-template-columns:1.3fr 1fr;gap:30px;align-items:start}
.mxl li{display:grid;grid-template-columns:280px 30px 1fr;align-items:center;gap:12px;background:#fff;margin-bottom:10px;padding:13px 18px}
.ma{font:400 16px CS;color:#008196}.mar{width:22px;height:16px;background:#fbab1e;clip-path:polygon(0 30%,60% 30%,60% 0,100% 50%,60% 100%,60% 70%,0 70%)}
.mxl b{font-family:CB;font-size:22px;color:#4e2b53}
.mxc{padding:30px 32px 34px;position:relative}.mxc h3{font-size:30px;margin:12px 0}.mxc p{font-size:18px;line-height:1.5}.mxi{width:64px}
/* talks */
.kn{display:grid;grid-template-columns:1.15fr 1fr;gap:40px;align-items:start;position:relative;z-index:1}
.kn .tag{margin-bottom:14px}.kn h2{font-size:52px;margin-bottom:8px}.knt{font:400 24px/1.25 CS;color:#008196;margin-bottom:12px}
.flag{margin-bottom:4px}.knp{font-size:18px;line-height:1.55;margin-top:10px}
.kn.fv h2{font-size:46px}.kn.fv .knp{font-size:16px;line-height:1.45}
.kno{padding:28px 30px 30px}.kno h3{font-size:26px;margin-bottom:16px}
.kno li{display:flex;gap:12px;align-items:flex-start;font:400 17px/1.35 CS;margin-bottom:12px}
.tk{flex:0 0 14px;height:14px;margin-top:4px;background:#fbab1e;clip-path:polygon(0 10%,100% 0,90% 100%,10% 90%)}
.knf{margin-top:18px}.knf p{font-size:15px;line-height:1.45;margin-bottom:6px}.knf b{color:#4e2b53}
.s-talk{right:40px;bottom:30px;width:90px;z-index:0}
.five{margin-top:14px}.five li{display:flex;align-items:center;gap:10px;font-size:14px;line-height:1.3;margin-bottom:6px}
.fn{flex:0 0 30px;height:26px;display:grid;place-items:center;font:400 13px CB}
/* get */
.g4s{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.g4{padding:26px 22px 28px;min-height:400px}.gw{font:400 14px CS;opacity:.95}.g4 h3{font-size:26px;line-height:1.1;margin:10px 0 16px}
.g4 li{font-size:16px;line-height:1.4;margin-bottom:10px;padding-left:12px;border-left:3px solid currentColor}
/* showcase */
.tag.big{font-size:18px;padding:9px 20px 10px}
.shn{font:400 14px CS;color:#4e2b53;margin-top:14px;max-width:780px}
.shl{position:absolute;left:60px;top:250px;width:640px}.shp{position:absolute;left:600px;top:236px;height:330px}
.shw1{position:absolute;left:880px;top:110px;width:330px;transform:rotate(-3deg)}.shw2{position:absolute;left:900px;top:320px;width:330px;transform:rotate(3deg)}
.shb{position:absolute}.shb.b1{left:60px;top:640px}.shb.b2{left:600px;top:640px}.shb.b3{left:930px;top:580px}
/* sta */
.st3s{display:grid;gap:16px;max-width:880px}.st3{display:grid;grid-template-columns:200px 1fr;align-items:center;padding:24px 30px}
.st3 b{font-family:CB;font-size:40px}.st3 p{font-size:22px;line-height:1.35}
.s-st{right:70px;top:200px;width:200px}
/* about */
.ab{display:grid;grid-template-columns:320px 1fr 300px;gap:32px}
.abp{height:520px}.abp img{width:100%;height:100%;object-fit:cover}
.abt .tag{margin-bottom:10px}.abt h2{margin-bottom:12px}.abt p{font-size:16px;line-height:1.5;margin-bottom:10px}
.abs{display:grid;gap:12px;align-content:start}.ps{padding:14px 20px}.ps b{display:block;font-family:CB;font-size:36px;line-height:1}.ps span{font:400 15px CS}
blockquote{padding:20px 22px;font:400 18px/1.4 CS}cite{display:block;font:400 13px CL;margin-top:10px;font-style:normal}
/* why */
.wg{display:grid;grid-template-columns:2fr 1fr;gap:18px}.uss{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.us{padding:18px 22px}.us h3{font-size:20px;margin-bottom:6px}.us p{font-size:14px;line-height:1.45}
.aws{padding:20px 22px}.aw{margin-top:14px}.aw img{height:60px;display:block;margin-bottom:6px}.aw b{display:block;font-size:15px;color:#4e2b53}.aw span{font-size:13px}
.wss{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}.ws{padding:14px 22px;display:flex;gap:18px;align-items:center}.ws b{font-family:CB;font-size:40px}.ws span{font:400 16px CS}
/* fees */
.fcs{display:grid;grid-template-columns:1fr 1fr;gap:28px}.fc{padding:26px 30px 24px;position:relative}
.fi{position:absolute;right:24px;top:22px;width:170px;height:120px}.fi img{width:100%;height:100%;object-fit:cover}
.fl{font:400 18px CS;color:#008196;margin:14px 0 4px}.fee{font-family:CB;font-size:60px;color:#4e2b53;margin:18px 0 12px}.fee span{display:block;font:400 17px CS;color:#0e2545;margin-top:4px}
.fc li{display:flex;gap:12px;align-items:center;font:400 18px CS;margin-bottom:8px}
.fnote{margin-top:22px;font:400 17px/1.45 CS;color:#4e2b53}
/* book */
.bss{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:28px}.bs{padding:22px 22px 26px;min-height:200px}
.bs span{font-family:CB;font-size:44px;display:block}.bs b{display:block;font-size:22px;line-height:1.15;margin:4px 0 8px}.bs p{font-size:15px}
.tag.mail{font-size:28px;padding:12px 26px 14px}.s-bk{right:80px;top:410px;width:150px}
.legal{position:absolute;left:60px;right:60px;bottom:26px;font-size:12px;color:#4e2b53}
'''

if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else A / 'docs/brochures'
    css = CSS.replace('{A}', str(A))
    P = build()
    h = out / 'keynotes-brochure-luke-speaks.html'
    h.write_text(f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Keynotes: Luke Speaks</title><style>{css}</style></head><body>{"".join(P)}</body></html>')
    import subprocess, os
    pdf = out / 'keynotes-brochure-luke-speaks.pdf'
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{h}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.pdf({{path:'{pdf}',width:'1280px',height:'720px',printBackground:true,margin:{{top:0,right:0,bottom:0,left:0}}}});
await b.close()}})();"""
    subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
    print(pdf)
