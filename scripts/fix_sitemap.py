#!/usr/bin/env python3
"""Fix sitemap: create single sitemap.xml from sitemap-0.xml for Google compatibility.
@astrojs/sitemap creates sitemap-index.xml by default, but Google expects /sitemap.xml
The sitemap-index.xml contains links to sitemap-0.xml, sitemap-1.xml, etc.
We need to copy sitemap-0.xml content to sitemap.xml (works when only one sitemap file).
"""
import os
import shutil

# Script is in 03-Web/web/scripts/, dist is in 03-Web/web/dist/
# So we need to go up one level from scripts/ to web/ then into dist/
HERE = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(HERE, "..", "dist")

# Find the first sitemap file (sitemap-0.xml, sitemap-1.xml, etc.)
def find_first_sitemap():
    for i in range(100):  # Check sitemap-0.xml through sitemap-99.xml
        candidate = os.path.join(DIST_DIR, f"sitemap-{i}.xml")
        if os.path.exists(candidate):
            return candidate
    return None

def main():
    first_sitemap = find_first_sitemap()
    if not first_sitemap:
        print(f"✗ No sitemap-*.xml found in {DIST_DIR}")
        print(f"  Run 'npm run build' first")
        return
    
    sitemap_main = os.path.join(DIST_DIR, "sitemap.xml")
    shutil.copy(first_sitemap, sitemap_main)
    
    num = first_sitemap.split("-")[-1].replace(".xml", "")
    print(f"✓ Fixed sitemap: created {sitemap_main}")
    print(f"  (copied from {os.path.basename(first_sitemap)})")
    print(f"\n  Next steps:")
    print(f"  1. Run: npm run build")
    print(f"  2. Run: ./publish.sh 'fix sitemap'")
    print(f"  3. In Google Search Console, test: https://beforethetoken.vercel.app/sitemap.xml")

if __name__ == "__main__":
    main()