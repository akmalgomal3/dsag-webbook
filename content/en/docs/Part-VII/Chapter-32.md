---
weight: 70500
title: "Chapter 32: Linear Programming"
description: "Linear Programming"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Optimization is a powerful tool for solving many types of problems, and linear programming provides one of the most fundamental approaches.</em>" : John Nash</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 32 covers linear programming: fundamental formulation, the Simplex algorithm, and implementations in Go using iterative methods and external solvers.
{{% /alert %}}

## 32.1. Linear Programming Formulation

**Definition:** <abbr title="Optimizing a linear objective function under linear equality and inequality constraints.">Linear Programming</abbr> (LP) optimizes linear <abbr title="The function to be maximized or minimized in an optimization problem.">objective function</abbr>. Subject to linear <abbr title="Conditions or restrictions in an optimization problem that define the solution space.">constraints</abbr>.

**Mechanics:**
Geometric optimization follows linear constraints. Constraints form convex polytope. <abbr title="The set of all valid solutions satisfying all constraints in an optimization problem.">"Feasible region"</abbr> represents valid space. Optimal solution resides on vertex. Solver walks edges to find peak.

**Use Cases:**
Airline scheduling. Portfolio optimization. Supply chains. Logistics routing.

**Memory Mechanics:**
Simplex uses tableau matrix. Row updates use Gaussian elimination. SIMD instructions optimize <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> memory. Large models use sparse memory maps. Prevents <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> exhaustion.

Standard form:
```
maximize: cᵀx
subject to: Ax ≤ b, x ≥ 0
```

### Operations & Complexity

| Algorithm | Worst Case | Average | Description |
|-----------|------------|---------|------------|
| <abbr title="An algorithm for solving linear programming problems by traversing polytope vertices.">Simplex</abbr> | <code>O(2^n)</code> | <code>O(n³)</code> | Pivot-based traversal |
| Interior Point | <code>O(n³·⁵L)</code> | <code>O(n³)</code> | Polynomial time |
| Dual Simplex | <code>O(2^n)</code> | <code>O(n³)</code> | Starts dual feasible |

### Pseudocode

```text
Solve2DLP(c1, c2, constraints):
    bestVal = -infinity
    bestX, bestY = 0, 0
    for each pair of constraints (i, j):
        compute intersection point (x, y)
        if x < 0 or y < 0: continue
        if point satisfies all constraints:
            val = c1*x + c2*y
            if val > bestVal:
                bestVal = val
                bestX, bestY = x, y
    return bestX, bestY, bestVal
```

### Idiomatic Go Implementation

Go lacks native LP solver. Use C bindings or simplified methods.

```go
package main

import (
    "fmt"
    "math"
)

func solve2DLP(c1, c2 float64, constraints [][3]float64) (float64, float64, float64) {
    bestVal := math.Inf(-1)
    var bestX, bestY float64
    n := len(constraints)
    for i := 0; i < n; i++ {
        for j := i + 1; j < n; j++ {
            a1, b1, c1c := constraints[i][0], constraints[i][1], constraints[i][2]
            a2, b2, c2c := constraints[j][0], constraints[j][1], constraints[j][2]
            det := a1*b2 - a2*b1
            if math.Abs(det) < 1e-9 {
                continue
            }
            x := (c1c*b2 - c2c*b1) / det
            y := (a1*c2c - a2*c1c) / det
            if x < 0 || y < 0 {
                continue
            }
            valid := true
            for _, con := range constraints {
                if con[0]*x+con[1]*y > con[2]+1e-9 {
                    valid = false
                    break
                }
            }
            if valid {
                val := c1*x + c2*y
                if val > bestVal {
                    bestVal = val
                    bestX, bestY = x, y
                }
            }
        }
    }
    return bestX, bestY, bestVal
}

func main() {
    constraints := [][3]float64{
        {1, 1, 4},
        {1, 2, 5},
        {-1, 0, 0},
        {0, -1, 0},
    }
    x, y, val := solve2DLP(3, 2, constraints)
    fmt.Printf("x=%.2f y=%.2f val=%.2f\n", x, y, val)
}
```

{{% alert icon="📌" context="warning" %}}
Manual Simplex implementation in Go is error-prone. Use GLPK, lp_solve, or `github.com/codered/lp` for production.
{{% /alert %}}

### Decision Matrix

| Use LP When... | Avoid If... |
|-------------------|------------------|
| Linear objective and constraints | Objective non-linear. Use NLP. |
| Continuous variable domains | Variables demand integers. Use MILP. |

### Edge Cases & Pitfalls

