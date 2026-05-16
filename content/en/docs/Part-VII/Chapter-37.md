---
weight: 71000
title: "Chapter 37: Segment Tree and Fenwick Tree"
description: "Segment Tree and Fenwick Tree"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Efficiency is doing things right; effectiveness is doing the right things.</em>" : Peter Drucker</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 37 covers <abbr title="A binary tree for range queries storing aggregated results over array segments.">segment trees</abbr> and <abbr title="A tree structure for efficient prefix sum queries using bitwise operations.">Fenwick trees</abbr>. Efficient range queries and point updates on arrays.
{{% /alert %}}

## 38.1. Segment Tree

**Definition:** Binary tree storing query results (sum, min, max) over array segments. Supports <code>O(log n)</code> range queries and point updates.

**Background:**
Precomputed aggregation. Linear scans are slow for repeated queries. Trees pre-calculate chunks hierarchically. Traversal follows <code>O(log n)</code> boundaries.

**Use Cases:**
Competitive programming. Dynamic financial ledgers. 2D game rendering visibility.

**Memory Mechanics:**
Array-based storage used. Segment Tree requires `4*n` size. Fenwick Tree uses `n+1` size. Fenwick uses bitwise jumps (`i & -i`). <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">Contiguous</abbr> layout optimizes <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> performance. Zero <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">GC</abbr> overhead during updates.

### Operations & Complexity

| Operation | Time | Space | Description |
|-----------|------|-------|-------------|
| Build | <code>O(n)</code> | <code>O(4n)</code> | Construct tree from array |
| Range Query | <code>O(log n)</code> | <code>O(1)</code> | Query over [l, r] |
| Point Update | <code>O(log n)</code> | <code>O(1)</code> | Update single element |

## 38.2. Range Sum Query

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

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

**Definition:** Fenwick tree achieves <code>O(log n)</code> query/update. Uses <code>O(n)</code> space. Efficient constant factors.

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
	fmt.Println(f.RangeQuery(2, 4)) // 15
}
```

## 38.4. Decision Matrix

| Use Segment Tree When... | Use Fenwick Tree When... |
|--------------------------|--------------------------|
| Min/max queries required | Sum queries suffice |
| Lazy propagation needed | Point updates are enough |
| Query is non-invertible | Operation is invertible (sum) |

### Edge Cases & Pitfalls

- **1-based indexing:** Fenwick trees are 1-based. Map indices carefully.
- **Overflow:** Use `int64` for large range sums.
- **Lazy propagation:** Segment trees require it for range updates. Complexity increases.

### Anti-Patterns

- **Index mixing:** Go arrays are 0-based. Fenwick trees use 1-based logic. Add 1 on input. Subtract 1 on output.
- **Over-engineering:** Using segment trees for simple sum queries is inefficient. Use Fenwick trees for <code>O(n)</code> space.
- **Missing lazy propagation:** Range updates without it take <code>O(n)</code>. System performance degrades.

## 38.5. Quick Reference

| Structure | Go Type | Query | Update | Space |
|-----------|---------|-------|--------|-------|
| Segment Tree | `[]int` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(4n)</code> |
| Fenwick Tree | `[]int` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Sparse Table | `[][]int` | <code>O(1)</code> | . | <code>O(n log n)</code> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 37:</strong> Segment and Fenwick trees handle range queries efficiently. Use Fenwick for sum queries. Use Segment trees for min/max or range updates. Implement Fenwick with 1-based indexing in Go.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
- [Chapter 32: Linear Programming](/docs/part-vii/chapter-32/)
- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
