---
weight: 30400
title: "Chapter 12: Graphs and Graph Representations"
description: "Graphs and Graph Representations"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="📘" context="success" %}}
Chapter 12 covers graph representations and traversal. Learn to use slices and maps for optimal cache performance in network structures.
{{% /alert %}}

## 12.1. Graph Representations

**Definition:** Graph models vertices and edges. Common forms include adjacency lists, adjacency matrices, and edge lists.

**Mechanics:**
Representation choice balances query speed against memory usage. Adjacency list records existing edges: saves memory in sparse networks. Adjacency matrix records all possible pairs: provides O(1) edge checks but uses O(V^2) space.

In Go, `[][]int` implements adjacency list. Outer slice holds vertices. Inner slices hold neighbor IDs. Memory footprint is small. `[][]bool` implements adjacency matrix. Consumes gigabytes for large V.

### Operations & Complexity

| Operation | Adj List | Adj Matrix | Edge List |
|---------|----------|------------|-----------|
| Space | <code>O(V+E)</code> | <code>O(V²)</code> | <code>O(E)</code> |
| Add edge | <code>O(1)</code> | <code>O(1)</code> | <code>O(1)</code> |
| Check edge | <code>O(degree)</code> | <code>O(1)</code> | <code>O(E)</code> |
| Iterate neighbors | <code>O(degree)</code> | <code>O(V)</code> | <code>O(E)</code> |

### Pseudocode

```text
Graph(n):
    adj = array of n empty lists

AddEdge(g, u, v):
    append v to adj[u]

Neighbors(g, u):
    return adj[u]
```

### Idiomatic Go Implementation

```go
package main

type Graph struct {
    adj [][]int
}

func NewGraph(n int) *Graph {
    return &Graph{adj: make([][]int, n)}
}

func (g *Graph) AddEdge(u, v int) {
    g.adj[u] = append(g.adj[u], v)
}

func (g *Graph) Neighbors(u int) []int {
    return g.adj[u]
}

func main() {
    g := NewGraph(5)
    g.AddEdge(0, 1)
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Sparse graphs (Adj List) | Dense graphs (Adj Matrix) |
| Fast edge checks needed | Memory is constrained |

### Edge Cases & Pitfalls

- **Self-loop:** Logic must handle `u == v`.
- **Undirected:** Add edge in both directions.
- **Out of Range:** Validate vertex IDs against slice bounds.

## 12.2. Graph Traversal

**Definition:** DFS explores deep paths first. BFS explores neighbors level-by-level.

**Mechanics:**
DFS uses stack or recursion. Solves topological sorting and cycle detection. BFS uses queue. Guarantees shortest path in unweighted graphs.

DFS recursion uses call stack. Deep graphs cause stack overflow. Use explicit slice as heap stack for safety. BFS uses slice as ring buffer to minimize reallocations.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| DFS | <code>O(V + E)</code> | Visit all reachable nodes |
| BFS | <code>O(V + E)</code> | Level-order visit |

### Pseudocode

```text
DFS(g, start):
    seen = array of false
    stack = [start]
    while stack not empty:
        v = pop stack
        if seen[v]: continue
        seen[v] = true
        visit(v)
        for neighbor n of v:
            if not seen[n]: push n to stack

BFS(g, start):
    seen = array of false
    queue = [start]
    seen[start] = true
    while queue not empty:
        v = dequeue
        visit(v)
        for neighbor n of v:
            if not seen[n]:
                seen[n] = true
                enqueue n
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

type Graph struct {
    adj [][]int
}

func (g *Graph) DFS(start int, visit func(int)) {
    seen := make([]bool, len(g.adj))
    var stk []int
    stk = append(stk, start)

    for len(stk) > 0 {
        v := stk[len(stk)-1]
        stk = stk[:len(stk)-1]
        if seen[v] { continue }
        seen[v] = true
        visit(v)
        for _, n := range g.adj[v] {
            if !seen[n] { stk = append(stk, n) }
        }
    }
}

func (g *Graph) BFS(start int, visit func(int)) {
    seen := make([]bool, len(g.adj))
    q := []int{start}
    seen[start] = true
    front := 0
    for front < len(q) {
        v := q[front]
        front++
        visit(v)
        for _, n := range g.adj[v] {
            if !seen[n] {
                seen[n] = true
                q = append(q, n)
            }
        }
    }
}
```

## 12.3. Shortest Path & MST

**Definition:** Dijkstra finds shortest weighted path. Kruskal and Prim find Minimum Spanning Tree (MST).

**Mechanics:**
Dijkstra uses greedy optimization. Processes cheapest route first via Priority Queue. Kruskal sorts edges and uses Union-Find. Prim expands from node via Priority Queue.

Dijkstra uses Min-Heap. Slice-backed heap stays in CPU cache. Random vertex access causes some cache thrashing. Speed of array-backed structures minimizes penalty.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Dijkstra | <code>O((V+E) log V)</code> | Priority queue required |
| Kruskal | <code>O(E log E)</code> | Sort edges + DSU |
| Prim | <code>O(E log V)</code> | Priority queue required |

### Idiomatic Go Implementation (Dijkstra)

```go
package main

import (
    "container/heap"
    "math"
)

type State struct { v, dist int }
type MinHeap []State
func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i].dist < h[j].dist }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x any)        { *h = append(*h, x.(State)) }
func (h *MinHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}

func (g *Graph) Dijkstra(src int, adj [][][2]int) []int {
    dist := make([]int, len(adj))
    for i := range dist { dist[i] = math.MaxInt32 }
    dist[src] = 0
    h := &MinHeap{{src, 0}}
    heap.Init(h)
    for h.Len() > 0 {
        s := heap.Pop(h).(State)
        if s.dist > dist[s.v] { continue }
        for _, e := range adj[s.v] {
            if nd := s.dist + e[1]; nd < dist[e[0]] {
                dist[e[0]] = nd
                heap.Push(h, State{e[0], nd})
            }
        }
    }
    return dist
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Weighted shortest path | Negative weights exist (use Bellman-Ford) |
| Sparse graph MST | Dense graph MST (Prim is better) |

### Anti-Patterns

- **Nested Maps:** `map[int]map[int]bool` destroys cache locality. Use `[][]int`.
- **Map Visited:** Using map for visited IDs is slow. Use `[]bool` indexed by vertex ID.
- **Incomplete Search:** Single-source visit misses isolated nodes. Loop through all nodes.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Adj List | `[][]int` | <code>O(V+E)</code> | <code>O(V+E)</code> | Sparse graphs |
| Adj Matrix | `[][]bool` | <code>O(1)</code> | <code>O(V^2)</code> | Dense graphs |
| Dijkstra | Min-Heap | <code>O(E log V)</code> | <code>O(V)</code> | Shortest path |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Use adjacency lists for sparse graphs. Use DFS for sorting. Use BFS for shortest unweighted path. Use Dijkstra for weights.
{{% /alert %}}

## See Also

- [Chapter 11: Disjoint Sets](/docs/part-iii/chapter-11/)
- [Chapter 13: Graph Traversal Algorithms](/docs/part-iv/chapter-13/)
- [Chapter 14: Single-Source Shortest Paths](/docs/part-iv/chapter-14/)
