---
weight: 70500
title: "Chapter 33: Linear Programming"
description: "Linear Programming"
icon: "article"
date: "2024-08-24T23:42:49+07:00"
lastmod: "2024-08-24T23:42:49+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Optimization is a powerful tool for solving many types of problems, and linear programming provides one of the most fundamental approaches.</em>" : John Nash</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 33 covers linear programming: fundamental formulation, the Simplex algorithm, and implementations in Go leveraging both iterative methods and external solvers.
{{% /alert %}}

## 33.1. Linear Programming Formulation

**Definition:** <abbr title="Optimizing a linear objective function under linear equality and inequality constraints.">Linear Programming</abbr> (LP) aims to maximize or minimize a linear <abbr title="The function to be maximized or minimized in an optimization problem.">objective function</abbr> subject strictly to linear equality and inequality <abbr title="Conditions or restrictions in an optimization problem that define the solution space.">constraints</abbr>.

**Background & Philosophy:**
The philosophy is geometric optimization. Linear constraints form a convex <abbr title="A plane figure bounded by straight line segments">polygon</abbr> (or polytope in N-dimensions) representing the <abbr title="The set of all valid solutions satisfying all constraints in an optimization problem.">"feasible region"</abbr>. The fundamental theorem of LP states that the optimal solution *always* lies on a vertex (corner) of this polytope. Because of this mathematical certainty, solvers do not need to check infinite interior points; they only need to "walk" along the edges from corner to corner until they find the peak.

**Use Cases:**
Airline crew scheduling, financial portfolio optimization, manufacturing supply chains, and routing massive logistical fleets.

**Memory Mechanics:**
LP solvers (like Simplex) use a tableau (a 2D matrix) to represent equations. Modifying this tableau involves Gaussian elimination, scanning and updating entire rows. Because the matrix elements are <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr>, the CPU processes them efficiently using SIMD instructions. However, in enormous real-world models with millions of variables, these matrices are hyper-sparse (mostly zeros). Efficient LP solvers discard the 2D array format entirely, using specialized sparse memory maps to prevent exhausting system <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>.

Standard form:
```
maximize: cᵀx
subject to: Ax ≤ b, x ≥ 0
```

### Operations & Complexity

| Algorithm | Worst Case | Average | Description |
|-----------|------------|---------|------------|
| <abbr title="An algorithm for solving linear programming problems by traversing polytope vertices.">Simplex</abbr> | <code>O(2^n)</code> | <code>O(n³)</code> | Pivot-based <abbr title="A fundamental unit of a graph, also called a node.">vertex</abbr> traversal |
| Interior Point | <code>O(n³·⁵L)</code> | <code>O(n³)</code> | Strictly polynomial |
| Dual Simplex | <code>O(2^n)</code> | <code>O(n³)</code> | Starts from a dual feasible state |

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

Go's standard <abbr title="A collection of precompiled routines that a program can use.">library</abbr> does not provide a native LP solver. Use C bindings or write a highly simplified implementation for trivial cases.

```go
package main

import (
    "fmt"
    "math"
)

// Simplified Simplex for 2 variables (graphical corner-point method)
func solve2DLP(c1, c2 float64, constraints [][3]float64) (float64, float64, float64) {
    bestVal := math.Inf(-1)
    var bestX, bestY float64
    // Find corner points from constraint intersections
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
    // max 3x + 2y subject to x + y <= 4, x + 2y <= 5, x,y >= 0
    constraints := [][3]float64{
        {1, 1, 4},
        {1, 2, 5},
        {-1, 0, 0}, // x >= 0  (encoded as -1*x + 0*y <= 0)
        {0, -1, 0}, // y >= 0  (encoded as 0*x + -1*y <= 0)
    }
    x, y, val := solve2DLP(3, 2, constraints)
    fmt.Printf("x=%.2f y=%.2f val=%.2f\n", x, y, val)
}
```

{{% alert icon="📌" context="warning" %}}
Writing a full, robust Simplex implementation in Go from scratch is incredibly verbose and error-prone. For production systems, leverage bindings to GLPK, lp_solve, or robust Go libraries such as `github.com/codered/lp`.
{{% /alert %}}

### Decision Matrix

| Use LP When... | Avoid If... |
|-------------------|------------------|
| Both the objective and constraints are strictly linear | The objective is non-linear (employ NLP instead) |
| Variables represent continuous domains | Variables demand integer values (employ MILP) |

### Edge Cases & Pitfalls

