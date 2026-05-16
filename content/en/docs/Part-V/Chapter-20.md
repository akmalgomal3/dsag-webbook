---
weight: 50200
title: "Chapter 20: Advanced Sorting Algorithms"
description: "Advanced Sorting Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Intelligence is the ability to adapt to change.</em>" : Stephen Hawking</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 20 covers advanced sorting. Topics: Merge, Quick, Heap Sort. Achieves `O(n log n)`. Forms real-world backbone. Uses Generics. Adds `context` parallelization.
{{% /alert %}}

## 20.1. Merge Sort

**Definition:** Divide and conquer algorithm. Divides array, recursively sorts halves, merges halves.

**Background & Philosophy:**
Philosophy: Divide and Conquer. Sorting and merging small arrays mathematically beats comparing all elements. Guarantees `O(n log n)` execution time regardless of input.

**Use Cases:**
External sorting (datasets larger than RAM). Sorting Linked Lists (lacks random access).

**Memory Mechanics:**
Memory intensive. Requires `O(n)` auxiliary array for merging. Naive Go recursion allocates short-lived slices. Triggers heavy Garbage Collector pressure. Thrashing array blocks between main array and auxiliary array ruins CPU cache locality.

### Idiomatic Go 1.21+ Generic Implementation

```go
package main

import (
	"cmp"
	"fmt"
)

func mergeSort[T cmp.Ordered](arr []T) []T {
	if len(arr) <= 1 {
		return arr
	}
	mid := len(arr) / 2
	left := mergeSort(arr[:mid])
	right := mergeSort(arr[mid:])
	return merge(left, right)
}

func merge[T cmp.Ordered](left, right []T) []T {
	result := make([]T, 0, len(left)+len(right))
	for len(left) > 0 && len(right) > 0 {
		if left[0] < right[0] {
			result = append(result, left[0])
			left = left[1:]
		} else {
			result = append(result, right[0])
			right = right[1:]
		}
	}
	result = append(result, left...)
	result = append(result, right...)
	return result
}
```

### Parallel Merge Sort with Context (Modern Go)

CPU-bound tasks require `context.Context` cancellation support.

```go
package main

import (
	"cmp"
	"context"
	"fmt"
	"sync"
)

func ParallelMergeSort[T cmp.Ordered](ctx context.Context, arr []T) ([]T, error) {
	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	default:
	}

	if len(arr) < 1024 {
		return mergeSort(arr), nil
	}

	mid := len(arr) / 2
	var left, right []T
	var lErr, rErr error
	var wg sync.WaitGroup

	wg.Add(2)
	go func() {
		defer wg.Done()
		left, lErr = ParallelMergeSort(ctx, arr[:mid])
	}()
	go func() {
		defer wg.Done()
		right, rErr = ParallelMergeSort(ctx, arr[mid:])
	}()
	wg.Wait()

	if lErr != nil { return nil, lErr }
	if rErr != nil { return nil, rErr }

	return merge(left, right), nil
}
```

## 20.2. Quick Sort

**Definition:** Selects pivot. Partitions array into smaller/larger elements. Recursively sorts partitions.

**Background & Philosophy:**
Philosophy: Partitioning. Skips meticulous merging. Moves elements relative to pivot. Gambles on random probability for balanced tree.

**Use Cases:**
Default general-purpose array sorting. Unmatched in-memory speed.

**Memory Mechanics:**
In-place execution. Zero `O(n)` heap allocations. Bypasses GC. Pointers scan array sequentially. Hardware prefetcher locks array blocks into L1 cache. Cache-friendliness makes Quick Sort consistently beat Merge Sort in reality.

### Idiomatic Go 1.21+ Generic Implementation

```go
package main

import (
	"cmp"
	"fmt"
)

func QuickSort[T cmp.Ordered](arr []T) {
	if len(arr) <= 1 {
		return
	}
	pivotIdx := partition(arr)
	QuickSort(arr[:pivotIdx])
	QuickSort(arr[pivotIdx+1:])
}

func partition[T cmp.Ordered](arr []T) int {
	pivot := arr[len(arr)-1]
	i := 0
	for j := 0; j < len(arr)-1; j++ {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[len(arr)-1] = arr[len(arr)-1], arr[i]
	return i
}
```

