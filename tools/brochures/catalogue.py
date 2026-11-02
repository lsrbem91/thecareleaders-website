"""Build the two summary brochures that go out with website enquiries:

  python3 tools/brochures/catalogue.py training [out_dir]   -> training-brochure.pdf (all courses)
  python3 tools/brochures/catalogue.py keynotes [out_dir]   -> keynotes-brochure.pdf (all keynotes)

Same design system and shared pages as the course brochures (build.py): Crossten, the Learning
palette, hand-cut strips and boxes, the TCLL pictograms. No shadows, filters, masks or opacity.
Course cards are read from courses/*.json, so the training brochure stays in step with the course brochures.
"""
import html, json, os, re, sys, subprocess, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build import strip, picto, opt, hires, box, ground, K, A, HERE, e

def nav(items, cur, dark):
    out = [strip(t, 'angled', 'apple' if dark else 'fuchsia', 'navon') if k == cur else f'<span class="navi">{e(t)}</span>' for k, t in items]
    return f'<nav class="nav"><img class="bm" src="{K}/brandmark.png" alt="">{"".join(out)}</nav>'

def make_page(items, label):
    def page(inner, cls, sec=None, n=None, t=None, bg=None, div=None):
        top = nav(items, sec, 'dark' in cls) if sec else ''
        foot = f'<div class="foot"><span>{e(label)} · thecareleaders.com</span><span>{n}</span></div>' if n else ''
        toc = f' data-toc="{e(t)}" data-n="{n}"' if t else ''
        toc += f' data-div="{div}"' if div else ''
        st = f' style="{bg}"' if bg else ''
        return f'<section class="pg {cls}"{toc}{st}>{top}{inner}{foot}</section>'
    return page

def cover(name, cat, head, intro, img, glance, long=False):
    g = ''.join(f'<div class="gl{" wide" if w else ""}" style="{box("indigo")}"><b>{e(a)}</b><span>{e(b)}</span><small>{e(c)}</small></div>' for a, b, c, w in glance)
    return f'''<section class="pg dark cover"><img class="logo" src="{A}/img/tcll/tcll-logo-white.png" alt="The Care Leaders Learning">
      <div class="cov">{strip(cat, 'ribbon', 'apple', 'cat')}<h1{' class="long"' if long else ''}>{e(name)}</h1><p class="hl">{head}</p><p class="intro">{e(intro)}</p></div>
      <img class="covimg" src="{img}" alt=""><div class="glance">{g}</div></section>'''

def contents(P, page, ci):
    items = []
    for k, pg in enumerate(P):
        if k in (0, ci): continue
        m = re.search(r'data-toc="([^"]+)" data-n="(\d+)"(?: data-div="(\d+)")?', pg)
        if m: items.append((m.group(2), html.unescape(m.group(1)), m.group(3)))
    hc = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']
    if not any(d for _, _, d in items):
        lis = ''.join(f'<li><span class="hx cx" style="background-image:url({K}/strips/hex-{hc[i % 5]}.png)">{n}</span>{e(t)}</li>' for i, (n, t, _) in enumerate(items))
        return page(f'<h2>Contents</h2><ol class="toc">{lis}</ol>', 'light', None, ci + 1)
    # Sectioned: each section opener starts a block; the pages after it sit under it
    secs = []
    for n, t, d in items:
        if d: secs.append([d, t, n, []])
        elif secs: secs[-1][3].append((n, t))
    blocks = ''
    for i, (d, t, n, sub) in enumerate(secs):
        lis = ''.join(f'<li><span class="tcn">{pn}</span>{e(pt)}</li>' for pn, pt in sub)
        blocks += f'''<div class="tcs" style="{box('white')}"><div class="tch"><span class="hx cx" style="background-image:url({K}/strips/hex-{hc[i % 5]}.png)">{d}</span>
          <h3>{e(t)}</h3><span class="tcp">from page {n}</span></div><ol>{lis}</ol></div>'''
    return page(f'<h2>Contents</h2><div class="tcg">{blocks}</div>', 'light', None, ci + 1)

def divider(page, d, n, title, lead, inside, grd, extra='', img=None):
    """Section opener: number, title, the question the section answers, and what is inside."""
    lis = ''.join(f'<li><img src="{K}/chev.png" alt="">{e(x)}</li>' for x in inside)
    return page(f'''<div class="dvl{' dvn' if extra else ''}">{strip(f'Section {d}', 'ribbon', 'apple', 'cat')}<h1 class="dvh">{e(title)}</h1>
      <p class="dvp">{e(lead)}</p><ul class="dvi">{lis}</ul></div>{extra}{f'<img class="dvimg" src="{img}" alt="">' if img else ''}''',
      'dark divp', None, n, title, ground(grd) if grd in ('tonal-midnight',) or not grd.startswith('tonal') else f'background:#241b40 url({K}/tcll2026/{grd}.jpg) center/cover', d)

def what_it_does(c):
    """The course intro without the repeated 'Training that' opening, so 18 cards don't all start the same way."""
    t = c['intro']
    if t.startswith('Non-violent resistance training that helps '):
        return 'Uses non-violent resistance to help ' + t[len('Non-violent resistance training that helps '):]
    t = re.sub(r'^Training that ', '', t)
    return t[0].upper() + t[1:]

def sta_page(page, sec, n, line):
    sta = [(18, 'fuchsia', '', 'Story', 'A real moment from care, told from the young person\'s side.'),
           (6, 'purple', '', 'Theory', 'The thinking that explains it, with honest evidence.'),
           (17, 'midgreen', 'dk', 'Action', 'Something to practise and use at work the next day.')]
    cards = ''.join(f'<div class="sta {d}" style="background-image:url({K}/strips/arrowlong-{col}.png)">{picto(p, "pic stp")}<b>{t}</b><p>{x}</p></div>' for p, col, d, t, x in sta)
    return page(f'''<h2>How we teach: Story, Theory, Action</h2>
      <p class="sub">Every Care Leaders Learning course, keynote, workbook and online lesson follows the same three steps.</p>
      <div class="stas">{cards}</div><p class="tln">{strip("Every time", "ribbon", "apple", "mini")} {e(line)}</p>''', 'dark spine', sec, n, 'How we teach: Story, Theory, Action', ground('spine-bands'))

