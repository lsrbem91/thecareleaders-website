"""Keynote brochure, option 3: Luke Speaks colours, logo and plain grounds, with the
Care Leaders Learning pictograms, hand-cut strips, boxes and hexagons recoloured to the Luke Speaks palette.

  python3 tools/brochures/hybrid.py [out_dir]  -> keynotes-brochure-hybrid.pdf

Content comes from catalogue.keynotes(), so all three keynote brochures stay in step.
"""
import re, sys, pathlib, subprocess, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PIL import Image
from build import K, A, HERE, e
import catalogue

OR, TE, PL, NA = '#fbab1e', '#008196', '#4e2b53', '#0e2545'
CREAM, BLUE = '#f6efe4', '#dae2e6'
LOGO = A / 'img/logos/luke-speaks.png'
# Each Learning colour takes the nearest Luke Speaks colour, so every shape keeps its role.
MAP = {'fuchsia': OR, 'red': OR, 'apple': OR, 'purple': PL, 'brightpurple': PL, 'indigo': NA,
       'midnight': NA, 'navy': NA, 'teal': TE, 'midgreen': TE, 'white': '#ffffff'}
LS_STRIPS = K / 'strips-ls'
LOGO_REV = K / 'luke-speaks-reversed.png'

def reversed_logo():
    """The Luke Speaks logo for navy pages: the navy lettering turned white, the orange kept."""
    im = Image.open(LOGO).convert('RGBA'); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and r < 120 and g < 120: px[x, y] = (255, 255, 255, a)
    im.save(LOGO_REV, optimize=True)

def recolour():
    """Tint the hand-cut strip, box and hexagon PNGs to the Luke Speaks palette, keeping their cut edges."""
    LS_STRIPS.mkdir(exist_ok=True)
    for f in (K / 'strips').glob('*.png'):
        col = f.stem.split('-', 1)[1]
        out = LS_STRIPS / f.name
        if out.exists() and out.stat().st_mtime > f.stat().st_mtime: continue
        im = Image.open(f).convert('RGBA'); a = im.getchannel('A')
        rgb = tuple(int(MAP[col][i:i + 2], 16) for i in (1, 3, 5))
        o = Image.new('RGBA', im.size, rgb + (255,)); o.putalpha(a); o.save(out, optimize=True)

CSS_SWAP = [('#241b40', NA), ('#312b6c', NA), ('#5f3c90', PL), ('#acc90b', OR), ('#7c05ca', TE), ('#cf0f55', PL),
            ('.bed-purple{background:#ede3ed}', f'.bed-purple{{background:{CREAM}}}'), ('.bed-green{background:#f0f1df}', f'.bed-green{{background:{CREAM}}}'),
            ('.bed-red{background:#f9e2df}', f'.bed-red{{background:{CREAM}}}')]
EXTRA = f'''
/* Luke Speaks grounds: plain navy for dark pages, cream and blue beds, no Learning patterns */
.pg.dark,.pg.dark.tmid{{background:{NA} !important}}.pg.tpale{{background:{BLUE} !important}}
.pg.cover{{background:{CREAM} !important;color:{NA}}}
.cover h1{{color:{PL}}}.cover .hl{{color:{NA}}}.cover .hl .apple{{color:{TE}}}.cover .intro{{color:{NA}}}
.cover .logo{{height:92px;width:auto}}.cover .cov{{top:170px}}.cover .gl{{color:#fff}}.cover .gl *{{color:#fff}}
h2{{color:{PL}}}.dark h2,.dark h3{{color:#fff}}
.bm{{height:34px;width:auto}}
/* text on the orange shapes is dark, as in the Luke Speaks kit */
[style*="-fuchsia.png"],[style*="-red.png"],[style*="-apple.png"]{{color:#2a1830 !important}}
[style*="-fuchsia.png"] *,[style*="-red.png"] *,[style*="-apple.png"] *{{color:#2a1830 !important}}
[style*="-white.png"] h3{{color:{PL} !important}}
[style*="-purple.png"],[style*="-brightpurple.png"],[style*="-indigo.png"],[style*="-navy.png"],[style*="-teal.png"]{{color:#fff !important}}
'''

def build(out, src='keynotes', slug_out='keynotes-brochure-hybrid'):
    recolour(); reversed_logo()
    slug, title, P = getattr(catalogue, src)()
    h = ''.join(P)
    h = h.replace(f'{K}/strips/', f'{LS_STRIPS}/')
    h = h.replace(f'{A}/img/tcll/tcll-logo-white.png', str(LOGO)).replace('alt="The Care Leaders Learning"', 'alt="Luke Speaks"')
    h = h.replace(f'{K}/brandmark.png', str(LOGO))
    # navy pages carry the reversed logo
    h = re.sub(r'(<section class="pg dark(?! cover)[^"]*"[^>]*>(?:(?!</section>).)*?)' + re.escape(str(LOGO)), lambda m: m.group(1) + str(LOGO_REV), h, flags=re.S)
    h = re.sub(r'background:#241b40 url\([^)]*\)[^;"]*', f'background:{NA}', h)
    h = h.replace('Why choose The Care Leaders Learning', 'Why book Luke')
    h = h.replace('Keynotes with Luke Rodgers BEM · The Care Leaders Learning', 'Keynotes with Luke Rodgers BEM · Luke Speaks')
    css = (HERE / 'brochure.css').read_text().replace('{ACC}', '#cf0f55').replace('{A}', str(A)).replace('{K}', str(K)) + catalogue.EXTRA_CSS
    css = re.sub(r'(\.dark\{background:)#241b40 url\([^)]*\) center/cover', r'\1' + NA, css)
    for a, b in CSS_SWAP: css = css.replace(a, b)
    css += EXTRA
    slug = slug_out
    hp = out / f'{slug}.html'
    hp.write_text(f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Keynotes: Luke Speaks</title><style>{css}</style></head><body>{h}</body></html>')
    pdf = out / f'{slug}.pdf'
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.pdf({{path:'{pdf}',width:'1280px',height:'720px',printBackground:true,margin:{{top:0,right:0,bottom:0,left:0}}}});
await b.close()}})();"""
    subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
    print(pdf)

if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else A / 'docs/brochures'
    if len(sys.argv) > 2: build(out, sys.argv[2], sys.argv[3])
    else: build(out)
