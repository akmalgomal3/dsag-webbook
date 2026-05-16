---
weight: 40600
title: "Chapter 18: Matchings in Bipartite Graphs"
description: "Matchings in Bipartite Graphs"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the most direct way to make our ideas into action.</em>" — Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 18: Bipartite Matching. Covers Hungarian Algorithm for weighted assignments and Hopcroft-Karp for maximum cardinality matching.
{{% /alert %}}

## 18.1. Bipartite Graphs and Matching

**Definition:** Bipartite graphs partition vertices into disjoint sets U and V. Edges only connect U to V. Matching creates vertex-disjoint edge sets.

**Logic:**
Conflict resolution. Pairs resources (U) with consumers (V). Proving bipartiteness via two-coloring enables optimized algorithms like Hopcroft-Karp.

**Use Cases:**
Ride-sharing dispatch. Job scheduling. Dating apps.

**Memory Mechanics:**
Bipartite check uses BFS. `color` array tracks partitions. O(V) memory usage. Stores small integer states. High CPU cache efficiency for massive node counts.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Bipartite check | <code>O(V+E)</code> | BFS coloring |
| Maximum matching | <code>O(E√V)</code> | Hopcroft-Karp |
| Weighted assignment | <code>O(V³)</code> | Hungarian Algorithm |

### Pseudocode

```text
IsBipartite(graph):
    color = array filled with -1
    for each vertex i:
        if color[i] != -1: continue
        queue = [i]
        color[i] = 0
        while queue not empty:
            v = dequeue(queue)
            for each neighbor u of v:
                if color[u] == -1:
                    color[u] = 1 - color[v]
                    enqueue(queue, u)
                else if color[u] == color[v]:
                    return false
    return true
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func isBipartite(g [][]int) bool {
	n := len(g)
	color := make([]int, n)
	for i := range color { color[i] = -1 }
	for i := 0; i < n; i++ {
		if color[i] != -1 { continue }
		q := []int{i}; color[i] = 0
		for len(q) > 0 {
			v := q[0]; q = q[1:]
			for _, u := range g[v] {
				if color[u] == -1 { color[u] = 1 - color[v]; q = append(q, u) }
				if color[u] == color[v] { return false }
			}
		}
	}
	return true
}

func main() {
	g := [][]int{{1, 3}, {0, 2}, {1, 3}, {0, 2}}
	fmt.Println(isBipartite(g))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| U-V structure is defined | Dealing with general graphs. Use Blossom algorithm. |
| Solving assignment problems | Non-bipartite matching required |

### Edge Cases & Pitfalls

- **Disconnected graph:** Check all components.
- **Self-loop:** Bipartite check fails immediately.

## 18.2. Hungarian Algorithm

**Definition:** Solves weighted assignment problems. Finds minimum cost matching in bipartite graphs.

**Logic:**
Matrix manipulation. Theorem: modifying row/column potentials preserves optimal assignment. Goal: produce matrix with zero-cost perfect matching.

**Use Cases:**
Task allocation. Payroll minimization. Resource-heavy optimization.

**Memory Mechanics:**
Manipulates 2D cost matrix. Uses parallel arrays for dual variables. Upfront allocation minimizes GC overhead. Vertical column scans may cause cache misses on large datasets.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Potentials update | <code>O(V^2)</code> | Per iteration |
| Total | <code>O(V³)</code> | For all iterations |

### Pseudocode

```text
Hungarian(cost):
    n = size of cost
    u, v, p, way = arrays size n+1
    for i from 1 to n:
        initialize minv and used
        repeat:
            find column j with minimum reduced cost
            update potentials u and v
            shift column j0
        until p[j0] == 0
        augment matching along way
    return -v[0]
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func hungarian(cost [][]int) int {
	n := len(cost)
	u := make([]int, n+1); v := make([]int, n+1)
	p := make([]int, n+1); way := make([]int, n+1)
	for i := 1; i <= n; i++ {
		p[0] = i; j0 := 0
		minv := make([]int, n+1); used := make([]bool, n+1)
		for j := 1; j <= n; j++ { minv[j] = 1<<30; used[j] = false }
		for {
			used[j0] = true; i0 := p[j0]; delta := 1<<30; j1 := 0
			for j := 1; j <= n; j++ {
				if !used[j] {
					cur := cost[i0-1][j-1] - u[i0] - v[j]
					if cur < minv[j] { minv[j] = cur; way[j] = j0 }
					if minv[j] < delta { delta = minv[j]; j1 = j }
				}
			}
			for j := 0; j <= n; j++ {
				if used[j] { u[p[j]] += delta; v[j] -= delta } else { minv[j] -= delta }
			}
			j0 = j1
			if p[j0] == 0 { break }
		}
		for {
			j1 := way[j0]; p[j0] = p[j1]; j0 = j1
			if j0 == 0 { break }
		}
	}
	return -v[0]
}

