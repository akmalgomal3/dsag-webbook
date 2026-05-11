---
weight: 50400
title: "Chapter 22: All-Pairs Shortest Paths"
description: "All-Pairs Shortest Paths"
icon: "article"
date: "2024-08-24T23:42:29+07:00"
lastmod: "2024-08-24T23:42:29+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The greatest <abbr title="The data associated with a key in a key-value pair.">value</abbr> of a picture is when it forces us to notice what we never expected to see.</em>" : John Tukey</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 22 focuses on All-Pairs Shortest Paths, detailing Floyd-Warshall for dense <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> routing and Johnson's algorithm for sparse graphs containing negative weights, emphasizing <abbr title="Relating to values or properties approached as a limit, used in algorithm analysis.">asymptotic</abbr> performance trade-offs.
{{% /alert %}}

## 22.1. <abbr title="An algorithm for finding shortest paths between all pairs of vertices.">Floyd-Warshall Algorithm</abbr>

**Definition:** Floyd-Warshall uses <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr> to compute the shortest paths between all pairs of vertices by iteratively testing intermediate nodes.

**Background & Philosophy:**
Instead of computing paths from a single starting point, Floyd-Warshall calculates the shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> between every pair of nodes simultaneously. The philosophy is grounded in Dynamic Programming: solving subproblems incrementally. It asks, "Is the path from A to B shorter if we route it through intermediate node K?" by slowly expanding the set of allowed intermediate nodes.

**Use Cases:**
Used in analyzing transportation networks (e.g., calculating transit distances between all major cities), computing routing tables in complex network topologies, and analyzing social network connections to determine the "degrees of separation" between all users.

**Memory Mechanics:**
Floyd-Warshall requires a 2D matrix (in Go, typically a `[][]float64` or `[][]int`). This creates a memory footprint of <code>O(V^2)</code>. While an array of slice headers in Go causes slight memory fragmentation, processing rows sequentially leverages <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. The three tight nested loops (`k, i, j`) fit perfectly into modern branch predictors. However, for a graph with 10,000 nodes, the distance matrix requires allocating 100 million integers, consuming hundreds of megabytes of <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Triple loop | <code>O(V³)</code> | Three nested loops |
| Memory | <code>O(V²)</code> | Distance matrix |
| <abbr title="A path that starts and ends at the same vertex.">Cycle</abbr> detect | <code>O(V)</code> | Check negative diagonal |

### Pseudocode

```text
FloydWarshall(graph):
    n = size of graph
    dist = copy of graph
    for i from 0 to n-1:
        dist[i][i] = 0
    for k from 0 to n-1:
        for i from 0 to n-1:
            for j from 0 to n-1:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

### Idiomatic Go Implementation

{{< prism lang="go" line-numbers="true">}}
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
{{< /prism >}}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Dense graphs | Graph is very large (V > 500) |
| Need all pairs | Sparse : Johnson's is faster |

### Edge Cases & Pitfalls

- **Negative <abbr title="A path that starts and ends at the same vertex.">cycle</abbr>:** Check if `dist[i][i] < 0` after completion.
- **Overflow:** Use `math.Inf(1)` to correctly represent ∞ without wrap-around.
- **Dense <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>:** <code>O(V³)</code> is prohibitively expensive for V > 10⁴.

## 22.2. Johnson’s Algorithm

**Definition:** Johnson's algorithm combines <abbr title="An algorithm finding shortest paths even with negative edge weights.">Bellman-Ford</abbr> (for reweighting edges to be non-negative) and <abbr title="An algorithm finding shortest paths in non-negative weighted graphs.">Dijkstra</abbr> to compute all-pairs shortest paths efficiently for sparse graphs with negative weights, achieving <code>O(V² log V + VE)</code> complexity.

**Background & Philosophy:**
Johnson's algorithm is a hybrid mathematical trick. Dijkstra is incredibly fast but breaks if negative weights exist. Bellman-Ford handles negative weights but is slow. The philosophy of Johnson's algorithm is to use the slow algorithm (Bellman-Ford) just once to mathematically "reweight" all edges to be positive, allowing the system to safely execute the fast algorithm (Dijkstra) `V` times.

**Use Cases:**
Essential when calculating all-pairs shortest paths on massive, sparse networks (like road networks or internet routing where nodes only connect to a few neighbors) that happen to include negative weights.

**Memory Mechanics:**
Johnson's algorithm avoids allocating massive <code>O(V^2)</code> matrices upfront. Instead, it relies on <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">adjacency lists</abbr> which take <code>O(V+E)</code> memory. Running Dijkstra repeatedly means dynamically allocating a <abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority Queue</abbr> per node. Go's <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> efficiently manages and recycles this short-lived <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> memory during the execution.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Bellman-Ford | <code>O(VE)</code> | Reweighting |
| Dijkstra × V | <code>O(V² log V + VE)</code> | Execution on sparse <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> |
| Total | <code>O(V² log V + VE)</code> | Better than V×Dijkstra without reweighting |

### Pseudocode

```text
Johnson(adj, n):
    h = array filled with infinity
    h[0] = 0
    repeat n-1 times:
        for each edge (u, v, w) in adj:
            if h[u] + w < h[v]: h[v] = h[u] + w
    for each start from 0 to n-1:
        dist = Dijkstra(adj_reweighted, start)
        for each v:
            if dist[v] finite: dist[v] += h[v] - h[start]
        result[start] = dist
    return result
