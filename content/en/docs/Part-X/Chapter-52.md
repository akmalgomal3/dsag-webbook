---
weight: 100200
title: "Chapter 52 - Strongly Connected Components"
description: "Strongly Connected Components"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>To understand a directed graph, first find its strongly connected components.</em>" — Robert Tarjan</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 52 explores strongly connected components (SCCs) — maximal subgraphs where every vertex is reachable from every other vertex — and Tarjan's and Kosaraju's algorithms for finding them.
{{% /alert %}}

## 52.1. What Are SCCs?

**Definition:** A <abbr title="A maximal subgraph of a directed graph where every vertex is reachable from every other vertex.">strongly connected component</abbr> is a maximal set of vertices where each vertex is reachable from every other. SCCs partition a directed graph into a DAG of meta-nodes.

### Condensation Graph

Contracting each SCC to a single node yields the <abbr title="A DAG formed by contracting each SCC of a directed graph into a single vertex.">condensation graph</abbr> — always a DAG.

| Original Graph | SCCs | Condensation |
|---------------|------|--------------|
| Complex directed | {A,B,C}, {D}, {E,F} | DAG of 3 nodes |

## 52.2. Kosaraju's Algorithm

1. DFS on original graph, push nodes to stack in finish order
2. Reverse all edges
3. DFS from stack top on reversed graph — each tree is an SCC

```go
func kosaraju(graph [][]int, n int) [][]int {
    // Step 1: DFS and fill stack
    visited := make([]bool, n)
    stack := []int{}
    
    var dfs1 func(u int)
    dfs1 = func(u int) {
        visited[u] = true
        for _, v := range graph[u] {
            if !visited[v] {
                dfs1(v)
            }
        }
        stack = append(stack, u)
    }
    
    for i := 0; i < n; i++ {
        if !visited[i] {
            dfs1(i)
        }
    }
    
    // Step 2: Build transpose
    transposed := make([][]int, n)
    for u, edges := range graph {
        for _, v := range edges {
            transposed[v] = append(transposed[v], u)
        }
    }
    
    // Step 3: DFS on transpose in stack order
    visited = make([]bool, n)
    var scc []int
    var result [][]int
    
    var dfs2 func(u int)
    dfs2 = func(u int) {
        visited[u] = true
        scc = append(scc, u)
        for _, v := range transposed[u] {
            if !visited[v] {
                dfs2(v)
            }
        }
    }
    
    for i := len(stack) - 1; i >= 0; i-- {
        v := stack[i]
        if !visited[v] {
            scc = nil
            dfs2(v)
            result = append(result, append([]int(nil), scc...))
        }
    }
    
    return result
}
```

## 52.3. Tarjan's Algorithm

Single-pass DFS using discovery times and low-link values to identify SCC roots.

| Algorithm | Passes | Space | Simplicity |
|-----------|--------|-------|------------|
| Kosaraju | 2 DFS + transpose | O(V + E) | Easier to understand |
| Tarjan | 1 DFS | O(V) | Slightly faster |

## 52.4. Applications

| Application | SCC Use |
|-------------|---------|
| **2-SAT** | Each SCC gives a variable assignment |
| **Dead code** | Unreachable SCCs in call graphs |
| **Web crawling** | Find clusters of mutually linking pages |
| **Package management** | Detect circular dependencies |

## 52.5. Decision Matrix

| Use Kosaraju When... | Use Tarjan When... |
|---------------------|-------------------|
| Teaching/learning | Production code |
| Memory not critical | Minimizing passes matters |
| Two-pass logic clearer | Single-pass simplicity preferred |

### Edge Cases & Pitfalls

- **Single-node SCCs:** Every isolated vertex is its own SCC.
- **Self-loops:** Create SCCs of size 1.
- **Large graphs:** Recursion depth may overflow — use iterative DFS or increase stack.

## 52.6. Quick Reference

| Concept | Value |
|---------|-------|
| Time complexity | O(V + E) |
| Space complexity | O(V) |
| Condensation | Always a DAG |

| Go stdlib | Usage |
|-----------|-------|
| No direct stdlib | Implement for graph analysis |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 52:</strong> Strongly connected components reveal the cyclic structure of directed graphs. By contracting SCCs into a DAG, complex graphs become analyzable. Kosaraju's elegant two-pass approach and Tarjan's single-pass efficiency both achieve O(V + E) — proving that deep structural insights often come from simple traversals.
{{% /alert %}}

## See Also

- [Chapter 51 — Topological Sort](/docs/Part-X/Chapter-51/)
- [Chapter 53 — A* Search](/docs/Part-X/Chapter-53/)
- [Chapter 54 — Tarjan's Bridge-Finding Algorithm](/docs/Part-X/Chapter-54/)

