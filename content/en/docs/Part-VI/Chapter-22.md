---
weight: 60100
title: "Chapter 22: Divide and Conquer"
description: "Divide and Conquer"
icon: "article"
date: "2024-08-24T23:41:51+07:00"
lastmod: "2024-08-24T23:41:51+07:00"
draft: false
katex: true
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A recursive method is often the most natural way to solve a problem that can be broken down into smaller problems of the same type.</em>" : Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 23 focuses on the <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr> paradigm, breaking down problems recursively. It implements classical algorithms and demonstrates how to parallelize independent sub-problems efficiently using Go's goroutines.
{{% /alert %}}

## 23.1. Introduction to <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr>

**Definition:** <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and conquer</abbr> breaks down a problem into smaller independent subproblems, solves them recursively, and combines their results.

**Background & Philosophy:**
The philosophy is breaking seemingly insurmountable problems into trivial base cases. Instead of attacking a fortress directly, you divide it into manageable stones. Because it maps problems to independent execution branches, it natively supports mathematical induction for correctness proofs and parallel processing.

**Use Cases:**
Essential for recursive sorting (Merge Sort, Quick Sort), fast multiplication (Karatsuba), and processing independent queries in massive distributed databases via MapReduce architectures.

**Memory Mechanics:**
<abbr title="An algorithmic paradigm breaking problems into independent subproblems">Divide and Conquer</abbr> relies heavily on the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>. Each recursive split pushes a new frame onto the stack. In Go, <abbr title="A lightweight concurrent execution thread managed by the Go runtime">goroutine</abbr> stacks start at 2KB and grow dynamically, preventing overflow for moderate depth <code>O(log n)</code>. When the divide step requires creating new slices `arr[:mid]`, Go merely copies a 24-byte <abbr title="A small struct describing a slice: pointer, length, capacity">slice header</abbr> (pointer, length, capacity) without allocating new arrays on the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>. This makes Go's slice splitting an incredibly fast <code>O(1)</code> memory operation that does not trigger the <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr>.

### Operations & Complexity

| Phase | Operation | Complexity | Description |
|------|---------|--------------|------------|
| Divide | Divide problem | <code>O(1)</code> or <code>O(n)</code> | Usually split in the middle |
| Conquer | Solve subproblem | T(n/b) | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> |
| Combine | Merge results | <code>O(n)</code> or <code>O(n log n)</code> | Merge, partition |

### Pseudocode

```text
sumDivideConquer(arr):
    if arr is empty:
        return 0
    if len(arr) == 1:
        return arr[0]
    mid = len(arr) / 2
    left = sumDivideConquer(arr[0:mid])
    right = sumDivideConquer(arr[mid:])
    return left + right
```

### Idiomatic Go Implementation

Basic <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>:

```go
package main

import "fmt"

func sumDC(arr []int) int {
	if len(arr) == 0 {
		return 0
	}
	if len(arr) == 1 {
		return arr[0]
	}
	mid := len(arr) / 2
	return sumDC(arr[:mid]) + sumDC(arr[mid:])
}

func main() {
	fmt.Println(sumDC([]int{1, 2, 3, 4, 5}))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Independent and non-overlapping subproblems | Overlapping subproblems (DP is better) |
| Combine step is cheaper than <abbr title="A straightforward approach trying all possible solutions.">brute force</abbr> | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> overhead > gain (small n) |
| Natural recursive structure | <abbr title="A LIFO (Last In, First Out) abstract data type.">Stack</abbr> <abbr title="The length of the path from the root to a node.">depth</abbr> is strictly limited |

### Edge Cases & Pitfalls
- **Case <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>:** <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> on n > 10⁴ can cause a <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>; convert to an iterative approach.
- **Case base case:** Forgetting to handle `len <= 1` causes infinite <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>.
- **Case off-by-one:** `arr[:mid]` and `arr[mid:]` for `mid = len/2` works perfectly for balanced splits.

## 23.2. Implementing <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr> in Go

**Definition:** Go supports <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> through slices, <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr>, and generics, with automatic memory management preventing leaks during intermediate allocations.

### Operations & Complexity

| Technique | Go Feature | Complexity | Description |
|--------|-----------|--------------|------------|
| Slice split | `arr[:mid]` | <code>O(1)</code> | Shared backing <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> |
| In-place partition | Swap | <code>O(n)</code> | <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick sort</abbr> |
| Merge auxiliary | `make([]T, n)` | <code>O(n)</code> | <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge sort</abbr> space |
| Tail <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">recursion</abbr> | Not optimized | . | Go does not optimize tail calls |

### Pseudocode

```text
quickSort(arr):
    if len(arr) <= 1:
        return
    pivotIndex = PARTISI(arr)
    quickSort(arr[0:pivotIndex])
    quickSort(arr[pivotIndex+1:])

PARTISI(arr):
    pivot = last element
    i = 0
    for j = 0 to len(arr)-2:
        if arr[j] < pivot:
            swap arr[i] and arr[j]
            i = i + 1
    swap arr[i] and pivot
    return i
```

### Idiomatic Go Implementation

In-place <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">quick sort</abbr>:

```go
package main

import "fmt"

func quickSort(arr []int) {
	if len(arr) <= 1 {
		return
	}
	pivot := partition(arr)
	quickSort(arr[:pivot])
	quickSort(arr[pivot+1:])
}

