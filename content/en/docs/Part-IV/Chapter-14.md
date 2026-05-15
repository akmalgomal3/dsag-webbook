---
weight: 40200
title: "Chapter 14: Single-Source Shortest Paths"
description: "Single-Source Shortest Paths"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The shortest path between two points is a straight line.</em>" : Archimedes</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 14 covers single-source shortest path algorithms: Dijkstra's algorithm and Bellman-Ford. Learn when to use each and how to implement them in Go.
{{% /alert %}}

## 14.1. Dijkstra's Algorithm

**Definition:** Dijkstra's algorithm finds the shortest paths from a source vertex to all other vertices in a <abbr title="A graph where each edge is assigned a weight or cost.">weighted graph</abbr> with non-negative <abbr title="A connection between two vertices in a graph.">edge</abbr> weights.

**Background & Philosophy:**
The core philosophy of Dijkstra is "greedy expansion with guaranteed finality." It fundamentally assumes that once the cheapest possible path to a node is discovered from the current frontier, no future path extending from other longer paths can ever be cheaper. This assumption mathematically holds true, but *only* if negative weights do not exist.

**Use Cases:**
Dijkstra is the foundation of network routing (like OSPF in IP networks) and mapping software (like finding the fastest driving route considering distance and speed limits).

**Memory Mechanics:**
Dijkstra algorithm's efficiency relies heavily on a <abbr title="A heap where each parent is less than or equal to its children">Min-Heap</abbr> (<abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority Queue</abbr>). In Go, this is a dynamically resizing slice that utilizes <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. When the algorithm "relaxes" an edge, it pushes a new `State` struct into the heap. Because the heap is contiguous, <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality during bubbling up/down operations is excellent. However, the `dist` (distance) array is accessed randomly based on graph topology, which can trigger <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr> in massive, highly-connected graphs.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Init | <code>O(V)</code> | Set distances to infinity |
| Extract min | <code>O(log V)</code> per extraction | <abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority queue</abbr> |
| Relax edges | <code>O(E)</code> total | Update distances |
| Total | <code>O((V + E) log V)</code> | With <abbr title="A heap implemented using a binary tree.">binary heap</abbr> |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

Use `container/heap` for the <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr>.

```go
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type Edge struct{ to, w int }
type Item struct{ v, d int }
type PQ []Item

func (p PQ) Len() int           { return len(p) }
func (p PQ) Less(i, j int) bool { return p[i].d < p[j].d }
func (p PQ) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }
func (p *PQ) Push(x interface{}) { *p = append(*p, x.(Item)) }
func (p *PQ) Pop() interface{} {
	old := *p
	n := len(old)
	*p = old[:n-1]
	return old[n-1]
}

func dijkstra(adj [][]Edge, src int) []int {
	n := len(adj)
	dist := make([]int, n)
	for i := range dist { dist[i] = math.MaxInt32 }
	dist[src] = 0
	pq := &PQ{{src, 0}}
	heap.Init(pq)
	for pq.Len() > 0 {
		u := heap.Pop(pq).(Item)
		if u.d > dist[u.v] { continue }
		for _, e := range adj[u.v] {
			if dist[u.v]+e.w < dist[e.to] {
				dist[e.to] = dist[u.v] + e.w
				heap.Push(pq, Item{e.to, dist[e.to]})
			}
		}
	}
	return dist
}

func main() {
	adj := [][]Edge{
		{{1, 4}, {2, 1}},
		{{3, 1}},
		{{1, 2}, {3, 5}},
		{},
	}
	fmt.Println(dijkstra(adj, 0)) // [0 3 1 4]
}
```

## 14.2. Bellman-Ford Algorithm

**Definition:** Bellman-Ford finds shortest paths from a single source in graphs with negative <abbr title="A connection between two vertices in a graph.">edge</abbr> weights (but no negative cycles).

**Background & Philosophy:**
While Dijkstra is greedy, Bellman-Ford is cautious and exhaustive. Its philosophy is based on dynamic programming: it assumes that any shortest path can have at most `V-1` edges. Therefore, by blindly relaxing all edges `V-1` times, the shortest distances must logically propagate to their final correct states.

