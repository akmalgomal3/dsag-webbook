---
weight: 30100
title: "Chapter 9: Trees and Balanced Trees"
description: "Trees and Balanced Trees"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The oak fought the wind and was broken, the willow bent when it must and survived.</em>" : Robert Jordan</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 9 covers tree data structures: binary search trees, self-balancing trees (AVL, Red-Black), and their operations. Understand tree rotations and when balance matters.
{{% /alert %}}

## 9.1. Binary Search Tree (BST)

**Definition:** A BST is a <abbr title="A tree where each node has at most two children">binary tree</abbr> where each node's left subtree contains only values less than the node, and the right subtree contains only values greater.

**Background & Philosophy:**
Trees mirror the hierarchical nature of human logic and decision-making. The philosophy of a <abbr title="A binary tree where the left child is smaller and the right child is larger than the parent.">Binary Search Tree (BST)</abbr> is to combine the dynamic <abbr title="The process of reserving memory for program use">memory allocation</abbr> flexibility of a linked list with the <code>O(log n)</code> search speed of a sorted array. It achieves this by enforcing a strict invariant: left is always smaller, right is always larger.

**Use Cases:**
Used in implementing sets and dictionaries, executing fast range queries (e.g., "find all users aged 20 to 30"), and powering the underlying autocomplete logic in modern search engines via Tries.

**Memory Mechanics:**
A standard BST is <abbr title="Memory blocks allocated in fragmented, separate locations.">non-contiguous</abbr>. Each `TreeNode` is allocated independently on the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> using `new` or `&TreeNode{}`. Because the nodes are scattered randomly in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>, traversing a tree forces the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> to constantly fetch new memory lines, resulting in high latency compared to scanning a flat array. Furthermore, every node carries the overhead of two 64-bit <abbr title="A variable that stores a memory address.">pointers</abbr> (`Left` and `Right`), which significantly increases the memory footprint per element.

### Operations & Complexity

| Operation | Average | Worst | Description |
|-----------|---------|-------|-------------|
| Search | <code>O(log n)</code> | <code>O(n)</code> | Unbalanced degenerates to list |
| Insert | <code>O(log n)</code> | <code>O(n)</code> | Find position, attach |
| Delete | <code>O(log n)</code> | <code>O(n)</code> | Three cases |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

```go
package main

import "fmt"

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func insert(root *TreeNode, val int) *TreeNode {
	if root == nil { return &TreeNode{Val: val} }
	if val < root.Val {
		root.Left = insert(root.Left, val)
	} else {
		root.Right = insert(root.Right, val)
	}
	return root
}

func search(root *TreeNode, val int) bool {
	if root == nil { return false }
	if val == root.Val { return true }
	if val < root.Val { return search(root.Left, val) }
	return search(root.Right, val)
}

func inorder(root *TreeNode) {
	if root == nil { return }
	inorder(root.Left)
	fmt.Printf("%d ", root.Val)
	inorder(root.Right)
}

func main() {
	var root *TreeNode
	for _, v := range []int{50, 30, 70, 20, 40, 60, 80} {
		root = insert(root, v)
	}
	fmt.Println(search(root, 40)) // true
	inorder(root)                 // 20 30 40 50 60 70 80
}
```

## 9.2. AVL Tree

**Definition:** An AVL tree is a self-balancing BST where the height difference between subtrees of any node is at most 1. Balance is maintained through rotations.

**Background & Philosophy:**
The philosophical problem with a standard BST is that sequential insertions (e.g., 1, 2, 3, 4) degrade the tree into a linked list, ruining the <code>O(log n)</code> guarantee. The AVL tree (named after Adelson-Velsky and Landis) solves this by enforcing a strict balance invariant. The philosophy is "correctness over insertion speed": it willingly sacrifices <code>O(1)</code> CPU cycles during insertion to perform rotations, ensuring that future search operations never degrade to <code>O(n)</code>.

**Use Cases:**
Ideal for read-heavy applications where searches vastly outnumber insertions and deletions, such as in-memory dictionary lookups or static indexing.

**Memory Mechanics:**
An AVL tree node requires an additional memory field to store the `Height` or `BalanceFactor` integer. This increases the struct size. During a rotation, memory addresses themselves do not change; only the <abbr title="A variable that stores a memory address.">pointers</abbr> (`Left` and `Right`) are reassigned. This <abbr title="Performing mathematical operations on memory addresses.">pointer swapping</abbr> is an <code>O(1)</code> operation and requires no new <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocations, making rotations extremely memory-efficient despite looking algorithmically complex.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Search | <code>O(log n)</code> | Height guaranteed <code>O(log n)</code> |
| Insert | <code>O(log n)</code> | Single or double rotation |
| Delete | <code>O(log n)</code> | Rebalance up the path |

