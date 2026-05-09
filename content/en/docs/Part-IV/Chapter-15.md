---
weight: 40300
title: "Chapter 15 - All-Pairs Shortest Paths"
description: "All-Pairs Shortest Paths"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The whole is greater than the sum of its parts.</em>" — Aristotle</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 15 covers all-pairs shortest path algorithms: Floyd-Warshall and Johnson's algorithm. Learn when to use each based on graph density and edge weights.
{{% /alert %}}

## 15.1. Floyd-Warshall Algorithm

**Definition:** Floyd-Warshall computes shortest paths between all pairs of vertices using dynamic programming. It works with negative edges (but no negative cycles) and handles dense graphs efficiently.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Triple nested loop | <code>O(V^3)</code> | Three nested loops over vertices |
| Memory | <code>O(V^2)</code> | Distance matrix |
| Cycle detect | <code>O(V)</code> | Check negative diagonal |

### Idiomatic Go Implementation

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

**Definition:** Johnson's algorithm reweights edges to eliminate negative weights, then runs Dijkstra from each vertex. It is efficient for sparse graphs.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Bellman-Ford | <code>O(VE)</code> | Reweight edges |
| V × Dijkstra | <code>O(VE log V)</code> | Sparse graph advantage |
| Total | <code>O(VE log V)</code> | Better than Floyd-Warshall for sparse graphs |

### Decision Matrix

| Use Floyd-Warshall When... | Use Johnson's When... |
|----------------------------|------------------------|
| Dense graph | Sparse graph |
| Simple implementation needed | Performance critical |
| Negative edges present | Negative edges present |
| V < 500 | V is large but E is small |

### Edge Cases & Pitfalls

- **Negative cycle:** Both algorithms fail; detect with Bellman-Ford first.
- **Overflow:** Use `math.Inf(1)` to represent infinity without wrap-around.
- **Dense graphs:** <code>O(V^3)</code> is prohibitively expensive for V > 10^4.

## 15.3. Quick Reference

| Algorithm | Time | Space | Graph Type | Negative Edges |
|-----------|------|-------|------------|----------------|
| Floyd-Warshall | <code>O(V^3)</code> | <code>O(V^2)</code> | Dense | Yes |
| Johnson | <code>O(VE log V)</code> | <code>O(V^2)</code> | Sparse | Yes |
| Naive V×Dijkstra | <code>O(VE log V)</code> | <code>O(V^2)</code> | Non-negative | No |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 15:</strong> Floyd-Warshall provides a simple <code>O(V^3)</code> solution for dense graphs, while Johnson's algorithm achieves better <code>O(VE log V)</code> performance on sparse graphs with negative weights. Choose based on graph density and always check for negative cycles first.
{{% /alert %}}

## See Also

- [Chapter 13 — Graph Traversal Algorithms](/docs/Part-IV/Chapter-13/)
- [Chapter 14 — Single-Source Shortest Paths](/docs/Part-IV/Chapter-14/)
- [Chapter 33 — Linear Programming](/docs/Part-VII/Chapter-33/)