WHY = json.loads((HERE / 'courses/nvr-essentials.json').read_text())['why']
def why_page(page, sec, n, sub):
    w = WHY
    usps = ''.join(f'<div class="usp" style="{box("white")}">{picto(p)}<h3>{e(t)}</h3><p>{e(x)}</p></div>' for p, t, x in w['usps'])
    aws = ''.join(f'<div class="awl"><img src="{A}/img/{img}" alt="{e(a)}"><b>{e(a)}</b><p>{e(b)}</p></div>' for img, a, b in w['awards'])
    cols = ['apple', 'teal']
    stats = ''.join(f'<div class="wst {"dk" if cols[i] == "apple" else ""}" style="background-image:url({K}/strips/arrowlong-{cols[i]}.png)"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(w['stats']))
    return page(f'''<h2>{e(w['title'])}</h2><p class="sub">{e(sub)}</p>
      <div class="wgrid"><div class="usps">{usps}</div><div class="awbox" style="{box('white')}">{strip('Award winning', 'angled', 'purple', 'mini')}{aws}</div></div>
      <div class="wsts">{stats}</div>''', 'dark tmid', sec, n, w['title'])

BIO = ["Luke went into care at 10. He has spent his career inside children's services as a consultant, trainer and keynote speaker, and is CEO of The Care Leaders.",
       "He has worked with councils nationally, including Durham County Council, where he put NVR into 11 children's homes and trained 120 residential staff, online and face to face.",
       "He led the national engagement on England's new fostering standards for the Department for Education.",
       "He is a former Knowledge Equity Fellow at Saïd Business School, University of Oxford, and was awarded the British Empire Medal in 2018 for commitment to children and families."]
SPEAK = [("45+", "keynotes since the start of 2024"), ("4,000+", "delegates have heard Luke speak since 2024"), ("400", "people in the largest single room so far")]
def luke_page(page, sec, n, image, for_line, quote, role):
    paras = ''.join(f'<p>{e(x)}</p>' for x in BIO)
    pcol = ['fuchsia', 'purple', 'teal']
    proof = ''.join(f'<div class="pf" style="{box(pcol[i])}"><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(SPEAK))
    return page(f'''<div class="fac"><div class="fl1"><img class="fph" src="{A}/img/brand/{image}" alt="Luke Rodgers BEM">
        {strip('From care leaver to care leader', 'ribbon', 'fuchsia', 'cat')}</div>
      <div class="fl2">{strip(role, 'angled', 'purple', 'mini')}<h2>Luke Rodgers BEM</h2><div class="fps">{paras}</div>
        <p class="fcourse">{picto(17, 'pic xs')}{e(for_line)}</p></div>
      <div class="fl3">{strip('On stage', 'angled', 'teal', 'mini')}<div class="pfs">{proof}</div>
        <blockquote style="{box("indigo")}">"{e(quote[0])}"<cite>{e(quote[1])}</cite></blockquote></div></div>''',
      'light', sec, n, f'{role}: Luke Rodgers BEM')

def fees_page(page, sec, n, title, cards, note, imgs):
    def fc(k, f):
        pts = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in f['points'])
        return f'''<div class="fc" style="{box('white')}"><img class="fimg" src="{imgs[k]}" alt="">{strip(f['label'], 'angled', 'teal', 'fl')}
          <p class="flen">{e(f['length'])}</p><p class="ftime">{e(f['time'])}</p><p class="fee">{e(f['fee'])} <span>{e(f['fee_note'])}</span></p><ul>{pts}</ul></div>'''
    return page(f'''<h2>{e(title)}</h2><div class="fcs">{''.join(fc(k, f) for k, f in enumerate(cards))}</div>
      <p class="fnote">{picto(12, 'pic xs')}{e(note)}</p>''', 'bed-blue', sec, n, title)

def book_page(page, sec, title, steps, legal, extra='', n=None):
    scol = ['apple', 'teal', 'brightpurple', 'indigo']
    st = ''.join(f'<div class="st {"dk" if scol[i] == "apple" else ""}" style="background-image:url({K}/strips/arrow-{scol[i]}.png)"><span>{i + 1}</span><b>{e(a)}</b><p>{e(b)}</p></div>' for i, (a, b) in enumerate(steps))
    return page(f'''<h2>{e(title)}</h2><div class="sts s{len(steps)}">{st}</div>
      {strip('hello@thecareleaders.com', 'ribbon', 'apple', 'mail')}{extra}<p class="legal{' lgn' if n else ''}">{legal}</p>''', 'tpale', sec, n, title if n else None)

def showcase_page(page, sec, n, slug, title, labels, free, half=None, note=None):
    S = K / 'showcase'
    strips = strip(free, 'ribbon', 'apple', 'dk') + (strip(half, 'ribbon', 'fuchsia') if half else '')
    nt = f'<p class="shnote">{e(note)}</p>' if note else ''
    return page(f'''<div class="shh"><h2>{e(title)}</h2></div>
      <img class="shl" src="{opt(S / f'{slug}-laptop.png', 1300)}" alt=""><img class="shp" src="{opt(S / f'{slug}-phone.png', 800)}" alt="">
      <img class="shw1" src="{S}/{slug}-workbook-cover.jpg" alt=""><img class="shw2" src="{S}/{slug}-workbook-page.jpg" alt="">
      <div class="shlb s1">{strip(labels[0], 'angled', 'purple')}</div><div class="shlb s2">{strip(labels[1], 'angled', 'teal')}</div>
      <div class="shlb s3">{strip(labels[2], 'angled', 'fuchsia')}</div><div class="shm">{strips}</div>{nt}''', 'bed-purple', sec, n, title)

AWARDS_LINE = 'Gold, Dual Perspective Leadership Award, iESE Public Sector Transformation Awards 2026 · Children &amp; Young People Now Workforce Development Award 2023'

# ---------------------------------------------------------------- training
# Courses grouped by who they are for (each course sits under its main audience; the "For" line shows the rest).
# Each entry is one page: (page title for the contents, [(group heading, course slugs)]).
SHELVES = [
    ('For carers and children\'s homes', [('For carers and children\'s homes', ['behind-the-behaviour', 'the-practice-toolkit', 'nvr-essentials', 'supporting-boys-in-care', 'trauma-attachment-transitions', 'care-not-custody'])]),
    ('For schools, social workers and other professionals', [('For schools', ['tools-for-schools', 'raising-aspirations', 'two-timetables']),
                                                             ('For social workers and other professionals', ['good-recording', 'language-that-lifts', 'the-person-behind-the-file'])]),
    ('For leaders, councils, young people and employers', [('For leaders, councils and young people', ['corporate-parenting-in-practice', 'co-producing-your-local-offer', 'five-s-framework', 'power-to-lead']),
                                                            ('For employers', ['leading-care-leavers-at-work', 'be-the-first-yes'])]),
]
def training():
    items = [('courses', 'The courses'), ('how', 'How we teach'), ('included', 'Included'), ('why', 'Why us'), ('fees', 'Fees'), ('book', 'Book')]
    page = make_page(items, 'Training · The Care Leaders Learning')
    C = {p.stem: json.loads(p.read_text()) for p in (HERE / 'courses').glob('*.json')}
    n_courses = sum(len(sl) for _, gs in SHELVES for _, sl in gs)
    assert n_courses == len(C), 'every course file must sit on a shelf'
    P = [cover('Training for the people around children in care', 'Training', f'{n_courses} courses. <span class="apple">Face to face or online.</span>',
               'Every course is written by people who have lived in care and people who have led services. Choose a course, then choose how your team learns it.',
               opt(hires('block-1.webp'), 960),
               [('Face to face or online', '6 hours in person, or 2 hours live online', 'you choose the format', True),
                ('60', 'people per course', 'one fee covers everyone', False), (str(n_courses), 'courses', 'all on the next pages', False)], long=True), '']
    num = lambda: len(P) + 1
    cols = ['fuchsia', 'purple', 'teal', 'indigo', 'midgreen', 'navy']
    beds = ['bed-purple', 'bed-blue', 'bed-green']
    hexes = ['purple', 'teal', 'indigo']
    # Section 1 opener doubles as the course finder: every course, numbered, under who it is for, with its page
    first = num() + 1
    idx, k = '', 0
    for s, (ptitle, groups) in enumerate(SHELVES):
        col = ''
        for g, (gt, slugs) in enumerate(groups):
            lis = ''
            for sl in slugs:
                k += 1; lis += f'<li><span class="hx" style="background-image:url({K}/strips/hex-{hexes[s]}.png)">{k}</span>{e(C[sl]["name"])}</li>'
            col += f'<p class="fnt">{e(gt)}<span>page {first + s}</span></p><ol>{lis}</ol>'
        idx += f'<div class="fnd">{col}</div>'
    P.append(divider(page, 1, num(), 'The courses', 'Find a course for your team, then choose face to face or online.',
                     [], 'tonal-midnight', f'<div class="fnds">{idx}</div>'))
    k = 0
    for s, (ptitle, groups) in enumerate(SHELVES):
        body = ''
        for g, (gt, slugs) in enumerate(groups):
            cards = ''
            for i, sl in enumerate(slugs):
                c = C[sl]; k += 1
                who = ', '.join([x[1] for x in c['audience']['groups'] if x[1] not in ('Both together', 'Your whole school')][:3])
                cards += f'''<div class="cc" style="{box('white')}"><span class="ccb" style="{box(cols[(i + s + g) % 6])}"></span>
                  <div class="cct"><span class="hx" style="background-image:url({K}/strips/hex-{hexes[s]}.png)">{k}</span><h3>{e(c['name'])}</h3></div>
                  <p class="cci">{e(what_it_does(c))}</p><p class="ccw"><b>For</b> {e(who)}</p></div>'''
            body += (f'<h2>{e(gt)}</h2>' if len(groups) == 1 else f'<h3 class="ccg">{e(gt)}</h3>') + f'<div class="ccs" style="grid-template-columns:repeat({4 if max(len(x[1]) for x in groups) == 4 else 3},1fr)">{cards}</div>'
        P.append(page(f'{body}<p class="ccf">Every course has its own page with the full details: thecareleaders.com/training</p>',
                      beds[s] + ' catp' + (' dbl' if len(groups) > 1 else ''), 'courses', num(), ptitle))
    # Two ways to run every course
    P.append(page(f'''<h2>Every course runs face to face or online</h2>
      <div class="two">
        <div class="tw" style="{box('navy')}">{picto(19)}{strip('Option 1', 'angled', 'apple', 'mini')}<h3>Face to face, a 6-hour day</h3>
          <p>Usually 10am to 4pm, in your building or a venue you choose, for up to 60 people. Time for every story and every activity, with practice in pairs and small groups.</p></div>
        <div class="tw" style="{box('purple')}">{picto(18)}{strip('Option 2', 'angled', 'apple', 'mini')}<h3>Live online, a 2-hour keynote</h3>
          <p>On Teams or Zoom, for up to 60 people. Luke gives the keynote, takes questions in the chat throughout and answers them live at the end. For teams who can&#8217;t give a full day.</p></div></div>
      <p class="tln dkl">{strip('Not sure which?', 'ribbon', 'apple', 'mini')} Try it online first, then get 20% off the face to face day. Details are with the fees.</p>''',
      'light', 'courses', num(), 'Every course runs face to face or online'))
    P.append(divider(page, 2, num(), 'How we teach', 'What happens in the room, and what your team keeps afterwards.',
                     ['Story, theory and action', 'What every delegate gets', 'The course online, on any device'], 'tonal-midnight', img=opt(K / 'tcll2026' / 'image-block-02.png', 620)))
    P.append(sta_page(page, 'how', num(), 'A story from care, the theory behind it, and a tool your team uses the next day.'))
    gets = [(20, 'Workbook', 'for life', 'Stories, tools and space to plan. Theirs to keep.'),
            (5, 'Recording', '12 months', 'A recording of the session to watch again for 12 months.'),
            (8, 'The course online', 'Free for 12 months', 'The course on our e-learning platform, The Care Leaders Online.'),
            (1, 'Certificate', 'of completion', 'For their development record.'),
            (16, '50% off', 'All our online training', "A year's membership of The Care Leaders Online at half price: every on-demand course, guest speakers and practice tools.")]
    g = ''.join(f'<div class="gi" style="{box("indigo")}">{picto(p)}<b>{e(t)}</b>{strip(s, "angled", "apple", "gs2")}<p>{e(d)}</p></div>' for p, t, s, d in gets)
    P.append(page(f'''<h2>What every delegate gets</h2><p class="sub">Face to face or online. All included in the fee.</p>
      <div class="gis">{g}</div><img class="incimg" src="{opt(K / 'tcll2026' / 'image-block-04.png', 600)}" alt="">''', 'light', 'included', num(), 'What every delegate gets'))
    P.append(showcase_page(page, 'included', num(), 'behind-the-behaviour', 'The course online, on any device',
                           ['The course home on a laptop', 'Every tool works on a phone', 'The workbook, theirs to keep'],
                           'Free for 12 months: the course online', 'All our online training: 50% off a year on The Care Leaders Online',
                           'Shown: Behind the Behaviour. Every course has its own online course and workbook.'))
    P.append(divider(page, 3, num(), 'Why choose us', 'Who builds the training, and who delivers it.',
                     ['Why us', 'Your facilitator'], 'tonal-midnight', img=opt(K / 'tcll2026' / 'image-block-06.png', 620)))
    P.append(why_page(page, 'why', num(), 'Training built by people who have lived in care and people who have led services.'))
    P.append(luke_page(page, 'why', num(), 'luke-speaking.jpg', 'Luke facilitates every course. Face to face he leads every part. Online, he gives the keynote and answers your questions live.',
                       ('Nothing was as transformative as hearing Luke speak about his life.', 'Dr Janet Rose, Principal, Norland College'), 'Your facilitator'))
    fmts = [{'label': 'Face to face', 'length': '6 hours', 'time': 'Usually 10am to 4pm', 'fee': '£3,950', 'fee_note': '+ VAT + travel expenses',
             'points': ['In your building or a venue you choose', 'Practice in pairs and small groups', 'You provide a room and a screen']},
            {'label': 'Live online', 'length': '2 hours', 'time': 'A live keynote with Q&A', 'fee': '£1,950', 'fee_note': '+ VAT',
             'points': ['On Teams or Zoom', 'Questions in the chat throughout', 'Live Q&A at the end']}]
    P.append(divider(page, 4, num(), 'Fees and booking', 'What it costs, and how to book.',
                     ['Fees for every course', 'Try it online first: 20% off the face to face day', 'Book your training in 4 steps'], 'tonal-midnight',
                     f'<div class="dvpx">{picto(19)}{picto(18)}{picto(16)}</div>'))
    P.append(fees_page(page, 'fees', num(), 'Fees for every course', fmts,
                       'The same fee for every course. One fee covers up to 60 people. We build examples from your own service into the training at no extra cost.',
                       [opt(hires('block-5.webp'), 500), opt(hires('block-3.webp'), 500)]))
    of = json.loads((HERE / 'courses/nvr-essentials.json').read_text())['offer']
    cl = [('teal', ''), ('apple', 'dk')]
    stp = ''.join(f'''<div class="ofs {cl[k][1]}" style="background-image:url({K}/strips/arrowlong-{cl[k][0]}.png)"><span class="ofn">{e(a)}</span>
        <div><b>{e(t)}</b><p class="ofp">{f'<s>{e(old)}</s> ' if old else ''}{e(fee)} <span>{e(note)}</span></p></div></div>''' for k, (a, t, fee, note, old) in enumerate(of['steps']))
    P.append(page(f'''<div class="ofl">{strip(of['tag'], 'ribbon', 'apple', 'cat')}<p class="ofb">{e(of['big'])}</p><p class="ofx">{e(of['line'])}</p></div>
      <div class="ofr">{stp}{strip(of['save'], 'ribbon', 'white', 'ofv dk')}</div><p class="oft">{e(of['terms'])}</p>''',
      'dark chev', 'fees', num(), 'Try it online first: 20% off the face to face day', ground('chevrons-colour')))
    P.append(book_page(page, 'book', 'Book your training in 4 steps',
                       [('Choose your course', 'Any of the courses in this brochure'), ('Choose your format', 'Face to face or live online'),
                        ('Pick a date', 'One that works for your team'), ('Book your training', 'Email us and we confirm it')],
                       f'{AWARDS_LINE} · The Care Leaders Ltd, company number 10782615 · thecareleaders.com', n=num()))
    P[1] = contents(P, page, 1)
    return 'training-brochure', 'Training: The Care Leaders Learning', P

# ---------------------------------------------------------------- keynotes
TALKS = [
    ('Living a Careless Life', 'What it is really like to grow up in care.', 'Whole services, conferences, schools and corporate parenting boards', 'A mixed audience',
     'Staff and leaders make decisions about children in care every day without hearing what it is like from the inside. Language, processes and missed moments can make a child feel like a case, and nobody in the room notices. This is the talk that changes that.',
     ['What children in care notice that adults miss', 'The moments that build trust, and the ones that break it', 'How systems and language can make children feel like a case', 'What one adult can change'], 14),
    ('Just Say Yes', 'Inspiring foster carers to say yes.', 'Foster carers, kinship carers and the fostering teams who support them', 'Foster carers',
     'Saying yes to a child often starts with a profile full of risks, behaviours and past moves, and rarely the full story. Then carers are asked to meet needs shaped by trauma and loss without training that explains why. That is not a failure of fostering. It is a gap in how we prepare carers, and this talk bridges it.',
     ['Understand how profiles shape what carers expect', 'Know the basics of trauma, attachment and behaviour as communication', 'Respond to hard moments with empathy, not fear', 'Leave with simple tools for daily care, and the confidence to say yes'], 19),
    ('The Power of the Profile', 'One day, the child will read what you wrote.', 'Social workers at every level, team managers, supervising social workers, IROs and students', 'Social workers',
     'The profile a social worker writes becomes a child\'s introduction to a school, a carer or a panel. It is often built from inherited case notes and incident logs, so the child is described by what went wrong. When the answer is no, it is the social worker who carries it. This talk is for the practitioner who knows the young person behind the paperwork.',
     ['Write profiles that inspire belief, not fear', 'Reframe behaviour through a trauma-informed lens', 'Understand the emotional and ethical weight of telling a child\'s story', 'Feel renewed confidence in advocating for a child'], 20),
    ('Tools for Schools', 'Read the behaviour, then reach for the right tool.', 'Headteachers, designated teachers, teachers and college staff', 'Schools and colleges',
     'For a child in care, school can become another place to feel misunderstood, especially when their past arrives as a behaviour record. Most teacher training doesn\'t cover trauma or children in care, yet schools are expected to be a critical support. This talk gives staff the understanding and the tools.',
     ['Read behaviour as communication and respond in the moment', 'Know what attachment and trauma look like in school', 'Understand how language and stigma shape a child\'s school life', 'Know where school and social care clash, and what to do about it'], 9),
    ('Lived Experience Leadership', 'Young people in service delivery and improvement, with the Five S framework.', 'Senior leaders, leadership teams and anyone who works with children', 'Senior leaders',
     'Most services involve young people in the same way: a consultation, a survey, a seat on a panel. That suits some young people and leaves others out. The Five S framework gives leaders a way to see where each young person is, from telling their story for the first time to leading the work and bringing the next person through, and offer a role that fits.',
     ['Know the five stages: storytelling, skills, strategies, scaling and succession', 'Recognise where the young people in their service are on it', 'Match young people to roles in service delivery and improvement that fit their stage', 'Plan how young people move through the stages, and who leads next'], 22),
    ('From Care Leaver to Care Leader', 'Your story as a strength, not a setback.', 'Care-experienced young people aged 14 and over, children in care councils and care leaver groups', 'Care-experienced young people',
     'Care-experienced young people are often described by other people\'s words: case notes, risk assessments and plans that follow them into school, housing and work. This talk helps them see that what they have lived through has built real skills, and that they can lead because of their experience, not in spite of it.',
     ['See their care experience as a strength, not a weakness', 'Recognise the skills they already have', 'Feel more confident about their future', 'See themselves as people who can lead change'], 1),
    ('Be the First Yes', 'Opening doors for care leavers in the workplace.', 'Employers, HR and early careers teams, hiring managers and social value leads', 'Employers',
     'Care leavers often start working life without the family networks, references and safety nets most people take for granted. Employers want to do the right thing but are not always sure how to start. Care leavers aren\'t asking for special treatment. They are asking for a chance, and this talk shows how to give one.',
     ['Understand who care leavers are and what support really looks like', 'Know how to make recruitment and induction care-aware', 'Plan mentoring and onboarding that helps people stay', 'Feel confident, not cautious, about being the first yes'], 21),
]
def keynotes():
    items = [('talks', 'The keynotes'), ('get', 'What you get'), ('luke', 'About Luke'), ('fees', 'Fees'), ('book', 'Book')]
    page = make_page(items, 'Keynotes with Luke Rodgers BEM · The Care Leaders Learning')
    P = [cover('Keynotes with Luke Rodgers BEM', 'Keynotes and conference workshops', 'From care leaver. <span class="apple">To care leader.</span>',
               'Story-led keynotes for conferences, staff days and boards: stories of care from Luke\'s lived experience, the theory behind them and tools your audience can use the next day.',
               opt(hires('block-2.webp'), 960),
               [('In person or online', 'keynotes of up to 90 minutes', 'or a conference workshop', True),
                (str(len(TALKS)), 'keynotes', 'or one built for your audience', False), ('4,000+', 'delegates since 2024', 'from 30 to 400 in a room', False)], long=True), '']
    num = lambda: len(P) + 1
    rows = ''.join(f'<li><span class="mxa">{e(aud)}</span><img src="{K}/chev.png" alt=""><b>{e(t)}</b></li>' for t, _, _, aud, _, _, _ in TALKS)
    P.append(page(f'''<h2>Find the keynote for your audience</h2>
      <div class="mx"><ol class="mxl">{rows}</ol>
        <div class="mxc" style="{box('navy')}">{picto(13)}<h3>Don&#8217;t see your audience here?</h3>
          <p>Tell us your conference theme, who&#8217;s coming and what you want them to leave with, and we&#8217;ll shape a custom keynote around them. It follows the same approach as every other talk, with the recording, the on-demand course and the workbook included.</p></div></div>''',
      'bed-purple', 'talks', num(), 'Find the keynote for your audience'))
    cols = ['fuchsia', 'purple', 'teal', 'indigo', 'midgreen', 'brightpurple', 'navy']
    beds = ['light', 'bed-blue', 'bed-green', 'bed-purple']
    for i, (t, tag, who, aud, para, outs, pc) in enumerate(TALKS):
        lis = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in outs)
        extra = ''
        if t == 'Lived Experience Leadership':
            five = [('Storytelling', 'Sharing their experience safely, on their own terms.'), ('Skills', 'Recognising and building the skills their experience has given them.'),
                    ('Strategies', 'Helping shape plans, services and decisions.'), ('Scaling', 'Leading pieces of work, such as training staff or running projects.'),
                    ('Succession', 'Mentoring and bringing the next young people through.')]
            hc = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']
            extra = '<ol class="fives">' + ''.join(f'<li><span class="hx" style="background-image:url({K}/strips/hex-{hc[k]}.png)">{k + 1}</span><b>{e(a)}.</b> {e(b)}</li>' for k, (a, b) in enumerate(five)) + '</ol>'
        flag = strip('Flagship talk', 'ribbon', 'apple', 'mini') if i == 0 else ''
        P.append(page(f'''<div class="kn{' five' if extra else ''}"><div class="knl">{strip('For ' + who[0].lower() + who[1:], 'angled', cols[i % 7], 'knf')}
            <h2>{e(t)}</h2><p class="knt">{e(tag)}</p>{flag}<p class="knp">{e(para)}</p>{extra}</div>
          <div class="knr"><div class="kno" style="{box('midnight')}">{picto(pc)}<h3>By the end, delegates will</h3><ul>{lis}</ul></div>
            <div class="knf3"><p><b>Length</b> 45 to 90 minutes</p><p><b>Format</b> Keynote or conference workshop, in person or online</p>
            <p><b>Comes with</b> The recording and an on-demand course for 12 months, plus a workbook to keep</p></div></div></div>''',
          beds[i % 4], 'talks', num(), t))
    four = [(9, 'Before the day', 'A planning call', ['A 30-minute planning call', 'The keynote shaped around your audience and theme', 'A title and blurb for your programme, plus Luke\'s photo and bio']),
            (18, 'On the day', 'The keynote', ['A keynote of up to 90 minutes', 'Time for questions and discussion', 'The slides, to share with delegates']),
            (20, 'On the day', 'A workbook for every delegate', ['Print-ready or digital', 'Activities for individuals and teams', 'Theirs to keep']),
            (8, 'After the day', 'The recording and course', ['The full keynote recorded', 'An on-demand course on The Care Leaders Online', '12 months\' access for every delegate'])]
    g = ''.join(f'<div class="gi g4" style="{box("indigo")}">{picto(p)}<b>{e(t)}</b>{strip(w, "angled", "apple", "gs2")}<ul>{"".join(f"<li>{e(x)}</li>" for x in pts)}</ul></div>' for p, w, t, pts in four)
    P.append(page(f'''<h2>More than a keynote</h2><p class="sub">Every booking, in person or online, comes with the same four things.</p>
      <div class="gis g4s">{g}</div>''', 'light', 'get', num(), 'More than a keynote: what every booking includes'))
    P.append(showcase_page(page, 'get', num(), 'tools-for-schools', 'The keynote course on any device',
                           ['The course home on a laptop', 'Every tool works on a phone', 'The workbook, theirs to keep'],
                           'Free for 12 months: the recording and the course', None,
                           'Shown: Tools for Schools. Every keynote has its own online course and workbook.'))
    P.append(sta_page(page, 'get', num(), 'Stories of care from Luke\'s lived experience, the theory behind them, and tools your audience uses the next day.'))
    P.append(luke_page(page, 'luke', num(), 'luke-lga-podium.jpg', 'Luke gives every keynote himself, in person or live online, and stays for questions.',
                       ('You demand bravery and humanity in equal measure.', 'Maggie Atkinson, former Children\'s Commissioner for England'), 'Your speaker'))
    P.append(why_page(page, 'luke', num(), 'Keynotes from someone who has lived in care and has led services.'))
    fmts = [{'label': 'In person', 'length': 'Keynote', 'time': 'Up to 90 minutes, at your event', 'fee': '£4,950', 'fee_note': '+ VAT + travel expenses',
             'points': ['A planning call before the day', 'A workbook for every delegate', 'The recording and course for 12 months']},
            {'label': 'Live online', 'length': 'Keynote', 'time': 'Up to 90 minutes, on Teams or Zoom', 'fee': '£2,490', 'fee_note': '+ VAT',
             'points': ['A planning call before the day', 'Questions in the chat and live Q&A', 'The recording and course for 12 months']}]
    P.append(fees_page(page, 'fees', num(), 'Fees for every keynote', fmts,
                       'Keynotes and conference workshops are contracted and invoiced by Luke Speaks Ltd, powered by The Care Leaders. If Luke is free, we hold your date for 14 days.',
                       [opt(hires('block-6.webp'), 500), opt(hires('block-3.webp'), 500)]))
    P.append(book_page(page, 'book', 'Book Luke in 4 steps',
                       [('Tell us about your event', 'The date, your audience and the talk'), ('Get availability and a fee', 'We hold the date for 14 days'),
                        ('Confirm by email', 'And send a purchase order if you use them'), ('Before the day', 'A planning call and a checklist')],
                       f'{AWARDS_LINE} · Luke Speaks Ltd, company number 15452230 · thecareleaders.com/keynotes'))
    P[1] = contents(P, page, 1)
    return 'keynotes-brochure', 'Keynotes: The Care Leaders Learning', P

