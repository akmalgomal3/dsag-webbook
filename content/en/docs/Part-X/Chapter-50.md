---
weight: 100100
title: "Chapter 50: Topological Sort"
description: "Topological Sort"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Topological sort: because some things must happen before others.</em>"</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 50 covers topological sorting. Sorting orders vertices in a directed acyclic graph. Edges point from earlier to later vertices.
{{% /alert %}}

## 50.1. The Problem

**Definition:** Topological sort produces linear ordering. Edges point forward. Sorting enables scheduling and dependency resolution.

**Background:** Tasks have prerequisites. Topological sort models constraints via Directed Acyclic Graphs (DAG). Algorithm confirms linear sequence or detects cycles.

**Use Cases:** Go module compilation. npm dependency resolution. Task orchestration (Apache Airflow).

**Memory Mechanics:** Kahn’s Algorithm uses `inDegree` array and `queue`. Processing zero-dependency nodes ensures cache locality. DFS-based sorting uses call stack. Deep chains risk stack overflow in DFS. Kahn’s algorithm provides memory stability.

### Real-World Examples

| Domain | Dependency | Topological Order |
|--------|-----------|-------------------|
| Build systems | File A includes B | Compile B before A |
| Course prerequisites | CS101 before CS201 | Take 101 first |
| Makefile targets | Object files need sources | Build sources first |
| Data pipelines | Transform A before B | Run A before B |

## 50.2. Algorithms

### Kahn's Algorithm (BFS)

Vertices with zero in-degree are removed.

```go
package main

import "fmt"

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

func main() {
    graph := [][]int{{1}, {2}, {}}
    fmt.Println(topoSortKahn(graph, 3))
}
```

### DFS-Based Algorithm

Explore descendants first. Push vertices to stack. Reverse result.

| Algorithm | Time | Space | Detects Cycles? |
|-----------|------|-------|-----------------|
| Kahn's | <code>O(V + E)</code> | <code>O(V)</code> | Yes (result < V) |
| DFS | <code>O(V + E)</code> | <code>O(V)</code> | Yes |

## 50.3. Decision Matrix

| Use Kahn's When... | Use DFS When... |
|-------------------|-----------------|
| You need to detect cycles explicitly | You want lexicographically smallest order |
| Iterative preferred | Recursive style natural |
| Counting in-degrees is easy | Graph is naturally explored depth-first |

### Edge Cases & Pitfalls

- **Cycles:** Sorting requires DAG. Validate graph.
- **Multiple valid orders:** Sorts are not unique. Logic must handle non-determinism.
- **Disconnected graphs:** Algorithm processes all components.

### Anti-Patterns

- **Hard-coding unique order:** Multiple valid sequences exist. Tie-breaking logic required for determinism.
- **DFS on deep chains:** Deep graphs cause stack overflow. Kahn's iterative queue avoids limit.
- **Ignoring cycle detection:** Undefined on cyclic graphs. Verify result length equals vertex count.
- **Skipping disconnected components:** DAGs contain isolated subgraphs. Seed all start nodes.

## 50.4. Quick Reference

| Concept | Detail |
|---------|--------|
| Input | DAG |
| Output | Linear vertex ordering |
| Cycle check | If result length < V, cycle exists |
| Applications | Scheduling, dependency resolution |

| Go stdlib | Usage |
|-----------|-------|
| `go/build` | Uses topo sort for package imports |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 50:</strong> Topological sort linearizes dependencies. Method provides execution plans. Kahn's algorithm processes prerequisites sequentially.
{{% /alert %}}

## See Also

- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/chapter-12/)
- [Chapter 51: Strongly Connected Components](/docs/part-x/chapter-51/)
- [Chapter 53: Tarjan's Bridge-Finding Algorithm](/docs/part-x/chapter-53/)
