---
weight: 60200
title: "Chapter 24 - Dynamic Programming"
description: "Dynamic Programming"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Those who cannot remember the past are condemned to repeat it.</em>" — George Santayana</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 24 covers dynamic programming (DP): a method for solving complex problems by breaking them into overlapping subproblems and storing solutions to avoid redundant computation.
{{% /alert %}}

## 24.1. DP Fundamentals

**Definition:** Dynamic programming solves problems by breaking them into smaller overlapping subproblems, solving each subproblem once, and storing the result for reuse. It applies when a problem exhibits **optimal substructure** and **overlapping subproblems**.

### Two Approaches

| Approach | Method | Space | Use Case |
|----------|--------|-------|----------|
| Top-down (Memoization) | Recursion + cache | <code>O(n)</code> | Natural recursive formulation |
| Bottom-up (Tabulation) | Iterative table filling | <code>O(n)</code> or <code>O(n^2)</code> | Better constant factors, no recursion stack |

## 24.2. Fibonacci and Memoization

**Definition:** The classic Fibonacci sequence demonstrates DP. Without memoization, it has <code>O(2^n)</code> complexity; with memoization, it drops to <code>O(n)</code>.

### Idiomatic Go Implementation

Use a `map[int]int` for memoization or a slice for tabulation.

```go
package main

import "fmt"

// Top-down with memoization
func fibMemo(n int, memo map[int]int) int {
	if n <= 1 { return n }
	if v, ok := memo[n]; ok { return v }
	memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo)
	return memo[n]
}

// Bottom-up tabulation
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

## 24.3. 0/1 Knapsack Problem

**Definition:** Given items with weights and values, select items to maximize total value without exceeding a weight capacity. Each item can be taken at most once.

### Idiomatic Go Implementation

Use a 2D DP table or optimize to 1D.

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

func max(a, b int) int { if a > b { return a }; return b }

func main() {
	weights := []int{2, 3, 4, 5}
	values := []int{3, 4, 5, 6}
	fmt.Println(knapsack(weights, values, 5)) // 7
}
```

## 24.4. Longest Common Subsequence (LCS)

**Definition:** Given two sequences, find the length of the longest subsequence present in both. A subsequence maintains relative order but need not be contiguous.

### Idiomatic Go Implementation

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

## 24.5. Decision Matrix

| Use DP When... | Avoid If... |
|----------------|-------------|
| Problem has overlapping subproblems | Greedy choice property holds (use greedy instead) |
| Optimal substructure exists | Subproblems are independent (use divide and conquer) |
| Brute force is exponential | A simpler algorithm achieves same result |

### Edge Cases & Pitfalls

- **Space optimization:** Many DP problems can reduce from <code>O(n^2)</code> to <code>O(n)</code> by only keeping the previous row.
- **Integer overflow:** Knapsack and similar problems may overflow; use `int64` for large values.
- **Base cases:** Incorrect initialization of DP table leads to wrong answers.

## 24.6. Quick Reference

| Problem | Go Type | Time | Space | Approach |
|---------|---------|------|-------|----------|
| Fibonacci | `[]int` or `map` | <code>O(n)</code> | <code>O(n)</code> | Tabulation |
| Knapsack 0/1 | `[][]int` | <code>O(nW)</code> | <code>O(nW)</code> | 2D DP |
| LCS | `[][]int` | <code>O(mn)</code> | <code>O(mn)</code> | 2D DP |
| Coin Change | `[]int` | <code>O(nk)</code> | <code>O(n)</code> | 1D DP |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 24:</strong> Dynamic programming transforms exponential-time recursive problems into polynomial-time solutions by storing subproblem results. Master the pattern: define states, write the recurrence, initialize base cases, and fill the table. In Go, use slices for tabulation and maps for sparse memoization.
{{% /alert %}}
