#!/usr/bin/env python3
import json
import re
import os
import glob

def extract_frontmatter(content):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", content

def parse_frontmatter(fm_text):
    result = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result

def plainify(text):
    # Remove markdown syntax
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    text = re.sub(r'[#*_`~]', '', text)  # formatting
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)  # comments
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)  # shortcodes
    text = re.sub(r'\n+', ' ', text)  # newlines
    return text.strip()

index = []

for md_file in sorted(glob.glob('content/en/docs/**/*.md', recursive=True)):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm_text, body = extract_frontmatter(content)
    fm = parse_frontmatter(fm_text)
    
    if not fm.get('weight'):
        continue
    
    # Generate URL from file path
    rel_path = md_file.replace('content/en/', '').replace('.md', '/')
    url = '/' + rel_path.lower().replace('_', '-')
    
    title = fm.get('title', '')
    description = fm.get('description', '')
    
    # Get plain text content (first 500 chars)
    plain = plainify(body)[:500]
    
    index.append({
        'title': title,
        'permalink': url,
        'summary': description or plain[:200],
        'content': plain
    })

# Sort by chapter number
def ch_num(entry):
    m = re.search(r'Chapter (\d+)', entry['title'])
    return int(m.group(1)) if m else 999

index.sort(key=ch_num)

os.makedirs('static', exist_ok=True)
with open('static/search.json', 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"Generated search.json with {len(index)} entries")
