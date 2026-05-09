---
weight: 70800
title: "Chapter 36 - Approximate Algorithms"
description: "Approximate Algorithms"
icon: "article"
date: "2024-08-24T23:42:51+07:00"
lastmod: "2024-08-24T23:42:51+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the soul of computing, and approximate algorithms are the art of making the impossible possible.</em>" — David Williamson</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 36 explores approximation algorithms: greedy heuristics, local search, and randomized rounding tailored specifically for solving NP-hard problems.
{{% /alert %}}

## 36.1. Greedy Approximation

**Definition:** Greedy algorithms continuously select the locally optimal choice at every isolated step. For a variety of NP-hard problems, a greedy approach yields a mathematically provable, bounded approximation ratio.

### Operations & Complexity

| Problem | Approx Ratio | Time | Description |
|---------|-------------|------|------------|
| Set Cover | H(n) ≈ ln n | <code>O(n log n)</code> | Greedy iteratively picks the maximum coverage |
| <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover | 2 | <code>O(V + E)</code> | Pick both endpoints of an uncovered <abbr title="A connection between two vertices in a graph.">edge</abbr> |
| Knapsack (fractional) | 1 (Exact) | <code>O(n log n)</code> | Strictly optimal for fractional variables |
| TSP (metric) | 2 (MST-based) | <code>O(V²)</code> | Employs the double-tree technique |

### Pseudocode

```text
FractionalKnapsack(items, capacity):
    sort items by value/weight descending
    totalValue = 0
    remaining = capacity
    for each item in items:
        if remaining <= 0: break
        if item.weight <= remaining:
            totalValue += item.value
            remaining -= item.weight
        else:
            totalValue += item.value * (remaining / item.weight)
            remaining = 0
    return totalValue
```

### Idiomatic Go Implementation

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
Fractional knapsack is flawlessly optimal because it can act greedily based solely upon the <abbr title="The data associated with a key in a key-value pair.">value</abbr>/weight ratio. The strict 0/1 Knapsack is absolutely NOT optimal utilizing a greedy approach; you must deploy DP or a Fully <abbr title="An algorithm whose running time is upper bounded by a polynomial expression.">Polynomial Time</abbr> Approximation Scheme (FPTAS).
{{% /alert %}}

### Decision Matrix

| Use Greedy When... | Avoid If... |
|-----------------------|------------------|
| A blazing-fast solution is absolutely required | A mathematically perfect, optimal guarantee is required |
| The resulting approximation ratio is acceptable | An exact, flawless solution is entirely mandatory |

### Edge Cases & Pitfalls

- **Zero weight items:** An item possessing 0 weight and a positive <abbr title="The data associated with a key in a key-value pair.">value</abbr> fundamentally possesses an infinite <abbr title="The data associated with a key in a key-value pair.">value</abbr> ratio. You must handle this explicitly to prevent division by zero.
- **Empty input:** The function must cleanly return 0 or an empty set.

## 36.2. <abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover 2-Approximation

**Definition:** A <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> cover is a curated set of vertices that seamlessly touches every single <abbr title="A connection between two vertices in a graph.">edge</abbr> within a <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>. A greedy 2-approximation vigorously selects both endpoints of any <abbr title="A connection between two vertices in a graph.">edge</abbr> that currently remains uncovered.

### Operations & Complexity

| Algorithm | Approx Ratio | Time | Space |
|-----------|-------------|------|-------|
| Greedy (both endpoints) | 2 | <code>O(V + E)</code> | <code>O(V)</code> |
| LP Rounding | 2 | <code>O(poly)</code> | <code>O(V + E)</code> |
| Best known mathematical | 2 - o(1) | — | A formal PTAS does not exist yet |

### Pseudocode

```text
VertexCoverApprox(graph):
    cover = empty set
    used = array of edges marked false
    repeat:
        found = false
        for each edge (u, v) not used:
            if u not in cover and v not in cover:
                add u and v to cover
                mark edge as used
                found = true
                break
    until not found
    return cover
```

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

{{% alert icon="📌" context="warning" %}}
<abbr title="A fundamental unit of a graph, also called a node.">Vertex</abbr> Cover is natively NP-hard. The 2-approximation stands as the best known polynomial-time approximation possible (unless the UGC is eventually proven false). Greedily picking the <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> boasting the absolute maximum <abbr title="The number of edges incident to a vertex.">degree</abbr> DOES NOT guarantee a ratio of 2.
{{% /alert %}}

### Decision Matrix

| Use 2-Approx When... | Avoid If... |
|-------------------------|------------------|
| Engaging with massive graphs | Seeking an exact, flawless minimum |
| Mandatory <abbr title="An algorithm whose running time is upper bounded by a polynomial expression.">polynomial time</abbr> is required | Engaging with microscopic graphs (execute <abbr title="A straightforward approach trying all possible solutions.">brute force</abbr> instead) |

