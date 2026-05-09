---
weight: 30300
title: "Chapter 11 - Disjoint Sets"
description: "Disjoint Sets"
icon: "article"
date: "2024-08-24T23:42:11+07:00"
lastmod: "2024-08-24T23:42:11+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Trees are the lifeblood of computer science. Master them, and you master the flow of data.</em>" — Anonymous</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 11 focuses on <abbr title="A search algorithm that finds the position of a target value within a sorted array.">Binary Search</abbr> Trees (BST), Self-Balancing Trees (AVL/Red-Black), and <abbr title="A hierarchical data structure with a root node and child nodes.">Tree</abbr> Augmentation. It explores implementing trees safely in Go using 1.18+ Generics while addressing the <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collection</abbr> (GC) pressure caused by excessive <abbr title="A variable that stores a memory address.">pointer</abbr> allocations.
{{% /alert %}}

## 11.1. <abbr title="A binary tree where the left child is smaller and the right child is larger than the parent.">Binary Search Tree</abbr> (BST)

**Definition:** A BST is a node-based <abbr title="A tree data structure in which each node has at most two children.">binary tree</abbr> where the left <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> strictly contains keys less than the <abbr title="The topmost node in a tree data structure.">root</abbr>, and the right <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> contains keys greater than the <abbr title="The topmost node in a tree data structure.">root</abbr>. It provides structured ordering and efficient <abbr title="The process of finding a specific element in a data structure.">searching</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Search | <code>O(h)</code> | h = <abbr title="The length of the longest path from a node to a leaf.">height</abbr>, <code>O(log n)</code> if perfectly balanced |
| Insert | <code>O(h)</code> | Traverses downward to find a valid <abbr title="A node with no children in a tree.">leaf</abbr> |
| Delete | <code>O(h)</code> | Handles three distinct cases: <abbr title="A node with no children in a tree.">leaf</abbr>, one <abbr title="A node directly connected to another node when moving away from the root.">child</abbr>, two children |

### Idiomatic Go 1.18+ Generic Implementation

A classic Go anti-pattern is creating trees using `interface{}` to hold arbitrary values, destroying type-safety and hurting performance. Utilizing Go 1.18 Generics (`[K constraints.Ordered, V any]`) creates a reusable, strongly-typed BST.

```go
package main

import (
	"fmt"
	"golang.org/x/exp/constraints"
)

// Node is a generic tree node holding an ordered Key and an arbitrary Value.
type Node[K constraints.Ordered, V any] struct {
	Key   K
	Value V
	Left  *Node[K, V]
	Right *Node[K, V]
}

// Insert traverses the tree and places the new key-value pair.
// Notice the pointer receiver (*Node) allowing us to safely return the modified tree.
func (n *Node[K, V]) Insert(key K, val V) *Node[K, V] {
	if n == nil {
		return &Node[K, V]{Key: key, Value: val}
	}
	if key < n.Key {
		n.Left = n.Left.Insert(key, val)
	} else if key > n.Key {
		n.Right = n.Right.Insert(key, val)
	} else {
		// Update value if key already exists
		n.Value = val 
	}
	return n
}

// Search returns a pointer to the found node, or nil.
func (n *Node[K, V]) Search(key K) *Node[K, V] {
	if n == nil || n.Key == key {
		return n
	}
	if key < n.Key {
		return n.Left.Search(key)
	}
	return n.Right.Search(key)
}

func main() {
	var root *Node[int, string]
	root = root.Insert(10, "Ten")
	root = root.Insert(5, "Five")
	root = root.Insert(15, "Fifteen")

	if found := root.Search(5); found != nil {
		fmt.Println("Found:", found.Value) // "Five"
	}
}
```

### The Go GC Pressure Problem
While trees are elegant, **allocating millions of `*Node` structs scatters memory randomly across the <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>.** Every time you call `&Node{}`, you create work for the Go Garbage Collector. During a GC sweep, the <abbr title="The period during which a computer program is executing.">runtime</abbr> must painstakingly trace every single left and right <abbr title="A variable that stores a memory address.">pointer</abbr> across the entire <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr> <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>.
- **Mitigation:** If you need a massive <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> that is built once and rarely deleted from, consider implementing a <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> using a pre-allocated flat slice (`[]Node`) and integer indexes instead of raw memory pointers.

## 11.2. Self-Balancing Trees (AVL)

**Definition:** Standard BSTs degenerate into <code>O(n)</code> linked lists if data is inserted in sorted order. AVL and Red-Black trees aggressively maintain an <code>O(log n)</code> <abbr title="The length of the longest path from a node to a leaf.">height</abbr> by executing structural rotations upon insertion or deletion.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Rotation | <code>O(1)</code> | Re-linking <abbr title="A node directly connected to another node when moving away from the root.">child</abbr> pointers locally |
| Insert AVL | <code>O(log n)</code> | Maximum of 2 rotations to restore balance |
| Search | <code>O(log n)</code> | Guaranteed <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> performance |

