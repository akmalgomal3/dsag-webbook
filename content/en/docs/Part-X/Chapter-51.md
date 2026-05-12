---
weight: 100100
title: "Chapter 51: Topological Sort"
description: "Topological Sort"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Topological sort: because some things must happen before others.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 51 covers topological sorting: ordering the vertices of a directed <abbr title="A graph containing no cycles">acyclic graph</abbr> so that every edge goes from earlier to later in the ordering.
{{% /alert %}}

## 51.1. The Problem

**Definition:** A <abbr title="A linear ordering of vertices in a directed acyclic graph such that for every directed edge uv, vertex u comes before v in the ordering.">topological sort</abbr> of a <abbr title="A directed graph with no directed cycles.">DAG</abbr> produces a linear ordering where all edges point forward. Essential for scheduling, dependency resolution, and compilation.

**Background & Philosophy:**
The philosophy is dependency resolution. In any complex system (compiling code, baking a cake), certain tasks are strictly blocked until prerequisites finish. Topological sort abstracts this real-world constraint into a mathematical Directed <abbr title="A graph containing no cycles">Acyclic Graph</abbr> (DAG), proving whether a viable linear sequence exists or if a paradox (cycle) prevents execution.

**Use Cases:**
Go's module compiler resolving package imports, npm `package.json` dependency graphs, and task orchestration engines like Apache Airflow.

**Memory Mechanics:**
Kahn’s Algorithm explicitly utilizes an `inDegree` integer array and a `queue` slice. By processing nodes with zero dependencies, it reads linearly from the queue, providing decent <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality. DFS-based topological sorting pushes nodes to the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>, executing recursively. If the dependency chain is exceedingly deep (thousands of sequential tasks), the DFS recursion risks <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>. Thus, Kahn’s queue-based approach is often preferred for memory stability in immense graphs.

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

Push vertices onto a stack after exploring all descendants, then reverse.

| Algorithm | Time | Space | Detects Cycles? |
|-----------|------|-------|-----------------|
| Kahn's | <code>O(V + E)</code> | <code>O(V)</code> | Yes (result < V) |
| DFS | <code>O(V + E)</code> | <code>O(V)</code> | Yes |

## 51.3. Decision Matrix

| Use Kahn's When... | Use DFS When... |
|-------------------|-----------------|
| You need to detect cycles explicitly | You want lexicographically smallest order |
| Iterative preferred | Recursive style natural |
| Counting in-degrees is easy | Graph is naturally explored depth-first |

### Edge Cases & Pitfalls

- **Cycles:** Topological sort is impossible on cyclic graphs; always check for validity.
- **Multiple valid orders:** Topological sorts are rarely unique; do not assume determinism.
- **Disconnected graphs:** Works perfectly fine; meticulously process each disconnected component.

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
<strong>Summary Chapter 51:</strong> Topological sort transforms a web of dependencies into a linear execution plan. Whether building software, scheduling courses, or orchestrating data pipelines, it answers the fundamental question: "What comes first?" The elegance of Kahn's algorithm lies in its simplicity: repeatedly doing what has no prerequisites until everything is done.
{{% /alert %}}

## See Also

- [Chapter 12: Graphs and Graph Representations](/docs/Part-III/Chapter-12/)
- [Chapter 52: Strongly Connected Components](/docs/Part-X/Chapter-52/)
- [Chapter 54: Tarjan's Bridge-Finding Algorithm](/docs/Part-X/Chapter-54/)
