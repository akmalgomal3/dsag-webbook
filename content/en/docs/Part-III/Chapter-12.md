---
weight: 30400
title: "Chapter 12 - Graphs and Graph Representations"
description: "Graphs and Graph Representations"
icon: "article"
date: "2024-08-24T23:42:24+07:00"
lastmod: "2024-08-24T23:42:24+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="📘" context="success" %}}
Chapter 12 focuses on advanced <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> representations and setups. It lays the groundwork for representing complex networks in Go using generic maps and slices to achieve optimal <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> performance.
{{% /alert %}}

## 12.1. <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr> Representations

**Definition:** A <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> can be represented as an <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">adjacency list</abbr> (a slice of slices), an <abbr title="A 2D array representing a graph, where rows and columns correspond to vertices.">adjacency matrix</abbr> (a 2D slice), or an <abbr title="A connection between two vertices in a graph.">edge</abbr> list. The <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">adjacency list</abbr> is the most common and idiomatic representation in Go.

### Operations & Complexity

| Operation | Adj List | Adj Matrix | <abbr title="A connection between two vertices in a graph.">Edge</abbr> List |
|---------|----------|------------|-----------|
| Space | <code>O(V+E)</code> | <code>O(V²)</code> | <code>O(E)</code> |
| Add <abbr title="A connection between two vertices in a graph.">edge</abbr> | <code>O(1)</code> | <code>O(1)</code> | <code>O(1)</code> |
| Check <abbr title="A connection between two vertices in a graph.">edge</abbr> | <code>O(degree)</code> | <code>O(1)</code> | <code>O(E)</code> |
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
| Sparse graphs (Adj List) | Very dense graphs (Adj Matrix) |
| Fast <abbr title="A connection between two vertices in a graph.">edge</abbr> checks are required (Adj Matrix) | Memory is strictly constrained |

### Edge Cases & Pitfalls

- **Self-loop:** Handle `u == v` based on your specific requirements.
- **Undirected graphs:** Remember to add the <abbr title="A connection between two vertices in a graph.">edge</abbr> in both directions.
- **<abbr title="A data structure that improves the speed of data retrieval operations.">Index</abbr> out of range:** Always ensure nodes are within valid bounds.

## 12.2. <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr> Traversal

**Definition:** DFS (<abbr title="A graph traversal algorithm that explores as far as possible along each branch before backtracking.">Depth-First Search</abbr>) and BFS (<abbr title="A graph traversal algorithm that explores neighbors level by level.">Breadth-First Search</abbr>) are fundamental <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> traversal algorithms. DFS utilizes a <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> (or <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>), while BFS utilizes a <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| DFS | <code>O(V + E)</code> | Visits all nodes and edges |
| BFS | <code>O(V + E)</code> | Level-order traversal |

### Pseudocode

```text
DFS(g, start):
    seen = array of false
    stack = [start]
    while stack not empty:
        v = pop stack
        if seen[v]:
            continue
        seen[v] = true
        visit(v)
        for each neighbor n of v:
            if not seen[n]:
                push n to stack

BFS(g, start):
    seen = array of false
    queue = [start]
    seen[start] = true
    while queue not empty:
        v = dequeue
        visit(v)
        for each neighbor n of v:
            if not seen[n]:
                seen[n] = true
                enqueue n
```

### Idiomatic Go Implementation

