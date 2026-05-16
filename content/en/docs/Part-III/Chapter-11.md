---
weight: 30300
title: "Chapter 11: Disjoint Sets (Union-Find)"
description: "Disjoint Sets (Union-Find) data structure and algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Divide and conquer is good, but knowing how to unite is better.</em>"</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 11 covers the Disjoint Set Union (DSU) data structure, focusing on path compression and union-by-rank optimizations.
{{% /alert %}}

## 11.1. Disjoint Set Union (DSU)

**Definition:** <abbr title="A data structure that tracks a partition of a set into disjoint, non-overlapping subsets.">Disjoint Set Union</abbr> (also called Union-Find) maintains a collection of non-overlapping sets. It supports two primary operations: finding which set an element belongs to and uniting two sets.

**Mechanics:**
DSU represents sets as trees where each node points to its parent. The root of the tree serves as the representative of the set.
- **Find:** Follows parent pointers until it reaches the root.
- **Union:** Connects the root of one tree to the root of another.

To maintain efficiency, two optimizations are used:
1. **Path Compression:** During a `Find` operation, make every node on the path point directly to the root. This flattens the tree.
2. **Union by Rank/Size:** Always attach the smaller tree under the root of the larger tree. This keeps the tree height minimal.

**Use Cases:**
- **Network Connectivity:** Determining if two nodes in a graph are in the same component.
- **Kruskal's Algorithm:** Finding the Minimum Spanning Tree (MST) of a graph.
- **Image Processing:** Connected component labeling.
- **Dynamic Connectivity:** Maintaining connectivity information as edges are added.

**Memory Mechanics:**
DSU is typically implemented using arrays (slices in Go).
- `parent[]`: Stores the parent of each element.
- `rank[]` or `size[]`: Stores the height or number of elements in each tree.
Using arrays ensures <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> memory allocation, which is cache-friendly and minimizes pointer chasing.

### Operations & Complexity

| Operation | Complexity (Naive) | Complexity (Optimized) | Description |
|-----------|--------------------|------------------------|-------------|
| Find | <code>O(n)</code> | <code>O(α(n))</code> | Returns representative of the set |
| Union | <code>O(n)</code> | <code>O(α(n))</code> | Merges two sets into one |

*Note: <code>α(n)</code> is the inverse Ackermann function, which grows extremely slowly (nearly constant <code>O(1)</code> for all practical purposes).*

### Idiomatic Go Implementation

```go
package main

import "fmt"

// DSU represents the Disjoint Set Union data structure.
type DSU struct {
	parent []int
	rank   []int
}

// NewDSU creates a new DSU with n elements.
func NewDSU(n int) *DSU {
	parent := make([]int, n)
	rank := make([]int, n)
	for i := range parent {
		parent[i] = i
	}
	return &DSU{parent: parent, rank: rank}
}

// Find returns the representative (root) of the set containing x.
// It implements path compression.
func (d *DSU) Find(x int) int {
	if d.parent[x] != x {
		d.parent[x] = d.Find(d.parent[x])
	}
	return d.parent[x]
}

// Union merges the sets containing x and y.
// It implements union by rank.
func (d *DSU) Union(x, y int) bool {
	rootX := d.Find(x)
	rootY := d.Find(y)
	if rootX == rootY {
		return false
	}

	// Union by rank
	if d.rank[rootX] < d.rank[rootY] {
		d.parent[rootX] = rootY
	} else if d.rank[rootX] > d.rank[rootY] {
		d.parent[rootY] = rootX
	} else {
		d.parent[rootY] = rootX
		d.rank[rootX]++
	}
	return true
}

func main() {
	dsu := NewDSU(5)
	dsu.Union(0, 2)
	dsu.Union(4, 2)
	dsu.Union(3, 1)

	fmt.Printf("Same set (0, 4): %v\n", dsu.Find(0) == dsu.Find(4)) // true
	fmt.Printf("Same set (0, 1): %v\n", dsu.Find(0) == dsu.Find(1)) // false
}
```

### Decision Matrix

| Use DSU When... | Avoid If... |
|--------------------|------------------|
| Tracking connected components | You need to delete edges (use more complex structures) |
| Kruskal's MST algorithm | Working with dense graphs where Prim's might be faster |
| Cycle detection in undirected graphs | Graph is directed (use DFS-based detection) |

### Edge Cases & Pitfalls
- **Index out of bounds:** Ensure elements are within the `[0, n-1]` range.
- **Unoptimized implementations:** Without path compression or union by rank, DSU can degrade to `O(n)`.
- **Initialization:** Forgetting to set `parent[i] = i` leads to incorrect results.

### Anti-Patterns
- **Recursive Find without Path Compression:** Leads to slow operations and potential stack overflow on large sets.
- **Ignoring Return Values:** `Union` should often return a boolean indicating if a merge actually happened.
- **Manual Parent Access:** Always use `Find` to ensure path compression and correct representative retrieval.

## Quick Reference

| Operation | Function | Complexity | Description |
|-----------|----------|------------|-------------|
| Initialization | `NewDSU(n)` | <code>O(n)</code> | Create n sets |
| Find | `Find(x)` | <code>O(α(n))</code> | Get set root |
| Union | `Union(x, y)` | <code>O(α(n))</code> | Merge two sets |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 11:</strong> Disjoint Set Union (DSU) is an efficient structure for tracking connectivity. Path compression and union-by-rank achieve nearly constant time complexity. It is essential for algorithms like Kruskal's MST.
{{% /alert %}}

## See Also
- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/chapter-12/)
- [Chapter 25: Minimum Spanning Trees (Kruskal & Prim)](/docs/part-vi/chapter-25/)
