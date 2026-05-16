---
weight: 100300
title: "Chapter 52: A* Search"
description: "A* Search"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A* is the closest thing to a silver bullet in pathfinding.</em>" : Steve Rabin</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 52 covers A* search. Pathfinding combines Dijkstra's completeness with heuristic guidance. Algorithm ensures optimal navigation.
{{% /alert %}}

## 52.1. From Dijkstra to A*

**Definition:** A* search extends Dijkstra. Nodes are prioritized by:

`f(n) = g(n) + h(n)`

Where:
- `g(n)`: Cost from start to n.
- `h(n)`: Heuristic estimate from n to goal.

**Background:** A* directs search intuition. Dijkstra explores broadly. Greedy Best-First uses only intuition. A* marries cost and estimation. Admissible heuristics guarantee optimal paths.

**Use Cases:** Video game pathfinding. GPS navigation. Robotic motion planning.

**Memory Mechanics:** A* uses Priority Queue and tracking maps. Go maps use non-contiguous memory. Large grids cause cache misses in maps. Performance requires flattening 2D grids to 1D slices. Contiguous memory lookups improve throughput.

| Algorithm | Priority | Guarantees |
|-----------|----------|------------|
| Dijkstra | g(n) | Optimal, explores broadly |
| Greedy Best-First | h(n) | Fast, not optimal |
| A* | g(n) + h(n) | Optimal if h is admissible |

## 52.2. The Heuristic

Admissible heuristics never overestimate cost.

| Domain | Heuristic | Admissible? |
|--------|-----------|-------------|
| Grid (4-way) | <abbr title="Distance measured along axes at right angles">Manhattan distance</abbr> | Yes |
| Grid (8-way) | Chebyshev distance | Yes |
| Euclidean space | <abbr title="The straight-line distance between two points">Euclidean distance</abbr> | Yes |
| Road networks | Precomputed landmarks | Approximate |

### Idiomatic Go: A* Core

```go
package main

import (
	"container/heap"
	"fmt"
	"math"
)

type Node struct {
	x, y int
	g, f float64
}

type PriorityQueue []*Node

func (pq PriorityQueue) Len() int            { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool  { return pq[i].f < pq[j].f }
func (pq PriorityQueue) Swap(i, j int)       { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x any) { *pq = append(*pq, x.(*Node)) }
func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	*pq = old[:n-1]
	return item
}

// heuristic returns Manhattan distance between two points.
func heuristic(a, b [2]int) float64 {
	return math.Abs(float64(a[0]-b[0])) + math.Abs(float64(a[1]-b[1]))
}

// neighbors returns passable adjacent cells (4-directional) within bounds.
func neighbors(pos [2]int, grid [][]int) [][2]int {
	dirs := [][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	var result [][2]int
	for _, d := range dirs {
		nx, ny := pos[0]+d[0], pos[1]+d[1]
		if ny >= 0 && ny < len(grid) && nx >= 0 && nx < len(grid[0]) && grid[ny][nx] == 1 {
			result = append(result, [2]int{nx, ny})
		}
	}
	return result
}

// reconstructPath builds the path from start to goal using cameFrom.
func reconstructPath(cameFrom map[[2]int][2]int, current [2]int) [][2]int {
	var path [][2]int
	for {
		path = append([][2]int{current}, path...)
		prev, ok := cameFrom[current]
		if !ok {
			break
		}
		current = prev
	}
	return path
}

// aStar finds the shortest path on a grid from start to goal.
// grid[y][x] == 1 means passable, 0 means blocked.
// Returns the path (nil if none) and the total cost.
func aStar(grid [][]int, start, goal [2]int) ([][2]int, float64) {
	open := &PriorityQueue{}
	heap.Init(open)
	heap.Push(open, &Node{x: start[0], y: start[1], g: 0, f: heuristic(start, goal)})

	cameFrom := make(map[[2]int][2]int)
	gScore := map[[2]int]float64{start: 0}
	fScore := map[[2]int]float64{start: heuristic(start, goal)}

	for open.Len() > 0 {
		current := heap.Pop(open).(*Node)
		pos := [2]int{current.x, current.y}

		if pos == goal {
			return reconstructPath(cameFrom, pos), gScore[pos]
		}

		for _, nb := range neighbors(pos, grid) {
			tentativeG := gScore[pos] + 1.0 // uniform cost per step

			if g, exists := gScore[nb]; !exists || tentativeG < g {
				cameFrom[nb] = pos
				gScore[nb] = tentativeG
				f := tentativeG + heuristic(nb, goal)
				fScore[nb] = f
				heap.Push(open, &Node{x: nb[0], y: nb[1], g: tentativeG, f: f})
			}
		}
	}
	// No path found
	return nil, math.Inf(1)
}

func main() {
	// 5x5 grid: 1 = passable, 0 = blocked (an obstacle in the middle column)
	grid := [][]int{
		{1, 1, 1, 1, 1},
		{1, 1, 0, 1, 1},
		{1, 1, 0, 1, 1},
		{1, 1, 1, 1, 1},
		{1, 1, 1, 1, 1},
	}
	start, goal := [2]int{0, 0}, [2]int{4, 4}
	path, cost := aStar(grid, start, goal)
	if path == nil {
		fmt.Println("No path found.")
		return
	}
	fmt.Printf("Shortest path cost: %.0f\n", cost)
	fmt.Printf("Path: %v\n", path)
}
```

## 52.3. Properties

| Condition | Guarantee |
|-----------|-----------|
| h admissible | A* finds optimal path |
| h consistent | No node re-expansion needed |
| h = 0 | A* becomes Dijkstra |
| h perfect | A* goes directly to goal |

## 52.4. Decision Matrix

| Use A* When... | Use Dijkstra When... |
|----------------|---------------------|
| Goal is rigorously known | Single-source all destinations |
| Good heuristic exists | No heuristic exists or graph is uniform |
| Pathfinding occurs in grids or maps | General network routing |

### Edge Cases & Pitfalls

- **Inadmissible heuristic:** Overestimation leads to suboptimal paths.
- **Tie-breaking:** f-score ties degrade to BFS. Secondary ordering logic prevents degradation.
- **Memory:** A* stores all nodes. IDA* handles large graphs.
- **Dynamic obstacles:** Shifting environments require replanning. Use D* Lite.

### Anti-Patterns

- **Inadmissible heuristic:** Guarantees fail. Shortest paths are missed.
- **A* for all-destinations:** Heuristic overhead is wasted. Dijkstra is more efficient.
- **Unsorted open list:** Min-heap is required. Performance negates heuristic gains without priority queue.
- **Ignoring ties:** High expansion occurs. Secondary keys reduce node processing.

## 52.5. Quick Reference

| Heuristic | Formula | Best For |
|-----------|---------|----------|
| Manhattan | <code>\|x₁-x₂\| + \|y₁-y₂\|</code> | 4-way grids |
| Euclidean | <code>√((x₁-x₂)² + (y₁-y₂)²)</code> | Free movement |
| Diagonal | <code>max(\|Δx\|, \|Δy\|)</code> | 8-way grids |

| Go stdlib | Usage |
|-----------|-------|
| `container/heap` | Priority queue for managing the open set |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 52:</strong> A* provides informed pathfinding. Heuristics guide Dijkstra's logic. Heuristic quality determines search speed.
{{% /alert %}}

## See Also

- [Chapter 14: Single-Source Shortest Paths](/docs/part-iv/chapter-14/)
- [Chapter 50: Topological Sort](/docs/part-x/chapter-50/)
- [Chapter 51: Strongly Connected Components](/docs/part-x/chapter-51/)