### Edge Cases & Pitfalls

- **Disconnected graphs:** Diligently handle every isolated component independently.
- **Self-loops:** A valid <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> cover must inherently incorporate the <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> generating a self-loop.

## 36.3. Metric TSP Approximation

**Definition:** A Metric TSP explicitly fulfills the triangle inequality. An MST-based 2-approximation operates by generating a double <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr>, formulating an Euler tour, and aggressively short-cutting visited nodes.

### Operations & Complexity

| Algorithm | Approx Ratio | Time | Description |
|-----------|-------------|------|------------|
| Nearest Neighbor | <code>O(log n)</code> | <code>O(n^2)</code> | Features zero mathematical guarantees |
| MST Double-tree | 2 | <code>O(n^2)</code> | Heavily relies upon the triangle inequality |
| Christofides | 1.5 | <code>O(n³)</code> | Remains the absolute best known metric TSP approximation |

### Pseudocode

```text
NearestNeighborTSP(distances):
    n = number of cities
    visited = array of false
    tour = [0]
    visited[0] = true
    current = 0
    while length(tour) < n:
        next = argmin distances[current][i] for unvisited i
        visited[next] = true
        append next to tour
        current = next
    return tour
```

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

{{% alert icon="📌" context="warning" %}}
The Nearest Neighbor approach absolutely does NOT guarantee a strict approximation ratio. Christofides (1.5-approx) requires an MST coupled with a minimum weight perfect matching executed upon odd-degree vertices. A full, robust implementation easily spans ~150 lines of Go code.
{{% /alert %}}

### Decision Matrix

| Use NN When... | Avoid If... |
|-------------------|------------------|
| A blazing-fast solution is overwhelmingly required | A guaranteed mathematical ratio bound is required |
| Operating upon a Euclidean/metric TSP | Attempting to solve an asymmetric TSP |

### Edge Cases & Pitfalls

- **Disconnected <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>:** The TSP is mathematically undefined on a disconnected <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr>.
- **Negative distances:** TSPs habitually require strictly non-negative distance metrics to function logically.

## 36.4. Randomized Approximation

**Definition:** Randomized algorithms inject calculated random choices to forge an expected, highly reliable approximation ratio.

### Operations & Complexity

| Problem | Expected Ratio | Time | Description |
|---------|---------------|------|------------|
| Max-Cut | 0.5 | <code>O(V + E)</code> | Executes a random partition |
| Max-SAT | 0.5 | <code>O(m)</code> | Generates a random assignment |
| Set Cover (randomized) | <code>O(log n)</code> | <code>O(n log n)</code> | Employs weighted sampling |

### Pseudocode

```text
MaxCutRandom(edges, n):
    setA = empty set
    for each vertex i from 0 to n-1:
        if random() < 0.5:
            add i to setA
    cutSize = 0
    for each edge (u, v):
        if (u in setA) XOR (v in setA):
            cutSize += 1
    return setA, cutSize
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math/rand"
    "time"
)

func maxCutRandom(edges [][2]int, n int) (map[int]bool, int) {
    rand.Seed(time.Now().UnixNano())
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
Randomized Max-Cut reliably produces an expected cut size roughly ≥ |E|/2. Amplification tactic: execute the algorithm <code>k</code> times, aggressively picking the absolute best result to crush the probability of failure exponentially.
{{% /alert %}}

### Decision Matrix

| Use Randomized When... | Avoid If... |
|---------------------------|------------------|
| A purely deterministic approach is incredibly difficult | A rigorous deterministic guarantee is absolutely mandatory |
| The mathematical expected ratio is sufficient | A <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> ratio is purely mandatory |

### Edge Cases & Pitfalls

- **Random seed:** Utilize `crypto/rand` exclusively for cryptography; rely upon `math/rand` for standard approximation algorithms.
- **Variance:** A single, isolated run may perform dreadfully. Always execute multiple sweeping trials.

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
<strong>Summary Chapter 36:</strong> This chapter discusses approximation algorithms designed for NP-hard problems: greedy fractional knapsack (provably optimal), a 2-approximation for <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> cover, nearest neighbor and Christofides methods for metric TSP, alongside a randomized Max-Cut approach. Leverage greedy techniques for lightning-fast solutions, randomized algorithms for robust expected ratios, and Christofides for a rigorous 1.5 guarantee on metric TSPs.
{{% /alert %}}

## See Also

- [Chapter 25 — Greedy Algorithms](/docs/Part-VI/Chapter-25/)
- [Chapter 28 — Probabilistic and Randomized Algorithms](/docs/Part-VI/Chapter-28/)
- [Chapter 43 — Modern Algorithmic Thinking](/docs/Part-VIII/Chapter-43/)
