#!/usr/bin/env python3
"""BTT web build step: compile content/research/*.md into data/research.json.

Each research article is a markdown file with small frontmatter:
  status: published|draft
  title: ...
  slug: ...
  date: ...
  summary: ...

Body is the article markdown. Only status=published is exposed on the web.
"""
import json, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(HERE, "content", "research")
OUT = os.path.join(HERE, "data", "research.json")


def load_research():
    items = []
    if not os.path.isdir(RESEARCH_DIR):
        return items
    for name in sorted(os.listdir(RESEARCH_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(RESEARCH_DIR, name)
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        fm = {}
        body = raw
        m = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", raw, re.S)
        if m:
            fm_text, body = m.group(1), m.group(2)
            for line in fm_text.splitlines():
                mm = re.match(r"^([A-Za-z_]+):\s?(.*)$", line)
                if mm:
                    value = mm.group(2).strip()
                    if value.startswith('"') and value.endswith('"') and len(value) > 1:
                        value = value[1:-1]
                    fm[mm.group(1).lower()] = value
        slug = fm.get("slug") or name[:-3]
        title = fm.get("title") or slug.replace("-", " ").title()
        status = (fm.get("status") or "draft").lower()
        date = (fm.get("date") or "").strip()
        summary = fm.get("summary") or ""
        items.append({
            "slug": slug,
            "title": title,
            "status": status,
            "date": date,
            "summary": summary,
            "body": body.strip(),
        })
    items.sort(key=lambda x: x.get("date") or "", reverse=True)
    return items


def main():
    items = load_research()
    published = [i for i in items if i.get("status") == "published"]
    out = {
        "count": len(items),
        "published_count": len(published),
        "items": items,
        "published": published,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(items)} research item(s) ({len(published)} published) to {OUT}")


if __name__ == "__main__":
    main()
