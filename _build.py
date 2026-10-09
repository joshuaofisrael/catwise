#!/usr/bin/env python3
"""MeowWise static site builder.
Content lives in _src/ as HTML fragments with a small front matter header.
Run: python3 _build.py   (writes the static site into the repo root; commit the output)

To move to a custom domain later: change SITE_URL below, add a CNAME file, rebuild, push,
then re ping IndexNow (./indexnow.sh) on the new host.
"""
import html, json, os, re, glob, datetime

SITE_URL = "https://meowwise.com/"   # <- the ONE place the base URL lives
SITE_NAME = "MeowWise"
LEGAL = "Joshua Israel Ventures LLC"
EMAIL = "joshuaofisrael@gmail.com"
INDEXNOW_KEY = "fbe2e797c1db901fb91646b40e01856f"
CF_BEACON_TOKEN = ""      # Cloudflare Web Analytics token; empty = beacon omitted
GSC_TOKEN = ""            # Google Search Console verification token; empty = tag omitted
TODAY = "2026-10-09"

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "_src")

NAV = [("index.html", "Home"), ("breeds.html", "Breeds"), ("care.html", "Care"), ("health.html", "Health"),
       ("behavior.html", "Behavior"), ("nutrition.html", "Nutrition"), ("kittens.html", "Kittens"),
       ("senior-cats.html", "Senior Cats"), ("toxic-to-cats.html", "Toxic Plants"), ("myths.html", "Myths vs Facts"), ("glossary.html", "Glossary"),
       ("blog/", "Blog"), ("games/", "Games"), ("teachers/", "Teachers"), ("contact.html", "Contact")]

# Pages that get the "Cite this page" box and a visible last reviewed date
CITABLE = ("article", "blog", "teacher", "research")
SECTIONS = {"games/": ("Games", "games/index.html"), "blog/": ("Blog", "blog/index.html"), "teachers/": ("For teachers", "teachers/index.html")}

LOGO = ('<svg role="img" width="36" height="36" viewBox="0 0 64 64" aria-labelledby="logo-t"><title id="logo-t">MeowWise logo</title>'
        '<path d="M12 54V22L8 6l16 10h16l16-10-4 16v32z" fill="#8e5cc8"/><path d="M13 19l-1-8 7 5zM51 19l1-8-7 5z" fill="#f8cfe2"/>'
        '<circle cx="24" cy="32" r="4" fill="#2b2236"/><circle cx="40" cy="32" r="4" fill="#2b2236"/>'
        '<path d="M29 40h6l-3 3.5z" fill="#f48fb1"/><path d="M14 42l10 1M14 47l10-1M50 42l-10 1M50 47l-10-1" stroke="#2b2236" stroke-width="1.6" stroke-linecap="round"/></svg>')

# Hand authored doodles (tiny inline SVG, decorative only)
PAW_DEF = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><symbol id="mw-paw" viewBox="0 0 24 24"><g fill="currentColor">'
           '<ellipse cx="12" cy="16.5" rx="5.2" ry="4.2"/><circle cx="5.6" cy="10.4" r="2.2"/><circle cx="9.6" cy="6.4" r="2.2"/>'
           '<circle cx="14.4" cy="6.4" r="2.2"/><circle cx="18.4" cy="10.4" r="2.2"/></g></symbol></svg>')
PAW = '<svg class="paw" width="18" height="18" aria-hidden="true" focusable="false"><use href="#mw-paw"/></svg>'
DIVIDER = '<div class="doodle" aria-hidden="true">' + PAW * 5 + '</div>'
YARN = ('<svg class="yarn" viewBox="0 0 40 40" width="34" height="34" aria-hidden="true" focusable="false">'
        '<circle cx="18" cy="18" r="12" fill="#f8cfe2" stroke="#b5487e" stroke-width="1.5"/>'
        '<path d="M8 14c6 2 14 2 20-4M7 20c8 2 16 0 22-8M10 26c6-1 12-5 16-12M22 7c-3 6-3 15 1 22" fill="none" stroke="#b5487e" stroke-width="1.3"/>'
        '<path d="M28 26c4 3 6 6 3 9s-6 0-8 3" fill="none" stroke="#b5487e" stroke-width="1.3" stroke-linecap="round"/></svg>')
FONT_LINKS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600&amp;display=swap">')


