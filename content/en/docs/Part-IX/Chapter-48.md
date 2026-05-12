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
Chapter 49 introduces suffix arrays — a space-efficient alternative to suffix trees for string searching, <abbr title="Finding a specific sequence within a larger data set">pattern matching</abbr>, and bioinformatics.
{{% /alert %}}

## 49.1. The String Search Problem

**Definition:** A <abbr title="A sorted array of all suffixes of a string, enabling efficient string matching and analysis.">suffix array</abbr> is the lexicographically sorted array of all suffixes of a string. It enables <code>O(n log n)</code> construction and <code>O(m log n)</code> pattern search.

**Background & Philosophy:**
The philosophy is reducing complex string geometries into mathematically sortable integers. Suffix Trees are comprehensive but complex to build and store. A Suffix Array abandons the tree structure, opting to sort pointers to the suffixes. It relies on the insight that binary search over a sorted list of suffixes solves <abbr title="Finding occurrences of a pattern within a text">string matching</abbr> directly.

**Use Cases:**
Bioinformatics (DNA sequence alignment), full-text search engines, and data compression (Burrows-Wheeler Transform).

**Memory Mechanics:**
A <abbr title="A compressed trie containing all suffixes of a text">Suffix Tree</abbr> allocates a node for every character, severely fragmenting <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. A Suffix Array merely stores an array of integers (the starting indices of suffixes). For a string of length `N`, it strictly requires <code>O(N)</code> contiguous memory (just `4N` or `8N` bytes). This <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> integer array allows the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> to prefetch data efficiently during binary searches, making it superior to Suffix Trees in real-world memory performance.

### Suffix Array vs <abbr title="A compressed trie containing all suffixes of a text">Suffix Tree</abbr>

| Aspect | Suffix Array | <abbr title="A compressed trie containing all suffixes of a text">Suffix Tree</abbr> |
|--------|--------------|-------------|
| Space | <code>O(n)</code> integers | <code>O(n)</code> pointers (heavy) |
| Construction | <code>O(n log n)</code> or <code>O(n)</code> | <code>O(n)</code> |
| Pattern search | <code>O(m log n)</code> | <code>O(m)</code> |
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

## 49.3. Pattern Search

With a suffix array, <abbr title="A search algorithm that finds the position of a target value within a sorted array.">binary search</abbr> finds all occurrences of pattern P in <code>O(\|P\| log n)</code> time.

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

- **Sentinel character:** Append `$` to ensure no suffix is a prefix of another.
- **Memory:** For large texts (genomes), use compressed suffix arrays.
- **Construction time:** <code>O(n² log n)</code> naive sort is too slow for n > 10⁵ — use doubling or SA-IS algorithm.

## 49.6. Quick Reference

| Algorithm | Time | Space |
|-----------|------|-------|
| Naive sort | <code>O(n² log n)</code> | <code>O(n)</code> |
| Doubling | <code>O(n log n)</code> | <code>O(n)</code> |
| SA-IS | <code>O(n)</code> | <code>O(n)</code> |

| Go stdlib | Usage |
|-----------|-------|
| `strings` | `Index`, `Contains` for simple cases |
| `index/suffixarray` | Go's production-ready suffix array implementation |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 47:</strong> Suffix arrays prove that sorting can solve complex string problems. By lexicographically sorting all suffixes, they transform <abbr title="Finding a specific sequence within a larger data set">pattern matching</abbr> into binary search — a direct <abbr title="Transforming one problem into another to prove difficulty">reduction</abbr> from string complexity to array simplicity. For static text search, they offer the best balance of speed, space, and implementation clarity.
{{% /alert %}}

## See Also

- [Chapter 34: <abbr title="Finding occurrences of a pattern within a text">String Matching</abbr> Algorithms](/docs/Part-VII/Chapter-34/)
- [Chapter 36: Trie Data Structures](/docs/Part-VII/Chapter-36/)
- [Chapter 49: Persistent Data Structures](/docs/Part-IX/Chapter-49/)
