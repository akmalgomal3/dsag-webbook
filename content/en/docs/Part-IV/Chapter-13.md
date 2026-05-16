---
weight: 40100
title: "Chapter 13: Graph Traversal Algorithms"
description: "Graph Traversal Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The journey of a thousand miles begins with one step.</em>" : Lao Tzu</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 13 covers graph traversal algorithms: depth-first search (DFS) and breadth-first search (BFS). Uses modern Go patterns (Generics, Iterators).
{{% /alert %}}

## 13.1. Depth-First Search (DFS)

**Definition:** Explores branch deeply before backtracking. Uses stack (explicit or recursive).

**Background & Philosophy:**
Aggressive exploration. Dives into unknown. Chases single path to dead end. Mimics human puzzle-solving.

**Use Cases:**
Detect cycles in dependency graphs (deadlocks). Generate mazes. Solve Sudoku via backtracking. Compute topological sorts.

**Memory Mechanics:**
Relies on stack memory. Recursive DFS pushes frames onto CPU call stack. Deep graphs trigger stack overflow. Iterative DFS shifts memory burden to heap via explicit slice stack.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Time | `O(V + E)` | Visit every vertex and edge |
| Space | `O(V)` | Recursion stack or explicit stack |
| Traversal | `O(1)` overhead | Using `iter.Seq` (Go 1.23+) |

### Idiomatic Go 1.23+ Implementation

Generics and Iterators enable clean traversal.

```go
package main

import (
	"fmt"
	"iter"
)

type Graph[K comparable] struct {
	Adj map[K][]K
}

func (g *Graph[K]) DFS(start K) iter.Seq[K] {
	return func(yield func(K) bool) {
		visited := make(map[K]bool)
		var visit func(K) bool
		visit = func(v K) bool {
			visited[v] = true
			if !yield(v) {
				return false
			}
			for _, neighbor := range g.Adj[v] {
				if !visited[neighbor] {
					if !visit(neighbor) {
						return false
					}
				}
			}
			return true
		}
		visit(start)
	}
}

func main() {
	g := &Graph[int]{
		Adj: map[int][]int{
			0: {1, 2},
			1: {0, 3},
			2: {0},
			3: {1},
		},
	}

	fmt.Print("DFS: ")
	for v := range g.DFS(0) {
		fmt.Print(v, " ")
	}
}
```

## 13.2. Breadth-First Search (BFS)

**Definition:** Explores all vertices at present depth before moving deeper. Uses queue. Finds shortest paths.

**Background & Philosophy:**
Cautious expansion. Radiates concentrically. Maps immediate surroundings. Guarantees shortest path on first discovery in unweighted graphs.

**Use Cases:**
Network routing algorithms. Social network analysis. Web crawling.

**Memory Mechanics:**
Requires queue (ring buffer). Holds exploration frontier. Wide graphs consume substantial heap memory. `visited` map prevents redundant enqueueing. Maintains `O(V)` space complexity.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Time | `O(V + E)` | Visit every vertex and edge |
| Space | `O(V)` | Queue storage |
| Shortest Path | Yes | In unweighted graphs |

### Idiomatic Go 1.23+ Implementation

```go
package main

import (
	"fmt"
	"iter"
)

type Graph[K comparable] struct {
	Adj map[K][]K
}

func (g *Graph[K]) BFS(start K) iter.Seq[K] {
	return func(yield func(K) bool) {
		visited := make(map[K]bool)
		queue := []K{start}
		visited[start] = true

		for len(queue) > 0 {
			v := queue[0]
			queue = queue[1:]

			if !yield(v) {
				return
			}

			for _, neighbor := range g.Adj[v] {
				if !visited[neighbor] {
					visited[neighbor] = true
					queue = append(queue, neighbor)
				}
			}
		}
	}
}

func main() {
	g := &Graph[int]{
		Adj: map[int][]int{
			0: {1, 2},
			1: {0, 3},
			2: {0},
			3: {1},
		},
	}

	fmt.Print("BFS: ")
	for v := range g.BFS(0) {
		fmt.Print(v, " ")
	}
}
```

## 13.3. Decision Matrix

| Use DFS When... | Use BFS When... |
|-----------------|-----------------|
| Need to detect cycles | Shortest path in unweighted graph |
| Topological sorting | Level-order traversal |
| Finding connected components | Finding shortest path |
| Backtracking problems | Web crawling breadth-first |

### Anti-Patterns
- **Marking visited on dequeue:** Duplicates work. Same vertex enters queue multiple times. Mark visited at enqueue time.
- **Recursive DFS on deep graphs:** Go stacks limit ~2 KB. Deep chain panics. Use explicit stack.
- **Naive Slice Queue:** `queue = queue[1:]` fragments memory on large graphs. Use circular buffer.

## 13.4. Quick Reference

| Algorithm | Implementation | Time | Space | Path | Use Case |
|-----------|---------|------|-------|------|----------|
| DFS | Recursion/Stack | `O(V+E)` | `O(V)` | Any | Cycle detection |
| BFS | Queue | `O(V+E)` | `O(V)` | Shortest | Shortest path |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 13:</strong> DFS explores deeply. BFS maps radially. Modern Go leverages Generics and Iterators for clean traversal.
{{% /alert %}}

## See Also
- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/chapter-12/)
- [Chapter 14: Single-Source Shortest Paths](/docs/part-iv/chapter-14/)
