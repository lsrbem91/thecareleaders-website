# Website audit: UX, design and SEO

Date: 11 October 2026. Site: thecareleaders.com interim build (47 pages). Audit run with axe-core 4.10 (WCAG 2.0/2.1/2.2 A and AA plus best practice), a link and anchor checker, computed-style checks at 1280px and 390px, and hand review.

## 1. UX and compliance checklist

Sources: WCAG 2.2 AA checklist (BrowserStack), UK company website requirements (1st Formations), PECR and UK GDPR cookie guidance.

Navigation and structure
- One primary menu, the same on every page, eight items or fewer. Current page marked.
- Every page reachable in three clicks from the home page. Every page linked from at least one other page.
- Breadcrumbs on every inner page.
- Skip link to main content.
- Logo links home. Footer repeats the menu, contact details and legal lines.
- No dead links, no links to redirect pages, no anchors that do not exist.
- Pages open at the top. Same-page anchors scroll to the section.

Accessibility (WCAG 2.2 AA)
- Text contrast at least 4.5:1, large text (24px, or 18.5px bold) at least 3:1, controls and focus rings at least 3:1.
- Interactive targets at least 24 by 24 CSS pixels.
- Visible focus style on every link, button and field, not hidden by sticky headers.
- One h1 per page. Heading levels never skip.
- Alt text on informative images, alt="" on decorative ones.
- Every form field labelled. Errors and status messages announced.
- Everything works by keyboard, including tabs, explorers and the mobile menu.
- No content flashes more than three times a second. Motion respects reduced-motion settings.
- Page language set. Viewport meta set. Text can be zoomed to 200 percent without horizontal scrolling.

Legal (UK)
- Registered company name, number, registered office and jurisdiction on every page (footer).
- Email and a non-electronic contact (phone or address).
- VAT number if VAT registered.
- Privacy notice: what is collected, why, lawful basis, retention, third parties, rights, how to complain.
- Cookie notice and consent before any non-essential cookie. Strictly necessary cookies need no consent.
- Accessibility statement (good practice under the Equality Act 2010, not mandated for private companies).

Functionality
- Every button leads somewhere real. No href="#".
- Forms submit and confirm. Downloads deliver a file or say clearly what happens next.
- Mobile menu opens and closes. Nothing overflows the viewport at 390px.
- No JavaScript errors in the console on any page.

## 2. Design checklist

Sources: web typography guidance (madegooddesigns.com), WCAG contrast rules, the TCL, Care to Work and Academy brand kits.

- Body text at least 16px on desktop and mobile; nothing a reader must read below 15px.
- Line height 1.4 to 1.6 for body, 1.1 to 1.3 for headings.
- Line length 45 to 75 characters, never more than about 95.
- One typeface family (Crossten), two or three weights. Weight is the family: no faux bold or italic.
- Heading scale on a fixed ratio; headings shrink on narrow screens.
- Consistent spacing scale between sections (48px desktop, less on mobile), and tighter spacing between a heading and its first paragraph than between paragraphs.
- Every colour pair on the site passes contrast (see section 1).
- Brand shapes only: TCL hand-cut marks on TCL pages, straps and passes on Care to Work, fans and page bars on the Academy. No stock shapes, circles or mazes in thumbnails.
- One visual device per block, top right, never as scattered decoration behind text.
- Thumbnails: solid brand bed, project name loud, client logo top right, same format throughout.
- Buttons: one primary and one secondary style per theme, minimum 44px tall.
- Cards in a grid are the same height and width.
- Images have intrinsic width and height so the page does not jump while loading.

## 3. SEO checklist

Sources: technical SEO checklist 2026 (nogood.io), Google Search Essentials.

Technical
- One title per page, under 65 characters, the search phrase first and the brand last.
- One meta description per page, 70 to 160 characters, written as the answer to the search.
- One h1 per page containing the page's main phrase. Headings in order.
- Canonical URL on every page. Open Graph title, description, image and URL.
- JSON-LD: Organization and Person on the home and About pages, WebPage or Article elsewhere, BreadcrumbList on inner pages.
- XML sitemap and robots.txt, with thank-you and utility pages excluded.
- Images: descriptive file names where possible, alt text, lazy loading below the fold, width and height set, compressed.
- Core Web Vitals: LCP under 2.5s, INP under 200ms, CLS under 0.1. Fonts loaded with font-display swap. No render-blocking third-party scripts.
- Mobile first: no horizontal scroll, tap targets sized, text readable without zoom.
- Internal links: every important page linked from the home page and at least two others, with descriptive link text.
- HTTPS, no mixed content, redirects for old URLs.