**Use Cases:**
Essential in financial trading systems to detect arbitrage opportunities (currency exchange loops that yield net profit) by identifying negative weight cycles, and in certain distance-vector routing protocols.

**Memory Mechanics:**
Bellman-Ford doesn't require complex data structures like a Priority Queue. It strictly iterates over a simple 1D slice of distances and an `[]Edge` list. Because it iterates over the linear `[]Edge` list repeatedly, the CPU's branch predictor and prefetcher can stream the edge data from <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> into the L1 <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> with incredible efficiency. Despite its higher mathematical time complexity <code>O(VE)</code>, its memory access pattern is so hardware-friendly that it often performs well on small-to-medium graphs.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Relax all edges | <code>O(E)</code> per <abbr title="The repetition of a process, typically using loops.">iteration</abbr> | V-1 iterations |
| Detect negative <abbr title="A path that starts and ends at the same vertex.">cycle</abbr> | <code>O(E)</code> | One extra <abbr title="The repetition of a process, typically using loops.">iteration</abbr> |
| Total | <code>O(VE)</code> | Slower than Dijkstra |

### Idiomatic Go Implementation

```go
package main

import (
	"fmt"
	"math"
)

type BellmanEdge struct{ from, to, w int }

func bellmanFord(edges []BellmanEdge, n, src int) ([]int, bool) {
	dist := make([]int, n)
	for i := range dist { dist[i] = math.MaxInt32 }
	dist[src] = 0
	for i := 0; i < n-1; i++ {
		for _, e := range edges {
			if dist[e.from] != math.MaxInt32 && dist[e.from]+e.w < dist[e.to] {
				dist[e.to] = dist[e.from] + e.w
			}
		}
	}
	for _, e := range edges {
		if dist[e.from] != math.MaxInt32 && dist[e.from]+e.w < dist[e.to] {
			return nil, false // Negative cycle
		}
	}
	return dist, true
}

func main() {
	edges := []BellmanEdge{{0, 1, -1}, {0, 2, 4}, {1, 2, 3}, {1, 3, 2}, {3, 2, 5}}
	dist, ok := bellmanFord(edges, 4, 0)
	fmt.Println(ok, dist) // true [0 -1 2 -1]
}
```

## 14.3. Decision Matrix

| Use Dijkstra When... | Use Bellman-Ford When... |
|----------------------|--------------------------|
| All <abbr title="A connection between two vertices in a graph.">edge</abbr> weights non-negative | Negative weights present |
| Performance is critical | Negative <abbr title="A path that starts and ends at the same vertex.">cycle</abbr> detection needed |
| Standard routing problems | Sparse graphs with negatives |

### Edge Cases & Pitfalls

- **Negative weights:** Dijkstra fails with negative weights; use Bellman-Ford.
- **Disconnected <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>:** Distance remains infinity for unreachable vertices.
- **<abbr title="A specialized tree-based data structure that satisfies the heap property.">Heap</abbr> stale entries:** Lazy deletion in <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr> is common in implementations.

## 14.4. Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Algorithm | Time | Space | Negative Weights | <abbr title="A path that starts and ends at the same vertex.">Cycle</abbr> Detect |
|-----------|------|-------|------------------|--------------|
| Dijkstra | <code>O((V+E) log V)</code> | <code>O(V)</code> | No | No |
| Bellman-Ford | <code>O(VE)</code> | <code>O(V)</code> | Yes | Yes |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 14:</strong> Dijkstra's algorithm is the go-to for non-negative weighted shortest paths with its efficient <code>O((V+E) log V)</code> complexity. Bellman-Ford handles negative weights and detects negative cycles at the cost of <code>O(VE)</code> time. In Go, use <code>container/heap</code> for Dijkstra's <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr>.
{{% /alert %}}

## See Also

- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/Chapter-12/)
- [Chapter 13: Graph Traversal Algorithms](/docs/part-iv/Chapter-13/)
- [Chapter 52: A* Search](/docs/part-x/Chapter-52/)
