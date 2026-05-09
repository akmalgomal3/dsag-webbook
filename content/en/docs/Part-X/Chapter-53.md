---
weight: 10200
title: "Chapter 53 - A* Search"
description: "A* Search"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A* is the closest thing to a silver bullet in pathfinding.</em>" — Steve Rabin</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 53 covers A* (A-Star) search — the dominant pathfinding algorithm combining Dijkstra's completeness with heuristic guidance for optimal and efficient navigation.
{{% /alert %}

## 53.1. From Dijkstra to A*

**Definition:** <abbr title="A best-first search algorithm that finds the shortest path from a start node to a goal node using a heuristic function.">A* search</abbr> extends Dijkstra by prioritizing nodes based on:

f(n) = g(n) + h(n)

Where:
- g(n): Cost from start to n (Dijkstra's priority)
- h(n): Heuristic estimate from n to goal (guidance)

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
type Node struct {
    x, y int
    g    float64 // cost from start
    f    float64 // g + h
}

func aStar(grid [][]int, start, goal [2]int) []Node {
    open := &PriorityQueue{}
    heap.Push(open, &Node{x: start[0], y: start[1], g: 0, 
        f: heuristic(start, goal)})
    
    cameFrom := map[[2]int][2]int{}
    gScore := map[[2]int]float64{start: 0}
    
    for open.Len() > 0 {
        current := heap.Pop(open).(*Node)
        if current.x == goal[0] && current.y == goal[1] {
            return reconstructPath(cameFrom, goal)
        }
        
        for _, neighbor := range neighbors(current, grid) {
            tentativeG := gScore[[2]int{current.x, current.y}] + cost(current, neighbor)
            if prevG, ok := gScore[neighbor]; !ok || tentativeG < prevG {
                cameFrom[neighbor] = [2]int{current.x, current.y}
                gScore[neighbor] = tentativeG
                f := tentativeG + heuristic(neighbor, goal)
                heap.Push(open, &Node{x: neighbor[0], y: neighbor[1], g: tentativeG, f: f})
            }
        }
    }
    return nil // No path found
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
| Goal is known | Single-source all destinations |
| Good heuristic exists | No heuristic or graph is uniform |
| Pathfinding in grids/maps | General network routing |

### Edge Cases & Pitfalls

- **Inadmissible heuristic:** May find suboptimal paths.
- **Tie-breaking:** f-score ties degrade to BFS without secondary ordering.
- **Memory:** A* keeps all nodes in memory — for huge graphs, use IDA*.
- **Dynamic obstacles:** Requires replanning (D* Lite for dynamic environments).

## 53.5. Quick Reference

| Heuristic | Formula | Best For |
|-----------|---------|----------|
| Manhattan | \|x₁-x₂\| + \|y₁-y₂\| | 4-way grids |
| Euclidean | √((x₁-x₂)² + (y₁-y₂)²) | Free movement |
| Diagonal | max(\|Δx\|, \|Δy\|) | 8-way grids |

| Go stdlib | Usage |
|-----------|-------|
| `container/heap` | Priority queue for open set |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 53:</strong> A* is the gold standard for informed pathfinding, combining the optimality of Dijkstra with the efficiency of heuristic guidance. The quality of the heuristic determines its performance — a perfect heuristic makes A* instant, while a zero heuristic reduces it to Dijkstra. In game development, robotics, and mapping, A* dominates because it respects both correctness and speed.
{{% /alert %}}
