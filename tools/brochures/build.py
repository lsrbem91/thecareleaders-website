"""Build a Care Leaders Learning course brochure from a course data file.

Usage: python3 tools/brochures/build.py courses/nvr-essentials.json [out_dir]

One template for every training course, built on the TCL Learning design system:
Crossten only (Black headlines, Semibold labels, Light body), the Learning palette,
hand-cut strips, boxes and hexagons, and the 22 TCLL pictograms with their fixed meanings.
No icon fonts, no drawn icons, no grey, no rounded corners.

Page order (navigation strip on every inner page):
 Cover · Contents · Problem · Who it's for · Outcomes · The course (face to face day, how each part
 works, live online session) · Included · Online showcase and toolkit (if the course has one)
 · Why us · About your facilitator · Formats and fees · Offer (if any) · Book
 Sales logic: problem, then value, then trust, then price, then the offer, then how to book.

Design rule: no CSS shadows, filters, masks or opacity. They export as soft masks
that the iPhone PDF viewer draws as dark boxes. Shapes are pre-tinted PNGs.
"""
import html, json, os, re, sys, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent
A = SITE / 'assets'
K = HERE / 'assets'
e = lambda s: html.escape(s, quote=True)

def strip(text, shape='ribbon', col='fuchsia', cls=''):
    return f'<span class="strip {shape} {cls}" style="background-image:url({K}/strips/{shape}-{col}.png)">{e(text)}</span>'
def picto(n, cls='pic'):
    return f'<img class="{cls}" src="{K}/picto/p{int(n):02d}.png" alt="">'
def opt(path, maxw=800):
    """A smaller copy of an image for the PDF: resized and quantised to 256 colours, alpha kept."""
    from PIL import Image
    src = pathlib.Path(path); out = K / 'opt' / f'{src.stem}-{maxw}.png'
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        out.parent.mkdir(exist_ok=True)
        im = Image.open(src).convert('RGBA'); im.thumbnail((maxw, maxw * 2))
        im.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(out, optimize=True)
    return out
def box(col):
    return f'background-image:url({K}/strips/box-{col}.png)'

NAV = [('problem', 'The problem'), ('who', "Who it's for"), ('outcomes', 'Outcomes'), ('course', 'The course'),
       ('included', 'Included'), ('online', 'Online course'), ('why', 'Why us'), ('formats', 'Formats and fees'), ('book', 'Book')]

def nav(cur, has_online, dark):
    items = [n for n in NAV if has_online or n[0] != 'online']
    out = []
    for k, t in items:
        if k == cur:
            out.append(strip(t, 'angled', 'apple' if dark else 'fuchsia', 'navon'))
        else:
            out.append(f'<span class="navi">{e(t)}</span>')
    return f'<nav class="nav"><img class="bm" src="{K}/brandmark.png" alt="">{"".join(out)}</nav>'

