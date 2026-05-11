# AGENTS.md — DSAG Book Development Guide

## Project Overview

This is a Hugo-based static site for "Modern Data Structures and Algorithms in Go" (DSAG).
- **Framework:** Hugo v0.161+ with custom theme
- **Language:** Go (for code examples), Markdown (for content)
- **Build:** `hugo --quiet` or `hugo server --port 1313`
- **Repository:** `https://github.com/akmalgomal3/dsag-webbook.git`

## Book Structure

The book contains **60 chapters** organized into **12 parts**:

| Part | Title | Chapters | Description |
|------|-------|----------|-------------|
| **Part I** | Foundations & Go Mechanics | 1–4 | Complexity, Go basics, fundamentals |
| **Part II** | Basic Data Structures | 5–8 | Arrays, slices, linked lists, hashing |
| **Part III** | Trees, Graphs & Representations | 9–12 | BST, heaps, disjoint sets, graphs |
| **Part IV** | Graph Algorithms | 13–18 | Traversal, shortest paths, MST, flows |
| **Part V** | Sorting & Searching | 19–22 | Sorting algorithms, search techniques |
| **Part VI** | Algorithmic Paradigms | 23–28 | DP, greedy, backtracking, divide & conquer |
| **Part VII** | Advanced Topics | 29–39 | Parallel, crypto, blockchain, tries, bit manipulation |
| **Part VIII** | History & Philosophy | 40–44 | Origins of algorithms, complexity theory, philosophy |
| **Part IX** | Advanced Data Structures | 45–50 | B-trees, skip lists, Bloom filters, LRU, suffix arrays, persistent DS |
| **Part X** | Advanced Graph Algorithms | 51–54 | Topological sort, SCC, A*, bridge-finding |
| **Part XI** | Specialized Sorting & Techniques | 55–57 | Counting/radix/bucket sort, sliding window, Kadane's |
| **Part XII** | Advanced Topics | 58–60 | Minimax, Mo's algorithm, convex hull |

## Chapter Writing Style Guide

### Core Philosophy

**Brevity over verbosity.** Each chapter should be readable in 7–10 minutes. A software engineer should finish a chapter with:
1. Clear intuition of how the data structure/algorithm works
2. Knowledge of when to use it (and when NOT to)
3. Ability to implement it idiomatically in Go
4. Awareness of edge cases and Go-specific pitfalls

### Chapter Template (MUST FOLLOW)

Every chapter MUST follow this structure:

```markdown
---
weight: <chapter_weight>
title: "Chapter <N> - <Description>"
description: "<Short description>"
icon: "article"
date: "2024-08-24T..."
lastmod: "2024-08-24T..."
draft: false
toc: true
katex: true
---

## <N>.<M>. <Topic Name>

**Definition:** 1-2 kalimat yang jelas dan actionable. Contoh:
> "Stack adalah struktur data LIFO (Last-In-First-Out) -- elemen terakhir masuk adalah pertama keluar."

**Background & Philosophy:** 2-4 sentences covering the rationale, design philosophy, or historical motivation. Why does this structure/algorithm exist? What problem does it solve at a conceptual level? Part VIII chapters will expand on history; keep it intuition-focused elsewhere.

**Use Cases:** 2-3 sentences describing practical scenarios where this structure/algorithm shines (and when it doesn't). Connect to real engineering decisions.

**Memory Mechanics:** 2-4 sentences explaining how this structure/algorithm behaves in memory (CPU cache, heap allocations, pointer chasing, spatial/temporal locality, Go GC implications). Every chapter MUST include this -- it is the unique value proposition of the DSAG book.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Op1     | O(...)       | Penjelasan singkat |

### Idiomatic Go Implementation

- Gunakan `[]T` (slice) untuk dynamic arrays
- Gunakan `container/list` untuk linked list
- Gunakan `container/heap` untuk heap
- Gunakan `sync.Mutex` untuk concurrency
- Gunakan `strings.Builder` untuk string building
- Gunakan `math/bits` untuk bitwise operations
- Hindari pseudocode yang redundan -- langsung ke Go
- Hindari kode dari bahasa lain (JANGAN pakai `Vec<T>`, `impl`, `let mut`, dll)

### Decision Matrix (RECOMMENDED)

| Use This When... | Avoid If... |
|---------------------|------------------|
| ...                 | ...              |

*Not all chapters need a formal Decision Matrix section. If the trade-offs are obvious from context, skip it or fold into Use Cases.*

### Edge Cases & Pitfalls (RECOMMENDED)

- **Case 1:** Deskripsi singkat
- **Case 2:** Deskripsi singkat

*Focus on Go-specific pitfalls (nil dereferences, GC pressure, integer overflow, slice aliasing). Anti-patterns are folded into this section or into Idiomatic Go Implementation alerts.*

### Quick Reference (format flexible)

Table format varies per chapter. Common columns: Name | Go Type | Time | Space | Use Case. May appear as `##` (H2) or `###` (H3) depending on chapter flow.

