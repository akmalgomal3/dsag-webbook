---
weight: 40500
title: "Chapter 17: Network Flow Algorithms"
description: "Network Flow Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the intellectual property of computer science; they are the critical tools for understanding how to solve complex problems effectively.</em>" — Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 17: Network Flow Algorithms. Covers Ford-Fulkerson, Edmonds-Karp, and Dinic's algorithms. Focuses on throughput optimization.
{{% /alert %}}

## 17.1. Ford-Fulkerson Method

**Definition:** Increases flow by finding augmenting paths via DFS. Stops when no paths exist between source and sink.

**Logic:**
Greedy incrementation. Fills paths to bottleneck limit. Uses residual back-edges for flow "undo". Back-edges ensure global optimization.

**Use Cases:**
Pipeline logistics. Telecom bandwidth allocation. Bipartite matching.

**Memory Mechanics:**
Relies on residual adjacency matrix `[][]int`. DFS adds to call stack. Pathologically slow for large capacities. Space complexity: O(V^2).

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Augmenting path | <code>O(E)</code> | Using DFS |
| Total | <code>O(E × max_flow)</code> | Capacity-dependent |
| Residual graph | <code>O(V²)</code> | Adjacency matrix storage |

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
| Implementation simplicity required | Large capacities present. Runtime can be exponential. |
| Graph is very small | Polynomial guarantee required |

### Edge Cases & Pitfalls

- **Overflow:** Ensure bottleneck values stay within `int` range.
- **DFS Pathing:** Slow for high capacities. Use Edmonds-Karp instead.

## 17.2. Edmonds-Karp Algorithm

**Definition:** Ford-Fulkerson variant using BFS for shortest augmenting paths. Polynomial complexity: <code>O(V E²)</code>.

**Logic:**
Rule: Always take shortest path by edge count. BFS prevents bouncing on high-capacity edges. Runtime bounded by graph size.

**Use Cases:**
General-purpose max flow. Small to medium graphs with variable capacities.

**Memory Mechanics:**
Replaces recursion with `[]int` Queue. Requires `parent` array for path reconstruction. Dynamic slice access may cause CPU cache misses on large graphs.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| BFS augmenting | <code>O(V)</code> | Shortest path count |
| Iterations | <code>O(VE)</code> | Path count bound |
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
| Polynomial guarantee needed | Massive graphs. Dinic's is faster. |
| Straightforward implementation | Very dense graphs |

## 17.3. Dinic’s Algorithm

**Definition:** Uses level graphs (BFS) and blocking flows (DFS). Complexity: <code>O(V²E)</code> general, <code>O(E√V)</code> for bipartite matching.

**Logic:**
Batch processing. Level Graph maps source distance via BFS. Pushes multiple flows simultaneously via DFS. Levels blocked when exhausted.

**Use Cases:**
Competitive programming. Heavy network calculations. Bipartite matching.

**Memory Mechanics:**
Uses `level` and `ptr` slices. Prevents redundant exploration. High CPU architecture sympathy. Higher RAM overhead than Edmonds-Karp.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Build level graph | <code>O(E)</code> | BFS step |
| Blocking flow | <code>O(VE)</code> | DFS step |
| Total (general) | <code>O(V²E)</code> | Dense networks |
| Total (bipartite) | <code>O(E√V)</code> | Optimal matching |

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
| Dense graphs | Simple implementation works |
| Critical performance | Trivially small graphs |

## 17.4. Minimum-Cost Flow

**Definition:** Finds max flow with minimum total cost. Uses successive shortest path algorithm via Dijkstra.

**Logic:**
Cheapest shipping strategy. Combines capacity tracking with greedy cost routing. Mathematically optimal cost configuration.

**Use Cases:**
Supply chain optimization. Uber driver assignment.

**Memory Mechanics:**
Tracks capacity, flow, and cost. High GC churn from repeated slice creation. Reuse `dist` and `parent` slices for performance stability.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Shortest path | <code>O(F · E log V)</code> | F = max flow |
| Total | <code>O(F · E log V)</code> | Dijkstra-driven |

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
func (q *MPQ) Push(x any) { *q = append(*q, x.(MI)) }
func (q *MPQ) Pop() any {
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
	cap := [][]int{{0, 3}, {0, 0}}
	cost := [][]int{{0, 5}, {0, 0}}
	fmt.Println(minCostFlow(cap, cost, 0, 1, 3))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Minimizing transportation cost | Cost is irrelevant |
| Positive edge costs | Negative cost cycles exist |

### Anti-Patterns

- **DFS Ford-Fulkerson on high capacity:** Pathological runtime. Use Edmonds-Karp or Dinic.
- **Missing reverse edges:** Prevents flow "undo". Residual graph becomes invalid.
- **Narrow integer types:** Capacity overflows int8/16. Use `int` or `int64`.

## 17.5. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Ford-Fulkerson | Recursive DFS | <code>O(E · maxFlow)</code> | <code>O(V²)</code> | Educational |
| Edmonds-Karp | BFS + Queue | <code>O(V E²)</code> | <code>O(V²)</code> | General purpose |
| Dinic | BFS + DFS | <code>O(V²E)</code> | <code>O(V²)</code> | Dense graphs / Bipartite |
| Min-Cost Flow | Dijkstra + PQ | <code>O(F · E log V)</code> | <code>O(V²)</code> | Logistics optimization |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 17:</strong> Network flow optimization. Use Edmonds-Karp for stability, Dinic for performance, and Min-Cost Flow for logistics.
{{% /alert %}}

## See Also

- [Chapter 16: Minimum Spanning Trees](/docs/part-iv/chapter-16/)
- [Chapter 18: Matchings in Bipartite Graphs](/docs/part-iv/chapter-18/)
- [Chapter 32: Linear Programming](/docs/part-vii/chapter-32/)
