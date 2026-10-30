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

def wb_cover(c, w):
    t = w.get('cover_title', c['name']).split(' ')
    mid = (len(t) + 1) // 2; title = ' '.join(t[:mid]) + '<br>' + ' '.join(t[mid:]) if len(t) > 1 else t[0]
    size = 92 if max(len(x) for x in t) < 10 and len(t) <= 3 else 70
    return f'''<html><head><style>{FONTS}</style></head><body style="width:794px;height:1123px;overflow:hidden;background:#dae2e6;position:relative">
<div style="position:absolute;left:0;top:0;width:794px;height:590px;background:#241b40 url({K}/tcll2026/tower-portrait.jpg) right top/auto 790px no-repeat"></div>
<div style="position:absolute;left:56px;top:{230 if size == 92 else 220}px;color:#fff;width:490px">
  <h1 style="font:400 {size}px/.95 CB">{title}</h1>
  <p style="font:400 21px CS;color:#acc90b;margin:18px 0 12px">{e(w['subtitle'])}</p>
  <p style="font-size:21px;line-height:1.45">{e(w['promise'])}</p></div>
<img src="{HERE}/learner-solo.png" style="position:absolute;right:30px;top:330px;height:470px">
<div style="position:absolute;left:56px;top:636px;width:400px">
  <p style="font:400 17px CS;color:#5f3c90">Course workbook</p>
  <p style="font-size:17px;line-height:1.5;margin-top:8px">{e(w.get('for', 'For anyone who works with or cares for children and young people.'))} Yours to keep.</p></div>
<div style="position:absolute;left:56px;top:930px">
  <p style="font:400 15px CS;color:#5f3c90">This workbook belongs to</p><div style="width:400px;border-bottom:2px solid #0e2545;height:40px"></div>
  <p style="font:400 15px CS;color:#5f3c90;margin-top:26px">Date started</p><div style="width:220px;border-bottom:2px solid #0e2545;height:40px"></div></div>
<img src="{HERE}/tcll-logo-landscape.png" style="position:absolute;right:56px;bottom:56px;width:170px">
</body></html>'''

def wb_page(c, w):
    pg = w['page']
    lines = lambda n: ''.join('<div style="border-bottom:1.5px solid #b9c6cd;height:34px"></div>' for _ in range(n))
    body = ''.join(f'''<div style="display:grid;grid-template-columns:40px 1fr;margin-bottom:18px"><span style="font:400 28px CB;color:#5f3c90">{i}</span>
      <div><p style="font:400 16px/1.35 CS">{e(q)}</p>{lines(3)}</div></div>''' for i, q in enumerate(pg['questions'], 1))
    return f'''<html><head><style>{FONTS}</style></head><body style="width:794px;height:1123px;overflow:hidden;background:#dae2e6;position:relative">
<div style="display:flex;justify-content:space-between;padding:40px 56px 12px;font:400 13px CS;border-bottom:1.5px solid #b9c6cd">
  <span style="color:#5f3c90">{e(c['name'])} · Course workbook</span><span>Action</span></div>
<div style="background:#312b6c;color:#fff;padding:30px 56px 30px;margin-top:22px">
  <h1 style="font:400 38px CB">{e(pg['title'])}</h1>
  <p style="font-size:17px;line-height:1.45;margin-top:8px;max-width:560px">{e(pg['intro'])}</p></div>
<div style="background:#fff;margin:26px 48px 0;padding:28px 30px 10px">{body}</div>
<div style="position:absolute;left:56px;right:56px;bottom:36px;display:flex;justify-content:space-between;font:400 13px CS"><span>thecareleaders.com</span><span>{pg.get('n', 12)}</span></div>
</body></html>'''

async def shoot(pg, doc, w, h, path):
    await pg.set_viewport_size({'width': w, 'height': h})
    f = OUT / '_tmp.html'; f.write_text(doc)
    await pg.goto(f'file://{f}'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
    await pg.screenshot(path=str(path)); f.unlink()

def rr(size, r, fill):
    im = Image.new('RGBA', size, (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill); return im

def frames(slug):
    mid, navy = (36, 27, 64, 255), (14, 37, 69, 255)
    scr = Image.open(OUT / '_laptop.png').convert('RGBA')
    bz = 34; W, H = scr.width + bz * 2, scr.height + bz * 2 + 10
    lap = Image.new('RGBA', (W + 160, H + 60), (0, 0, 0, 0))
    lid = rr((W, H), 36, mid); lid.paste(scr, (bz, bz + 6)); lap.alpha_composite(lid, (80, 0))
    d = ImageDraw.Draw(lap)
    d.polygon([(0, H + 12), (W + 160, H + 12), (W + 120, H + 58), (40, H + 58)], fill=navy)
    d.rectangle([80, H, W + 80, H + 12], fill=(49, 43, 108, 255))
    d.rectangle([(W + 160) // 2 - 110, H + 12, (W + 160) // 2 + 110, H + 22], fill=mid)
    lap.thumbnail((1400, 1400)); lap.save(OUT / f'{slug}-laptop.png', optimize=True)
    ps = Image.open(OUT / '_phone.png').convert('RGBA')
    pb = 26; ph = rr((ps.width + pb * 2, ps.height + pb * 2), 110, mid)
    m = rr(ps.size, 84, (255, 255, 255, 255)); scr2 = Image.new('RGBA', ps.size, (0, 0, 0, 0)); scr2.paste(ps, (0, 0), m)
    ph.alpha_composite(scr2, (pb, pb))
    ImageDraw.Draw(ph).rounded_rectangle([ph.width // 2 - 110, pb + 26, ph.width // 2 + 110, pb + 86], 30, fill=(0, 0, 0, 255))
    ph.thumbnail((1400, 1400)); ph.save(OUT / f'{slug}-phone.png', optimize=True)
    for n in ('workbook-cover', 'workbook-page'):
        Image.open(OUT / f'_{n}.png').convert('RGB').save(OUT / f'{slug}-{n}.jpg', quality=90)
    for n in ('_laptop', '_phone', '_workbook-cover', '_workbook-page'):
        (OUT / f'{n}.png').unlink()

async def main(c):
    s, w = c['screens'], c['workbook']
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, doc, wd, ht, sc in [('_laptop', laptop(s), 1440, 810, 1), ('_phone', phone(s), 390, 844, 2),
                                      ('_workbook-cover', wb_cover(c, w), 794, 1123, 1), ('_workbook-page', wb_page(c, w), 794, 1123, 1)]:
            pg = await b.new_page(device_scale_factor=sc)
            await shoot(pg, doc, wd, ht, OUT / f'{name}.png'); await pg.close()
        await b.close()

if __name__ == '__main__':
    src = pathlib.Path(sys.argv[1]); src = src if src.exists() else BRO / src
    c = json.loads(src.read_text())
    asyncio.run(main(c)); frames(c['slug']); print(sorted(p.name for p in OUT.glob(c['slug'] + '-*')))
