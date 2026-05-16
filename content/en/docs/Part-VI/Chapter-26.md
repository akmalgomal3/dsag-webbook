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
<strong>"<em>Recursion reflects problems into simpler versions.</em>" — Brian Kernighan</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Advanced <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> includes <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr>, recursive structures, <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr>, <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr>, and <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr>. 
{{% /alert %}}

## 26.1. Fundamentals of <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr>

**Definition:** <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> calls itself to solve smaller sub-problems. It terminates at a base case.

**Mechanics:**
Functions map complex states to simpler sub-states. Correctness relies on induction.

**Use Cases:**
- Tree Traversals.
- Parsing hierarchical structures (ASTs).
- Orchestrating distributed tasks.

**Memory Management:**
Recursion loads the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>. Go parallel recursion uses goroutines. This shifts load from one deep stack to many shallow 2KB <abbr title="A lightweight concurrent execution thread managed by the Go runtime">goroutine</abbr> stacks. It enables horizontal scaling. Thresholds prevent <abbr title="A lightweight concurrent execution thread managed by the Go runtime">goroutine</abbr> overhead for small sub-problems.

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

### Go Implementation

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
Go lacks tail call optimization. Deep <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> risks overflow. Use <abbr title="The repetition of a process, typically using loops.">iteration</abbr> for extreme depth.
{{% /alert %}}

### Decision Matrix

| Use <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> If... | Avoid If... |
|------------------------|------------------|
| Problem divides naturally | <abbr title="The length of the path from the root to a node.">Depth</abbr> > 10^4 |
| <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> is required | Sub-problems overlap without <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr> |
| <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and conquer</abbr> | Performance requires zero overhead |

### Edge Cases & Pitfalls

- **<abbr title="An error caused by using more stack memory than allocated.">Stack overflow</abbr>:** Excessive <abbr title="The length of the path from the root to a node.">depth</abbr> exceeds bounds.
- **Missing base case:** Function loops infinitely.
- **Redundant computation:** Lack of <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr> repeats sub-problems.

## 26.2. <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr>

**Definition:** Break problem into independent sub-problems. Solve recursively. Combine results.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> | <code>O(n log n)</code> | <code>O(n)</code> | Stable. Divides arrays. |
| <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick Sort</abbr> | <code>O(n log n)</code> avg | <code>O(log n)</code> | In-place. Randomized pivot. |
| <abbr title="A search algorithm that finds the position of a target value within a sorted array.">Binary Search</abbr> | <code>O(log n)</code> | <code>O(1)</code> | Sorted <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> required. |

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

### Go Implementation

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
<abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick Sort</abbr> with deterministic pivot on sorted <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> hits <code>O(n^2)</code>. Random pivot prevents this.
{{% /alert %}}

### Decision Matrix

| Use D&C If... | Avoid If... |
|--------------------|------------------|
| Problem partitions independently | Sub-problems overlap |
| Combining is simpler than direct solution | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> overhead kills performance |

### Edge Cases & Pitfalls

- **Base cases:** Handle single-element arrays immediately.
- **Overflow:** Compute mid using `low + (high-low)/2`.
- **<abbr title="The length of the path from the root to a node.">Depth</abbr>:** <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick Sort</abbr> on <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">linked list</abbr> overflows stack.

## 26.3. Recursive Data Structures

**Definition:** Structures defined in terms of themselves. Examples include linked lists and binary trees.

### Operations & Complexity

| Operation | <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">Linked List</abbr> | <abbr title="A tree data structure in which each node has at most two children.">Binary Tree</abbr> (BST) |
|---------|-------------|-------------------|
| Insert | <code>O(n)</code> | <code>O(log n)</code> balanced |
| Search | <code>O(n)</code> | <code>O(log n)</code> balanced |
| Delete | <code>O(n)</code> | <code>O(log n)</code> balanced |
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

### Go Implementation

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
Go relies on pointers (`*Tree`) and explicit nil checks for recursive structures.
{{% /alert %}}

### Decision Matrix

| Use If... | Avoid If... |
|----------------|------------------|
| Hierarchical relationships exist | Random access dominates |
| Dynamic sizing is required | <abbr title="A variable that stores a memory address.">Pointer</abbr> overhead kills memory |

### Edge Cases & Pitfalls

