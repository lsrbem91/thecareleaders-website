"""Keynote brochure in The Care Leaders branding.

  python3 tools/brochures/tcl.py [out_dir]  -> keynotes-brochure-tcl.pdf

Content and page order come from catalogue.keynotes3() (sections, Story, Theory, Action keynote pages).
This file swaps in The Care Leaders brand: the colour system from the TCL Brand Guidelines, the TCL logo,
TCL visual toolkit icons and the finished TCL imagery (Branding - TCL > 2. TCL Brand > 6. Imagery).
"""
import re, sys, pathlib, subprocess, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PIL import Image
from build import K, A, HERE, e, opt
import catalogue

NA, TE, OR, IN, PU, AG = '#0e2545', '#008196', '#fbab1e', '#4e2b53', '#7c05ca', '#a4cd39'   # TCL brand colours
BLUEBED, ORANGEBED = '#dae2e6', '#eee0d5'
T = K / 'tcl'
LOGO, LOGO_W = T / 'tcl-logo-full.png', A / 'img/logos/tcl-white.png'
BR = A / 'img/brand'
# Each Learning colour takes the nearest TCL colour, so every shape keeps its role
MAP = {'fuchsia': OR, 'red': OR, 'apple': OR, 'purple': IN, 'brightpurple': PU, 'indigo': NA,
       'midnight': NA, 'navy': NA, 'teal': TE, 'midgreen': AG, 'white': '#ffffff'}
STRIPS = K / 'strips-tcl'

def recolour():
    STRIPS.mkdir(exist_ok=True)
    for f in (K / 'strips').glob('*.png'):
        out = STRIPS / f.name
        if out.exists() and out.stat().st_mtime > f.stat().st_mtime: continue
        im = Image.open(f).convert('RGBA'); a = im.getchannel('A')
        col = MAP[f.stem.split('-', 1)[1]]
        o = Image.new('RGBA', im.size, tuple(int(col[i:i + 2], 16) for i in (1, 3, 5)) + (255,)); o.putalpha(a); o.save(out, optimize=True)

def icons(*names):
    return '<div class="dvpx tclic">' + ''.join(f'<img src="{n}" alt="">' for n in names) + '</div>'

THEME = {
    'talk_img': {'Living a Careless Life': T / 'young-person-1.png', 'Just Say Yes': T / 'foster-carer.png',
                 'The Power of the Profile': T / 'social-worker.png', 'Tools for Schools': T / 'teacher.png',
                 'Lived Experience Leadership': T / 'senior-manager.png', 'From Care Leaver to Care Leader': T / 'young-person-2.png',
                 'Be the First Yes': T / 'lived-experience-leader.png'},
    'sta_icons': [T / 'icon-338.png', T / 'icon-551.png', BR / 'arrow-orange.png'],
    'div': {2: f'<img class="dvimg" src="{opt(T / "tablet.png", 620)}" alt="">',
            3: f'<img class="dvimg" src="{opt(T / "directors.png", 620)}" alt="">',
            4: icons(T / 'icon-341.png', T / 'icon-443.png', T / 'icon-428.png')},
}
# TCL icons for the remaining Learning pictograms, in page order, each chosen for what it sits beside
PICTO_SEQ = [T / 'icon-341.png',  # custom keynote: a conversation
             T / 'icon-338.png', BR / 'bolt-orange.png', T / 'icon-551.png', BR / 'arrow-teal.png',  # planning call, keynote, workbook, recording and course
             T / 'icon-337.png', T / 'icon-547.png', BR / 'arrow-navy.png',  # story, theory, action
             T / 'icon-463.png',  # stays for questions
             T / 'icon-379.png', BR / 'crown-orange.png', T / 'icon-550.png', T / 'icon-340.png',  # why us
             T / 'icon-442.png']  # fees note

CSS_SWAP = [('#241b40', NA), ('#312b6c', NA), ('#5f3c90', IN), ('#acc90b', OR), ('#7c05ca', TE), ('#cf0f55', TE),
            ('.bed-purple{background:#ede3ed}', f'.bed-purple{{background:{ORANGEBED}}}'), ('.bed-green{background:#f0f1df}', f'.bed-green{{background:{ORANGEBED}}}'),
            ('.bed-red{background:#f9e2df}', f'.bed-red{{background:{ORANGEBED}}}')]
