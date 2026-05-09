---
weight: 6300
title: "Chapter 25 - Greedy Algorithms"
description: "Greedy Algorithms"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Greed, for lack of a better word, is good.</em>" — Gordon Gekko</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 25 covers greedy algorithms: making locally optimal choices at each step to find a global optimum. Learn when greediness works and when it fails.
{{% /alert %}}

## 25.1. Greedy Strategy

**Definition:** A greedy algorithm builds a solution piece by piece, always choosing the next piece that offers the most immediate benefit. It works only when the problem has the **greedy choice property** and **optimal substructure**.

### When Greedy Works

| Problem | Greedy Choice | Proof |
|---------|--------------|-------|
| Fractional Knapsack | Highest value/weight ratio | Exchange argument |
| Activity Selection | Earliest finish time | Staying ahead |
| Huffman Coding | Lowest frequency pair | Cut-and-paste |
| Minimum Spanning Tree | Lightest safe edge | Cut property |

## 25.2. Fractional Knapsack

**Definition:** Given items with weights and values, fill a knapsack to maximize value. Unlike 0/1 knapsack, you can take fractions of items.

### Idiomatic Go Implementation

Sort by value-to-weight ratio in descending order.

```go
package main

import (
	"fmt"
	"sort"
)

type Item struct {
	Weight int
	Value  int
}

func fractionalKnapsack(items []Item, capacity int) float64 {
	sort.Slice(items, func(i, j int) bool {
		vi := float64(items[i].Value) / float64(items[i].Weight)
		vj := float64(items[j].Value) / float64(items[j].Weight)
		return vi > vj
	})
	
	var total float64
	for _, item := range items {
		if capacity >= item.Weight {
			total += float64(item.Value)
			capacity -= item.Weight
		} else {
			total += float64(item.Value) * float64(capacity) / float64(item.Weight)
			break
		}
	}
	return total
}

func main() {
	items := []Item{{10, 60}, {20, 100}, {30, 120}}
	fmt.Println(fractionalKnapsack(items, 50)) // 240
}
```

## 25.3. Activity Selection

**Definition:** Given activities with start and finish times, select the maximum number of non-overlapping activities.

### Idiomatic Go Implementation

Always pick the activity with the earliest finish time.

```go
package main

import (
	"fmt"
	"sort"
)

type Activity struct {
	Start  int
	Finish int
}

func activitySelection(activities []Activity) []Activity {
	sort.Slice(activities, func(i, j int) bool {
		return activities[i].Finish < activities[j].Finish
	})
	
	var selected []Activity
	var lastFinish int
	for _, act := range activities {
		if act.Start >= lastFinish {
			selected = append(selected, act)
			lastFinish = act.Finish
		}
	}
	return selected
}

func main() {
	acts := []Activity{{1, 4}, {3, 5}, {0, 6}, {5, 7}, {3, 8}, {5, 9}}
	fmt.Println(len(activitySelection(acts))) // 4
}
```

## 25.4. Huffman Coding

**Definition:** Huffman coding constructs an optimal prefix-free binary code by greedily merging the two least frequent symbols.

### Idiomatic Go Implementation

Use `container/heap` for the priority queue.

```go
package main

import (
	"container/heap"
	"fmt"
)

type Node struct {
	Char  rune
	Freq  int
	Left  *Node
	Right *Node
}

type NodeHeap []*Node

func (h NodeHeap) Len() int           { return len(h) }
func (h NodeHeap) Less(i, j int) bool { return h[i].Freq < h[j].Freq }
func (h NodeHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *NodeHeap) Push(x interface{}) { *h = append(*h, x.(*Node)) }
func (h *NodeHeap) Pop() interface{} {
	old := *h
	n := len(old)
	*h = old[:n-1]
	return old[n-1]
}

func buildHuffman(freq map[rune]int) *Node {
	h := &NodeHeap{}
	heap.Init(h)
	for ch, f := range freq {
		heap.Push(h, &Node{Char: ch, Freq: f})
	}
	for h.Len() > 1 {
		a := heap.Pop(h).(*Node)
		b := heap.Pop(h).(*Node)
		heap.Push(h, &Node{Freq: a.Freq + b.Freq, Left: a, Right: b})
	}
	return heap.Pop(h).(*Node)
}

func main() {
	freq := map[rune]int{'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
	root := buildHuffman(freq)
	fmt.Println(root.Freq) // 100
}
```

## 25.5. Decision Matrix

| Use Greedy When... | Avoid If... |
|--------------------|-------------|
| Greedy choice property provably holds | Local optimum ≠ global optimum |
| Need fast, simple approximation | Exact optimal solution required |
| Problem structure supports exchange argument | Counterexamples exist (e.g., 0/1 knapsack) |

### Edge Cases & Pitfalls

- **Proving correctness:** Always verify the greedy choice property before implementing.
- **Fractional vs 0/1:** Greedy works for fractional knapsack but fails for 0/1 knapsack.
- **Tie-breaking:** When multiple choices have equal value, the tie-breaking strategy matters.

## 25.6. Quick Reference

| Problem | Greedy Choice | Time | Space | Optimal? |
|---------|--------------|------|-------|----------|
| Fractional Knapsack | Max value/weight | <code>O(n log n)</code> | <code>O(1)</code> | Yes |
| Activity Selection | Earliest finish | <code>O(n log n)</code> | <code>O(1)</code> | Yes |
| Huffman Coding | Min frequency pair | <code>O(n log n)</code> | <code>O(n)</code> | Yes |
| 0/1 Knapsack | — | — | — | No (use DP) |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 25:</strong> Greedy algorithms provide fast, elegant solutions when the greedy choice property holds. Always verify correctness with an exchange argument or counterexample before relying on a greedy approach. In Go, leverage `sort.Slice` and `container/heap` for efficient implementation.
{{% /alert %}}
