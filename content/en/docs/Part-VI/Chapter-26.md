---
weight: 60500
title: "Chapter 26: Advanced Recursive Algorithms"
description: "Advanced Recursive Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A recursive function calls itself, like a mirror facing a mirror, reflecting a problem into simpler and simpler versions of itself until it vanishes.</em>" : Brian Kernighan</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 27 covers advanced <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>: <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr>, recursive data structures, <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr>, <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr>, and <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr> — all implemented idiomatically in Go.
{{% /alert %}}

## 27.1. Fundamentals of <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr>

**Definition:** <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> is a programming technique where a function calls itself to solve smaller sub-problems until it reaches a base case.

**Background & Philosophy:**
The philosophy elevates recursion from a simple loop replacement to a structural paradigm. It treats functions as mathematical formulas that map complex states to simpler sub-states, proving algorithmic correctness through induction.

**Use Cases:**
Tree Traversals, parsing hierarchical data structures like ASTs in compilers, and orchestrating complex distributed tasks.

**Memory Mechanics:**
Advanced recursion heavily loads the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>. In Go, parallel recursion (spawning goroutines for sub-branches) shifts this load from a single deep stack to thousands of shallow, 2KB <abbr title="A lightweight concurrent execution thread managed by the Go runtime">goroutine</abbr> stacks spread across the <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. This enables massive horizontal scaling without single-thread <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>, provided the developer sets a threshold to avoid <abbr title="A lightweight concurrent execution thread managed by the Go runtime">goroutine</abbr> overhead for trivially small sub-problems.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Factorial | <code>O(n)</code> | n recursive calls |
| Naive Fibonacci | <code>O(2^n)</code> | Exponential without <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr> |
| Memoized Fibonacci | <code>O(n)</code> | <abbr title="An algorithm whose running time grows linearly with input size.">Linear time</abbr> with caching |
| <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> | <code>O(n log n)</code> | Classic <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> |

### Pseudocode

```text
Factorial(n):
    if n <= 1:
        return 1
    return n * Factorial(n - 1)

Fibonacci(n, cache):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = Fibonacci(n-1, cache) + Fibonacci(n-2, cache)
    return cache[n]
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func factorial(n int) int {
    if n <= 1 {
        return 1
    }
    return n * factorial(n-1)
}

func fibonacci(n int, cache map[int]int) int {
    if val, ok := cache[n]; ok {
        return val
    }
    if n <= 1 {
        return n
    }
    cache[n] = fibonacci(n-1, cache) + fibonacci(n-2, cache)
    return cache[n]
}

func main() {
    fmt.Println("5! =", factorial(5))
    cache := make(map[int]int)
    fmt.Println("Fib(10) =", fibonacci(10, cache))
}
```

{{% alert icon="📌" context="warning" %}}
Go does not guarantee tail call optimization. Avoid extremely deep <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>; use <abbr title="The repetition of a process, typically using loops.">iteration</abbr> or increase the <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> size if necessary.
{{% /alert %}}

### Decision Matrix

| Use <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> When... | Avoid If... |
|------------------------|------------------|
| The problem divides naturally (trees, graphs) | <abbr title="The length of the path from the root to a node.">Depth</abbr> > 10^4 (risk of <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>) |
| <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> is required (N-Queens, Sudoku) | Sub-problems overlap heavily without <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr> |
| <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and conquer</abbr> (Merge/<abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick sort</abbr>) | Performance is hyper-critical and call overhead matters |

### Edge Cases & Pitfalls

- **<abbr title="An error caused by using more stack memory than allocated.">Stack overflow</abbr>:** <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> without a base case or excessive <abbr title="The length of the path from the root to a node.">depth</abbr>. Go stacks start at 2KB and grow, but are still bounded.
- **Missing base case:** Always define the termination condition.
- **Redundant computation:** Without <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr>, naive Fibonacci computes the same sub-problems repeatedly.

## 27.2. <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr>

