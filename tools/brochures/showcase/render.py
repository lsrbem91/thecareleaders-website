"""Render the NVR Essentials showcase images for the brochure.

Builds four screens in the TCL Learning design system, then places them in
device frames:
  - laptop: The NVR Toolkit course home on The Care Leaders Online
  - phone:  the Hot-moment protocol tool in section 3
  - workbook cover and one workbook page (A4 portrait)

These are designed screens that follow the platform design, not live captures.
Swap in real screenshots by dropping PNGs at the same paths before building.

Usage: python3 tools/brochures/showcase/render.py
Output: tools/brochures/assets/showcase/nvr-*.png
"""
import pathlib, asyncio
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
BRO = HERE.parent
SITE = BRO.parent.parent
A = SITE / 'assets'
K = BRO / 'assets'
OUT = K / 'showcase'
OUT.mkdir(exist_ok=True)

FONTS = f'''@font-face{{font-family:CB;src:url({A}/fonts/crossten-black.woff2)}}
@font-face{{font-family:CS;src:url({A}/fonts/crossten-semibold.woff2)}}
@font-face{{font-family:CL;src:url({A}/fonts/crossten-light.woff2)}}
*{{box-sizing:border-box;margin:0;padding:0}} ul,ol{{list-style:none}}
body{{font-family:CL,sans-serif;color:#0e2545}} b{{font-family:CS;font-weight:400}}
.strip{{display:inline-block;background-size:100% 100%;background-repeat:no-repeat;font:400 15px CS;padding:7px 34px 8px 14px;color:#fff}}
'''
def strip(t, shape, col, style=''):
    return f'<span class="strip" style="background-image:url({K}/strips/{shape}-{col}.png);{style}">{t}</span>'
def hexn(n, col, size=44):
    return f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{int(size*.58)}px;background:url({K}/strips/hex-{col}.png) center/100% 100%;color:#fff;font:400 {int(size*.34)}px CB;flex:0 0 {size}px">{n}</span>'

SECTIONS = [('Foundations', 'Your young person'), ('Parental presence', 'Presence map'),
            ('De-escalation', 'Hot-moment protocol'), ('Baskets', 'Baskets sort'),
            ('Reconciliation', 'Gesture menu'), ('Acts of resistance', 'Resistance planner'),
            ('Supporters and self-care', 'Supporter mapper'), ('Announcements', 'Announcement builder'),
            ('Sit-ins', 'Sit-in script builder'), ('Bringing it together', 'Your certificate')]
HC = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']

