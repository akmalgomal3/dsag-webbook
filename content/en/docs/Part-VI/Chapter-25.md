---
weight: 60400
title: "Chapter 25: Backtracking"
description: "Backtracking"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Difficulty holds opportunity.</em>" — Albert Einstein</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
<abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> builds candidates incrementally. It abandons partial candidates upon constraint violation.
{{% /alert %}}

## 25.1. Backtracking Fundamentals

**Definition:** <abbr title="Building candidates incrementally and abandoning dead ends">Backtracking</abbr> refines <abbr title="A straightforward approach trying all possible solutions">brute-force</abbr>. It builds solutions incrementally. It backtracks upon constraint violation. It equals depth-first search of solution space.

**Mechanics:**
Backtracking explores exhaustively. Intelligent pruning stops dead ends. A violated constraint kills the search branch.

**Use Cases:**
- Constraint satisfaction (Sudoku).
- Regular expression parsing.
- Password discovery.
- Logical state machines (N-Queens).

**Memory Management:**
Backtracking uses the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>. Go passes slice <abbr title="A variable that stores a memory address.">pointers</abbr>. This avoids <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocation. Developers must undo mutations (`path = path[:len(path)-1]`) before returning. Failure corrupts shared memory.

### Template Structure

```text
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

## 25.2. N-Queens Problem

**Goal:** Place N queens on N×N board. Queens cannot threaten each other.

### Go Implementation

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

## 25.3. Subset Sum

**Goal:** Find subset matching target sum.

### Go Implementation

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

## 25.4. Permutations

**Goal:** Generate all permutations.

### Go Implementation

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

## 25.5. Selection Matrix

| Use Backtracking If... | Avoid If... |
|------------------------|-------------|
| Need all valid solutions | Only need existence |
| Constraints prune search | Problem size > 20 |
| Exact solution required | Approximation suffices |


### Decision Matrix

| Prefer This Approach When... | Prefer Alternatives When... |
|-----------------------------|------------------------------|
| Input constraints are known and stable. | Constraints change frequently or are unknown. |
| You need predictable complexity bounds. | You prioritize implementation speed over guarantees. |
| The trade-off is clear for production usage. | Benchmark evidence is insufficient. |

### Edge Cases & Pitfalls

- **State Management:** Restore state after recursion.
- **Pruning:** Missing pruning causes brute-force degradation.
- **Duplicates:** Sort and skip repeated elements.

### Anti-Patterns

- **Missing Restoration:** Forgetting state undo corrupts subsequent branches. Use `defer` or explicit undo.
- **No Pruning:** Search degenerates to <code>O(2^n)</code> brute force.
- **In-place Mutation:** Appending without popping corrupts branches.

## 25.6. Quick Reference

| Problem | Go Type | Time | Space | Key Insight |
|---------|---------|------|-------|-------------|
| N-Queens | `[]int` | <code>O(n!)</code> | <code>O(n)</code> | Column + diagonal checks |
| Subset Sum | Recursion | <code>O(2^n)</code> | <code>O(n)</code> | Include/exclude element |
| Permutations | Recursion | <code>O(n!)</code> | <code>O(n)</code> | Track used elements |
| Sudoku | `[][]int` | <code>O(9^m)</code> | <code>O(81)</code> | Constraint propagation |


{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Backtracking explores solution space systematically. Build candidates. Validate. Recurse. Undo. Go slices require proper cleanup.
{{% /alert %}}

## See Also

- [Chapter 23: Dynamic Programming](/docs/part-vi/chapter-23/)
- [Chapter 24: Greedy Algorithms](/docs/part-vi/chapter-24/)
- [Chapter 57: Minimax and Game Trees](/docs/part-xii/chapter-57/)