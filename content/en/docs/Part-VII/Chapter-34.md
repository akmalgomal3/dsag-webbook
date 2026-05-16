---
weight: 70700
title: "Chapter 34: String Matching Algorithms"
description: "String Matching Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithmic thinking is a fundamental part of our toolbox, helping us solve problems with precision and elegance.</em>" : Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 34 covers <abbr title="Finding occurrences of a pattern within a text">string matching</abbr> algorithms: Naive, <abbr title="A linear-time string matching algorithm using prefix-suffix tables.">KMP</abbr>, <abbr title="A string matching algorithm scanning right to left using heuristics.">Boyer-Moore</abbr>, <abbr title="A string matching algorithm using rolling hash for efficient comparison.">Rabin-Karp</abbr>, and <abbr title="A multi-pattern string matching algorithm using a trie with failure links.">Aho-Corasick</abbr> in Go.
{{% /alert %}}

## 34.1. Naive <abbr title="Finding occurrences of a pattern within a text">String Matching</abbr>

**Definition:** Compares pattern directly against every overlapping text position.

**Mechanics:**
Advanced algorithms preprocess patterns. Mismatches trigger skips over known non-matching chunks. Guarantees efficiency over random streams.

**Use Cases:**
UNIX `grep`. DNA sequence analysis. Virus signature scanning.

**Memory Mechanics:**
Operates on raw bytes. Convert to `[]rune` for multi-byte Unicode. Byte arrays standard for traditional matching.

### Operations & Complexity

| Case | Time | Space |
|-------|------|-------|
| Best | <code>O(n)</code> | Immediate match |
| Average | <code>O(n × m)</code> | Exhaustive search |
| Worst | <code>O(n × m)</code> | Repetitive overlapping patterns |

### Pseudocode

```text
NaiveSearch(text, pattern):
    positions = empty list
    n = length(text), m = length(pattern)
    for i from 0 to n-m:
        match = true
        for j from 0 to m-1:
            if text[i+j] != pattern[j]:
                match = false
                break
        if match:
            append i to positions
    return positions
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func naiveSearch(text, pattern string) []int {
    var positions []int
    n, m := len(text), len(pattern)
    if m == 0 || m > n {
        return positions
    }
    for i := 0; i <= n-m; i++ {
        match := true
        for j := 0; j < m; j++ {
            if text[i+j] != pattern[j] {
                match = false
                break
            }
        }
        if match {
            positions = append(positions, i)
        }
    }
    return positions
}

func main() {
    text := "ABABDABACDABABCABAB"
    pattern := "ABABCABAB"
    fmt.Println("Positions:", naiveSearch(text, pattern))
}
```

{{% alert icon="📌" context="warning" %}}
Go indices raw bytes. Use `[]rune` for Unicode awareness. Traditional algorithms use byte arrays.
{{% /alert %}}

### Decision Matrix

| Use Naive When... | Avoid If... |
|----------------------|------------------|
| Rapid prototyping | Massive text. Heavy repetition. |
| Pattern length m < 5 | Pattern length m large (> 100) |

## 34.2. Knuth-Morris-Pratt (KMP)

**Definition:** Uses prefix-suffix data (LPS array). Skips redundant comparisons.

### Operations & Complexity

| Operation | Time | Space |
|---------|------|-------|
| Preprocessing LPS | <code>O(m)</code> | <code>O(m)</code> |
| Search | <code>O(n)</code> | <code>O(m)</code> |
| Total | <code>O(n + m)</code> | <code>O(m)</code> |

### Pseudocode

