---
weight: 4500
title: "Chapter 17 - Network Flow Algorithms"
description: "Network Flow Algorithms"
icon: "article"
date: "2024-08-24T23:42:30+07:00"
lastmod: "2024-08-24T23:42:30+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the intellectual property of computer science; they are the critical tools for understanding how to solve complex problems effectively.</em>" — Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 17 focuses on Network Flow Algorithms (Ford-Fulkerson, Edmonds-Karp, Dinic's). It demonstrates how to maximize network <abbr title="The amount of data processed in a given amount of time.">throughput</abbr> and minimize transportation costs effectively within dense graphs.
{{% /alert %}}

## 17.1. Ford-Fulkerson Method

**Definition:** Ford-Fulkerson iteratively increases flow by finding an augmenting <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> from the source to the sink using DFS, until no such <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> exists.

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

{{< prism lang="go" line-numbers="true">}}
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
{{< /prism >}}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| A simple implementation is needed | Capacities are large — runtime can be exponential |
| The graph is extremely small | A strict polynomial guarantee is required |

### Edge Cases & Pitfalls

- **Integer capacities:** Ensure ... does not trigger an integer overflow.
- **Augmenting path DFS:** This can be extremely slow for large capacities; use Edmonds-Karp instead.

## 17.2. Edmonds-Karp Algorithm

**Definition:** Edmonds-Karp is an implementation of the Ford-Fulkerson method that uses BFS to find the shortest augmenting path, guaranteeing a polynomial complexity of ....

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| BFS augmenting | ... | Shortest path by edge count |
| Iterations | ... | Bound on the number of augmenting paths |
| Total | ... | Strictly polynomial |

### Pseudocode


### Idiomatic Go Implementation

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
		for len(q) > 0 && <abbr title="A node that has a child node.">parent</abbr>[t] == -1 {
			u := q[0]; q = q[1:]
			for v := 0; v < n; v++ {
				if parent[v] == -1 && cap[u][v]-flow[u][v] > 0 {
					<abbr title="A node that has a child node.">parent</abbr>[v] = u; q = append(q, v)
				}
			}
		}
		if <abbr title="A node that has a child node.">parent</abbr>[t] == -1 { break }
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

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Need a polynomial time guarantee | The graph is massive — Dinic's is much faster |
| A straightforward implementation is preferred | The graph is very dense |

## 17.3. Dinic’s Algorithm

**Definition:** Dinic's algorithm utilizes a level graph (built via BFS) and blocking flows (found via DFS) to dramatically accelerate maximum flow computations, achieving ... complexity.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Build level graph | ... | Using BFS |
| Blocking flow | ... | Using DFS |
| Total | ... | Extremely fast for dense graphs |

### Pseudocode


### Idiomatic Go Implementation

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
					<abbr title="The set of all nodes at a given depth.">level</abbr>[v] = <abbr title="The set of all nodes at a given depth.">level</abbr>[u]+1; q = append(q, v)
				}
			}
		}
		return <abbr title="The set of all nodes at a given depth.">level</abbr>[t] >= 0
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

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Dense graphs | A simpler implementation is preferred (choose Edmonds-Karp) |
| High performance is critical | The graph is trivially small |

## 17.4. Minimum-Cost Flow

**Definition:** Minimum-cost flow finds the maximum flow that incurs the absolute minimum total cost, utilizing the successive shortest path algorithm equipped with Dijkstra on the residual graph.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Successive shortest path | ... | F = max flow |
| Total | ... | Driven by Dijkstra |

### Pseudocode


### Idiomatic Go Implementation

package main

import (
	"container/heap"
	"fmt"
)

type MI struct{ v, d int }
type MPQ []MI
func (q MPQ) Len() int { return len(q) }
func (q MPQ) Less(i, j int) bool { return q[i].d < q[j].d }
func (q MPQ) Swap(i, j int) { q[i], q[j] = q[j], q[i] }
func (q *MPQ) Push(x interface{}) { *q = append(*q, x.(MI)) }
func (q *MPQ) Pop() interface{} { old := *q; n := len(old); *q = old[:n-1]; return old[n-1] }

func minCostFlow(cap, cost [][]int, s, t, maxf int) int {
	n := len(cap)
	flow := make([][]int, n); for i := range flow { flow[i] = make([]int, n) }
	total := 0
	for maxf > 0 {
		dist := make([]int, n); par := make([]int, n)
		for i := range dist { dist[i] = -1; par[i] = -1 }
		dist[s] = 0; pq := &MPQ{{s, 0}}; <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>.Init(pq)
		for pq.Len() > 0 {
			c := <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>.Pop(pq).(MI); if c.d > dist[c.v] { continue }
			for v := 0; v < n; v++ {
				if cap[c.v][v]-flow[c.v][v] > 0 {
					nd := dist[c.v] + cost[c.v][v]
					if dist[v] == -1 || nd < dist[v] { dist[v] = nd; par[v] = c.v; heap.Push(pq, MI{v, nd}) }
				}
			}
		}
		if dist[t] == -1 { break }
		b := maxf
		for v := t; v != s; v = par[v] { if cap[par[v]][v]-flow[par[v]][v] < b { b = cap[par[v]][v]-flow[par[v]][v] } }
		for v := t; v != s; v = par[v] { u := par[v]; flow[u][v] += b; flow[v][u] -= b; total += b*cost[u][v] }
		maxf -= b
	}
	return total
}

func main() {
	cap := [][]int...
	cost := [][]int...
	fmt.Println(minCostFlow(cap, cost, 0, 3, 3))
}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Need to aggressively minimize transportation or assignment cost | You only need max flow without caring about cost |
| All edge costs are positive | There is a negative cost cycle |

## 17.5. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Ford-Fulkerson | Recursive DFS | ... | ... | Educational / Conceptual |
| Edmonds-Karp | BFS + Queue | ... | ... | General purpose max flow |
| Dinic | BFS level + DFS | ... | ... | Dense networks |
| Min-Cost Flow | ... | ... | ... | Logistics, optimal assignment |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 17:</strong> This chapter discusses network flow algorithms: Ford-Fulkerson, Edmonds-Karp, Dinic's, and min-cost flow. Use Edmonds-Karp for <abbr title="An algorithm whose running time is upper bounded by a polynomial expression.">polynomial time</abbr> guarantees, Dinic's for dense networks requiring high performance, and min-cost flow when minimizing transportation or assignment cost.
{{% /alert %}}