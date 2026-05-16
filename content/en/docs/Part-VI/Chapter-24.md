---
weight: 60300
title: "Chapter 24: Greedy Algorithms"
description: "Greedy Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Local optimization wins.</em>" — Gordon Gekko</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Greedy algorithms make locally optimal choices. Goal: find <abbr title="The best possible solution over the entire search space">global optimum</abbr>. Fast but structure-dependent.
{{% /alert %}}

## 24.1. Greedy Strategy

**Definition:** A <abbr title="An algorithm making locally optimal choices at each step">greedy algorithm</abbr> builds solutions incrementally. It picks the immediate best choice. Requires **greedy choice property** and **<abbr title="Property where optimal solution contains optimal sub-solutions">optimal substructure</abbr>**.

**Mechanics:**
Greedy ignores the future. It never reconsiders past choices. Speed is the priority. Correctness depends on problem structure.

**Use Cases:**
- Network routing (<abbr title="An algorithm finding shortest paths in non-negative weighted graphs.">Dijkstra</abbr>).
- Data compression (<abbr title="A greedy algorithm for lossless data compression using variable-length codes.">Huffman coding</abbr>).
- Resource scheduling.

**Memory Management:**
Sorting precedes greedy choice. Sorting consumes <code>O(log n)</code> space. The greedy phase is a linear <code>O(n)</code> scan. Sequential access ensures high <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>.

### Effective Greedy Choices

| Problem | Choice | Proof |
|---------|--------|-------|
| Fractional Knapsack | Max value/weight ratio | Exchange argument |
| Activity Selection | Earliest finish time | Staying ahead |
| Huffman Coding | Lowest frequency pair | Cut-and-paste |
| Minimum Spanning Tree | Lightest safe edge | Cut property |

## 24.2. Fractional Knapsack

**Fact:** Items can be divided. Sort items by value/weight ratio. Take highest first.

### Go Implementation

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

## 24.3. Activity Selection

**Fact:** Maximize non-overlapping tasks. Sort by earliest finish time. Pick first available.

### Go Implementation

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

## 24.4. Huffman Coding

**Fact:** Optimal prefix codes. Merge two lowest frequencies repeatedly. Use priority queue.

### Go Implementation

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
func (h *NodeHeap) Push(x any) { *h = append(*h, x.(*Node)) }
func (h *NodeHeap) Pop() any {
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

## 24.5. Decision Matrix

| Use Greedy If... | Avoid If... |
|------------------|-------------|
| Greedy choice is optimal | Local choice blocks global best |
| Speed is required | Exact solution needed |
| Exchange argument holds | Counterexamples exist |

### Edge Cases & Pitfalls

- **Verification:** Prove greedy choice before coding.
- **Knapsack:** Greedy fails for 0/1 knapsack. Use DP.
- **Sorting:** Use stable sort if equal weights exist.

### Anti-Patterns

- **Greedy for 0/1 Knapsack:** Returns sub-optimal results. DP is required.
- **No Proof:** Coding without proving the exchange argument leads to silent failure.
- **Unstable Sorting:** Equal weights reorder unpredictably. Use `sort.SliceStable`.

## 24.6. Quick Reference

| Problem | Greedy Choice | Time | Space | Optimal? |
|---------|---------------|------|-------|----------|
| Fractional Knapsack | Max value/weight | <code>O(n log n)</code> | <code>O(1)</code> | Yes |
| Activity Selection | Earliest finish | <code>O(n log n)</code> | <code>O(1)</code> | Yes |
| Huffman Coding | Min frequency pair | <code>O(n log n)</code> | <code>O(n)</code> | Yes |
| 0/1 Knapsack | N/A | N/A | N/A | No |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Greedy algorithms trade reconsideration for speed. Verify with exchange argument. Use `sort.Slice` and `container/heap` in Go.
{{% /alert %}}

## See Also

- [Chapter 23: Dynamic Programming](/docs/part-vi/chapter-23/)
- [Chapter 25: Backtracking](/docs/part-vi/chapter-25/)
- [Chapter 35: Approximate Algorithms](/docs/part-vii/chapter-35/)