**Definition:** A strategy that breaks a problem into independent sub-problems, solves each recursively, and then combines their results.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> | <code>O(n log n)</code> | <code>O(n)</code> | Stable, divides arrays |
| <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick Sort</abbr> | <code>O(n log n)</code> avg | <code>O(log n)</code> | In-place, randomized pivot |
| <abbr title="A search algorithm that finds the position of a target value within a sorted array.">Binary Search</abbr> | <code>O(log n)</code> | <code>O(1)</code> iterative, <code>O(log n)</code> recursive | Sorted <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> required |

### Pseudocode

```text
MergeSort(A):
    if length(A) <= 1:
        return A
    mid = length(A) / 2
    left = MergeSort(A[0:mid])
    right = MergeSort(A[mid:])
    return Merge(left, right)

QuickSort(A):
    if length(A) <= 1:
        return A
    pivot = random element in A
    left = elements < pivot
    mid = elements == pivot
    right = elements > pivot
    return QuickSort(left) + mid + QuickSort(right)
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math/rand"
    "time"
)

func mergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    mid := len(arr) / 2
    left := mergeSort(arr[:mid])
    right := mergeSort(arr[mid:])
    return merge(left, right)
}

func merge(left, right []int) []int {
    result := make([]int, 0, len(left)+len(right))
    i, j := 0, 0
    for i < len(left) && j < len(right) {
        if left[i] < right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }
    result = append(result, left[i:]...)
    result = append(result, right[j:]...)
    return result
}

func quickSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    pivot := arr[rand.Intn(len(arr))]
    var left, mid, right []int
    for _, v := range arr {
        switch {
        case v < pivot:
            left = append(left, v)
        case v == pivot:
            mid = append(mid, v)
        default:
            right = append(right, v)
        }
    }
    left = quickSort(left)
    right = quickSort(right)
    return append(append(left, mid...), right...)
}

func main() {
    rand.Seed(time.Now().UnixNano()) // removed in Go 1.20+: auto-seeded
    arr := []int{3, 1, 4, 1, 5, 9, 2, 6}
    fmt.Println("Merge:", mergeSort(arr))
    fmt.Println("Quick:", quickSort(arr))
}
```

{{% alert icon="📌" context="warning" %}}
<abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick Sort</abbr> with a deterministic pivot on a sorted <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> degrades to <code>O(n^2)</code>. A random pivot or median-of-three avoids this <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> scenario.
{{% /alert %}}

### Decision Matrix

| Use D&C When... | Avoid If... |
|--------------------|------------------|
| The problem can be partitioned independently | Sub-problems overlap (use DP instead) |
| Combining results is easier than a direct solution | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> overhead outweighs the performance gain |

### Edge Cases & Pitfalls

- **Empty or single-element <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>:** Handle these immediately before recursive calls.
- **Integer overflow on mid:** Use `mid := low + (high-low)/2` instead of `(low+high)/2`.
- **<abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> <abbr title="The length of the path from the root to a node.">depth</abbr>:** <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick Sort</abbr> on a <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">linked list</abbr> can cause a <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>.

## 27.3. Recursive Data Structures

**Definition:** Data structures defined in terms of themselves, such as linked lists and binary trees.

### Operations & Complexity

| Operation | <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">Linked List</abbr> | <abbr title="A tree data structure in which each node has at most two children.">Binary Tree</abbr> (BST) |
|---------|-------------|-------------------|
| Insert | <code>O(n)</code> | <code>O(h)</code> = <code>O(log n)</code> balanced |
| Search | <code>O(n)</code> | <code>O(h)</code> = <code>O(log n)</code> balanced |
| Delete | <code>O(n)</code> | <code>O(h)</code> = <code>O(log n)</code> balanced |
| Traversal | <code>O(n)</code> | <code>O(n)</code> |

### Pseudocode

