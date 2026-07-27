#!/usr/bin/env python3
"""BTT web build step: compile content/pulse/pulse.md into data/pulse.json.

Each pulse entry is separated by a line with only '---' and uses a small
frontmatter block (key: value). Example:

---
type: signal
project: Arcus
date: 2026-07-27
text: Arcus added a new CLOB partner; on-chain liquidity improved noticeably.
---

The 'project' field accepts a project name or slug; it is normalized to the
canonical slug from data/projects.json when possible. 'type' is one of
signal | insight | question | note. Entries without text are skipped.
"""
import json, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PULSE_MD = os.path.join(HERE, "content", "pulse", "pulse.md")
PROJECTS_JSON = os.path.join(HERE, "data", "projects.json")
OUT = os.path.join(HERE, "data", "pulse.json")

VALID_TYPES = {"signal", "insight", "question", "note"}


def load_slug_map():
    """name (lower) or slug -> canonical slug."""
    m = {}
    if os.path.exists(PROJECTS_JSON):
        with open(PROJECTS_JSON) as f:
            data = json.load(f)
        for p in data.get("projects", []):
            row = p.get("project_row", {})
            slug = (row.get("slug") or "").lower()
            name = (row.get("name") or "").lower()
            if slug:
                m[slug] = slug
            if name:
                m[name] = slug
    return m


def normalize_slug(project, slug_map):
    if not project:
        return ""
    key = project.strip().lower()
    if key in slug_map:
        return slug_map[key]
    # try partial match on name/slug containing the token
    for k, v in slug_map.items():
        if key in k or k in key:
            return v
    return project.strip().lower().replace(" ", "-")


def parse_entries(text):
    # split on lines that are exactly '---'
    blocks = re.split(r"(?m)^---\s*$", text)
    entries = []
    for blk in blocks:
        blk = blk.strip()
        if not blk:
            continue
        # skip blocks that look like doc comments / headings (no real entry)
        first = blk.splitlines()[0].strip() if blk.splitlines() else ""
        if first.startswith("#"):
            continue
        # parse simple 'key: value' lines at the top until blank line
        fm = {}
        body_lines = []
        in_fm = True
        for line in blk.splitlines():
            if in_fm:
                mm = re.match(r"^([A-Za-z_]+):\s?(.*)$", line)
                if mm:
                    fm[mm.group(1).lower()] = mm.group(2).strip()
                    continue
                else:
                    in_fm = False
            body_lines.append(line)
        # any remaining text after frontmatter = text (if 'text' not given)
        body = "\n".join(body_lines).strip()
        entry = dict(fm)
        if not entry.get("text") and body:
            entry["text"] = body
        if entry.get("text"):
            entries.append(entry)
    return entries


def main():
    slug_map = load_slug_map()
    if not os.path.exists(PULSE_MD):
        out = {"count": 0, "pulse": []}
        with open(OUT, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print("No pulse.md found; wrote empty pulse.json")
        return

    with open(PULSE_MD) as f:
        raw = f.read()
    parsed = parse_entries(raw)
    # newest-appended (bottom of file) should surface first; stable sort below
    # keeps this order for entries that share the same date.
    parsed.reverse()
    out_items = []
    for i, e in enumerate(parsed):
        ptype = (e.get("type") or "note").lower()
        if ptype not in VALID_TYPES:
            ptype = "note"
        slug = normalize_slug(e.get("project"), slug_map)
        date = (e.get("date") or "").strip()
        text = " ".join((e.get("text") or "").split())
        # extract a trailing "Source: <url>" into a clickable source_url field
        m = re.search(r"(?i)\bsource:\s*(https?://\S+)\s*$", text)
        source_url = ""
        if m:
            source_url = m.group(1)
            text = text[:m.start()].strip()
        pid = f"{slug or 'p'}-{date or 'nd'}-{i+1}"
        out_items.append({
            "id": pid,
            "type": ptype,
            "project_slug": slug,
            "project": e.get("project", ""),
            "date": date,
            "text": text,
            "source_url": source_url,
        })
    # sort by date desc (newest first), entries without date last;
    # equal dates keep the reversed (newest-appended-first) order
    out_items.sort(key=lambda x: x["date"] or "0000-00-00", reverse=True)
    out = {"count": len(out_items), "pulse": out_items}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(out_items)} pulse item(s) to {OUT}")


if __name__ == "__main__":
    main()
