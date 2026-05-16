---
weight: 60200
title: "Chapter 23: Dynamic Programming"
description: "Dynamic Programming"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Memory prevents repetition.</em>" — George Santayana</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Dynamic programming (DP) solves complex problems. It breaks problems into <abbr title="Subproblems that recur multiple times in a recursive solution">overlapping subproblems</abbr>. It stores solutions to prevent redundant work.
{{% /alert %}}

## 23.1. DP Fundamentals

**Definition:** <abbr title="A method combining solutions to overlapping subproblems">Dynamic programming</abbr> solves problems by breaking them into <abbr title="Subproblems that recur multiple times in a recursive solution">overlapping subproblems</abbr>. Solve once. Store result. Reuse. Requires **<abbr title="Property where optimal solution contains optimal sub-solutions">optimal substructure</abbr>** and **<abbr title="Subproblems that recur multiple times in a recursive solution">overlapping subproblems</abbr>**.

**Mechanics:**
DP trades space for time. Caching subproblem results transforms exponential <code>O(2^n)</code> recursion into polynomial <code>O(n)</code> order.

**Use Cases:**
- Sequence alignment (DNA matching).
- Financial derivative pricing.
- Resource allocation (Knapsack).

**Memory Management:**
2D DP tables use `m * n` memory. Go `[][]int` scatters memory across slices. This causes <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>. State reduction saves space. Using two 1D slices instead of a matrix improves <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. This reduces <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">GC</abbr> pressure.

### Two Approaches

| Approach | Method | Space | Use Case |
|----------|--------|-------|----------|
| Top-down | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> + <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> | <code>O(n)</code> | Recursive logic |
| Bottom-up | Iterative table | <code>O(n)</code> or <code>O(n^2)</code> | No <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> overhead |

## 23.2. Fibonacci and Memoization

**Fact:** Fibonacci without memoization is <code>O(2^n)</code>. Memoization reduces it to <code>O(n)</code>.

### Go Implementation

```go
package main

import "fmt"

// Top-down: recursion + map
func fibMemo(n int, memo map[int]int) int {
	if n <= 1 { return n }
	if v, ok := memo[n]; ok { return v }
	memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo)
	return memo[n]
}

// Bottom-up: iteration + slice
func fibTab(n int) int {
	if n <= 1 { return n }
	dp := make([]int, n+1)
	dp[0], dp[1] = 0, 1
	for i := 2; i <= n; i++ {
		dp[i] = dp[i-1] + dp[i-2]
	}
	return dp[n]
}

func main() {
	fmt.Println(fibMemo(30, map[int]int{})) // 832040
	fmt.Println(fibTab(30))                 // 832040
}
```

## 23.3. 0/1 Knapsack Problem

**Goal:** Maximize item value within weight capacity. Items selected once.

### Go Implementation

```go
package main

import "fmt"

func knapsack(weights, values []int, capacity int) int {
	n := len(weights)
	dp := make([][]int, n+1)
	for i := range dp { dp[i] = make([]int, capacity+1) }
	
	for i := 1; i <= n; i++ {
		for w := 0; w <= capacity; w++ {
			if weights[i-1] <= w {
				dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i-1]]+values[i-1])
			} else {
				dp[i][w] = dp[i-1][w]
			}
		}
	}
	return dp[n][capacity]
}

func main() {
	weights := []int{2, 3, 4, 5}
	values := []int{3, 4, 5, 6}
	fmt.Println(knapsack(weights, values, 5)) // 7
}
```

## 23.4. Longest Common Subsequence (LCS)

**Goal:** Find length of longest shared subsequence. Relative order matters. Contiguity does not.

### Go Implementation

```go
package main

import "fmt"

func lcs(s1, s2 string) int {
	m, n := len(s1), len(s2)
	dp := make([][]int, m+1)
	for i := range dp { dp[i] = make([]int, n+1) }
	
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if s1[i-1] == s2[j-1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				dp[i][j] = max(dp[i-1][j], dp[i][j-1])
			}
		}
	}
	return dp[m][n]
}

func main() {
	fmt.Println(lcs("ABCDE", "ACE")) // 3
}
```

## 23.5. Decision Matrix

| Use DP If... | Use Alternatives If... |
|--------------|------------------------|
| Overlapping subproblems exist | <abbr title="An algorithm making locally optimal choices at each step.">Greedy</abbr> choice property holds |
| Optimal substructure exists | Subproblems are independent |
| Brute force is exponential | Simple algorithm exists |

### Edge Cases & Pitfalls

- **Space:** Reduce <code>O(n^2)</code> to <code>O(n)</code> using rolling arrays.
- **Overflow:** Large values exceed `int`. Use `int64`.
- **Initialization:** Base cases must be set. Zero-values lead to errors.

### Anti-Patterns

- **Maps for Dense State:** `map[int]int` is slow. Slice-based tabulation is 5-10x faster.
- **Wasted Memory:** 2D tables waste cache if subproblems only need previous rows.
- **Missing Base Cases:** Relying on zero-values creates bugs. Initialize explicitly.

## 23.6. Quick Reference

| Problem | Go Type | Time | Space | Approach |
|---------|---------|------|-------|----------|
| Fibonacci | `[]int` | <code>O(n)</code> | <code>O(n)</code> | Tabulation |
| Knapsack 0/1 | `[][]int` | <code>O(nW)</code> | <code>O(nW)</code> | 2D DP |
| LCS | `[][]int` | <code>O(mn)</code> | <code>O(mn)</code> | 2D DP |
| Coin Change | `[]int` | <code>O(nk)</code> | <code>O(n)</code> | 1D DP |


{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> DP solves exponential recursive problems in polynomial time. Identify states. Define recurrence. Initialize base cases. Fill table. Use slices for speed.
{{% /alert %}}

## See Also

- [Chapter 22: <abbr title="An algorithmic paradigm breaking problems into independent subproblems">Divide and Conquer</abbr>](/docs/part-vi/chapter-22/)
- [Chapter 24: Greedy Algorithms](/docs/part-vi/chapter-24/)
- [Chapter 25: <abbr title="Building candidates incrementally and abandoning dead ends">Backtracking</abbr>](/docs/part-vi/chapter-25/)