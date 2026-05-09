---
weight: 9400
title: "Chapter 49 - Suffix Arrays"
description: "Suffix Arrays"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>String algorithms are the hidden engines of the modern world.</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 49 introduces suffix arrays — a space-efficient alternative to suffix trees for string searching, pattern matching, and bioinformatics.
{{% /alert %}}

## 49.1. The String Search Problem

**Definition:** A <abbr title="A sorted array of all suffixes of a string, enabling efficient string matching and analysis.">suffix array</abbr> is the lexicographically sorted array of all suffixes of a string. It enables powerful string operations with O(n log n) construction and O(m log n) pattern search.

### Suffix Array vs Suffix Tree

| Aspect | Suffix Array | Suffix Tree |
|--------|--------------|-------------|
| Space | O(n) integers | O(n) pointers (heavy) |
| Construction | O(n log n) or O(n) | O(n) |
| Pattern search | O(m log n) | O(m) |
| Implementation | Moderate | Complex |

## 49.2. Construction

For string "banana":

| Index | Suffix |
|-------|--------|
| 5 | a |
| 3 | ana |
| 1 | anana |
| 0 | banana |
| 4 | na |
| 2 | nana |

Suffix array: [5, 3, 1, 0, 4, 2]

### Idiomatic Go: Naive Construction

```go
func buildSuffixArray(s string) []int {
    n := len(s)
    sa := make([]int, n)
    for i := range sa {
        sa[i] = i
    }
    sort.Slice(sa, func(i, j int) bool {
        return s[sa[i]:] < s[sa[j]:]
    })
    return sa
}
```

## 49.3. Pattern Search

With a suffix array, binary search finds all occurrences of pattern P in O(|P| log n) time.

### Longest Common Prefix (LCP)

The <abbr title="An array storing the length of the longest common prefix between each adjacent pair of suffixes in the suffix array.">LCP array</abbr> enables:
- Finding repeated substrings
- Computing number of distinct substrings
- Solving bioinformatics problems

## 49.4. Applications

| Application | How Suffix Array Helps |
|-------------|----------------------|
| **Full-text search** | Find all occurrences of a word |
| **Bioinformatics** | DNA sequence alignment |
| **Data compression** | Burrows-Wheeler transform |
| **Plagiarism detection** | Find longest common substring |

## 49.5. Decision Matrix

| Use Suffix Arrays When... | Use Tries When... |
|---------------------------|-------------------|
| Searching in one static text | Dynamic dictionary of words |
| Space matters | Prefix queries dominate |
| Multiple pattern searches | Single pattern, many texts |

### Edge Cases & Pitfalls

- **Sentinel character:** Append '$' to ensure no suffix is a prefix of another.
- **Memory:** For large texts (genomes), use compressed suffix arrays.
- **Construction time:** O(n² log n) naive sort is too slow for n > 10⁵ — use doubling or SA-IS algorithm.

## 49.6. Quick Reference

| Algorithm | Time | Space |
|-----------|------|-------|
| Naive sort | O(n² log n) | O(n) |
| Doubling | O(n log n) | O(n) |
| SA-IS | O(n) | O(n) |

| Go stdlib | Usage |
|-----------|-------|
| `strings` | `Index`, `Contains` for simple cases |
| `index/suffixarray` | Go's suffix array implementation |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 49:</strong> Suffix arrays prove that sorting can solve complex string problems elegantly. By lexicographically sorting all suffixes, they transform pattern matching into binary search — a beautiful reduction from string complexity to array simplicity. For static text search, they offer the best balance of speed, space, and implementation clarity.
{{% /alert %}}
