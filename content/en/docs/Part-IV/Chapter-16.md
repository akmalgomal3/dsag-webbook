---
weight: 40400
title: "Chapter 16: Minimum Spanning Trees"
description: "Minimum Spanning Trees"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The most damaging phrase in the language is: 'We've always done it this way.'</em>" — Grace Hopper</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 16: Minimum Spanning Trees (MST). Covers Kruskal's, Prim's, and Borůvka's algorithms. Compares usage and implementations.
{{% /alert %}}

## 16.1. Kruskal’s Algorithm

**Definition:** Builds MST by selecting minimum weight edges. Uses <abbr title="An algorithm to perform union and find operations on disjoint sets.">Union-Find</abbr> to prevent cycles.

**Logic:**
Global greed. Evaluates all edges simultaneously. Selects absolute cheapest edge. Merges forest fragments into global <abbr title="A spanning tree with the minimum possible total edge weight.">Minimum Spanning Tree</abbr>.

**Use Cases:**
Physical infrastructure layout. Long-distance fiber optic networks.

**Memory Mechanics:**
Relies on edge list `[]Edge`. Global sort operates on <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> memory. Leverages <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr>. Union-Find uses flat `[]int` slices. Avoids dynamic <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocation. High memory efficiency.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Sort edges | <code>O(E log E)</code> | `sort.Slice` |
| <abbr title="An algorithm to perform union and find operations on disjoint sets.">Union-Find</abbr> | <code>O(E α(V))</code> | Inverse Ackermann |
| Total | <code>O(E log E)</code> | Dominated by <abbr title="The process of arranging elements in a specific order.">sorting</abbr> |

### Pseudocode

```text
Kruskal(n, edges):
    sort edges by weight ascending
    uf = UnionFind(n)
    mst = empty list
    for each edge (u, v, w) in edges:
        if uf.union(u, v):
            mst.append(edge)
            if len(mst) == n-1: break
    return mst
```

### Idiomatic Go Implementation

```go
package main

import (
	"fmt"
	"sort"
)

type Edge struct{ u, v, w int }
type UF struct{ p, r []int }

func newUF(n int) *UF {
	p, r := make([]int, n), make([]int, n)
	for i := range p { p[i] = i }
	return &UF{p, r}
}

func (u *UF) find(x int) int {
	if u.p[x] != x { u.p[x] = u.find(u.p[x]) }
	return u.p[x]
}

func (u *UF) union(a, b int) bool {
	ra, rb := u.find(a), u.find(b)
	if ra == rb { return false }
	if u.r[ra] < u.r[rb] { ra, rb = rb, ra }
	u.p[rb] = ra
	if u.r[ra] == u.r[rb] { u.r[ra]++ }
	return true
}

func kruskal(n int, edges []Edge) []Edge {
	sort.Slice(edges, func(i, j int) bool { return edges[i].w < edges[j].w })
	uf := newUF(n)
	mst := []Edge{}
	for _, e := range edges {
		if uf.union(e.u, e.v) { mst = append(mst, e) }
	}
	return mst
}

func main() {
	edges := []Edge{{0, 1, 10}, {0, 2, 6}, {0, 3, 5}, {1, 3, 15}, {2, 3, 4}}
	fmt.Println(kruskal(4, edges))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Edge list format exists | Adjacency list format is required |
| Sparse graph | Online MST processing required |

### Edge Cases & Pitfalls

- **Disconnected graph:** MST covers largest component only. Run BFS/DFS reachability check first.
- **Missing path compression:** Union-Find degrades to <code>O(log V)</code>. Kills performance.

## 16.2. Prim’s Algorithm

**Definition:** Expands MST from single start vertex. Selects minimum connecting edge to unvisited vertex.

**Logic:**
Local greed. Grows continuously outward. Takes cheapest adjacent step.

**Use Cases:**
Dense network design. Printed circuit board (PCB) layouts.

**Memory Mechanics:**
Requires <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">Adjacency List</abbr> and Min-Heap. Heap acts as exploration frontier. Dense graphs cause rapid heap growth and <abbr title="Memory blocks allocated in fragmented, separate locations.">non-contiguous</abbr> allocations. Avoids upfront <code>O(E log E)</code> sorting cost.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Extract-Min | <code>O(log V)</code> | Binary heap |
| Total | <code>O((V + E) log V)</code> | Ideal for dense graphs |

### Pseudocode

```text
Prim(g, start):
    mst = empty list
    visited = array of false
    pq = min-heap containing edges from start
    visited[start] = true
    while pq not empty and len(mst) < V-1:
        edge = pop min from pq
        if visited[edge.to]: continue
        visited[edge.to] = true
        mst.append(edge)
        for each neighbor of edge.to:
            if not visited[neighbor]:
                push neighbor edge to pq
    return mst
```

### Idiomatic Go Implementation

```go
package main

import (
	"container/heap"
	"fmt"
)

type PE struct{ v, w, from int }
type PQ []PE

func (q PQ) Len() int           { return len(q) }
func (q PQ) Less(i, j int) bool { return q[i].w < q[j].w }
func (q PQ) Swap(i, j int)      { q[i], q[j] = q[j], q[i] }
func (q *PQ) Push(x any) { *q = append(*q, x.(PE)) }
func (q *PQ) Pop() any {
	old := *q
	n := len(old)
	*q = old[:n-1]
	return old[n-1]
}