def parse(path):
    raw = open(path, encoding="utf-8").read()
    head, body = raw.split("\n---\n", 1)
    meta = {"source": [], "related": []}
    for line in head.strip().splitlines():
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if k == "source":
            label, url = [x.strip() for x in v.rsplit("|", 1)]
            meta["source"].append((label, url))
        elif k == "ngss":
            code, url = [x.strip() for x in v.split("|", 1)]
            meta.setdefault("ngss", []).append((code, url))
        elif k == "related":
            meta["related"] = [x.strip() for x in v.split(",") if x.strip()]
        else:
            meta[k] = v
    rel = os.path.relpath(path, SRC).replace(os.sep, "/")
    meta["slug"] = rel
    meta["body"] = body
    meta.setdefault("type", "article")
    meta.setdefault("published", TODAY)
    meta.setdefault("updated", meta["published"])
    meta.setdefault("label", meta.get("h1", meta["title"].split(" | ")[0]))
    meta.setdefault("reviewed", meta["updated"])
    return meta


def url_of(slug):
    if slug.endswith("index.html"):
        slug = slug[: -len("index.html")]
    return SITE_URL + slug


def fix_links(s, prefix):
    def rep(m):
        target = m.group(2)
        if target == "/":
            target = prefix or "./"
        else:
            target = prefix + target[1:]
        return m.group(1) + target + '"'
    return re.sub(r'((?:href|src)=")(/(?!/)[^"]*)"', rep, s)


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def faq_items(body):
    m = re.search(r'<section class="card faq"[^>]*>(.*?)</section>', body, re.S)
    if not m:
        return []
    return [(strip_tags(q), strip_tags(a)) for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>", m.group(1), re.S)]


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


BRAND = {"@type": "Brand", "name": SITE_NAME, "url": SITE_URL, "logo": SITE_URL + "favicon.svg"}
# MeowWise is only a brand (not a DBA); the legal publisher is always the LLC.
ORG = {"@type": "Organization", "@id": SITE_URL + "#org", "name": LEGAL, "legalName": LEGAL, "url": SITE_URL, "email": EMAIL,
       "brand": BRAND}


def human_date(d):
    return datetime.date.fromisoformat(d).strftime("%-d %B %Y")


def apa_date(d):
    return datetime.date.fromisoformat(d).strftime("%Y, %B %-d")


def mla_date(d):
    mon = {1: "Jan.", 2: "Feb.", 3: "Mar.", 4: "Apr.", 5: "May", 6: "June", 7: "July", 8: "Aug.", 9: "Sept.", 10: "Oct.", 11: "Nov.", 12: "Dec."}[d.month]
    return f"{d.day} {mon} {d.year}"


def cite_box(p, url):
    t = p.get("h1", p["title"].split(" | ")[0])
    d = datetime.date.fromisoformat(p["reviewed"])
    bare = url.replace("https://", "")
    tq = html.escape(t if t.endswith(("?", "!", ".")) else t + ".")
    tt = html.escape(t)
    apa = f"{SITE_NAME}. ({apa_date(p['reviewed'])}). <i>{tt}</i>{'' if t.endswith(('?', '!', '.')) else '.'} {url}"
    mla = f"\u201c{tq}\u201d <i>{SITE_NAME}</i>, {LEGAL}, {mla_date(d)}, {bare}."
    chi = f"{SITE_NAME}. \u201c{tq}\u201d {LEGAL}. Last modified {d.strftime('%B %-d, %Y')}. {url}."
    return ('<section class="card cite" id="cite" aria-labelledby="cite-h"><h2 id="cite-h">Cite this page</h2>'
            '<p class="sci">Students and teachers are welcome to cite this page. Add your access date if your teacher or style guide asks for one.</p>'
            f'<p><b>APA (7th ed.)</b><br>{apa}</p><p><b>MLA (9th ed.)</b><br>{mla}</p><p><b>Chicago (bibliography)</b><br>{chi}</p></section>')


def games_live():
    return os.path.exists(os.path.join(ROOT, "games", "index.html"))


def render(p, pages_by_slug, blog_posts):
    slug = p["slug"]
    prefix = "../" * slug.count("/")
    url = url_of(slug)
    title = p["title"]
    desc = p["description"]
    typ = p["type"]
    noindex = typ in ("noindex",)
    body = p["body"].replace("{{SITE}}", SITE_URL)

    if "{{BLOG_LIST}}" in body:
        items = "".join(
            f'<li><a href="/{b["slug"]}"><b>{html.escape(b["label"])}</b></a><br><span class=sci>{html.escape(b["description"])}</span></li>'
            for b in blog_posts)
        body = body.replace("{{BLOG_LIST}}", f'<ul class="postlist">{items}</ul>')

    if "{{GAMES}}" in body:
        if games_live():
            g = ('<p>Our free <a href="/games/">MeowWise cat games</a> run in the browser with no sign up, no accounts and no data collected. '
                 'Use them as a warm up, a station activity or a reward after a worksheet, then ask students what real cat fact each game is based on.</p>')
        else:
            g = ('<p><b>Coming soon:</b> a small set of free, original cat games that run in the browser with no sign up and no data collected. '
                 'They will appear on this page as classroom activity ideas when they launch.</p>')
        body = body.replace("{{GAMES}}", g)

    lds = []
    if typ == "home":
        lds.append({"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL,
                    "publisher": {"@type": "Organization", "@id": SITE_URL + "#org", "name": LEGAL}})
        lds.append(dict({"@context": "https://schema.org"}, **ORG))
    crumbs = []
    if typ != "home" and not noindex:
        crumbs = [("Home", SITE_URL, "index.html")]
        for pre, (nm, idx) in SECTIONS.items():
            if slug.startswith(pre) and slug != idx:
                crumbs.append((nm, url_of(idx), pre))
        crumbs.append((p["label"], url, ""))
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u, _) in enumerate(crumbs)]})
    if typ in ("article", "blog"):
        lds.append({"@context": "https://schema.org", "@type": "BlogPosting" if typ == "blog" else "Article",
                    "headline": p.get("h1", title)[:110], "description": desc,
                    "datePublished": p["published"], "dateModified": p["updated"],
                    "image": SITE_URL + "og.png", "author": {"@type": "Organization", "@id": SITE_URL + "#org", "name": LEGAL, "url": SITE_URL},
                    "publisher": dict({"@context": "https://schema.org"}, **ORG), "mainEntityOfPage": url,
                    "citation": [u for _, u in p["source"]] or None})
        if lds[-1]["citation"] is None:
            del lds[-1]["citation"]
    if typ == "teacher":
        lr = {"@context": "https://schema.org", "@type": "LearningResource", "name": p.get("h1", title), "description": desc, "url": url,
              "inLanguage": "en", "isAccessibleForFree": True, "learningResourceType": p.get("resource_type", "Lesson ideas"),
              "educationalLevel": [x.strip() for x in p.get("level", "").split(",") if x.strip()],
              "audience": {"@type": "EducationalAudience", "educationalRole": "teacher"},
              "datePublished": p["published"], "dateModified": p["reviewed"],
              "publisher": dict({"@context": "https://schema.org"}, **ORG), "author": {"@type": "Organization", "@id": SITE_URL + "#org", "name": LEGAL},
              "about": {"@type": "Thing", "name": "Domestic cat", "sameAs": "https://www.wikidata.org/wiki/Q146"}}
        if p.get("ngss"):
            lr["educationalAlignment"] = [{"@type": "AlignmentObject", "alignmentType": "teaches",
                                           "educationalFramework": "Next Generation Science Standards", "targetName": c, "targetUrl": u}
                                          for c, u in p["ngss"]]
        if p["source"]:
            lr["citation"] = [u for _, u in p["source"]]
        lds.append(lr)
    if typ == "research":
        items = re.findall(r'<li class="paper"[^>]*data-doi="([^"]+)"[^>]*>(.*?)</li>', body, re.S)
        parts = []
        for doi, inner in items:
            m = re.search(r'<cite>(.*?)</cite>', inner, re.S)
            parts.append({"@type": "ScholarlyArticle", "name": strip_tags(m.group(1)) if m else doi, "sameAs": "https://doi.org/" + doi,
                          "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": doi}})
        lds.append({"@context": "https://schema.org", "@type": "CollectionPage", "name": p.get("h1", title), "description": desc, "url": url,
                    "dateModified": p["reviewed"], "publisher": dict({"@context": "https://schema.org"}, **ORG),
                    "audience": {"@type": "Audience", "audienceType": "students, teachers and researchers"},
                    "mainEntity": {"@type": "ItemList", "numberOfItems": len(parts),
                                   "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": x} for i, x in enumerate(parts)]}})
    faqs = faq_items(body)
    if faqs:
        lds.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})

    head = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width,initial-scale=1">']
    if GSC_TOKEN and typ == "home":
        head.append(f'<meta name="google-site-verification" content="{GSC_TOKEN}">')
    head.append(f"<title>{html.escape(title)}</title>")
    head.append(f'<meta name="description" content="{html.escape(desc)}">')
    if noindex:
        head.append('<meta name="robots" content="noindex">')
    else:
        head.append(f'<link rel="canonical" href="{url}">')
    css = SITE_URL + "style.css" if slug == "404.html" else prefix + "style.css"
    fav = SITE_URL + "favicon.svg" if slug == "404.html" else prefix + "favicon.svg"
    head.append(FONT_LINKS)
    head.append(f'<link rel="stylesheet" href="{css}"><link rel="icon" href="{fav}" type="image/svg+xml">')
    ogt = "article" if typ in ("article", "blog") else "website"
    head.append(f'<meta property="og:type" content="{ogt}"><meta property="og:site_name" content="{SITE_NAME}">'
                f'<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
                f'<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}og.png">'
                f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
                f'<meta property="og:image:alt" content="MeowWise: plain language cat care guide">'
                f'<meta name="twitter:card" content="summary_large_image">')
    head += [ld(x) for x in lds]
    head.append("</head><body>")

    def link(target):
        return SITE_URL + target if slug == "404.html" else "/" + target

    navhtml = "".join(
        f'<a href="{link(t)}"' + (' aria-current="page"' if (t == slug or (t == "blog/" and slug.startswith("blog/")) or (t == "games/" and slug.startswith("games/"))) else "") + f">{n}</a>"
        for t, n in NAV)
    header = (PAW_DEF + f'<a class="skip" href="#main">Skip to content</a><header><a class="brand" href="{link("index.html")}">{LOGO}<span>{SITE_NAME}</span>{PAW}</a>'
              '<button class="menu" aria-label="Menu" onclick="document.body.classList.toggle(\'open\')">☰</button>'
              f'<nav aria-label="Main">{navhtml}</nav></header>')

    main = ['<main id="main">']
    if crumbs:
        main.append('<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(
            f'<a href="{link(t)}">{html.escape(n)}</a>' if i < len(crumbs) - 1
            else f'<span aria-current="page">{html.escape(n)}</span>' for i, (n, u, t) in enumerate(crumbs)) + "</nav>")
    if p.get("h1") and typ != "home":
        main.append(f'<h1>{html.escape(p["h1"])}</h1>')
    if typ in CITABLE:
        main.append(f'<p class="meta">By the {SITE_NAME} team · Published <time datetime="{p["published"]}">{human_date(p["published"])}</time>'
                    f' · Last reviewed <time datetime="{p["reviewed"]}">{human_date(p["reviewed"])}</time></p>')
    if p.get("printable"):
        main.append('<p class="noprint"><button class="btn" type="button" onclick="window.print()">Print this page</button> '
                    '<span class="sci">Free to print for classroom use. No sign up, no ads.</span></p>')
    main.append(body)
    if p["related"]:
        lis = "".join(f'<li><a href="/{r}">{html.escape(pages_by_slug[r]["label"])}</a></li>' for r in p["related"])
        main.append(f'<aside class="card related"><h2>Keep reading</h2><ul>{lis}</ul></aside>')
    if p["source"]:
        lis = "".join(f'<li><a href="{html.escape(u)}" rel="noopener">{html.escape(l)}</a></li>' for l, u in p["source"])
        main.append(f'<section class="card sources" id="sources"><h2>Sources</h2><ol>{lis}</ol></section>')
    if typ in CITABLE:
        main.append(cite_box(p, url))
    if typ in ("article", "blog"):
        main.append('<p class="note">General education, not veterinary advice. If you are worried about your cat, contact your veterinarian; in an emergency, go to the nearest emergency vet.</p>')
    main.append("</main>")

    footer = (DIVIDER + f'<footer>{YARN}<section class="contact-us" id="contact-us" aria-labelledby="contact-us-h"><h2 id="contact-us-h">Contact us</h2>'
              f'<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use our <a href="{link("contact.html")}">contact form</a>.</p></section>'
              f'<p>{SITE_NAME}: original educational content about cats. All text and illustrations are original; photos are CC0 and credited. Not a substitute for veterinary care.</p>'
              f'<p class="llc">© 2026 {LEGAL}. All rights reserved. {SITE_NAME} is owned and operated by {LEGAL}.</p>'
              f'<p class="legal"><a href="{link("terms.html")}">Terms</a> · <a href="{link("privacy.html")}">Privacy</a> · <a href="{link("disclaimer.html")}">Disclaimer</a> · <a href="{link("contact.html")}">Contact</a> · <a href="{link("about.html")}">About</a> · <a href="{link("blog/")}">Blog</a> · <a href="{link("teachers/")}">For teachers</a> · <a href="{link("research/")}">Research</a> · <a href="{link("games/")}">Games</a> · <a href="{link("photo-credits.html")}">Photo credits</a></p></footer>')
    beacon = ""
    if CF_BEACON_TOKEN:
        beacon = ("<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
                  f"data-cf-beacon='{{\"token\": \"{CF_BEACON_TOKEN}\"}}'></script><!-- End Cloudflare Web Analytics -->")
    out = "\n".join(head) + "\n" + header + "\n" + "\n".join(main) + "\n" + footer + beacon + "</body></html>\n"
    if slug != "404.html":
        out = fix_links(out, prefix)
    return out