```go
package main

import (
    "container/list"
    "fmt"
)

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
        if seen[v] {
            continue
        }
        seen[v] = true
        visit(v)
        for _, n := range g.adj[v] {
            if !seen[n] {
                stk = append(stk, n)
            }
        }
    }
}

func (g *Graph) BFS(start int, visit func(int)) {
    seen := make([]bool, len(g.adj))
    q := list.New()
    q.PushBack(start)
    seen[start] = true

    for q.Len() > 0 {
        v := q.Remove(q.Front()).(int)
        visit(v)
        for _, n := range g.adj[v] {
            if !seen[n] {
                seen[n] = true
                q.PushBack(n)
            }
        }
    }
}

func main() {
    g := &Graph{adj: [][]int{{1}, {0, 2}, {1}}}
    g.DFS(0, func(v int) { fmt.Print(v, " ") })
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Need shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> in an <abbr title="A graph where edges have no associated weight.">unweighted graph</abbr> (BFS) | Need weighted paths (use Dijkstra) |
| <abbr title="A linear ordering of vertices such that for every directed edge uv, u comes before v.">Topological sort</abbr> (DFS) | Simple <abbr title="A path that starts and ends at the same vertex.">cycle</abbr> detection (use <abbr title="An algorithm to perform union and find operations on disjoint sets.">Union-Find</abbr>) |

### Edge Cases & Pitfalls

- **Disconnected <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>:** Loop through all nodes to ensure full coverage.
- **Revisit:** Always use a `seen` map/slice to avoid infinite loops.
- **<abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> limit:** Use iterative DFS for extremely large or deep graphs.

## 12.3. Shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">Path</abbr> & MST

**Definition:** Dijkstra finds the shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> from a source to all nodes. Kruskal and Prim algorithms find the <abbr title="A spanning tree with the minimum possible total edge weight.">Minimum Spanning Tree</abbr> (MST).

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Dijkstra | <code>O((V+E) log V)</code> | With a <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr> |
| Kruskal | <code>O(E log E)</code> | Sort edges + DSU |
| Prim | <code>O(E log V)</code> | With a <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr> |

### Pseudocode

```text
Dijkstra(g, src):
    dist = array of infinity
    dist[src] = 0
    pq = min-heap containing (src, 0)
    while pq not empty:
        (v, d) = pop min from pq
        if d > dist[v]:
            continue
        for each (neighbor, weight) in adj[v]:
            nd = d + weight
            if nd < dist[neighbor]:
                dist[neighbor] = nd
                push (neighbor, nd) to pq
    return dist
```

### Idiomatic Go Implementation

```go
package main

import (
    "container/heap"
    "fmt"
    "math"
)

type WGraph struct {
    adj [][][2]int // [node, weight]
}

type State struct {
    v    int
    dist int
}

type MinHeap []State

func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i].dist < h[j].dist }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x any)        { *h = append(*h, x.(State)) }
func (h *MinHeap) Pop() any {
    old := *h
    n := len(old)
    *h = old[:n-1]
    return old[n-1]
}

func (g *WGraph) Dijkstra(src int) []int {
    dist := make([]int, len(g.adj))
    for i := range dist {
        dist[i] = math.MaxInt32
    }
    dist[src] = 0
    h := &MinHeap{{src, 0}}
    heap.Init(h)
    for h.Len() > 0 {
        s := heap.Pop(h).(State)
        if s.dist > dist[s.v] {
            continue
        }
        for _, e := range g.adj[s.v] {
            if nd := s.dist + e[1]; nd < dist[e[0]] {
                dist[e[0]] = nd
                heap.Push(h, State{e[0], nd})
            }
        }
    }
    return dist
}

func main() {
    g := &WGraph{adj: [][][2]int{{{1, 4}, {2, 1}}, {{3, 1}}, {{1, 2}, {3, 5}}, {}}}
    fmt.Println(g.Dijkstra(0))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Need shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> in a <abbr title="A graph where each edge is assigned a weight or cost.">weighted graph</abbr> (Dijkstra) | Negative weights exist (use Bellman-Ford) |
| Sparse <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> MST (Kruskal) | Dense <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> MST (Prim is better) |

### Edge Cases & Pitfalls

- **Negative weights:** Dijkstra will fail; use Bellman-Ford.
- **Disconnected nodes:** Distance remains `MaxInt32`.
- **Integer overflow:** Always check before adding weights to prevent overflow.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Adj List | `[][]int` | <code>O(V+E)</code> | <code>O(V+E)</code> | Sparse <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> |
| Adj Matrix | `[][]bool` | <code>O(1)</code> access | <code>O(V^2)</code> | Dense <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> |
| <abbr title="A connection between two vertices in a graph.">Edge</abbr> List | `[]Edge` | <code>O(E)</code> | <code>O(E)</code> | Kruskal's MST |
| Weighted | `[][][2]int` | <code>O(V+E)</code> | <code>O(V+E)</code> | Dijkstra |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 12:</strong> This chapter covers <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> representations (<abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">adjacency list</abbr>, matrix, <abbr title="A connection between two vertices in a graph.">edge</abbr> list), traversal algorithms (DFS and BFS), and shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> with Dijkstra. Use adjacency lists for sparse graphs, DFS for topological <abbr title="The process of arranging elements in a specific order.">sorting</abbr>, BFS for shortest paths in unweighted graphs, and Dijkstra for weighted shortest paths.
{{% /alert %}}