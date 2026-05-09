---
weight: 70700
title: "Chapter 35 - String Matching Algorithms"
description: "String Matching Algorithms"
icon: "article"
date: "2024-08-24T23:42:50+07:00"
lastmod: "2024-08-24T23:42:50+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithmic thinking is a fundamental part of our toolbox, helping us solve problems with precision and elegance.</em>" — Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 35 covers powerful string matching algorithms: Naive, KMP, Boyer-Moore, Rabin-Karp, and Aho-Corasick implemented natively in Go.
{{% /alert %}}

## 35.1. Naive String Matching

**Definition:** The naive algorithm meticulously compares the targeted pattern directly against every possible overlapping position sequentially along the text.

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
Go dictates string indexing at the raw byte <abbr title="The set of all nodes at a given depth.">level</abbr>. To correctly parse multi-byte Unicode strings, aggressively convert them into a `[]rune` <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> first. Nevertheless, traditional string matching algorithms fundamentally operate upon standard byte arrays.
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

**Definition:** The <abbr title="The Knuth-Morris-Pratt string-searching algorithm that searches for occurrences of a word within a text.">KMP algorithm</abbr> aggressively leverages the intricate prefix-suffix data derived from the Longest Prefix Suffix (LPS) <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> to expertly circumvent completely redundant data comparisons.

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
| Average | <code>O(n/m)</code> | — |
| Worst | <code>O(n × m)</code> | When all input characters are painfully identical |

### Pseudocode

```text
PreprocessBadChar(pattern):
    badChar = array of size alphabet initialized to -1
    for i from 0 to length(pattern)-1:
        badChar[pattern[i]] = i
    return badChar

BoyerMooreSearch(text, pattern):
    n = length(text), m = length(pattern)
    badChar = PreprocessBadChar(pattern)
    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift+j]:
            j -= 1
        if j < 0:
            report match at shift
            shift += 1
        else:
            skip = max(1, j - badChar[text[shift+j]])
            shift += skip
```

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
A basic Boyer-Moore employing only the bad character heuristic stands exceptionally practical. Adding the good suffix rule actively repairs the <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> scenario but severely tangles complexity. For strict production integrity, aggressively lean on Go's deeply optimized `strings.Index`.
{{% /alert %}}

### Decision Matrix

| Use BM When... | Avoid If... |
|-------------------|------------------|
| <abbr title="The process of finding a specific element in a data structure.">Searching</abbr> through large alphabets (ASCII, Unicode text) | Scanning raw binary data overflowing with repetitive characters |
| Hunting for exceptionally long patterns (> 20 characters) | Seeking very short, fleeting patterns |

### Edge Cases & Pitfalls

- **Negative shift anomaly:** Aggressively guarantee the shift remains strictly positive. A bad character might incorrectly yield a negative shift if the last occurrence resides deeply behind the current mismatch position.
- **Bytes versus Runes:** Boyer-Moore is deeply locked to raw bytes. Processing raw Unicode mandates precise and careful structural adaptations.

## 35.4. Rabin-Karp

**Definition:** The <abbr title="A string-searching algorithm using hashing to find patterns in a text.">Rabin-Karp algorithm</abbr> meticulously calculates a rolling mathematical hash to seamlessly compare a pattern <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> directly alongside text substrings.

### Operations & Complexity

| Case | Time | Space |
|-------|------|-------|
| Average | <code>O(n + m)</code> | <code>O(1)</code> |
| Worst | <code>O(n × m)</code> | <code>O(1)</code> (Hash <abbr title="An event when two keys hash to the same index.">collision</abbr>) |

### Pseudocode

```text
RabinKarpSearch(text, pattern):
    n = length(text), m = length(pattern)
    hashP = hash of pattern
    hashT = hash of text[0:m]
    for i from 0 to n-m:
        if hashP == hashT:
            if text[i:i+m] == pattern:
                report match at i
        if i < n-m:
            hashT = roll hash forward by removing text[i] and adding text[i+m]
```

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

{{% alert icon="📌" context="warning" %}}
Rabin-Karp dramatically shines when aggressively matching multiple distinct patterns simultaneously (by incorporating a <abbr title="A hash table-based implementation of the Set interface.">hash set</abbr>). When facing a single solitary pattern, KMP or Boyer-Moore practically always outperform it.
{{% /alert %}}

### Decision Matrix

| Use RK When... | Avoid If... |
|-------------------|------------------|
| Conducting highly complex multiple pattern searches | Running a single pattern search against a microscopic text |
| Processing heavy plagiarism detection modules | A flawless <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> performance guarantee is absolutely essential |

