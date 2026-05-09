---
weight: 3100
title: "Chapter 9 - Trees and Balanced Trees"
description: "Trees and Balanced Trees"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The oak fought the wind and was broken, the willow bent when it must and survived.</em>" — Robert Jordan</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 9 covers tree data structures: binary search trees, self-balancing trees (AVL, Red-Black), and their operations. Understand tree rotations and when balance matters.
{{% /alert %}}

## 9.1. Binary Search Tree (BST)

**Definition:** A BST is a binary tree where each node's left subtree contains only values less than the node, and the right subtree contains only values greater.

### Operations & Complexity

| Operation | Average | Worst | Description |
|-----------|---------|-------|-------------|
| Search | <code>O(log n)</code> | <code>O(n)</code> | Unbalanced degenerates to list |
| Insert | <code>O(log n)</code> | <code>O(n)</code> | Find position, attach |
| Delete | <code>O(log n)</code> | <code>O(n)</code> | Three cases |

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

**Definition:** An AVL tree is a self-balancing BST where the height difference between subtrees of any node is at most 1. Balance is maintained through rotations.

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

## 9.3. Decision Matrix

| Use BST When... | Use Balanced Tree When... |
|-----------------|---------------------------|
| Data is random or mostly static | Frequent insertions/deletions |
| Memory is extremely constrained | Worst-case guarantees required |
| Simple implementation preferred | <code>O(n)</code> worst-case unacceptable |

### Edge Cases & Pitfalls

- **Degenerate tree:** Sorted input creates a linked list; always use balanced trees for dynamic data.
- **Go generics:** Go 1.18+ enables type-safe generic trees using `constraints.Ordered`.
- **GC overhead:** Tree nodes are individually allocated; large trees create GC pressure.

## 9.4. Quick Reference

| Tree | Height | Search | Insert | Delete | Balance |
|------|--------|--------|--------|--------|---------|
| BST (random) | <code>O(log n)</code> avg | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | None |
| BST (sorted) | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> | None |
| AVL Tree | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | Strict |
| Red-Black | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | Relaxed |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 9:</strong> Binary search trees provide efficient ordered storage but require balancing for guaranteed performance. AVL trees offer strict balance with more rotations; Red-Black trees trade slightly less balance for simpler insertion/deletion. In Go, prefer the standard library's <code>container/rbtree</code> (if available) or implement generics-based trees for type safety.
{{% /alert %}}
