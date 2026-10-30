"""Render a course's showcase images for its brochure, from the "screens" block of the course data file.

Builds four images in the TCL Learning design system:
  - {slug}-laptop.png : the course home on The Care Leaders Online, in a laptop frame
  - {slug}-phone.png  : one tool or lesson from the course, in a phone frame
  - {slug}-workbook-cover.jpg and {slug}-workbook-page.jpg : the course workbook (A4 portrait)

These are designed screens that follow the platform design, not live captures.
Swap in real screenshots by dropping images at the same paths before building.

Usage: python3 tools/brochures/showcase/render.py courses/<course>.json
"""
import json, pathlib, asyncio, sys, html
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
BRO = HERE.parent
SITE = BRO.parent.parent
A = SITE / 'assets'
K = BRO / 'assets'
OUT = K / 'showcase'
OUT.mkdir(exist_ok=True)
e = lambda s: html.escape(s, quote=True)

FONTS = f'''@font-face{{font-family:CB;src:url({A}/fonts/crossten-black.woff2)}}
@font-face{{font-family:CS;src:url({A}/fonts/crossten-semibold.woff2)}}
@font-face{{font-family:CL;src:url({A}/fonts/crossten-light.woff2)}}
*{{box-sizing:border-box;margin:0;padding:0}} ul,ol{{list-style:none}}
body{{font-family:CL,sans-serif;color:#0e2545}} b{{font-family:CS;font-weight:400}}
.strip{{display:inline-block;background-size:100% 100%;background-repeat:no-repeat;font:400 15px CS;padding:7px 34px 8px 14px;color:#fff}}
'''
def strip(t, shape, col, style=''):
    return f'<span class="strip" style="background-image:url({K}/strips/{shape}-{col}.png);{style}">{e(t)}</span>'
def hexn(n, col, size=44):
    return f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{int(size*.58)}px;background:url({K}/strips/hex-{col}.png) center/100% 100%;color:#fff;font:400 {int(size*.34)}px CB;flex:0 0 {size}px">{n}</span>'
HC = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']

