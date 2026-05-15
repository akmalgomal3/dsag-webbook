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
Chapter 35 covers <abbr title="Finding occurrences of a pattern within a text">string matching</abbr> algorithms: Naive, <abbr title="A linear-time string matching algorithm using prefix-suffix tables.">KMP</abbr>, <abbr title="A string matching algorithm scanning right to left using heuristics.">Boyer-Moore</abbr>, <abbr title="A string matching algorithm using rolling hash for efficient comparison.">Rabin-Karp</abbr>, and <abbr title="A multi-pattern string matching algorithm using a trie with failure links.">Aho-Corasick</abbr> implemented in Go.
{{% /alert %}}

## 35.1. Naive <abbr title="Finding occurrences of a pattern within a text">String Matching</abbr>

**Definition:** The naive algorithm meticulously compares the targeted pattern directly against every possible overlapping position sequentially along the text.

**Background & Philosophy:**
The philosophy is recognizing patterns efficiently. Instead of treating text as a random stream, advanced <abbr title="Finding occurrences of a pattern within a text">string matching</abbr> algorithms preprocess the pattern (or the text) to map out structural repetitions. They mathematically guarantee that if a mismatch occurs, the algorithm skips chunks of text it already knows cannot match.

**Use Cases:**
The UNIX `grep` command, DNA sequence analysis in bioinformatics, and virus signature scanning in antivirus software.

**Memory Mechanics:**
<abbr title="Finding occurrences of a pattern within a text">String matching</abbr> fundamentally operates on raw bytes. To correctly parse multi-byte Unicode strings, convert them into a `[]rune` <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> first. Nevertheless, traditional string matching algorithms operate upon standard byte arrays.

### Operations & Complexity

| Case | Time | Space |
|-------|------|-------|
| Best | <code>O(n)</code> | Pattern matched instantly at the start |
| Average | <code>O(n × m)</code> | Standard exhaustive search |
| Worst | <code>O(n × m)</code> | Highly repetitive, overlapping patterns |

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
Go dictates string indexing at the raw byte <abbr title="The set of all nodes at a given depth.">level</abbr>. To correctly parse multi-byte Unicode strings, convert them into a `[]rune` <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> first. Nevertheless, traditional string matching algorithms operate upon standard byte arrays.
{{% /alert %}}

### Decision Matrix

| Use Naive When... | Avoid If... |
|----------------------|------------------|
| Rapidly prototyping, or managing tiny text streams | The text is massive, and the pattern displays fierce repetition |
| The pattern length m < 5 | The pattern length m is huge (> 100) |

### Edge Cases & Pitfalls

- **Empty pattern:** Decide to either return all possible positions natively or exit immediately yielding an empty slice.
- **Unicode formatting:** The `len(string)` function exclusively counts raw bytes, blatantly ignoring actual visual runes.

## 35.2. Knuth-Morris-Pratt (KMP)

**Definition:** The <abbr title="The Knuth-Morris-Pratt string-searching algorithm that searches for occurrences of a word within a text.">KMP algorithm</abbr> uses <abbr title="A substring at the beginning of a string.">prefix</abbr>-<abbr title="A substring at the end of a string.">suffix</abbr> data derived from the Longest Prefix Suffix (LPS) <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> to skip redundant data comparisons.

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
KMP achieves peak optimality when dealing with texts packed with repetitive prefix-suffix overlaps. However, for exceptionally large alphabets, Boyer-Moore routinely outpaces it.
{{% /alert %}}

### Decision Matrix

| Use KMP When... | Avoid If... |
|--------------------|------------------|
| Analyzing massive text chunks featuring a medium-sized pattern | Operating over a large alphabet where pattern matches are rare |
| A guaranteed, airtight <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> <code>O(n)</code> performance is mandated | Extensive heuristic leaping and skipping is highly preferred |

### Edge Cases & Pitfalls

- **LPS bounds violation:** Assiduously confirm `length = lps[length-1]` is executed solely if `length > 0`.
- **Pattern length 1:** The generated LPS is merely `[0]`; manually handle this if optimizing heavily.

