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
<strong>"<em>Algorithms are the soul of computing, and approximate algorithms are the art of making the impossible possible.</em>" : David Williamson</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 36 explores approximation algorithms: greedy heuristics, local search, and randomized rounding tailored specifically for solving NP-hard problems.
{{% /alert %}}

## 36.1. Greedy Approximation

**Definition:** Greedy algorithms continuously select the locally optimal choice at every isolated step. For a variety of <abbr title="A class of problems at least as hard as NP-Complete problems.">NP-hard</abbr> problems, a greedy approach yields a mathematically provable, bounded <abbr title="A guarantee of how close an approximation is to the optimal solution.">approximation ratio</abbr>.

**Background & Philosophy:**
The philosophy embraces pragmatic imperfection. When a problem is <abbr title="A class of problems at least as hard as NP-Complete problems.">NP-Hard</abbr> (like calculating the flawless shortest route for 1,000 delivery trucks), finding the perfect mathematical answer might take a supercomputer millions of years. Approximate algorithms proudly trade absolute perfection for guaranteed speed, securing answers that are "good enough" (e.g., guaranteed to be no worse than 2x the optimal cost).

**Use Cases:**
Heuristic routing in Google Maps, grouping millions of distinct products into the fewest possible shipping boxes (Set Cover), and optimizing layouts for microchip circuitry.

**Memory Mechanics:**
Because approximate algorithms often fall back on greedy sorting or minimum spanning trees (MST), their memory footprint heavily depends on the underlying graph structures. A common greedy approximation requires sorting edge weights <code>O(E log E)</code>, relying entirely on <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> slices that process quickly in <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr>. Randomization (like Max-Cut) simply iterates through memory flipping bits randomly, which operates efficiently but places heavy demands on the entropy generator's shared memory lock if not isolated per thread.

### Operations & Complexity

| Problem | Approx Ratio | Time | Description |
|---------|-------------|------|------------|
| Set Cover | H(n) ≈ ln n | <code>O(n log n)</code> | Greedy iteratively picks the maximum coverage |
| <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover | 2 | <code>O(V + E)</code> | Pick both endpoints of an uncovered <abbr title="A connection between two vertices in a graph.">edge</abbr> |
| Knapsack (fractional) | 1 (Exact) | <code>O(n log n)</code> | Strictly optimal for fractional variables |
| TSP (metric) | 2 (MST-based) | <code>O(V²)</code> | Employs the double-tree technique |

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
Fractional knapsack is optimal because it can act greedily based on the <abbr title="The data associated with a key in a key-value pair.">value</abbr>/weight ratio. The 0/1 Knapsack is not optimal using a greedy approach; you must deploy DP or a Fully <abbr title="An algorithm whose running time is upper bounded by a polynomial expression.">Polynomial Time</abbr> Approximation Scheme (<abbr title="Fully Polynomial Time Approximation Scheme - finds near-optimal solutions in polynomial time.">FPTAS</abbr>).
{{% /alert %}}

## 36.2. <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover 2-Approximation

**Definition:** A <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> cover is a curated set of vertices that seamlessly touches every single <abbr title="A connection between two vertices in a graph.">edge</abbr> within a <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>. A greedy 2-approximation vigorously selects both endpoints of any <abbr title="A connection between two vertices in a graph.">edge</abbr> that currently remains uncovered.

### Operations & Complexity

| Algorithm | Approx Ratio | Time | Space |
|-----------|-------------|------|-------|
| Greedy (both endpoints) | 2 | <code>O(V + E)</code> | <code>O(V)</code> |
| LP Rounding | 2 | <code>O(poly)</code> | <code>O(V + E)</code> |
| Best known mathematical | 2 - o(1) | . | A formal PTAS does not exist yet |

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
| Small vertex cover | ILP exact | 1 (exact) | Only for V < ~30 |
| Large vertex cover | Greedy both-endpoints | 2 | Simple, fast |
| Sparse graphs | Greedy vertex cover | 2 | O(V+E) |
| Metric TSP (fast) | Nearest Neighbor | O(log n) | Fast but no constant guarantee |
| Metric TSP (provable) | Christofides | 1.5 | MST + min-weight matching |
| Max-Cut (simple) | Random partition | E/2 expected | Run k times for amplification |
| Fractional Knapsack | Greedy by ratio | 1 (exact) | Optimal for fractional variant |
| 0/1 Knapsack | DP or FPTAS | 1 (exact) or (1−ε) | Use FPTAS for large n |