def laptop(s):
    secs = s['sections']; done = s.get('done', 1); n = len(secs); cols = min(n, 5)
    cards = ''
    for i, (t, tool) in enumerate(secs, 1):
        if i <= done:
            st = f'<span style="display:flex;align-items:center;gap:6px;font:400 13px CS;color:#78ae5d"><img src="{K}/tick.png" style="width:16px">Complete</span>'
        elif i == done + 1:
            st = strip('Continue', 'angled', 'fuchsia', 'font-size:12px;padding:4px 22px 5px 9px')
        else:
            st = '<span style="font:400 13px CS;color:#312b6c">Not started</span>'
        bg = '#f0f1df' if i <= done else ('#ede3ed' if i == done + 1 else '#fff')
        big = n <= 5
        cards += f'''<div style="background:{bg};border:2px solid #dae2e6;padding:16px 16px 14px;display:flex;flex-direction:column;gap:8px;min-height:{230 if big else 150}px">
          {hexn(i, HC[(i-1) % 5])}<b style="font:400 {22 if big else 18}px/1.15 CB">{e(t)}</b>
          <span style="font-size:{16 if big else 14}px;line-height:1.3">{e(s.get('tool_label', 'Tool'))}: {e(tool)}</span><div style="margin-top:auto">{st}</div></div>'''
    segs = ''.join(f'<span style="flex:1;height:10px;background:{"#acc90b" if i < done else "#4a4170"}"></span>' for i in range(n))
    nxt = secs[done][0] if done < n else secs[-1][0]
    return f'''<html><head><style>{FONTS}</style></head><body style="width:1440px;height:810px;overflow:hidden;background:#fff">
<header style="display:flex;align-items:center;gap:14px;padding:14px 40px;border-bottom:2px solid #dae2e6">
  <img src="{HERE}/tcll-brandmark.png" style="width:36px"><span style="font:400 19px CB">The Care Leaders Online</span>
  <nav style="margin-left:40px;display:flex;gap:28px;font:400 15px CS;color:#312b6c"><span>Home</span><span style="color:#cf0f55">My courses</span><span>Learning library</span><span>Certificates</span></nav>
  <span style="margin-left:auto;display:flex;align-items:center;gap:10px;font:400 15px CS"><span style="width:34px;height:34px;background:#5f3c90;color:#fff;display:flex;align-items:center;justify-content:center;font:400 14px CB">ST</span>Sam T.</span>
</header>
<section style="background:#241b40 url({A}/img/tcll/tcll-pattern.jpg) center/cover;color:#fff;height:340px;padding:40px 40px 0;position:relative">
  {strip(s['kind'], 'ribbon', 'apple', 'color:#241b40;font-size:14px')}
  <h1 style="font:400 {60 if len(s['title']) < 22 else 48}px/1 CB;margin:16px 0 12px;max-width:760px">{e(s['title'])}</h1>
  <p style="font-size:20px;line-height:1.4;max-width:640px">{e(s['intro'])}</p>
  <div style="display:flex;align-items:center;gap:22px;margin-top:24px;width:640px">
    <div style="flex:1"><div style="display:flex;gap:4px">{segs}</div><p style="font:400 14px CS;margin-top:8px">{done} of {n} {s.get('unit', 'sections')} complete</p></div>
    {strip('Continue: ' + nxt, 'arrow', 'apple', 'color:#241b40;font-size:17px;padding:11px 48px 12px 16px')}</div>
  <img src="{K}/tcll2026/{s.get('hero', 'image-block-01.png')}" style="position:absolute;right:40px;bottom:0;height:300px">
</section>
<section style="padding:26px 40px">
  <div style="display:flex;align-items:baseline;gap:16px;margin-bottom:16px"><h2 style="font:400 28px CB">Your {e(s.get('unit', 'sections'))}</h2><span style="font:400 15px CS;color:#312b6c">12 months' access · Certificate on completion</span></div>
  <div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:14px">{cards}</div>
</section></body></html>'''

def phone(s):
    p = s['phone']; n = len(s['sections']); at = p.get('section_no', 1)
    f = ''.join(f'''<div style="margin-bottom:12px"><p style="font:400 13px CS;color:#5f3c90;margin-bottom:5px">{i}. {e(a)}</p>
      <div style="border:2px solid #dae2e6;background:#fff;padding:10px 12px;font-size:14.5px;line-height:1.35">{e(b)}</div></div>'''
                for i, (a, b) in enumerate(p['fields'], 1))
    segs = ''.join(f'<span style="flex:1;height:6px;background:{"#acc90b" if i < at else "#dae2e6"}"></span>' for i in range(n))
    nxt = s['sections'][at][0] if at < n else 'Finish'
    return f'''<html><head><style>{FONTS}</style></head><body style="width:390px;height:844px;overflow:hidden;background:#f0f1df;position:relative">
<div style="height:46px;background:#241b40"></div>
<header style="background:#241b40;color:#fff;padding:4px 18px 14px">
  <p style="font:400 12px CS;color:#acc90b">{e(s.get('unit_one', 'Section'))} {at} · {e(s['sections'][at - 1][0])}</p>
  <div style="display:flex;gap:3px;margin-top:10px">{segs}</div></header>
<main style="padding:18px 18px 0">
  {strip('Tool', 'angled', 'teal', 'font-size:12px;padding:5px 26px 6px 10px')}
  <h1 style="font:400 29px/1.05 CB;margin:10px 0 8px">{e(p['title'])}</h1>
  <p style="font-size:15px;line-height:1.4;margin-bottom:16px">{e(p['intro'])}</p>
  {f}
  <div style="display:flex;gap:10px;margin-top:6px">{strip('Save to my plan', 'arrow', 'fuchsia', 'font-size:14px;padding:10px 40px 11px 12px')}
  <span style="font:400 13px CS;color:#312b6c;align-self:center">Download PDF</span></div>
  <div style="background:#312b6c;color:#fff;padding:14px 16px;margin-top:18px"><p style="font:400 12px CS;color:#acc90b">Key learning</p>
  <p style="font:400 16px/1.3 CB;margin-top:4px">{e(p['key'])}</p></div>
</main>
<footer style="position:absolute;left:0;right:0;bottom:0;height:64px;background:#fff;border-top:2px solid #dae2e6;display:flex;align-items:center;justify-content:space-between;padding:0 18px 10px;font:400 14px CS">
  <span style="color:#312b6c">Previous</span>{strip('Next: ' + nxt, 'arrow', 'apple', 'color:#241b40;font-size:13px;padding:7px 34px 8px 10px')}</footer></body></html>'''

