---
weight: 40100
title: "Chapter 13: Graph Traversal Algorithms"
description: "Graph Traversal Algorithms"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The journey of a thousand miles begins with one step.</em>" : Lao Tzu</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 13 covers graph traversal algorithms: Depth-First Search (DFS) and Breadth-First Search (BFS). Learn how to systematically explore graphs and their applications.
{{% /alert %}}

## 13.1. Depth-First Search (DFS)

**Definition:** DFS explores as far as possible along each branch before backtracking. It uses a <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> (explicit or recursive <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>).

**Background & Philosophy:**
The philosophy of DFS is "aggressive exploration". It dives into the unknown, chasing a single <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> until it hits a dead end. This strategy naturally maps to how human problem-solving often works: follow an idea to its conclusion before trying an alternative.

**Use Cases:**
Essential for detecting cycles in a dependency <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> (like finding deadlocks in database transactions), generating mazes, solving Sudoku puzzles via backtracking, and computing <abbr title="A linear ordering of vertices such that for every directed edge uv, u comes before v.">topological sorts</abbr> for build systems.

**Memory Mechanics:**
DFS is intrinsically linked to <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> memory. When written recursively, each visited node pushes a new frame onto the CPU's <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>. If the <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> is an incredibly long chain of nodes (e.g., 1 million nodes), this deep recursion can trigger a <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>, crashing the program. To avoid this, Go engineers often write iterative DFS using an explicit slice `[]int` acting as a <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr>. This shifts the memory burden from the limited execution stack to the vast <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Time | <code>O(V + E)</code> | Visit every vertex and edge |
| Space | <code>O(V)</code> | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> or explicit <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> |
| Path finding | Yes | Any <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr>, not necessarily shortest |

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

**Definition:** BFS explores all vertices at the present depth before moving to vertices at the next depth level. It uses a <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr> and finds shortest paths in unweighted graphs.

**Background & Philosophy:**
The philosophy of BFS is "cautious expansion". It radiates outward concentrically, completely mapping its immediate surroundings before venturing further. Because it expands uniformly step-by-step, it provides a mathematical guarantee: the first time BFS discovers a node, it has found the shortest possible <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> to that node in an unweighted <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>.

**Use Cases:**
Used fundamentally in routing algorithms (e.g., fewest hops between routers), social network analysis ("degrees of separation"), and web crawling.

**Memory Mechanics:**
Unlike DFS, BFS cannot be easily implemented recursively. It relies on a <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr>, which in Go is best implemented using a dynamically resizing slice (<abbr title="Fixed-size buffer that wraps around using modulo">ring buffer</abbr>). As BFS expands, the queue holds the "frontier" of exploration. In a highly dense graph, this frontier can grow massively wide, consuming substantial <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> memory. The `visited` map or slice ensures that memory isn't wasted queueing nodes multiple times, maintaining <code>O(V)</code> <abbr title="A computational complexity that describes the amount of memory space taken by an algorithm.">space complexity</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Time | <code>O(V + E)</code> | Visit every vertex and edge |
| Space | <code>O(V)</code> | <abbr title="A FIFO (First In, First Out) abstract data type.">Queue</abbr> storage |
| Shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> | Yes | In unweighted graphs |

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
| Need to detect cycles | Shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> in unweighted <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> |
| <abbr title="A linear ordering of vertices such that for every directed edge uv, u comes before v.">Topological sorting</abbr> | Level-order traversal |
| Finding connected components | Finding shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> |
| Backtracking problems | Web crawling breadth-first |

### Edge Cases & Pitfalls

- **<abbr title="An error caused by using more stack memory than allocated.">Stack overflow</abbr>:** Deep <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> in DFS can overflow; use iterative DFS for deep graphs.
- **Disconnected graphs:** Run DFS/BFS from every unvisited vertex.
- **Visited tracking:** Always mark visited when enqueueing in BFS, not when dequeuing.

## 13.4. Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Algorithm | Go Type | Time | Space | Path | Use Case |
|-----------|---------|------|-------|------|----------|
| DFS | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr>/<abbr title="A LIFO (Last In, First Out) abstract data type.">Stack</abbr> | <code>O(V+E)</code> | <code>O(V)</code> | Any | <abbr title="A path that starts and ends at the same vertex.">Cycle</abbr> detection, backtracking |
| BFS | <abbr title="A FIFO (First In, First Out) abstract data type.">Queue</abbr> | <code>O(V+E)</code> | <code>O(V)</code> | Shortest | Unweighted shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 13:</strong> DFS and BFS are fundamental <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> traversal techniques. DFS excels at exploration and <abbr title="A path that starts and ends at the same vertex.">cycle</abbr> detection using <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> or an explicit <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr>. BFS guarantees shortest paths in unweighted graphs using a <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr>. In Go, use slices as stacks and queues for efficient traversal.
{{% /alert %}}

## See Also

- [Chapter 12: Graphs and Graph Representations](/docs/Part-III/Chapter-12/)
- [Chapter 14: Single-Source Shortest Paths](/docs/Part-IV/Chapter-14/)
- [Chapter 15: All-Pairs Shortest Paths](/docs/Part-IV/Chapter-15/)