def main():
    pages = [parse(f) for f in sorted(glob.glob(os.path.join(SRC, "**", "*.html"), recursive=True))]
    by_slug = {p["slug"]: p for p in pages}
    blog_posts = sorted([p for p in pages if p["type"] == "blog"], key=lambda p: (p["published"], p["title"]))
    for p in pages:
        dest = os.path.join(ROOT, p["slug"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(render(p, by_slug, blog_posts))
    indexable = [p for p in pages if p["type"] != "noindex"]
    order = {s: i for i, (s, _) in enumerate(NAV)}
    indexable.sort(key=lambda p: (order.get(p["slug"], order.get(p["slug"].replace("index.html", ""), 99)), p["slug"]))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in indexable:
        sm.append(f"<url><loc>{url_of(p['slug'])}</loc><lastmod>{p['updated']}</lastmod></url>")
    sm.append(f"<url><loc>{SITE_URL}llms.txt</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")

    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "Perplexity-User",
            "ClaudeBot", "Claude-SearchBot", "Claude-User", "Google-Extended", "Applebot", "Applebot-Extended",
            "DuckAssistBot", "Amazonbot"]
    rb = "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {SITE_URL}sitemap.xml\n"
    open(os.path.join(ROOT, "robots.txt"), "w").write(rb)

    def line(p):
        return f"- [{p['label']}]({url_of(p['slug'])}): {p['description']}"
    guides = [p for p in indexable if p["type"] == "article" and not p["slug"].startswith("blog/") and p.get("group") != "tool"]
    tools = [p for p in indexable if p.get("group") == "tool"]
    posts = [p for p in indexable if p["type"] == "blog"]
    edu = [p for p in indexable if p["type"] in ("teacher", "research")]
    info = [by_slug[s] for s in ("about.html", "contact.html", "terms.html", "privacy.html", "disclaimer.html") if s in by_slug]
    breeds_anchor = by_slug.get("breeds.html", {}).get("anchors", "").replace("{{SITE}}", SITE_URL)
    llms = [f"# {SITE_NAME}", "",
            f"> {SITE_NAME} is a free, original, plain language guide to cats for owners and future owners: cat breeds and their inherited health risks, everyday care, health warning signs and emergencies, behavior and body language, nutrition, kittens and senior cats. Every guide answers the main question first and cites veterinary sources such as the Cornell Feline Health Center, AAFP, AAHA, International Cat Care and UC Davis. {SITE_NAME} is a brand owned and operated by {LEGAL}.",
            "", "The content is general education, not veterinary advice.", "", "## Guides"]
    for p in guides:
        llms.append(line(p))
        if p["slug"] == "breeds.html" and breeds_anchor:
            llms.append("  - Breed sections: " + breeds_anchor)
    llms += ["", "## Tools"] + [line(p) + " (searchable table with a stable #anchor per item)" for p in tools]
    llms += ["", "## Blog"] + [line(p) for p in posts]
    llms += ["", "## For teachers, students and researchers", "Free classroom resources (no sign up, no ads, no data collection) with NGSS alignments, answer keys, a vocabulary list, and a list of peer reviewed papers with DOIs."]
    llms += [line(p) for p in edu]
    llms += ["", "## Optional"] + [line(p) for p in info]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(llms) + "\n")
    open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w").write(INDEXNOW_KEY)
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    print(f"built {len(pages)} pages, {len(indexable)} in sitemap")


if __name__ == "__main__":
    main()
