# MeowWise

Original, sourced cat care information site operated by Joshua Israel Ventures LLC.

- Live: https://meowwise.com/ (custom domain via the `CNAME` file; GitHub Pages project repo joshuaofisrael/meowwise)
- Stack: HTML fragments in `_src/` rendered by `python3 _build.py` into static HTML at the repo root (commit the output). One `style.css`, no frameworks, no tracking cookies.
- Hosting: GitHub Pages, deploy from branch `main`, folder `/`.
- Base URL lives in one place: `SITE_URL` in `_build.py` (also `BASE` in `indexnow.sh`).
- Custom domain: `CNAME` contains `meowwise.com`; keep it in the repo root. Changing domain means updating `SITE_URL`, `BASE` and `CNAME` together, rebuilding, pushing, then `./indexnow.sh`.
- After every publish: add the page in `_src/`, rebuild (sitemap and llms.txt regenerate), push, wait for Pages, run `./indexnow.sh <changed urls>`, log it in `seo-log.md`.
- Analytics: set `CF_BEACON_TOKEN` in `_build.py` once a Cloudflare Web Analytics token exists. Search Console: set `GSC_TOKEN`.
- Toxic plant and household checker: edit `_tools/gen_toxic.py` (entries, sources, REVIEWED date), run it, then `python3 _build.py`.
