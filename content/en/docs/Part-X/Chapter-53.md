---
weight: 100300
title: "Chapter 53: A* Search"
description: "A* Search"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A* is the closest thing to a silver bullet in pathfinding.</em>" : Steve Rabin</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 53 covers A* (A-Star) search: the dominant pathfinding algorithm combining Dijkstra's completeness with heuristic guidance for optimal and efficient navigation.
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
A* aggressively relies upon a Priority Queue (a Min-Heap) and tracking maps (`cameFrom`, `gScore`). In Go, `map[[2]int]float64` is heavily utilized to map 2D grid coordinates to values. Maps in Go hash keys and scatter data <abbr title="Memory blocks allocated in fragmented, separate locations.">non-contiguous</abbr>ly across the heap. For a sprawling map (like a 10,000x10,000 grid), millions of map accesses cause severe <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>. High-performance A* implementations abandon maps, instead flattening the 2D grid into a massive 1D slice where `index = y*width + x`, enabling `O(1)` contiguous memory lookups and restoring blazing CPU speeds.

| Algorithm | Priority | Guarantees |
|-----------|----------|------------|
| Dijkstra | g(n) | Optimal, explores broadly |
| Greedy Best-First | h(n) | Fast, not optimal |
| A* | g(n) + h(n) | Optimal if h is admissible |

## 53.2. The Heuristic

An <abbr title="A heuristic that never overestimates the true cost to reach the goal.">admissible heuristic</abbr> never overestimates the true cost. Common choices:

| Domain | Heuristic | Admissible? |
|--------|-----------|-------------|
| Grid (4-way) | Manhattan distance | Yes |
| Grid (8-way) | Chebyshev distance | Yes |
| Euclidean space | Euclidean distance | Yes |
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
    g    float64 // cost from start
    f    float64 // g + h
}

// Minimal placeholder priority queue for illustration
type PriorityQueue []*Node
func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].f < pq[j].f }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Node)) }
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	*pq = old[0 : n-1]
	return item
}

func heuristic(a, b [2]int) float64 {
	// Manhattan distance
	return math.Abs(float64(a[0]-b[0])) + math.Abs(float64(a[1]-b[1]))
}

// Pseudo-implementation to demonstrate structure
func aStar(start, goal [2]int) {
    open := &PriorityQueue{}
    heap.Push(open, &Node{x: start[0], y: start[1], g: 0, f: heuristic(start, goal)})
    
    // cameFrom := map[[2]int][2]int{}
    // gScore := map[[2]int]float64{start: 0}
    
    for open.Len() > 0 {
        current := heap.Pop(open).(*Node)
        if current.x == goal[0] && current.y == goal[1] {
            fmt.Println("Path found!")
            return
        }
        
        // Loop neighbors, compute tentativeG, push to heap
    }
}

func main() {
    aStar([2]int{0, 0}, [2]int{2, 2})
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

- **Inadmissible heuristic:** May easily find suboptimal paths.
- **Tie-breaking:** f-score ties degrade heavily to BFS without secondary ordering logic.
- **Memory:** A* aggressively keeps all nodes in memory. For huge graphs, strictly deploy IDA* (Iterative Deepening A*).
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
<strong>Summary Chapter 53:</strong> A* is the gold standard for informed pathfinding, combining the optimality of Dijkstra with the efficiency of heuristic guidance. The quality of the heuristic entirely determines its performance: a perfect heuristic makes A* instant, while a zero heuristic collapses it to Dijkstra. In game development, robotics, and mapping, A* dominates because it powerfully respects both mathematical correctness and physical speed.
{{% /alert %}}

## See Also

- [Chapter 14: Single-Source Shortest Paths](/docs/Part-IV/Chapter-14/)
- [Chapter 51: Topological Sort](/docs/Part-X/Chapter-51/)
- [Chapter 52: Strongly Connected Components](/docs/Part-X/Chapter-52/)
