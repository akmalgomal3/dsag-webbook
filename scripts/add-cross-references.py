#!/usr/bin/env python3
"""Add See Also cross-references to chapters."""
import os
import glob
import re

# Map chapter number -> list of related chapter numbers
RELATED = {
    1: [2, 3, 40],
    2: [3, 4, 33],
    3: [1, 2, 4],
    4: [2, 3, 6],
    5: [6, 7, 8],
    6: [5, 7, 48],
    7: [5, 6, 47],
    8: [5, 6, 9],
    9: [10, 11, 37],
    10: [9, 16, 22],
    11: [9, 12, 45],
    12: [11, 13, 14],
    13: [12, 14, 15],
    14: [12, 13, 53],
    15: [13, 14, 33],
    16: [10, 17, 18],
    17: [16, 18, 33],
    18: [16, 17, 52],
    19: [20, 21, 55],
    20: [19, 21, 55],
    21: [7, 19, 22],
    22: [10, 21, 33],
    23: [24, 26, 27],
    24: [23, 25, 26],
    25: [24, 26, 36],
    26: [24, 25, 58],
    27: [23, 24, 28],
    28: [26, 27, 46],
    29: [30, 34, 39],
    30: [29, 31, 32],
    31: [30, 32, 47],
    32: [30, 31, 37],
    33: [2, 15, 29],
    34: [29, 35, 39],
    35: [34, 37, 49],
    36: [25, 28, 43],
    37: [9, 35, 49],
    38: [9, 33, 37],
    39: [29, 34, 43],
    40: [41, 42, 44],
    41: [40, 42, 43],
    42: [40, 41, 43],
    43: [41, 42, 44],
    44: [40, 41, 43],
    45: [9, 11, 47],
    46: [9, 28, 45],
    47: [7, 45, 48],
    48: [6, 7, 47],
    49: [35, 37, 50],
    50: [37, 49, 42],
    51: [12, 52, 54],
    52: [51, 53, 54],
    53: [14, 51, 52],
    54: [51, 52, 12],
    55: [19, 20, 57],
    56: [55, 57, 24],
    57: [24, 55, 56],
    58: [24, 26, 59],
    59: [55, 57, 58],
    60: [33, 53, 59],
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