EXTRA = f'''
/* The Care Leaders grounds: navy for dark pages, white, blue bed and orange bed; no Learning patterns */
.pg.dark,.pg.dark.tmid{{background:{NA} !important}}.pg.tpale{{background:{BLUEBED} !important}}
.pg.cover{{background:#fff !important;color:{NA}}}
.cover h1{{color:{NA}}}.cover .hl{{color:{NA}}}.cover .hl .apple{{color:{TE}}}.cover .intro{{color:{NA}}}
.cover .logo{{height:84px;width:auto}}.cover .cov{{top:170px}}.cover .gl{{color:#fff}}.cover .gl *{{color:#fff}}
h2{{color:{NA}}}.dark h2,.dark h3{{color:#fff}}
.nav img.bm{{height:30px !important;width:auto !important;max-width:none !important;margin-right:8px}}
[style*="-fuchsia.png"],[style*="-red.png"],[style*="-apple.png"],[style*="-midgreen.png"]{{color:{NA} !important}}
[style*="-fuchsia.png"] *,[style*="-red.png"] *,[style*="-apple.png"] *,[style*="-midgreen.png"] *{{color:{NA} !important}}
[style*="-white.png"] h3{{color:{NA} !important}}
[style*="-purple.png"],[style*="-brightpurple.png"],[style*="-indigo.png"],[style*="-navy.png"],[style*="-teal.png"]{{color:#fff !important}}
img.tcli{{object-fit:contain}}
.tclic img{{width:150px;height:150px;object-fit:contain}}
.k3i{{height:230px}}
'''

def build(out):
    recolour()
    slug, title, P = catalogue.keynotes3(THEME)
    h = ''.join(P)
    h = h.replace(f'{K}/strips/', f'{STRIPS}/')
    h = h.replace(f'{A}/img/tcll/tcll-logo-white.png', str(LOGO)).replace('alt="The Care Leaders Learning"', 'alt="The Care Leaders"')
    h = h.replace(f'{K}/brandmark.png', str(LOGO))
    h = re.sub(r'(<section class="pg dark(?! cover)[^"]*"[^>]*>(?:(?!</section>).)*?)' + re.escape(str(LOGO)), lambda m: m.group(1) + str(LOGO_W), h, flags=re.S)
    h = re.sub(r'background:#241b40 url\([^)]*\)[^;"]*', f'background:{NA}', h)
    h = h.replace(f'{K}/chev.png', str(BR / 'arrow-orange.png'))
    seq = iter(PICTO_SEQ)
    n = len(re.findall(r'src="[^"]*/picto/p\d\d\.png"', h)); assert n == len(PICTO_SEQ), (n, len(PICTO_SEQ))
    h = re.sub(r'class="([^"]*)" src="[^"]*/picto/p\d\d\.png"', lambda m: f'class="{m.group(1)} tcli" src="{next(seq)}"', h)
    h = h.replace('Every Care Leaders Learning course, keynote, workbook and online lesson', 'Every Care Leaders course, keynote, workbook and online lesson')
    h = h.replace('Keynotes with Luke Rodgers BEM · The Care Leaders Learning', 'Keynotes with Luke Rodgers BEM · The Care Leaders')
    css = (HERE / 'brochure.css').read_text().replace('{ACC}', '#cf0f55').replace('{A}', str(A)).replace('{K}', str(K)) + catalogue.EXTRA_CSS
    css = re.sub(r'(\.dark\{background:)#241b40 url\([^)]*\) center/cover', r'\1' + NA, css)
    for a, b in CSS_SWAP: css = css.replace(a, b)
    css += EXTRA
    slug = 'keynotes-brochure-tcl'
    hp = out / f'{slug}.html'
    hp.write_text(f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Keynotes: The Care Leaders</title><style>{css}</style></head><body>{h}</body></html>')
    pdf = out / f'{slug}.pdf'
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{hp}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.pdf({{path:'{pdf}',width:'1280px',height:'720px',printBackground:true,margin:{{top:0,right:0,bottom:0,left:0}}}});
await b.close()}})();"""
    subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
    print(pdf)

if __name__ == '__main__':
    build(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else A / 'docs/brochures')