# ---------- laptop: course home (1440 x 900) ----------
def laptop():
    cards = ''
    for i, (s, t) in enumerate(SECTIONS, 1):
        if i <= 3:
            st = f'<span style="display:flex;align-items:center;gap:6px;font:400 13px CS;color:#78ae5d"><img src="{K}/tick.png" style="width:16px">Complete</span>'
        elif i == 4:
            st = strip('Continue', 'angled', 'fuchsia', 'font-size:12px;padding:4px 22px 5px 9px')
        else:
            st = '<span style="font:400 13px CS;color:#312b6c">Not started</span>'
        bg = '#f0f1df' if i <= 3 else ('#ede3ed' if i == 4 else '#fff')
        cards += f'''<div style="background:{bg};border:2px solid #dae2e6;padding:16px 16px 14px;display:flex;flex-direction:column;gap:8px;min-height:150px">
          {hexn(i, HC[(i-1) % 5])}<b style="font:400 18px/1.15 CB">{s}</b>
          <span style="font-size:14px;line-height:1.3">Tool: {t}</span><div style="margin-top:auto">{st}</div></div>'''
    segs = ''.join(f'<span style="flex:1;height:10px;background:{"#acc90b" if i < 3 else "#4a4170"}"></span>' for i in range(10))
    return f'''<html><head><style>{FONTS}</style></head><body style="width:1440px;height:810px;overflow:hidden;background:#fff">
<header style="display:flex;align-items:center;gap:14px;padding:14px 40px;border-bottom:2px solid #dae2e6">
  <img src="{HERE}/tcll-brandmark.png" style="width:36px"><span style="font:400 19px CB">The Care Leaders Online</span>
  <nav style="margin-left:40px;display:flex;gap:28px;font:400 15px CS;color:#312b6c"><span>Home</span><span style="color:#cf0f55">My courses</span><span>Learning library</span><span>Certificates</span></nav>
  <span style="margin-left:auto;display:flex;align-items:center;gap:10px;font:400 15px CS"><span style="width:34px;height:34px;background:#5f3c90;color:#fff;display:flex;align-items:center;justify-content:center;font:400 14px CB">ST</span>Sam T.</span>
</header>
<section style="background:#241b40 url({A}/img/tcll/tcll-pattern.jpg) center/cover;color:#fff;height:340px;padding:40px 40px 0;position:relative">
  {strip('Online course and toolkit', 'ribbon', 'apple', 'color:#241b40;font-size:14px')}
  <h1 style="font:400 60px/1 CB;margin:16px 0 12px">The NVR Toolkit</h1>
  <p style="font-size:20px;line-height:1.4;max-width:640px">Calm, safe, non-violent responses when behaviour escalates. Ten sections, with an interactive tool in each.</p>
  <div style="display:flex;align-items:center;gap:22px;margin-top:24px;width:640px">
    <div style="flex:1"><div style="display:flex;gap:4px">{segs}</div><p style="font:400 14px CS;margin-top:8px">3 of 10 sections complete</p></div>
    {strip('Continue: Baskets', 'arrow', 'apple', 'color:#241b40;font-size:17px;padding:11px 48px 12px 16px')}</div>
  <img src="{A}/img/tcll/blocks/block-1.webp" style="position:absolute;right:40px;bottom:0;height:300px">
</section>
<section style="padding:26px 40px">
  <div style="display:flex;align-items:baseline;gap:16px;margin-bottom:16px"><h2 style="font:400 28px CB">Your sections</h2><span style="font:400 15px CS;color:#312b6c">12 months' access · Certificate on completion</span></div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px">{cards}</div>
</section></body></html>'''

# ---------- phone: hot-moment protocol (390 x 844) ----------
def phone():
    rows = [('What I notice first', 'Voice gets louder. Starts pacing by the door.'),
            ('My cold-iron line', '"I\'m not going to argue. I\'m staying right here."'),
            ('What I will not do', 'Shout, threaten, or make a deal in the moment.'),
            ('When I come back to it', 'Tomorrow, once we are both calm.')]
    f = ''.join(f'''<div style="margin-bottom:12px"><p style="font:400 13px CS;color:#5f3c90;margin-bottom:5px">{i}. {a}</p>
      <div style="border:2px solid #dae2e6;background:#fff;padding:10px 12px;font-size:14.5px;line-height:1.35">{b}</div></div>'''
                for i, (a, b) in enumerate(rows, 1))
    segs = ''.join(f'<span style="flex:1;height:6px;background:{"#acc90b" if i < 3 else "#dae2e6"}"></span>' for i in range(10))
    return f'''<html><head><style>{FONTS}</style></head><body style="width:390px;height:844px;overflow:hidden;background:#f0f1df;position:relative">
<div style="height:46px;background:#241b40"></div>
<header style="background:#241b40;color:#fff;padding:4px 18px 14px">
  <p style="font:400 12px CS;color:#acc90b">Section 3 · De-escalation</p>
  <div style="display:flex;gap:3px;margin-top:10px">{segs}</div></header>
<main style="padding:18px 18px 0">
  {strip('Tool', 'angled', 'teal', 'font-size:12px;padding:5px 26px 6px 10px')}
  <h1 style="font:400 29px/1.05 CB;margin:10px 0 8px">Your hot-moment protocol</h1>
  <p style="font-size:15px;line-height:1.4;margin-bottom:16px">Plan what you will say and do before the next hot moment with your young person.</p>
  {f}
  <div style="display:flex;gap:10px;margin-top:6px">{strip('Save to my plan', 'arrow', 'fuchsia', 'font-size:14px;padding:10px 40px 11px 12px')}
  <span style="font:400 13px CS;color:#312b6c;align-self:center">Download PDF</span></div>
  <div style="background:#312b6c;color:#fff;padding:14px 16px;margin-top:18px"><p style="font:400 12px CS;color:#acc90b">Key learning</p>
  <p style="font:400 16px/1.3 CB;margin-top:4px">Strike when the iron is cold. Stay present now, respond later.</p></div>
</main>
<footer style="position:absolute;left:0;right:0;bottom:0;height:64px;background:#fff;border-top:2px solid #dae2e6;display:flex;align-items:center;justify-content:space-between;padding:0 18px 10px;font:400 14px CS">
  <span style="color:#312b6c">Previous</span>{strip('Next: Baskets', 'arrow', 'apple', 'color:#241b40;font-size:13px;padding:7px 34px 8px 10px')}</footer></body></html>'''