def talk_page(page, i, talk, n, sec='talks'):
    """A keynote page with more to look at: numbered hexagon, large pictogram, the outcomes, and who it is for."""
    t, tag, who, aud, para, outs, pc = talk
    cols = ['fuchsia', 'purple', 'teal', 'indigo', 'midgreen', 'brightpurple', 'navy']
    beds = ['light', 'bed-blue', 'bed-green', 'bed-purple']
    col = cols[i % 7]
    lis = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in outs)
    extra = ''
    if t == 'Lived Experience Leadership':
        five = [('Storytelling', 'Sharing their experience safely, on their own terms.'), ('Skills', 'Recognising and building the skills their experience has given them.'),
                ('Strategies', 'Helping shape plans, services and decisions.'), ('Scaling', 'Leading pieces of work, such as training staff or running projects.'),
                ('Succession', 'Mentoring and bringing the next young people through.')]
        hc = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']
        extra = '<ol class="fives">' + ''.join(f'<li><span class="hx" style="background-image:url({K}/strips/hex-{hc[k]}.png)">{k + 1}</span><b>{e(a)}.</b> {e(b)}</li>' for k, (a, b) in enumerate(five)) + '</ol>'
    flag = strip('Flagship talk', 'ribbon', 'apple', 'mini') if i == 0 else ''
    tiles = [(19, 'navy', 'In person', 'or live online'), (5, 'purple', '45 to 90 minutes', 'keynote or workshop'), (20, 'teal', 'Workbook, recording', 'and course included')]
    glance = '' if extra else '<div class="tkg">' + ''.join(f'<div class="tkt" style="{box(c)}">{picto(pp, "pic sm")}<div><b>{e(x)}</b><span>{e(y)}</span></div></div>' for pp, c, x, y in tiles) + '</div>'
    return page(f'''<span class="tkbig" style="background-image:url({K}/strips/hex-{col}.png)"></span>
      <div class="tk2{' five' if extra else ''}{' lt' if len(t) > 22 else ''}"><div class="tkl">
        <div class="tkh"><span class="tkn" style="background-image:url({K}/strips/hex-{col}.png)">{i + 1}</span>
          <div><span class="tko">Keynote {i + 1} of {len(TALKS)}</span>{flag}</div></div>
        <h2>{e(t)}</h2><p class="knt">{e(tag)}</p><p class="knp">{e(para)}</p>{extra}{glance}</div>
      <div class="tkr"><div class="tkp" style="{box(col)}">{picto(pc, 'pic tkpi')}</div>
        <div class="kno" style="{box('midnight')}"><h3>By the end, delegates will</h3><ul>{lis}</ul></div></div></div>
      <div class="tkw" style="background-image:url({K}/strips/arrowlong-{'apple' if col != 'midgreen' else 'teal'}.png)"><b>Best for</b>{e(who)}</div>''',
      beds[i % 4] + ' tkp2', sec, n, t)