func main() {
	cost := [][]int{{5, 10}, {15, 20}}
	fmt.Println(hungarian(cost)) // Outputs: 25
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Weighted assignment problem | Unweighted graph. Use Hopcroft-Karp. |
| Square cost matrix | Rectangular matrix. Requires padding. |

### Edge Cases & Pitfalls

- **Negative costs:** Offset weights with large constant.
- **Rectangular matrices:** Pad with weight-0 dummy nodes.

## 18.3. Hopcroft-Karp Algorithm

**Definition:** Finds maximum cardinality matching in unweighted bipartite graphs. Combines BFS level graphs with DFS augmenting paths.

**Logic:**
Batch augmentation. BFS partitions unmatched nodes into distance layers. DFS finds all disjoint augmenting paths of current length simultaneously.

**Use Cases:**
Massive unweighted assignments. University course enrollment.

**Memory Mechanics:**
Uses adjacency lists and 1D tracking slices. Reusing BFS queue reduces GC pressure. Scales to millions of nodes.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| BFS phase | <code>O(E)</code> | Level construction |
| DFS phase | <code>O(V)</code> | Path augmentation |
| Total | <code>O(E √V)</code> | High scalability |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func hopcroftKarp(adj [][]int, nLeft, nRight int) int {
	pairU := make([]int, nLeft); pairV := make([]int, nRight)
	dist := make([]int, nLeft)
	for i := range pairU { pairU[i] = -1 }
	for i := range pairV { pairV[i] = -1 }
	bfs := func() bool {
		q := []int{}
		for u := 0; u < nLeft; u++ {
			if pairU[u] == -1 { dist[u] = 0; q = append(q, u) } else { dist[u] = -1 }
		}
		found := false
		for len(q) > 0 {
			u := q[0]; q = q[1:]
			for _, v := range adj[u] {
				pu := pairV[v]
				if pu != -1 && dist[pu] == -1 { dist[pu] = dist[u]+1; q = append(q, pu) }
				if pu == -1 { found = true }
			}
		}
		return found
	}
	var dfs func(u int) bool
	dfs = func(u int) bool {
		for _, v := range adj[u] {
			pu := pairV[v]
			if pu == -1 || (dist[pu] == dist[u]+1 && dfs(pu)) {
				pairU[u] = v; pairV[v] = u
				return true
			}
		}
		dist[u] = -1
		return false
	}
	matching := 0
	for bfs() {
		for u := 0; u < nLeft; u++ {
			if pairU[u] == -1 && dfs(u) { matching++ }
		}
	}
	return matching
}

func main() {
	adj := [][]int{{0}, {0, 1}, {1, 2}}
	fmt.Println(hopcroftKarp(adj, 3, 3)) // Output: 3
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Unweighted bipartite matching | Weighted graph. Use Hungarian. |
| Maximum cardinality required | General graph. Use Blossom algorithm. |

### Anti-Patterns

- **Greedy matching without augmentation:** Fails to guarantee maximum matching. Use augmenting paths.
- **Incorrect BFS reset:** Clear layering logic (`dist []int`) per phase.
- **Inefficient adjacency storage:** Use `[][]int` adjacency lists. Avoid `map[int][]int` for performance.

## 18.4. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Bipartite Check | `[]int` color | <code>O(V + E)</code> | <code>O(V)</code> | Structure validation |
| Hungarian | `[][]int` matrix | <code>O(V³)</code> | <code>O(V²)</code> | Weighted assignment |
| Hopcroft-Karp | `[][]int` adj | <code>O(E √V)</code> | <code>O(V)</code> | Max cardinality matching |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 18:</strong> Bipartite matching optimization. Use Hungarian for weighted costs. Use Hopcroft-Karp for large-scale unweighted matching.
{{% /alert %}}

## See Also

- [Chapter 16: Minimum Spanning Trees](/docs/part-iv/chapter-16/)
- [Chapter 17: Network Flow Algorithms](/docs/part-iv/chapter-17/)
- [Chapter 51: Strongly Connected Components](/docs/part-x/chapter-51/)
