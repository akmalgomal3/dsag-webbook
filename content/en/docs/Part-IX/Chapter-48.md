---
weight: 90500
title: "Chapter 48: Suffix Arrays"
description: "Suffix Arrays"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>String algorithms are the hidden engines of the modern world.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Suffix arrays are space-efficient alternatives to suffix trees. Optimized for string searching and bioinformatics.
{{% /alert %}}

## 48.1. Purpose

**Definition:** A <abbr title="A sorted array of all suffixes of a string, enabling efficient string matching and analysis.">suffix array</abbr> is the lexicographically sorted array of all suffixes of a string. Enables <code>O(n log n)</code> construction and <code>O(m log n)</code> pattern search.

**Logic:**
String geometries reduced to sortable integers. Sorts pointers to suffixes. Binary search over sorted suffixes solves matching directly.

**Use Cases:**
Bioinformatics (DNA sequence alignment). Full-text search engines. Data compression (Burrows-Wheeler Transform).

**Memory Mechanics:**
Suffix trees allocate nodes for every character. Suffix arrays store integer indices. String length N requires <code>O(N)</code> contiguous memory. Contiguous integer arrays allow efficient prefetching and <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> performance.

### Comparison: Suffix Array vs Suffix Tree

| Aspect | Suffix Array | Suffix Tree |
|--------|--------------|-------------|
| Space | <code>O(n)</code> integers | <code>O(n)</code> pointers (heavy) |
| Construction | <code>O(n log n)</code> / <code>O(n)</code> | <code>O(n)</code> |
| Search | <code>O(m log n)</code> | <code>O(m)</code> |
| Implementation | Moderate | Complex |

## 48.2. Construction

Example: "banana":

| Index | Suffix |
|-------|--------|
| 5 | a |
| 3 | ana |
| 1 | anana |
| 0 | banana |
| 4 | na |
| 2 | nana |

Suffix array: [5, 3, 1, 0, 4, 2]

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr>: Naive Construction

```go
package main

import (
	"fmt"
	"sort"
)

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

func main() {
    sa := buildSuffixArray("banana")
    fmt.Println(sa) // [5 3 1 0 4 2]
}
```

## 48.3. Search

Binary search finds pattern P in <code>O(\|P\| log n)</code>.

### Longest Common Prefix (LCP)

<abbr title="An array storing the length of the longest common prefix between each adjacent pair of suffixes in the suffix array.">LCP array</abbr> enables:
- Finding repeated substrings.
- Counting distinct substrings.
- DNA sequence analysis.

## 48.4. Applications

| Application | Function |
|-------------|----------------------|
| **Full-text search** | Fast word occurrence lookups. |
| **Bioinformatics** | DNA sequence alignment. |
| **Compression** | Burrows-Wheeler transform base. |
| **Plagiarism** | Longest common substring detection. |

## 48.5. Decision Matrix

| Use Suffix Arrays When... | Use Tries When... |
|---------------------------|-------------------|
| Static text search. | Dynamic word dictionary. |
| Memory is constrained. | Prefix queries dominate. |
| Multiple pattern checks. | Single pattern, many texts. |

### Constraints & Risks

- **Sentinels:** Append `$` to prevent one suffix being a prefix of another.
- **Scaling:** Use compressed suffix arrays for massive genomes.
- **Efficiency:** Naive <code>O(n² log n)</code> sort fails for n > 10⁵. Use SA-IS algorithm.

### Anti-Patterns

- **Large Naive Sort:** Naive sorting full suffixes is catastrophically slow. Use <code>O(n)</code> SA-IS.
- **Mutating Text:** Any text change requires full rebuild. Use automata for dynamic text.
- **Missing Sentinels:** Without unique terminators, lexicographic ordering breaks.
- **Dictionary Lookups:** Tries beat suffix arrays for simple "starts with" queries.

## 48.6. Quick Reference

| Algorithm | Time | Space |
|-----------|------|-------|
| Naive sort | <code>O(n² log n)</code> | <code>O(n)</code> |
| Doubling | <code>O(n log n)</code> | <code>O(n)</code> |
| SA-IS | <code>O(n)</code> | <code>O(n)</code> |

| Go stdlib | Usage |
|-----------|-------|
| `strings` | `Index`, `Contains` for simple strings. |
| `index/suffixarray` | Production implementation. |

{{% alert icon="🎯" context="success" %}}
Suffix arrays transform string matching into binary search. Space efficient. sorting all suffixes solves complex string problems.
{{% /alert %}}

## See Also

- [Chapter 34: String Matching Algorithms](/docs/part-vii/chapter-34/)
- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
- [Chapter 49: Persistent Data Structures](/docs/part-ix/chapter-49/)
