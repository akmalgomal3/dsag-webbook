---
weight: 40500
title: "Chapter 17: Network Flow Algorithms"
description: "Network Flow Algorithms"
icon: "article"
date: "2024-08-24T23:42:30+07:00"
lastmod: "2024-08-24T23:42:30+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the intellectual property of computer science; they are the critical tools for understanding how to solve complex problems effectively.</em>" : Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 17 focuses on Network Flow Algorithms (Ford-Fulkerson, Edmonds-Karp, Dinic's). It demonstrates how to maximize network <abbr title="The amount of data processed in a given amount of time.">throughput</abbr> and minimize transportation costs effectively within dense graphs.
{{% /alert %}}

## 17.1. Ford-Fulkerson Method

**Definition:** Ford-Fulkerson iteratively increases flow by finding an augmenting <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> from the source to the sink using DFS, until no such <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> exists.

**Background & Philosophy:**
Network flow problems model the transport of goods, liquids, or data across a constrained network. Ford-Fulkerson is a "method" rather than an algorithm because it does not strictly specify how to find the path. The philosophy is greedy incrementation: find any path that can take more flow, fill it up to its bottleneck, and crucially, create "residual" back-edges. These back-edges act as an "undo" button, allowing future paths to push flow back the other way if it leads to a globally higher total flow.

**Use Cases:**
Used in pipeline logistics (water or oil routing), allocating bandwidth in telecom networks, and calculating maximum bipartite matching (e.g., matching job applicants to open positions).

**Memory Mechanics:**
The algorithm heavily relies on a "Residual Graph", typically implemented as an <abbr title="A 2D array representing a graph, where rows and columns correspond to vertices.">Adjacency Matrix</abbr> (`[][]int`). In Go, mutating a 2D slice directly modifies the underlying <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. DFS traverses this matrix recursively, adding to the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>. Because Ford-Fulkerson uses DFS, it can pathologically ping-pong back and forth between two nodes if the capacities are chosen poorly, making it incredibly inefficient in terms of CPU cycles, though its <abbr title="A computational complexity that describes the amount of memory space taken by an algorithm.">space complexity</abbr> remains a steady <code>O(V^2)</code>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Augmenting <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> | <code>O(E)</code> | Using DFS |
| Total | <code>O(E × max_flow)</code> | Not guaranteed to be polynomial |
| Residual <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> | <code>O(V²)</code> | <abbr title="A 2D array representing a graph, where rows and columns correspond to vertices.">Adjacency matrix</abbr> |

### Pseudocode

```text
FordFulkerson(capacity, source, sink):
    flow = n×n zero matrix
    total = 0
    while true:
        visited = array of false
        aug = DFS(source, infinity)
        if aug == 0: break
        total += aug
    return total

DFS(u, minFlow):
    if u == sink: return minFlow
    visited[u] = true
    for each v:
        if not visited[v] and residual > 0:
            f = DFS(v, min(minFlow, residual))
            if f > 0:
                flow[u][v] += f
                flow[v][u] -= f
                return f
    return 0
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func fordFulkerson(cap [][]int, s, t int) int {
	n := len(cap)
	flow := make([][]int, n)
	for i := range flow { flow[i] = make([]int, n) }
	var aug func(u int, visited []bool, minFlow int) int
	aug = func(u int, visited []bool, minFlow int) int {
		if u == t { return minFlow }
		visited[u] = true
		for v := 0; v < n; v++ {
			if !visited[v] && cap[u][v]-flow[u][v] > 0 {
				if f := aug(v, visited, min(minFlow, cap[u][v]-flow[u][v])); f > 0 {
					flow[u][v] += f; flow[v][u] -= f
					return f
				}
			}
		}
		return 0
	}
	total := 0
	for {
		visited := make([]bool, n)
		f := aug(s, visited, 1<<30)
		if f == 0 { break }
		total += f
	}
	return total
}

func min(a, b int) int { if a < b { return a }; return b }

func main() {
	cap := [][]int{
		{0,16,13,0,0,0}, {0,0,10,12,0,0}, {0,4,0,0,14,0},
		{0,0,9,0,0,20}, {0,0,0,7,0,4}, {0,0,0,0,0,0},
	}
	fmt.Println(fordFulkerson(cap, 0, 5))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| A simple implementation is needed | Capacities are large — runtime can be exponential |
| The graph is extremely small | A strict polynomial guarantee is required |

### Edge Cases & Pitfalls

- **Integer capacities:** Ensure `bottleneck := 1 << 30` does not trigger an integer overflow.
- **Augmenting path DFS:** This can be extremely slow for large capacities; use Edmonds-Karp instead.

## 17.2. Edmonds-Karp Algorithm

**Definition:** Edmonds-Karp is an implementation of the Ford-Fulkerson method that uses BFS to find the shortest augmenting path, guaranteeing a polynomial complexity of <code>O(V E²)</code>.

**Background & Philosophy:**
Edmonds-Karp fixes the pathological flaw in Ford-Fulkerson by formalizing the path-finding rule: "Always take the shortest path by edge count." This philosophy of Breadth-First traversal eliminates the possibility of bouncing back and forth on large capacity edges, bounding the algorithm's runtime mathematically to the number of nodes and edges, regardless of how massive the integer capacities are.

**Use Cases:**
The standard fallback algorithm for general-purpose max flow calculations when the graph is small to medium-sized and capacity numbers vary wildly.

**Memory Mechanics:**
By using BFS, Edmonds-Karp replaces the DFS <abbr title="Memory used to execute functions and store local variables.">call stack</abbr> with a heap-allocated Queue (`[]int`). In Go, tracking the path requires a `parent` array. As the BFS scans the matrix, it constantly reads from the queue, checks the capacity matrix, and updates the parent slice. Since these slices are accessed dynamically, <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> misses are common on large graphs, making Edmonds-Karp strictly slower than Dinic's for dense configurations.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| BFS augmenting | <code>O(V)</code> | Shortest path by edge count |
| Iterations | <code>O(VE)</code> | Bound on the number of augmenting paths |
| Total | <code>O(V E²)</code> | Strictly polynomial |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func edmondsKarp(cap [][]int, s, t int) int {
	n := len(cap)
	flow := make([][]int, n)
	for i := range flow { flow[i] = make([]int, n) }
	total := 0
	for {
		parent := make([]int, n)
		for i := range parent { parent[i] = -1 }
		q := []int{s}; parent[s] = s
		for len(q) > 0 && parent[t] == -1 {
			u := q[0]; q = q[1:]
			for v := 0; v < n; v++ {
				if parent[v] == -1 && cap[u][v]-flow[u][v] > 0 {
					parent[v] = u; q = append(q, v)
				}
			}
		}
		if parent[t] == -1 { break }
		bottleneck := 1 << 30
		for v := t; v != s; v = parent[v] {
			u := parent[v]
			if cap[u][v]-flow[u][v] < bottleneck { bottleneck = cap[u][v] - flow[u][v] }
		}
		for v := t; v != s; v = parent[v] {
			u := parent[v]
			flow[u][v] += bottleneck; flow[v][u] -= bottleneck
		}
		total += bottleneck
	}
	return total
}

func main() {
	cap := [][]int{
		{0,16,13,0,0,0}, {0,0,10,12,0,0}, {0,4,0,0,14,0},
		{0,0,9,0,0,20}, {0,0,0,7,0,4}, {0,0,0,0,0,0},
	}
	fmt.Println(edmondsKarp(cap, 0, 5))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Need a polynomial time guarantee | The graph is massive — Dinic's is much faster |
| A straightforward implementation is preferred | The graph is very dense |

## 17.3. Dinic’s Algorithm

**Definition:** Dinic's algorithm utilizes a level graph (built via BFS) and blocking flows (found via DFS) to dramatically accelerate maximum flow computations, achieving <code>O(E √V)</code> complexity.

**Background & Philosophy:**
Dinic's philosophy is "batch processing". Instead of finding one path at a time (like Edmonds-Karp), it builds a "Level Graph" mapping distance from the source. Then, it pushes multiple flows simultaneously through this graph until the entire level structure is blocked. It combines the rigorous pathing of BFS with the aggressive exploration of DFS.

**Use Cases:**
The absolute gold standard for competitive programming and heavy-duty network calculations, such as bipartite matching where its time complexity drops miraculously to <code>O(E √V)</code>.

**Memory Mechanics:**
Dinic’s introduces a `level` slice alongside the `flow` and `capacity` matrices. During the DFS phase, a `ptr` (or `dead-end`) array is often used to avoid re-exploring edges that can no longer take flow. This requires slightly more <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> than Edmonds-Karp, but the avoidance of redundant memory fetches makes Dinic's algorithm remarkably sympathetic to the CPU architecture. The combination of state arrays forces Go's Garbage Collector to trace slightly more data, but the execution speedup heavily outweighs this.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Build level graph | <code>O(E)</code> | Using BFS |
| Blocking flow | <code>O(VE)</code> | Using DFS |
| Total | <code>O(E √V)</code> | Extremely fast for dense graphs |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func dinic(cap [][]int, s, t int) int {
	n := len(cap)
	flow := make([][]int, n)
	for i := range flow { flow[i] = make([]int, n) }
	level := make([]int, n)
	bfs := func() bool {
		for i := range level { level[i] = -1 }
		q := []int{s}; level[s] = 0
		for len(q) > 0 {
			u := q[0]; q = q[1:]
			for v := 0; v < n; v++ {
				if level[v] == -1 && cap[u][v]-flow[u][v] > 0 {
					level[v] = level[u]+1; q = append(q, v)
				}
			}
		}
		return level[t] >= 0
	}
	var dfs func(u, f int) int
	dfs = func(u, f int) int {
		if u == t { return f }
		for v := 0; v < n; v++ {
			if level[v] == level[u]+1 && cap[u][v]-flow[u][v] > 0 {
				if ret := dfs(v, min(f, cap[u][v]-flow[u][v])); ret > 0 {
					flow[u][v] += ret; flow[v][u] -= ret
					return ret
				}
			}
		}
		return 0
	}
	total := 0
	for bfs() {
		for f := dfs(s, 1<<30); f > 0; f = dfs(s, 1<<30) {
			total += f
		}
	}
	return total
}

func min(a, b int) int { if a < b { return a }; return b }

func main() {
	cap := [][]int{
		{0,16,13,0,0,0}, {0,0,10,12,0,0}, {0,4,0,0,14,0},
		{0,0,9,0,0,20}, {0,0,0,7,0,4}, {0,0,0,0,0,0},
	}
	fmt.Println(dinic(cap, 0, 5))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Dense graphs | A simpler implementation is preferred (choose Edmonds-Karp) |
| High performance is critical | The graph is trivially small |

## 17.4. Minimum-Cost Flow

**Definition:** Minimum-cost flow finds the maximum flow that incurs the absolute minimum total cost, utilizing the successive shortest path algorithm equipped with Dijkstra on the residual graph.

**Background & Philosophy:**
Max flow tells you *how much* you can ship; Min-Cost Flow tells you the *cheapest way* to ship it. The philosophy combines the greedy routing of Dijkstra with the residual tracking of Ford-Fulkerson. It proves that by always pushing flow through the cheapest available path until capacity is met, the final flow configuration is mathematically optimal in cost.

**Use Cases:**
Supply chain optimization (e.g., shipping goods from multiple factories to multiple warehouses at the lowest freight cost), and the assignment problem (e.g., assigning Uber drivers to riders minimizing total travel distance).

**Memory Mechanics:**
Min-Cost Flow requires tracking `capacity`, `flow`, and `cost` matrices. It runs a Priority Queue (Min-Heap) for Dijkstra in every phase. Because Go creates a new slice for the Priority Queue upon every Dijkstra invocation, the <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> experiences high churn. Allocating the `dist` and `parent` arrays outside the loop and reusing them avoids unnecessary heap allocations and stabilizes memory performance.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Successive shortest path | <code>O(F · E log V)</code> | F = max flow |
| Total | <code>O(F · E log V)</code> | Driven by Dijkstra |

### Idiomatic Go Implementation

```go
package main

import (
	"container/heap"
	"fmt"
)

type MI struct{ v, d int }
type MPQ []MI

func (q MPQ) Len() int           { return len(q) }
func (q MPQ) Less(i, j int) bool { return q[i].d < q[j].d }
func (q MPQ) Swap(i, j int)      { q[i], q[j] = q[j], q[i] }
func (q *MPQ) Push(x interface{}) { *q = append(*q, x.(MI)) }
func (q *MPQ) Pop() interface{} {
	old := *q
	n := len(old)
	*q = old[:n-1]
	return old[n-1]
}

func minCostFlow(cap, cost [][]int, s, t, maxf int) int {
	n := len(cap)
	flow := make([][]int, n)
	for i := range flow { flow[i] = make([]int, n) }
	total := 0
	for maxf > 0 {
		dist := make([]int, n)
		par := make([]int, n)
		for i := range dist { dist[i] = -1; par[i] = -1 }
		dist[s] = 0
		pq := &MPQ{{s, 0}}
		heap.Init(pq)
		for pq.Len() > 0 {
			c := heap.Pop(pq).(MI)
			if c.d > dist[c.v] { continue }
			for v := 0; v < n; v++ {
				if cap[c.v][v]-flow[c.v][v] > 0 {
					nd := dist[c.v] + cost[c.v][v]
					if dist[v] == -1 || nd < dist[v] {
						dist[v] = nd
						par[v] = c.v
						heap.Push(pq, MI{v, nd})
					}
				}
			}
		}
		if dist[t] == -1 { break }
		b := maxf
		for v := t; v != s; v = par[v] {
			if cap[par[v]][v]-flow[par[v]][v] < b {
				b = cap[par[v]][v] - flow[par[v]][v]
			}
		}
		for v := t; v != s; v = par[v] {
			u := par[v]
			flow[u][v] += b
			flow[v][u] -= b
			total += b * cost[u][v]
		}
		maxf -= b
	}
	return total
}

func main() {
    // Basic demonstration values
	cap := [][]int{{0, 3}, {0, 0}}
	cost := [][]int{{0, 5}, {0, 0}}
	fmt.Println(minCostFlow(cap, cost, 0, 1, 3))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Need to aggressively minimize transportation or assignment cost | You only need max flow without caring about cost |
| All edge costs are positive | There is a negative cost cycle |

## 17.5. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Ford-Fulkerson | Recursive DFS | <code>O(E · maxFlow)</code> | <code>O(V²)</code> | Educational / Conceptual |
| Edmonds-Karp | BFS + Queue | <code>O(V E²)</code> | <code>O(V²)</code> | General purpose max flow |
| Dinic | BFS level + DFS | <code>O(E √V)</code> | <code>O(V²)</code> | Dense networks |
| Min-Cost Flow | Dijkstra + PQ | <code>O(F · E log V)</code> | <code>O(V²)</code> | Logistics, optimal assignment |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 17:</strong> This chapter discusses network flow algorithms: Ford-Fulkerson, Edmonds-Karp, Dinic's, and min-cost flow. Use Edmonds-Karp for <abbr title="An algorithm whose running time is upper bounded by a polynomial expression.">polynomial time</abbr> guarantees, Dinic's for dense networks requiring high performance, and min-cost flow when minimizing transportation or assignment cost.
{{% /alert %}}

## See Also

- [Chapter 16: Minimum Spanning Trees](/docs/Part-IV/Chapter-16/)
- [Chapter 18: Matchings in Bipartite Graphs](/docs/Part-IV/Chapter-18/)
- [Chapter 32: Linear Programming](/docs/Part-VII/Chapter-32/)