# ---------- workbook (A4 794 x 1123) ----------
def wb_cover():
    return f'''<html><head><style>{FONTS}</style></head><body style="width:794px;height:1123px;overflow:hidden;background:#dae2e6;position:relative">
<div style="position:absolute;left:0;top:0;width:794px;height:590px;background:#241b40"></div>
<img src="{K}/strips/angled-apple.png" style="position:absolute;left:560px;top:0;width:90px;height:60px">
<img src="{K}/strips/hex-teal.png" style="position:absolute;left:600px;top:96px;width:110px;height:64px">
<img src="{K}/strips/arrow-purple.png" style="position:absolute;left:540px;top:190px;width:200px;height:56px">
<img src="{K}/strips/ribbon-fuchsia.png" style="position:absolute;left:580px;top:276px;width:130px;height:40px">
<div style="position:absolute;left:56px;top:250px;color:#fff;width:470px">
  <h1 style="font:400 92px/.95 CB">NVR<br>Essentials</h1>
  <p style="font:400 21px CS;color:#acc90b;margin:18px 0 12px">Non-violent resistance</p>
  <p style="font-size:21px;line-height:1.45">Calm, safe responses when a young person's behaviour escalates, and a plan to repair afterwards.</p></div>
<img src="{HERE}/learner-solo.png" style="position:absolute;right:30px;top:330px;height:470px">
<div style="position:absolute;left:56px;top:636px;width:400px">
  <p style="font:400 17px CS;color:#5f3c90">Course workbook</p>
  <p style="font-size:17px;line-height:1.5;margin-top:8px">For anyone who works with or cares for children and young people. Yours to keep.</p></div>
<div style="position:absolute;left:56px;top:930px">
  <p style="font:400 15px CS;color:#5f3c90">This workbook belongs to</p><div style="width:400px;border-bottom:2px solid #0e2545;height:40px"></div>
  <p style="font:400 15px CS;color:#5f3c90;margin-top:26px">Date started</p><div style="width:220px;border-bottom:2px solid #0e2545;height:40px"></div></div>
<img src="{HERE}/tcll-logo-landscape.png" style="position:absolute;right:56px;bottom:56px;width:170px">
</body></html>'''

def wb_page():
    qs = ['What do you notice first when your young person starts to escalate?',
          'Write your cold-iron line. Short, calm, and something you can say on any shift.',
          'What will you not do in the moment?',
          'When and how will you come back to it once everyone is calm?']
    lines = lambda n: ''.join('<div style="border-bottom:1.5px solid #b9c6cd;height:34px"></div>' for _ in range(n))
    body = ''.join(f'''<div style="display:grid;grid-template-columns:40px 1fr;margin-bottom:18px"><span style="font:400 28px CB;color:#5f3c90">{i}</span>
      <div><p style="font:400 16px/1.35 CS">{q}</p>{lines(3)}</div></div>''' for i, q in enumerate(qs, 1))
    return f'''<html><head><style>{FONTS}</style></head><body style="width:794px;height:1123px;overflow:hidden;background:#dae2e6;position:relative">
<div style="display:flex;justify-content:space-between;padding:40px 56px 12px;font:400 13px CS;border-bottom:1.5px solid #b9c6cd;margin:0 0 0">
  <span style="color:#5f3c90">NVR Essentials · Course workbook</span><span>Action</span></div>
<div style="background:#312b6c;color:#fff;padding:30px 56px 30px;margin-top:22px">
  <h1 style="font:400 38px CB">Your hot-moment protocol</h1>
  <p style="font-size:17px;line-height:1.45;margin-top:8px;max-width:560px">Keep your young person in mind. Plan this now, while you are calm, so you are not deciding in the moment.</p></div>
<div style="background:#fff;margin:26px 48px 0;padding:28px 30px 10px">{body}</div>
<div style="position:absolute;left:56px;right:56px;bottom:36px;display:flex;justify-content:space-between;font:400 13px CS"><span>thecareleaders.com</span><span>14</span></div>
</body></html>'''

