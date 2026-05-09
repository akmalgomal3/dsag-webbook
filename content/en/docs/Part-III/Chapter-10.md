---
weight: 30200
title: "Chapter 10 - Heaps and Priority Queues"
description: "Heaps and Priority Queues"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The best way to predict the future is to invent it.</em>" — Alan Kay</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 10 covers heaps and priority queues: tree-based structures for efficient access to the maximum or minimum element. Essential for scheduling, graph algorithms, and top-k problems.
{{% /alert %}}

## 10.1. Binary Heap

**Definition:** A binary heap is a complete binary tree where each parent is greater than (max-heap) or less than (min-heap) its children. It supports extract-max and insert in <code>O(log n)</code>.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Insert | <code>O(log n)</code> | Add at end, bubble up |
| Extract Max/Min | <code>O(log n)</code> | Remove root, heapify down |
| Peek | <code>O(1)</code> | View root without removal |
| Build Heap | <code>O(n)</code> | Bottom-up heapify |

## 10.2. Priority Queue

**Definition:** A priority queue is an abstract data type where each element has a priority. The highest-priority element is served first. A heap is the canonical implementation.

### Idiomatic Go Implementation

Go's `container/heap` provides a heap interface. Wrap it with generics for type safety.

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

func (h *IntHeap) Push(x interface{}) {
	*h = append(*h, x.(int))
}

func (h *IntHeap) Pop() interface{} {
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
| Need frequent max/min access | Only sequential access needed |
| Implementing Dijkstra's algorithm | Data is already sorted |
| Top-k problems | Random access required |

### Edge Cases & Pitfalls

- **Stability:** Standard heaps are not stable; ties broken arbitrarily.
- **Update priority:** Decreasing a key requires bubble-up; not directly supported by `container/heap`.
- **Memory layout:** Heap as array has excellent cache locality compared to tree pointers.

## 10.4. Quick Reference

| Structure | Go Type | Insert | Extract | Peek | Use Case |
|-----------|---------|--------|---------|------|----------|
| Min Heap | `[]int` + interface | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(1)</code> | Dijkstra, scheduling |
| Max Heap | `[]int` + interface | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(1)</code> | Median finding |
| Priority Queue | `container/heap` | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(1)</code> | Task queues |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 10:</strong> Heaps provide <code>O(log n)</code> insertion and extraction of extreme elements, making them ideal for priority queues and graph algorithms. In Go, use <code>container/heap</code> with a generic wrapper for type-safe priority queues. Remember that heaps excel at extreme-value access, not general searching.
{{% /alert %}}

## See Also

- [Chapter 9 — Trees and Balanced Trees](/docs/Part-III/Chapter-9/)
- [Chapter 16 — Minimum Spanning Trees](/docs/Part-IV/Chapter-16/)
- [Chapter 22 — Median and Order Statistics](/docs/Part-V/Chapter-22/)