CUT = ['polygon(0 1.5%,99.2% 0,100% 98.4%,0.8% 100%)', 'polygon(0.6% 0,100% 1.2%,99.4% 100%,0 98.8%)',
       'polygon(0 0,99.5% 1.6%,100% 100%,0.4% 98.6%)', 'polygon(0.8% 1%,100% 0,99.2% 99%,0 100%)']
COL = [('#cf0f55', '#fff'), ('#5f3c90', '#fff'), ('#008196', '#fff'), ('#312b6c', '#fff'), ('#78ae5d', '#241b40'),
       ('#7c05ca', '#fff'), ('#0e2545', '#fff')]
WB_CSS = (".wbh{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid #b9c6cd;font:400 13px CS}"
          ".band{margin:16px -56px 0;padding:18px 56px 24px;background:#7c05ca url(" + str(K) + "/tcll2026/tonal-purple.jpg) center/cover;color:#fff;"
          "display:grid;grid-template-columns:330px 1fr 64px;gap:28px;align-items:center;clip-path:polygon(0 0,100% 0,100% 88%,0 100%)}"
          ".band h1{font:400 27px/1.12 CB}.band p{font-size:15px;line-height:1.5}"
          ".pan{background:#fff;padding:14px 18px}"
          ".lab{font:400 13px CS;color:#5f3c90}"
          ".tab{position:absolute;right:0;top:330px;width:26px;height:120px;background:#5f3c90;color:#fff;display:grid;place-items:center;font:400 12px CS;writing-mode:vertical-rl}"
          ".wbf{position:absolute;left:56px;right:56px;bottom:26px;padding-top:12px;border-top:1px solid #b9c6cd;display:flex;justify-content:space-between;font:400 13px CS}"
          ".ln{border-bottom:1.5px solid #b9c6cd;height:30px}")


def wb_img(c):
    """An image block not already used elsewhere in this brochure (cover, formats page, included page, laptop screen)."""
    cov = c.get('cover_image', '')
    spare = [x for x in ('5', '3', '2', '6') if f'block-{x}' not in cov]
    return f'image-block-0{spare[2] if len(spare) > 2 else spare[-1]}.png'


