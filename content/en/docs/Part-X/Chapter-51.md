---
weight: 100200
title: "Chapter 51: Strongly Connected Components"
description: "Strongly Connected Components"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>To understand a <abbr title="A graph where edges have direction from one vertex to another">directed graph</abbr>, first find its strongly connected components.</em>" — Robert Tarjan</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 51 covers strongly connected components (SCCs). Vertices in SCCs are mutually reachable. Algorithms include Tarjan's and Kosaraju's.
{{% /alert %}}

## 51.1. What Are SCCs?

**Definition:** Strongly connected component is maximal vertex set. Every vertex reaches every other vertex. SCCs partition directed graphs into DAG meta-nodes.

**Background:** Condensation simplifies complex graphs. Algorithms group tightly interconnected nodes. Grouping collapses graphs into Directed Acyclic Graphs (DAG). Macro-structure analysis becomes possible.

**Use Cases:** Social media cluster analysis. Database query optimization. Compiler logic for recursive calls.

**Memory Mechanics:** Kosaraju's algorithm uses two passes. Method requires graph transposition. Transposition doubles heap footprint. GC overhead increases on large datasets. Tarjan's algorithm uses single pass. Discovery and low-link arrays track roots. Method avoids secondary graph allocation. RAM usage decreases. Recursive call stack pressure increases.

### Condensation Graph

SCC contraction creates condensation graphs. Condensation graphs are always DAGs.

| Original Graph | SCCs | Condensation |
|---------------|------|--------------|
| Complex directed | {A,B,C}, {D}, {E,F} | DAG of 3 nodes |

## 51.2. Kosaraju's Algorithm

1. DFS on original graph. Push nodes to stack in finish order.
2. Reverse edges.
3. DFS from stack top on reversed graph. Each tree identifies one SCC.

```go
package main

import "fmt"

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

func main() {
    graph := [][]int{{1}, {2}, {0}}
    fmt.Println(kosaraju(graph, 3))
}
```

## 51.3. Tarjan's Algorithm

Single-pass DFS identifies SCC roots. Discovery times and low-link values enable tracking.

| Algorithm | Passes | Space | Simplicity |
|-----------|--------|-------|------------|
| Kosaraju | 2 DFS + transpose | <code>O(V + E)</code> | Easier to understand |
| Tarjan | 1 DFS | <code>O(V)</code> | Slightly faster |

## 51.4. Applications

| Application | SCC Use |
|-------------|---------|
| **2-SAT** | Each SCC gives a variable assignment |
| **Dead code** | Unreachable SCCs in call graphs |
| **Web crawling** | Find clusters of mutually linking pages |
| **Package management** | Detect circular dependencies |

## 51.5. Decision Matrix

| Use Kosaraju When... | Use Tarjan When... |
|---------------------|-------------------|
| Teaching or learning the concept | Production code |
| Memory is not a critical constraint | Minimizing passes matters |
| Two-pass logic is clearer | Single-pass simplicity is strictly preferred |

### Edge Cases & Pitfalls

- **Single-node SCCs:** Isolated vertices function as independent SCCs.
- **Self-loops:** Loops create SCCs of size 1.
- **Large graphs:** Recursion depth risks stack overflow. Iterative DFS provides safety.

### Anti-Patterns

- **Confusing orders:** Kosaraju finish stack is reverse topological order. Misinterpretation causes condensation errors.
- **Ignoring memory limits:** Kosaraju doubles heap usage. Tarjan preserves RAM.
- **Filtering single nodes:** Isolated vertices are legitimate SCCs. Removal skews condensation DAG.
- **Over-optimizing:** Tarjan is faster but complex. Kosaraju suffices for non-critical memory.

## 51.6. Quick Reference

| Concept | Value |
|---------|-------|
| Time complexity | <code>O(V + E)</code> |
| Space complexity | <code>O(V)</code> |
| Condensation | Always a DAG |

| Go stdlib | Usage |
|-----------|-------|
| No direct stdlib | Implement manually for deep graph analysis |


{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 51:</strong> SCCs reveal cyclic structures. Contraction enables graph analysis. Algorithms achieve linear time complexity.
{{% /alert %}}

## See Also

- [Chapter 50: Topological Sort](/docs/part-x/chapter-50/)
- [Chapter 52: A* Search](/docs/part-x/chapter-52/)
- [Chapter 53: Tarjan's Bridge-Finding Algorithm](/docs/part-x/chapter-53/)