- **Infeasible problem:** Constraints contradict. Phase-I Simplex detects.
- **Unbounded problem:** Objective grows to infinity. Check feasible boundaries.
- **Degeneracy:** Simplex cycles infinitely. Use Bland's rule.

## 32.2. Integer Linear Programming

**Definition:** Variables must be integers. Branch and Bound is industry standard.

### Operations & Complexity

| Algorithm | Worst Case | Description |
|-----------|------------|------------|
| Branch and Bound | <code>O(2^n)</code> | Exponential exploration |
| Cutting Plane | <code>O(2^n)</code> | Polynomial for LP relaxation |

### Pseudocode

```text
KnapsackILP(weights, values, capacity):
    n = length(weights)
    dp = 2D table (n+1) x (capacity+1) initialized to 0
    for i from 1 to n:
        for w from 0 to capacity:
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])
    return dp[n][capacity]
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func knapsackILP(weights, values []int, capacity int) int {
    n := len(weights)
    dp := make([][]int, n+1)
    for i := range dp {
        dp[i] = make([]int, capacity+1)
    }
    for i := 1; i <= n; i++ {
        for w := 0; w <= capacity; w++ {
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w {
                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]]+values[i-1])
            }
        }
    }
    return dp[n][capacity]
}

func main() {
    weights := []int{2, 3, 4, 5}
    values := []int{3, 4, 5, 6}
    fmt.Println("Knapsack ILP:", knapsackILP(weights, values, 5))
}
```

{{% alert icon="📌" context="warning" %}}
0/1 Knapsack is NP-hard. Resolvable in pseudo-polynomial <code>O(nW)</code> time. Branch and Bound applies universally to ILP.
{{% /alert %}}

### Decision Matrix

| Use DP When... | Use Branch & Bound When... |
|-------------------|-------------------------------|
| Knapsack with small capacity | Generalized ILP problem |
| Pseudo-polynomial time acceptable | Global optimality required |

## 32.3. Duality and Sensitivity

**Definition:** Every LP (primal) has associated dual. Optimal primal equals optimal dual.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Dual formulation | <code>O(mn)</code> | Convert constraints |
| Shadow price | <code>O(1)</code> | Read from optimal tableau |
| Sensitivity range | <code>O(n)</code> | Calculated per variable |

### Pseudocode

```text
FormulateDual(A, b, c):
    m = rows in A
    n = cols in A
    dual objective: minimize b^T y
    dual constraints: A^T y >= c, y >= 0
    return dual formulation
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func formulateDual(A [][]float64, b, c []float64) {
    m, n := len(A), len(A[0])
    fmt.Println("Dual variables:", m)
    fmt.Println("Dual objective: minimize b^T y")
    fmt.Printf("Dual constraints: A^T y >= c (%d constraints)\n", n)
}

func main() {
    A := [][]float64{{1, 1}, {1, 2}}
    b := []float64{4, 5}
    c := []float64{3, 2}
    formulateDual(A, b, c)
}
```

{{% alert icon="📌" context="warning" %}}
Dual LP aids sensitivity analysis. Primal-dual algorithms use it. Production solvers provide dual data automatically.
{{% /alert %}}

### Decision Matrix

| Use Dual When... | Avoid If... |
|---------------------|------------------|
| Sensitivity analysis required | Primal solution suffices |
| Primal model infeasible | Dual yields no insight |

### Anti-Patterns

- **Hand-rolling Simplex:** Manual implementations unstable. Use GLPK or lp_solve.
- **Floating-point DP:** `float64` in knapsack DP causes rounding errors. Use `int`.
- **Skip relaxation checks:** Branch and Bound on infeasible regions wastes time. Solve LP relaxation first. Prune branches early.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| LP Solver | External | <code>O(n^3)</code> avg | varies | Continuous optimization |
| Knapsack DP | `[][]int` | <code>O(nW)</code> | <code>O(nW)</code> | Integer programming |
| Constraints | `[]float64` | . | . | Mathematical bounds |
| Dual | Formulation | <code>O(mn)</code> | varies | Sensitivity analysis |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 32:</strong> Linear programming optimizes linear objectives under constraints. Simplex traverses polytope vertices. ILP uses branch and bound. Duality provides sensitivity analysis. Use external solvers for production.
{{% /alert %}}

## See Also

- [Chapter 2: Complexity Analysis](/docs/part-i/chapter-2/)
- [Chapter 15: All-Pairs Shortest Paths](/docs/part-iv/chapter-15/)
- [Chapter 28: Vector, Matrix, and Tensor Operations](/docs/part-vii/chapter-28/)
