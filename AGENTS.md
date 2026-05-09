# AGENTS.md — DSAG Book Development Guide

## Project Overview

This is a Hugo-based static site for "Modern Data Structures and Algorithms in Go" (DSAG).
- **Framework:** Hugo v0.161+ with Docsy-like theme
- **Language:** Go (for code examples), Markdown (for content)
- **Build:** `hugo --quiet` or `hugo server --port 1313`

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
weight: <chapter_number>00
title: "Chapter <N>"
description: "<Short description>"
icon: "article"
date: "2024-08-24T..."
lastmod: "2024-08-24T..."
draft: false
toc: true
katex: true
---

## <N>.<M>. <Topic Name>

**Definisi:** 1–2 kalimat yang jelas dan actionable. Contoh:
> "Stack adalah struktur data LIFO (Last-In-First-Out) — elemen terakhir masuk adalah pertama keluar."

### Operasi & Kompleksitas

| Operasi | Kompleksitas | Keterangan |
|---------|--------------|------------|
| Op1     | O(...)       | Penjelasan singkat |

### Implementasi Idiomatik Go

- Gunakan `[]T` (slice) untuk dynamic arrays
- Gunakan `container/list` untuk linked list
- Gunakan `container/heap` untuk heap
- Gunakan `sync.Mutex` untuk concurrency
- Gunakan `strings.Builder` untuk string building
- Gunakan `math/bits` untuk bitwise operations
- Hindari pseudocode yang redundan — langsung ke Go
- Hindari kode dari bahasa lain (JANGAN pakai `Vec<T>`, `impl`, `let mut`, dll)

### Decision Matrix

| Pakai <Ini> Kalau... | Hindari Kalau... |
|---------------------|------------------|
| ...                 | ...              |

### Edge Cases & Pitfalls

- **Case 1:** Deskripsi singkat
- **Case 2:** Deskripsi singkat

### Quick Reference (per chapter)

| Struktur | Go Type | Akses | Insert | Delete | Use Case |
|----------|---------|-------|--------|--------|----------|
| ...      | ...     | ...   | ...    | ...    | ...      |
```

### Rules

1. **NO redundant pseudocode** — pseudocode hanya untuk konsep non-trivial
2. **NO language mixing** — kode harus Go idiomatik, bukan Rust/C++/Python yang di-relabel
3. **NO verbose narratives** — maksimal 1 paragraf per konsep
4. **NO historical background** — pembaca sudah tahu DS penting
5. **NO mathematical proofs** — intuisi > proof
6. **MUST include decision matrix** — "pakai ini kalau..."
7. **MUST include Go stdlib references** — `container/heap`, `sync.Map`, dsb.
8. **MUST include anti-patterns** — kesalahan umum di Go
9. **MUST include Big-O table** — minimal untuk operasi utama
10. **Code max 40 lines** per block — jika lebih, split menjadi fungsi terpisah

### Frontmatter

```yaml
---
weight: <chapter_number>00  # e.g., 1000 for Ch 10
title: "Chapter <N>"
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
# Build
hugo --quiet

# Development server
hugo server --port 1313
```

## Content Directory Structure

```
content/docs/
├── Table-of-Contents.md
├── how-to-use-dsag.md
├── Preface.md
├── Foreword.md
├── Foreword-2.md
├── closing-remark.md
├── Part-I/
│   ├── Chapter-1.md
│   ├── Chapter-2.md
│   ├── ...
├── Part-II/
│   ├── Chapter-6.md
│   ├── ...
├── Part-III/
│   ├── Chapter-9.md
│   ├── Chapter-10.md  # Example: Elementary Data Structures
│   └── ...
└── Part-IV/
    ├── Chapter-16.md
    └── ...
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

## Checklist Before Committing

- [ ] Hugo builds without errors (`hugo --quiet`)
- [ ] No corrupted shortcode tags
- [ ] Code is idiomatic Go (not Rust/Python/C++)
- [ ] Chapter follows the template structure
- [ ] Decision matrix included
- [ ] Big-O table included
- [ ] Edge cases listed
- [ ] Go stdlib references included
- [ ] No empty content without placeholder