def wb_cover(c, w):
    t = w.get('cover_title', c['name'])
    size = 76 if len(t) <= 16 else (62 if len(t) <= 26 else 52)
    return f'''<html><head><style>{FONTS}</style></head><body style="width:1123px;height:794px;overflow:hidden;background:#241b40;position:relative;color:#fff">
<div style="position:absolute;inset:0;background:#241b40 url({K}/tcll2026/tower-landscape.jpg) right center/auto 100% no-repeat"></div>
<img src="{A}/img/tcll/tcll-logo-white.png" style="position:absolute;left:56px;top:44px;width:190px">
<div style="position:absolute;left:56px;top:160px;width:600px">
  <p style="font:400 18px CS;color:#acc90b;margin-bottom:16px">Course workbook</p>
  <h1 style="font:400 {size}px/1 CB">{e(t)}</h1>
  <p style="font:400 22px CS;color:#acc90b;margin:20px 0 14px">{e(w['subtitle'])}</p>
  <p style="font-size:20px;line-height:1.45;max-width:520px">{e(w['promise'])}</p></div>
<img src="{K}/tcll2026/{wb_img(c)}" style="position:absolute;right:120px;bottom:0;height:400px;max-width:400px;object-fit:contain;object-position:bottom">
<div style="position:absolute;left:56px;bottom:56px;display:flex;gap:40px">
  <div><p style="font:400 14px CS;color:#acc90b">This workbook belongs to</p><div style="width:300px;border-bottom:2px solid #fff;height:36px"></div></div>
  <div><p style="font:400 14px CS;color:#acc90b">Date started</p><div style="width:160px;border-bottom:2px solid #fff;height:36px"></div></div></div>
</body></html>'''


def _block(i, a, b, extra=''):
    bg, fg = COL[i % len(COL)]
    num = '#acc90b' if fg == '#fff' else '#241b40'
    small = 'tight' in extra
    return (f'<div style="min-width:0;background:{bg};color:{fg};clip-path:{CUT[i % 4]};padding:{"10px 8px 12px" if small else "14px 14px 16px"};display:flex;flex-direction:column;gap:6px;{extra.replace("tight;", "")}">'
            f'<span style="font:400 {24 if small else 30}px/1 CB;color:{num}">{i + 1}</span>'
            f'<b lang="en-GB" style="font:400 {12 if small else 17}px/1.12 CB;hyphens:{'auto' if small else 'none'};overflow-wrap:{'anywhere' if small else 'normal'}">{e(a)}</b><span style="font-size:{11.5 if small else 13}px;line-height:1.33">{e(b)}</span></div>')