```text
ComputeLPS(pattern):
    m = length(pattern)
    lps = new array of size m initialized to 0
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1
    return lps

KMPSearch(text, pattern):
    n = length(text), m = length(pattern)
    lps = ComputeLPS(pattern)
    i, j = 0, 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1; j += 1
        if j == m:
            report match at i-j
            j = lps[j-1]
        else if i < n and text[i] != pattern[j]:
            if j != 0: j = lps[j-1]
            else: i += 1
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func computeLPS(pattern string) []int {
    m := len(pattern)
    lps := make([]int, m)
    length := 0
    for i := 1; i < m; {
        if pattern[i] == pattern[length] {
            length++
            lps[i] = length
            i++
        } else {
            if length != 0 {
                length = lps[length-1]
            } else {
                lps[i] = 0
                i++
            }
        }
    }
    return lps
}

func kmpSearch(text, pattern string) []int {
    var positions []int
    n, m := len(text), len(pattern)
    if m == 0 {
        return positions
    }
    lps := computeLPS(pattern)
    i, j := 0, 0
    for i < n {
        if text[i] == pattern[j] {
            i++
            j++
        }
        if j == m {
            positions = append(positions, i-j)
            j = lps[j-1]
        } else if i < n && text[i] != pattern[j] {
            if j != 0 {
                j = lps[j-1]
            } else {
                i++
            }
        }
    }
    return positions
}

func main() {
    text := "ABABDABACDABABCABAB"
    pattern := "ABABCABAB"
    fmt.Println("KMP:", kmpSearch(text, pattern))
}
```

{{% alert icon="📌" context="warning" %}}
KMP optimal for repetitive prefix-suffix overlaps. Boyer-Moore faster for large alphabets.
{{% /alert %}}

## 34.3. Boyer-Moore

**Definition:** Evaluates pattern right-to-left. Uses "bad character" heuristic. Leaps over mismatches.

### Operations & Complexity

| Case | Time | Space |
|-------|------|-------|
| Best | <code>O(n/m)</code> | Massive leaps |
| Average | <code>O(n/m)</code> | . |
| Worst | <code>O(n × m)</code> | Identical input characters |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func preprocessBadChar(pattern string) [256]int {
    var badChar [256]int
    for i := range badChar {
        badChar[i] = -1
    }
    for i := 0; i < len(pattern); i++ {
        badChar[pattern[i]] = i
    }
    return badChar
}

func boyerMooreSearch(text, pattern string) []int {
    var positions []int
    n, m := len(text), len(pattern)
    if m == 0 || m > n {
        return positions
    }
    badChar := preprocessBadChar(pattern)
    shift := 0
    for shift <= n-m {
        j := m - 1
        for j >= 0 && pattern[j] == text[shift+j] {
            j--
        }
        if j < 0 {
            positions = append(positions, shift)
            if shift+m < n {
                shift += m - badChar[text[shift+m]]
            } else {
                shift++
            }
        } else {
            bc := badChar[text[shift+j]]
            if bc == -1 {
                shift += j + 1
            } else {
                skip := j - bc
                if skip < 1 {
                    skip = 1
                }
                shift += skip
            }
        }
    }
    return positions
}

func main() {
    text := "ABAAABCD"
    pattern := "ABC"
    fmt.Println("BM:", boyerMooreSearch(text, pattern))
}
```

## 34.4. Rabin-Karp

**Definition:** Uses rolling hash. Compares pattern hash against text substring hashes.

### Operations & Complexity

| Case | Time | Space |
|-------|------|-------|
| Average | <code>O(n + m)</code> | <code>O(1)</code> |
| Worst | <code>O(n × m)</code> | <code>O(1)</code> (Hash collisions) |

### Idiomatic Go Implementation

```go
package main

import "fmt"

const primeRK = 16777619

func rabinKarpSearch(text, pattern string) []int {
    var positions []int
    n, m := len(text), len(pattern)
    if m == 0 || m > n {
        return positions
    }
    var hashP, hashT uint32
    var pow uint32 = 1
    for i := 0; i < m-1; i++ {
        pow = pow * primeRK
    }
    for i := 0; i < m; i++ {
        hashP = hashP*primeRK + uint32(pattern[i])
        hashT = hashT*primeRK + uint32(text[i])
    }
    for i := 0; i <= n-m; i++ {
        if hashP == hashT {
            match := true
            for j := 0; j < m; j++ {
                if text[i+j] != pattern[j] {
                    match = false
                    break
                }
            }
            if match {
                positions = append(positions, i)
            }
        }
        if i < n-m {
            hashT = (hashT-uint32(text[i])*pow)*primeRK + uint32(text[i+m])
        }
    }
    return positions
}

