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
<strong>"<em>Algorithms are the most direct way to make our ideas into action.</em>" : Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 18 focuses on Matchings in Bipartite Graphs, detailing the Hungarian Algorithm for optimal weighted assignments and Hopcroft-Karp for executing maximum cardinality matching efficiently.
{{% /alert %}}

## 18.1. Bipartite Graphs and Matching

**Definition:** A bipartite <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> is a <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> whose vertices can be partitioned into two disjoint sets, U and V, such that every <abbr title="A connection between two vertices in a graph.">edge</abbr> connects a <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> in U to one in V. A matching is a set of edges that do not share any vertices.

**Background & Philosophy:**
Bipartite graphs model two distinct classes of objects that only interact across class lines. The philosophy of matching is conflict resolution: given a set of resources (U) and a set of consumers (V), how do we pair them exclusively without any overlaps? By mathematically proving a graph is bipartite (using two-coloring), we can unlock hyper-optimized algorithms (like Hopcroft-Karp) that would otherwise fail on general graphs.

**Use Cases:**
Used in ride-sharing apps (matching Riders to Drivers), dating apps (matching Users), and job scheduling algorithms in cloud infrastructure (matching Pods to available Worker Nodes).

**Memory Mechanics:**
Checking if a graph is bipartite uses a standard BFS. The `color` array (acting as both the `visited` map and the partition tracker) takes <code>O(V)</code> memory. Because BFS explores layer by layer, it accesses the `color` array randomly based on edge connections. However, since the array merely stores small integer states (`-1`, `0`, `1`), the memory footprint is minimal and fits comfortably in the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> even for millions of nodes.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Bipartite check | <code>O(V+E)</code> | BFS coloring |
| Maximum matching (HK) | <code>O(E√V)</code> | Hopcroft-Karp |
| Minimum weight (Hungarian) | <code>O(V³)</code> | Assignment problem |

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

Bipartite check using BFS:
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
| The U-V structure is clearly defined | Dealing with general graphs — use the Blossom algorithm |
| Solving assignment problems | Solving non-bipartite matchings |

### Edge Cases & Pitfalls

- **Disconnected <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>:** Ensure all components are checked.
- **Self-loop:** Immediately causes a bipartite check failure.

## 18.2. Hungarian Algorithm

**Definition:** The Hungarian Algorithm solves the assignment problem by finding the minimum total cost matching in a weighted bipartite <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>.

**Background & Philosophy:**
The Hungarian algorithm approaches the assignment problem using matrix manipulation (specifically, adding and subtracting potentials). The philosophy is based on the theorem that if a number is added to or subtracted from all entries of any row or column of a cost matrix, an optimal assignment for the resulting cost matrix is also an optimal assignment for the original matrix. The goal is to manipulate the matrix until a perfect matching of zeroes appears.

**Use Cases:**
Perfect for allocating tasks to workers where each worker has a different cost or time to complete a specific task, aiming to minimize the overall payroll or execution time.

**Memory Mechanics:**
The algorithm heavily manipulates a 2D `cost` matrix, making its memory access patterns dense. Go implementations typically use several parallel arrays (`u`, `v`, `p`, `way`, `minv`, `used`) to track dual variables and path construction. By allocating these arrays once upfront (`make([]int, n+1)`), the <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> overhead is practically zero during the loop execution. Because it constantly scans rows and columns, <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr> happen when scanning columns vertically, leading to the strict <code>O(V^3)</code> empirical runtime on large sets.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Potentials update | <code>O(V^2)</code> | Per <abbr title="The repetition of a process, typically using loops.">iteration</abbr> |
| Total | <code>O(V³)</code> | For V iterations |

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
    // 2 workers, 2 tasks. Costs: Worker 1 (5, 10), Worker 2 (15, 20)
	cost := [][]int{{5, 10}, {15, 20}}
	fmt.Println(hungarian(cost)) // Outputs: 25
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Solving weighted assignments | Graph is unweighted — use Hopcroft-Karp |
| The cost matrix is strictly square | Rectangular matrices — requires dummy padding |

### Edge Cases & Pitfalls

- **Negative costs:** Add a large constant offset to all edge weights.
- **Rectangular matrix:** Pad it with dummy nodes and edges of weight 0 to make it square.

## 18.3. Hopcroft-Karp Algorithm

**Definition:** Hopcroft-Karp finds the maximum cardinality matching in a bipartite graph by combining BFS to build a layered level graph and DFS to find augmenting paths efficiently.

**Background & Philosophy:**
Hopcroft-Karp mirrors the logic of Dinic's Algorithm (from Network Flow) but applies it exclusively to unweighted bipartite graphs. The philosophy is "batch augmentation." Instead of finding one matching at a time, it runs BFS to partition the un-matched nodes into distance layers, then runs DFS to snatch up every possible disjoint augmenting path of that specific length simultaneously. 

**Use Cases:**
Massive unweighted assignment problems, such as matching thousands of university students to available courses based purely on their preference lists (without any priority weights).

**Memory Mechanics:**
Hopcroft-Karp requires an <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">adjacency list</abbr> `[][]int` and pairs of tracking arrays (`pairU`, `pairV`, `dist`). Because it operates entirely on 1D slices and avoids complex 2D capacity matrices, it scales exceptionally well. The BFS phase allocates a temporary queue in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. Reusing a pre-allocated slice for this queue across the <code>O(√V)</code> phases drastically reduces the Go <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector's</abbr> burden, enabling millions of nodes to be matched in milliseconds.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| BFS level | <code>O(E)</code> | Per phase |
| DFS augment | <code>O(V)</code> | Per phase |
| Total | <code>O(E √V)</code> | Up to `√V` phases |

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
| Exploring unweighted bipartite matching | It is a weighted graph — use Hungarian |
| Maximizing the cardinality of the matching | It is a general graph — use the Blossom algorithm |

### Edge Cases & Pitfalls

- **Left-right partition:** Double-check that left and right partition sizes accurately match your inputs.
- **Multiple edges:** Hopcroft-Karp handles duplicate edges gracefully without breaking.

### Anti-Patterns

- **Greedy matching without augmenting paths:** Greedily picking edges does not guarantee maximum matching. Always use Hungarian augmenting paths or Hopcroft-Karp for optimality.
- **Forgetting to reset `visited` per augmenting-BFS iteration:** In Hopcroft-Karp, the distance layering (`dist []int`) is rebuilt each phase, but the per-DFS `seen` set must be cleared per vertex, not globally.
- **Using `map[int][]int` for adjacency on small integer vertex IDs:** A `[][]int` adjacency list with pre-allocated capacity is faster and produces less GC pressure than map-based adjacency.

## 18.4. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Bipartite Check | `[]int` color | <code>O(V + E)</code> | <code>O(V)</code> | Structure validation |
| Hungarian | `[][]int` matrix | <code>O(V³)</code> | <code>O(V²)</code> | Weighted assignment |
| Hopcroft-Karp | `[][]int` adj | <code>O(E √V)</code> | <code>O(V)</code> | Max cardinality matching |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 18:</strong> This chapter covers bipartite <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> validation, the Hungarian algorithm for weighted assignment, and Hopcroft-Karp for maximum cardinality matching. Use Hungarian for square cost matrices and Hopcroft-Karp for large unweighted bipartite matching problems.
{{% /alert %}}

## See Also

- [Chapter 16: Minimum Spanning Trees](/docs/part-iv/chapter-16/)
- [Chapter 17: Network Flow Algorithms](/docs/part-iv/chapter-17/)
- [Chapter 51: Strongly Connected Components](/docs/part-x/chapter-51/)