### Rotations

| Rotation | Condition | Action |
|----------|-----------|--------|
| Left Rotation | Right-heavy, right child balanced or right-heavy | Rotate left around node |
| Right Rotation | Left-heavy, left child balanced or left-heavy | Rotate right around node |
| Left-Right | Left-heavy, left child right-heavy | Left rotate child, right rotate node |
| Right-Left | Right-heavy, right child left-heavy | Right rotate child, left rotate node |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

```go
package main

import (
	"fmt"
	"cmp"
)

type AVLNode[K cmp.Ordered] struct {
	Key    K
	Height int
	Left   *AVLNode[K]
	Right  *AVLNode[K]
}

func height[K cmp.Ordered](n *AVLNode[K]) int {
	if n == nil { return 0 }
	return n.Height
}

func balanceFactor[K cmp.Ordered](n *AVLNode[K]) int {
	if n == nil { return 0 }
	return height(n.Left) - height(n.Right)
}

func rotateRight[K cmp.Ordered](y *AVLNode[K]) *AVLNode[K] {
	x := y.Left
	T2 := x.Right
	x.Right = y
	y.Left = T2
	y.Height = max(height(y.Left), height(y.Right)) + 1
	x.Height = max(height(x.Left), height(x.Right)) + 1
	return x
}

func rotateLeft[K cmp.Ordered](x *AVLNode[K]) *AVLNode[K] {
	y := x.Right
	T2 := y.Left
	y.Left = x
	x.Right = T2
	x.Height = max(height(x.Left), height(x.Right)) + 1
	y.Height = max(height(y.Left), height(y.Right)) + 1
	return y
}

func avlInsert[K cmp.Ordered](root *AVLNode[K], key K) *AVLNode[K] {
	if root == nil { return &AVLNode[K]{Key: key, Height: 1} }
	if key < root.Key {
		root.Left = avlInsert(root.Left, key)
	} else if key > root.Key {
		root.Right = avlInsert(root.Right, key)
	} else {
		return root // duplicate keys not allowed
	}
	root.Height = 1 + max(height(root.Left), height(root.Right))

	bf := balanceFactor(root)
	// Left Heavy
	if bf > 1 && key < root.Left.Key { return rotateRight(root) }
	// Right Heavy
	if bf < -1 && key > root.Right.Key { return rotateLeft(root) }
	// Left-Right
	if bf > 1 && key > root.Left.Key {
		root.Left = rotateLeft(root.Left)
		return rotateRight(root)
	}
	// Right-Left
	if bf < -1 && key < root.Right.Key {
		root.Right = rotateRight(root.Right)
		return rotateLeft(root)
	}
	return root
}

func inorder[K cmp.Ordered](root *AVLNode[K]) {
	if root == nil { return }
	inorder(root.Left)
	fmt.Printf("%v(h=%d) ", root.Key, root.Height)
	inorder(root.Right)
}

func main() {
	var root *AVLNode[int]
	for _, v := range []int{10, 20, 30, 40, 50, 25} {
		root = avlInsert(root, v)
	}
	inorder(root) // 10 20 25 30 40 50 (balanced)
}
```

## 9.3. Decision Matrix

| Use BST When... | Use Balanced Tree When... |
|-----------------|---------------------------|
| Data is random or mostly static | Frequent insertions/deletions |
| Memory is extremely constrained | Worst-case guarantees required |
| Simple implementation preferred | <code>O(n)</code> worst-case unacceptable |

### Edge Cases & Pitfalls

- **Degenerate tree:** Sorted input creates a linked list; always use balanced trees for dynamic data.
- **Go generics:** Go 1.21+ enables type-safe generic trees using `cmp.Ordered` (the modern replacement for the deprecated `constraints.Ordered`).
- **GC overhead:** Tree nodes are individually allocated; large trees create <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">GC</abbr> pressure.

## 9.4. Quick Reference

| Tree | Height | Search | Insert | Delete | Balance |
|------|--------|--------|--------|--------|---------|
| BST (random) | <code>O(log n)</code> avg | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | None |
| BST (sorted) | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> | None |
| AVL Tree | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | Strict |
| Red-Black | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | Relaxed |

{{% alert icon="🎯" context="success" %}}
 <strong>Summary Chapter 9:</strong> Binary search trees provide efficient ordered storage but require balancing for guaranteed performance. AVL trees offer strict balance with more rotations; Red-Black trees trade slightly less balance for simpler insertion/deletion. Go has no Red-Black tree in the standard library — use generics-based trees for type safety or third-party packages.
{{% /alert %}}

## See Also

- [Chapter 10: Heaps and Priority Queues](/docs/part-iii/chapter-10/)
- [Chapter 11: Disjoint Sets](/docs/part-iii/chapter-11/)
- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
