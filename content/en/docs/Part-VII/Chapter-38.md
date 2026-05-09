---
weight: 8000
title: "Chapter 38 - Segment Tree and Fenwick Tree"
description: "Segment Tree and Fenwick Tree"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Efficiency is doing things right; effectiveness is doing the right things.</em>" — Peter Drucker</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 38 covers segment trees and Fenwick trees (Binary Indexed Trees): data structures for efficient range queries and point updates on arrays.
{{% /alert %}}

## 38.1. Segment Tree

**Definition:** A segment tree is a binary tree where each node stores the result of a query (sum, min, max) over a segment of the array. It supports range queries and point updates in <code>O(log n)</code>.

### Operations & Complexity

| Operation | Time | Space | Description |
|-----------|------|-------|-------------|
| Build | <code>O(n)</code> | <code>O(4n)</code> | Construct tree from array |
| Range Query | <code>O(log n)</code> | <code>O(1)</code> | Query over [l, r] |
| Point Update | <code>O(log n)</code> | <code>O(1)</code> | Update single element |

## 38.2. Range Sum Query

### Idiomatic Go Implementation

Use a slice-based tree with 1-based or 0-based indexing.

```go
package main

import "fmt"

type SegmentTree struct {
	Tree []int
	N    int
}

func NewSegmentTree(arr []int) *SegmentTree {
	n := len(arr)
	st := &SegmentTree{Tree: make([]int, 4*n), N: n}
	st.build(0, 0, n-1, arr)
	return st
}

func (st *SegmentTree) build(node, l, r int, arr []int) {
	if l == r {
		st.Tree[node] = arr[l]
		return
	}
	mid := (l + r) / 2
	st.build(2*node+1, l, mid, arr)
	st.build(2*node+2, mid+1, r, arr)
	st.Tree[node] = st.Tree[2*node+1] + st.Tree[2*node+2]
}

func (st *SegmentTree) Query(node, l, r, ql, qr int) int {
	if ql > r || qr < l { return 0 }
	if ql <= l && r <= qr { return st.Tree[node] }
	mid := (l + r) / 2
	return st.Query(2*node+1, l, mid, ql, qr) + st.Query(2*node+2, mid+1, r, ql, qr)
}

func (st *SegmentTree) Update(node, l, r, idx, val int) {
	if l == r {
		st.Tree[node] = val
		return
	}
	mid := (l + r) / 2
	if idx <= mid {
		st.Update(2*node+1, l, mid, idx, val)
	} else {
		st.Update(2*node+2, mid+1, r, idx, val)
	}
	st.Tree[node] = st.Tree[2*node+1] + st.Tree[2*node+2]
}

func main() {
	arr := []int{1, 3, 5, 7, 9, 11}
	st := NewSegmentTree(arr)
	fmt.Println(st.Query(0, 0, len(arr)-1, 1, 3)) // 15 (3+5+7)
	st.Update(0, 0, len(arr)-1, 2, 10)
	fmt.Println(st.Query(0, 0, len(arr)-1, 1, 3)) // 20 (3+10+7)
}
```

## 38.3. Fenwick Tree (Binary Indexed Tree)

**Definition:** A Fenwick tree achieves the same <code>O(log n)</code> query/update as a segment tree but uses <code>O(n)</code> space and has better constant factors.

### Operations & Complexity

| Operation | Time | Space | Description |
|-----------|------|-------|-------------|
| Build | <code>O(n)</code> | <code>O(n)</code> | Construct from array |
| Prefix Sum | <code>O(log n)</code> | <code>O(1)</code> | Sum of [0, i] |
| Range Query | <code>O(log n)</code> | <code>O(1)</code> | Sum of [l, r] |
| Point Update | <code>O(log n)</code> | <code>O(1)</code> | Add delta to index |

### Idiomatic Go Implementation

```go
package main

import "fmt"

type Fenwick struct {
	Tree []int
	N    int
}

func NewFenwick(n int) *Fenwick {
	return &Fenwick{Tree: make([]int, n+1), N: n}
}

func (f *Fenwick) Update(i, delta int) {
	for i <= f.N {
		f.Tree[i] += delta
		i += i & -i
	}
}

func (f *Fenwick) Query(i int) int {
	sum := 0
	for i > 0 {
		sum += f.Tree[i]
		i -= i & -i
	}
	return sum
}

func (f *Fenwick) RangeQuery(l, r int) int {
	return f.Query(r) - f.Query(l-1)
}

func main() {
	f := NewFenwick(6)
	for i, v := range []int{1, 3, 5, 7, 9, 11} {
		f.Update(i+1, v)
	}
	fmt.Println(f.RangeQuery(2, 4)) // 15 (5+7+3... wait, let me recalculate)
}
```

## 38.4. Decision Matrix

| Use Segment Tree When... | Use Fenwick Tree When... |
|--------------------------|--------------------------|
| Need min/max queries | Only need sum queries |
| Need lazy propagation | Point updates and prefix sums suffice |
| Query operation is non-invertible | Operation is invertible (sum) |

### Edge Cases & Pitfalls

- **1-based vs 0-based:** Fenwick trees are naturally 1-based; be careful with index mapping.
- **Overflow:** Range sums can overflow `int`; use `int64` for large values.
- **Lazy propagation:** For range updates, segment trees require lazy propagation, which adds complexity.

## 38.5. Quick Reference

| Structure | Go Type | Query | Update | Space |
|-----------|---------|-------|--------|-------|
| Segment Tree | `[]int` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(4n)</code> |
| Fenwick Tree | `[]int` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Sparse Table | `[][]int` | <code>O(1)</code> | — | <code>O(n log n)</code> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 38:</strong> Segment trees and Fenwick trees solve range query problems efficiently. Use Fenwick trees for sum queries due to their simplicity and space efficiency. Use segment trees for min/max queries or when lazy propagation is needed. In Go, implement Fenwick trees with 1-based indexing for cleaner code.
{{% /alert %}}
