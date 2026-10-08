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
TODAY = "2026-10-08"

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "_src")

NAV = [("index.html", "Home"), ("breeds.html", "Breeds"), ("care.html", "Care"), ("health.html", "Health"),
       ("behavior.html", "Behavior"), ("nutrition.html", "Nutrition"), ("kittens.html", "Kittens"),
       ("senior-cats.html", "Senior Cats"), ("toxic-to-cats.html", "Toxic Plants"), ("myths.html", "Myths vs Facts"), ("glossary.html", "Glossary"),
       ("blog/", "Blog"), ("contact.html", "Contact")]

LOGO = ('<svg role="img" width="34" height="34" viewBox="0 0 64 64" aria-labelledby="logo-t"><title id="logo-t">MeowWise logo</title>'
        '<path d="M12 54V22L8 6l16 10h16l16-10-4 16v32z" fill="#b794f6"/>'
        '<circle cx="24" cy="32" r="4" fill="#17121f"/><circle cx="40" cy="32" r="4" fill="#17121f"/>'
        '<path d="M29 41h6l-3 3z" fill="#17121f"/><path d="M14 42l10 1M14 47l10-1M50 42l-10 1M50 47l-10-1" stroke="#17121f" stroke-width="1.6"/></svg>')


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


ORG = {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL, "legalName": LEGAL, "email": EMAIL,
       "logo": SITE_URL + "favicon.svg"}


def human_date(d):
    return datetime.date.fromisoformat(d).strftime("%-d %B %Y")


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

    lds = []
    if typ == "home":
        lds.append({"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL,
                    "publisher": {"@type": "Organization", "name": SITE_NAME, "legalName": LEGAL}})
        lds.append(dict({"@context": "https://schema.org"}, **ORG))
    crumbs = []
    if typ != "home" and not noindex:
        crumbs = [("Home", SITE_URL)]
        if slug.startswith("blog/") and slug != "blog/index.html":
            crumbs.append(("Blog", url_of("blog/index.html")))
        crumbs.append((p["label"], url))
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    if typ in ("article", "blog"):
        lds.append({"@context": "https://schema.org", "@type": "BlogPosting" if typ == "blog" else "Article",
                    "headline": p.get("h1", title)[:110], "description": desc,
                    "datePublished": p["published"], "dateModified": p["updated"],
                    "image": SITE_URL + "og.png", "author": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
                    "publisher": dict({"@context": "https://schema.org"}, **ORG), "mainEntityOfPage": url,
                    "citation": [u for _, u in p["source"]] or None})
        if lds[-1]["citation"] is None:
            del lds[-1]["citation"]
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
        f'<a href="{link(t)}"' + (' aria-current="page"' if (t == slug or (t == "blog/" and slug.startswith("blog/"))) else "") + f">{n}</a>"
        for t, n in NAV)
    header = (f'<a class="skip" href="#main">Skip to content</a><header><a class="brand" href="{link("index.html")}">{LOGO}<span>{SITE_NAME}</span></a>'
              '<button class="menu" aria-label="Menu" onclick="document.body.classList.toggle(\'open\')">☰</button>'
              f'<nav aria-label="Main">{navhtml}</nav></header>')

    main = ['<main id="main">']
    if crumbs:
        main.append('<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(
            f'<a href="{link("index.html") if n == "Home" else ("/blog/" if n == "Blog" else "")}">{html.escape(n)}</a>' if i < len(crumbs) - 1
            else f'<span aria-current="page">{html.escape(n)}</span>' for i, (n, u) in enumerate(crumbs)) + "</nav>")
    if p.get("h1") and typ != "home":
        main.append(f'<h1>{html.escape(p["h1"])}</h1>')
    if typ in ("article", "blog"):
        main.append(f'<p class="meta">By the {SITE_NAME} team · Last updated <time datetime="{p["updated"]}">{human_date(p["updated"])}</time></p>')
    main.append(body)
    if p["related"]:
        lis = "".join(f'<li><a href="/{r}">{html.escape(pages_by_slug[r]["label"])}</a></li>' for r in p["related"])
        main.append(f'<aside class="card related"><h2>Keep reading</h2><ul>{lis}</ul></aside>')
    if p["source"]:
        lis = "".join(f'<li><a href="{html.escape(u)}" rel="noopener">{html.escape(l)}</a></li>' for l, u in p["source"])
        main.append(f'<section class="card sources" id="sources"><h2>Sources</h2><ol>{lis}</ol></section>')
    if typ in ("article", "blog"):
        main.append('<p class="note">General education, not veterinary advice. If you are worried about your cat, contact your veterinarian; in an emergency, go to the nearest emergency vet.</p>')
    main.append("</main>")

    footer = (f'<footer><section class="contact-us" id="contact-us" aria-labelledby="contact-us-h"><h2 id="contact-us-h">Contact us</h2>'
              f'<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use our <a href="{link("contact.html")}">contact form</a>.</p></section>'
              f'<p>{SITE_NAME}: original educational content about cats. All text and illustrations are original. Not a substitute for veterinary care.</p>'
              f'<p class="llc">Operated by {LEGAL}</p>'
              f'<p><a href="{link("about.html")}">About</a> · <a href="{link("contact.html")}">Contact</a> · <a href="{link("privacy.html")}">Privacy</a> · <a href="{link("blog/")}">Blog</a></p>'
              f'<p>© 2026 Joshua Israel</p></footer>')
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
    info = [by_slug[s] for s in ("about.html", "contact.html", "privacy.html") if s in by_slug]
    breeds_anchor = by_slug.get("breeds.html", {}).get("anchors", "").replace("{{SITE}}", SITE_URL)
    llms = [f"# {SITE_NAME}", "",
            f"> {SITE_NAME} is a free, original, plain language guide to cats for owners and future owners: cat breeds and their inherited health risks, everyday care, health warning signs and emergencies, behavior and body language, nutrition, kittens and senior cats. Every guide answers the main question first and cites veterinary sources such as the Cornell Feline Health Center, AAFP, AAHA, International Cat Care and UC Davis. Operated by {LEGAL}.",
            "", "The content is general education, not veterinary advice.", "", "## Guides"]
    for p in guides:
        llms.append(line(p))
        if p["slug"] == "breeds.html" and breeds_anchor:
            llms.append("  - Breed sections: " + breeds_anchor)
    llms += ["", "## Tools"] + [line(p) + " (searchable table with a stable #anchor per item)" for p in tools]
    llms += ["", "## Blog"] + [line(p) for p in posts] + ["", "## Optional"] + [line(p) for p in info]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(llms) + "\n")
    open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w").write(INDEXNOW_KEY)
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    print(f"built {len(pages)} pages, {len(indexable)} in sitemap")


if __name__ == "__main__":
    main()
