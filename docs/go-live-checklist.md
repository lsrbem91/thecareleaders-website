# Go-live checklist

Created 22 October 2026. There was no checklist in the repo before this, so this file starts it.

## Content fixes (branch fixes-2026-10-22, not yet merged)

- [x] Figures: "36 local authorities" used everywhere; "50" now reads as a separate total (organisations, including the 36 councils plus national bodies and partners). Pages: index, our-work, about, training, partnerships, search index.
- [x] Keynotes stat reworded to "4,000+ delegates have heard Luke speak since 2024". Page: keynotes.
- [x] "Plain English" removed everywhere it was used. Pages: training, be-the-first-yes, co-producing-your-local-offer.
- [x] Programmes page: "what it costs to commission" changed to "how to commission it".
- [x] Consultancy word marks (bulb and glyph letters): proper words added as screen-reader text. Pages: consultancy, consultancy-transformation, consultancy-participation, consultancy-employment, about.
- [x] Programme brochures: "2026 to 27" removed from the covers of Designated Leaders, Mentors Who Care and The NVR Programme (PDFs and cover images).
- [x] Free resources page built, then removed on 22 October at Luke's request (can be rebuilt from git history).
- [x] Blog kept (Luke decided 22 October).

## Mailchimp

- [x] Tag brochure-mentors-who-care created (ID 4229774) and wired into the brochure form.
- [x] Tag guide-attachment-trauma created (ID 4229775), kept for when free resources return.
- [x] Undated PDFs uploaded to Mailchimp files: designated_leaders.01.pdf, mentors_who_care.pdf, nvr_programme.pdf.
- [x] Brochure delivery - NVR Programme: built as a draft (trigger brochure-nvr-advanced, NVR email, undated PDF and cover). Luke to check and click Continue > Turn flow on.
- [x] Brochure delivery - Mentors Who Care: built as a draft (trigger brochure-mentors-who-care, Mentors email, undated PDF and cover). Luke to check and click Continue > Turn flow on.
- [x] Designated Leaders email (live flow): Pause & edit, then swap the header image for br-designated-leaders.01.jpg and the download link for designated-leaders.02.pdf (no phone number), both in Content Studio. Turn back on.
- [x] Phone number removed from brochures. In Content Studio, swap the download link in each live brochure email for the new file: Academy > care-leaders-academy.01.pdf, Fellowship > care-leaders-fellowship.01.pdf, Care to Work > care-to-work.01.pdf (and the .01 versions of the two Care to Work sub-brochures if any email uses them). NVR and Mentors files were already clean.
- [x] Welcome email delayed by one day so new contacts don't get two emails at once (done 22 October, all flows back on).
- [ ] Popup: the "Website popup | Free mini-guide" form is still a draft. Connect www.thecareleaders.com as a site in Mailchimp (Integrations > Manually connect site), add the mc.js snippet to every page, then publish the popup. Do this at the domain switch: the connection checks the live domain.
- [ ] Add "Being a podcast guest" to the Power Automate auto-reply flow (optional).

## Power Automate enquiry flow

- [x] Brochure links: all six programmes (DLP, Academy, Care to Work, Fellowship, NVR Programme, Mentors Who Care) now get the brochure in the auto-reply. NVR points to the undated nvr-programme.pdf. Training entries removed.
- [x] Auto-replies (keynote, holding, general) now send from hello@, with no Reply To pointing at luke@.
- [x] "Copy to Luke" now goes to hello@, not luke@, and only for keynote and training enquiries (the ones that check the diary). Other enquiries get the Web3Forms notification only.
- [x] First names are capitalised before they reach the auto-reply and the brochure emails.
- [x] "Website enquiry: forward to Luke" flow is off.
- [x] Web3Forms already sends to hello@ and the flow trigger already watches hello@. The emails in luke@ came from "Copy to Luke", now fixed.
- [ ] At the domain switch: change the github.io links in BrochureLine and the booking terms links in Keynote reply (and check the other reply steps) to https://www.thecareleaders.com/.

- [ ] DfE Fostering Quality Standards case study built (case-study-dfe-fostering-standards.html) but hidden until DfE approves: not linked anywhere, noindex, out of sitemap and search. On approval: add the Our work card, the Fostering page button, sitemap, search, and the Summit > NMS > NAVSH previous/next chain, and remove the noindex tag.
- [ ] Get DfE (Aisling Nuttall / Ola Wojnowska) OK to publish the case study before unhiding it (does not block the domain switch): the engagement report was written for the Department and the standards are not yet published.

## Tests before the switch

- [x] Send one enquiry through the contact form and one podcast guest form; check both reach hello@ (passed 22 October).
- [x] Download one programme brochure with a fresh email address; check the email arrives (passed 22 October).
- [x] Client quotes approved by text (Adrian Dyke, Emmy O'Shaughnessy, Paul Rudd); NAVSH wording approved. Confirmed by Luke 22 October.

- [x] Full site test, 96 pages at 1280 and 390 (22 October): no JS errors, broken links or overflow.
- [x] Safari: card images no longer cropped (confirmed by Luke 22 October).

## Domain switch (do together)

1. Sign in to GitHub in Chrome. Repo Settings > Pages > custom domain www.thecareleaders.com. Add the CNAME file to the repo at the same time.
2. DNS: www CNAME to lsrbem91.github.io. Apex A records 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.
3. Leave the Microsoft email records alone: MX, SPF TXT, DKIM, autodiscover.
4. After about an hour, tick Enforce HTTPS, then recheck the live site and old-site redirects.
5. Cancel the WordPress hosting only once the new site is confirmed live.
