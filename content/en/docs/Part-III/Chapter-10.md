---
weight: 30200
title: "Chapter 10: Heaps and Priority Queues"
description: "Heaps and Priority Queues"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The best way to predict the future is to invent it.</em>" : Alan Kay</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 10 covers heaps and priority queues: tree-based structures for efficient access to the maximum or minimum element. Essential for scheduling, graph algorithms, and top-k problems.
{{% /alert %}}

## 10.1. Binary Heap

**Definition:** A binary heap is a complete binary tree where each parent is greater than (max-heap) or less than (min-heap) its children. It supports extract-max and insert in <code>O(log n)</code>.

**Background & Philosophy:**
While standard binary trees are optimized for searching any arbitrary element in <code>O(log n)</code> time, a heap sacrifices full searchability to absolutely optimize retrieving the single most important element (the min or max). The philosophy is "partial ordering". By only enforcing ordering between parent and child (and not between siblings), the heap drastically reduces the number of operations needed to insert or extract data compared to a fully sorted array or a balanced BST.

**Use Cases:**
Essential for implementing Priority Queues in operating system task schedulers, finding the shortest path in graph algorithms like Dijkstra's, and solving "Top K" streaming problems (e.g., maintaining the leaderboard of the top 100 players in real-time).

**Memory Mechanics:**
The most brilliant aspect of a binary heap is its memory mapping. Although conceptually a tree, a heap is almost universally implemented using a flat, <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> array (or slice in Go). Mathematical formulas (`2*i + 1` for left child, `2*i + 2` for right child, `(i-1)/2` for parent) replace physical <abbr title="A variable that stores a memory address.">pointers</abbr>. This eliminates the memory overhead of pointers entirely and exploits <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr> to the maximum. Traversing a heap means moving sequentially through <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>, resulting in near-perfect <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> hit rates.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Insert | <code>O(log n)</code> | Add at end, bubble up |
| Extract Max/Min | <code>O(log n)</code> | Remove root, heapify down |
| Peek | <code>O(1)</code> | View root without removal |
| Build Heap | <code>O(n)</code> | Bottom-up heapify |

## 10.2. Priority Queue

**Definition:** A <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr> is an abstract data type where each element has a priority. The highest-priority element is served first. A heap is the canonical implementation.

**Background & Philosophy:**
A standard queue treats all elements equally (FIFO). A priority queue reflects the real world: some tasks are simply more important than others and must preempt the queue. The philosophy is "fairness based on weight, not arrival time".

**Use Cases:**
Used in routing network packets where VoIP traffic takes priority over file downloads, event-driven simulations, and Huffman coding for data compression.

**Memory Mechanics:**
In Go, `container/heap` is not a data structure itself, but rather a set of interface methods applied to your own slice. When you call `heap.Push()`, Go appends the item to your underlying slice (potentially triggering an <code>O(n)</code> memory reallocation if capacity is exceeded) and then performs memory swaps (exchanging values at different array indices) to "bubble up" the value. These swaps are purely <code>O(1)</code> memory writes within the <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> array.

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

- [Chapter 9: Trees and Balanced Trees](/docs/Part-III/Chapter-9/)
- [Chapter 16: Minimum Spanning Trees](/docs/Part-IV/Chapter-16/)
- [Chapter 22: Median and Order Statistics](/docs/Part-V/Chapter-22/)
