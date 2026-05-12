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
Chapter 53 covers A* (A-Star) search: the dominant pathfinding algorithm combining Dijkstra's completeness with <abbr title="A technique that employs practical methods to find solutions that are sufficient for the immediate goals.">heuristic</abbr> guidance for optimal and efficient navigation.
{{% /alert %}}

## 53.1. From Dijkstra to A*

**Definition:** <abbr title="A best-first search algorithm that finds the shortest path from a start node to a goal node using a heuristic function.">A* search</abbr> extends Dijkstra by prioritizing nodes based on:

`f(n) = g(n) + h(n)`

Where:
- `g(n)`: Cost from start to n (Dijkstra's priority)
- `h(n)`: Heuristic estimate from n to goal (guidance)

**Background & Philosophy:**
The philosophy is directed intuition. Dijkstra explores blindly in all directions (like a water spill), and Greedy Best-First searches purely on intuition (often hitting dead ends). A* perfectly marries the two. By formally evaluating `f(n) = g(n) + h(n)` (actual cost + guessed cost), A* proves mathematically that as long as the guess never overestimates reality, it will find the perfect path with minimal exploration.

**Use Cases:**
AI pathfinding in video games, GPS navigation systems planning physical routes, and robotic motion planning.

**Memory Mechanics:**
A* relies on a Priority Queue (a <abbr title="A heap where each parent is less than or equal to its children">Min-Heap</abbr>) and tracking maps (`cameFrom`, `gScore`). In Go, `map[[2]int]float64` is used to map 2D grid coordinates to values. Maps in Go hash keys and scatter data <abbr title="Memory blocks allocated in fragmented, separate locations.">non-contiguous</abbr>ly across the heap. For a large grid (like a 10,000x10,000 grid), millions of map accesses cause severe <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>. High-performance A* implementations abandon maps, instead flattening the 2D grid into a 1D slice where `index = y*width + x`, enabling <code>O(1)</code> contiguous memory lookups and high CPU throughput.

| Algorithm | Priority | Guarantees |
|-----------|----------|------------|
| Dijkstra | g(n) | Optimal, explores broadly |
| Greedy Best-First | h(n) | Fast, not optimal |
| A* | g(n) + h(n) | Optimal if h is admissible |

## 53.2. The Heuristic

An <abbr title="A heuristic that never overestimates the true cost to reach the goal.">admissible heuristic</abbr> never overestimates the true cost. Common choices:

| Domain | Heuristic | Admissible? |
|--------|-----------|-------------|
| Grid (4-way) | <abbr title="Distance measured along axes at right angles">Manhattan distance</abbr> | Yes |
| Grid (8-way) | Chebyshev distance | Yes |
| Euclidean space | <abbr title="The straight-line distance between two points">Euclidean distance</abbr> | Yes |
| Road networks | Precomputed landmarks | Approximate |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr>: A* Core

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
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Node)) }
func (pq *PriorityQueue) Pop() interface{} {
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

## 53.3. Properties

| Condition | Guarantee |
|-----------|-----------|
| h admissible | A* finds optimal path |
| h consistent | No node re-expansion needed |
| h = 0 | A* becomes Dijkstra |
| h perfect | A* goes directly to goal |

## 53.4. Decision Matrix

| Use A* When... | Use Dijkstra When... |
|----------------|---------------------|
| Goal is rigorously known | Single-source all destinations |
| Good heuristic exists | No heuristic exists or graph is uniform |
| Pathfinding occurs in grids or maps | General network routing |

### Edge Cases & Pitfalls

- **<abbr title=\"A heuristic that overestimates the true cost and may lead to suboptimal solutions.\">Inadmissible heuristic</abbr>:** May easily find suboptimal paths.
- **Tie-breaking:** f-score ties degrade heavily to BFS without secondary ordering logic.
- **Memory:** A* keeps all nodes in memory. For large graphs, deploy IDA* (Iterative Deepening A*).
- **Dynamic obstacles:** Requires full replanning (deploy D* Lite for shifting environments).

## 53.5. Quick Reference

| Heuristic | Formula | Best For |
|-----------|---------|----------|
| Manhattan | <code>\|x₁-x₂\| + \|y₁-y₂\|</code> | 4-way grids |
| Euclidean | <code>√((x₁-x₂)² + (y₁-y₂)²)</code> | Free movement |
| Diagonal | <code>max(\|Δx\|, \|Δy\|)</code> | 8-way grids |

| Go stdlib | Usage |
|-----------|-------|
| `container/heap` | Priority queue for managing the open set |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 51:</strong> A* is the gold standard for informed pathfinding, combining the optimality of Dijkstra with the efficiency of <abbr title="A technique that employs practical methods to find solutions that are sufficient for the immediate goals.">heuristic</abbr> guidance. The quality of the heuristic entirely determines its performance: a perfect heuristic makes A* instant, while a zero heuristic collapses it to Dijkstra. In game development, robotics, and mapping, A* dominates because it powerfully respects both mathematical correctness and physical speed.
{{% /alert %}}

## See Also

- [Chapter 14: Single-Source Shortest Paths](/docs/Part-IV/Chapter-14/)
- [Chapter 50: Topological Sort](/docs/Part-X/Chapter-50/)
- [Chapter 51: Strongly Connected Components](/docs/Part-X/Chapter-51/)
