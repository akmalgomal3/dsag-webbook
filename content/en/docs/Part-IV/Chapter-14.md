---
weight: 40200
title: "Chapter 14 - Single-Source Shortest Paths"
description: "Single-Source Shortest Paths"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The shortest path between two points is a straight line.</em>" — Archimedes</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 14 covers single-source shortest path algorithms: Dijkstra's algorithm and Bellman-Ford. Learn when to use each and how to implement them in Go.
{{% /alert %}}

## 14.1. Dijkstra's Algorithm

**Definition:** Dijkstra's algorithm finds the shortest paths from a source vertex to all other vertices in a weighted graph with non-negative edge weights.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Init | <code>O(V)</code> | Set distances to infinity |
| Extract min | <code>O(log V)</code> per extraction | Priority queue |
| Relax edges | <code>O(E)</code> total | Update distances |
| Total | <code>O((V + E) log V)</code> | With binary heap |

### Idiomatic Go Implementation

Use `container/heap` for the priority queue.

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

**Definition:** Bellman-Ford finds shortest paths from a single source in graphs with negative edge weights (but no negative cycles).

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Relax all edges | <code>O(E)</code> per iteration | V-1 iterations |
| Detect negative cycle | <code>O(E)</code> | One extra iteration |
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
| All edge weights non-negative | Negative weights present |
| Performance is critical | Negative cycle detection needed |
| Standard routing problems | Sparse graphs with negatives |

### Edge Cases & Pitfalls

- **Negative weights:** Dijkstra fails with negative weights; use Bellman-Ford.
- **Disconnected graph:** Distance remains infinity for unreachable vertices.
- **Heap stale entries:** Lazy deletion in priority queue is common in implementations.

## 14.4. Quick Reference

| Algorithm | Time | Space | Negative Weights | Cycle Detect |
|-----------|------|-------|------------------|--------------|
| Dijkstra | <code>O((V+E) log V)</code> | <code>O(V)</code> | No | No |
| Bellman-Ford | <code>O(VE)</code> | <code>O(V)</code> | Yes | Yes |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 14:</strong> Dijkstra's algorithm is the go-to for non-negative weighted shortest paths with its efficient <code>O((V+E) log V)</code> complexity. Bellman-Ford handles negative weights and detects negative cycles at the cost of <code>O(VE)</code> time. In Go, use <code>container/heap</code> for Dijkstra's priority queue.
{{% /alert %}}

## See Also

- [Chapter 12 — Graphs and Graph Representations](/docs/Part-III/Chapter-12/)
- [Chapter 13 — Graph Traversal Algorithms](/docs/Part-IV/Chapter-13/)
- [Chapter 53 — A* Search](/docs/Part-X/Chapter-53/)