def keynotes2():
    """The keynote brochure with sections, section openers and livelier keynote pages (option with sections)."""
    items = [('talks', 'The keynotes'), ('get', 'What you get'), ('luke', 'About Luke'), ('fees', 'Fees'), ('book', 'Book')]
    page = make_page(items, 'Keynotes with Luke Rodgers BEM · The Care Leaders Learning')
    P = [cover('Keynotes with Luke Rodgers BEM', 'Keynotes and conference workshops', 'From care leaver. <span class="apple">To care leader.</span>',
               'Story-led keynotes for conferences, staff days and boards: stories of care from Luke\'s lived experience, the theory behind them and tools your audience can use the next day.',
               opt(hires('block-2.webp'), 960),
               [('In person or online', 'keynotes of up to 90 minutes', 'or a conference workshop', True),
                (str(len(TALKS)), 'keynotes', 'or one built for your audience', False), ('4,000+', 'delegates since 2024', 'from 30 to 400 in a room', False)], long=True), '']
    num = lambda: len(P) + 1
    first = num() + 2  # after the opener and the audience page
    lis = ''.join(f'<li><span class="hx" style="background-image:url({K}/strips/hex-{["fuchsia", "purple", "teal", "indigo", "midgreen", "brightpurple", "navy"][k % 7]}.png)">{k + 1}</span>{e(t)}<span class="fpg">page {first + k}</span></li>'
                  for k, (t, *_r) in enumerate(TALKS))
    P.append(divider(page, 1, num(), 'The keynotes', 'Seven talks, each built for a different audience. Or tell us yours and we shape one around them.',
                     [], 'tonal-midnight', f'<div class="fnd kfd"><p class="fnt">The {len(TALKS)} keynotes</p><ol>{lis}</ol></div>'))
    rows = ''.join(f'<li><span class="mxa">{e(aud)}</span><img src="{K}/chev.png" alt=""><b>{e(t)}</b></li>' for t, _, _, aud, _, _, _ in TALKS)
    P.append(page(f'''<h2>Find the keynote for your audience</h2>
      <div class="mx"><ol class="mxl">{rows}</ol>
        <div class="mxc" style="{box('navy')}">{picto(13)}<h3>Don&#8217;t see your audience here?</h3>
          <p>Tell us your conference theme, who&#8217;s coming and what you want them to leave with, and we&#8217;ll shape a custom keynote around them. It follows the same approach as every other talk, with the recording, the on-demand course and the workbook included.</p></div></div>''',
      'bed-purple', 'talks', num(), 'Find the keynote for your audience'))
    for i, tk in enumerate(TALKS):
        P.append(talk_page(page, i, tk, num()))
    P.append(divider(page, 2, num(), 'What you get', 'Everything that comes with a booking, and how every keynote is built.',
                     ['More than a keynote', 'The keynote course on any device', 'Story, theory and action'], 'tonal-midnight', img=opt(K / 'tcll2026' / 'image-block-04.png', 620)))
    four = [(9, 'Before the day', 'A planning call', ['A 30-minute planning call', 'The keynote shaped around your audience and theme', 'A title and blurb for your programme, plus Luke\'s photo and bio']),
            (18, 'On the day', 'The keynote', ['A keynote of up to 90 minutes', 'Time for questions and discussion', 'The slides, to share with delegates']),
            (20, 'On the day', 'A workbook for every delegate', ['Print-ready or digital', 'Activities for individuals and teams', 'Theirs to keep']),
            (8, 'After the day', 'The recording and course', ['The full keynote recorded', 'An on-demand course on The Care Leaders Online', '12 months\' access for every delegate'])]
    g = ''.join(f'<div class="gi g4" style="{box("indigo")}">{picto(p)}<b>{e(t)}</b>{strip(w, "angled", "apple", "gs2")}<ul>{"".join(f"<li>{e(x)}</li>" for x in pts)}</ul></div>' for p, w, t, pts in four)
    P.append(page(f'''<h2>More than a keynote</h2><p class="sub">Every booking, in person or online, comes with the same four things.</p>
      <div class="gis g4s">{g}</div>''', 'light', 'get', num(), 'More than a keynote: what every booking includes'))
    P.append(showcase_page(page, 'get', num(), 'tools-for-schools', 'The keynote course on any device',
                           ['The course home on a laptop', 'Every tool works on a phone', 'The workbook, theirs to keep'],
                           'Free for 12 months: the recording and the course', None,
                           'Shown: Tools for Schools. Every keynote has its own online course and workbook.'))
    P.append(sta_page(page, 'get', num(), 'Stories of care from Luke\'s lived experience, the theory behind them, and tools your audience uses the next day.'))
    P.append(divider(page, 3, num(), 'About Luke', 'Who gives the keynote, and why organisations book him.',
                     ['Your speaker: Luke Rodgers BEM', 'Why book Luke'], 'tonal-midnight', img=opt(K / 'tcll2026' / 'image-block-05.png', 620)))
    P.append(luke_page(page, 'luke', num(), 'luke-lga-podium.jpg', 'Luke gives every keynote himself, in person or live online, and stays for questions.',
                       ('You demand bravery and humanity in equal measure.', 'Maggie Atkinson, former Children\'s Commissioner for England'), 'Your speaker'))
    P.append(why_page(page, 'luke', num(), 'Keynotes from someone who has lived in care and has led services.').replace('Why choose The Care Leaders Learning', 'Why book Luke'))
    P.append(divider(page, 4, num(), 'Fees and booking', 'What it costs, and how to book.',
                     ['Fees for every keynote', 'Book Luke in 4 steps'], 'tonal-midnight', f'<div class="dvpx">{picto(19)}{picto(18)}{picto(16)}</div>'))
    fmts = [{'label': 'In person', 'length': 'Keynote', 'time': 'Up to 90 minutes, at your event', 'fee': '£4,950', 'fee_note': '+ VAT + travel expenses',
             'points': ['A planning call before the day', 'A workbook for every delegate', 'The recording and course for 12 months']},
            {'label': 'Live online', 'length': 'Keynote', 'time': 'Up to 90 minutes, on Teams or Zoom', 'fee': '£2,490', 'fee_note': '+ VAT',
             'points': ['A planning call before the day', 'Questions in the chat and live Q&A', 'The recording and course for 12 months']}]
    P.append(fees_page(page, 'fees', num(), 'Fees for every keynote', fmts,
                       'Keynotes and conference workshops are contracted and invoiced by Luke Speaks Ltd, powered by The Care Leaders. If Luke is free, we hold your date for 14 days.',
                       [opt(hires('block-6.webp'), 500), opt(hires('block-3.webp'), 500)]))
    P.append(book_page(page, 'book', 'Book Luke in 4 steps',
                       [('Tell us about your event', 'The date, your audience and the talk'), ('Get availability and a fee', 'We hold the date for 14 days'),
                        ('Confirm by email', 'And send a purchase order if you use them'), ('Before the day', 'A planning call and a checklist')],
                       f'{AWARDS_LINE} · Luke Speaks Ltd, company number 15452230 · thecareleaders.com/keynotes'))
    P[1] = contents(P, page, 1)
    return 'keynotes-brochure-sections', 'Keynotes: The Care Leaders Learning', P

