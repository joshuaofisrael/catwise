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