Content
- Each page targets one search intent and uses the words the searcher would use, in the title, h1, first paragraph and at least one h2.
- Location and sector words where they matter: England, councils, local authorities, virtual schools, fostering services.
- Proof near the top: numbers, clients, awards.
- Case studies named by client and project, with the outcome in the first paragraph.

## 4. Who searches for us, and what they type

Reasoned from the client list (directors and assistant directors of children's services, heads of service, virtual school heads, fostering and corporate parenting leads, designated teachers, residential and leaving care managers, conference organisers). No search-volume tool was used; these are the phrases to confirm in Google Search Console once the site is live.

Consultancy
- children's social care consultancy
- children's services consultancy UK
- children's services transformation consultancy
- fostering recruitment and retention consultancy
- fostering service improvement
- youth participation strategy consultancy
- care leaver employment programme
- corporate parenting employment care leavers
- care leavers local offer consultancy
- co-production children's services

Training and programmes
- designated teacher training looked after children
- virtual school training for schools
- NVR training residential children's homes
- non-violent resistance training foster carers
- trauma-informed training schools children in care
- training on children in care for teachers
- case recording training social work
- attachment and trauma training school staff
- leadership programme care experienced young people
- care leavers leadership programme

Keynotes
- care experienced keynote speaker
- keynote speaker children's social care conference
- speaker for foster carer conference
- lived experience speaker social work

Brand searches (make sure we rank first)
- The Care Leaders
- Luke Rodgers BEM
- The Care Leaders Online
- The Care Leaders Fellowship
- Care to Work The Care Leaders

## 5. Audit findings and what changed

Before the pass: 148 colour contrast failures across the site, 6 invalid ARIA ids, 5 heading skips, 2 nested landmarks, titles up to 101 characters and descriptions up to 201, 47 pages with images not lazy loaded and no intrinsic sizes, footer and breadcrumb links under 24px tall, body text at 12 to 14px in cards and timetables, one page (consultancy-fostering) skipped by the site pass so it had the old menu, no canonical and a link to a redirect, and seven keynote brochure buttons that went nowhere.

Fixed
- Contrast: eyebrows and labels moved from teal #008196 to #006473 on beds, orange small text to #c4230a, Why Care cornflower tiles to navy text, tool-group labels to ink with a colour dot, Designated Leaders hero span to teal. Dark-ground themes set per kit.
- ARIA: explorer ids slugged (no spaces). Tools panel is a div, not a nested aside. Sessions use h3, not h4. Hidden h2s on Contact and Keynotes so headings never skip.
- Titles trimmed to 65 characters, descriptions to 160, every page.
- Images after the first two in main lazy-load with intrinsic width and height (CLS).
- Footer, breadcrumb and contact links padded to 24px targets. Visible focus ring (3px amber) on every control.
- Minimum 15px for card, timetable, list and note text. Paragraph measure capped at 72 characters.
- Fostering page now gets the shared header, footer, canonical, Open Graph and JSON-LD.
- Keynote brochure buttons now open an email request until the PDFs exist.
- Duplicate scatter shapes on hand-edited pages removed.

Still to do (needs Luke or a live domain)
- Cookie banner: not needed yet because the site sets no cookies. Needed the day Mailchimp, analytics or YouTube embeds go live.
- Privacy page: add the lawful basis, retention and complaint route lines once Mailchimp is in.
- Accessibility statement page.
- Run Lighthouse on the live domain for Core Web Vitals; the local build cannot measure real load times.
- Submit the sitemap to Google Search Console and check the keyword list above against real queries after four weeks.
- Case study hero and gallery photography (Summit, PROCLAIM, Bucks, Durham Cares) is still the biggest visual gap.

## 6. Processes on the site and what each needs

| Process | Where | Status | Needs |
|---|---|---|---|
| Brochure download (gated) | Designated Leaders, Academy, Care to Work, NVR Programme, Fellowship, Good recording, NVR Essentials, Journey Through Care, Tools for Schools | Holding message, no email sent | Mailchimp audience, nine landing pages or one with a hidden field, nine PDFs (five not yet made: NVR Programme, Care to Work, Fellowship 2027, four course brochures) |
| Keynote brochure | Keynote thank-you page, seven buttons | Opens an email request | Seven keynote PDFs, then the gated download above |
| Book a keynote | Keynotes page and Contact | Live, Microsoft Forms | The auto-reply flow in the keynote booking spec |
| Start a conversation | Every page | Live, email and phone | Nothing |
| Watch on YouTube | Case studies | Live links | CLNM video still to confirm |
| The Care Leaders Online | Footer and Training | Live link | Nothing |
| Newsletter sign-up | Not on the site | Missing | Decide whether to add once Mailchimp is in |

These items are added to the keynote automation list in docs/go-live-checklist.md.