def diagram(kind, pl):
    items = pl['items']; n = len(items)
    if kind == 'roof':
        cols = ''.join(_block(i, a, b, ('tight;' if n >= 6 else '') + 'min-height:270px') for i, (a, b) in enumerate(items))
        return (f'<div style="background:#241b40;color:#fff;clip-path:polygon(3% 0,97% 0,100% 100%,0 100%);padding:12px 40px 14px;text-align:center">'
                f'<b style="font:400 21px CB;color:#acc90b">{e(pl["stance"])}</b></div>'
                f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:7px;margin-top:8px">{cols}</div>'
                '<div style="height:14px;background:#0e2545;margin-top:8px;clip-path:polygon(0 0,100% 20%,99% 100%,1% 100%)"></div>')
    if kind == 'levels':
        cols3 = ['#008196', '#5f3c90', '#cf0f55']
        rows = ''.join(
            f'<div style="display:grid;grid-template-columns:130px 1fr;margin-top:{0 if i == 0 else 10}px">'
            f'<div style="background:{cols3[i % 3]};color:#fff;display:grid;place-items:center;font:400 22px CB;clip-path:{CUT[i % 4]}">{e(a)}</div>'
            f'<div style="background:#f0f1df;padding:14px 18px;clip-path:{CUT[(i + 1) % 4]};font-size:15px;line-height:1.4;display:flex;align-items:center;min-height:{78 + i * 18}px">{e(b)}</div></div>'
            for i, (a, b) in enumerate(items))
        return f'<p class="lab" style="margin-bottom:8px">From least to most serious</p>{rows}'
    if kind == 'swap':
        rows = ''.join(
            f'<div style="display:grid;grid-template-columns:1fr 50px 1.3fr;align-items:center;margin-top:{0 if i == 0 else 10}px">'
            f'<div style="background:#f9e2df;padding:16px 18px;font:400 18px CS;color:#0e2545;clip-path:{CUT[i % 4]}"><s style="text-decoration-color:#cf0f55;text-decoration-thickness:3px">{e(a)}</s></div>'
            f'<span style="justify-self:center;width:26px;height:34px;background:#acc90b;clip-path:polygon(0 0,100% 50%,0 100%)"></span>'
            f'<div style="background:#78ae5d;padding:16px 18px;font:400 18px CB;color:#241b40;clip-path:{CUT[(i + 2) % 4]}">{e(b)}</div></div>'
            for i, (a, b) in enumerate(items))
        return ('<div style="display:grid;grid-template-columns:1fr 50px 1.3fr;margin-bottom:8px"><span class="lab">Instead of</span><span></span>'
                f'<span class="lab">Children asked for</span></div>{rows}')
    if kind == 'hub':
        pos = {4: [(1, 1), (3, 1), (1, 3), (3, 3)], 5: [(1, 1), (2, 1), (3, 1), (1, 3), (3, 3)],
               6: [(1, 1), (2, 1), (3, 1), (1, 3), (2, 3), (3, 3)]}[n]
        cells = ''.join(f'<div style="grid-column:{x};grid-row:{y};display:flex">{_block(i, a, b, "flex:1")}</div>'
                        for i, ((a, b), (x, y)) in enumerate(zip(items, pos)))
        centre = (f'<div style="grid-column:1 / 4;grid-row:2;background:#241b40;color:#fff;clip-path:polygon(2% 0,98% 0,100% 50%,98% 100%,2% 100%,0 50%);'
                  f'display:grid;place-items:center;padding:12px 30px;text-align:center"><b style="font:400 20px CB;color:#acc90b">{e(pl["stance"])}</b></div>')
        if n == 5:
            cells = cells.replace('grid-column:3;grid-row:3', 'grid-column:2 / 4;grid-row:3')
        return f'<div style="display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr auto 1fr;gap:9px;height:100%">{cells}{centre}</div>'
    blocks = ''
    for i, (a, b) in enumerate(items):
        blocks += _block(i, a, b, 'flex:1;min-height:330px')
        if i < n - 1:
            blocks += '<span style="flex:0 0 18px;align-self:center;height:34px;background:#acc90b;clip-path:polygon(0 0,100% 50%,0 100%)"></span>'
    return f'<p class="lab" style="margin-bottom:10px">{e(pl["stance"])}</p><div style="display:flex;gap:6px;align-items:stretch">{blocks}</div>'


def wb_page(c, w):
    pg = w['page']; pl = c['pillars']
    n = len(pl['items'])
    kind = w.get('diagram') or ('roof' if n >= 6 else 'steps')
    qs = ''.join(f'<div style="margin-top:{0 if i == 1 else 12}px"><p style="font:400 14.5px/1.35 CS"><b style="font:400 18px CB;color:#5f3c90;margin-right:8px">{i}</b>{e(q)}</p>'
                 '<div class="ln"></div><div class="ln"></div><div class="ln"></div></div>' for i, q in enumerate(pg['questions'][:3], 1))
    return f'''<html><head><style>{FONTS}{WB_CSS}</style></head><body style="width:1123px;height:794px;overflow:hidden;background:#dae2e6;position:relative">
<div style="padding:36px 56px 0">
<div class="wbh"><span style="color:#5f3c90">{e(c['name'])} · Course workbook</span><span>Theory</span></div>
<div class="band"><h1>{e(pl['title'])}</h1><p>{e(pl['stance_line'])}</p><img src="{K}/picto/p06.png" style="width:60px;height:60px"></div>
<div style="display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:14px;margin-top:14px;height:452px">
  <div class="pan" style="clip-path:{CUT[0]};display:flex;flex-direction:column;padding:16px 18px">
    <div style="flex:1;min-height:0">{diagram(kind, pl)}</div>
    <p style="font-size:12px;line-height:1.35;color:#312b6c;margin-top:10px">{e(pl['base'])}</p></div>
  <div class="pan" style="clip-path:{CUT[2]};padding:16px 18px">
    <p class="lab">Try it with one child in mind</p>
    <h2 style="font:400 19px/1.15 CB;margin:4px 0 12px">{e(pg['title'])}</h2>{qs}</div>
</div></div>
<span class="tab">Theory</span>
<div class="wbf"><span>thecareleaders.com</span><span style="font:400 16px CB">{pg.get('n', 12)}</span></div>
</body></html>'''