- **Dangling <abbr title="A variable that stores a memory address.">pointers</abbr>:** Check `nil` before dereference.
- **Cycles:** Avoid unnecessary cyclical designs.
- **Traversal:** Deep trees overflow stacks. Use explicit stack <abbr title="The repetition of a process, typically using loops.">iteration</abbr>.

## 26.4. <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">Memoization</abbr> and <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr>

**Definition:** <abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">Memoization</abbr> caches results. <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr> breaks down sub-problems into tables.

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

### Go Implementation

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
Top-down <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> risks <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr> for n > 10^5. Bottom-up handles massive scales.
{{% /alert %}}

### Decision Matrix

| Use Top-down If... | Use Bottom-up If... |
|-------------------------|--------------------------|
| Sub-problems skip evaluation | Sub-problems demand evaluation |
| Logic remains natural | Space optimization matters |
| n remains small | n grows large |

### Edge Cases & Pitfalls

- **Overflow:** Fibonacci exceeds `int64` at n=93. Use `math/big`.
- **Base cases:** Validate boundaries.
- **Memory waste:** Rolling arrays reduce space for previous-row dependencies.

## 26.5. Advanced <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr>

**Definition:** <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> trials possibilities and reverts upon invalidity. Built for constraint satisfaction.

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

### Go Implementation

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
<abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> explodes in time. Pruning stops invalid branches early.
{{% /alert %}}

### Decision Matrix

| Use <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> If... | Avoid If... |
|-----------------------------|------------------|
| Enumeration is required | Solution space explodes |
| Constraints evaluate fast | DP or greedy succeeds |

### Edge Cases & Pitfalls

- **No solution:** Handle impossible cases.
- **State mutation:** Restore state perfectly after <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>.
- **Duplicates:** Track sets to avoid repetition.

## 26.6. Recursive Parallelism

**Definition:** Concurrent <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> using goroutines.

### Operations & Complexity

| Model | Time | Overhead |
|-------|------|----------|
| Sequential | <code>O(T)</code> | 0 |
| Goroutine per sub-problem | <code>O(T/p)</code> | Context switch |
| Worker pool | <code>O(T/p)</code> | High task efficiency |

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

### Go Implementation

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
Thresholding limits <abbr title="A lightweight concurrent execution thread managed by the Go runtime">goroutine</abbr> overhead. Execute small sub-problems sequentially.
{{% /alert %}}

### Decision Matrix

| Use Parallel If... | Avoid If... |
|------------------------|------------------|
| Sub-problems divide independently | Sub-problems remain tiny |
| Execution is CPU-bound | Execution is I/O-bound |

### Edge Cases & Pitfalls

- **Goroutine leaks:** Synchronize with `sync.WaitGroup`.
- **Data races:** Avoid concurrent slice writes.
- **Excessive concurrency:** Bound execution with thresholds or worker pools.

### Anti-Patterns

- **Stack overflow:** Deep recursion panics. Convert to iteration.
- **Closure capture:** Loop variables leak by reference. Pass them as arguments.
- **Redundant recomputation:** Unmemoized recursion recalculates overlap exponentially. Cache results.

## 26.7. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|-----------|---------|------|-------|----------|
| Factorial | func | <code>O(n)</code> | <code>O(n)</code> | Basic |
| Fibonacci memo | map[int]int | <code>O(n)</code> | <code>O(n)</code> | DP |
| Merge Sort | []int | <code>O(n log n)</code> | <code>O(n)</code> | Stable sorting |
| Quick Sort | []int | <code>O(n log n)</code> avg | <code>O(log n)</code> | In-place sorting |
| Knapsack 0/1 | [][]int | <code>O(nW)</code> | <code>O(nW)</code> | Combinatorial DP |
| N-Queens | <abbr title="Building candidates incrementally and abandoning dead ends">backtracking</abbr> | <code>O(n!)</code> | <code>O(n)</code> | Constraint |
| Binary Search | []int | <code>O(log n)</code> | <code>O(1)</code> | Sorted search |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Advanced <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> implements <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr>, <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr>, <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr>, and parallelism. Caching stops redundancy. Thresholds stop overhead.
{{% /alert %}}

## See Also

- [Chapter 22: <abbr title="An algorithmic paradigm breaking problems into independent subproblems">Divide and Conquer</abbr>](/docs/part-vi/chapter-22/)
- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/part-vi/chapter-23/)
- [Chapter 27: Probabilistic and Randomized Algorithms](/docs/part-vi/chapter-27/)