```

### Idiomatic Go Implementation

{{< prism lang="go" line-numbers="true">}}
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type E struct{ to int; w float64 }
type It struct{ v int; d float64 }
type Q []It
func (q Q) Len() int { return len(q) }
func (q Q) Less(i, j int) bool { return q[i].d < q[j].d }
func (q Q) Swap(i, j int) { q[i], q[j] = q[j], q[i] }
func (q *Q) Push(x interface{}) { *q = append(*q, x.(It)) }
func (q *Q) Pop() interface{} { old := *q; n := len(old); *q = old[:n-1]; return old[n-1] }

func johnson(adj [][]E, n int) [][]float64 {
	h := make([]float64, n); for i := range h { h[i] = math.Inf(1) }; h[0] = 0
	for k := 0; k < n-1; k++ {
		for u := 0; u < n; u++ { for _, e := range adj[u] { if h[u]+e.w < h[e.to] { h[e.to] = h[u]+e.w } } }
	}
	all := make([][]float64, n)
	for s := 0; s < n; s++ {
		d := make([]float64, n); for i := range d { d[i] = math.Inf(1) }; d[s] = 0
		pq := &Q{}; heap.Init(pq)
		for pq.Len() > 0 {
			c := heap.Pop(pq).(It); if c.d > d[c.v] { continue }
			for _, e := range adj[c.v] {
				w := e.w + h[c.v] - h[e.to]
				if d[c.v]+w < d[e.to] { d[e.to] = d[c.v]+w; heap.Push(pq, It{e.to, d[e.to]}) }
			}
		}
		for v := range d { if d[v] != math.Inf(1) { d[v] += h[v] - h[s] } }
		all[s] = d
	}
	return all
}

func main() {
    // Demonstration slice mapping omitted for brevity
	fmt.Println("Johnson Algorithm implementation")
}
{{< /prism >}}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Sparse graph | Dense : Floyd-Warshall is much simpler |
| Negative weights exist | Non-negative : Standard V×Dijkstra is faster |

### Edge Cases & Pitfalls

- **Negative cycle:** Bellman-Ford will fail; you must detect this before running Dijkstra.
- **Reweight error:** Ensure that `h(v) = h(u) + w(u,v)` holds true after reweighting.

## 22.3. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
|| Floyd-Warshall | `[][]int` matrix | <code>O(V³)</code> | <code>O(V²)</code> | Dense, small V |
|| Johnson | `[]Edge` + PQ | <code>O(V² log V + VE)</code> | <code>O(V²)</code> | Sparse, negative weights |
|| Naive V×Dijkstra | `[]Edge` + PQ | <code>O(VE log V)</code> | <code>O(V²)</code> | Non-negative, sparse |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 22:</strong> This chapter presents Floyd-Warshall for dense graphs and Johnson's algorithm for sparse graphs with negative weights. Use Floyd-Warshall for small dense graphs requiring all-pairs shortest paths; prefer Johnson's for large sparse graphs to achieve better <abbr title="Relating to values or properties approached as a limit, used in algorithm analysis.">asymptotic</abbr> performance.
{{% /alert %}}

## See Also

- [Chapter 10: Heaps and Priority Queues](/docs/Part-III/Chapter-10/)
- [Chapter 21: Searching Algorithms](/docs/Part-V/Chapter-21/)
- [Chapter 33: Linear Programming](/docs/Part-VII/Chapter-33/)
