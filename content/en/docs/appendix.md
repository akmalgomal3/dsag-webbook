---
weight: 9000
title: "Appendix"
description: "Supplementary Material"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

This appendix contains supplementary material from chapters that were integrated into other sections.

---

## Big-O Cheat Sheet

Quick reference for time and space complexity of common data structures and algorithms.

### Data Structures

| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
| Dynamic Array (Slice) | O(1) | O(n) | O(1) amortized | O(n) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Table |: | O(1) avg | O(1) avg | O(1) avg | O(n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Heap | O(n) | O(n) | O(log n) | O(log n) | O(n) |
| Trie | O(m) | O(m) | O(m) | O(m) | O(n·m) |
| Segment Tree | O(log n) |: | O(log n) | O(log n) | O(n) |
| B-Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Skip List | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Bloom Filter |: | O(k) | O(k) |: | O(n) |

### Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| Radix Sort | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes |
| Bucket Sort | O(n) | O(n) | O(n²) | O(n) | Yes |

### Graph Algorithms

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
| DFS | O(V + E) | O(V) | Connectivity, cycles |
| Dijkstra | O((V + E) log V) | O(V) | Shortest path (weighted, no negatives) |
| Bellman-Ford | O(V·E) | O(V) | Shortest path (with negatives) |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
| Kruskal | O(E log E) | O(V) | MST |
| Prim | O((V + E) log V) | O(V) | MST |
| Topological Sort | O(V + E) | O(V) | Dependency ordering |
| A* | O(E) | O(V) | Pathfinding with heuristic |

### Array/String Techniques

| Technique | Time | Space | Use Case |
|-----------|------|-------|----------|
| Two Pointers | O(n) | O(1) | Sorted pair search |
| Sliding Window | O(n) | O(1) | Subarray/substring problems |
| Kadane's Algorithm | O(n) | O(1) | Maximum subarray |
| Prefix Sum | O(n) preprocessing, O(1) query | O(n) | Range sum queries |
| Mo's Algorithm | O((n + q)√n) | O(n) | Offline range queries |

---

## Section 1


{{% alert icon="💡" context="info" %}}
<strong>"<em>The art of programming is the skill of controlling complexity.</em>": Marijn Haverbeke</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 16 focuses on the Design of Algorithms and Running Times, evaluating algorithms theoretically and empirically, and exploring how to effectively <abbr title="A test used to compare the performance of computer hardware or software.">benchmark</abbr> and profile algorithmic execution in Go.
{{% /alert %}}

## 16.1. Understanding Algorithmic Complexity

**Definition:** Algorithmic complexity measures the growth of time or space required as a function of the input size n, using <abbr title="A mathematical notation describing the limiting behavior of a function when the argument tends towards a particular value or infinity.">Big-O</abbr>, <abbr title="A mathematical notation describing the lower bound of an algorithm's growth rate.">Big-Ω</abbr>, and <abbr title="A mathematical notation describing the tight bound of an algorithm's growth rate.">Big-Θ</abbr> notations.

### Operations & Complexity

| Notation | Definition | Characteristic |
|--------|----------|---------------|
| Big-O | <abbr title="A function that grows at least as fast as the given function.">Upper bound</abbr> | <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">Worst-case</abbr> guarantee |
| Big-Ω | <abbr title="A function that grows no faster than the given function.">Lower bound</abbr> | <abbr title="The minimum runtime or resource usage of an algorithm over all possible inputs.">Best-case</abbr> scenario |
| Big-Θ | <abbr title="A function that grows at the same rate as the given function, both upper and lower.">Tight bound</abbr> | Upper = Lower |

### Pseudocode

```text
benchmarkSort(n):
    data = array of n random integers
    start = current time
    sort data in ascending order
    return elapsed time
```

### Idiomatic Go Implementation

<abbr title="A test used to compare the performance of computer hardware or software.">Benchmark</abbr> to measure growth rate:

```go
package main

import (
	"fmt"
	"math/rand"
	"sort"
	"time"
)

func benchmarkSort(n int) time.Duration {
	data := make([]int, n)
	for i := range data {
		data[i] = rand.Intn(n * 10)
	}
	start := time.Now()
	sort.Ints(data)
	return time.Since(start)
}

func main() {
	for _, n := range []int{1000, 10000, 100000} {
		fmt.Printf("n=%d: %v\n", n, benchmarkSort(n))
	}
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Need theoretical guarantees | Quick prototyping without analysis |
| Comparing algorithms | Input size is always small and constant |
| Communicating complexity to the team | Over-engineering for n < 100 |

### Edge Cases & Pitfalls
- **Case hidden constants:** An algorithm with better asymptotic complexity but a large constant can be slower than `O(n log n)` for practical n.
- **Case average vs worst:** Quick sort is `O(n²)` worst-case but `O(n log n)` average; consider a randomized pivot.
- **Case space complexity:** Recursion depth can consume `O(n)` stack space; consider an iterative version.

## 16.2. Algorithm Design Techniques

**Definition:** Algorithm design techniques—divide and conquer, dynamic programming, greedy, backtracking, and randomized—provide strategies to solve problems with optimal efficiency.

### Operations & Complexity

| Technique | Strategy | Example | Time | Space |
|--------|----------|--------|------|-------|
| Divide and Conquer | Divide, solve, merge | Merge sort | `O(n log n)` | `O(n)` |
| Dynamic Programming | Subproblem + memo | Fibonacci DP | `O(n)` | `O(n)` |
| Greedy | Local optimal | Activity selection | `O(n log n)` | `O(n)` |
| Backtracking | DFS + prune | N-Queens | `O(n!)` worst | `O(n)` |
| Randomized | Random choice | Randomized quicksort | `O(n log n)` expected | `O(log n)` |

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Overlapping subproblems (DP) | Independent subproblems (DnC is simpler) |
| Greedy choice property is proven | Need global optimal without proof |
| Backtracking for constraint satisfaction | Solution space is too large without pruning |
| Randomized to avoid worst-case | Deterministic output is required |

### Edge Cases & Pitfalls
- **Case DP table initialization:** Forgetting to initialize base cases leads to incorrect results.
- **Case greedy counter-example:** Greedy coin change with arbitrary denominations is not optimal.
- **Case backtracking explosion:** Without pruning, backtracking degenerates to brute force.
- **Case randomized seed:** Forgetting to seed causes the same random sequence on every run.

## 16.3. Measuring and Optimizing Performance

**Definition:** Performance measurement in Go utilizes benchmarks, profiling, and optimization techniques like cache efficiency, loop unrolling, and parallelization.

### Operations & Complexity

| Tool/Technique | Command | Usage |
|-------------|----------|----------|
| Benchmark | `go test -bench=.` | Measure throughput |
| CPU Profile | `go tool pprof cpu.prof` | Hotspot detection |
| Memory Profile | `go tool pprof mem.prof` | Allocation tracking |
| Trace | `go tool trace trace.out` | Goroutine visualization |
| Inlining | Compiler auto | Reduce call overhead |

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Need empirical evidence | Premature optimization without profiling |
| Bottlenecks are identified | Optimization sacrifices readability |
| Parallelism helps (CPU-bound) | Synchronization overhead > speedup |

### Edge Cases & Pitfalls
- **Case premature optimization:** Profile first, optimize later.
- **Case <abbr title="A test used to compare the performance of computer hardware or software.">benchmark</abbr> noise:** Use `-count=5` and `benchstat` for statistical significance.
- **Case pprof sampling:** CPU profiler is sampling-based; small hotspots might be missed.
- **Case false sharing:** Parallel access to adjacent variables in a <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> line causes invalidation.

## 16.4. The Role of Data Structures in Algorithm Efficiency

**Definition:** Appropriate data structures can reduce algorithm complexity from <code>O(n)</code> to <code>O(log n)</code> or <code>O(1)</code>; the choice depends on access patterns and dominant operations.

### Operations & Complexity

| Structure | Dominant Operation | Complexity | Use Case |
|----------|-----------------|--------------|----------|
| <abbr title="A data structure that implements an associative array using a hash function.">Hash Table</abbr> | Search/Insert/Delete | <code>O(1)</code> avg | Caching, indexing |
| Balanced BST | Ordered ops | <code>O(log n)</code> | Range queries, order stats |
| <abbr title="A specialized tree-based data structure that satisfies the heap property.">Heap</abbr> | Min/Max access | <code>O(1)</code> peek, <code>O(log n)</code> push/pop | <abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority queue</abbr> |
| <abbr title="A tree-like data structure used to store a dynamic set of strings.">Trie</abbr> | Prefix search | <code>O(L)</code> | Autocomplete |
| <abbr title="A tree data structure for storing intervals or segments, allowing range queries.">Segment Tree</abbr> | Range query | <code>O(log n)</code> | Range sum/min |

### Pseudocode

```text
trieInsert(root, word):
    node = root
    for each character in word:
        if character not in node.children:
            create new child node
        node = node.children[character]
    node.isEnd = true

trieSearch(root, word):
    node = root
    for each character in word:
        if character not in node.children:
            return false
        node = node.children[character]
    return node.isEnd
```

### Idiomatic Go Implementation

<abbr title="A tree-like data structure used to store a dynamic set of strings.">Trie</abbr> for prefix search:

```go
package main

import "fmt"

type TrieNode struct {
	children map[rune]*TrieNode
	isEnd    bool
}

func (t *TrieNode) Insert(word string) {
	node := t
	for _, ch := range word {
		if node.children == nil {
			node.children = make(map[rune]*TrieNode)
		}
		if node.children[ch] == nil {
			node.children[ch] = &TrieNode{}
		}
		node = node.children[ch]
	}
	node.isEnd = true
}

func (t *TrieNode) Search(word string) bool {
	node := t
	for _, ch := range word {
		if node.children[ch] == nil {
			return false
		}
		node = node.children[ch]
	}
	return node.isEnd
}

func main() {
	root := &TrieNode{}
	root.Insert("go")
	fmt.Println(root.Search("go"))
	fmt.Println(root.Search("golang"))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Frequent lookup by <abbr title="A field or set of fields used to identify a record.">key</abbr> | Ordered <abbr title="The repetition of a process, typically using loops.">iteration</abbr> is required (maps are not ordered) |
| Ordered range queries | Avg <code>O(1)</code> lookup is the absolute priority |
| Prefix matching | Memory is strictly limited (tries are memory-heavy) |

### Edge Cases & Pitfalls
- **Case map <abbr title="The repetition of a process, typically using loops.">iteration</abbr> order:** Maps are not ordered; use a slice of keys for deterministic <abbr title="The repetition of a process, typically using loops.">iteration</abbr>.
- **Case <abbr title="A tree-like data structure used to store a dynamic set of strings.">trie</abbr> memory:** Tries can be very memory inefficient for sparse data.
- **Case balanced <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr>:** Self-balancing trees (AVL/Red-Black) require manual implementation in Go.
- **Case <abbr title="A tree data structure for storing intervals or segments, allowing range queries.">segment tree</abbr> size:** Segment trees require 4*n space; be careful with large n.

## 16.5. Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Complexity analysis | Manual / <abbr title="A mathematical notation describing the limiting behavior of a function when the argument tends towards a particular value or infinity.">Big-O</abbr> | varies |: | Worst, avg, best analysis |
| <abbr title="The process of arranging elements in a specific order.">Sorting</abbr> | `sort` package | <code>O(n log n)</code> |: | Ints, Strings, Slice |
| <abbr title="The process of finding a specific element in a data structure.">Searching</abbr> | `sort.Search` | <code>O(log n)</code> |: | <abbr title="A search algorithm that finds the position of a target value within a sorted array.">Binary search</abbr> (requires sorted) |
| DP table | `[]T` 2D slice | varies | varies | Bottom-up approach |
| <abbr title="A specialized tree-based data structure that satisfies the heap property.">Heap</abbr> | `container/heap` | <code>O(log n)</code> ops |: | Implement 5 methods |
| <abbr title="A tree-like data structure used to store a dynamic set of strings.">Trie</abbr> | custom struct | <code>O(L)</code> | varies | Prefix search |
| <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr> | `map[T][]T` | <code>O(V+E)</code> | <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">Adjacency list</abbr> |
| Profile | `pprof` |: | CPU, memory, goroutine |
| <abbr title="A test used to compare the performance of computer hardware or software.">Benchmark</abbr> | `testing.B` |: | Built-in |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 16:</strong> This chapter focuses on algorithm design techniques and complexity analysis using Big-O, Big-Ω, and Big-Θ notations. It covers <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr>, <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr>, greedy algorithms, and <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr>, along with performance measurement tools and the critical role of selecting efficient data structures.
{{% /alert %}}

---

## Section 2


{{% alert icon="💡" context="info" %}}
<strong>"<em>The best algorithm designers understand the underlying principles that govern efficient problem-solving.</em>": Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 18 focuses on Algorithm Design Techniques, diving into overlapping sub-problems and optimal substructures. It compares various design philosophies to tackle complex computational limits.
{{% /alert %}}

## 18.1. Introduction to Algorithm Design

**Definition:** Algorithm design is the process of selecting appropriate strategies to solve computational problems efficiently, balancing time and <abbr title="A computational complexity that describes the amount of memory space taken by an algorithm.">space complexity</abbr> based on problem characteristics.

### Operations & Complexity

| Aspect | Complexity | Description |
|-------|--------------|------------|
| <abbr title="A straightforward approach trying all possible solutions.">Brute Force</abbr> | <code>O(n!)</code> / <code>O(2^n)</code> | Check all possibilities |
| <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr> | <code>O(n log n)</code> - <code>O(n^{2})</code> | Divide, solve, combine |
| <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr> | <code>O(n)</code> - <code>O(n^{2})</code> | Store subproblem results |
| Greedy | <code>O(n log n)</code> | Make locally optimal choices |
| <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> | <code>O(2^n)</code> exponential | Exploration with pruning |

### Decision Matrix

| Use This Technique When... | Avoid If... |
|---------------------------|------------------|
| Independent subproblems → <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr> | Subproblems overlap |
| Overlapping subproblems → DP | No optimal substructure |
| Greedy-choice property → Greedy | Exact solution required and greedy fails |
| Constraint satisfaction → <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> | Search space is too large without pruning |

### Edge Cases & Pitfalls

- **Empty input:** Always validate `len(input) == 0` before processing.
- **<abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> overflow:** Go does not optimize tail <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>; use <abbr title="The repetition of a process, typically using loops.">iteration</abbr> for very deep calls.
- **Wrong technique choice:** <abbr title="A straightforward approach trying all possible solutions.">Brute force</abbr> on large inputs will cause timeouts.

## 18.2. <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr>

**Definition:** Break the problem into smaller subproblems, solve them recursively, and combine the results.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Divide | <code>O(1)</code> | Split <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> in the middle |
| Conquer | <code>T(n/2)</code> | Recurse on subarray |
| Combine | <code>O(n)</code> | Merge sorted results |
| Total (<abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr>) | <code>O(n log n)</code> | All cases |

### Pseudocode

```text
MergeSort(arr):
    if length(arr) <= 1:
        return arr
    mid = length(arr) / 2
    left = MergeSort(arr[0:mid])
    right = MergeSort(arr[mid:end])
    return Merge(left, right)

Merge(left, right):
    result = empty list
    while left and right not empty:
        append smaller front element to result
    append remaining elements
    return result
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

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
        if left[i] <= right[j] {
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
    arr := []int{38, 27, 43, 3, 9, 82, 10}
    fmt.Println(mergeSort(arr))
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Problem can be split independently | Subproblems overlap (choose DP instead) |
| Stable <abbr title="The process of arranging elements in a specific order.">sorting</abbr> is needed | Memory is limited (in-place QuickSort is better) |
| Data is large and parallelizable | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> overhead is more expensive than <abbr title="The repetition of a process, typically using loops.">iteration</abbr> |

### Edge Cases & Pitfalls

- **Empty <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>:** The base case `len(arr) <= 1` handles this.
- **<abbr title="The process of reserving a partial or complete portion of computer memory for the execution of programs.">Memory allocation</abbr>:** <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> requires <code>O(n)</code> extra space; for limited memory, use in-place QuickSort.
- **<abbr title="An error caused by using more stack memory than allocated.">Stack overflow</abbr>:** On extremely large arrays, deep <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> can cause stack overflows in Go.

## 18.3. <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr>

**Definition:** DP solves problems by breaking them down into overlapping subproblems, storing results to avoid redundant calculations.

### Operations & Complexity

| Approach | Time | Space | Description |
|------------|-------|-------|------------|
| Top-down (<abbr title="A dynamic programming technique storing the results of expensive function calls and returning cached results.">memoization</abbr>) | <code>O(n)</code> | <code>O(n)</code> <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> + memo | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> + <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> |
| Bottom-up (<abbr title="A bottom-up dynamic programming technique filling a table iteratively.">tabulation</abbr>) | <code>O(n)</code> | <code>O(n)</code> | <abbr title="The repetition of a process, typically using loops.">Iteration</abbr> + <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> |
| Space-optimized | <code>O(n)</code> | <code>O(1)</code> | Only store the last states |

### Pseudocode

```text
FibonacciMemo(n, memo):
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = FibonacciMemo(n-1, memo) + FibonacciMemo(n-2, memo)
    return memo[n]

Knapsack(W, weights, values):
    dp = 2D array of size (n+1) x (W+1) filled with 0
    for i from 1 to n:
        for w from 0 to W:
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func fibMemo(n int, memo map[int]int) int {
    if n <= 1 {
        return n
    }
    if v, ok := memo[n]; ok {
        return v
    }
    memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo)
    return memo[n]
}

func fibBottomUp(n int) int {
    if n <= 1 {
        return n
    }
    a, b := 0, 1
    for i := 2; i <= n; i++ {
        a, b = b, a+b
    }
    return b
}

func main() {
    fmt.Println(fibMemo(10, make(map[int]int)))
    fmt.Println(fibBottomUp(10))
}
```

```go
package main

import "fmt"

func knapsack(w int, weights, values []int) int {
    n := len(weights)
    dp := make([][]int, n+1)
    for i := range dp {
        dp[i] = make([]int, w+1)
    }
    for i := 1; i <= n; i++ {
        for j := 0; j <= w; j++ {
            if weights[i-1] <= j {
                dp[i][j] = max(values[i-1]+dp[i-1][j-weights[i-1]], dp[i-1][j])
            } else {
                dp[i][j] = dp[i-1][j]
            }
        }
    }
    return dp[n][w]
}

func main() {
    weights := []int{1, 2, 3}
    values := []int{6, 10, 12}
    fmt.Println(knapsack(5, weights, values))
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Overlapping subproblems exist | Independent subproblems (<abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> is simpler) |
| Optimal substructure is present | No optimal structure |
| Exact solution is needed | Greedy is proven optimal and faster |

### Edge Cases & Pitfalls

- **Memo initialization:** Do not forget to initialize the map/slice before use.
- **<abbr title="A data structure that improves the speed of data retrieval operations.">Index</abbr> off-by-one:** DP tables often use the <abbr title="A data structure that improves the speed of data retrieval operations.">index</abbr> <code>i-1</code> for the <code>i</code>-th item.
- **Space bloat:** For large <code>n</code>, use space optimization with a rolling <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>.

## 18.4. Greedy Algorithms

**Definition:** Greedy algorithms build a solution by making the locally optimal choice at each step, hoping to reach the global optimum.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|-------|-------|------------|
| Activity Selection | <code>O(n log n)</code> | <code>O(1)</code> | Sort by finish time |
| Dijkstra | <code>O((V+E) \log V)</code> | <code>O(V)</code> | <abbr title="A queue where each element has a priority and the highest priority element is served first.">Priority queue</abbr> |
| Huffman Coding | <code>O(n log n)</code> | <code>O(n)</code> | <abbr title="A heap where the parent node is less than or equal to its children.">Min-heap</abbr> |

### Pseudocode

```text
Dijkstra(graph, start):
    dist = array of infinity
    dist[start] = 0
    minHeap = [(start, 0)]
    while minHeap not empty:
        (u, d) = pop minHeap
        if d > dist[u]: continue
        for each edge (u, v, w):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                push (v, dist[v]) to minHeap
    return dist
```

### Idiomatic Go Implementation

```go
package main

import (
    "container/heap"
    "fmt"
)

type Edge struct {
    to     int
    weight int
}

type Item struct {
    node int
    dist int
}

type MinHeap []Item

func (h MinHeap) Len() int            { return len(h) }
func (h MinHeap) Less(i, j int) bool  { return h[i].dist < h[j].dist }
func (h MinHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x interface{}) { *h = append(*h, x.(Item)) }
func (h *MinHeap) Pop() interface{} {
    old := *h
    n := len(old)
    *h = old[:n-1]
    return old[n-1]
}

func dijkstra(graph [][]Edge, start int) []int {
    n := len(graph)
    dist := make([]int, n)
    for i := range dist {
        dist[i] = int(^uint(0) >> 1)
    }
    dist[start] = 0
    h := &MinHeap{{start, 0}}
    heap.Init(h)
    for h.Len() > 0 {
        item := heap.Pop(h).(Item)
        if item.dist > dist[item.node] {
            continue
        }
        for _, e := range graph[item.node] {
            if d := item.dist + e.weight; d < dist[e.to] {
                dist[e.to] = d
                heap.Push(h, Item{e.to, d})
            }
        }
    }
    return dist
}

func main() {
    graph := [][]Edge{
        {{1, 4}, {2, 1}},
        {{3, 1}},
        {{1, 2}, {3, 5}},
        {},
    }
    fmt.Println(dijkstra(graph, 0))
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Greedy-choice property is proven | Exact solution is needed and greedy is unproven |
| Optimal substructure exists | Local choices don't lead to global optimum (e.g., 0/1 Knapsack) |
| Need a fast, near-optimal solution | Approximation ratio doesn't meet requirements |

### Edge Cases & Pitfalls

- **Negative weights:** Dijkstra fails with negative edges; use Bellman-Ford.
- **Unproven optimality:** Always verify the greedy-choice property before using.
- **Empty <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr>:** Ensure the <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> isn't disconnected or handle unreachable nodes.

## 18.5. <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> and Branch-and-Bound

**Definition:** <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> explores solutions incrementally and backtracks if a constraint is violated. Branch-and-Bound adds pruning based on bounds for optimization.

### Operations & Complexity

| Technique | Time | Space | Description |
|--------|-------|-------|------------|
| <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> | <code>O(2^n)</code> / <code>O(n!)</code> | <code>O(n)</code> <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> | DFS exploration |
| Branch-and-Bound | <code>O(2^n)</code> worst | <code>O(n)</code> | Pruning with bounds |

### Pseudocode

```text
SolveNQueens(board, row):
    n = size(board)
    if row == n:
        return true
    for col from 0 to n-1:
        if IsSafe(board, row, col):
            board[row][col] = true
            if SolveNQueens(board, row+1):
                return true
            board[row][col] = false
    return false

IsSafe(board, row, col):
    check column and diagonals above
    return true if no queen attacks
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func isSafe(board [][]bool, row, col int) bool {
    for i := 0; i < row; i++ {
        if board[i][col] {
            return false
        }
        if d := row - i; col-d >= 0 && board[i][col-d] {
            return false
        }
        if d := row - i; col+d < len(board) && board[i][col+d] {
            return false
        }
    }
    return true
}

func solveNQueens(board [][]bool, row int) bool {
    n := len(board)
    if row == n {
        return true
    }
    for col := 0; col < n; col++ {
        if isSafe(board, row, col) {
            board[row][col] = true
            if solveNQueens(board, row+1) {
                return true
            }
            board[row][col] = false
        }
    }
    return false
}

func main() {
    n := 8
    board := make([][]bool, n)
    for i := range board {
        board[i] = make([]bool, n)
    }
    if solveNQueens(board, 0) {
        for _, r := range board {
            for _, c := range r {
                if c {
                    fmt.Print("Q ")
                } else {
                    fmt.Print(". ")
                }
            }
            fmt.Println()
        }
    }
}
```

```go
package main

import "fmt"

func tsp(graph [][]int, curr int, visited map[int]bool, cost, start int) int {
    if len(visited) == len(graph) {
        return cost + graph[curr][start]
    }
    minCost := int(^uint(0) >> 1)
    for next := 0; next < len(graph); next++ {
        if !visited[next] {
            visited[next] = true
            if c := tsp(graph, next, visited, cost+graph[curr][next], start); c < minCost {
                minCost = c
            }
            delete(visited, next)
        }
    }
    return minCost
}

func main() {
    graph := [][]int{
        {0, 10, 15, 20},
        {10, 0, 35, 25},
        {15, 35, 0, 30},
        {20, 25, 30, 0},
    }
    visited := map[int]bool{0: true}
    fmt.Println(tsp(graph, 0, visited, 0, 0))
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Need all valid solutions | Need an optimal solution and search space is too large |
| Constraint propagation is effective | No significant pruning is possible |
| Branch-and-Bound: need tight bounds | Bounds are too loose → no pruning happens |

### Edge Cases & Pitfalls

- **<abbr title="An error caused by using more stack memory than allocated.">Stack overflow</abbr>:** Large <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> depths can cause stack overflows.
- **State mutation:** Ensure <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr> restores the state (unmarks) correctly.
- **Map as visited:** In Go, maps are <abbr title="A value that enables a program to indirectly access a particular datum.">reference</abbr> types; make sure to copy them if necessary.

## 18.6. Problem Reduction and Transformations

**Definition:** Problem reduction transforms a complex problem into another problem that already has an efficient solution, then maps the solution back to the original problem.

### Operations & Complexity

| Aspect | Complexity | Description |
|-------|--------------|------------|
| Transformation | <code>O(n)</code> - <code>O(n^{2})</code> | Depends on the problem |
| Target solution | Per target algorithm | E.g., TSP <code>O(n^2 2^n)</code> |
| Inverse mapping | <code>O(n)</code> | Convert solution back to original form |

### Pseudocode

```text
HamiltonianToTSP(graph):
    n = size(graph)
    tsp = n x n matrix
    for i from 0 to n-1:
        for j from 0 to n-1:
            if i == j:
                tsp[i][j] = 0
            else if graph[i][j]:
                tsp[i][j] = 1
            else:
                tsp[i][j] = infinity
    return tsp
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func hamiltonianToTSP(graph [][]bool) ([][]int, bool) {
    n := len(graph)
    tsp := make([][]int, n)
    inf := int(^uint(0) >> 1)
    for i := range tsp {
        tsp[i] = make([]int, n)
        for j := range tsp[i] {
            if i == j {
                tsp[i][j] = 0
            } else if graph[i][j] {
                tsp[i][j] = 1
            } else {
                tsp[i][j] = inf
            }
        }
    }
    return tsp, true
}

func main() {
    graph := [][]bool{
        {false, true, true, false},
        {true, false, true, true},
        {true, true, false, false},
        {false, true, false, false},
    }
    tsp, ok := hamiltonianToTSP(graph)
    if ok {
        fmt.Println("TSP graph:", tsp)
    }
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Original problem is hard, target has a solution | Transformation overhead is more expensive than a direct solution |
| Need complexity proofs (NP-Completeness) | Target problem also lacks an efficient solution |

### Edge Cases & Pitfalls

- **Transformation cost:** Ensure transformation cost does not exceed direct solution cost.
- **Solution preservation:** Verify that the target solution maps back to a valid original solution.
- **Precision loss:** Numeric transformations might lose precision.

### Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr> | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> | <code>O(n log n)</code> | varies | <abbr title="The process of arranging elements in a specific order.">Sorting</abbr>, FFT, closest pair |
| <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr> | DP table | <code>O(n)</code> - <code>O(n^2)</code> | varies | Knapsack, LCS, shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> |
| Greedy | Local choice | <code>O(n log n)</code> | varies | Dijkstra, Huffman, MST |
| <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr> | DFS + pruning | Exponential | varies | N-Queens, Sudoku |
| Branch-and-Bound | Optimization + bounds | Exponential (bounded) | varies | TSP, integer programming |
| Problem Reduction | Transform | Varies | varies | NP-Completeness proofs |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 18:</strong> This chapter covers core algorithm design techniques including <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr>, <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">Dynamic Programming</abbr>, Greedy Algorithms, <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr>, Branch-and-Bound, and Problem Reduction. It provides idiomatic Go implementations, complexity analysis, and decision matrices to help you choose the right technique based on problem characteristics such as overlapping subproblems, optimal substructure, and constraint satisfaction.
{{% /alert %}}

---

## Section 3


{{% alert icon="💡" context="info" %}}
<strong>"<em>The great thing about graphs is that they give us a way to think about the world in a very powerful and abstract way, which can then be applied to many practical problems.</em>": Donald E. Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 19 focuses on <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr> Traversal Algorithms (DFS, BFS, IDDFS). It elevates implementations using Go 1.18+ Generics to traverse graphs containing Strings, UUIDs, or custom Structs, as required in modern production environments.
{{% /alert %}}

## 19.1. Generic <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr> Representation

**Definition:** In academic settings, graphs are often represented as `[][]int` (adjacency matrices or lists). However, in real-world systems, nodes are rarely sequential integers; they are IDs, usernames, or IPs. 

We represent a modern Go sparse <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> as an <abbr title="A collection of lists representing a graph, where each list describes the neighbors of a vertex.">adjacency list</abbr> utilizing a generic `map[T][]T`.

### Idiomatic Go 1.18+ Generic <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr>

```go
package main

import "fmt"

// Graph is a generic adjacency list where nodes can be any comparable type.
type Graph[T comparable] struct {
	Adj map[T][]T
}

func NewGraph[T comparable]() *Graph[T] {
	return &Graph[T]{
		Adj: make(map[T][]T),
	}
}

// AddEdge inserts a directed edge. Call it twice for undirected graphs.
func (g *Graph[T]) AddEdge(u, v T) {
	g.Adj[u] = append(g.Adj[u], v)
	
	// Ensure the destination node exists in the map to prevent panics during iteration
	if _, exists := g.Adj[v]; !exists {
		g.Adj[v] = []T{}
	}
}

func main() {
	g := NewGraph[string]()
	g.AddEdge("Alice", "Bob")
	g.AddEdge("Alice", "Charlie")
	fmt.Println("Alice's connections:", g.Adj["Alice"])
}
```

### Edge Cases & Pitfalls
- **Memory Overhead:** A `map[T][]T` carries a heavier memory footprint than a raw `[][]int`. If your nodes *are* guaranteed to be sequential, densely packed integers starting from 0, a slice-of-slices remains computationally superior.

## 19.2. <abbr title="A graph traversal algorithm that explores as far as possible along each branch before backtracking.">Depth-First Search</abbr> (DFS)

**Definition:** DFS explores a <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> as deeply as possible along each branch before <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr>, utilizing a <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr>.

### Idiomatic Go 1.18+ Iterative DFS

We rigorously avoid <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> for DFS in Go to categorically eliminate the risk of a <abbr title="An error caused by using more stack memory than allocated.">Stack Overflow</abbr> panic on exceptionally deep graphs.

```go
package main

import "fmt"

type Graph[T comparable] struct {
	Adj map[T][]T
}

// DFSIterative executes a depth-first search and returns the visitation order.
func (g *Graph[T]) DFSIterative(start T) []T {
	visited := make(map[T]bool)
	var stack []T
	var order []T

	// Initialize
	stack = append(stack, start)

	for len(stack) > 0 {
		// Pop the top of the stack
		v := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		if visited[v] {
			continue
		}

		visited[v] = true
		order = append(order, v)

		// Push neighbors onto the stack
		// Note: Iterating a map is randomized in Go. 
		// If deterministic order is required, you must sort the neighbors here.
		for _, neighbor := range g.Adj[v] {
			if !visited[neighbor] {
				stack = append(stack, neighbor)
			}
		}
	}
	return order
}
```

### Decision Matrix

| Use DFS When... | Avoid If... |
|-------------------|------------------|
| Need <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">backtracking</abbr> capabilities (e.g., Maze solving) | Graphs are exceedingly deep and you are using <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> |
| Generating a <abbr title="A linear ordering of vertices such that for every directed edge uv, u comes before v.">Topological Sort</abbr> | Finding the shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> (DFS wanders blindly) |

## 19.3. <abbr title="A graph traversal algorithm that explores neighbors level by level.">Breadth-First Search</abbr> (BFS)

**Definition:** BFS explores a <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> <abbr title="The set of all nodes at a given depth.">level</abbr> by <abbr title="The set of all nodes at a given depth.">level</abbr> using a <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr>. It is the absolute ideal algorithm for locating the shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> within an <abbr title="A graph where edges have no associated weight.">unweighted graph</abbr>.

### Idiomatic Go 1.18+ Generic BFS

```go
package main

import "fmt"

// BFS executes a breadth-first search, returning both the visitation order
// and a map detailing the shortest distance from the start node.
func (g *Graph[T]) BFS(start T) ([]T, map[T]int) {
	visited := make(map[T]bool)
	dist := make(map[T]int)
	var queue []T
	var order []T

	// Initialize
	queue = append(queue, start)
	visited[start] = true
	dist[start] = 0

	for len(queue) > 0 {
		// Dequeue (Note: Naive slice shifting `queue[1:]` is used here for brevity,
		// but a Circular Buffer should be used in heavy production to prevent memory leaks).
		v := queue[0]
		queue = queue[1:]

		order = append(order, v)

		for _, neighbor := range g.Adj[v] {
			if !visited[neighbor] {
				visited[neighbor] = true
				dist[neighbor] = dist[v] + 1
				queue = append(queue, neighbor)
			}
		}
	}
	return order, dist
}
```

### Decision Matrix

| Use BFS When... | Avoid If... |
|-------------------|------------------|
| Need unweighted shortest paths | Weighted graphs: use Dijkstra instead |
| Level-order traversal | Memory is extremely limited on very wide graphs (<abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr> bloat) |

## 19.4. Advanced Traversal Techniques

### 21.4.1. Bidirectional Search

**Definition:** A search that runs simultaneously from both the start and the goal until they physically intersect, significantly crushing the search space from <code>O(b^d)</code> down to <code>O(b^{d/2})</code>.

### 21.4.2. Iterative Deepening DFS (IDDFS)

**Definition:** IDDFS executes standard DFS but strictly enforces an incrementally increasing <abbr title="The length of the path from the root to a node.">depth</abbr> limit. It masterfully combines the minimal memory footprint of DFS with the complete, optimal pathfinding guarantees of BFS.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Implementation | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Generic <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">Graph</abbr> | `map[T][]T` | <code>O(1)</code> access | <code>O(V+E)</code> | Robust production networks |
| Iterative DFS | `[]T` <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> | <code>O(V+E)</code> | <code>O(V)</code> | <abbr title="An algorithmic technique for solving problems recursively by trying to build a solution incrementally.">Backtracking</abbr>, <abbr title="A path that starts and ends at the same vertex.">cycle</abbr> detection |
| BFS | `[]T` <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr> | <code>O(V+E)</code> | <code>O(V)</code> | Shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> (unweighted) |
| IDDFS | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> limit | <code>O(b^d)</code> | <code>O(d)</code> | Memory constrained environments |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 19:</strong> Utilizing Go 1.18 Generics to map `[T comparable]` profoundly transforms <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> traversal from academic exercises into robust, production-ready systems capable of routing strings, IPs, and user objects. Use Iterative DFS to circumvent stack overflows, and BFS for lightning-fast unweighted pathfinding.
{{% /alert %}}

---

## Section 4


{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithmic thinking and reasoning will make you more effective in solving complex problems, but it’s important to use the right tool for the job.</em>": Jeff Dean</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 20 focuses on Single-Source Shortest Paths. It abandons fragile <abbr title="A shared boundary across which two or more separate components exchange information.">interface</abbr> casting and implements a high-performance Generic Dijkstra utilizing `container/heap`, alongside Bellman-Ford for negative weight detection.
{{% /alert %}}

## 20.1. Generic Dijkstra’s Algorithm

**Definition:** Dijkstra eagerly discovers the absolute shortest <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> from a single source to all reachable vertices in a <abbr title="A non-linear data structure consisting of nodes (vertices) and edges.">graph</abbr> harboring strictly non-negative <abbr title="A connection between two vertices in a graph.">edge</abbr> weights. It accomplishes this through greedy expansion powered by a <abbr title="A queue where each element has a priority and the highest priority element is served first.">priority queue</abbr> (<abbr title="A heap where the parent node is less than or equal to its children.">min-heap</abbr>).

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Initialization | <code>O(V)</code> | Allocate distance maps |
| Extract-Min | <code>O(log V)</code> | <abbr title="A heap implemented using a binary tree.">Binary heap</abbr> extraction |
| Relaxation | <code>O(E log V)</code> | Total relaxation cost across all edges |
| Total | <code>O((V+E) log V)</code> | Utilizing a binary <abbr title="A heap where the parent node is less than or equal to its children.">min-heap</abbr> |

### Idiomatic Go 1.18+ Generic Implementation

To build a production-grade Dijkstra, we must first establish a generic <abbr title="A heap where the parent node is less than or equal to its children.">Min-Heap</abbr> specifically engineered to store <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> states without suffering from <abbr title="A shared boundary across which two or more separate components exchange information.">interface</abbr> boxing.

```go
package main

import (
	"container/heap"
	"fmt"
)

// Edge represents a directed connection with a positive weight.
type Edge[T comparable] struct {
	To     T
	Weight int
}

// Graph is a generic weighted adjacency list.
type Graph[T comparable] struct {
	Adj map[T][]Edge[T]
}

func NewGraph[T comparable]() *Graph[T] {
	return &Graph[T]{Adj: make(map[T][]Edge[T])}
}

func (g *Graph[T]) AddEdge(from, to T, weight int) {
	g.Adj[from] = append(g.Adj[from], Edge[T]{To: to, Weight: weight})
}

// --- Heap Implementation ---

type State[T comparable] struct {
	Node T
	Dist int
}

// internalHeap satisfies container/heap but operates on generic States.
type internalHeap[T comparable] []State[T]

func (h internalHeap[T]) Len() int           { return len(h) }
func (h internalHeap[T]) Less(i, j int) bool { return h[i].Dist < h[j].Dist } // Min-Heap
func (h internalHeap[T]) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *internalHeap[T]) Push(x any) {
	*h = append(*h, x.(State[T]))
}

func (h *internalHeap[T]) Pop() any {
	old := *h
	n := len(old)
	item := old[n-1]
	*h = old[:n-1]
	return item
}

// --- Dijkstra Core ---

// Dijkstra computes the shortest path from the start node.
func (g *Graph[T]) Dijkstra(start T) map[T]int {
	dist := make(map[T]int)
	
	// We use a map to simulate "infinity". If a key doesn't exist, it's unreachable.
	dist[start] = 0

	pq := &internalHeap[T]{State[T]{Node: start, Dist: 0}}
	heap.Init(pq)

	for pq.Len() > 0 {
		// Pop the closest node
		current := heap.Pop(pq).(State[T])

		// Heap Staleness Check: We might have pushed a better path earlier.
		// If this extracted state is worse than our known best, aggressively discard it.
		if current.Dist > dist[current.Node] {
			continue
		}

		// Relax all outgoing edges
		for _, edge := range g.Adj[current.Node] {
			newDist := current.Dist + edge.Weight
			
			// If we haven't visited this node, or we found a strictly faster route
			knownDist, exists := dist[edge.To]
			if !exists || newDist < knownDist {
				dist[edge.To] = newDist
				heap.Push(pq, State[T]{Node: edge.To, Dist: newDist})
			}
		}
	}

	return dist
}

func main() {
	g := NewGraph[string]()
	g.AddEdge("A", "B", 4)
	g.AddEdge("A", "C", 1)
	g.AddEdge("C", "B", 2)
	g.AddEdge("B", "D", 5)
	g.AddEdge("C", "D", 8)

	distances := g.Dijkstra("A")
	fmt.Println("Shortest Distances from A:")
	for node, d := range distances {
		fmt.Printf(" -> %s: %d\n", node, d)
	}
	// Output: 
	// -> A: 0
	// -> C: 1
	// -> B: 3
	// -> D: 8
}
```

### Decision Matrix

| Use Dijkstra When... | Avoid If... |
|-------------------|------------------|
| <abbr title="A connection between two vertices in a graph.">Edge</abbr> weights are strictly non-negative | Negative weights exist (It will fail silently or infinite loop) |
| You require paths from a single starting point | You require paths between absolutely all nodes simultaneously (Floyd-Warshall) |

### Edge Cases & Pitfalls
- **<abbr title="A specialized tree-based data structure that satisfies the heap property.">Heap</abbr> Staleness:** Dijkstra routinely pushes duplicate nodes into the <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr> when shorter paths are discovered. You **must** implement the staleness check (`if current.Dist > dist[current.Node]`) to discard outdated paths and prevent performance implosions.

## 20.2. <abbr title="An algorithm that computes shortest paths from a single source, handling negative weights.">Bellman-Ford Algorithm</abbr>

**Definition:** Bellman-Ford systematically relaxes every single <abbr title="A connection between two vertices in a graph.">edge</abbr> <code>V-1</code> times. It acts as the ultimate fallback when dealing with graphs infected by negative weight edges.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Relaxation | <code>O(VE)</code> | V-1 violent sweeps across all E edges |
| <abbr title="A path that starts and ends at the same vertex.">Cycle</abbr> detect | <code>O(E)</code> | One final sweep to verify stability |
| Total | <code>O(VE)</code> | Dramatically slower than Dijkstra |

### Edge Cases & Pitfalls

- **Negative <abbr title="A path that starts and ends at the same vertex.">cycle</abbr>:** If an <abbr title="A connection between two vertices in a graph.">edge</abbr> can be relaxed on the <code>V</code>-th <abbr title="The repetition of a process, typically using loops.">iteration</abbr>, a negative weight <abbr title="A path that starts and ends at the same vertex.">cycle</abbr> definitively exists. The algorithm must aggressively halt and throw an error.
- **Unreachable nodes:** Distance maps should not be initialized to zero; missing keys or explicit infinity constants must be used.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Generic Dijkstra | `container/heap` | <code>O((V+E) \log V)</code> | <code>O(V)</code> | Fast GPS / Network Routing |
| Bellman-Ford | <abbr title="A connection between two vertices in a graph.">Edge</abbr> slice iterations | <code>O(VE)</code> | <code>O(V)</code> | Financial Arbitrage detection |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 20:</strong> Dijkstra provides lightning-fast pathfinding for standard graphs, but requires strict protection against "<abbr title="A specialized tree-based data structure that satisfies the heap property.">Heap</abbr> Staleness." By deploying Go Generics `[T comparable]`, our routing algorithms seamlessly <abbr title="A shared boundary across which two or more separate components exchange information.">interface</abbr> with high-level application data like UUIDs and Strings, completely eliminating the translation layers historically required for integer-only <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> algorithms.
{{% /alert %}}

---