| Name | Go Type | Complexity | Use Case |
|------|---------|-----------|----------|
| ...  | ...     | ...       | ...      |
```

### Rules

1. **NO redundant pseudocode** — pseudocode hanya untuk konsep non-trivial
2. **NO language mixing** — kode harus Go idiomatik, bukan Rust/C++/Python yang di-relabel
3. **NO verbose narratives** — maksimal 1 paragraf per konsep
4. **Background & Philosophy is REQUIRED** — 2-4 sentences per section, focus on intuition and rationale. Part VIII chapters may expand to full historical treatment.
5. **NO mathematical proofs** — intuisi > proof
6. **Decision Matrix is RECOMMENDED** — include when trade-offs are non-obvious; skip when context makes them clear
7. **MUST include Go stdlib references** — `container/heap`, `sync.Map`, dsb.
8. **Anti-patterns section is OPTIONAL** — flag common Go mistakes inline in Edge Cases & Pitfalls or as alerts in Idiomatic Go Implementation. Do NOT create a standalone section unless a chapter specifically needs it.
9. **MUST include Big-O table** — minimal untuk operasi utama
10. **Code max 40 lines** per block — jika lebih, split menjadi fungsi terpisah

### Frontmatter

```yaml
---
weight: <chapter_weight>
# Format: Part_N * 10000 + chapter_in_part * 100
# Part index: N * 10000
# Part I: 10000-10400, Part II: 20000-20400, Part III: 30000-30400
# Part IV: 40000-40600, Part V: 50000-50400, Part VI: 60000-60600
# Part VII: 70000-71100, Part VIII: 80000-80500
# Part IX: 90000-90600, Part X: 100000-100400
# Part XI: 110000-110300, Part XII: 120000-120300
title: "Chapter <N> - <Description>"
description: "<One-line description>"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---
```

### Alerts

Gunakan alert sesuai konteks:
- `{{% alert icon="💡" context="info" %}}` — Definisi, insight
- `{{% alert icon="📌" context="warning" %}}` — Anti-pattern, pitfall
- `{{% alert icon="🎯" context="success" %}}` — Key takeaway, summary

## Build & Deploy

```bash
# Build (with minification)
hugo --minify --quiet

