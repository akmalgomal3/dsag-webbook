#!/usr/bin/env python3
"""Verify Go code blocks in chapters compile."""
import os
import re
import subprocess
import tempfile
import glob

BASE = "content/en/docs"
results = {"ok": 0, "skip": 0, "fail": 0, "errors": [], "skip_reasons": {}}

for md_file in glob.glob(f"{BASE}/**/Chapter-*.md", recursive=True):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all Go code blocks
    code_blocks = re.findall(r'```go(.*?)```', content, re.DOTALL)
    
    for i, code in enumerate(code_blocks):
        code = code.strip()
        if not code:
            continue
        
        # Skip if it's clearly a snippet (no package main and no package declaration)
        # or has obvious placeholder text
        if "package main" not in code and "package " not in code:
            results["skip"] += 1
            results["skip_reasons"]["no_package_decl"] = results["skip_reasons"].get("no_package_decl", 0) + 1
            continue
        if "placeholder" in code.lower():
            results["skip"] += 1
            results["skip_reasons"]["placeholder"] = results["skip_reasons"].get("placeholder", 0) + 1
            continue
        if "golang.org/x/" in code:
            results["skip"] += 1
            results["skip_reasons"]["external_module"] = results["skip_reasons"].get("external_module", 0) + 1
            continue
        if "package main" in code and "func main(" not in code:
            code += "\n\nfunc main() {}\n"
        
        # Try to compile
        with tempfile.TemporaryDirectory() as tmpdir:
            main_file = os.path.join(tmpdir, "main.go")
            with open(main_file, "w") as f:
                f.write(code)
            
            result = subprocess.run(
                ["go", "build", "-o", "/dev/null", main_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                results["ok"] += 1
            else:
                results["fail"] += 1
                rel = os.path.relpath(md_file, BASE)
                results["errors"].append(f"{rel} block {i+1}: {result.stderr.strip()[:120]}")

print(f"Compile OK:   {results['ok']}")
print(f"Skipped:      {results['skip']}")
print(f"Failed:       {results['fail']}")
if results["skip_reasons"]:
    print("\nSkip reasons:")
    for reason, count in sorted(results["skip_reasons"].items()):
        print(f"  - {reason}: {count}")
if results["errors"]:
    print("\nErrors:")
    for err in results["errors"][:10]:
        print(f"  - {err}")
    if len(results["errors"]) > 10:
        print(f"  ... and {len(results['errors']) - 10} more")
