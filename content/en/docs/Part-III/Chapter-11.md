---
weight: 30300
title: "Chapter 11: Binary Search Trees and Self-Balancing Trees"
description: "Binary Search Trees and Self-Balancing Trees"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Trees are the lifeblood of computer science. Master them, and you master the flow of data.</em>" : Anonymous</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 11 covers Generic BSTs, AVL trees, and augmentation techniques for rank queries.
{{% /alert %}}

## 11.1. Binary Search Tree (BST)

**Definition:** BST stores ordered data where left subtree is smaller and right is larger than root.

**Mechanics:**
BST embeds binary search into dynamic structure. Hierarchical pointers allow O(log n) insertion without memory shifting. Maintains order through structural linking rather than layout.

Nodes reside on heap as distinct allocations. Pointer chasing causes cache misses. Go generics `[K cmp.Ordered, V any]` eliminate interface boxing overhead and improve spatial locality.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Search | <code>O(h)</code> | O(log n) if balanced |
| Insert | <code>O(h)</code> | Traverses down to leaf |
| Delete | <code>O(h)</code> | Reassigns pointers |

### Idiomatic Go 1.18+ Generic Implementation

```go
package main

import (
	"fmt"
	"cmp"
)

type Node[K cmp.Ordered, V any] struct {
	Key   K
	Value V
	Left  *Node[K, V]
	Right *Node[K, V]
}

func (n *Node[K, V]) Insert(key K, val V) *Node[K, V] {
	if n == nil {
		return &Node[K, V]{Key: key, Value: val}
	}
	if key < n.Key {
		n.Left = n.Left.Insert(key, val)
	} else if key > n.Key {
		n.Right = n.Right.Insert(key, val)
	} else {
		n.Value = val 
	}
	return n
}

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
		fmt.Println("Found:", found.Value)
	}
}
```

**GC Pressure:**
Millions of nodes scatter memory across heap. Garbage collector must trace every pointer during sweeps. Use flat slices with integer indexes for static trees to reduce GC load.

## 11.2. Self-Balancing Trees (AVL)

**Definition:** AVL trees execute structural rotations to maintain O(log n) height. Prevents degradation into linked lists.

**Mechanics:**
Standard BST shape depends on insertion order. Self-balancing trees execute proactive rotations to prevent O(n) degradation. Maintains mathematical bounds on worst-case performance.

Nodes track height. Rotations swap pointers locally. Operations cost O(1) time and zero new heap allocations.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Rotation | <code>O(1)</code> | Re-links local child pointers |
| Insert | <code>O(log n)</code> | Max 2 rotations per insert |
| Search | <code>O(log n)</code> | Guaranteed height bound |

### Idiomatic Generic AVL Rotations

```go
package main

import (
	"fmt"
	"cmp"
)

type AVLNode[K cmp.Ordered, V any] struct {
	Key    K
	Value  V
	Height int
	Left   *AVLNode[K, V]
	Right  *AVLNode[K, V]
}

func avlInsert[K cmp.Ordered, V any](root *AVLNode[K, V], key K, val V) *AVLNode[K, V] {
	if root == nil { return &AVLNode[K, V]{Key: key, Value: val, Height: 1} }
	if key < root.Key {
		root.Left = avlInsert(root.Left, key, val)
	} else if key > root.Key {
		root.Right = avlInsert(root.Right, key, val)
	} else {
		root.Value = val
		return root
	}
	root.Height = 1 + max(avlHeight(root.Left), avlHeight(root.Right))
	bf := avlBalance(root)
	if bf > 1 && key < root.Left.Key { return avlRotateRight(root) }
	if bf < -1 && key > root.Right.Key { return avlRotateLeft(root) }
	if bf > 1 && key > root.Left.Key {
		root.Left = avlRotateLeft(root.Left)
		return avlRotateRight(root)
	}
	if bf < -1 && key < root.Right.Key {
		root.Right = avlRotateRight(root.Right)
		return avlRotateLeft(root)
	}
	return root
}

func avlHeight[K cmp.Ordered, V any](n *AVLNode[K, V]) int {
	if n == nil { return 0 }
	return n.Height
}

func avlBalance[K cmp.Ordered, V any](n *AVLNode[K, V]) int {
	if n == nil { return 0 }
	return avlHeight(n.Left) - avlHeight(n.Right)
}
```

### Decision Matrix

| Use Balanced Trees When... | Avoid If... |
|---------------------|------------------|
| Need guaranteed O(log n) | Data is static (use sorted slice) |
| Managing dynamic indexes | Pointer overhead slows application |

## 11.3. Tree Augmentation

**Definition:** Augmentation stores specialized metadata like subtree size in node structs. Enables rank queries.

**Mechanics:**
Trees are recursive. Augmentation caches subtree aggregates at the root of subtrees. Prevents repeated recursive calculations.

Adding fields increases node size. Updates happen during insertion or deletion by traversing up to root. Uses integer arithmetic in CPU cache.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Subtree Size | <code>O(1)</code> | Read from node field |
| Rank Query | <code>O(h)</code> | Calculate via subtree sizes |

### Idiomatic Generic Augmentation

```go
package main

import (
	"fmt"
	"cmp"
)

type AugNode[K cmp.Ordered] struct {
	Key         K
	SubtreeSize int
	Left, Right *AugNode[K]
}

func augInsert[K cmp.Ordered](n *AugNode[K], key K) *AugNode[K] {
	if n == nil { return &AugNode[K]{Key: key, SubtreeSize: 1} }
	if key < n.Key {
		n.Left = augInsert(n.Left, key)
	} else if key > n.Key {
		n.Right = augInsert(n.Right, key)
	}
	n.SubtreeSize = 1 + size(n.Left) + size(n.Right)
	return n
}

func (n *AugNode[K]) Rank(key K) int {
	if n == nil { return 0 }
	if key < n.Key { return n.Left.Rank(key) }
	leftSize := size(n.Left)
	if key == n.Key { return leftSize }
	return leftSize + 1 + n.Right.Rank(key)
}

func size[K cmp.Ordered](n *AugNode[K]) int {
	if n == nil { return 0 }
	return n.SubtreeSize
}
```

### Edge Cases & Pitfalls

- **Empty Tree:** Operations must handle nil root.
- **Duplicates:** Decide between overwrite or multiset policy.
- **Stack Overflow:** Deep trees break recursion. Use iterative DFS.
- **GC Pressure:** Millions of nodes tax tracing. Use slices for static data.

### Anti-Patterns

- **Unbalanced BST:** Sorted input turns BST into O(n) list. Use balancing.
- **Deep Recursion:** AVL deletes can trigger deep call chains. Use iterative logic.
- **Pointer Bloat:** Many heap allocations hurt performance. Use sorted slices for batch workloads.

## Quick Reference

| Name | Go Type | Time | Memory / GC | Use Case |
|------|---------|------|-------|----------|
| Generic BST | `*Node[K, V]` | <code>O(h)</code> | High | Dynamic order |
| AVL Tree | `*AVLNode[K, V]` | <code>O(log n)</code> | High | Guaranteed bounds |
| Sorted Slice | `[]T` | <code>O(log n)</code> | Zero | Static read-heavy |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Use generics for type-safe trees. Monitor GC costs of pointer-based structures. Slices are better for static data.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/chapter-12/)
- [Chapter 44: B-Trees](/docs/part-ix/chapter-44/)
