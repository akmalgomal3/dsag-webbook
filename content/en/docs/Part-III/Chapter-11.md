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
Chapter 11 focuses on <abbr title="A tree data structure in which each node has at most two children.">Binary Search Trees</abbr> (BST), AVL self-balancing trees, and tree augmentation techniques in Go using generics.
{{% /alert %}}

## 11.1. <abbr title="A binary tree where the left child is smaller and the right child is larger than the parent.">Binary Search Tree</abbr> (BST)

**Definition:** A BST is a node-based <abbr title="A tree data structure in which each node has at most two children.">binary tree</abbr> where the left <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> strictly contains keys less than the <abbr title="The topmost node in a tree data structure.">root</abbr>, and the right <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> contains keys greater than the <abbr title="The topmost node in a tree data structure.">root</abbr>. It provides structured ordering and efficient <abbr title="The process of finding a specific element in a data structure.">searching</abbr>.

**Background & Philosophy:**
The philosophy of a BST is to embed binary search directly into a dynamic data structure. While searching a sorted array is <code>O(log n)</code>, inserting into an array requires <code>O(n)</code> memory shifting. A BST allows <code>O(log n)</code> insertion by using a hierarchy of <abbr title="A variable that stores a memory address.">pointers</abbr>. This delegates the responsibility of maintaining order from the memory layout (array) to the structural linking (tree nodes).

**Use Cases:**
Used when maintaining a dynamically changing dataset that must be frequently queried in order, such as a real-time leaderboard, database indexing, or implementing an in-memory Set or Map where iterating keys in sorted order is required.

**Memory Mechanics:**
Every `Node` is a distinct allocation on the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>. Because these nodes are not <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr>, traversing down the tree (following the `Left` or `Right` pointers) causes <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr> at almost every step. In Go, an <abbr title="An interface with no methods that can hold any type">empty interface</abbr> `interface{}` used to hold arbitrary values adds an extra 16 bytes of overhead per node. Go 1.18 Generics remove this boxing overhead, allowing the compiler to pack the exact data type directly into the node struct, slightly improving <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Search | <code>O(h)</code> | h = <abbr title="The length of the longest path from a node to a leaf.">height</abbr>, <code>O(log n)</code> if perfectly balanced |
| Insert | <code>O(h)</code> | Traverses downward to find a valid <abbr title="A node with no children in a tree.">leaf</abbr> |
| Delete | <code>O(h)</code> | Handles three distinct cases: <abbr title="A node with no children in a tree.">leaf</abbr>, one <abbr title="A node directly connected to another node when moving away from the root.">child</abbr>, two children |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> 1.18+ Generic Implementation

A classic Go anti-pattern is creating trees using `interface{}` to hold arbitrary values, destroying type-safety and hurting performance. Utilizing Go 1.18 Generics (`[K cmp.Ordered, V any]`) creates a reusable, strongly-typed BST.

```go
package main

import (
	"fmt"
	"cmp"
)

// Node is a generic tree node holding an ordered Key and an arbitrary Value.
type Node[K cmp.Ordered, V any] struct {
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
While trees represent data hierarchically, **allocating millions of `*Node` structs scatters memory randomly across the <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>.** Every time you call `&Node{}`, you create work for the Go Garbage Collector. During a GC sweep, the <abbr title="The period during which a computer program is executing.">runtime</abbr> must painstakingly trace every single left and right <abbr title="A variable that stores a memory address.">pointer</abbr> across the entire <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr> <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>.
- **Mitigation:** If you need a massive <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> that is built once and rarely deleted from, consider implementing a <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> using a pre-allocated flat slice (`[]Node`) and integer indexes instead of raw memory <abbr title="A variable that stores a memory address.">pointers</abbr>.

## 11.2. Self-Balancing Trees (AVL)

**Definition:** Standard BSTs degenerate into <code>O(n)</code> linked lists if data is inserted in sorted order. AVL and Red-Black trees maintain an <code>O(log n)</code> <abbr title="The length of the longest path from a node to a leaf.">height</abbr> by executing structural rotations upon insertion or deletion.

**Background & Philosophy:**
Unpredictability is the enemy of scalable systems. A standard BST is unpredictable because its shape depends entirely on insertion order. Self-balancing trees embody the philosophy of proactive maintenance: spending a small amount of extra effort upfront (rotations) to prevent severe degradation later.

**Use Cases:**
Essential for backend indexing systems like the Linux completely fair scheduler (CFS) which uses a Red-Black tree to track process execution times, or building maps/sets where worst-case performance must be mathematically bounded.

**Memory Mechanics:**
Maintaining balance requires tracking tree depth or color. An AVL tree node usually adds an `int` or `int8` field to store the height. Because Go aligns structs to memory word boundaries, adding a single `int8` might still consume 8 bytes of padding depending on field ordering. The rotations themselves are remarkably cheap, executed by swapping three or four 64-bit pointers without allocating any new <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap memory</abbr>.

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
	"cmp"
)

func main() {
	// AVL tree demonstration: inserting keys
	var root *AVLNode[int, string]
	for _, kv := range []struct {
		k int
		v string
	}{ {10, "Ten"}, {20, "Twenty"}, {30, "Thirty"}, {40, "Forty"}, {50, "Fifty"}, {25, "Twenty-Five"} } {
		root = avlInsert(root, kv.k, kv.v)
	}
	// In-order traversal prints keys in sorted order
	avlInorder(root) // 10 20 25 30 40 50
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
	root.Height = 1 + avlMax(avlHeight(root.Left), avlHeight(root.Right))
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

func avlMax(a, b int) int {
	if a > b { return a }
	return b
}

func avlBalance[K cmp.Ordered, V any](n *AVLNode[K, V]) int {
	if n == nil { return 0 }
	return avlHeight(n.Left) - avlHeight(n.Right)
}

func avlInorder[K cmp.Ordered, V any](n *AVLNode[K, V]) {
	if n == nil { return }
	avlInorder(n.Left)
	fmt.Printf("%d ", n.Key)
	avlInorder(n.Right)
}

type AVLNode[K cmp.Ordered, V any] struct {
	Key    K
	Value  V
	Height int
	Left   *AVLNode[K, V]
	Right  *AVLNode[K, V]
}

```

