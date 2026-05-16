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
<strong>"<em>The shortest path between two points is a straight line.</em>" — Archimedes</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 14: Dijkstra and Bellman-Ford algorithms. Covers usage, logic, and Go implementation.
{{% /alert %}}

## 14.1. Dijkstra's Algorithm

**Definition:** Dijkstra finds shortest paths from source to all vertices. Required: weighted graph, non-negative edge weights.

**Logic:**
Greedy expansion. Assumes cheapest frontier path is final. Logic holds if negative weights are absent.

**Use Cases:**
Network routing (OSPF). Mapping software. GPS navigation.

**Memory Mechanics:**
Relies on <abbr title="A heap where each parent is less than or equal to its children">Min-Heap</abbr>. Go implementations use contiguous slices. High <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality during heap operations. Large graphs trigger <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr> during random distance array access.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Init | <code>O(V)</code> | Initialize distances |
| Extract min | <code>O(log V)</code> | Priority queue operation |
| Relax edges | <code>O(E)</code> | Total distance updates |
| Total | <code>O((V + E) log V)</code> | With binary heap |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

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
func (p *PQ) Push(x any) { *p = append(*p, x.(Item)) }
func (p *PQ) Pop() any {
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

**Definition:** Finds shortest paths from source. Supports negative edge weights. Detects negative cycles.

**Logic:**
Dynamic programming. Path contains max `V-1` edges. Relax all edges `V-1` times to ensure correct distances.

**Use Cases:**
Financial arbitrage detection. Distance-vector routing protocols.

**Memory Mechanics:**
Uses simple distance slices and edge lists. Linear access pattern. CPU prefetcher friendly. Performs well on small graphs despite `O(VE)` complexity.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Relax edges | <code>O(E)</code> | Per iteration |
| Detect cycle | <code>O(E)</code> | Extra iteration |
| Total | <code>O(VE)</code> | All iterations |

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
| Weights are non-negative | Negative weights present |
| Speed is priority | Cycle detection required |
| Standard routing | Sparse graphs with negatives |

### Edge Cases & Pitfalls

- **Negative weights:** Dijkstra fails. Use Bellman-Ford.
- **Disconnected graph:** Unreachable vertices stay at infinite distance.
- **Heap stale entries:** Handle outdated items in priority queue.

### Anti-Patterns

- **Dijkstra with negative edges:** Assumes positive weights. Negative edges yield incorrect results.
- **Constant slice allocation:** Reuse `dist` slice. Avoids overhead.
- **Storing full paths:** Use parent pointers. Saves O(V²) memory.

## 14.4. Quick Reference

| Algorithm | Time | Space | Negative Weights | Cycle Detect |
|-----------|------|-------|------------------|--------------|
| Dijkstra | <code>O((V+E) log V)</code> | <code>O(V)</code> | No | No |
| Bellman-Ford | <code>O(VE)</code> | <code>O(V)</code> | Yes | Yes |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 14:</strong> Dijkstra is optimal for positive weights. Bellman-Ford handles negatives and cycles. Use <code>container/heap</code> for Dijkstra in Go.
{{% /alert %}}

## See Also

- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/chapter-12/)
- [Chapter 13: Graph Traversal Algorithms](/docs/part-iv/chapter-13/)
- [Chapter 52: A* Search](/docs/part-x/chapter-52/)
