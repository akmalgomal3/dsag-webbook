---
weight: 6400
title: "Chapter 26 - Backtracking"
description: "Backtracking"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>In the middle of difficulty lies opportunity.</em>" — Albert Einstein</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 26 covers backtracking: a systematic way to explore all potential solutions by building candidates incrementally and abandoning partial candidates ("backtracking") as soon as they cannot possibly lead to a valid solution.
{{% /alert %}}

## 26.1. Backtracking Fundamentals

**Definition:** Backtracking is a refined brute-force approach that builds a solution incrementally. If a partial solution violates constraints, the algorithm backtracks and tries the next alternative. It is equivalent to a depth-first search of the solution space.

### Template Structure

```
func backtrack(candidate, path) {
    if isValidSolution(path) {
        recordSolution(path)
        return
    }
    for each option in candidates {
        if isValid(option, path) {
            path.add(option)
            backtrack(remainingCandidates, path)
            path.remove(option) // backtrack
        }
    }
}
```

## 26.2. N-Queens Problem

**Definition:** Place N queens on an N×N chessboard such that no two queens threaten each other. Queens attack horizontally, vertically, and diagonally.

### Idiomatic Go Implementation

Use a slice to track column positions; index represents row.

```go
package main

import "fmt"

func solveNQueens(n int) [][]string {
	var result [][]string
	var board []int // board[row] = col
	
	var backtrack func(row int)
	backtrack = func(row int) {
		if row == n {
			result = append(result, buildBoard(board, n))
			return
		}
		for col := 0; col < n; col++ {
			if isValid(board, row, col) {
				board = append(board, col)
				backtrack(row + 1)
				board = board[:len(board)-1]
			}
		}
	}
	
	backtrack(0)
	return result
}

func isValid(board []int, row, col int) bool {
	for r := 0; r < row; r++ {
		c := board[r]
		if c == col || row-r == col-c || row-r == c-col {
			return false
		}
	}
	return true
}

func buildBoard(board []int, n int) []string {
	var result []string
	for _, col := range board {
		row := make([]byte, n)
		for i := range row { row[i] = '.' }
		row[col] = 'Q'
		result = append(result, string(row))
	}
	return result
}

func main() {
	solutions := solveNQueens(4)
	fmt.Println(len(solutions)) // 2
}
```

## 26.3. Subset Sum

**Definition:** Given a set of integers and a target sum, determine if there is a subset that sums to the target.

### Idiomatic Go Implementation

```go
package main

import "fmt"

func subsetSum(nums []int, target int) bool {
	var backtrack func(start, sum int) bool
	backtrack = func(start, sum int) bool {
		if sum == target { return true }
		if sum > target || start >= len(nums) { return false }
		// Include nums[start]
		if backtrack(start+1, sum+nums[start]) { return true }
		// Exclude nums[start]
		if backtrack(start+1, sum) { return true }
		return false
	}
	return backtrack(0, 0)
}

func main() {
	nums := []int{3, 34, 4, 12, 5, 2}
	fmt.Println(subsetSum(nums, 9))  // true (4+5)
	fmt.Println(subsetSum(nums, 30)) // false
}
```

## 26.4. Permutations

**Definition:** Generate all permutations of a given set of distinct elements.

### Idiomatic Go Implementation

```go
package main

import "fmt"

func permutations(nums []int) [][]int {
	var result [][]int
	var backtrack func(path []int, used []bool)
	backtrack = func(path []int, used []bool) {
		if len(path) == len(nums) {
			perm := make([]int, len(path))
			copy(perm, path)
			result = append(result, perm)
			return
		}
		for i := 0; i < len(nums); i++ {
			if used[i] { continue }
			used[i] = true
			backtrack(append(path, nums[i]), used)
			used[i] = false
		}
	}
	backtrack([]int{}, make([]bool, len(nums)))
	return result
}

func main() {
	fmt.Println(len(permutations([]int{1, 2, 3}))) // 6
}
```

## 26.5. Decision Matrix

| Use Backtracking When... | Avoid If... |
|--------------------------|-------------|
| Need all valid solutions | Only need existence (use DP or greedy) |
| Constraints prune search space heavily | Problem size > 20 (exponential blowup) |
| Exact solution required | Approximation suffices |

### Edge Cases & Pitfalls

- **State management:** Ensure state is fully restored after recursive calls.
- **Pruning:** Aggressive pruning is essential; without it, backtracking degrades to brute force.
- **Duplicate handling:** For inputs with duplicates, sort and skip repeated elements.

## 26.6. Quick Reference

| Problem | Go Type | Time | Space | Key Insight |
|---------|---------|------|-------|-------------|
| N-Queens | `[]int` | <code>O(n!)</code> | <code>O(n)</code> | Column + diagonal checks |
| Subset Sum | Recursion | <code>O(2^n)</code> | <code>O(n)</code> | Include/exclude each element |
| Permutations | Recursion | <code>O(n!)</code> | <code>O(n)</code> | Track used elements |
| Sudoku | `[][]int` | <code>O(9^m)</code> | <code>O(81)</code> | Constraint propagation |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 26:</strong> Backtracking systematically explores the solution space using depth-first search with pruning. Master the template: build candidates incrementally, validate constraints, recurse, and undo changes. In Go, use slices for state tracking and ensure proper cleanup after each recursive call.
{{% /alert %}}
