---
weight: 60100
title: "Chapter 22: Divide and Conquer"
description: "Divide and Conquer"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
katex: true
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A recursive method is often the most natural way to solve a problem that can be broken down into smaller problems of the same type.</em>" — Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 22: Divide and Conquer paradigm. Recursive problem decomposition. Parallelization using Go goroutines.
{{% /alert %}}

## 22.1. Introduction to <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr>

**Definition:** Splits problem into smaller independent subproblems. Solves recursively. Combines results.

**Logic:**
Decomposes complex problems into trivial base cases. Maps to independent execution branches. Supports mathematical induction and parallel processing.

**Use Cases:**
Recursive sorting (Merge Sort, Quick Sort). Fast multiplication (Karatsuba). MapReduce distributed queries.

**Memory Mechanics:**
Relies on <abbr title="Memory used to execute functions and store local variables.">call stack</abbr>. Go goroutine stacks start at 2KB and grow dynamically. O(log n) depth avoids overflow. Slice splitting `arr[:mid]` copies 24-byte header only. No heap allocation. Fast O(1) memory operation.

### Operations & Complexity

| Phase | Operation | Complexity | Description |
|------|---------|----------------------------------------------|------------|
| Divide | Split problem | <code>O(1)</code> or <code>O(n)</code> | Usually middle split |
| Conquer | Solve subproblem | <code>T(n/b)</code> | Recursive step |
| Combine | Merge results | <code>O(n)</code> or <code>O(n log n)</code> | Result integration |

### Pseudocode

```text
sumDivideConquer(arr):
    if arr is empty: return 0
    if len(arr) == 1: return arr[0]
    mid = len(arr) / 2
    left = sumDivideConquer(arr[0:mid])
    right = sumDivideConquer(arr[mid:])
    return left + right
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func sumDC(arr []int) int {
	if len(arr) == 0 { return 0 }
	if len(arr) == 1 { return arr[0] }
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
| Independent subproblems exist | Subproblems overlap (use DP) |
| Combine step is efficient | Recursion overhead > speed gain |
| Natural recursive structure | Stack depth is strictly limited |

### Edge Cases & Pitfalls
- **Stack overflow:** Deep recursion (n > 10⁴) risks stack exhaustion. Use iterative approach.
- **Base case:** Handle `len <= 1` to prevent infinite recursion.
- **Off-by-one:** Use `arr[:mid]` and `arr[mid:]` for balanced splits.

## 22.2. Implementing <abbr title="An algorithmic paradigm that breaks a problem into subproblems, solves them, and combines the results.">Divide and Conquer</abbr> in Go

**Definition:** Go employs slices, recursion, and generics. Automatic memory management prevents intermediate leaks.

### Operations & Complexity

| Technique | Go Feature | Complexity | Description |
|--------|-----------|--------------|------------|
| Slice split | `arr[:mid]` | <code>O(1)</code> | Shared backing array |
| In-place partition | Swap | <code>O(n)</code> | Quick sort step |
| Merge auxiliary | `make([]T, n)` | <code>O(n)</code> | Merge sort space |
| Tail recursion | Not optimized | . | Go lacks tail-call optimization |

### Idiomatic Go Implementation (Quick Sort)

```go
package main

import "fmt"

func quickSort(arr []int) {
	if len(arr) <= 1 { return }
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

## 22.3. Case Studies

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| Merge sort | <code>O(n log n)</code> | <code>O(n)</code> | Stable, predictable |
| Quick sort | <code>O(n log n)</code> avg | <code>O(log n)</code> | In-place, fast average |
| Binary search | <code>O(log n)</code> | <code>O(1)</code> | Requires sorted data |
| Strassen | <code>O(n^2.81)</code> | <code>O(n²)</code> | Large matrix optimization |

## 22.4. Parallelizing in Go

**Definition:** Independent subproblems enable goroutine-based concurrency.

**Rules:**
Use threshold for granularity (e.g., n > 1000). Small tasks should run sequentially to avoid spawning overhead.

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Massive datasets + multi-core | Small datasets (n < 1000) |
| Balanced subproblems | Highly uneven task sizes |
| CPU-bound computation | I/O-bound tasks (use channels) |

### Anti-Patterns

- **Unbounded spawning:** Spawning goroutines per subproblem without threshold kills performance. Use minimum size limits.
- **Data races:** Concurrent writes to overlapping slices cause corruption. Partition output ranges.
- **Load imbalance:** Bad pivot strategies cause idle cores. Use randomized pivots.

## 22.5. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Merge sort | Recursion + merge | <code>O(n log n)</code> | <code>O(n)</code> | Stable, parallel sorting |
| Quick sort | In-place partition | <code>O(n log n)</code> avg | <code>O(log n)</code> | Memory-efficient sorting |
| Binary search | Iterative loop | <code>O(log n)</code> | <code>O(1)</code> | Fast lookup |
| Strassen | Recursion | <code>O(n^{2.807})</code> | <code>O(n^{2.807})</code> | Matrix multiplication |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 22:</strong> Divide and Conquer breaks problems into independent sub-tasks. Optimal for recursive sorting and searching. Goroutines enable efficient multi-core parallelization.
{{% /alert %}}

## See Also

- [Chapter 23: Dynamic Programming](/docs/part-vi/chapter-23/)
- [Chapter 25: Backtracking](/docs/part-vi/chapter-25/)
- [Chapter 26: Advanced Recursive Algorithms](/docs/part-vi/chapter-26/)