## 20.3. Heap Sort

**Definition:** Builds max heap from array. Repeatedly extracts maximum element to array end.

**Background & Philosophy:**
Treats array as binary tree. Philosophy: Strict priority management. Max-Heap guarantees largest element stays at index 0.

**Use Cases:**
Real-time systems. Linux kernel. Guarantees `O(n log n)` time with strict `O(1)` auxiliary space.

**Memory Mechanics:**
Poor memory access patterns. Parent-child math (`2*i + 1`) jumps across indices. Causes severe cache misses. Mathematically optimal but lacks hardware sympathy. Slower than Quick Sort.

### Idiomatic Go 1.21+ Generic Implementation

```go
package main

import (
	"cmp"
	"fmt"
)

func HeapSort[T cmp.Ordered](arr []T) {
	n := len(arr)
	for i := n/2 - 1; i >= 0; i-- {
		heapify(arr, n, i)
	}
	for i := n - 1; i > 0; i-- {
		arr[0], arr[i] = arr[i], arr[0]
		heapify(arr, i, 0)
	}
}

func heapify[T cmp.Ordered](arr []T, n, i int) {
	largest := i
	left := 2*i + 1
	right := 2*i + 2
	if left < n && arr[left] > arr[largest] { largest = left }
	if right < n && arr[right] > arr[largest] { largest = right }
	if largest != i {
		arr[i], arr[largest] = arr[largest], arr[i]
		heapify(arr, n, largest)
	}
}
```

## 20.4. Decision Matrix

| Algorithm | Time | Space | Stable | Cache Friendly | Best For |
|-----------|------|-------|--------|----------------|----------|
| Merge Sort | `O(n log n)` | `O(n)` | Yes | Poor | External sorting, stability |
| Quick Sort | `O(n log n)` avg | `O(log n)` | No | Good | General purpose, in-place |
| Heap Sort | `O(n log n)` | `O(1)` | No | Poor | Constrained memory |
| Go slices.Sort | `O(n log n)` | `O(log n)` | No | Excellent | Production |

### Edge Cases & Pitfalls
- **Pivot selection:** Randomized pivot avoids `O(n^2)` worst case in Quick Sort.
- **Stability:** Quick/Heap Sort are unstable. Use Merge Sort if stability required.
- **Concurrency:** Parallel algorithms must accept context cancellation.

### Anti-Patterns
- **Temporary recursion slices:** Turns `O(n log n)` time into massive GC pressure. Pre-allocate auxiliary array once.
- **Ignoring hardware sympathy:** Using Heap Sort for massive arrays instead of cache-friendly Quick Sort.
- **Deterministic Pivot:** Last-element pivot on sorted data triggers quadratic degradation.

## 20.5. Quick Reference

| Name | Go Type | Time | Space | Stable | Use Case |
|------|---------|------|-------|--------|----------|
| Merge Sort | Generic | `O(n log n)` | `O(n)` | Yes | Linked lists, stability |
| Quick Sort | Generic | `O(n log n)` avg | `O(log n)` | No | General purpose |
| Heap Sort | Generic | `O(n log n)` | `O(1)` | No | Embedded systems |
| Go slices.Sort | Generic | `O(n log n)` | `O(log n)` | No | Standard library default |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 20:</strong> Advanced sorting achieves `O(n log n)` via Divide and Conquer, Partitioning, or Priority Management. Modern Go utilizes Generics for safety and Context for robust parallelization.
{{% /alert %}}

## See Also
- [Chapter 19: Basic Sorting Algorithms](/docs/part-v/chapter-19/)
- [Chapter 21: Searching Algorithms](/docs/part-v/chapter-21/)
- [Chapter 54: Counting, Radix, and Bucket Sort](/docs/part-xi/chapter-54/)