# ---------------------------------------------------------------- keynotes, Story Theory Action pages
# From the keynote overviews in Luke Speaks > General > Bio Info > Luke Speaks Keynotes (and the keynote overview documents).
STA_TALKS = {
    'Living a Careless Life': (
        "Luke went into care at 10. He shares stories from his own time in care that are moving and often funny, and that show the moments when one adult and one relationship changed what happened next.",
        "Two ideas explain how systems shape the way a child is seen. The first is how profiles and referrals are written: too often they describe a child by what went wrong, and placements and school places are lost because of it. The second is the Two Timetables, where school and social care clash around the child, from reviews held in school to how information is shared.",
        "Your audience leaves knowing how to talk with children, read the message in a behaviour and spot the triggers that can take a child back to trauma, and how much one relationship can do."),
    'Just Say Yes': (
        "Luke shares stories from his time in foster care: what it felt like to be judged by a profile, to be misunderstood and then believed in, and the moments when a foster carer made a life-changing difference. They show how relationships, not labels, create safety.",
        "Attachment and how early relationships shape behaviour, the impact of trauma on brain development and emotional regulation, and the link between behaviour and survival. It explains why traditional approaches to discipline may not work for children in care.",
        "Simple tools carers can use straight away: reframing behaviour through a trauma-informed lens, ways of talking that build trust and calm conflict, making home feel safe and predictable, and responding to hard moments with empathy, not punishment."),
    'The Power of the Profile': (
        "Luke shares what it was like to read his own file: to be introduced through incident logs, and turned down because of paperwork that did not show who he was.",
        "Trauma-informed storytelling, attachment and the psychology of language. A profile is often built from inherited court reports, incident logs and assessments, so the child is described by what went wrong. This explains how those words shape what a school, carer or panel expects before they meet the child.",
        "Practical ways to write profiles that are honest, balanced and hopeful, reframe behaviour so it reduces fear, and help other professionals say yes through the way information is shared. It also recognises the weight social workers carry when the answer is no."),
    'Tools for Schools': (
        "Luke shares his own school experiences: what it felt like to be labelled and excluded, and the difference it made when a teacher believed in him. His story helps staff understand the inner world of a child in care.",
        "Trauma, attachment and child development made relevant to the classroom, so staff understand the why behind the behaviour they see. Most teacher training does not cover trauma or children in care, yet schools are expected to be a critical support.",
        "Tools to respond to trauma-based behaviour without escalating it, build safe learning environments where every child can thrive, and talk with children in care in ways that build trust, not fear."),
    'Lived Experience Leadership': (
        "Luke shares his own journey from telling his story to leading national work, and what helped at each stage.",
        None,
        "Leaders map where the young people in their service are on the five stages, match them to roles in service delivery and improvement that fit their stage, and plan how each young person moves on, and who leads next."),
    'From Care Leaver to Care Leader': (
        "Luke shares his journey from growing up in care to becoming a national leader, speaker and founder. His story shows what is possible for every care-experienced young person.",
        "How the care system shapes identity, how trauma shapes behaviour, and how getting through hard times builds real leadership skills: adapting, solving problems, reading people and keeping going. Young people are often described by other people\'s words in case notes and plans. This talk helps them tell their own.",
        "Young people reframe their experience as a strength, recognise the skills they already have, and see themselves as people who can lead change in their own lives and beyond."),
    'Be the First Yes': (
        "Luke shares his own move from care into work, and how one opportunity changed his future.",
        "The barriers care leavers face in getting and keeping work, often without family networks, references or a safety net, and the behavioural science behind stigma, opportunity and belonging. Care leavers are not asking for special treatment. They are asking for a chance.",
        "Clear steps to make recruitment and induction care-aware, offer mentoring and onboarding that helps people stay, and build teams where care-experienced staff can grow."),
}
FIVE_S = [('Storytelling', 'sharing their experience safely, on their own terms'), ('Skills', 'recognising the skills their experience has given them'),
          ('Strategies', 'helping shape plans, services and decisions'), ('Scaling', 'leading pieces of work, such as training staff'),
          ('Succession', 'mentoring and bringing the next young people through')]