```text
TreeInsert(node, value):
    if node is nil:
        create new node with value
        return
    if value < node.value:
        if node.left is nil:
            node.left = new node(value)
        else:
            TreeInsert(node.left, value)
    else:
        if node.right is nil:
            node.right = new node(value)
        else:
            TreeInsert(node.right, value)

TreeInorder(node):
    if node is nil:
        return empty list
    return TreeInorder(node.left) + [node.value] + TreeInorder(node.right)
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

type Node struct {
    Value int
    Next  *Node
}

type Tree struct {
    Value int
    Left  *Tree
    Right *Tree
}

func (t *Tree) Insert(value int) {
    if t == nil {
        return
    }
    if value < t.Value {
        if t.Left == nil {
            t.Left = &Tree{Value: value}
        } else {
            t.Left.Insert(value)
        }
    } else {
        if t.Right == nil {
            t.Right = &Tree{Value: value}
        } else {
            t.Right.Insert(value)
        }
    }
}

func (t *Tree) Inorder() []int {
    if t == nil {
        return nil
    }
    result := t.Left.Inorder()
    result = append(result, t.Value)
    result = append(result, t.Right.Inorder()...)
    return result
}

func main() {
    root := &Tree{Value: 5}
    for _, v := range []int{3, 7, 1, 4, 6, 8} {
        root.Insert(v)
    }
    fmt.Println("Inorder:", root.Inorder())
}
```

{{% alert icon="📌" context="warning" %}}
Go does not have destructuring pattern matching. Use pointers (`*Tree`) and explicit nil checks to manipulate recursive structures.
{{% /alert %}}

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Establishing hierarchical relationships (trees) | Frequent random access is needed (use slices) |
| Dynamic sizing with frequent inserts/deletes | <abbr title="A variable that stores a memory address.">Pointer</abbr> memory overhead is a concern |

### Edge Cases & Pitfalls

- **Dangling <abbr title="A variable that stores a memory address.">pointer</abbr>:** Always check for `nil` before dereferencing.
- **Circular references:** Go's GC handles cycles, but avoid unnecessary cyclical designs.
- **<abbr title="An error caused by using more stack memory than allocated.">Stack overflow</abbr> traversal:** For exceedingly deep trees, use <abbr title="The repetition of a process, typically using loops.">iteration</abbr> with an explicit <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr>.

## 27.4. <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">Memoization</abbr> and <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr>

**Definition:** <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">Memoization</abbr> caches function results for identical inputs; <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr> breaks down overlapping sub-problems and stores solutions in a table.

### Operations & Complexity

| Approach | Time | Space |
|------------|------|-------|
| Top-down (<abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr>) | <code>O(n)</code> | <code>O(n)</code> call <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> + <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> |
| Bottom-up (<abbr title="A bottom-up dynamic programming technique filling a table iteratively.">tabulation</abbr>) | <code>O(n)</code> | <code>O(n)</code> table |
| Space-optimized | <code>O(n)</code> | <code>O(1)</code> or <code>O(k)</code> |

### Pseudocode

```text
FibMemo(n):
    cache = empty map
    return FibHelper(n, cache)

FibHelper(n, cache):
    if n <= 1: return n
    if n in cache: return cache[n]
    cache[n] = FibHelper(n-1, cache) + FibHelper(n-2, cache)
    return cache[n]

Knapsack(weights, values, capacity):
    dp = 2D table of size (n+1) x (capacity+1) initialized to 0
    for i from 1 to n:
        for w from 0 to capacity:
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func fibMemo(n int) int {
    cache := make(map[int]int)
    var fib func(int) int
    fib = func(n int) int {
        if n <= 1 {
            return n
        }
        if v, ok := cache[n]; ok {
            return v
        }
        cache[n] = fib(n-1) + fib(n-2)
        return cache[n]
    }
    return fib(n)
}

func fibBottomUp(n int) int {
    if n <= 1 {
        return n
    }
    dp := make([]int, n+1)
    dp[1] = 1
    for i := 2; i <= n; i++ {
        dp[i] = dp[i-1] + dp[i-2]
    }
    return dp[n]
}

func knapsack(weights, values []int, capacity int) int {
    n := len(weights)
    dp := make([][]int, n+1)
    for i := range dp {
        dp[i] = make([]int, capacity+1)
    }
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
    fmt.Println("Fib memo:", fibMemo(40))
    fmt.Println("Fib DP:", fibBottomUp(40))
    weights := []int{2, 3, 4, 5}
    values := []int{3, 4, 5, 6}
    fmt.Println("Knapsack:", knapsack(weights, values, 5))
}
```

{{% alert icon="📌" context="warning" %}}
Top-down approaches with deep <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> in Go carry the risk of <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr> for n > 10^5. Bottom-up approaches are safer for massive scales.
{{% /alert %}}