async def shoot(pg, html, w, h, path, scale):
    await pg.set_viewport_size({'width': w, 'height': h})
    f = OUT / '_tmp.html'; f.write_text(html)
    await pg.goto(f'file://{f}'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
    await pg.screenshot(path=str(path)); f.unlink()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, html, w, h, sc in [('laptop-screen', laptop(), 1440, 810, 1), ('phone-screen', phone(), 390, 844, 2),
                                     ('nvr-workbook-cover', wb_cover(), 794, 1123, 1), ('nvr-workbook-page', wb_page(), 794, 1123, 1)]:
            pg = await b.new_page(device_scale_factor=sc)
            await shoot(pg, html, w, h, OUT / f'{name}.png', sc); await pg.close()
        await b.close()

def rr(size, r, fill):
    im = Image.new('RGBA', size, (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill); return im

def frames():
    mid, navy = (36, 27, 64, 255), (14, 37, 69, 255)
    # laptop
    scr = Image.open(OUT / 'laptop-screen.png').convert('RGBA')
    bz = 34; W, H = scr.width + bz * 2, scr.height + bz * 2 + 10
    lap = Image.new('RGBA', (W + 160, H + 60), (0, 0, 0, 0))
    lid = rr((W, H), 36, mid); lid.paste(scr, (bz, bz + 6)); lap.alpha_composite(lid, (80, 0))
    d = ImageDraw.Draw(lap)
    d.polygon([(0, H + 12), (W + 160, H + 12), (W + 120, H + 58), (40, H + 58)], fill=navy)
    d.rectangle([80, H, W + 80, H + 12], fill=(49, 43, 108, 255))
    d.rectangle([(W + 160) // 2 - 110, H + 12, (W + 160) // 2 + 110, H + 22], fill=(36, 27, 64, 255))
    lap.save(OUT / 'nvr-laptop.png')
    # phone
    ps = Image.open(OUT / 'phone-screen.png').convert('RGBA')
    pb = 26; ph = rr((ps.width + pb * 2, ps.height + pb * 2), 110, mid)
    m = rr(ps.size, 84, (255, 255, 255, 255)); scr2 = Image.new('RGBA', ps.size, (0, 0, 0, 0)); scr2.paste(ps, (0, 0), m)
    ph.alpha_composite(scr2, (pb, pb))
    ImageDraw.Draw(ph).rounded_rectangle([ph.width // 2 - 110, pb + 26, ph.width // 2 + 110, pb + 86], 30, fill=(0, 0, 0, 255))
    ph.save(OUT / 'nvr-phone.png')
    for n in ('laptop-screen', 'phone-screen'):
        (OUT / f'{n}.png').unlink()
    # downsize workbook pages for print at 2x display size
    for n in ('nvr-workbook-cover', 'nvr-workbook-page'):
        im = Image.open(OUT / f'{n}.png').convert('RGB'); im.save(OUT / f'{n}.jpg', quality=90); (OUT / f'{n}.png').unlink()
    for n in ('nvr-laptop', 'nvr-phone'):
        im = Image.open(OUT / f'{n}.png'); im.thumbnail((1400, 1400)); im.save(OUT / f'{n}.png', optimize=True)

if __name__ == '__main__':
    asyncio.run(main()); frames(); print(sorted(p.name for p in OUT.iterdir()))
