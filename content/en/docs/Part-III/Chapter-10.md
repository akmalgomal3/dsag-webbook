---
weight: 30200
title: "Chapter 10: Heaps and Priority Queues"
description: "Heaps and Priority Queues"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The best way to predict the future is to invent it.</em>" : Alan Kay</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 10 covers heaps and priority queues. Use these for scheduling, graph algorithms, and top-k problems.
{{% /alert %}}

## 10.1. Binary Heap

**Definition:** Binary heap is a complete binary tree. Parent is always greater than (max-heap) or less than (min-heap) its children.

**Mechanics:**
Binary heap optimizes extreme element retrieval. Sacrifices full searchability for fast min/max access. Partial ordering reduces operations compared to full sorting.

Heap uses flat array mapping. Indices compute parent and child locations without pointers. Left child is `2*i + 1`. Right child is `2*i + 2`. Parent is `(i-1)/2`. Array layout ensures high cache hit rates.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Insert | <code>O(log n)</code> | Add at end, bubble up |
| Extract | <code>O(log n)</code> | Remove root, heapify down |
| Peek | <code>O(1)</code> | View root |
| Build Heap | <code>O(n)</code> | Bottom-up heapify |

## 10.2. Priority Queue

**Definition:** Priority queue serves highest-priority elements first. Heap is the standard implementation.

**Mechanics:**
Priority queue prioritizes by weight rather than arrival time. Essential for network routing and task scheduling.

Go `container/heap` applies methods to a slice. `Push` appends to slice and bubbles up. `Pop` swaps with end and sinks down. Memory writes stay within contiguous array.

### Idiomatic Go Implementation

```go
package main

import (
	"container/heap"
	"fmt"
)

type IntHeap []int

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] < h[j] } // Min-heap
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *IntHeap) Push(x any) {
	*h = append(*h, x.(int))
}

func (h *IntHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func main() {
	h := &IntHeap{}
	heap.Init(h)
	heap.Push(h, 3)
	heap.Push(h, 1)
	heap.Push(h, 4)
	fmt.Println((*h)[0])       // 1 (peek)
	fmt.Println(heap.Pop(h))   // 1
	fmt.Println(heap.Pop(h))   // 3
	fmt.Println(heap.Pop(h))   // 4
}
```

## 10.3. Decision Matrix

| Use Heap When... | Avoid If... |
|------------------|-------------|
| Frequent min/max access needed | Random access required |
| Implementing Dijkstra | Data is already sorted |
| Top-k problems | Only sequential access needed |

### Edge Cases & Pitfalls

- **Stability:** Heaps do not preserve relative order of equal elements.
- **Priority updates:** `container/heap` does not natively support `DecreaseKey`.
- **Memory:** Array-based heaps outperform pointer-based trees in cache efficiency.

### Anti-Patterns

- **Frequent Sorting:** Calling `sort.Sort` on every insert is O(n log n). Use heap for O(log n).
- **Missing Init:** Appending to slice without `heap.Init` breaks invariants. Always initialize.
- **Lazy Delete:** `container/heap` lacks priority updates. Push new values and skip stale entries during `Pop`.

## 10.4. Quick Reference

| Structure | Go Type | Insert | Extract | Peek | Use Case |
|-----------|---------|--------|---------|------|----------|
| Min Heap | `[]int` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(1)</code> | Dijkstra |
| Max Heap | `[]int` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(1)</code> | Median |
| Priority Queue | `heap.Interface` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(1)</code> | Task queue |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Heaps allow fast extreme-value access. Use for priority queues and graph algorithms. Not for general searching.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
- [Chapter 16: Minimum Spanning Trees](/docs/part-iv/chapter-16/)