def page(inner, cls, sec=None, c=None, n=None, t=None):
    dark = 'dark' in cls
    top = nav(sec, bool(c.get('toolkit')), dark) if sec else ''
    foot = f'<div class="foot"><span>{e(c["name"])} · Course brochure · thecareleaders.com</span><span>{n}</span></div>' if n else ''
    toc = f' data-toc="{e(t)}" data-n="{n}"' if t else ''
    return f'<section class="pg {cls}"{toc}>{top}{inner}{foot}</section>'

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
      <img class="covimg" src="{opt(A / 'img/tcll' / c['cover_image'], 960)}" alt="">
      <div class="glance">{glance}</div>''', 'dark cover', c=c))

    # 2 Contents (filled in at the end, once page numbers are known)
    P.append('')
    CONTENTS = 1

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
      'bed-red', 'problem', c, num(), 'The problem this course solves'))

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

    # 5a Course-specific model page (NVR: the 7 pillars)
    pl = c.get('pillars')
    if pl:
        pc = ['fuchsia', 'purple', 'teal', 'indigo', 'midgreen', 'brightpurple', 'navy']
        cols_ = ''.join(f'<div class="pil" style="{box(pc[i])}"><span class="tn">{i + 1}</span><h3>{e(a)}</h3><p>{e(t)}</p></div>' for i, (a, t) in enumerate(pl['items']))
        P.append(page(f'''<h2>{e(pl['title'])}</h2>
          <div class="roof" style="{box('midnight')}"><b>{e(pl['stance'])}</b><p>{e(pl['stance_line'])}</p></div>
          <div class="pils">{cols_}</div>
          <div class="pbase" style="{box('white')}">{picto(6, 'pic xs')}{e(pl['base'])}</div>''', 'bed-blue', 'course', c, num()))

    # 5 Option 1: the face to face day
    parts = c['parts']; half = len(parts) // 2
    pcols = ['fuchsia', 'purple', 'teal', 'indigo']
    def blk(i, p):
        return f'''<div class="tb" style="{box(pcols[(i - 1) % 4])}"><span class="tn">{i}</span><h3>{e(p["title"])}</h3>
          <p class="ts">{e(p["theory"])}</p>{strip(p["leave"], "ribbon", "apple", "lv")}</div>'''
    am = ''.join(blk(i + 1, p) for i, p in enumerate(parts[:half]))
    pm = ''.join(blk(i + 1 + half, p) for i, p in enumerate(parts[half:]))
    P.append(page(f'''<h2>Option 1: face to face, a 6-hour day</h2>
      <div class="ruler" style="background-image:url({K}/strips/arrowlong-navy.png)"><span>10am</span><span>Morning: parts 1 and 2</span><span>Lunch</span><span>Afternoon: parts 3 and 4</span><span>4pm</span></div>
      <div class="trow"><div class="tbs">{am}</div><div class="lunch" style="{box('midgreen')}">Lunch</div><div class="tbs">{pm}</div></div>
      <p class="tln">{strip('You leave with', 'ribbon', 'apple', 'mini')} a tool ready to use on your next shift.</p>''', 'light', 'course', c, num()))

    # 5b The live online session: a keynote, not a shorter day
    on = c.get('online_session')
    if on:
        k, ch, qa = on['keynote'], on['chat'], on['qa']
        hcs = ['fuchsia', 'purple', 'teal', 'indigo']
        ideas = ''.join(f'<li><span class="hx" style="background-image:url({K}/strips/hex-{hcs[n % 4]}.png)">{n + 1}</span>{e(x)}</li>' for n, x in enumerate(k['ideas']))
        bub = ''.join(f'<p class="bub" style="{box("white")}">{e(x)}</p>' for x in ch['bubbles'])
        P.append(page(f'''<h2>{e(on['title'])}</h2><p class="sub osub">{e(on['sub'])}</p>
          <div class="ons">
            <div class="onk" style="{box('navy')}">{picto(18, 'pic onp')}<h3>{e(k['title'])}</h3><p>{e(k['text'])}</p><ol class="onl">{ideas}</ol></div>
            <div class="onc" style="{box('purple')}">{picto(13, 'pic onp')}<h3>{e(ch['title'])}</h3><p>{e(ch['text'])}</p>{bub}</div>
            <div class="onq" style="{box('apple')}">{picto(11, 'pic onp')}<h3>{e(qa['title'])}</h3><p>{e(qa['text'])}</p><ul class="onal">{''.join(f'<li><img src="{K}/chev.png" alt="">{e(x)}</li>' for x in qa.get('asks', []))}</ul></div></div>
          <p class="tln">{strip('Afterwards', 'ribbon', 'apple', 'mini')} {e(on['after'])}</p>
          <p class="tln onx">{e(on['compare'])}</p>''', 'dark', 'course', c, num()))

    # 6 Our framework: Story, Theory, Action (the same page in every brochure)
    sta = [(18, 'fuchsia', '', 'Story', 'A real moment from care, told from the young person\'s side.'),
           (6, 'purple', '', 'Theory', 'The thinking that explains it, with honest evidence.'),
           (17, 'midgreen', 'dk', 'Action', 'Something to practise and use at work the next day.')]
    cards = ''.join(f'<div class="sta {d}" style="background-image:url({K}/strips/arrowlong-{col}.png)">{picto(n, "pic stp")}<b>{t}</b><p>{x}</p></div>' for n, col, d, t, x in sta)
    P.append(page(f'''<h2>How we teach: Story, Theory, Action</h2>
      <p class="sub">Every Care Leaders Learning course, workbook and online lesson follows the same three steps.</p>
      <div class="stas">{cards}</div>{f'<p class="tln">{strip("In this course", "ribbon", "apple", "mini")} {e(c["story_line"])}</p>' if c.get('story_line') else ''}''', 'bed-purple', 'course', c, num()))

    # 8 Included
    gp = [20, 5, 8, 1, 16]
    gets = ''.join(f'<div class="gi" style="{box("indigo")}">{picto(gp[k % 5])}<b>{e(t)}</b>{strip(s, "angled", "apple", "gs2")}<p>{e(d)}</p></div>'
                   for k, (_, t, s, d) in enumerate(c['gets']))
    P.append(page(f'''<h2>What every delegate gets</h2><p class="sub">Face to face or online. All included in the fee.</p>
      <div class="gis">{gets}</div>''', 'light', 'included', c, num()))

    # 9 Online showcase: devices and workbook
    sh = c.get('showcase')
    if sh:
        S = f'{K}/showcase'; lb = sh['labels']
        P.append(page(f'''<div class="shh"><h2>{e(sh['title'])}</h2><p class="sub">{e(sh['sub'])}</p></div>
          <img class="shl" src="{opt(K / 'showcase' / sh['laptop'], 1300)}" alt=""><img class="shp" src="{opt(K / 'showcase' / sh['phone'], 800)}" alt="">
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

    # 11 Why choose us: USPs, awards with their logos, stats
    w = c.get('why')
    if w:
        usps = ''.join(f'<div class="usp" style="{box("white")}">{picto(n)}<h3>{e(t)}</h3><p>{e(x)}</p></div>' for n, t, x in w['usps'])
        aws = ''.join(f'<div class="awl"><img src="{A}/img/{img}" alt="{e(a)}"><b>{e(a)}</b><p>{e(b_)}</p></div>' for img, a, b_ in w['awards'])
        cols2 = ['apple', 'teal']
        stats = ''.join(f'<div class="wst {"dk" if cols2[i] == "apple" else ""}" style="background-image:url({K}/strips/arrowlong-{cols2[i]}.png)"><b>{e(a)}</b><p>{e(b_)}</p></div>'
                        for i, (a, b_) in enumerate(w['stats']))
        P.append(page(f'''<h2>{e(w['title'])}</h2><p class="sub">{e(w['sub'])}</p>
          <div class="wgrid"><div class="usps">{usps}</div>
            <div class="awbox" style="{box('white')}">{strip('Award winning', 'angled', 'purple', 'mini')}{aws}</div></div>
          <div class="wsts">{stats}</div>''', 'dark', 'why', c, num(), w['title']))

    # 12 About your facilitator
    f = c.get('facilitator')
    if f:
        paras = ''.join(f'<p>{e(x)}</p>' for x in f['paras'])
        pcol = ['fuchsia', 'purple', 'teal']
        proof = ''.join(f'<div class="pf" style="{box(pcol[i])}"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(f['proof']))
        P.append(page(f'''<div class="fac"><div class="fl1"><img class="fph" src="{A}/img/brand/{f['image']}" alt="{e(f['name'])}">
            {strip(f['line'], 'ribbon', 'fuchsia', 'cat')}</div>
          <div class="fl2">{strip(f['role'], 'angled', 'purple', 'mini')}<h2>{e(f['name'])}</h2><div class="fps">{paras}</div>
            <p class="fcourse">{picto(17, 'pic xs')}{e(f['for_course'])}</p></div>
          <div class="fl3">{strip('NVR in practice', 'angled', 'teal', 'mini')}<div class="pfs">{proof}</div>
            <blockquote style="{box('indigo')}">"{e(f['quote'][0])}"<cite>{e(f['quote'][1])}</cite></blockquote></div></div>''',
          'light', 'why', c, num(), f'About your facilitator: {f["name"]}'))

    # 7 Formats and fees
    imgs = [opt(A / 'img/tcll/blocks/block-5.webp', 500), opt(A / 'img/tcll/blocks/block-3.webp', 500)]
    def offer(f):
        if not f.get('offer'): return ''
        return f'<div class="foff" style="{box("apple")}"><b>{e(f["offer"][0])}</b><p>{e(f["offer"][1])}</p></div>'
    def fmt(k, f):
        pts = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in f['points'])
        return f'''<div class="fc" style="{box('white')}"><img class="fimg" src="{imgs[k % 2]}" alt="">
          {strip(f['label'], 'angled', 'teal', 'fl')}
          <p class="flen">{e(f['length'])}</p><p class="ftime">{e(f['time'])}</p>
          <p class="fee">{e(f['fee'])} <span>{e(f['fee_note'])}</span></p><ul>{pts}</ul></div>'''
    P.append(page(f'''<h2>Face to face or live online</h2>
      <div class="fcs">{''.join(fmt(k, f) for k, f in enumerate(c['formats']))}</div>
      <p class="fnote">{picto(12, 'pic xs')}{e(c['fees_note'])}</p>''', 'bed-blue', 'formats', c, num()))

    # 7b Offer: try it online first
    of = c.get('offer')
    if of:
        cols = [('teal', ''), ('apple', 'dk')]
        stp = ''.join(f'''<div class="ofs {cols[k][1]}" style="background-image:url({K}/strips/arrowlong-{cols[k][0]}.png)"><span class="ofn">{e(n)}</span>
            <div><b>{e(t)}</b><p class="ofp">{f'<s>{e(old)}</s> ' if old else ''}{e(fee)} <span>{e(note)}</span></p></div></div>'''
            for k, (n, t, fee, note, old) in enumerate(of['steps']))
        P.append(page(f'''<div class="ofl">{strip(of['tag'], 'ribbon', 'apple', 'cat')}<p class="ofb">{e(of['big'])}</p><p class="ofx">{e(of['line'])}</p></div>
          <div class="ofr">{stp}{strip(of['save'], 'ribbon', 'white', 'ofv dk')}</div>
          <p class="oft">{e(of['terms'])}</p>''', 'dark', 'formats', c, num(), f"Try it online first: {of['big']} the face to face day"))

    # 13 Book
    scol = ['apple', 'teal', 'brightpurple']
    steps = [('Choose your format', 'Face to face or live online'), ('Pick a date', 'One that works for your team'),
             ('Book your training', 'Email us and we confirm it')]
    st = ''.join(f'<div class="st {"dk" if scol[i] == "apple" else ""}" style="background-image:url({K}/strips/arrow-{scol[i]}.png)"><span>{i + 1}</span><b>{e(a)}</b><p>{e(b)}</p></div>'
                 for i, (a, b) in enumerate(steps))
    rel = ''.join(f'<p><span class="k">{e(a)}.</span> {e(b)}</p>' for a, b in c.get('related', []))
    P.append(page(f'''<h2>Book {e(name)} in {len(steps)} steps</h2>
      <div class="sts">{st}</div>
      {strip('hello@thecareleaders.com', 'ribbon', 'apple', 'mail')}
      <div class="rel rel2">{strip('Often booked with', 'angled', 'purple', 'mini')}{rel}</div>
      <p class="legal">Gold, Dual Perspective Leadership Award, iESE Public Sector Transformation Awards 2026 · Children &amp; Young People Now Workforce Development Award 2023 · The Care Leaders Ltd, company number 10782615 · thecareleaders.com</p>''',
      'light', 'book', c))

    # Contents: every numbered page, by its heading
    items = []
    for k, pg in enumerate(P):
        if k in (0, CONTENTS): continue
        m = re.search(r'data-toc="([^"]+)" data-n="(\d+)"', pg) or None
        if m: t, n = html.unescape(m.group(1)), m.group(2)
        else:
            h = re.search(r'<h2>(.*?)</h2>', pg, re.S); n = re.search(r'<div class="foot"><span>.*?</span><span>(\d+)</span>', pg)
            t = re.sub('<[^>]+>', '', h.group(1)) if h else ''; n = n.group(1) if n else str(k + 1)
            t = html.unescape(t)
        if t: items.append((n, t))
    hc2 = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']
    lis = ''.join(f'<li><span class="hx cx" style="background-image:url({K}/strips/hex-{hc2[i % 5]}.png)">{n}</span>{e(t)}</li>' for i, (n, t) in enumerate(items))
    P[CONTENTS] = page(f'<h2>Contents</h2><ol class="toc">{lis}</ol>', 'light', None, c, 2)

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
