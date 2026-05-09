---
weight: 100100
title: "Chapter 51 - Topological Sort"
description: "Topological Sort"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Topological sort: because some things must happen before others.</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 51 covers topological sorting — ordering the vertices of a directed acyclic graph so that every edge goes from earlier to later in the ordering.
{{% /alert %}}

## 51.1. The Problem

**Definition:** A <abbr title="A linear ordering of vertices in a directed acyclic graph such that for every directed edge uv, vertex u comes before v in the ordering.">topological sort</abbr> of a <abbr title="A directed graph with no directed cycles.">DAG</abbr> produces a linear ordering where all edges point forward. Essential for scheduling, dependency resolution, and compilation.

### Real-World Examples

| Domain | Dependency | Topological Order |
|--------|-----------|-------------------|
| Build systems | File A includes B | Compile B before A |
| Course prerequisites | CS101 before CS201 | Take 101 first |
| Makefile targets | Object files need sources | Build sources first |
| Data pipelines | Transform A before B | Run A before B |

## 51.2. Algorithms

### Kahn's Algorithm (BFS)

Repeatedly remove vertices with zero in-degree:

```go
func topoSortKahn(graph [][]int, n int) []int {
    inDegree := make([]int, n)
    for _, edges := range graph {
        for _, v := range edges {
            inDegree[v]++
        }
    }
    
    queue := []int{}
    for i, d := range inDegree {
        if d == 0 {
            queue = append(queue, i)
        }
    }
    
    result := []int{}
    for len(queue) > 0 {
        u := queue[0]
        queue = queue[1:]
        result = append(result, u)
        
        for _, v := range graph[u] {
            inDegree[v]--
            if inDegree[v] == 0 {
                queue = append(queue, v)
            }
        }
    }
    
    if len(result) != n {
        return nil // Cycle detected
    }
    return result
}
```

### DFS-Based Algorithm

Push vertices onto a stack after exploring all descendants, then reverse.

| Algorithm | Time | Space | Detects Cycles? |
|-----------|------|-------|-----------------|
| Kahn's | O(V + E) | O(V) | Yes (result < V) |
| DFS | O(V + E) | O(V) | Yes |

## 51.3. Decision Matrix

| Use Kahn's When... | Use DFS When... |
|-------------------|-----------------|
| You need to detect cycles explicitly | You want lexicographically smallest order |
| Iterative preferred | Recursive style natural |
| Counting in-degrees is easy | Graph is naturally explored depth-first |

### Edge Cases & Pitfalls

- **Cycles:** Topological sort is impossible on cyclic graphs — always check.
- **Multiple valid orders:** Topological sorts are not unique; don't assume determinism.
- **Disconnected graphs:** Works fine — process each component.

## 51.4. Quick Reference

| Concept | Detail |
|---------|--------|
| Input | DAG |
| Output | Linear vertex ordering |
| Cycle check | If result length < V, cycle exists |
| Applications | Scheduling, dependency resolution |

| Go stdlib | Usage |
|-----------|-------|
| `go/build` | Uses topo sort for package imports |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 51:</strong> Topological sort transforms a web of dependencies into a linear execution plan. Whether building software, scheduling courses, or orchestrating data pipelines, it answers the fundamental question: "What comes first?" The elegance of Kahn's algorithm lies in its simplicity — repeatedly doing what has no prerequisites until everything is done.
{{% /alert %}}

## See Also

- [Chapter 12 — Graphs and Graph Representations](/docs/Part-III/Chapter-12/)
- [Chapter 52 — Strongly Connected Components](/docs/Part-X/Chapter-52/)
- [Chapter 54 — Tarjan's Bridge-Finding Algorithm](/docs/Part-X/Chapter-54/)

