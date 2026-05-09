---
weight: 120300
title: "Chapter 60 - Convex Hull"
description: "Convex Hull"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The convex hull is to computational geometry what sorting is to algorithms.</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 60 covers the convex hull — the smallest convex shape containing a set of points, and Graham's and Andrew's algorithms for computing it.
{{% /alert %}}

## 60.1. What Is a Convex Hull?

**Definition:** The <abbr title="The smallest convex set that contains a given set of points, analogous to stretching a rubber band around the points.">convex hull</abbr> of a set of points is the smallest convex polygon containing them all. Imagine stretching a rubber band around nails on a board.

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

func cross(o, a, b Point) int {
    return (a.x-o.x)*(b.y-o.y) - (a.y-o.y)*(b.x-o.x)
}
```

## 60.3. Algorithm Comparison

| Algorithm | Time | Space | Simplicity |
|-----------|------|-------|------------|
| Graham scan | O(n log n) | O(n) | Moderate |
| Andrew's monotone chain | O(n log n) | O(n) | Simple |
| Jarvis march | O(nh) | O(1) | Simple (h = hull points) |
| QuickHull | O(n log n) avg | O(n) | Moderate |

## 60.4. Geometric Primitives

| Primitive | Formula | Meaning |
|-----------|---------|---------|
| Cross product | (a-o) × (b-o) | Orientation of o→a→b |
| Cross > 0 | | Counter-clockwise turn |
| Cross < 0 | | Clockwise turn |
| Cross = 0 | | Collinear |

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
- **Integer overflow:** Use 64-bit integers for cross products.

## 60.6. Quick Reference

| Concept | Value |
|---------|-------|
| Lower bound | Ω(n log n) (reduction from sorting) |
| Output size | h points (h ≤ n) |
| Orientation | Cross product sign |

| Go stdlib | Usage |
|-----------|-------|
| `sort` | Point sorting |
| `image` | Point representations |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 60:</strong> The convex hull is computational geometry's gateway problem. Andrew's monotone chain algorithm achieves optimal O(n log n) time with elegant simplicity — sort, then sweep. The cross product, testing whether three points make a left or right turn, is the fundamental primitive. From collision detection to geographic information systems, the convex hull reduces complex point sets to their essential boundary.
{{% /alert %}}