# One Learning image per keynote, each used once in the brochure
TALK_IMG = {'Living a Careless Life': 'image-block-06.png', 'Just Say Yes': 'image-block-02.png', 'The Power of the Profile': 'image-block-03.png',
            'Tools for Schools': 'image-block-01.png', 'Lived Experience Leadership': 'image-block-04.png',
            'From Care Leaver to Care Leader': 'image-block-05.png', 'Be the First Yes': 'woman-laptop.png'}

def sta_talk_page(page, i, talk, n, thm=None):
    thm = thm or {}
    """Keynote page: number, title, an overview (Story, Theory, Action order), the outcomes, who it is for, and an image."""
    t, tag, who, aud, para, outs, pc = talk
    cols = ['fuchsia', 'purple', 'teal', 'indigo', 'midgreen', 'brightpurple', 'navy']
    beds = ['light', 'bed-blue', 'bed-green', 'bed-purple']
    col = cols[i % 7]
    st, th, ac = STA_TALKS[t]
    if th is None:
        hc = ['purple', 'teal', 'fuchsia', 'indigo', 'midgreen']
        th = ('<span>The Five S framework, five stages from first telling a story to leading the work:</span><ol class="fives s5">' +
              ''.join(f'<li><span class="hx" style="background-image:url({K}/strips/hex-{hc[k]}.png)">{k + 1}</span><b>{e(a)}</b>&nbsp;{e(b)}</li>' for k, (a, b) in enumerate(FIVE_S)) + '</ol>')
    else:
        th = e(th)
    # Overview written in the Story, Theory, Action order, as plain paragraphs
    ov = f'<p>{e(st)}</p>' + (f'<div class="ovf">{th}</div>' if th.startswith('<span>') else f'<p>{th}</p>') + f'<p>{e(ac)}</p>'
    lis = ''.join(f'<li><img src="{K}/tick.png" alt="">{e(x)}</li>' for x in outs)
    src = thm['talk_img'][t] if 'talk_img' in thm else (K / TALK_IMG[t] if TALK_IMG[t].startswith('woman') else K / 'tcll2026' / TALK_IMG[t])
    flag = strip('Flagship talk', 'ribbon', 'apple', 'mini') if i == 0 else ''
    return page(f'''<div class="k3{' k3f' if t == 'Lived Experience Leadership' else ''}{' k3lt' if len(t) > 26 else ''}"><div class="k3l">
        <div class="tkh"><span class="tkn" style="background-image:url({K}/strips/hex-{col}.png)">{i + 1}</span>
          <div><span class="tko">Keynote {i + 1} of {len(TALKS)}</span>{flag}</div></div>
        <h2>{e(t)}</h2><p class="knt">{e(tag)}</p><div class="ov"><h3>Overview</h3>{ov}</div></div>
      <div class="k3r"><img class="k3i" src="{opt(src, 640)}" alt="">
        <div class="kno" style="{box('midnight')}"><h3>By the end, delegates will</h3><ul>{lis}</ul></div>
        <div class="kbf" style="{box('teal')}"><h3>Best for</h3><p>{e(who)}</p></div></div></div>''',
      beds[i % 4] + ' tkp2', 'talks', n, t)

