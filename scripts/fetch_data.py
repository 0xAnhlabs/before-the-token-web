#!/usr/bin/env python3
"""BTT web build step: pull published projects from Supabase view (read-only, anon key)
and emit data/projects.json. Runs on Vercel at build time (env SUPABASE_ANON_KEY)
and locally (falls back to the operator .env). No DB writes. Safe to rerun.
"""
import json, os, sys, urllib.request, urllib.parse

PROJECT_REF = "gtbxhctyrkezetkkdydv"
BASE = f"https://{PROJECT_REF}.supabase.co/rest/v1/btt_public_projects"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "projects.json")
LOCAL_ENV = "/Users/trananh/.hermes/profiles/btt_operator/.env"


def load_anon():
    # 1) env var (Vercel)
    v = os.environ.get("SUPABASE_ANON_KEY")
    if v:
        return v
    # 2) local operator .env fallback
    if os.path.exists(LOCAL_ENV):
        with open(LOCAL_ENV) as f:
            for line in f:
                line = line.strip()
                if line.startswith("SUPABASE_ANON_KEY") and "=" in line:
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SUPABASE_ANON_KEY not found in env or local .env")


def fetch_all(anon):
    rows, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "select": "*", "order": "name.asc",
            "limit": "1000", "offset": str(offset),
        })
        req = urllib.request.Request(f"{BASE}?{q}", headers={
            "apikey": anon, "Authorization": f"Bearer {anon}",
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            chunk = json.loads(r.read().decode())
        if not chunk:
            break
        rows.extend(chunk)
        if len(chunk) < 1000:
            break
        offset += 1000
    return rows


def build_project_row(row):
    return {
        "name": row.get("name", ""), "slug": row.get("slug", ""),
        "category": row.get("category", ""), "ecosystem": row.get("ecosystem", "") or "",
        "product_stage": row.get("product_stage", ""),
        "activity_status": row.get("activity_status", ""),
        "token_status": row.get("token_status", ""),
        "funding_summary": row.get("funding_summary", "") or "",
        "key_backers": row.get("key_backers", "") or "",
        "note": row.get("note", "") or "",
        "website_url": (row.get("website_url", "") or "").strip(),
        "x_url": (row.get("x_url", "") or "").strip(),
    }


def main():
    anon = load_anon()
    rows = fetch_all(anon)
    out = {"generated_from": "btt_public_projects", "count": len(rows), "projects": []}
    for row in rows:
        content = row.get("content") or {}
        out["projects"].append({
            "project_row": build_project_row(row),
            "revision_meta": {
                "revision_id": row.get("revision_id"),
                "revision_number": row.get("revision_number"),
                "schema_version": row.get("schema_version"),
                "taxonomy_version": row.get("taxonomy_version"),
                "published_at": row.get("published_at"),
                "updated_at": row.get("updated_at"),
            },
            "revision_content": content,
        })
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(rows)} project(s) to {OUT}")


if __name__ == "__main__":
    main()