### Decision Matrix

| Use Balanced Trees When... | Avoid If... |
|---------------------|------------------|
| You strictly mandate a guaranteed <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> <code>O(log n)</code> | Data is entirely static (sort a slice and use <abbr title="A search algorithm that finds the position of a target value within a sorted array.">binary search</abbr>) |
| Managing in-memory indexes | The heavy <abbr title="A variable that stores a memory address.">pointer</abbr> overhead and GC tracing stalls your application |

## 11.3. <abbr title="A hierarchical data structure with a root node and child nodes.">Tree</abbr> Augmentation

**Definition:** Augmentation involves injecting specialized metadata (such as <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> sizes or sums) directly into the <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> structs. This natively unlocks advanced capabilities like high-speed rank querying.

**Background & Philosophy:**
Trees are inherently recursive. Augmentation is based on the philosophy of dynamic programming applied to trees: caching aggregated information about a subtree directly at the root of that subtree. This prevents having to recursively calculate counts or sums repeatedly.

**Use Cases:**
Used in building Order Statistic Trees where you need to query "what is the 50th smallest element" in <code>O(log n)</code> time, or in interval trees which detect overlapping schedules in calendaring systems.

**Memory Mechanics:**
Adding an `int` field like `SubtreeSize` directly increases the size of the node. Every time a node is inserted or deleted, the system must traverse back up the tree to the root, updating this integer. This increases CPU instruction count, but involves no new memory allocations. It is pure integer arithmetic directly in the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> if the ancestors are still resident.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| <abbr title="A tree consisting of a node and all of its descendants.">Subtree</abbr> Size | <code>O(1)</code> | Read directly from the augmented field |
| Rank Query | <code>O(h)</code> | Derived recursively via <abbr title="A tree consisting of a node and all of its descendants.">subtree</abbr> sizes |

### Idiomatic Generic Augmentation

```go
package main

import (
	"fmt"
	"cmp"
)

func main() {
	var root *AugNode[int]
	vals := []int{50, 30, 70, 20, 40, 60, 80}
	for _, v := range vals {
		root = augInsert(root, v)
	}
	// Rank of 50 in the tree (0-indexed: should be 3)
	if n := root.Rank(50); n != -1 {
		fmt.Println("Rank of 50:", n) // Rank of 50: 3
	}
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

type AugNode[K cmp.Ordered] struct {
	Key         K
	SubtreeSize int
	Left, Right *AugNode[K]
}

func size[K cmp.Ordered](n *AugNode[K]) int {
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
- **Deep recursion:** Recursive traversal overflows stack on deep trees : use iterative DFS.
- **GC pressure:** Millions of tree nodes = heavy GC tracing; prefer sorted slices for static data.
- **Nil pointer dereference:** Always check node != nil before accessing fields.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type Implementation | Time | Memory / GC Pressure | Use Case |
|------|---------|------|-------|----------|
| Generic BST | `*Node[K, V]` | <code>O(h)</code> | Extremely High (<abbr title="A variable that stores a memory address.">pointer</abbr> chasing) | Fast ordered inserts |
| <abbr title="A self-balancing binary search tree with a balance factor of -1, 0, or 1.">AVL Tree</abbr> | `*AVLNode[K, V]` | <code>O(log n)</code> | Extremely High | Guaranteed <code>O(log n)</code> bounds |
| Sorted Slice | `[]T` | <code>O(log n)</code> search | Zero GC overhead | Read-heavy, static data |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 11:</strong> Generics `[K cmp.Ordered]` make tree implementations type-safe and reusable. Be aware of the GC cost: pointer-based trees generate heavy tracing pressure for large datasets. For static data, a sorted slice with `sort.Search` delivers <code>O(log n)</code> search with zero allocation overhead.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/chapter-12/)
- [Chapter 44: B-Trees](/docs/part-ix/chapter-44/)