def keynotes3(theme=None):
    """Keynote brochure with sections, and Story, Theory, Action keynote pages each with a Learning image.
    Photos of Luke on the cover and fees pages, so each Learning image appears once, on its keynote."""
    B = A / 'img/brand'
    th = theme or {}
    dx = lambda k, default: th.get('div', {}).get(k, default)
    items = [('talks', 'The keynotes'), ('get', 'What you get'), ('luke', 'About Luke'), ('fees', 'Fees'), ('book', 'Book')]
    page = make_page(items, 'Keynotes with Luke Rodgers BEM · The Care Leaders Learning')
    P = [cover('Keynotes with Luke Rodgers BEM', 'Keynotes and conference workshops', 'From care leaver. <span class="apple">To care leader.</span>',
               'Story-led keynotes for conferences, staff days and boards: stories of care from Luke\'s lived experience, the theory behind them and tools your audience can use the next day.',
               opt(B / 'luke-lga-wide.jpg', 960),
               [('In person or online', 'keynotes of up to 90 minutes', 'or a conference workshop', True),
                (str(len(TALKS)), 'keynotes', 'or one built for your audience', False), ('4,000+', 'delegates since 2024', 'from 30 to 400 in a room', False)], long=True).replace('class="covimg"', 'class="covimg covph"'), '']
    num = lambda: len(P) + 1
    first = num() + 2
    hx = ["fuchsia", "purple", "teal", "indigo", "midgreen", "brightpurple", "navy"]
    lis = ''.join(f'<li><span class="hx" style="background-image:url({K}/strips/hex-{hx[k % 7]}.png)">{k + 1}</span>{e(t)}<span class="fpg">page {first + k}</span></li>'
                  for k, (t, *_r) in enumerate(TALKS))
    P.append(divider(page, 1, num(), 'The keynotes', 'Seven talks, each built for a different audience. Or tell us yours and we shape one around them.',
                     [], 'tonal-midnight', f'<div class="fnd kfd"><p class="fnt">The {len(TALKS)} keynotes</p><ol>{lis}</ol></div>'))
    rows = ''.join(f'<li><span class="mxa">{e(aud)}</span><img src="{K}/chev.png" alt=""><b>{e(t)}</b></li>' for t, _, _, aud, _, _, _ in TALKS)
    P.append(page(f'''<h2>Find the keynote for your audience</h2>
      <div class="mx"><ol class="mxl">{rows}</ol>
        <div class="mxc" style="{box('navy')}">{picto(13)}<h3>Don&#8217;t see your audience here?</h3>
          <p>Tell us your conference theme, who&#8217;s coming and what you want them to leave with, and we&#8217;ll shape a custom keynote around them. It follows the same approach as every other talk, with the recording, the on-demand course and the workbook included.</p></div></div>''',
      'bed-purple', 'talks', num(), 'Find the keynote for your audience'))
    for i, tk in enumerate(TALKS):
        P.append(sta_talk_page(page, i, tk, num(), th))
    P.append(divider(page, 2, num(), 'What you get', 'Everything that comes with a booking, and how every keynote is built.',
                     ['More than a keynote', 'The keynote course on any device', 'Story, theory and action'], 'tonal-midnight', dx(2, f'<div class="dvpx">{picto(9)}{picto(20)}{picto(8)}</div>')))
    four = [(9, 'Before the day', 'A planning call', ['A 30-minute planning call', 'The keynote shaped around your audience and theme', 'A title and blurb for your programme, plus Luke\'s photo and bio']),
            (18, 'On the day', 'The keynote', ['A keynote of up to 90 minutes', 'Time for questions and discussion', 'The slides, to share with delegates']),
            (20, 'On the day', 'A workbook for every delegate', ['Print-ready or digital', 'Activities for individuals and teams', 'Theirs to keep']),
            (8, 'After the day', 'The recording and course', ['The full keynote recorded', 'An on-demand course on The Care Leaders Online', '12 months\' access for every delegate'])]
    g = ''.join(f'<div class="gi g4" style="{box("indigo")}">{picto(p)}<b>{e(t)}</b>{strip(w, "angled", "apple", "gs2")}<ul>{"".join(f"<li>{e(x)}</li>" for x in pts)}</ul></div>' for p, w, t, pts in four)
    P.append(page(f'''<h2>More than a keynote</h2><p class="sub">Every booking, in person or online, comes with the same four things.</p>
      <div class="gis g4s">{g}</div>''', 'light', 'get', num(), 'More than a keynote: what every booking includes'))
    P.append(showcase_page(page, 'get', num(), 'tools-for-schools', 'The keynote course on any device',
                           ['The course home on a laptop', 'Every tool works on a phone', 'The workbook, theirs to keep'],
                           'Free for 12 months: the recording and the course', None,
                           'Shown: Tools for Schools. Every keynote has its own online course and workbook.'))
    P.append(sta_page(page, 'get', num(), 'Stories of care from Luke\'s lived experience, the theory behind them, and tools your audience uses the next day.'))
    P.append(divider(page, 3, num(), 'About Luke', 'Who gives the keynote, and why organisations book him.',
                     ['Your speaker: Luke Rodgers BEM', 'Why book Luke'], 'tonal-midnight', dx(3, f'<div class="dvpx">{picto(13)}{picto(1)}{picto(14)}</div>')))
    P.append(luke_page(page, 'luke', num(), 'luke-lga-podium.jpg', 'Luke gives every keynote himself, in person or live online, and stays for questions.',
                       ('You demand bravery and humanity in equal measure.', 'Maggie Atkinson, former Children\'s Commissioner for England'), 'Your speaker'))
    P.append(why_page(page, 'luke', num(), 'Keynotes from someone who has lived in care and has led services.').replace('Why choose The Care Leaders Learning', 'Why book Luke'))
    P.append(divider(page, 4, num(), 'Fees and booking', 'What it costs, and how to book.',
                     ['Fees for every keynote', 'Book Luke in 4 steps'], 'tonal-midnight', dx(4, f'<div class="dvpx">{picto(19)}{picto(18)}{picto(16)}</div>')))
    fmts = [{'label': 'In person', 'length': 'Keynote', 'time': 'Up to 90 minutes, at your event', 'fee': '£4,950', 'fee_note': '+ VAT + travel expenses',
             'points': ['A planning call before the day', 'A workbook for every delegate', 'The recording and course for 12 months']},
            {'label': 'Live online', 'length': 'Keynote', 'time': 'Up to 90 minutes, on Teams or Zoom', 'fee': '£2,490', 'fee_note': '+ VAT',
             'points': ['A planning call before the day', 'Questions in the chat and live Q&A', 'The recording and course for 12 months']}]
    P.append(fees_page(page, 'fees', num(), 'Fees for every keynote', fmts,
                       'Keynotes and conference workshops are contracted and invoiced by Luke Speaks Ltd, powered by The Care Leaders. If Luke is free, we hold your date for 14 days.',
                       [opt(B / 'luke-stage.jpg', 500), opt(B / 'luke-room.jpg', 500)]).replace('class="fimg"', 'class="fimg lsph"'))
    P.append(book_page(page, 'book', 'Book Luke in 4 steps',
                       [('Tell us about your event', 'The date, your audience and the talk'), ('Get availability and a fee', 'We hold the date for 14 days'),
                        ('Confirm by email', 'And send a purchase order if you use them'), ('Before the day', 'A planning call and a checklist')],
                       f'{AWARDS_LINE} · Luke Speaks Ltd, company number 15452230 · thecareleaders.com/keynotes', n=num()))
    P[1] = contents(P, page, 1)
    return 'keynotes-brochure-sta', 'Keynotes: Luke Speaks', P

