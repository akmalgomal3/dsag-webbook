---
weight: 70800
title: "Chapter 35: Approximate Algorithms"
description: "Approximate Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the soul of computing, and approximate algorithms are the art of making the impossible possible.</em>" — David Williamson</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 35 covers approximation algorithms: greedy heuristics, local search, and randomized rounding for NP-hard problems.
{{% /alert %}}

## 35.1. Greedy Approximation

**Definition:** Greedy algorithms select local optimal choice at every step. NP-hard problems receive bounded <abbr title="A guarantee of how close an approximation is to the optimal solution.">approximation ratio</abbr>.

**Background:**
NP-Hard problems take excessive time for exact solutions. Approximate algorithms trade perfection for speed. Results stay within guaranteed bounds: cost never exceeds 2x optimal.

**Use Cases:**
Google Maps routing. Set Cover for shipping optimization. Microchip circuitry layout.

**Memory Mechanics:**
Algorithms use greedy sorting or MST. Edge weight sorting takes <code>O(E log E)</code>. <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">Contiguous</abbr> slices improve <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> locality. Randomization flips bits in memory. Entropy generators require shared memory locks.

### Operations & Complexity

| Problem | Approx Ratio | Time | Description |
|---------|-------------|------|------------|
| Set Cover | H(n) ≈ ln n | <code>O(n log n)</code> | Picks maximum coverage iteratively |
| <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover | 2 | <code>O(V + E)</code> | Picks both endpoints of uncovered <abbr title="A connection between two vertices in a graph.">edge</abbr> |
| Knapsack (fractional) | 1 (Exact) | <code>O(n log n)</code> | Optimal for fractional variables |
| TSP (metric) | 2 (MST-based) | <code>O(V²)</code> | Uses double-tree technique |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

```go
package main

import (
    "fmt"
    "sort"
)

// Fractional Knapsack - mathematically optimal greedy approach
type Item struct {
    Weight int
    Value  int
}

func fractionalKnapsack(items []Item, capacity int) float64 {
    sort.Slice(items, func(i, j int) bool {
        vi, vj := float64(items[i].Value)/float64(items[i].Weight),
            float64(items[j].Value)/float64(items[j].Weight)
        return vi > vj
    })
    totalValue := 0.0
    remaining := capacity
    for _, item := range items {
        if remaining <= 0 {
            break
        }
        if item.Weight <= remaining {
            totalValue += float64(item.Value)
            remaining -= item.Weight
        } else {
            totalValue += float64(item.Value) * float64(remaining) / float64(item.Weight)
            remaining = 0
        }
    }
    return totalValue
}

func main() {
    items := []Item{{10, 60}, {20, 100}, {30, 120}}
    fmt.Println("Max value:", fractionalKnapsack(items, 50))
}
```

{{% alert icon="📌" context="warning" %}}
Fractional knapsack is optimal using value/weight ratio. 0/1 Knapsack requires DP or <abbr title="Fully Polynomial Time Approximation Scheme - finds near-optimal solutions in polynomial time.">FPTAS</abbr>.
{{% /alert %}}

## 35.2. <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover 2-Approximation

**Definition:** Vertex cover touches every <abbr title="A connection between two vertices in a graph.">edge</abbr>. Greedy 2-approximation selects both endpoints of uncovered edges.

### Operations & Complexity

| Algorithm | Approx Ratio | Time | Space |
|-----------|-------------|------|-------|
| Greedy (both endpoints) | 2 | <code>O(V + E)</code> | <code>O(V)</code> |
| LP Rounding | 2 | <code>O(poly)</code> | <code>O(V + E)</code> |
| Best known mathematical | 2 - o(1) | . | PTAS does not exist |

### Idiomatic Go Implementation

```go
package main

import "fmt"

type Graph struct {
    V     int
    Edges [][2]int
}

func vertexCoverApprox(g Graph) map[int]bool {
    covered := make(map[int]bool)
    used := make([]bool, len(g.Edges))
    for {
        found := false
        for i, e := range g.Edges {
            if used[i] {
                continue
            }
            u, v := e[0], e[1]
            if !covered[u] && !covered[v] {
                covered[u] = true
                covered[v] = true
                used[i] = true
                found = true
                break
            }
        }
        if !found {
            break
        }
    }
    return covered
}

func main() {
    g := Graph{V: 4, Edges: [][2]int{{0, 1}, {1, 2}, {2, 3}, {3, 0}}}
    cover := vertexCoverApprox(g)
    fmt.Println("Vertex Cover:", cover)
}
```

### Decision Matrix

| Scenario | Best Algorithm | Approx Ratio | Notes |
|----------|---------------|-------------|-------|
| Small vertex cover | ILP exact | 1 (exact) | V < 30 |
| Large vertex cover | Greedy both-endpoints | 2 | Simple and fast |
| Sparse graphs | Greedy vertex cover | 2 | O(V+E) |
| Metric TSP (fast) | Nearest Neighbor | O(log n) | No constant guarantee |
| Metric TSP (provable) | Christofides | 1.5 | MST + min-weight matching |
| Max-Cut (simple) | Random partition | E/2 expected | Run k times |
| Fractional Knapsack | Greedy by ratio | 1 (exact) | Optimal |
| 0/1 Knapsack | DP or FPTAS | 1 (exact) or (1−ε) | Use FPTAS for large n |