### Decision Matrix

| Use Top-down When... | Use Bottom-up When... |
|-------------------------|--------------------------|
| Not all sub-problems need evaluating | Every sub-problem must be evaluated |
| A recursive formulation is more natural | Space optimization is required |
| n is small to medium | n is exceptionally large, avoiding the call <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> |

### Edge Cases & Pitfalls

- **Integer overflow:** DP on Fibonacci exceeds `int64` at n=93. Utilize `math/big` if necessary.
- **Wrong base case:** Continuously validate the initial boundary conditions.
- **Space waste:** Use a rolling <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> if you only require the immediate previous row.

## 27.5. Advanced <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr>

**Definition:** <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> systematically trials possibilities and "reverts" when a solution is invalid, primarily used for constraint satisfaction problems.

### Operations & Complexity

| Problem | Time | Space |
|---------|------|-------|
| N-Queens | <code>O(n!)</code> | <code>O(n)</code> <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> |
| Permutations | <code>O(n!)</code> | <code>O(n)</code> |
| Sudoku | <code>O(9^m)</code> | <code>O(81)</code> |

### Pseudocode

```text
SolveNQueens(n):
    board = n x n grid filled with "."
    result = empty list
    PlaceQueen(row):
        if row == n:
            add board copy to result
            return
        for col from 0 to n-1:
            if IsValid(board, row, col):
                board[row][col] = "Q"
                PlaceQueen(row + 1)
                board[row][col] = "."
    PlaceQueen(0)
    return result
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func solveNQueens(n int) [][]string {
    var result [][]string
    board := make([][]byte, n)
    for i := range board {
        board[i] = make([]byte, n)
        for j := range board[i] {
            board[i][j] = '.'
        }
    }
    var solve func(row int)
    solve = func(row int) {
        if row == n {
            temp := make([]string, n)
            for i := range board {
                temp[i] = string(board[i])
            }
            result = append(result, temp)
            return
        }
        for col := 0; col < n; col++ {
            if isValid(board, row, col, n) {
                board[row][col] = 'Q'
                solve(row + 1)
                board[row][col] = '.'
            }
        }
    }
    solve(0)
    return result
}

func isValid(board [][]byte, row, col, n int) bool {
    for i := 0; i < row; i++ {
        if board[i][col] == 'Q' {
            return false
        }
        if diagCol := col - row + i; diagCol >= 0 && diagCol < n && board[i][diagCol] == 'Q' {
            return false
        }
        if antiCol := col + row - i; antiCol >= 0 && antiCol < n && board[i][antiCol] == 'Q' {
            return false
        }
    }
    return true
}

func main() {
    solutions := solveNQueens(4)
    fmt.Printf("%d solutions for 4-Queens\n", len(solutions))
}
```

{{% alert icon="📌" context="warning" %}}
<abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> can be explosive in execution time. Implement pruning (cutting branches that are demonstrably invalid) to speed up execution.
{{% /alert %}}

### Decision Matrix

| Use <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> When... | Avoid If... |
|-----------------------------|------------------|
| You must enumerate all valid solutions | The solution space is impossibly large |
| Constraints are easy to verify | The problem can be solved with DP/greedy algorithms |

### Edge Cases & Pitfalls

- **No solution:** Always handle scenarios where no valid solution exists.
- **State mutation:** Ensure you perfectly undo any changes after <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> (restore the state).
- **Duplicate solutions:** Employ an ordering logic or a set to prevent yielding duplicates.

## 27.6. Recursive Parallelism

**Definition:** Running recursive sub-problems concurrently using goroutines to dramatically speed up <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> algorithms.

### Operations & Complexity

| Model | Time | Overhead |
|-------|------|----------|
| Sequential | <code>O(T)</code> | 0 |
| Goroutine per sub-problem | <code>O(T/p)</code> | Context switch |
| Worker pool | <code>O(T/p)</code> | More efficient for numerous tasks |

### Pseudocode

