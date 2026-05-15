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
<strong>"<em>Words are, of course, the most powerful drug used by mankind.</em>" : Rudyard Kipling</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 37 covers <abbr title="A tree data structure for storing and searching strings with common prefixes.">Trie</abbr> (<abbr title="A tree storing strings where common prefixes are shared, also called a Trie.">prefix tree</abbr>) data structures: efficient storage and retrieval of strings with common prefixes. Essential for autocomplete, spell checking, and IP routing.
{{% /alert %}}

## 37.1. Trie Fundamentals

**Definition:** A Trie is a tree where each node represents a character. Paths from root to leaf form complete words. All descendants of a node share the same prefix.

**Background & Philosophy:**
The philosophy is structural prefix sharing. Instead of storing ten words that start with "auto" as ten distinct strings, a Trie stores the prefix "a-u-t-o" exactly once, branching off only when the words diverge. It transforms string retrieval from an <code>O(N)</code> scan into an <code>O(m)</code> traversal based strictly on the word's length, independent of dictionary size.

**Use Cases:**
Search engine autocomplete engines, routing IP addresses in networking hardware (<abbr title="A space-optimized Trie with edge labels, also known as a Radix Trie.">Radix Tries</abbr>), and mobile phone predictive text keyboards.

**Memory Mechanics:**
A standard Trie is incredibly memory-hungry. Each <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> in Go typically holds a `map[rune]*TrieNode`. Allocating millions of tiny maps across the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> severely fragments <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> and causes massive <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> tracing overhead. High-performance production Tries (like Double-Array Tries or Radix Trees) compress these <abbr title="A variable that stores a memory address.">pointers</abbr> into packed, flat arrays to drastically reduce memory footprints and restore <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality.

### Operations & Complexity

| Operation | Time | Space | Description |
|-----------|------|-------|-------------|
| Insert | <code>O(m)</code> | <code>O(m)</code> | m = word length |
| Search | <code>O(m)</code> | <code>O(1)</code> | Exact match |
| StartsWith | <code>O(m)</code> | <code>O(1)</code> | Prefix check |
| Delete | <code>O(m)</code> | <code>O(1)</code> | Remove word |

## 37.2. Basic Trie

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

Use a map for children to support any character set dynamically.

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

## 37.3. Autocomplete

**Definition:** Given a prefix, return all words in the Trie that start with that prefix.

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

## 37.4. Decision Matrix

| Use Trie When... | Avoid If... |
|------------------|-------------|
| Many strings share prefixes | Strings are random with no common prefixes |
| Need fast prefix queries | Memory is extremely constrained |
| Implementing autocomplete or spell checker | Only exact match lookups needed (use hashmap) |

### Edge Cases & Pitfalls

- **Memory overhead:** Each node allocates a map; for dense alphabets (e.g., Unicode), use arrays or compressed tries.
- **Empty string:** Decide whether empty string is a valid word in your Trie.
- **Case sensitivity:** Normalize to lowercase before insertion unless case matters.

## 37.5. Quick Reference

| Operation | Go Type | Time | Space | Use Case |
|-----------|---------|------|-------|----------|
| Insert | `map[rune]*TrieNode` | <code>O(m)</code> | <code>O(m)</code> | Dictionary building |
| Search | `map[rune]*TrieNode` | <code>O(m)</code> | <code>O(1)</code> | Word validation |
| Prefix | `map[rune]*TrieNode` | <code>O(m)</code> | <code>O(k)</code> | Autocomplete |
| Compressed Trie | Edge labels | <code>O(m)</code> | Reduced | Memory optimization |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 35:</strong> Tries excel at prefix-based string operations with <code>O(m)</code> time complexity. In Go, use `map[rune]*TrieNode` for flexibility or fixed-size arrays for performance. Apply tries to autocomplete, spell checking, and any problem involving shared string prefixes.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/Chapter-9/)
- [Chapter 34: <abbr title="Finding occurrences of a pattern within a text">String Matching</abbr> Algorithms](/docs/part-vii/Chapter-34/)
- [Chapter 48: Suffix Arrays](/docs/part-ix/Chapter-48/)
