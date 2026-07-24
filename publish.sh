#!/usr/bin/env bash
# BTT web publish helper. Run from this dir: ./publish.sh "commit message"
set -e
cd "$(dirname "$0")"

# 1) refresh data from Supabase public view (read-only, anon) into web/data/projects.json
python3 scripts/fetch_data.py

# 2) build static site
npm run build

# 3) commit + push
git add -A
git commit -q -m "${1:-update btt web}" || echo "nothing to commit"
git push -u origin main

# 4) trigger Vercel deploy (build reads SUPABASE_ANON_KEY env, regenerates data, builds)
curl -s -o /dev/null -w "Deploy Hook: %{http_code}\n" -X POST "https://api.vercel.com/v1/integrations/deploy/prj_iWMjFGMt4i0uCPN55pB6aE8BN9WB/weAf2YKo0V"

echo "PUSHED + DEPLOY TRIGGERED. Remote (no token stored in repo):"
git remote get-url origin