```text
ParallelMergeSort(A):
    if length(A) <= 1:
        return A
    if length(A) < threshold:
        return SequentialMergeSort(A)
    mid = length(A) / 2
    left = spawn ParallelMergeSort(A[0:mid])
    right = ParallelMergeSort(A[mid:])
    wait for left
    return Merge(left, right)
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "sync"
)

func parallelMergeSort(arr []int, wg *sync.WaitGroup) []int {
    defer wg.Done()
    if len(arr) <= 1 {
        return arr
    }
    if len(arr) < 1000 {
        return sequentialMergeSort(arr)
    }
    mid := len(arr) / 2
    var left, right []int
    var wgl, wgr sync.WaitGroup
    wgl.Add(1)
    go func() {
        left = parallelMergeSort(arr[:mid], &wgl)
    }()
    wgr.Add(1)
    right = parallelMergeSort(arr[mid:], &wgr)
    wgr.Wait()
    wgl.Wait()
    return merge(left, right)
}

func sequentialMergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    mid := len(arr) / 2
    return merge(sequentialMergeSort(arr[:mid]), sequentialMergeSort(arr[mid:]))
}

func merge(left, right []int) []int {
    result := make([]int, 0, len(left)+len(right))
    i, j := 0, 0
    for i < len(left) && j < len(right) {
        if left[i] < right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }
    result = append(result, left[i:]...)
    result = append(result, right[j:]...)
    return result
}

func main() {
    arr := []int{5, 2, 8, 1, 9, 3, 7, 4, 6}
    var wg sync.WaitGroup
    wg.Add(1)
    sorted := parallelMergeSort(arr, &wg)
    fmt.Println("Parallel sorted:", sorted)
}
```

{{% alert icon="📌" context="warning" %}}
Thresholding is vital for recursive parallelism. Spawning goroutines on tiny sub-problems severely degrades performance due to overhead. Establish a minimum cutoff (e.g., 1000 elements).
{{% /alert %}}

### Decision Matrix

| Use Parallel When... | Avoid If... |
|------------------------|------------------|
| Sub-problems are large and entirely independent | Sub-problems are tiny (< 1000 elements) |
| The problem is CPU-bound | The problem is I/O-bound (use pipelines instead) |

### Edge Cases & Pitfalls

- **Goroutine leak:** Always verify that channels are closed or `defer wg.Done()` is invoked, ideally using `sync.WaitGroup`.
- **Data race:** Goroutines must not write to the identical slice without explicit synchronization.
- **Too many goroutines:** Restrict the count via thresholding or a bounded worker pool.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|-----------|---------|------|-------|----------|
| Factorial | func recursion | <code>O(n)</code> | <code>O(n)</code> stack | Basic example |
| Fibonacci memo | map[int]int | <code>O(n)</code> | <code>O(n)</code> | Classic DP |
| Merge Sort | []int | <code>O(n log n)</code> | <code>O(n)</code> | Stable sorting |
| Quick Sort | []int | <code>O(n log n)</code> avg | <code>O(log n)</code> | In-place sorting |
| Knapsack 0/1 | [][]int | <code>O(nW)</code> | <code>O(nW)</code> | Combinatorial DP |
| N-Queens | <abbr title="Building candidates incrementally and abandoning dead ends">backtracking</abbr> | <code>O(n!)</code> | <code>O(n)</code> | Constraint satisfaction |
| Binary Search | []int | <code>O(log n)</code> | <code>O(1)</code> | Search on sorted |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 26:</strong> This chapter covers advanced recursive algorithms: <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> (<abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">merge sort</abbr>, <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">quick sort</abbr>), recursive data structures (BST), <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr> and <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr> (Fibonacci, knapsack), <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr> (N-Queens), and recursive parallelism with goroutines. Use <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> for naturally dividing problems, <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr> for overlapping sub-problems, and bottom-up <abbr title="A bottom-up dynamic programming technique filling a table iteratively.">tabulation</abbr> for large scales.
{{% /alert %}}

## See Also

- [Chapter 22: <abbr title="An algorithmic paradigm breaking problems into independent subproblems">Divide and Conquer</abbr>](/docs/part-vi/chapter-22/)
- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/part-vi/chapter-23/)
- [Chapter 27: Probabilistic and Randomized Algorithms](/docs/part-vi/chapter-27/)
