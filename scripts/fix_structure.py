import os
import re

def fix_chapter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove generic Quick Reference template
    generic_qr_pattern = re.compile(
        r'## Quick Reference\s*\n\s*\n'
        r'\| Topic \| Recommendation \|\s*\n'
        r'\|-+\|-+\|\s*\n'
        r'\| Primary strategy \| Prefer the method with proven bounds for your workload\. \|\s*\n'
        r'\| Data size \| Benchmark with realistic input distributions\. \|\s*\n'
        r'\| Memory behavior \| Favor contiguous layouts where possible\. \|\s*\n?',
        re.MULTILINE
    )
    new_content = generic_qr_pattern.sub('', content)

    # Required sections
    required_sections = [
        "Definition",
        "Background & Philosophy",
        "Use Cases",
        "Memory Mechanics",
        "Operations & Complexity",
        "Idiomatic Go Implementation",
        "Decision Matrix",
        "Edge Cases & Pitfalls",
        "Anti-Patterns",
        "Quick Reference",
        "See Also"
    ]

    # Enhanced detection logic
    found_sections = {}
    for section in required_sections:
        # Check for header
        header_pattern = re.compile(rf'^##+ (?:[\d\.]+\s+)?{re.escape(section)}', re.MULTILINE | re.IGNORECASE)
        if header_pattern.search(new_content):
            found_sections[section] = True
            continue
        
        # Check for bold label (especially for top 4)
        if section in ["Definition", "Background & Philosophy", "Use Cases", "Memory Mechanics"]:
            label_pattern = re.compile(rf'^\*\*{re.escape(section)}:\*\*', re.MULTILINE | re.IGNORECASE)
            if label_pattern.search(new_content):
                found_sections[section] = True
                continue
        
        # Special check for "Operations & Complexity" which might be "Complexity Analysis"
        if section == "Operations & Complexity":
            if re.search(r'^##+ (?:[\d\.]+\s+)?Complexity Analysis', new_content, re.MULTILINE | re.IGNORECASE):
                found_sections[section] = True
                continue

    # 2. Cleanup previous placeholders if any (to avoid duplicates from previous run)
    for section in required_sections:
        placeholder_pattern = re.compile(rf'\n## {re.escape(section)}\n\n\[Placeholder for {section}\]\n', re.MULTILINE)
        new_content = placeholder_pattern.sub('', new_content)

    # 3. Insertion logic
    lines = new_content.split('\n')
    see_also_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^##+ (?:[\d\.]+\s+)?See Also', line, re.IGNORECASE):
            see_also_idx = i
            break
    
    missing_sections = [s for s in required_sections if s not in found_sections]
    
    if not missing_sections:
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False

    # Add missing sections before "See Also" or at the end
    added_content = ""
    for section in missing_sections:
        if section == "See Also": continue
        added_content += f"\n## {section}\n\n[Placeholder for {section}]\n"

    if see_also_idx != -1:
        # Move See Also to end if we are appending
        see_also_block = '\n'.join(lines[see_also_idx:])
        content_before = '\n'.join(lines[:see_also_idx])
        new_content = content_before + added_content + "\n" + see_also_block
    else:
        new_content = '\n'.join(lines) + added_content + "\n## See Also\n\n[Placeholder for See Also]\n"

    # Clean up double newlines
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

if __name__ == "__main__":
    docs_dir = "dsag/content/en/docs"
    changed_count = 0
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.startswith("Chapter-") and file.endswith(".md"):
                if fix_chapter(os.path.join(root, file)):
                    changed_count += 1
    print(f"Processed {changed_count} files for structural integrity (Pass 2).")
