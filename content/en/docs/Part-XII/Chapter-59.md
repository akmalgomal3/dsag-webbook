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
The convex hull is the fundamental operation of <abbr title="Algorithms for solving geometric problems">computational geometry</abbr>. It is analogous to sorting.
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
The <abbr title="The smallest convex set that contains a given set of points, analogous to stretching a rubber band around the points.">convex hull</abbr> is the smallest convex shape containing all points. Andrew's Monotone Chain is the standard algorithm.
{{% /alert %}}

## 59.1. What Is a Convex Hull?

**Definition:** The hull is the smallest convex <abbr title="A plane figure bounded by straight line segments">polygon</abbr> containing all points. It resembles a rubber band stretched around nails.

**Mechanics:**
Exterior boundary isolation defines the hull. Most points are interior noise. The hull isolates perimeter points.

**Use Cases:**
3D collision detection, pattern recognition, and territory mapping.

**Memory Mechanics:**
Andrew's Monotone Chain sorts points in `O(n log n)`. <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">Contiguous</abbr> arrays leverage <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality. A `[]Point` slice acts as a <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr>. Operations execute in `O(1)` memory access. Heap allocations are minimal.

### Applications

| Field | Usage |
|-------------|-----|
| Collision detection | Bounding volume |
| Geographic systems | Territory boundaries |
| Image processing | Shape analysis |
| Machine learning | Cluster boundaries |

## 59.2. Andrew's Monotone Chain

Sort points by x-coordinate. Build lower and upper hulls separately.

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

## 59.3. Algorithm Comparison

| Algorithm | Time | Space | Simplicity |
|-----------|------|-------|------------|
| Graham scan | <code>O(n log n)</code> | <code>O(n)</code> | Moderate |
| Andrew's monotone chain | <code>O(n log n)</code> | <code>O(n)</code> | Simple |
| Jarvis march | <code>O(nh)</code> | <code>O(1)</code> | Simple |
| QuickHull | <code>O(n log n)</code> avg | <code>O(n)</code> | Moderate |

## 59.4. Geometric Primitives

| Primitive | Meaning |
|-----------|---------|
| Cross product | Orientation of o→a→b |
| Cross > 0 | Counter-clockwise turn |
| Cross < 0 | Clockwise turn |
| Cross = 0 | Collinear |

## 59.5. Decision Matrix

| Use Andrew's When... | Use Jarvis When... |
|---------------------|-------------------|
| General cases | Hull points h << n |
| Simplicity is priority | Sorting overhead is restricted |
| Collinear points exist | Only extreme points required |

### Edge Cases & Pitfalls

- **Collinear points:** Decide inclusion of intermediate points.
- **Duplicate points:** Deduplicate before processing.
- **Collinear sets:** Result is a line segment.
- **Integer overflow:** Use 64-bit integers for <abbr title="An operation on two vectors that produces a third vector perpendicular to both, used to determine turn orientation.">cross products</abbr>.

### Anti-Patterns

- **Duplicate input:** Duplicate points corrupt collinear detection. Deduplicate first.
- **Floating-point logic:** Rounding errors flip orientation signs. Use integer cross products.
- **Ignoring degenerates:** Collinear points or N < 3 produce line segments. Algorithms must handle these.
- **Overextending output:** Hull provides boundaries only. Distance queries require rotating calipers.

## 59.6. Quick Reference

| Concept | Value |
|---------|-------|
| Lower bound | <code>Ω(n log n)</code> |
| Output size | h points |
| Orientation | Cross product sign |

| Go stdlib | Usage |
|-----------|-------|
| `sort` | Point sorting |
| `image` | Point representations |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
**Summary Chapter 59:** The convex hull is the gateway to <abbr title="Algorithms for solving geometric problems">computational geometry</abbr>. Andrew's monotone chain achieves <code>O(n log n)</code> time. The <abbr title="An operation on two vectors that produces a third vector perpendicular to both, used to determine turn orientation.">cross product</abbr> is the fundamental primitive.
{{% /alert %}}

## See Also

- [Chapter 32: Linear Programming](/docs/part-vii/chapter-32/)
- [Chapter 52: A* Search](/docs/part-x/chapter-52/)
- [Chapter 58: Mo's Algorithm](/docs/part-xii/chapter-58/)