func main() {
    text := "AABAACAADAABAAABAA"
    pattern := "AABA"
    fmt.Println("RK:", rabinKarpSearch(text, pattern))
}
```

## 34.5. Aho-Corasick

**Definition:** Finite <abbr title="A self-operating state machine or computational model.">state machine</abbr>. Trie with failure links. Locates multiple patterns in single pass.

### Idiomatic Go Implementation

```go
package main

import "fmt"

type ACNode struct {
    children [256]*ACNode
    fail     *ACNode
    output   []string
    isEnd    bool
}

func buildTrie(patterns []string) *ACNode {
    root := &ACNode{}
    for _, p := range patterns {
        node := root
        for i := 0; i < len(p); i++ {
            c := p[i]
            if node.children[c] == nil {
                node.children[c] = &ACNode{}
            }
            node = node.children[c]
        }
        node.isEnd = true
        node.output = append(node.output, p)
    }
    return root
}

func buildFailureLinks(root *ACNode) {
    queue := []*ACNode{}
    for c := 0; c < 256; c++ {
        if child := root.children[c]; child != nil {
            child.fail = root
            queue = append(queue, child)
        }
    }
    for len(queue) > 0 {
        node := queue[0]
        queue = queue[1:]
        for c := 0; c < 256; c++ {
            child := node.children[c]
            if child == nil {
                continue
            }
            fail := node.fail
            for fail != nil && fail.children[c] == nil {
                fail = fail.fail
            }
            if fail == nil {
                child.fail = root
            } else {
                child.fail = fail.children[c]
                child.output = append(child.output, child.fail.output...)
            }
            queue = append(queue, child)
        }
    }
}

func ahoCorasickSearch(text string, root *ACNode) map[string][]int {
    matches := make(map[string][]int)
    node := root
    for i := 0; i < len(text); i++ {
        c := text[i]
        for node != root && node.children[c] == nil {
            node = node.fail
        }
        if child := node.children[c]; child != nil {
            node = child
        }
        for _, pattern := range node.output {
            matches[pattern] = append(matches[pattern], i-len(pattern)+1)
        }
    }
    return matches
}

func main() {
    patterns := []string{"he", "she", "his", "hers"}
    root := buildTrie(patterns)
    buildFailureLinks(root)
    text := "ahishers"
    matches := ahoCorasickSearch(text, root)
    fmt.Println("Matches:", matches)
}
```

### Anti-Patterns

- **Unicode index by byte:** UTF-8 strings return bytes. Use `[]rune` for correct rune matching.
- **Rabin-Karp hash only:** Match is not guaranteed. Verify actual characters after hash hit.
- **Rebuilding Aho-Corasick:** Construct once. Search many. Amortize preprocessing cost.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Naive | . | <code>O(nm)</code> | <code>O(1)</code> | Prototyping |
| KMP | preprocessed | <code>O(n)</code> | <code>O(m)</code> | Worst-case guarantees |
| Boyer-Moore | preprocessed | <code>O(n/m)</code> avg | <code>O(\sigma)</code> | Large alphabets |
| Rabin-Karp | hashed | <code>O(n)</code> avg | <code>O(1)</code> | Multiple pattern scans |
| Aho-Corasick | <abbr title="A tree-like data structure used to store a dynamic set of strings.">trie</abbr> | <code>O(n + occ)</code> | <code>O(\sum m)</code> | Dictionary matching |
| `strings.Index` | builtin | hyper-optimized | <code>O(1)</code> | Production default |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 34:</strong> String matching uses Naive, KMP, Boyer-Moore, Rabin-Karp, and Aho-Corasick. KMP locks worst-case. Boyer-Moore handles wide alphabets. Aho-Corasick matches dictionaries in one pass.
{{% /alert %}}

## See Also

- [Chapter 33: Polynomial and FFT](/docs/part-vii/chapter-33/)
- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
- [Chapter 48: Suffix Arrays](/docs/part-ix/chapter-48/)
