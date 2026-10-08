#!/usr/bin/env bash
# Ping IndexNow for MeowWise. Usage: ./indexnow.sh URL [URL...]  (no args = all sitemap URLs)
# BASE must match SITE_URL in _build.py. The key file lives at ${BASE}${KEY}.txt
KEY=fbe2e797c1db901fb91646b40e01856f
BASE=https://joshuaofisrael.github.io/meowwise/
HOST=$(echo "$BASE" | sed -E 's#https?://([^/]+)/.*#\1#')
if [ $# -eq 0 ]; then set -- $(curl -s "${BASE}sitemap.xml" | grep -o '<loc>[^<]*' | sed 's/<loc>//'); fi
LIST=$(printf '%s\n' "$@" | python3 -c 'import sys,json;print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')
curl -s -o /dev/null -w "IndexNow HTTP %{http_code} ($# URLs)\n" -X POST https://api.indexnow.org/indexnow \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d "{\"host\":\"$HOST\",\"key\":\"$KEY\",\"keyLocation\":\"${BASE}${KEY}.txt\",\"urlList\":$LIST}"
