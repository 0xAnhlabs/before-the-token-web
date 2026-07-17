#!/usr/bin/env bash
# BTT web publish helper. Run from this dir: ./publish.sh "commit message"
set -e
cd "$(dirname "$0")"

# 1) refresh data from Supabase public view (read-only, anon)
python3 "../../scripts/btt_build.py"
cp "../build/projects.json" data/projects.json

# 2) build static site
npm run build

# 3) commit + push
git add -A
git commit -q -m "${1:-update btt web}" || echo "nothing to commit"
git push -u origin main

echo "PUSHED. Remote (no token stored in repo):"
git remote get-url origin
