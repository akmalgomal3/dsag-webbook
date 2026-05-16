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
<strong>"<em>The oak fought the wind and was broken, the willow bent when it must and survived.</em>" — Robert Jordan</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 9 covers BST, AVL, and Red-Black trees. Understand rotations and height balance.
{{% /alert %}}

## 9.1. Binary Search Tree (BST)

**Definition:** Binary Search Tree stores nodes where left child is smaller and right child is larger than parent.

**Mechanics:**
BST combines list flexibility with O(log n) search speed. Search follows left or right paths based on value comparison.

Nodes reside in non-contiguous memory on heap. Each node takes two pointers. Scattered allocations cause cache misses. Memory footprint is high due to pointer overhead.

### Operations & Complexity

| Operation | Average | Worst | Description |
|-----------|---------|-------|-------------|
| Search | <code>O(log n)</code> | <code>O(n)</code> | Unbalanced tree degrades to list |
| Insert | <code>O(log n)</code> | <code>O(n)</code> | Find position, attach node |
| Delete | <code>O(log n)</code> | <code>O(n)</code> | Reassign pointers |

### Idiomatic Go Implementation

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

**Definition:** AVL tree is self-balancing BST. Maximum height difference between subtrees is 1.

**Mechanics:**
Standard BST degrades to linked list on sorted input. AVL enforces balance via rotations. Sacrifices insertion speed for search guarantees.

Nodes store height value. Rotation swaps pointers without heap allocation. Pointer swapping is O(1).

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Search | <code>O(log n)</code> | Height balance guaranteed |
| Insert | <code>O(log n)</code> | Rotation keeps tree short |
| Delete | <code>O(log n)</code> | Rebalance up the tree |

### Rotations

| Rotation | Condition | Action |
|----------|-----------|--------|
| Left Rotation | Right-heavy | Rotate left around node |
| Right Rotation | Left-heavy | Rotate right around node |
| Left-Right | Left child right-heavy | Left rotate child, right rotate node |
| Right-Left | Right child left-heavy | Right rotate child, left rotate node |

### Idiomatic Go Implementation

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
		return root
	}
	root.Height = 1 + max(height(root.Left), height(root.Right))

	bf := balanceFactor(root)
	if bf > 1 && key < root.Left.Key { return rotateRight(root) }
	if bf < -1 && key > root.Right.Key { return rotateLeft(root) }
	if bf > 1 && key > root.Left.Key {
		root.Left = rotateLeft(root.Left)
		return rotateRight(root)
	}
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
	inorder(root) // 10 20 25 30 40 50
}
```

## 9.3. Decision Matrix

| Use BST When... | Use Balanced Tree When... |
|-----------------|---------------------------|
| Data is random | Frequent changes occur |
| Memory is low | Worst-case O(log n) needed |
| Simple code suffices | O(n) worst-case is unacceptable |

### Edge Cases & Pitfalls

- **Degeneration:** Sorted input breaks standard BST. Use balanced trees.
- **Go Generics:** Use `cmp.Ordered` for type-safe keys.
- **GC Pressure:** Tree nodes are scattered on heap. Reclaims via garbage collector.

### Anti-Patterns

- **Useless Trees:** Using BST when `map` works. Use `map` for simple key-value.
- **Type Erosion:** Using `any` instead of generics. Use `cmp.Ordered` for safety.
- **Stack Overflow:** Deep trees break recursion. Use iterative stack for depth.
- **Allocation Spam:** Millions of nodes tax GC. Use sync.Pool or flat slices.

## 9.4. Quick Reference

| Tree | Height | Search | Insert | Delete | Balance |
|------|--------|--------|--------|--------|---------|
| BST (random) | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | None |
| BST (sorted) | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> | None |
| AVL Tree | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | Strict |
| Red-Black | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | Relaxed |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> BST provides ordered storage. AVL keeps strict balance. Red-Black trade balance for insertion speed.
{{% /alert %}}

## See Also

- [Chapter 10: Heaps and Priority Queues](/docs/part-iii/chapter-10/)
- [Chapter 11: Disjoint Sets](/docs/part-iii/chapter-11/)
- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
