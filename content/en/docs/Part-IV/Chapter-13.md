---
weight: 40100
title: "Chapter 13 - Graph Traversal Algorithms"
description: "Graph Traversal Algorithms"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The journey of a thousand miles begins with one step.</em>" — Lao Tzu</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 13 covers graph traversal algorithms: Depth-First Search (DFS) and Breadth-First Search (BFS). Learn how to systematically explore graphs and their applications.
{{% /alert %}}

## 13.1. Depth-First Search (DFS)

**Definition:** DFS explores as far as possible along each branch before backtracking. It uses a stack (explicit or recursive call stack).

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Time | <code>O(V + E)</code> | Visit every vertex and edge |
| Space | <code>O(V)</code> | Recursion stack or explicit stack |
| Path finding | Yes | Any path, not necessarily shortest |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func dfs(g [][]int, start int) []int {
	visited := make([]bool, len(g))
	var order []int
	var explore func(v int)
	explore = func(v int) {
		visited[v] = true
		order = append(order, v)
		for _, u := range g[v] {
			if !visited[u] {
				explore(u)
			}
		}
	}
	explore(start)
	return order
}

func main() {
	g := [][]int{{1, 2}, {0, 3}, {0}, {1}}
	fmt.Println(dfs(g, 0)) // [0 1 3 2]
}
```

## 13.2. Breadth-First Search (BFS)

**Definition:** BFS explores all vertices at the present depth before moving to vertices at the next depth level. It uses a queue and finds shortest paths in unweighted graphs.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Time | <code>O(V + E)</code> | Visit every vertex and edge |
| Space | <code>O(V)</code> | Queue storage |
| Shortest path | Yes | In unweighted graphs |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func bfs(g [][]int, start int) []int {
	visited := make([]bool, len(g))
	queue := []int{start}
	visited[start] = true
	var order []int
	for len(queue) > 0 {
		v := queue[0]
		queue = queue[1:]
		order = append(order, v)
		for _, u := range g[v] {
			if !visited[u] {
				visited[u] = true
				queue = append(queue, u)
			}
		}
	}
	return order
}

func main() {
	g := [][]int{{1, 2}, {0, 3}, {0}, {1}}
	fmt.Println(bfs(g, 0)) // [0 1 2 3]
}
```

## 13.3. Decision Matrix

| Use DFS When... | Use BFS When... |
|-----------------|-----------------|
| Need to detect cycles | Shortest path in unweighted graph |
| Topological sorting | Level-order traversal |
| Finding connected components | Finding shortest path |
| Backtracking problems | Web crawling breadth-first |

### Edge Cases & Pitfalls

- **Stack overflow:** Deep recursion in DFS can overflow; use iterative DFS for deep graphs.
- **Disconnected graphs:** Run DFS/BFS from every unvisited vertex.
- **Visited tracking:** Always mark visited when enqueueing in BFS, not when dequeuing.

## 13.4. Quick Reference

| Algorithm | Go Type | Time | Space | Path | Use Case |
|-----------|---------|------|-------|------|----------|
| DFS | Recursion/Stack | <code>O(V+E)</code> | <code>O(V)</code> | Any | Cycle detection, backtracking |
| BFS | Queue | <code>O(V+E)</code> | <code>O(V)</code> | Shortest | Unweighted shortest path |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 13:</strong> DFS and BFS are fundamental graph traversal techniques. DFS excels at exploration and cycle detection using recursion or an explicit stack. BFS guarantees shortest paths in unweighted graphs using a queue. In Go, use slices as stacks and queues for efficient traversal.
{{% /alert %}}

## See Also

- [Chapter 12 — Graphs and Graph Representations](/docs/Part-III/Chapter-12/)
- [Chapter 14 — Single-Source Shortest Paths](/docs/Part-IV/Chapter-14/)
- [Chapter 15 — All-Pairs Shortest Paths](/docs/Part-IV/Chapter-15/)