# Development server
hugo server --port 1313
```

## Content Directory Structure

```
content/
├── _index.md                              # Landing page
└── en/
    └── docs/
        ├── Preface.md
        ├── Foreword.md
        ├── Foreword-2.md
        ├── Table-of-Contents.md
        ├── how-to-use-dsag.md
        ├── closing-remark.md
        ├── appendix.md
        ├── Part-I/           # Ch 1-4
        │   ├── _index.md
        │   ├── Chapter-1.md
        │   ├── Chapter-2.md
        │   ├── Chapter-3.md
        │   └── Chapter-4.md
        ├── Part-II/          # Ch 5-8
        │   ├── _index.md
        │   ├── Chapter-5.md
        │   ├── Chapter-6.md
        │   ├── Chapter-7.md
        │   └── Chapter-8.md
        ├── Part-III/         # Ch 9-12
        │   ├── _index.md
        │   ├── Chapter-9.md
        │   ├── Chapter-10.md
        │   ├── Chapter-11.md
        │   └── Chapter-12.md
        ├── Part-IV/          # Ch 13-18
        │   ├── _index.md
        │   ├── Chapter-13.md
        │   ├── Chapter-14.md
        │   ├── Chapter-15.md
        │   ├── Chapter-16.md
        │   ├── Chapter-17.md
        │   └── Chapter-18.md
        ├── Part-V/           # Ch 19-22
        │   ├── _index.md
        │   ├── Chapter-19.md
        │   ├── Chapter-20.md
        │   ├── Chapter-21.md
        │   └── Chapter-22.md
        ├── Part-VI/          # Ch 23-28
        │   ├── _index.md
        │   ├── Chapter-23.md
        │   ├── Chapter-24.md
        │   ├── Chapter-25.md
        │   ├── Chapter-26.md
        │   ├── Chapter-27.md
        │   └── Chapter-28.md
        ├── Part-VII/         # Ch 29-39
        │   ├── _index.md
        │   ├── Chapter-29.md
        │   ├── Chapter-30.md
        │   ├── Chapter-31.md
        │   ├── Chapter-32.md
        │   ├── Chapter-33.md
        │   ├── Chapter-34.md
        │   ├── Chapter-35.md
        │   ├── Chapter-36.md
        │   ├── Chapter-37.md
        │   ├── Chapter-38.md
        │   └── Chapter-39.md
        ├── Part-VIII/        # Ch 40-44
        │   ├── _index.md
        │   ├── Chapter-40.md
        │   ├── Chapter-41.md
        │   ├── Chapter-42.md
        │   ├── Chapter-43.md
        │   └── Chapter-44.md
        ├── Part-IX/          # Ch 45-50
        │   ├── _index.md
        │   ├── Chapter-45.md
        │   ├── Chapter-46.md
        │   ├── Chapter-47.md
        │   ├── Chapter-48.md
        │   ├── Chapter-49.md
        │   └── Chapter-50.md
        ├── Part-X/           # Ch 51-54
        │   ├── _index.md
        │   ├── Chapter-51.md
        │   ├── Chapter-52.md
        │   ├── Chapter-53.md
        │   └── Chapter-54.md
        ├── Part-XI/          # Ch 55-57
        │   ├── _index.md
        │   ├── Chapter-55.md
        │   ├── Chapter-56.md
        │   └── Chapter-57.md
        └── Part-XII/         # Ch 58-60
            ├── _index.md
            ├── Chapter-58.md
            ├── Chapter-59.md
            └── Chapter-60.md
```

## Common Issues

### Hugo Shortcode Corruption
If you see errors like:
```
unclosed shortcode
closing tag for shortcode 'alert' does not match start tag
```

Check for corrupted closing tags. The correct format is:
```
{{% /alert %}}
```

Common corruptions:
- `{{% /alert %}}` → has CJK characters replacing `%`
- `{{% /alert %}} %}}` → extra trailing `%}}`
- `{{% /alert %}})}}` → extra `)}` after close
- `{{%/alert%}}` → missing spaces
- `{{% /alert %}` → missing closing brace

### Empty Content Crash
If Hugo crashes with:
```
slice bounds out of range [:XXXX] with capacity 512
```

Add a minimal placeholder to the markdown body:
```markdown
---
...
---

<!-- empty -->
```

### Missing Part Section
If a Part does not appear in sidebar or TOC, check that the Part directory has an `_index.md` file with proper frontmatter:
```yaml
---
weight: <part_weight>  # e.g., 6000 for Part VI
title: "Part VI - <Title>"
---
```

## Checklist Before Committing

- [ ] Hugo builds without errors (`hugo --quiet`)
- [ ] No corrupted shortcode tags
- [ ] Code is idiomatic Go (not Rust/Python/C++)
- [ ] Chapter follows the template structure (Definition, Background & Philosophy, Use Cases, Memory Mechanics, Operations & Complexity, Idiomatic Go Implementation)
- [ ] Decision matrix included (if trade-offs are non-obvious)
- [ ] Big-O table included
- [ ] Edge cases listed (Go-specific pitfalls covered)
- [ ] Go stdlib references included
- [ ] No empty content without placeholder
- [ ] Chapter title format: `Chapter N - [Description]`
- [ ] Weight follows part numbering convention
- [ ] Summary alert icon="🎯" context="success" included