async def shoot(pg, doc, w, h, path):
    await pg.set_viewport_size({'width': w, 'height': h})
    f = path.with_suffix('.html'); f.write_text(doc)
    await pg.goto(f'file://{f}'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
    await pg.screenshot(path=str(path)); f.unlink()

def rr(size, r, fill):
    im = Image.new('RGBA', size, (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill); return im

def frames(slug):
    mid, navy = (36, 27, 64, 255), (14, 37, 69, 255)
    scr = Image.open(TMP / '_laptop.png').convert('RGBA')
    bz = 34; W, H = scr.width + bz * 2, scr.height + bz * 2 + 10
    lap = Image.new('RGBA', (W + 160, H + 60), (0, 0, 0, 0))
    lid = rr((W, H), 36, mid); lid.paste(scr, (bz, bz + 6)); lap.alpha_composite(lid, (80, 0))
    d = ImageDraw.Draw(lap)
    d.polygon([(0, H + 12), (W + 160, H + 12), (W + 120, H + 58), (40, H + 58)], fill=navy)
    d.rectangle([80, H, W + 80, H + 12], fill=(49, 43, 108, 255))
    d.rectangle([(W + 160) // 2 - 110, H + 12, (W + 160) // 2 + 110, H + 22], fill=mid)
    lap.thumbnail((1400, 1400)); lap.save(OUT / f'{slug}-laptop.png', optimize=True)
    ps = Image.open(TMP / '_phone.png').convert('RGBA')
    pb = 26; ph = rr((ps.width + pb * 2, ps.height + pb * 2), 110, mid)
    m = rr(ps.size, 84, (255, 255, 255, 255)); scr2 = Image.new('RGBA', ps.size, (0, 0, 0, 0)); scr2.paste(ps, (0, 0), m)
    ph.alpha_composite(scr2, (pb, pb))
    ImageDraw.Draw(ph).rounded_rectangle([ph.width // 2 - 110, pb + 26, ph.width // 2 + 110, pb + 86], 30, fill=(0, 0, 0, 255))
    ph.thumbnail((1400, 1400)); ph.save(OUT / f'{slug}-phone.png', optimize=True)
    for n in ('workbook-cover', 'workbook-page'):
        Image.open(TMP / f'_{n}.png').convert('RGB').save(OUT / f'{slug}-{n}.jpg', quality=90)
    for n in ('_laptop', '_phone', '_workbook-cover', '_workbook-page'):
        (TMP / f'{n}.png').unlink()
    TMP.rmdir()

async def main(c):
    s, w = c['screens'], c['workbook']
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, doc, wd, ht, sc in [('_laptop', laptop(s), 1440, 810, 1), ('_phone', phone(s), 390, 844, 2),
                                      ('_workbook-cover', wb_cover(c, w), 1123, 794, 1), ('_workbook-page', wb_page(c, w), 1123, 794, 1)]:
            pg = await b.new_page(device_scale_factor=sc)
            await shoot(pg, doc, wd, ht, TMP / f'{name}.png'); await pg.close()
        await b.close()

if __name__ == '__main__':
    src = pathlib.Path(sys.argv[1]); src = src if src.exists() else BRO / src
    c = json.loads(src.read_text())
    TMP = OUT / f"_tmp-{c['slug']}"; TMP.mkdir(exist_ok=True)
    asyncio.run(main(c)); frames(c['slug']); print(sorted(p.name for p in OUT.glob(c['slug'] + '-*')))
