#!/usr/bin/env python3
"""Add See Also cross-references to chapters."""
import os
import glob
import re

# Map chapter number -> list of related chapter numbers
RELATED = {
    1: [2, 3, 39],
    2: [3, 4, 32],
    3: [1, 2, 4],
    4: [2, 3, 6],
    5: [6, 7, 8],
    6: [5, 7, 47],
    7: [5, 6, 46],
    8: [5, 6, 9],
    9: [10, 11, 36],
    10: [9, 16],
    11: [9, 12, 44],
    12: [11, 13, 14],
    13: [12, 14, 15],
    14: [12, 13, 52],
    15: [13, 14, 32],
    16: [10, 17, 18],
    17: [16, 18, 32],
    18: [16, 17, 51],
    19: [20, 21, 54],
    20: [19, 21, 54],
    21: [7, 19],
    22: [23, 25, 26],
    23: [22, 24, 25],
    24: [23, 25, 35],
    25: [23, 24, 57],
    26: [22, 23, 27],
    27: [25, 26, 45],
    28: [29, 33, 38],
    29: [28, 30, 31],
    30: [29, 31, 46],
    31: [29, 30, 36],
    32: [2, 15, 28],
    33: [28, 34, 38],
    34: [33, 36, 48],
    35: [24, 27, 42],
    36: [9, 34, 48],
    37: [9, 32, 36],
    38: [28, 33, 42],
    39: [40, 41, 43],
    40: [39, 41, 42],
    41: [39, 40, 42],
    42: [40, 41, 43],
    43: [39, 40, 42],
    44: [9, 11, 46],
    45: [9, 27, 44],
    46: [7, 44, 47],
    47: [6, 7, 46],
    48: [34, 36, 49],
    49: [36, 48, 41],
    50: [12, 51, 53],
    51: [50, 52, 53],
    52: [14, 50, 51],
    53: [50, 51, 12],
    54: [19, 20, 56],
    55: [54, 56, 23],
    56: [23, 54, 55],
    57: [23, 25, 58],
    58: [54, 56, 57],
    59: [32, 52, 58],
}

# Chapter title cache
CHAPTER_TITLES = {}
for md_file in glob.glob('content/en/docs/**/Chapter-*.md', recursive=True):
    with open(md_file, 'r') as f:
        content = f.read()
    m = re.search(r'title: "Chapter (\d+) - (.+)"', content)
    if m:
        num = int(m.group(1))
        title = m.group(2)
        CHAPTER_TITLES[num] = title

def get_chapter_file(ch_num):
    for md_file in glob.glob('content/en/docs/**/Chapter-*.md', recursive=True):
        if f'Chapter-{ch_num}.md' in md_file:
            return md_file
    return None

def get_part_dir(ch_num):
    file = get_chapter_file(ch_num)
    if file:
        return os.path.dirname(file).replace('content/en/docs/', '')
    return None

for ch_num, related in RELATED.items():
    file = get_chapter_file(ch_num)
    if not file:
        continue
    
    with open(file, 'r') as f:
        content = f.read()
    
    # Check if already has See Also
    if '## See Also' in content:
        continue
    
    # Build See Also section
    links = []
    for r in related:
        if r in CHAPTER_TITLES:
            part = get_part_dir(r)
            if part:
                links.append(f'- [Chapter {r} — {CHAPTER_TITLES[r]}](/docs/{part}/Chapter-{r}/)')
    
    if not links:
        continue
    
    see_also = '\n\n## See Also\n\n' + '\n'.join(links) + '\n'
    
    # Insert before the summary alert
    # Find the last alert with summary
    summary_pattern = r'({{% alert icon="🎯" context="success" %}}.*?){{% /alert %}}'
    match = list(re.finditer(summary_pattern, content, re.DOTALL))
    if match:
        last_match = match[-1]
        end_pos = last_match.end()
        content = content[:end_pos] + see_also + content[end_pos:]
    else:
        # Append to end
        content = content.rstrip() + see_also
    
    with open(file, 'w') as f:
        f.write(content)
    
    print(f"Added See Also to Chapter {ch_num}")

print("Done.")
