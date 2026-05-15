---
weight: 120300
title: "Chapter 59: Convex Hull"
description: "Convex Hull"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The convex hull is to <abbr title="Algorithms for solving geometric problems">computational geometry</abbr> what sorting is to algorithms.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 60 covers the convex hull: the smallest convex shape containing a set of points, mapping Graham's and Andrew's algorithms for computing it.
{{% /alert %}}

## 60.1. What Is a Convex Hull?

**Definition:** The <abbr title="The smallest convex set that contains a given set of points, analogous to stretching a rubber band around the points.">convex hull</abbr> of a set of points is the smallest convex <abbr title="A plane figure bounded by straight line segments">polygon</abbr> containing them all. Imagine stretching a rubber band around nails on a board.

**Background & Philosophy:**
The philosophy is exterior boundary isolation. When given thousands of scattered points, most are interior noise. The convex hull acts as a mathematical boundary, isolating the subset of points that define the geometric perimeter.

**Use Cases:**
3D collision detection in video games (generating bounding boxes), pattern recognition in computer vision, and mapping physical territory borders in geographic information systems (GIS).

**Memory Mechanics:**
Andrew's Monotone Chain initially performs an <code>O(n log n)</code> sort on the points array. Because the array (`[]Point`) is completely <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr>, the sort leverages high <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality. After sorting, the algorithm builds the hull using a simple `[]Point` slice as a <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr>. Pushing and popping points from the end of this slice executes entirely in <code>O(1)</code> memory access without generating new <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocations. Andrew's Monotone Chain is fast on modern CPUs, operating at memory bus speed.

### Why It Matters

| Application | Use |
|-------------|-----|
| Collision detection | Bounding volume |
| Geographic systems | Territory boundaries |
| Image processing | Shape analysis |
| Machine learning | Cluster boundaries |

## 60.2. Andrew's Monotone Chain

Sort points by x-coordinate, then build lower and upper hulls.

```go
package main

import (
	"fmt"
	"sort"
)

type Point struct{ x, y int }

func convexHull(points []Point) []Point {
    n := len(points)
    if n <= 1 {
        return points
    }
    
    sort.Slice(points, func(i, j int) bool {
        if points[i].x == points[j].x {
            return points[i].y < points[j].y
        }
        return points[i].x < points[j].x
    })
    
    build := func(hull []Point, points []Point) []Point {
        for _, p := range points {
            for len(hull) >= 2 && cross(hull[len(hull)-2], hull[len(hull)-1], p) <= 0 {
                hull = hull[:len(hull)-1]
            }
            hull = append(hull, p)
        }
        return hull
    }
    
    lower := build([]Point{}, points)
    upper := build([]Point{}, reverse(points))
    
    return append(lower[:len(lower)-1], upper[:len(upper)-1]...)
}

func reverse(points []Point) []Point {
    reversed := make([]Point, len(points))
    for i := range points {
        reversed[i] = points[len(points)-1-i]
    }
    return reversed
}

func cross(o, a, b Point) int {
    return (a.x-o.x)*(b.y-o.y) - (a.y-o.y)*(b.x-o.x)
}

func main() {
    points := []Point{{0, 3}, {1, 1}, {2, 2}, {4, 4}, {0, 0}, {1, 2}, {3, 1}, {3, 3}}
    fmt.Println(convexHull(points))
}
```

## 60.3. Algorithm Comparison

| Algorithm | Time | Space | Simplicity |
|-----------|------|-------|------------|
| Graham scan | <code>O(n log n)</code> | <code>O(n)</code> | Moderate |
| Andrew's monotone chain | <code>O(n log n)</code> | <code>O(n)</code> | Simple |
| Jarvis march | <code>O(nh)</code> | <code>O(1)</code> | Simple (h = hull points) |
| QuickHull | <code>O(n log n)</code> avg | <code>O(n)</code> | Moderate |

## 60.4. Geometric Primitives

| Primitive | Formula | Meaning |
|-----------|---------|---------|
| Cross product | (a-o) × (b-o) | Orientation of o→a→b |
| Cross > 0 | . | Counter-clockwise turn |
| Cross < 0 | . | Clockwise turn |
| Cross = 0 | . | Collinear |

## 60.5. Decision Matrix

| Use Andrew's When... | Use Jarvis When... |
|---------------------|-------------------|
| General case | h is very small (h << n) |
| Simplicity preferred | No sorting overhead allowed |
| Collinear points on hull | Only extreme points needed |

### Edge Cases & Pitfalls

- **Collinear points:** Decide whether to include intermediate points on edges.
- **Duplicate points:** Remove or handle gracefully.
- **All points collinear:** Hull is a line segment.
- **Integer overflow:** Use 64-bit integers for <abbr title="An operation on two vectors that produces a third vector perpendicular to both, used to determine turn orientation.">cross products</abbr>.

### Anti-Patterns

- **Not removing duplicate points before computing:** Duplicate points produce zero-length cross products and can silently corrupt collinear detection — always deduplicate first.
- **Using floating-point cross products:** Integer cross products are exact; floating-point arithmetic introduces rounding errors that flip orientation signs and produce wrong hulls.
- **Forgetting to handle degenerate input:** All-collinear points or fewer than three distinct points produce degenerate hulls (line segments or single points); algorithms must handle these edge cases without crashing.
- **Assuming hull alone solves distance queries:** The convex hull gives the boundary, but finding the farthest pair of hull points requires rotating calipers, not a second hull computation.

## 60.6. Quick Reference

| Concept | Value |
|---------|-------|
| Lower bound | <code>Ω(n log n)</code> (reduction from sorting) |
| Output size | h points (h ≤ n) |
| Orientation | Cross product sign |

| Go stdlib | Usage |
|-----------|-------|
| `sort` | Point sorting |
| `image` | Point representations |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 59:</strong> The convex hull is <abbr title="Algorithms for solving geometric problems">computational geometry</abbr>'s gateway problem. Andrew's monotone chain algorithm achieves optimal <code>O(n log n)</code> time — sort, then sweep. The <abbr title="An operation on two vectors that produces a third vector perpendicular to both, used to determine turn orientation.">cross product</abbr>, testing whether three points make a left or right turn, is the fundamental primitive. From collision detection to geographic information systems, the convex hull reduces complex point sets to their essential boundary.
{{% /alert %}}

## See Also

- [Chapter 32: Linear Programming](/docs/part-vii/chapter-32/)
- [Chapter 52: A* Search](/docs/part-x/chapter-52/)
- [Chapter 58: Mo's Algorithm](/docs/part-xii/chapter-58/)