EXTRA_CSS = '''
.cover h1.long{font-size:64px}
.ccs{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.catp h2{font-size:38px;margin-bottom:16px}
.cc{background-size:100% 100%;padding:20px 22px 20px 26px;position:relative;min-height:220px}
.ccb{position:absolute;left:0;top:14px;bottom:14px;width:8px;background-size:100% 100%}
.cc h3{font-size:24px;line-height:1.05;margin-bottom:6px}
.cch{font:400 15px CS;color:#7c05ca;margin-bottom:8px}
.cci{font-size:17px;line-height:1.4;margin-bottom:10px}
.ccw{font-size:13px;line-height:1.35;color:#312b6c}.ccw b{font-family:CS}
.ccu{position:absolute;left:26px;bottom:14px;font:400 12px CS;color:#008196}
.two{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.tw{background-size:100% 100%;color:#fff;padding:30px 34px 34px;min-height:330px}
.tw .pic{display:block;margin-bottom:16px}.tw h3{font-size:34px;line-height:1.05;margin:12px 0 12px}.tw p{font-size:19px;line-height:1.5}
.tln.dkl{color:#0e2545;margin-top:26px;font-size:19px}
.mx{display:grid;grid-template-columns:1.3fr 1fr;gap:30px;align-items:start}
.mxl li{display:grid;grid-template-columns:300px 26px 1fr;align-items:center;gap:12px;background:#fff;margin-bottom:10px;padding:13px 18px}
.mxl li img{width:22px}.mxa{font:400 16px CS;color:#5f3c90}.mxl b{font-family:CB;font-size:22px}
.mxc{background-size:100% 100%;color:#fff;padding:30px 30px 34px}.mxc h3{font-size:30px;line-height:1.05;margin:14px 0 12px}.mxc p{font-size:18px;line-height:1.5}
.kn{display:grid;grid-template-columns:1.15fr 1fr;gap:40px;align-items:start}
.knf{margin-bottom:16px}.kn h2{font-size:52px;margin-bottom:8px}
.knt{font:400 24px/1.25 CS;color:#7c05ca;margin-bottom:14px}
.knp{font-size:18px;line-height:1.55;margin-top:12px}
.kn.five .knp{font-size:16px;line-height:1.45}.kn.five h2{font-size:46px}
.kno{background-size:100% 100%;color:#fff;padding:26px 30px 28px}.kno h3{font-size:26px;margin:12px 0 14px}
.kno li{display:flex;gap:12px;align-items:flex-start;font:400 17px/1.35 CS;margin-bottom:12px}.kno li img{width:24px;margin-top:2px}
.knf3{margin-top:18px}.knf3 p{font-size:15px;line-height:1.45;margin-bottom:6px}.knf3 b{font-family:CS;color:#5f3c90}
.fives{margin-top:14px}.fives li{display:flex;align-items:center;gap:10px;font-size:14px;line-height:1.3;margin-bottom:6px}
.fives .hx{flex:0 0 30px;height:30px;font-size:14px}
.g4s{grid-template-columns:repeat(4,1fr)}.gi.g4{min-height:420px}.gi.g4 ul{margin-top:10px}.gi.g4 li{font-size:16px;line-height:1.4;margin-bottom:8px;padding-left:14px;border-left:3px solid #acc90b}
.sts.s4{grid-template-columns:repeat(4,1fr)}
.tcg{display:grid;grid-template-columns:1fr 1fr;gap:18px 22px;margin-top:4px}
.tcs{background-size:100% 100%;padding:18px 24px 20px}
.tch{display:flex;align-items:center;gap:14px;padding-bottom:10px;margin-bottom:8px;border-bottom:2px solid #e3dcef}
.tch h3{font-size:26px;flex:1}.tcp{font:400 14px CS;color:#7c05ca}
.tcs li{display:flex;gap:14px;font:400 17px/1.3 CS;padding:4px 0;color:#241b40}.tcn{width:58px;text-align:center;color:#008196;font-family:CB}
.divp{padding-top:70px}.dvimg{position:absolute;right:60px;top:150px;max-width:560px;max-height:440px}
.dvpx{position:absolute;right:90px;top:200px;display:flex;gap:30px}.dvpx .pic{width:150px;height:150px}.dvl{position:absolute;left:60px;top:120px;width:620px}
.dvh{font-size:84px;line-height:1;margin:22px 0 18px;color:#fff}.dvp{font:400 24px/1.35 CS;margin-bottom:26px;color:#fff}
.dvi li{display:flex;gap:14px;align-items:center;font:400 21px CS;margin-bottom:12px}.dvi img{width:22px}
.dvl.dvn{width:380px}.dvl.dvn .dvh{font-size:64px}
.fnds{position:absolute;left:470px;right:50px;top:110px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.fnt{font:400 18px/1.2 CB;color:#acc90b;margin-bottom:12px;min-height:44px}.fnt span{display:block;font:400 13px CS;color:#fff;margin-top:4px}
.fnd li{display:flex;gap:10px;align-items:center;font:400 16px/1.2 CS;margin-bottom:12px}.fnd .hx{flex:0 0 40px;width:40px;height:24px;font-size:13px}
.cct{display:flex;gap:12px;align-items:center;margin-bottom:10px}.cct h3{margin:0}.cct .hx{flex:0 0 46px}
.catp.dbl .cc{min-height:0}.ccg{font-size:28px;margin:0 0 10px}.catp.dbl .ccs+.ccg{margin-top:12px}.catp.dbl .ccf{margin-top:10px}.catp.dbl .cci{font-size:16px}.catp.dbl .cc h3{font-size:21px}.catp.dbl .cc{padding-top:16px;padding-bottom:14px}.catp.dbl .cct{margin-bottom:8px}.fnd ol+.fnt{margin-top:18px}
.ccf{margin-top:16px;font:400 15px CS;color:#312b6c}
.tkp2{padding-top:88px}
.tkbig{position:absolute;right:-90px;bottom:-70px;width:360px;height:204px;background-size:100% 100%}
.tk2{display:grid;grid-template-columns:1.2fr 1fr;gap:36px;align-items:start;position:relative}
.tkh{display:flex;align-items:center;gap:16px;margin-bottom:10px}
.tkn{width:110px;height:62px;flex:0 0 110px;background-size:100% 100%;color:#fff;font:400 30px CB;display:flex;align-items:center;justify-content:center}
.tko{display:block;font:400 16px CS;color:#5f3c90;margin-bottom:4px}
.tk2 h2{font-size:62px;line-height:1;margin-bottom:10px}.tk2 .knt{font-size:26px}.tk2.five h2,.tk2.lt h2{font-size:44px}
.tk2 .knp{font-size:18px;line-height:1.55;margin-top:10px}.tk2.five .knp{font-size:15.5px;line-height:1.45}
.tkr{position:relative;padding-top:56px}
.tkp{position:absolute;right:18px;top:0;width:112px;height:112px;background-size:100% 100%;display:flex;align-items:center;justify-content:center;z-index:2}
.pic.tkpi{width:84px;height:84px}
.tkr .kno{padding-top:30px;padding-right:140px}.tkr .kno h3{margin-top:0}
.tkr .kno ul{margin-right:-110px}
.tkw{position:absolute;left:60px;bottom:52px;max-width:860px;background-size:100% 100%;padding:12px 70px 13px 18px;font:400 17px/1.3 CS;color:#241b40}
.tkw b{font-family:CB;margin-right:12px}
.tkg{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}
.tkt{background-size:100% 100%;color:#fff;padding:14px 14px 16px;display:flex;gap:10px;align-items:center}.tkt b{display:block;font:400 16px/1.15 CB}.tkt span{font:400 13px CS}
.kfd{position:absolute;left:640px;top:130px;width:560px}.kfd li{font-size:20px;margin-bottom:16px}.kfd .hx{flex:0 0 52px;width:52px;height:30px;font-size:16px}
.kfd .fpg{margin-left:auto;font:400 14px CS;color:#acc90b}
.k3{display:grid;grid-template-columns:1.25fr 1fr;gap:34px;align-items:start;position:relative}
.k3 h2{font-size:50px;line-height:1;margin-bottom:6px}.k3 .knt{font-size:22px;margin-bottom:12px}
.sta3 li{display:flex;gap:14px;align-items:flex-start;margin-bottom:12px}.stic{width:46px;height:46px;flex:0 0 46px;object-fit:contain}
.sta3 b{font:400 19px CB;display:block;margin-bottom:2px}.sta3 p{font-size:15px;line-height:1.42}
.k3f h2{font-size:42px}.k3lt h2{font-size:38px;white-space:nowrap}.k3f .knt{font-size:18px;margin-bottom:8px}.k3f .sta3 li{margin-bottom:6px}.k3f .stic{width:38px;height:38px;flex-basis:38px}.k3f .sta3 p{font-size:14px;line-height:1.35}
.fives.s5{margin-top:6px}.fives.s5 li{margin-bottom:3px;font-size:13px;gap:8px}.fives.s5 .hx{flex:0 0 26px;width:26px;height:22px;font-size:12px}.fives.s5 b{font:400 13px CS;display:inline;margin:0}
.k3r{display:flex;flex-direction:column;gap:12px;margin-top:-30px}
.k3i{height:180px;width:auto;max-width:100%;align-self:center;object-fit:contain}
.k3r .kno{padding:20px 24px 16px}.k3r .kno h3{font-size:22px;margin:0 0 10px}.k3r .kno li{font-size:15px;margin-bottom:8px}
.fimg.lsph{top:18px;height:120px;width:170px;max-width:170px;object-fit:cover;clip-path:polygon(6% 0,100% 0,100% 100%,0 94%)}
.covph{object-fit:cover;clip-path:polygon(10% 0,100% 0,100% 100%,0 96%)}
.legal.lgn{bottom:44px}
.ov h3{font-size:22px;margin:4px 0 8px}.k3 .ov p{font-size:18px;line-height:1.5;margin-bottom:12px}
.ovf{font-size:16px;line-height:1.45;margin-bottom:12px}.ovf .fives.s5 li{font-size:14px}.k3.k3f .ov p{font-size:15.5px;line-height:1.42;margin-bottom:9px}
.k3r .kbf{padding:16px 24px 18px;color:#fff}.kbf h3{font-size:20px;margin-bottom:4px;color:#fff}.kbf p{font:400 15px/1.4 CS}
.shnote{position:absolute;left:930px;top:612px;width:300px;font:400 13px/1.35 CS;color:#312b6c}
'''

def render(slug, title, P, out):
    css = (HERE / 'brochure.css').read_text().replace('{ACC}', '#cf0f55').replace('{A}', str(A)).replace('{K}', str(K)) + EXTRA_CSS
    h = out / f'{slug}.html'
    h.write_text(f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{e(title)}</title><style>{css}</style></head><body>{"".join(P)}</body></html>')
    pdf = out / f'{slug}.pdf'
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{h}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.pdf({{path:'{pdf}',width:'1280px',height:'720px',printBackground:true,margin:{{top:0,right:0,bottom:0,left:0}}}});
await b.close()}})();"""
    subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
    print(pdf)

if __name__ == '__main__':
    which = sys.argv[1]; out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else A / 'docs/brochures'
    render(*{'training': training, 'keynotes': keynotes, 'keynotes2': keynotes2, 'keynotes3': keynotes3}[which](), out)
