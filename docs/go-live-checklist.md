# Go-live checklist

Created 22 October 2026. There was no checklist in the repo before this, so this file starts it.

## Content fixes (branch fixes-2026-10-22, not yet merged)

- [x] Figures: "36 local authorities" used everywhere; "50" now reads as a separate total (organisations, including the 36 councils plus national bodies and partners). Pages: index, our-work, about, training, partnerships, search index.
- [x] Keynotes stat reworded to "4,000+ delegates have heard Luke speak since 2024". Page: keynotes.
- [x] "Plain English" removed everywhere it was used. Pages: training, be-the-first-yes, co-producing-your-local-offer.
- [x] Programmes page: "what it costs to commission" changed to "how to commission it".
- [x] Consultancy word marks (bulb and glyph letters): proper words added as screen-reader text. Pages: consultancy, consultancy-transformation, consultancy-participation, consultancy-employment, about.
- [x] Programme brochures: "2026 to 27" removed from the covers of Designated Leaders, Mentors Who Care and The NVR Programme (PDFs and cover images).
- [x] Free resources page (resources.html) with a gated download for the Attachment Aware and Trauma Informed mini guide. Linked from the main menu and footer on every page.
- [ ] Add the mini guide PDF at assets/docs/guides/attachment-aware-trauma-informed.pdf (Luke to supply). Check it has no "CPD accredited" wording.
- [x] Blog kept (Luke decided 22 October).

## Mailchimp

- [x] Tag brochure-mentors-who-care created (ID 4229774) and wired into the brochure form.
- [x] Tag guide-attachment-trauma created (ID 4229775) and wired into the resources form.
- [x] Undated PDFs uploaded to Mailchimp files: designated_leaders.01.pdf, mentors_who_care.pdf, nvr_programme.pdf.
- [ ] Brochure delivery - NVR Programme: built as a draft (trigger brochure-nvr-advanced, NVR email, undated PDF and cover). Luke to check and click Continue > Turn flow on.
- [ ] Brochure delivery - Mentors Who Care: built as a draft (trigger brochure-mentors-who-care, Mentors email, undated PDF and cover). Luke to check and click Continue > Turn flow on.
- [ ] Guide delivery automation for the Attachment and Trauma mini guide (needs the PDF).
- [ ] Designated Leaders email (live flow): Pause & edit, then swap the header image for br-designated-leaders.01.jpg and the download link for designated_leaders.01.pdf, both in Content Studio. Turn back on.
- [ ] Welcome email delayed by one day so new contacts don't get two emails at once.
- [ ] Popup: the "Website popup | Free mini-guide" form is still a draft. Connect www.thecareleaders.com as a site in Mailchimp (Integrations > Manually connect site), add the mc.js snippet to every page, then publish the popup. Do this at the domain switch: the connection checks the live domain.
- [ ] Add "Being a podcast guest" to the Power Automate auto-reply flow on hello@ (optional).

## Tests before the switch

- [ ] Send one enquiry through the contact form and one podcast guest form; check both reach hello@.
- [ ] Download one programme brochure with a fresh email address; check the email arrives.
- [ ] Get written OK for client quotes: Adrian Dyke, Emmy O'Shaughnessy, Paul Rudd, NAVSH framing.

## Domain switch (do together)

1. Sign in to GitHub in Chrome. Repo Settings > Pages > custom domain www.thecareleaders.com. Add the CNAME file to the repo at the same time.
2. DNS: www CNAME to lsrbem91.github.io. Apex A records 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.
3. Leave the Microsoft email records alone: MX, SPF TXT, DKIM, autodiscover.
4. After about an hour, tick Enforce HTTPS, then recheck the live site and old-site redirects.
5. Cancel the WordPress hosting only once the new site is confirmed live.
