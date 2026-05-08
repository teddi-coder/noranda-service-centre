#!/usr/bin/env python3
"""
Remove #promo section and all promo-related CSS from every .html file.
Run from any directory — uses absolute paths.
"""
import re
import os
import glob

ROOT = '/Volumes/KINGSTON/noranda-service-centre'

# Match <section id="promo" ...> ... </section> (non-greedy won't work with DOTALL
# because "promo" section may contain nested <section> tags — but looking at the HTML
# these promo sections have no nested <section> tags, so a greedy match up to first
# </section> after the opening tag is fine. We use a targeted pattern.
PROMO_SECTION_RE = re.compile(
    r'\n?<section id="promo"[^>]*>.*?</section>',
    re.DOTALL
)

# Match any CSS line/block referencing #promo or .promo- inside a <style> block.
# We'll remove individual lines that contain these selectors.
PROMO_CSS_LINE_RE = re.compile(
    r'[ \t]*(?:#promo|\.promo-)[^\n]*\n?'
)

# Also handle the @media block that wraps promo-grid — two forms:
# compact:  @media(max-width:768px){.promo-grid{...}}
# spaced:   @media (max-width: 768px) { .promo-grid { ... } }
PROMO_MEDIA_COMPACT_RE = re.compile(
    r'[ \t]*@media\([^)]*\)\{\.promo-grid\{[^}]*\}\}\n?'
)
PROMO_MEDIA_SPACED_RE = re.compile(
    r'[ \t]*@media\s*\([^)]*\)\s*\{\s*\.promo-grid\s*\{[^}]*\}\s*\}\n?'
)

html_files = glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True)
# Exclude macOS resource fork files (._index.html handled by glob pattern above —
# actually ._index.html won't match index.html, we're safe)

changed = []
for path in sorted(html_files):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # 1. Remove promo section HTML
    content = PROMO_SECTION_RE.sub('', content)

    # 2. Remove promo CSS lines (compact style — no spaces around braces)
    content = PROMO_CSS_LINE_RE.sub('', content)

    # 3. Remove @media promo-grid blocks (compact)
    content = PROMO_MEDIA_COMPACT_RE.sub('', content)

    # 4. Remove @media promo-grid blocks (spaced)
    content = PROMO_MEDIA_SPACED_RE.sub('', content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(path)
        print(f'  CHANGED: {path}')
    else:
        print(f'  unchanged: {path}')

print(f'\nDone. Modified {len(changed)} file(s).')
