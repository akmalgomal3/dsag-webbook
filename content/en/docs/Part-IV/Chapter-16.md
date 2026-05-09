---
weight: 4400
title: "Chapter 16 - Minimum Spanning Trees"
description: "Minimum Spanning Trees"
icon: "article"
date: "2024-08-24T23:42:30+07:00"
lastmod: "2024-08-24T23:42:30+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The most damaging phrase in the language is: 'We've always done it this way.'</em>" — Grace Hopper</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 16 focuses on Minimum Spanning Trees (MST) utilizing Kruskal's, Prim's, and Borůvka's algorithms. It applies Generic Go <abbr title="An algorithm to perform union and find operations on disjoint sets.">Union-Find</abbr> sets and priority queues to efficiently map optimal network topologies.
{{% /alert %}}

## 16.1. Kruskal’s Algorithm

**Definition:** Kruskal builds an MST by greedily selecting the smallest edges, utilizing a <abbr title="An algorithm to perform union and find operations on disjoint sets.">Union-Find</abbr> data structure to detect and avoid cycles.

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

{{< prism lang="go" line-numbers="true">}}
package main

import (
	"fmt"
	"sort"
)

type <abbr title="A connection between two vertices in a graph.">Edge</abbr> struct{ u, v, w int }
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
	edges := []Edge...
	fmt.Println(kruskal(4, edges))
}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Edge list is readily available | Adjacency list format is required |
| E is relatively small (sparse) | Need online MST (edges arriving continuously) |

### Edge Cases & Pitfalls

- **Disconnected graph:** An MST only covers the largest component; check if ....
- **Union-Find without path compression:** This can degenerate to ... per operation, wrecking performance.

## 16.2. Prim’s Algorithm

**Definition:** Prim expands the MST from a single starting vertex, consistently choosing the smallest edge that connects to an unvisited vertex outside the current MST.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Extract-Min | ... | Binary heap |
| Total | ... | Ideal for dense graphs |

### Pseudocode


### Idiomatic Go Implementation

package main

import (
	"container/heap"
	"fmt"
)

type PE struct{ v, w, from int }
type PQ []PE
func (q PQ) Len() int { return len(q) }
func (q PQ) Less(i, j int) bool { return q[i].w < q[j].w }
func (q PQ) Swap(i, j int) { q[i], q[j] = q[j], q[i] }
func (q *PQ) Push(x interface{}) { *q = append(*q, x.(PE)) }
func (q *PQ) Pop() interface{} { old := *q; n := len(old); *q = old[:n-1]; return old[n-1] }

func prim(n int, adj [][]PE) []PE {
	inMST := make([]bool, n)
	pq := &PQ{}
	heap.Init(pq)
	heap.Push(pq, PE{v: 0, w: 0, from: -1})
	mst := []PE{}
	for len(mst) < n && pq.Len() > 0 {
		e := <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>.Pop(pq).(PE)
		if inMST[e.v] { continue }
		inMST[e.v] = true
		if e.from != -1 { mst = append(mst, e) }
		for _, ne := range adj[e.v] {
			if !inMST[ne.v] { <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>.Push(pq, PE{v: ne.v, w: ne.w, from: e.v}) }
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
{{< /prism >}}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Dense graphs | <abbr title="A connection between two vertices in a graph.">Edge</abbr> list is easier to process (Kruskal) |
| <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">Adjacency list</abbr> is readily available | Global <abbr title="A connection between two vertices in a graph.">edge</abbr> <abbr title="The process of arranging elements in a specific order.">sorting</abbr> is necessary |

## 16.3. Borůvka’s Algorithm

**Definition:** Borůvka runs in parallel to find the smallest <abbr title="A connection between two vertices in a graph.">edge</abbr> for every component and merges them, making it highly suitable for distributed computing.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Per phase | <code>O(E log V)</code> | Merging components |
| Total | <code>O(E log V)</code> | log V phases |

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

{{< prism lang="go" line-numbers="true">}}
package main

import "fmt"

type Ed struct{ u, v, w int }
type Uf struct{ p, r []int }
func NewUf(n int) *Uf { p := make([]int, n); for i := range p { p[i] = i }; return &Uf{p, make([]int, n)} }
func (u *Uf) f(x int) int { if u.p[x] != x { u.p[x] = u.f(u.p[x]) }; return u.p[x] }
func (u *Uf) uni(a, b int) bool { ra, rb := u.f(a), u.f(b); if ra == rb { return false }; if u.r[ra] < u.r[rb] { ra, rb = rb, ra }; u.p[rb] = ra; if u.r[ra] == u.r[rb] { u.r[ra]++ }; return true }

func boruvka(n int, edges []Ed) []Ed {
	uf := NewUf(n); mst := []Ed{}
	for len(mst) < n-1 {
		best := make([]*Ed, n)
		for i := range edges {
			e := &edges[i]; ru, rv := uf.f(e.u), uf.f(e.v)
			if ru == rv { continue }
			if best[ru] == nil || e.w < best[ru].w { best[ru] = e }
			if best[rv] == nil || e.w < best[rv].w { best[rv] = e }
		}
		for _, e := range best { if e != nil && uf.uni(e.u, e.v) { mst = append(mst, *e) } }
	}
	return mst
}

func main() {
	edges := []Ed...
	fmt.Println(boruvka(4, edges))
}
{{< /prism >}}

### Decision Matrix

| Use This When... | Avoid If... |
|-------------------|------------------|
| Parallel processing environment | A simpler implementation suffices (Kruskal) |
| Distributed systems | Single-threaded environments |

## 16.4. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Kruskal | ... + Union-Find | ... | ... | Edge list, sparse graph |
| Prim | ... | ... | ... | Dense graph, adjacency list |
| Borůvka | Union-Find | ... | ... | Parallel, distributed |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 16:</strong> This chapter covers Kruskal's, Prim's, and Borůvka's algorithms for <abbr title="A spanning tree with the minimum possible total edge weight.">Minimum Spanning Tree</abbr>. Use Kruskal when you have an <abbr title="A connection between two vertices in a graph.">edge</abbr> list, Prim for dense graphs with adjacency lists, and Borůvka for parallel or distributed computation scenarios.
{{% /alert %}}