## 35.3. Boyer-Moore

**Definition:** Boyer-Moore evaluates patterns in complete reverse (from right to left) and relies upon a "bad character" heuristic to perform massive leaps and skips over mismatching data blocks.

### Operations & Complexity

| Case | Time | Space |
|-------|------|-------|
| Best | <code>O(n/m)</code> | Featuring massive skips |
| Average | <code>O(n/m)</code> | . |
| Worst | <code>O(n × m)</code> | When all input characters are painfully identical |

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

{{% alert icon="📌" context="warning" %}}
A basic Boyer-Moore employing only the bad character heuristic is practical. Adding the good suffix rule repairs the <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> scenario but tangles complexity. For production use, lean on Go's optimized `strings.Index`.
{{% /alert %}}

## 35.4. Rabin-Karp

**Definition:** The <abbr title="A string-searching algorithm using hashing to find patterns in a text.">Rabin-Karp algorithm</abbr> meticulously calculates a rolling mathematical hash to seamlessly compare a pattern <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> directly alongside text substrings.

### Operations & Complexity

| Case | Time | Space |
|-------|------|-------|
| Average | <code>O(n + m)</code> | <code>O(1)</code> |
| Worst | <code>O(n × m)</code> | <code>O(1)</code> (Hash <abbr title="An event when two keys hash to the same index.">collision</abbr>) |

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

## 35.5. Aho-Corasick

**Definition:** Aho-Corasick builds a finite <abbr title="A self-operating state machine or computational model.">state machine</abbr> (a <abbr title="A tree-like data structure used to store a dynamic set of strings.">trie</abbr> with failure links) to locate multiple patterns in a single pass.

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

- **Indexing Unicode strings by byte position:** Go's `string` is UTF-8 encoded; `s[i]` gives a byte, not a rune. Convert to `[]rune` for Unicode-aware matching or stay in byte domain for ASCII-only patterns.
- **Rabin-Karp without collision verification:** A rolling hash match is not a guaranteed match. Always verify the substring equals the pattern after a hash hit, or produce false positives.
- **Rebuilding Aho-Corasick per query:** Preprocessing is O(Σm); construct the automaton once and reuse it across multiple texts to amortize the cost.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Naive | . | <code>O(nm)</code> | <code>O(1)</code> | Early prototyping |
| KMP | preprocessed | <code>O(n)</code> | <code>O(m)</code> | Deep <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> guarantees |
| Boyer-Moore | preprocessed | <code>O(n/m)</code> avg | <code>O(\sigma)</code> | Utilizing large character alphabets |
| Rabin-Karp | hashed | <code>O(n)</code> avg | <code>O(1)</code> | Running multiple simultaneous pattern scans |
| Aho-Corasick | <abbr title="A tree-like data structure used to store a dynamic set of strings.">trie</abbr> | <code>O(n + occ)</code> | <code>O(\sum m)</code> | Full dictionary text matching |
| `strings.Index` | builtin | hyper-optimized | <code>O(1)</code> | Primary production single <abbr title="Finding a specific sequence within a larger data set">pattern matching</abbr> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 34:</strong> This chapter dissects <abbr title="A field or set of fields used to identify a record.">key</abbr> <abbr title="Finding occurrences of a pattern within a text">string matching</abbr> algorithms: the Naive approach achieving <code>O(nm)</code>, KMP reliably offering <code>O(n+m)</code>, Boyer-Moore's rapid <code>O(n/m)</code> average, Rabin-Karp utilizing efficient rolling hashes, and the multi-pattern Aho-Corasick for dense multiple-pattern environments. Leverage KMP to lock down a strict <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> guarantee, Boyer-Moore to handle wide alphabets, and Aho-Corasick for sweeping dictionary matches.
{{% /alert %}}

## See Also

- [Chapter 33: Polynomial and FFT](/docs/part-vii/chapter-33/)
- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
- [Chapter 48: Suffix Arrays](/docs/part-ix/chapter-48/)
