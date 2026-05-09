---
weight: 40600
title: "Chapter 18 - Matchings in Bipartite Graphs"
description: "Matchings in Bipartite Graphs"
icon: "article"
date: "2024-08-24T23:42:32+07:00"
lastmod: "2024-08-24T23:42:32+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the most direct way to make our ideas into action.</em>" — Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 18 focuses on Matchings in Bipartite Graphs, detailing the Hungarian Algorithm for optimal weighted assignments and Hopcroft-Karp for executing maximum cardinality matching efficiently.
{{% /alert %}}

## 18.1. Bipartite Graphs and Matching

**Definition:** A bipartite <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> is a <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> whose vertices can be partitioned into two disjoint sets, U and V, such that every <abbr title="A connection between two vertices in a graph.">edge</abbr> connects a <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> in U to one in V. A matching is a set of edges that do not share any vertices.

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
{{< prism lang="go" line-numbers="true">}}
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
{{< /prism >}}

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

{{< prism lang="go" line-numbers="true">}}
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
	cost := [][]int...
	fmt.Println(hungarian(cost))
}
{{< /prism >}}

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

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| BFS level | ... | Per phase |
| DFS augment | ... | Per phase |
| Total | ... | Up to ... phases |

### Pseudocode


### Idiomatic Go Implementation

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
	adj := [][]int...
	fmt.Println(hopcroftKarp(adj, 3, 3))
}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Exploring unweighted bipartite matching | It is a weighted graph — use Hungarian |
| Maximizing the cardinality of the matching | It is a general graph — use the Blossom algorithm |

### Edge Cases & Pitfalls

- **Left-right partition:** Double-check that ... and ... sizes accurately match your inputs.
- **Multiple edges:** Hopcroft-Karp handles duplicate edges gracefully without breaking.

## 18.4. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Bipartite Check | ... color | ... | ... | Structure validation |
| Hungarian | ... | ... | ... | Weighted assignment |
| Hopcroft-Karp | ... adj | ... | ... | Max cardinality matching |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 18:</strong> This chapter covers bipartite <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> validation, the Hungarian algorithm for weighted assignment, and Hopcroft-Karp for maximum cardinality matching. Use Hungarian for square cost matrices and Hopcroft-Karp for large unweighted bipartite matching problems.
{{% /alert %}}