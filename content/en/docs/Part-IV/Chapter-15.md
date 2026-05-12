---
weight: 40300
title: "Chapter 15: All-Pairs Shortest Paths"
description: "All-Pairs Shortest Paths"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The whole is greater than the sum of its parts.</em>" : Aristotle</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 15 covers all-pairs shortest path algorithms: Floyd-Warshall and Johnson's algorithm. Learn when to use each based on graph density and edge weights.
{{% /alert %}}

## 15.1. Floyd-Warshall Algorithm

**Definition:** Floyd-Warshall computes shortest paths between all pairs of vertices using <abbr title="A method combining solutions to overlapping subproblems">dynamic programming</abbr>. It works with negative edges (but no negative cycles) and handles dense graphs efficiently.

**Background & Philosophy:**
Instead of computing paths from a single starting point, Floyd-Warshall calculates the shortest path between *every* pair of nodes simultaneously. The philosophy is grounded in <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>: solving subproblems incrementally. It asks, "Is the path from A to B shorter if we route it through intermediate node K?" by slowly expanding the set of allowed intermediate nodes.

**Use Cases:**
Used in analyzing transportation networks (e.g., calculating transit distances between all major cities), computing routing tables in complex network topologies, and analyzing social network connections to determine the "degrees of separation" between all users.

**Memory Mechanics:**
Floyd-Warshall requires a 2D matrix (in Go, typically a `[][]float64` or `[][]int`). This creates a memory footprint of <code>O(V^2)</code>. While an array of slice headers in Go causes slight <abbr title="Inefficient RAM usage creating small unusable blocks">memory fragmentation</abbr>, processing rows sequentially leverages <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. The three tight nested loops (`k, i, j`) fit perfectly into modern branch predictors. However, for a graph with 10,000 nodes, the distance matrix requires allocating 100 million integers, consuming hundreds of megabytes of <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Triple nested loop | <code>O(V^3)</code> | Three nested loops over vertices |
| Memory | <code>O(V^2)</code> | Distance matrix |
| <abbr title="A path that starts and ends at the same vertex.">Cycle</abbr> detect | <code>O(V)</code> | Check negative diagonal |

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

**Definition:** Johnson's algorithm reweights edges to eliminate negative weights, then runs Dijkstra from each vertex. It is efficient for sparse graphs.

**Background & Philosophy:**
Johnson's algorithm is a hybrid mathematical trick. Dijkstra is incredibly fast but breaks if negative weights exist. Bellman-Ford handles negative weights but is slow. The philosophy of Johnson's algorithm is to use the slow algorithm (Bellman-Ford) just *once* to mathematically "reweight" all edges to be positive, allowing the system to safely execute the fast algorithm (Dijkstra) `V` times.

**Use Cases:**
Essential when calculating all-pairs shortest paths on massive, sparse networks (like road networks or internet routing where nodes only connect to a few neighbors) that happen to include negative weights (like routing costs that factor in discounts or incentives).

**Memory Mechanics:**
Johnson's algorithm avoids allocating massive <code>O(V^2)</code> matrices upfront. Instead, it relies on <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">adjacency lists</abbr> which take <code>O(V+E)</code> memory. Running Dijkstra repeatedly means dynamically allocating a <abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority Queue</abbr> per node. Go's <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> efficiently manages and recycles this short-lived <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> memory during the execution, keeping the overall <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> consumption significantly lower than Floyd-Warshall's rigid matrix requirements for sparse graphs.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Bellman-Ford | <code>O(VE)</code> | Reweight edges |
| V × Dijkstra | <code>O(VE log V)</code> | Sparse <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> advantage |
| Total | <code>O(VE log V)</code> | Better than Floyd-Warshall for sparse graphs |

### Decision Matrix

| Use Floyd-Warshall When... | Use Johnson's When... |
|----------------------------|------------------------|
| Dense <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> | Sparse <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> |
| Simple implementation needed | Performance critical |
| Negative edges present | Negative edges present |
| V < 500 | V is large but E is small |

### Edge Cases & Pitfalls

- **Negative <abbr title="A path that starts and ends at the same vertex.">cycle</abbr>:** Both algorithms fail; detect with Bellman-Ford first.
- **Overflow:** Use `math.Inf(1)` to represent infinity without wrap-around.
- **Dense graphs:** <code>O(V^3)</code> is prohibitively expensive for V > 10^4.

## 15.3. Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Algorithm | Time | Space | <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr> Type | Negative Edges |
|-----------|------|-------|------------|----------------|
| Floyd-Warshall | <code>O(V^3)</code> | <code>O(V^2)</code> | Dense | Yes |
| Johnson | <code>O(VE log V)</code> | <code>O(V^2)</code> | Sparse | Yes |
| Naive V×Dijkstra | <code>O(VE log V)</code> | <code>O(V^2)</code> | Non-negative | No |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 15:</strong> Floyd-Warshall provides a simple <code>O(V^3)</code> solution for dense graphs, while Johnson's algorithm achieves better <code>O(VE log V)</code> performance on sparse graphs with negative weights. Choose based on <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> density and always check for negative cycles first.
{{% /alert %}}

## See Also

- [Chapter 13: Graph Traversal Algorithms](/docs/Part-IV/Chapter-13/)
- [Chapter 14: Single-Source Shortest Paths](/docs/Part-IV/Chapter-14/)
- [Chapter 33: Linear Programming](/docs/Part-VII/Chapter-33/)