func prim(n int, adj [][]PE) []PE {
	inMST := make([]bool, n)
	pq := &PQ{}
	heap.Init(pq)
	heap.Push(pq, PE{v: 0, w: 0, from: -1})
	mst := []PE{}
	for len(mst) < n && pq.Len() > 0 {
		e := heap.Pop(pq).(PE)
		if inMST[e.v] { continue }
		inMST[e.v] = true
		if e.from != -1 { mst = append(mst, e) }
		for _, ne := range adj[e.v] {
			if !inMST[ne.v] { heap.Push(pq, PE{v: ne.v, w: ne.w, from: e.v}) }
		}
	}
	return mst
}

func main() {
	adj := make([][]PE, 4)
	adj[0] = []PE{{1,10,-1},{2,20,-1}}
	adj[1] = []PE{{0,10,-1},{2,30,-1},{3,5,-1}}
	adj[2] = []PE{{0,20,-1},{1,30,-1},{3,15,-1}}
	adj[3] = []PE{{1,5,-1},{2,15,-1}}
	fmt.Println(prim(4, adj))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Dense graphs | Edge list format exists |
| Adjacency list format exists | Global edge sorting is required |

## 16.3. Borůvka’s Algorithm

**Definition:** Finds minimum connecting edge per component in parallel. Merges components iteratively.

**Logic:**
Concurrent component merging. Evaluates all forest trees simultaneously. Scales horizontally.

**Use Cases:**
Distributed systems. Massive MapReduce clusters. RAM-exceeding datasets.

**Memory Mechanics:**
Uses flat `best` array. Halves component count per phase. Runs max `log V` phases. Sequential array access ensures <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. Avoids pointer chasing.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Per phase | <code>O(E log V)</code> | Component merging |
| Total | <code>O(E log V)</code> | Max log V phases |

### Pseudocode

```text
Boruvka(n, edges):
    uf = UnionFind(n)
    mst = empty list
    while len(mst) < n-1:
        best = array of nil
        for each edge (u, v, w):
            ru, rv = uf.find(u), uf.find(v)
            if ru == rv: continue
            if best[ru] nil or w < best[ru].w: best[ru] = edge
            if best[rv] nil or w < best[rv].w: best[rv] = edge
        for each edge in best:
            if edge not nil and uf.union(edge.u, edge.v):
                mst.append(edge)
    return mst
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

type Ed struct{ u, v, w int }
type Uf struct{ p, r []int }

func NewUf(n int) *Uf {
    p := make([]int, n)
    for i := range p { p[i] = i }
    return &Uf{p, make([]int, n)}
}

func (u *Uf) f(x int) int {
    if u.p[x] != x { u.p[x] = u.f(u.p[x]) }
    return u.p[x]
}

func (u *Uf) uni(a, b int) bool {
    ra, rb := u.f(a), u.f(b)
    if ra == rb { return false }
    if u.r[ra] < u.r[rb] { ra, rb = rb, ra }
    u.p[rb] = ra
    if u.r[ra] == u.r[rb] { u.r[ra]++ }
    return true
}

func boruvka(n int, edges []Ed) []Ed {
	uf := NewUf(n)
	mst := []Ed{}
	for len(mst) < n-1 {
		best := make([]*Ed, n)
		for i := range edges {
			e := &edges[i]
			ru, rv := uf.f(e.u), uf.f(e.v)
			if ru == rv { continue }
			if best[ru] == nil || e.w < best[ru].w { best[ru] = e }
			if best[rv] == nil || e.w < best[rv].w { best[rv] = e }
		}
		for _, e := range best {
		    if e != nil && uf.uni(e.u, e.v) {
		        mst = append(mst, *e)
		    }
		}
	}
	return mst
}

func main() {
	edges := []Ed{{0, 1, 10}, {0, 2, 6}, {0, 3, 5}, {1, 3, 15}, {2, 3, 4}}
	fmt.Println(boruvka(4, edges))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Distributed computing environment | Simple implementation works |
| Parallel processing framework | Single-threaded environment |

### Anti-Patterns

- **Skipping path compression:** Degrades Find to <code>O(log V)</code>. Wrecks Kruskal efficiency. Always compress paths.
- **Prim on edge lists:** Requires O(V²) conversion. Kruskal avoids this cost.
- **Unverified graph connectivity:** MST requires single connected component. Verify `len(mst) == V-1`.

## 16.4. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Kruskal | `[]Edge` + Union-Find | <code>O(E log E)</code> | <code>O(V)</code> | Edge list, sparse graph |
| Prim | `[]Edge` + PQ | <code>O((V + E) log V)</code> | <code>O(V)</code> | <abbr title="A graph with edges close to the maximum possible">Dense graph</abbr>, adjacency list |
| Borůvka | Union-Find | <code>O(E log V)</code> | <code>O(V)</code> | Parallel, distributed |


{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 16:</strong> Kruskal uses edge lists. Prim uses adjacency lists for dense graphs. Borůvka supports parallel processing.
{{% /alert %}}

## See Also

- [Chapter 10: Heaps and Priority Queues](/docs/part-iii/chapter-10/)
- [Chapter 17: Network Flow Algorithms](/docs/part-iv/chapter-17/)
- [Chapter 18: Matchings in Bipartite Graphs](/docs/part-iv/chapter-18/)