- **Infeasible problem:** Constraints blatantly contradict each other. Verify using phase-I of the Simplex method.
- **Unbounded problem:** The objective function can grow to infinity. Verify the feasible region's boundaries.
- **Degeneracy:** Simplex can fall into infinite cycling. Counteract this by implementing Bland's rule.

## 33.2. Integer Linear Programming

**Definition:** Integer Linear Programming (ILP) strictly mandates that some or all variables represent integer values. Branch and Bound stands as the industry-standard resolution method.

### Operations & Complexity

| Algorithm | Worst Case | Description |
|-----------|------------|------------|
| Branch and Bound | <code>O(2^n)</code> | Exponential exploration |
| Cutting Plane | <code>O(2^n)</code> | Polynomial solely for the LP relaxation |

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

import (
    "fmt"
)

// 0/1 Knapsack treated as an ILP via DP (pseudo-polynomial time)
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

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

func main() {
    weights := []int{2, 3, 4, 5}
    values := []int{3, 4, 5, 6}
    fmt.Println("Knapsack ILP:", knapsackILP(weights, values, 5))
}
```

{{% alert icon="📌" context="warning" %}}
0/1 Knapsack is inherently NP-hard, yet resolvable within pseudo-polynomial <code>O(nW)</code> bounds. Branch and Bound serves as a much more universally applicable approach for standard ILP.
{{% /alert %}}

### Decision Matrix

| Use DP When... | Use Branch & Bound When... |
|-------------------|-------------------------------|
| Solving Knapsack with a reasonably small W | Facing a generalized ILP problem |
| Pseudo-polynomial performance is acceptable | An exact, globally optimal solution is absolutely required |

### Edge Cases & Pitfalls

- **Integer overflow:** The required DP table can expand massively. Utilize heavy space optimization (e.g., 1D arrays).
- **Feasibility:** Consistently verify if any mathematical solution actively satisfies the defined constraints.

## 33.3. Duality and Sensitivity

**Definition:** Every single LP (the primal) possesses an associated dual. Strong duality states: the optimal primal equals the optimal dual, provided a feasible solution exists.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Dual formulation | <code>O(mn)</code> | Structurally converting constraints |
| Shadow price | <code>O(1)</code> | Readily available from the optimal tableau |
| Sensitivity range | <code>O(n)</code> | Calculated per individual variable |

### Pseudocode

```text
FormulateDual(A, b, c):
    m = number of rows in A
    n = number of cols in A
    dual objective: minimize b^T y
    dual constraints: A^T y >= c, y >= 0
    return dual formulation
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

// Dual formulation of max c^T x subject to Ax <= b is min b^T y subject to A^T y >= c, y >= 0
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
The Dual LP proves highly beneficial for intensive sensitivity analysis and driving primal-dual algorithms. Within Go, calculating the dual formulation manually is rarely necessary; external solvers naturally provide this data.
{{% /alert %}}

### Decision Matrix

| Use Dual When... | Avoid If... |
|---------------------|------------------|
| Conducting deep sensitivity analysis | The primal solution independently suffices |
| The primal model is infeasible | Exploring the dual yields no actionable benefit |

### Edge Cases & Pitfalls

- **Weak duality:** Any feasible dual <abbr title="The data associated with a key in a key-value pair.">value</abbr> definitively bounds the primal. The gap fails to reach zero solely if the system is infeasible or unbounded.
- **Complementary slackness:** Strictly utilize this to verify the ultimate optimality.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| LP Solver | External / custom | <code>O(n^3)</code> avg | varies | Continuous variable optimization |
| Knapsack DP | `[][]int` | <code>O(nW)</code> | <code>O(nW)</code> | Integer-based programming |
| Constraints | `[]float64` | . | . | Defining mathematical bounds |
| Objective | `[]float64` | . | . | Establishing coefficients |
| Dual | Formulation | <code>O(mn)</code> | varies | Executing sensitivity analysis |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 33:</strong> This chapter discusses linear programming: grasping standard formulations, applying the Simplex algorithm conceptually for 2 variables, tackling integer linear programming through <abbr title="Finding optimal solutions by pruning search trees">branch and bound</abbr> (and DP for knapsack variants), and examining duality for sensitivity analysis. Strongly prefer external solvers for production environments; reserve manual implementations purely for deep educational exercises.
{{% /alert %}}

## See Also

- [Chapter 2: Complexity Analysis](/docs/Part-I/Chapter-2/)
- [Chapter 15: All-Pairs Shortest Paths](/docs/Part-IV/Chapter-15/)
- [Chapter 29: Vector, Matrix, and Tensor Operations](/docs/Part-VII/Chapter-29/)
