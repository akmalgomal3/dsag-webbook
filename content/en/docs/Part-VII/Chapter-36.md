---
weight: 70900
title: "Chapter 36: Trie Data Structures"
description: "Trie Data Structures"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Words are, of course, the most powerful drug used by mankind.</em>" — Rudyard Kipling</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 36 covers <abbr title="A tree data structure for storing and searching strings with common prefixes.">Trie</abbr> (<abbr title="A tree storing strings where common prefixes are shared, also called a Trie.">prefix tree</abbr>) data structures. Efficient string storage and retrieval. Used for autocomplete, spell checking, and IP routing.
{{% /alert %}}

## 36.1. Trie Fundamentals

**Definition:** Trie is a tree. Each node represents one character. Paths form words. Descendants share prefixes.

**Background:**
Structural prefix sharing. Prefixes stored once. Branches occur at word divergence. Retrieval takes <code>O(m)</code> time. Performance independent of dictionary size.

**Use Cases:**
Search engine autocomplete. IP routing in network hardware. Predictive text keyboards.

**Memory Mechanics:**
Standard Trie consumes high memory. Each <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> uses `map[rune]*TrieNode`. Heap allocation causes fragmentation. <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> overhead increases. High-performance versions use flat arrays for <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> locality.

### Operations & Complexity

| Operation | Time | Space | Description |
|-----------|------|-------|-------------|
| Insert | <code>O(m)</code> | <code>O(m)</code> | m = word length |
| Search | <code>O(m)</code> | <code>O(1)</code> | Exact match |
| StartsWith | <code>O(m)</code> | <code>O(1)</code> | Prefix check |
| Delete | <code>O(m)</code> | <code>O(1)</code> | Remove word |

## 36.2. Basic Trie

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

```go
package main

import "fmt"

type TrieNode struct {
	Children map[rune]*TrieNode
	IsEnd    bool
}

type Trie struct {
	Root *TrieNode
}

func NewTrie() *Trie {
	return &Trie{Root: &TrieNode{Children: make(map[rune]*TrieNode)}}
}

func (t *Trie) Insert(word string) {
	node := t.Root
	for _, ch := range word {
		if node.Children[ch] == nil {
			node.Children[ch] = &TrieNode{Children: make(map[rune]*TrieNode)}
		}
		node = node.Children[ch]
	}
	node.IsEnd = true
}

func (t *Trie) Search(word string) bool {
	node := t.Root
	for _, ch := range word {
		if node.Children[ch] == nil { return false }
		node = node.Children[ch]
	}
	return node.IsEnd
}

func (t *Trie) StartsWith(prefix string) bool {
	node := t.Root
	for _, ch := range prefix {
		if node.Children[ch] == nil { return false }
		node = node.Children[ch]
	}
	return true
}

func main() {
	trie := NewTrie()
	words := []string{"cat", "car", "card", "care", "dog"}
	for _, w := range words { trie.Insert(w) }
	
	fmt.Println(trie.Search("car"))   // true
	fmt.Println(trie.Search("cart"))  // false
	fmt.Println(trie.StartsWith("ca")) // true
}
```

## 36.3. Autocomplete

**Definition:** Returns all words sharing a specific prefix.

### Idiomatic Go Implementation

```go
package main

import "fmt"

type TrieNode struct {
	Children map[rune]*TrieNode
	IsEnd    bool
}

type Trie struct {
	Root *TrieNode
}

func NewTrie() *Trie {
	return &Trie{Root: &TrieNode{Children: make(map[rune]*TrieNode)}}
}

func (t *Trie) Insert(word string) {
	node := t.Root
	for _, ch := range word {
		if node.Children[ch] == nil {
			node.Children[ch] = &TrieNode{Children: make(map[rune]*TrieNode)}
		}
		node = node.Children[ch]
	}
	node.IsEnd = true
}

func (t *Trie) AutoComplete(prefix string) []string {
	node := t.Root
	for _, ch := range prefix {
		if node.Children[ch] == nil { return nil }
		node = node.Children[ch]
	}
	var results []string
	var dfs func(n *TrieNode, path string)
	dfs = func(n *TrieNode, path string) {
		if n.IsEnd { results = append(results, prefix+path) }
		for ch, child := range n.Children {
			dfs(child, path+string(ch))
		}
	}
	dfs(node, "")
	return results
}

func main() {
	trie := NewTrie()
	for _, w := range []string{"cat", "car", "card", "care", "carpet"} {
		trie.Insert(w)
	}
	fmt.Println(trie.AutoComplete("car")) // [car card care carpet]
}
```

## 36.4. Decision Matrix

| Use Trie When... | Avoid If... |
|------------------|-------------|
| Strings share common prefixes | Strings lack common prefixes |
| Fast prefix queries required | Memory is extremely limited |
| Autocomplete or spell checking | Only exact matches needed (use hashmap) |

### Edge Cases & Pitfalls

- **Memory overhead:** Map allocation per node is expensive. Use arrays for fixed sets.
- **Empty string:** Decide validity of `""`.
- **Case sensitivity:** Normalize to lowercase before insertion.

### Anti-Patterns

- **Uncompressed Unicode tries:** Map overhead is severe. Use Radix trees for large sets.
- **Undefined empty string behavior:** Create explicit rules for `""`.
- **Unbounded results:** Short prefixes yield large result sets. Use counters or top-k logic.

## 36.5. Quick Reference

| Operation | Go Type | Time | Space | Use Case |
|-----------|---------|------|-------|----------|
| Insert | `map[rune]*TrieNode` | <code>O(m)</code> | <code>O(m)</code> | Dictionary building |
| Search | `map[rune]*TrieNode` | <code>O(m)</code> | <code>O(1)</code> | Word validation |
| Prefix | `map[rune]*TrieNode` | <code>O(m)</code> | <code>O(k)</code> | Autocomplete |
| Compressed Trie | Edge labels | <code>O(m)</code> | Reduced | Memory optimization |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 36:</strong> Tries provide <code>O(m)</code> string operations. Use `map[rune]*TrieNode` for character sets. Use arrays for performance. Best for autocomplete and spell checking.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
- [Chapter 34: <abbr title="Finding occurrences of a pattern within a text">String Matching</abbr> Algorithms](/docs/part-vii/chapter-34/)
- [Chapter 48: Suffix Arrays](/docs/part-ix/chapter-48/)
