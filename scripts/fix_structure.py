#!/usr/bin/env python3
import os
import re
import glob

BASE = "content/en/docs"

# Map part number to chapters
PART_CHAPTERS = {
    1: [1,2,3,4],
    2: [5,6,7,8],
    3: [9,10,11,12],
    4: [13,14,15,16,17,18],
    5: [19,20,21],
    6: [22,23,24,25,26,27],
    7: [28,29,30,31,32,33,34,35,36,37,38],
    8: [39,40,41,42,43],
    9: [44,45,46,47,48,49],
    10: [50,51,52,53],
    11: [54,55,56],
    12: [57,58,59],
}

for part_num, chapters in PART_CHAPTERS.items():
    part_dir = f"Part-{['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII'][part_num-1]}"
    part_path = os.path.join(BASE, part_dir)
    
    if not os.path.exists(part_path):
        print(f"SKIP: {part_path} not found")
        continue
    
    # Fix _index.md
    index_file = os.path.join(part_path, "_index.md")
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            content = f.read()
        
        # Fix weight
        content = re.sub(r'^weight:\s*\d+', f'weight: {part_num * 10000}', content, flags=re.MULTILINE)
        
        # Fix title format: "Part VIII: Title" -> "Part VIII - Title"
        # Match Roman numeral or digit after "Part "
        content = re.sub(
            r'title:\s*"Part\s+([IVX]+|\d+):\s*',
            f'title: "Part {part_num} - ',
            content
        )
        
        with open(index_file, 'w') as f:
            f.write(content)
        print(f"FIXED: {index_file}")
    
    # Fix chapters
    for i, ch_num in enumerate(chapters, start=1):
        ch_file = os.path.join(part_path, f"Chapter-{ch_num}.md")
        if not os.path.exists(ch_file):
            print(f"MISSING: {ch_file}")
            continue
        
        with open(ch_file, 'r') as f:
            content = f.read()
        
        # Fix weight
        new_weight = part_num * 10000 + i * 100
        content = re.sub(r'^weight:\s*\d+', f'weight: {new_weight}', content, flags=re.MULTILINE)
        
        # Add katex: true if missing
        if 'katex:' not in content:
            content = re.sub(r'^(toc:\s*true)\s*$', r'\1\nkatex: true', content, flags=re.MULTILINE)
            print(f"  +KATEX: {ch_file}")
        
        with open(ch_file, 'w') as f:
            f.write(content)
        print(f"FIXED: {ch_file} -> weight {new_weight}")

print("\nDone.")