func partition(arr []int) int {
	last := len(arr) - 1
	pivot := arr[last]
	i := 0
	for j := 0; j < last; j++ {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[last] = arr[last], arr[i]
	return i
}

func main() {
	data := []int{3, 6, 8, 10, 1, 2, 1}
	quickSort(data)
	fmt.Println(data)
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| In-place <abbr title="The process of arranging elements in a specific order.">sorting</abbr> is required | Data is nearly sorted (<abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> <code>O(n^2)</code>) |
| Memory is strictly limited | A stable sort is required |
| <abbr title="The expected runtime or resource usage of an algorithm over random inputs.">Average-case</abbr> <code>O(n log n)</code> is sufficient | <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">Worst-case</abbr> guarantee is required (use <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">merge sort</abbr>) |

### Edge Cases & Pitfalls
- **Case sorted input:** <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick sort</abbr> with the last element as pivot degrades to <code>O(n^2)</code>; use a randomized pivot or median-of-three.
- **Case duplicate elements:** Partitioning with just `<` can lead to imbalanced splits; consider three-way partitioning.
- **Case small subarrays:** Switch to <abbr title="A sorting algorithm that builds the final sorted array one item at a time.">insertion sort</abbr> for n < 10-20 (hybrid sort).

## 23.3. Case Studies: Divide and Conquer Algorithms

**Definition:** Case studies of merge sort, quick sort, binary search, and Strassen's matrix multiplication demonstrate the practical application of divide and conquer with time and space trade-offs.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| Merge sort | <code>O(n log n)</code> | <code>O(n)</code> | Stable, predictable |
| Quick sort | <code>O(n log n)</code> avg | <code>O(log n)</code> | In-place, fast avg |
| Binary search | <code>O(log n)</code> | <code>O(1)</code> | Sorted data required |
| Strassen | <code>O(n^2.81)</code> | <code>O(n²)</code> | Large matrices only |

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Need stable and predictable sort | <code>O(n)</code> auxiliary memory is unavailable |
| Data is sorted and frequently searched | Data is dynamic with many inserts |
| Large matrices where Strassen is beneficial | Small matrices (overhead > gain) |

### Edge Cases & Pitfalls
- **Case integer overflow on mid:** Use `mid := lo + (hi-lo)/2` to prevent overflow in other languages (Go handles slice indices safely, but it's a good habit).
- **Case empty slice:** `mergeSort(nil)` and `binarySearch(nil, x)` must be safe.
- **Case duplicate keys:** `binarySearch` may return the first occurrence or an arbitrary one; define the requirement clearly.

## 23.4. Parallelizing <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr> Algorithms in Go

**Definition:** Independent subproblems in <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> algorithms enable trivial parallelization using goroutines, but synchronization overhead must be carefully managed.

### Operations & Complexity

| Aspect | Sequential | Parallel | Overhead |
|-------|------------|----------|----------|
| <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge sort</abbr> | <code>O(n log n)</code> | <code>O(n log n / p)</code> | <code>O(n)</code> merge, goroutine spawn |
| <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick sort</abbr> | <code>O(n log n)</code> avg | <code>O(n log n / p)</code> | Partition is sequential |
| Granularity | . | Threshold n > 1000 | Spawn cost < sort cost |

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Large datasets and multi-core are available | Small datasets (< 1000 elements) |
| Balanced subproblems | Highly uneven subproblem sizes |
| CPU-bound and pure computation | I/O-bound (use channels/callbacks instead) |

### Edge Cases & Pitfalls
- **Case goroutine explosion:** Without a threshold, > 10⁶ goroutines can exhaust memory.
- **Case load imbalance:** Parallel <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">quick sort</abbr> with a bad pivot makes one goroutine busy while others idle.
- **Case false sharing:** Goroutines accessing adjacent data in a <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> line causes invalidation.
- **Case WaitGroup misuse:** `wg.Add` must be called before the `go` statement; `wg.Done` must be called (defer is recommended).

## 23.5. Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge sort</abbr> | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> + merge | <code>O(n log n)</code> | <code>O(n)</code> | Stable <abbr title="The process of arranging elements in a specific order.">sorting</abbr>, parallel |
| <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">Quick sort</abbr> | In-place partition | <code>O(n log n)</code> avg | <code>O(log n)</code> | In-place <abbr title="The process of arranging elements in a specific order.">sorting</abbr> |
| <abbr title="A search algorithm that finds the position of a target value within a sorted array.">Binary search</abbr> | Iterative loop | <code>O(log n)</code> | <code>O(1)</code> | Sorted <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> lookup |
| Strassen | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> + matrix ops | <code>O(n^{2.807})</code> | <code>O(n^{2.807})</code> | Fast matrix multiply |
| Sum/Max | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> | <code>O(n)</code> | <code>O(log n)</code> | Trivial parallelization |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 22:</strong> This chapter introduces the <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">divide and conquer</abbr> paradigm with implementations of <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">merge sort</abbr>, <abbr title="A divide-and-conquer sorting algorithm using a pivot element to partition the array.">quick sort</abbr>, and <abbr title="A search algorithm that finds the position of a target value within a sorted array.">binary search</abbr> in Go. It covers recursive decomposition, in-place partitioning techniques, and parallelization using goroutines for CPU-bound problems on multi-core systems.
{{% /alert %}}

## See Also

- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/Part-VI/Chapter-23/)
- [Chapter 25: <abbr title="Building candidates incrementally and abandoning dead ends">Backtracking</abbr>](/docs/Part-VI/Chapter-25/)
- [Chapter 26: Advanced Recursive Algorithms](/docs/Part-VI/Chapter-26/)
