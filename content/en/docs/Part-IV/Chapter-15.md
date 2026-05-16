---
weight: 40300
title: "Chapter 15: All-Pairs Shortest Paths"
description: "All-Pairs Shortest Paths"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The whole is greater than the sum of its parts.</em>" — Aristotle</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 15: Floyd-Warshall and Johnson's algorithms. Compares usage for dense vs sparse graphs.
{{% /alert %}}

## 15.1. Floyd-Warshall Algorithm

**Definition:** Computes shortest paths between all vertex pairs. Uses dynamic programming. Supports negative edges. Handles dense graphs efficiently.

**Logic:**
Simultaneous calculation of all paths. Incrementally expands set of intermediate nodes. Checks if node K improves path between A and B.

**Use Cases:**
Transportation network analysis. Network routing tables. Social network connectivity.

**Memory Mechanics:**
Requires 2D matrix. Memory: O(V^2). Sequential row access maximizes spatial locality. Large graphs (V > 10,000) risk massive RAM consumption.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Triple loop | <code>O(V^3)</code> | Iterate over all vertex triplets |
| Memory | <code>O(V^2)</code> | Matrix storage |
| Cycle detect | <code>O(V)</code> | Negative diagonal check |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

```go
package main

import (
	"fmt"
	"math"
)

func floydWarshall(g [][]float64) [][]float64 {
	n := len(g)
	dist := make([][]float64, n)
	for i := range dist {
		dist[i] = make([]float64, n)
		copy(dist[i], g[i])
	}
	for i := 0; i < n; i++ { dist[i][i] = 0 }
	for k := 0; k < n; k++ {
		for i := 0; i < n; i++ {
			for j := 0; j < n; j++ {
				if dist[i][k]+dist[k][j] < dist[i][j] {
					dist[i][j] = dist[i][k] + dist[k][j]
				}
			}
		}
	}
	return dist
}

func main() {
	inf := math.Inf(1)
	g := [][]float64{
		{0, 3, inf, inf},
		{2, 0, inf, 1},
		{inf, 7, 0, 2},
		{6, inf, inf, 0},
	}
	fmt.Println(floydWarshall(g))
}
```

## 15.2. Johnson's Algorithm

**Definition:** Reweights edges to remove negatives. Executes Dijkstra from all vertices. Optimal for sparse graphs.

**Logic:**
Hybrid method. Runs Bellman-Ford once to ensure positive weights. Runs Dijkstra V times for performance.

**Use Cases:**
Massive sparse networks. Road networks with discounts or negative costs.

**Memory Mechanics:**
Uses adjacency lists. Memory: O(V+E). Go GC handles temporary priority queues. More RAM-efficient than Floyd-Warshall for sparse graphs.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Bellman-Ford | <code>O(VE)</code> | Edge reweighting step |
| V × Dijkstra | <code>O(VE log V)</code> | Repeated Dijkstra runs |
| Total | <code>O(VE log V)</code> | Optimal for sparse graphs |

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
func (p *PQ) Push(x any)        { *p = append(*p, x.(Item)) }
func (p *PQ) Pop() any {
	old := *p
	n := len(old)
	*p = old[:n-1]
	return old[n-1]
}

func bellmanFord(adj [][]Edge) ([]int, bool) {
	n := len(adj)
	h := make([]int, n)
	for i := 0; i < n-1; i++ {
		for u := 0; u < n; u++ {
			for _, e := range adj[u] {
				if h[u]+e.w < h[e.to] {
					h[e.to] = h[u] + e.w
				}
			}
		}
	}
	for u := 0; u < n; u++ {
		for _, e := range adj[u] {
			if h[u]+e.w < h[e.to] {
				return nil, false
			}
		}
	}
	return h, true
}

func dijkstra(adj [][]Edge, src int, h []int) []int {
	n := len(adj)
	dist := make([]int, n)
	for i := range dist { dist[i] = math.MaxInt32 }
	dist[src] = 0
	pq := &PQ{{src, 0}}
	heap.Init(pq)
	for pq.Len() > 0 {
		cur := heap.Pop(pq).(Item)
		if cur.d > dist[cur.v] { continue }
		for _, e := range adj[cur.v] {
			if dist[cur.v]+e.w < dist[e.to] {
				dist[e.to] = dist[cur.v] + e.w
				heap.Push(pq, Item{e.to, dist[e.to] + h[src] - h[e.to]})
			}
		}
	}
	for i := range dist {
		if dist[i] < math.MaxInt32 {
			dist[i] = dist[i] - h[src] + h[i]
		}
	}
	return dist
}

func johnson(adj [][]Edge) ([][]int, bool) {
	h, ok := bellmanFord(adj)
	if !ok { return nil, false }
	n := len(adj)
	allPairs := make([][]int, n)
	for u := 0; u < n; u++ {
		allPairs[u] = dijkstra(adj, u, h)
	}
	return allPairs, true
}

func main() {
	adj := [][]Edge{
		{{1, -2}, {2, 4}},
		{{2, 3}, {3, 2}},
		{},
		{{0, -1}},
	}
	result, ok := johnson(adj)
	if !ok {
		fmt.Println("Negative cycle detected")
		return
	}
	for i, row := range result {
		fmt.Printf("From %d: %v\n", i, row)
	}
}
```

### Decision Matrix

| Use Floyd-Warshall When... | Use Johnson's When... |
|----------------------------|------------------------|
| Graph is dense | Graph is sparse |
| Implementation simplicity | Execution speed priority |
| Negative edges present | Negative edges present |
| V < 500 | Large V, small E |

### Edge Cases & Pitfalls

- **Negative cycle:** Both fail. Detect with Bellman-Ford.
- **Overflow:** Use `math.Inf(1)` to avoid wrap-around errors.
- **Dense graphs:** O(V^3) scales poorly for V > 10^4.

### Anti-Patterns

- **Floyd-Warshall on sparse graphs:** Inefficient if E ≈ V. Johnson's is faster.
- **Unsafe infinity values:** Integer addition on MaxInt overflows. Use `math.MaxInt/2` or `math.Inf(1)`.
- **Inefficient matrix updates:** Update in-place. Matrix copying kills throughput.

## 15.3. Quick Reference

| Algorithm | Time | Space | Graph Type | Negative Edges |
|-----------|------|-------|------------|----------------|
| Floyd-Warshall | <code>O(V^3)</code> | <code>O(V^2)</code> | Dense | Yes |
| Johnson | <code>O(VE log V)</code> | <code>O(V^2)</code> | Sparse | Yes |
| V×Dijkstra | <code>O(VE log V)</code> | <code>O(V^2)</code> | Non-negative | No |


{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 15:</strong> Floyd-Warshall for dense graphs. Johnson's for sparse graphs with negatives. Density determines algorithm choice.
{{% /alert %}}

## See Also

- [Chapter 13: Graph Traversal Algorithms](/docs/part-iv/chapter-13/)
- [Chapter 14: Single-Source Shortest Paths](/docs/part-iv/chapter-14/)
- [Chapter 32: Linear Programming](/docs/part-vii/chapter-32/)