### Edge Cases & Pitfalls

- **Fractional vs 0/1:** Greedy is optimal only for fractional knapsack. Applying it to 0/1 knapsack produces arbitrarily bad results.
- **Triangle inequality:** Christofides' 1.5-approximation only works on metric TSP (distances satisfy triangle inequality). If distances violate it, the guarantee evaporates.
- **Random amplification:** One run of randomized Max-Cut gives expected E/2. Run it k times and keep the best cut to drive the failure probability down to 2^{-k}.
- **Vertex cover tie-breaking:** The greedy 2-approximation picks both endpoints of an uncovered edge. The result depends on edge iteration order — different orders produce different covers of the same approximation quality.
- **TSP nearest neighbor trap:** Nearest neighbor can produce tours up to O(log n) times optimal, and its output depends heavily on the starting city.

## 36.3. Metric TSP Heuristic (Nearest Neighbor)

**Definition:** A Metric TSP explicitly fulfills the triangle inequality. The Nearest Neighbor heuristic constructs a tour by repeatedly visiting the closest unvisited city. This is a practical heuristic (not a constant-factor approximation) — in the worst case, nearest neighbor can produce tours up to O(log n) times the optimal. For a provable 2-approximation, use the MST double-tree approach: compute an MST, double its edges, form an Euler tour, and shortcut repeated vertices.

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

## 36.4. Randomized Approximation

**Definition:** Randomized algorithms inject calculated random choices to forge an expected, highly reliable approximation ratio.

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
Randomized Max-Cut reliably produces an expected cut size roughly ≥ |E|/2. Amplification tactic: execute the algorithm <code>k</code> times, selecting the best result to reduce the probability of failure exponentially.
{{% /alert %}}

### Anti-Patterns

- **Applying greedy to 0/1 Knapsack:** The greedy value/weight ratio strategy is optimal only for fractional knapsack. For 0/1 Knapsack, use DP or an FPTAS — greedy produces arbitrarily bad results.
- **Assuming TSP nearest neighbor gives a constant-factor guarantee:** Nearest neighbor can produce results O(log n) times optimal. For a proven 1.5-approximation on metric TSP, use Christofides' algorithm.
- **Running randomized Max-Cut only once:** A single random partition gives expected E/2 but high variance. Run k independent trials and keep the best to reduce failure probability exponentially.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover | `map[int]bool` | <code>O(V+E)</code> | <code>O(V)</code> | Greedy 2-approx |
| Set Cover | <abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority queue</abbr> | <code>O(n log n)</code> | varies | Greedy ln n-approx |
| TSP Metric | `[]int` tour | <code>O(n^2)</code> | <code>O(n)</code> | 2-approx MST double-tree |
| TSP Metric | `[]int` tour | <code>O(n^3)</code> | <code>O(n)</code> | 1.5-approx Christofides |
| Max-Cut | `map[int]bool` | <code>O(E)</code> | <code>O(V)</code> | Random partition |
| Knapsack Frac | `[]Item` | <code>O(n log n)</code> | <code>O(n)</code> | Greedy optimal |
| Knapsack 0/1 | DP | 1 | <code>O(nW)</code> | `[][]int` matrix |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 35:</strong> This chapter discusses approximation algorithms designed for NP-hard problems: greedy fractional knapsack (provably optimal), a 2-approximation for <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> cover, nearest neighbor and Christofides methods for metric TSP, alongside a randomized Max-Cut approach. Leverage greedy techniques for lightning-fast solutions, randomized algorithms for consistent expected ratios, and Christofides for a rigorous 1.5 guarantee on metric TSPs.
{{% /alert %}}

## See Also

- [Chapter 24: Greedy Algorithms](/docs/part-vi/chapter-24/)
- [Chapter 27: Probabilistic and Randomized Algorithms](/docs/part-vi/chapter-27/)
- [Chapter 42: Modern Algorithmic Thinking](/docs/part-viii/chapter-42/)
