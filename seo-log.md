# MeowWise SEO log

## 2026-10-08: v1 launch
Built: home, 9 guides (breeds, care, health, behavior, nutrition, kittens, senior cats, myths, glossary), blog index + 5 answer first posts, About, Contact (mailto + FormSubmit form), Privacy, thanks (noindex), 404 (noindex).
Signature tool: /toxic-to-cats.html "Is this plant or household item toxic to cats?" checker (51 entries; lilies flagship; cut flowers, houseplants, garden plants, essential oils, household and medicines, small food section; per entry anchor, risk level, call line first, sources and reviewed date; FAQPage). Second asset: /breeds.html breed health checklist (15 breeds, inherited conditions with DNA tests per UC Davis VGL and Cornell HCM breed list), deep linkable rows (#maine-coon etc) and breeder questions.
SEO: unique titles/descriptions, canonicals, OG + og.png, JSON-LD (WebSite, Organization on home; Article/BlogPosting with dates, citations; BreadcrumbList; FAQPage only for visible FAQs), sitemap with lastmod, robots.txt allowing all search and AI crawlers, llms.txt, IndexNow key file.
Every page footer: visible "Contact us" (mailto joshuaofisrael@gmail.com + link to form) and "Operated by Joshua Israel Ventures LLC".
Pending: Cloudflare beacon token (API token lacks Web Analytics permission), GSC verification token from Joshua, FormSubmit activation click, custom domain.

## Scorecard
| Date | Window | Impressions | Clicks | CTR | Avg pos | Indexed pages | Top100/20/10/3 queries | Growing pages | Declining pages | Conversions |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-08 | 7d | n/a (no GSC yet) | n/a | n/a | n/a | 20 URLs in sitemap | n/a | n/a | n/a | n/a |

## 2026-10-08 launch checks
- Live: all 20 sitemap URLs plus robots.txt, sitemap.xml, llms.txt, key file, og.png return 200; unknown path returns 404 page.
- IndexNow (api.indexnow.org): HTTP 202 for 21 URLs (20 pages plus llms.txt).
- Crawler UA spot check (Googlebot, Bingbot, GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Claude-SearchBot, Applebot, DuckAssistBot, Amazonbot): 200.
- Open: Cloudflare beacon (token lacks RUM permission), GSC verification token, FormSubmit activation.

## 2026-10-08 rebrand to MeowWise
- Reason: the previous name failed the trademark check (an existing cat care app and a published book use it). Planned domain: meowwise.com (no CNAME yet).
- Repo renamed to joshuaofisrael/meowwise; base path now /meowwise/. Old project path URLs return 404 (GitHub does not redirect project Pages after a rename).
- Live check: all 20 sitemap URLs plus robots.txt, sitemap.xml, llms.txt, key file, og.png, favicon, style.css return 200; 404 page works.
- IndexNow (api.indexnow.org): HTTP 202 for 21 URLs at the new location.
- og.png regenerated with the MeowWise name.
- FormSubmit: one test submission sent; activation email requested (pending Joshua's click).

## 2026-10-08 custom domain meowwise.com
- DNS: four GitHub apex A records plus www CNAME (verified with dig). CNAME file added; Pages custom domain set via API.
- Certificate: Let's Encrypt, approved for meowwise.com and www.meowwise.com, expires 2027-01-06. Enforce HTTPS on.
- All canonicals, OG URLs, JSON-LD, sitemap.xml, robots.txt Sitemap line, llms.txt and indexnow.sh now use https://meowwise.com/. 0 github.io strings in site output.
- Live: all 20 sitemap URLs plus robots.txt, sitemap.xml, llms.txt, key file, og.png return 200 over HTTPS. www and the old github.io path redirect to https://meowwise.com/.
- IndexNow (api.indexnow.org, host meowwise.com): HTTP 202 for 21 URLs.
- FormSubmit: one test from meowwise.com; activation email requested.
- Next: Search Console (domain property or HTML tag) when Joshua is back.

## 2026-10-08 pastel restyle and LLC legal pages (commit 04d4488)
- Restyle: pastel pink background #fff5fa, lavender #f1eafb, mint #b8ecd7, plum headings #5b2a86, links #6a2c9e, ink #2b2236. Fredoka 600 headings from Google Fonts (preconnect, display=swap, one weight). Inline SVG paw and yarn doodles. style.css 3166 to 5461 bytes. All text pairs checked at WCAG AA or better (see /workspace/animal-sites/cats/contrast-2026-10-08.txt).
- Legal: footer "© 2026 Joshua Israel Ventures LLC. All rights reserved. MeowWise is owned and operated by Joshua Israel Ventures LLC." plus Terms, Privacy, Disclaimer, Contact links on every page. New /terms.html and /disclaimer.html; privacy rewritten (LLC is controller); About says MeowWise is a brand of the LLC. JSON-LD Organization is the LLC with MeowWise as Brand; WebSite and Article publisher point to the LLC.
- Sitemap now 22 pages plus llms.txt. IndexNow: HTTP 200 for 23 URLs (all pages changed by the footer).
- Deferred to after 19:45 London (box load rules): screenshots at 390x844 and 1280x800, full live crawl, games hub.

## 2026-10-08 education campaign step 1: teachers hub, research page, Cite this page
- Opportunity: teacher and student searches ("cat worksheet for 3rd grade", "cat adaptations lesson plan", "cat facts for kids printable") plus citation friendly pages that educators, librarians and AI answer engines can recommend.
- New pages (8): /teachers/ hub (LearningResource, 7 NGSS PEs verified on nextgenscience.org: K-LS1-1, 1-LS1-2, 3-LS3-1, 4-LS1-1, 4-LS1-2, MS-LS4-5, HS-LS3-1), /teachers/cat-fact-sheet.html, /teachers/cat-worksheet-3rd-grade.html, /teachers/cat-adaptations-lesson-plan.html, /teachers/cat-quiz.html, /teachers/vocabulary.html, /research/ (CollectionPage with 19 ScholarlyArticle DOIs, every DOI checked against Europe PMC, Crossref or the publisher).
- Site wide: "Cite this page" box (APA 7, MLA 9, Chicago) and "Published / Last reviewed" line on every article, blog post, teacher page and the research page. Teachers nav item; footer links For teachers and Research; home tile. Print CSS (black on white, menus and footer extras hidden, answer keys on a new page).
- llms.txt: new "For teachers, students and researchers" section. Sitemap 29 pages plus llms.txt.
- Games: hub shows a "coming soon" note; it switches to a /games/ link automatically on the next build once games/index.html exists.
- Outreach target CSV kept local only (outreach/ is in .gitignore) because the repo is public.

## 2026-10-08 daily run: cat communication cluster plus fact article
- Data: no Search Console or analytics yet (both pending), so no query data to act on. Light run only (weekday 14:00 to 19:45 box load window).
- Highest EV action: build out the behavior and communication cluster, which already has the slow blink post. New answer first post "Do cats know their names?" (high volume question query; top results are mostly news rewrites of the 2019 study, so a page with the actual study design, numbers, the 2022 follow up and the limits adds value).
- Internal links: behavior pillar gets a "Do cats know their names?" card, the Saito 2019 source and a related link; slow blink post links to it; /research/ gains Saito 2019 and Takagi 2022 entries and the Saito 2013 entry now lists the post under Used on. Blog index description updated.
- Article sources (all opened): Saito et al. 2019 Sci Rep 9:5394 (10.1038/s41598-019-40616-4); Takagi et al. 2022 Sci Rep 12:6155 (10.1038/s41598-022-10261-5); Saito and Shinozuka 2013 Anim Cogn 16:685-690 (10.1007/s10071-013-0620-4). Details confirmed on Crossref.
- Schema: BlogPosting (publisher Joshua Israel Ventures LLC), FAQPage with 4 questions, BreadcrumbList. Sitemap 30 pages plus llms.txt.