### Edge Cases & Pitfalls

- **Fractional vs 0/1:** Greedy works for fractional only. 0/1 knapsack yields bad results with greedy.
- **Triangle inequality:** Christofides requires metric TSP. Violating triangle inequality breaks guarantees.
- **Random amplification:** Single run gives expected E/2. Run k times to reduce failure probability.
- **Vertex cover tie-breaking:** Results depend on edge order. Quality remains constant at 2x.
- **TSP nearest neighbor trap:** Tours reach O(log n) times optimal. Start city choice changes output.

## 35.3. Metric TSP Heuristic (Nearest Neighbor)

**Definition:** Metric TSP follows triangle inequality. Nearest Neighbor visits closest unvisited city. Not a constant-factor approximation. Max error is O(log n). MST double-tree provides provable 2-approximation.

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math"
)

func nearestNeighborTSP(dist [][]float64) []int {
    n := len(dist)
    visited := make([]bool, n)
    tour := make([]int, 0, n)
    current := 0
    visited[current] = true
    tour = append(tour, current)
    for len(tour) < n {
        next := -1
        minDist := math.MaxFloat64
        for i := 0; i < n; i++ {
            if !visited[i] && dist[current][i] < minDist {
                minDist = dist[current][i]
                next = i
            }
        }
        if next == -1 {
            break
        }
        visited[next] = true
        tour = append(tour, next)
        current = next
    }
    return tour
}

func tourLength(tour []int, dist [][]float64) float64 {
    total := 0.0
    for i := 0; i < len(tour); i++ {
        j := (i + 1) % len(tour)
        total += dist[tour[i]][tour[j]]
    }
    return total
}

func main() {
    dist := [][]float64{
        {0, 10, 15, 20},
        {10, 0, 35, 25},
        {15, 35, 0, 30},
        {20, 25, 30, 0},
    }
    tour := nearestNeighborTSP(dist)
    fmt.Println("Tour:", tour)
    fmt.Println("Length:", tourLength(tour, dist))
}
```

## 35.4. Randomized Approximation

**Definition:** Randomized algorithms use random choices. Achieve expected approximation ratios.

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math/rand"
)

func maxCutRandom(edges [][2]int, n int) (map[int]bool, int) {
    setA := make(map[int]bool)
    for i := 0; i < n; i++ {
        if rand.Float64() < 0.5 {
            setA[i] = true
        }
    }
    cutSize := 0
    for _, e := range edges {
        _, inA := setA[e[0]]
        _, inB := setA[e[1]]
        if inA != inB {
            cutSize++
        }
    }
    return setA, cutSize
}

func main() {
    edges := [][2]int{{0, 1}, {1, 2}, {2, 3}, {3, 0}, {0, 2}}
    set, size := maxCutRandom(edges, 4)
    fmt.Println("Set A:", set)
    fmt.Println("Cut size:", size)
}
```

{{% alert icon="📌" context="warning" %}}
Randomized Max-Cut produces expected cut size ≥ |E|/2. Run <code>k</code> times to reduce failure probability.
{{% /alert %}}

### Anti-Patterns

- **Greedy for 0/1 Knapsack:** Strategy fails. Use DP or FPTAS.
- **TSP Nearest Neighbor guarantee:** No constant guarantee exists. Use Christofides for 1.5-approx.
- **Single Max-Cut run:** High variance occurs. Perform k trials.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover | `map[int]bool` | <code>O(V+E)</code> | <code>O(V)</code> | Greedy 2-approx |
| Set Cover | <abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority queue</abbr> | <code>O(n log n)</code> | varies | Greedy ln n-approx |
| TSP Metric | `[]int` tour | <code>O(n^2)</code> | <code>O(n)</code> | 2-approx MST double-tree |
| TSP Metric | `[]int` tour | <code>O(n^3)</code> | <code>O(n)</code> | 1.5-approx Christofides |
| Max-Cut | `map[int]bool` | <code>O(E)</code> | <code>O(V)</code> | Random partition |
| Knapsack Frac | `[]Item` | <code>O(n log n)</code> | <code>O(n)</code> | Greedy optimal |
| Knapsack 0/1 | `[][]int` matrix | <code>O(nW)</code> | <code>O(nW)</code> | DP-based approach |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 35:</strong> Chapter covers approximation algorithms for NP-hard problems. Greedy fractional knapsack is optimal. Vertex cover has 2-approximation. Metric TSP uses Nearest Neighbor or Christofides. Randomized Max-Cut provides expected ratios. Use greedy for speed, randomization for expected bounds, and Christofides for 1.5 guarantee.
{{% /alert %}}

## See Also

- [Chapter 24: Greedy Algorithms](/docs/part-vi/chapter-24/)
- [Chapter 27: Probabilistic and Randomized Algorithms](/docs/part-vi/chapter-27/)
- [Chapter 42: Modern Algorithmic Thinking](/docs/part-viii/chapter-42/)