### Idiomatic Generic AVL Rotations

```go
package main

import (
	"fmt"
	"golang.org/x/exp/constraints"
)

type AVLNode[K constraints.Ordered, V any] struct {
	Key    K
	Value  V
	Height int
	Left   *AVLNode[K, V]
	Right  *AVLNode[K, V]
}

func height[K constraints.Ordered, V any](n *AVLNode[K, V]) int {
	if n == nil {
		return 0
	}
	return n.Height
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func rotateRight[K constraints.Ordered, V any](y *AVLNode[K, V]) *AVLNode[K, V] {
	x := y.Left
	T2 := x.Right

	// Perform rotation
	x.Right = y
	y.Left = T2

	// Update heights
	y.Height = max(height(y.Left), height(y.Right)) + 1
	x.Height = max(height(x.Left), height(x.Right)) + 1

	return x
}
```

### Decision Matrix

| Use Balanced Trees When... | Avoid If... |
|---------------------|------------------|
| You strictly mandate a guaranteed <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> <code>O(log n)</code> | Data is entirely static (simply sort a slice and use <abbr title="A search algorithm that finds the position of a target value within a sorted array.">binary search</abbr>) |
| Managing in-memory indexes | The heavy <abbr title="A variable that stores a memory address.">pointer</abbr> overhead and GC tracing stalls your application |

## 11.3. <abbr title="A hierarchical data structure with a root node and child nodes.">Tree</abbr> Augmentation

**Definition:** Augmentation involves injecting specialized metadata (such as <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> sizes or sums) directly into the <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> structs. This natively unlocks advanced capabilities like high-speed rank querying.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| <abbr title="A tree consisting of a node and all of its descendants.">Subtree</abbr> Size | <code>O(1)</code> | Read directly from the augmented field |
| Rank Query | <code>O(h)</code> | Derived recursively via <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> sizes |

### Idiomatic Generic Augmentation

```go
package main

import "golang.org/x/exp/constraints"

type AugNode[K constraints.Ordered] struct {
	Key         K
	SubtreeSize int
	Left, Right *AugNode[K]
}

func size[K constraints.Ordered](n *AugNode[K]) int {
	if n == nil {
		return 0
	}
	return n.SubtreeSize
}

// Rank safely locates the position of a given value inside the tree.
func (n *AugNode[K]) Rank(key K) int {
	if n == nil {
		return 0
	}
	if key < n.Key {
		return n.Left.Rank(key)
	}
	
	leftSize := size(n.Left)
	if key == n.Key {
		return leftSize
	}
	
	// Value is greater: rank includes the left tree, the root itself (+1), and the rank in the right tree.
	return leftSize + 1 + n.Right.Rank(key)
}
```

### Edge Cases & Pitfalls

- **Empty tree:** `Search`, `Min`, `Max` panic or return zero value if tree is nil.
- **Duplicate keys:** Standard BST rejects duplicates; decide policy (overwrite or multiset).
- **Unbalanced input:** Sorted input degenerates BST to O(n) linked list.
- **Deep recursion:** Recursive traversal overflows stack on deep trees — use iterative DFS.
- **GC pressure:** Millions of tree nodes = heavy GC tracing; prefer sorted slices for static data.
- **Nil pointer dereference:** Always check node != nil before accessing fields.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type Implementation | Time | Memory / GC Pressure | Use Case |
|------|---------|------|-------|----------|
| Generic BST | `*Node[K, V]` | <code>O(h)</code> | Extremely High (<abbr title="A variable that stores a memory address.">pointer</abbr> chasing) | Fast ordered inserts |
| <abbr title="A self-balancing binary search tree with a balance factor of -1, 0, or 1.">AVL Tree</abbr> | `*AVLNode[K, V]` | <code>O(log n)</code> | Extremely High | Guaranteed <code>O(log n)</code> bounds |
| Sorted Slice | `[]T` | <code>O(log n)</code> search | Zero GC overhead | Read-heavy, static data |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 11:</strong> Utilizing Generics `[K constraints.Ordered]` makes <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> implementations in Go radically safer and vastly more reusable. However, always remain fiercely aware of the architectural cost of trees in Go: allocating millions of tiny structs generates heavy GC tracing pressure. If your <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> is static, a simple sorted slice paired with `sort.Search` is infinitely faster and friendlier to the CPU <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr>.
{{% /alert %}}