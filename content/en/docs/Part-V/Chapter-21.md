---
weight: 50300
title: "Chapter 21: Searching Algorithms"
description: "Searching Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The art of programming is the art of organizing complexity.</em>" — Edsger Dijkstra</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 21 covers searching. Topics: Linear, Binary, Interpolation Search. Implements via Generics (`cmp.Ordered`) and `slices` package.
{{% /alert %}}

## 21.1. Linear Search

**Definition:** Sequentially checks each element until target found or end reached.

**Background & Philosophy:**
Philosophy: exhaustive brute-force. Assumes no structure. Resilient but inefficient.

**Use Cases:**
Unindexed data. Short arrays. Unsortable data streams.

**Memory Mechanics:**
Excellent spatial locality. CPU cache prefetcher predicts sequential access. Loads contiguous memory blocks to L1 cache. For small arrays (`n < 64`), Linear Search beats Binary Search due to zero branch misprediction.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Search | `O(n)` | Scan every element |
| Best case | `O(1)` | Target at first position |
| Space | `O(1)` | No extra memory |

### Idiomatic Go 1.21+ Generic Implementation

Use `slices.Contains` or `slices.Index`.

```go
package main

import (
	"fmt"
	"slices"
)

func linearSearch[T comparable](arr []T, target T) int {
	for i, v := range arr {
		if v == target {
			return i
		}
	}
	return -1
}

func main() {
	arr := []string{"Go", "Rust", "C++", "Zig"}
	
	if slices.Contains(arr, "Rust") {
		fmt.Println("Found Rust!")
	}

	idx := slices.Index(arr, "C++")
	fmt.Println("Index:", idx)
}
```

## 21.2. Binary Search

**Definition:** Repeatedly divides sorted array in half. Eliminates half remaining elements per comparison. Requires sorted data.

**Background & Philosophy:**
Philosophy: elimination. Safely discards half the search space per check. Reduces million elements to 20 comparisons.

**Use Cases:**
Querying ordered data. B-Trees. Resolving numerical ranges.

**Memory Mechanics:**
Jumps across array (`n/2`, `n/4`). Breaks CPU cache line. Causes repeated cache misses. RAM latency bottlenecks performance on massive datasets. Logarithmic algorithmic advantage still dominates scales.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Search | `O(log n)` | Halve search space |
| Precondition | Sorted data | Sort first if unsorted |
| Space | `O(1)` | Iterative version |

### Idiomatic Go 1.21+ Generic Implementation

Use `slices.BinarySearch`.

```go
package main

import (
	"cmp"
	"fmt"
	"slices"
)

func binarySearch[T cmp.Ordered](arr []T, target T) int {
	left, right := 0, len(arr)-1
	for left <= right {
		mid := left + (right-left)/2
		if arr[mid] == target {
			return mid
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	return -1
}

func main() {
	arr := []int{1, 3, 5, 7, 9, 11, 13}
	
	idx, found := slices.BinarySearch(arr, 7)
	if found {
		fmt.Println("Index:", idx)
	}
}
```

## 21.3. Interpolation Search

**Definition:** Estimates target position via linear interpolation. `O(log log n)` for uniformly distributed data.

**Background & Philosophy:**
Mimics physical dictionary use. Guesses position based on data distribution.

**Use Cases:**
Massive, uniformly distributed numerical datasets. Math calculation cheaper than Binary Search cache misses.

**Memory Mechanics:**
Uses complex arithmetic for index guessing. ALUs perform math instantly. Accurate guess minimizes cache misses compared to strict halving.

### Operations & Complexity

| Case | Complexity | Condition |
|------|------------|-----------|
| Average | `O(log log n)` | Uniform distribution |
| Worst | `O(n)` | Exponential distribution |
| Best | `O(1)` | Target at exact guess |

### Idiomatic Go Generic Implementation

```go
package main

func interpolationSearch(arr []int, target int) int {
	low, high := 0, len(arr)-1
	for low <= high && target >= arr[low] && target <= arr[high] {
		if low == high {
			if arr[low] == target { return low }
			break
		}
		pos := low + ((target-arr[low])*(high-low))/(arr[high]-arr[low])
		if arr[pos] == target { return pos }
		if arr[pos] < target { low = pos + 1 } else { high = pos - 1 }
	}
	return -1
}
```

## 21.4. Decision Matrix

| Use Search When... | Conditions | Cache Locality | Time |
|--------------------|------------|----------------|------|
| Linear Search | Short or Unsorted | Excellent | `O(n)` |
| Binary Search | Large and Sorted | Poor | `O(log n)` |
| Interpolation Search | Large, Sorted, Uniform | Good | `O(log log n)` |
| Hash Map Lookup | Key-Value Needs | None | `O(1)` avg |

### Edge Cases & Pitfalls
- **Integer overflow:** `mid := left + (right-left)/2` prevents overflow.
- **Unsorted input:** Binary search fails silently. Verify via `slices.IsSorted`.
- **Search vs Map:** `map[T]struct{}` outperforms repeated binary searches for simple existence checks.

### Anti-Patterns
- **Sorting for single search:** Sorting (`O(n log n)`) costs more than single linear search (`O(n)`).
- **Binary searching unsorted slice:** Results undefined. Sort first.
- **Ignoring `slices.BinarySearchFunc`:** Manual loops over complex structs breed bugs. Use standard library custom comparison functions.

## 21.5. Quick Reference

| Algorithm | Go Implementation | Precondition | Complexity |
|-----------|-------------------|--------------|------------|
| Linear Search | `slices.Index` | None | `O(n)` |
| Existence Check | `slices.Contains` | None | `O(n)` |
| Binary Search | `slices.BinarySearch` | Sorted | `O(log n)` |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 21:</strong> Prefer `slices` package. Linear search for unstructured data. Binary search for sorted data. Interpolation search minimizes cache misses on uniform numerical data.
{{% /alert %}}

## See Also
- [Chapter 7: Hashing and Hash Tables](/docs/part-ii/chapter-7/)
- [Chapter 19: Basic Sorting Algorithms](/docs/part-v/chapter-19/)