### Edge Cases & Pitfalls

- **Hash <abbr title="An event when two keys hash to the same index.">collision</abbr> risks:** Relentlessly double-check the raw characters whenever a hash match mathematically presents itself.
- **Integer overflow collapse:** Depend exclusively on `uint64` or strictly bounded modular arithmetic to accommodate sweeping text blocks securely.

## 35.5. Aho-Corasick

**Definition:** Aho-Corasick systematically erects a robust finite state machine (a <abbr title="A tree-like data structure used to store a dynamic set of strings.">trie</abbr> fortified with failure links) engineered specifically to unearth numerous scattered patterns efficiently in a single, blazing-fast pass.

### Operations & Complexity

| Operation | Time | Space |
|---------|------|-------|
| Build <abbr title="A tree-like data structure used to store a dynamic set of strings.">trie</abbr> | <code>O(sum of pattern lengths)</code> | <code>O(sum of pattern lengths)</code> |
| Build failure links | <code>O(sum of pattern lengths)</code> | — |
| Search | <code>O(n + matches)</code> | <code>O(sum of pattern lengths)</code> |

### Pseudocode

```text
BuildTrie(patterns):
    root = new node
    for each pattern in patterns:
        node = root
        for each char c in pattern:
            if node.children[c] is nil:
                node.children[c] = new node
            node = node.children[c]
        node.isEnd = true
        node.output.append(pattern)
    return root

BuildFailureLinks(root):
    queue = [children of root]
    while queue not empty:
        node = dequeue
        for each child of node:
            set child failure link via traversal
            enqueue child

AhoCorasickSearch(text, root):
    matches = empty map
    node = root
    for i from 0 to length(text)-1:
        c = text[i]
        while node != root and node.children[c] is nil:
            node = node.fail
        if node.children[c] exists:
            node = node.children[c]
        for each pattern in node.output:
            append i-length(pattern)+1 to matches[pattern]
    return matches
```

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

{{% alert icon="📌" context="warning" %}}
Aho-Corasick savagely consumes a heavy footprint of <code>O(alphabet × nodes)</code> memory = <code>O(256 × total pattern length)</code>. For dense Unicode processing, aggressively migrate toward `map[byte]*ACNode` or `map[rune]*ACNode`.
{{% /alert %}}

### Decision Matrix

| Use AC When... | Avoid If... |
|-------------------|------------------|
| Unearthing vast quantities of multiple distinct patterns (> 5) | <abbr title="The process of finding a specific element in a data structure.">Searching</abbr> relentlessly for a solitary, lonely pattern |
| Operating over a massive streaming text layout | The hardware is incredibly starved for memory capacity |

### Edge Cases & Pitfalls

- **Overlapping patterns:** The core Aho-Corasick logic vigorously finds and records absolutely all occurrences, blatantly including messy overlaps.
- **Empty pattern:** Consistently verify that you meticulously accommodate for completely void pattern inputs.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Naive | — | <code>O(nm)</code> | <code>O(1)</code> | Early prototyping |
| KMP | preprocessed | <code>O(n)</code> | <code>O(m)</code> | Deep <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> guarantees |
| Boyer-Moore | preprocessed | <code>O(n/m)</code> avg | <code>O(\sigma)</code> | Utilizing large character alphabets |
| Rabin-Karp | hashed | <code>O(n)</code> avg | <code>O(1)</code> | Running multiple simultaneous pattern scans |
| Aho-Corasick | <abbr title="A tree-like data structure used to store a dynamic set of strings.">trie</abbr> | <code>O(n + occ)</code> | <code>O(\sum m)</code> | Full dictionary text matching |
| `strings.Index` | builtin | hyper-optimized | <code>O(1)</code> | Primary production single pattern matching |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 35:</strong> This chapter dissects <abbr title="A field or set of fields used to identify a record.">key</abbr> string matching algorithms: the Naive approach achieving <code>O(nm)</code>, KMP reliably offering <code>O(n+m)</code>, Boyer-Moore's rapid <code>O(n/m)</code> average, Rabin-Karp utilizing efficient rolling hashes, and the powerful Aho-Corasick for dense multiple-pattern environments. Leverage KMP to lock down a strict <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> guarantee, Boyer-Moore to aggressively handle wide alphabets, and Aho-Corasick for sweeping dictionary matches.
{{% /alert %}}

## See Also

- [Chapter 34 — Polynomial and FFT](/docs/Part-VII/Chapter-34/)
- [Chapter 37 — Trie Data Structures](/docs/Part-VII/Chapter-37/)
- [Chapter 49 — Suffix Arrays](/docs/Part-IX/Chapter-49/)
