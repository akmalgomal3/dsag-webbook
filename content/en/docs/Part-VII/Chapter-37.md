---
weight: 7900
title: "Chapter 37 - Trie Data Structures"
description: "Trie Data Structures"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Words are, of course, the most powerful drug used by mankind.</em>" — Rudyard Kipling</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 37 covers Trie (prefix tree) data structures: efficient storage and retrieval of strings with common prefixes. Essential for autocomplete, spell checking, and IP routing.
{{% /alert %}}

## 37.1. Trie Fundamentals

**Definition:** A Trie is a tree where each node represents a character. Paths from root to leaf form complete words. All descendants of a node share the same prefix.

### Operations & Complexity

| Operation | Time | Space | Description |
|-----------|------|-------|-------------|
| Insert | <code>O(m)</code> | <code>O(m)</code> | m = word length |
| Search | <code>O(m)</code> | <code>O(1)</code> | Exact match |
| StartsWith | <code>O(m)</code> | <code>O(1)</code> | Prefix check |
| Delete | <code>O(m)</code> | <code>O(1)</code> | Remove word |

## 37.2. Basic Trie

### Idiomatic Go Implementation

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
| Implementing autocomplete or spell checker | Only exact match lookups needed (use hash map) |

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
<strong>Summary Chapter 37:</strong> Tries excel at prefix-based string operations with <code>O(m)</code> time complexity. In Go, use `map[rune]*TrieNode` for flexibility or fixed-size arrays for performance. Apply tries to autocomplete, spell checking, and any problem involving shared string prefixes.
{{% /alert %}}
