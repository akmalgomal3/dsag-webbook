---
weight: 50100
title: "Chapter 19: Basic Sorting Algorithms"
description: "Basic Sorting Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Sorting is the process of arranging elements in a specific order, typically ascending or descending.</em>"</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 19 covers basic sorting. Topics: Bubble, Selection, Insertion Sort. Explores mechanics, complexity. Uses Go `cmp.Ordered` Generics.
{{% /alert %}}

## 19.1. Bubble Sort

**Definition:** Steps through list. Compares adjacent elements. Swaps if wrong order. Places largest element at end per pass.

**Background & Philosophy:**
Naive local optimization. Repeatedly fixes adjacent inversions. Largest elements "bubble" up. Simplest sorting translation.

**Use Cases:**
Educational only. Detect already-sorted arrays (early exit). Sort nearly-sorted polygons in graphics.

**Memory Mechanics:**
Operates entirely in-place (`O(1)` auxiliary space). Swaps adjacent elements. Exploits spatial locality. CPU cache prefetcher loads contiguous array block into L1 cache. Algorithmically slow (`O(n^2)`). Memory fetches minimal compared to jumping algorithms.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Comparisons | `O(n^2)` | n(n-1)/2 comparisons |
| Swaps | `O(n^2)` worst | Adjacent elements swapped |
| Best case | `O(n)` | Already sorted (with optimization) |
| Space | `O(1)` | In-place |

### Idiomatic Go 1.21+ Implementation

Use Generics and `cmp.Ordered` constraint. Supports any comparable type.

```go
package main

import (
	"cmp"
	"fmt"
)

func bubbleSort[T cmp.Ordered](arr []T) {
	n := len(arr)
	for i := 0; i < n; i++ {
		swapped := false
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
				swapped = true
			}
		}
		if !swapped {
			break
		}
	}
}

func main() {
	arr := []string{"Go", "Python", "Rust", "Java"}
	bubbleSort(arr)
	fmt.Println("Sorted:", arr)
}
```

## 19.2. Selection Sort

**Definition:** Divides array into sorted/unsorted regions. Selects smallest unsorted element. Appends to sorted region.

**Background & Philosophy:**
Absolute minimization of writes. Scans entire unsorted region. Finds absolute minimum. Performs single swap.

**Use Cases:**
Embedded systems. Writing to Flash/EEPROM degrades hardware. Guarantees exactly `n-1` writes.

**Memory Mechanics:**
Reads extensively. Writes minimally. Scans contiguous array repeatedly. Cache friendly for reading. Swap operation jumps to arbitrary index. Causes minor cache misses vs Bubble Sort adjacent swaps.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Comparisons | `O(n^2)` | Always n(n-1)/2 |
| Swaps | `O(n)` | Exactly n-1 swaps |
| Best/Worst | `O(n^2)` | No adaptive behavior |
| Space | `O(1)` | In-place |

### Idiomatic Go 1.21+ Implementation

```go
package main

import (
	"cmp"
	"fmt"
)

func selectionSort[T cmp.Ordered](arr []T) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		minIdx := i
		for j := i + 1; j < n; j++ {
			if arr[j] < arr[minIdx] {
				minIdx = j
			}
		}
		arr[i], arr[minIdx] = arr[minIdx], arr[i]
	}
}

func main() {
	arr := []float64{64.5, 25.2, 12.1, 22.3, 11.0}
	selectionSort(arr)
	fmt.Println("Sorted:", arr)
}
```

## 19.3. Insertion Sort

**Definition:** Builds sorted array one element at a time. Inserts element into correct position within sorted portion.

**Background & Philosophy:**
Mirrors sorting playing cards by hand. Takes one item. Inserts into correct position. Adapts intelligently to partially sorted input.

**Use Cases:**
Best algorithm for small datasets (`n < 20`). Optimized base case for hybrid algorithms (Timsort, Go pdqsort).

**Memory Mechanics:**
Continuously shifts elements right. Overlaps memory move operations. Shifts elements sequentially in contiguous block. Highly hardware-friendly. CPU branch predictor and cache prefetcher anticipate linear access. Exceptionally fast for small arrays.

### Operations & Complexity

| Case | Complexity | Condition |
|------|------------|-----------|
| Best | `O(n)` | Already sorted |
| Average | `O(n^2)` | Random order |
| Worst | `O(n^2)` | Reverse sorted |
| Space | `O(1)` | In-place |

### Idiomatic Go 1.21+ Implementation

```go
package main

import (
	"cmp"
	"fmt"
)

func insertionSort[T cmp.Ordered](arr []T) {
	for i := 1; i < len(arr); i++ {
		key := arr[i]
		j := i - 1
		for j >= 0 && arr[j] > key {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = key
	}
}

func main() {
	arr := []int{12, 11, 13, 5, 6}
	insertionSort(arr)
	fmt.Println("Sorted:", arr)
}
```

### Decision Matrix

| Algorithm | Use When... | Avoid If... |
|-----------|-------------|-------------|
| Bubble Sort | Educational only | Any production code |
| Selection Sort | Minimizing swaps critical | Performance matters |
| Insertion Sort | Small or nearly sorted data | Large random datasets |

### Edge Cases & Pitfalls
- **Stability:** Bubble and Insertion Sort are stable. Selection Sort is not.
- **Adaptive:** Insertion Sort performs `O(n)` on sorted input.
- **Go Built-in:** Use `slices.Sort()` (Go 1.21+) for production.

### Anti-Patterns
- **Custom `O(n^2)` in production:** Never the right choice. Use `slices.Sort` (pdqsort hybrid).
- **`sort.Interface` over `cmp.Ordered`:** Go 1.21+ `slices.SortFunc` with `cmp.Compare` replaces verbose `sort.Interface` structs.
- **Manual Insertion Sort on small slices:** `slices.Sort` handles small slices automatically via insertion sort fallback.

## 19.4. Quick Reference

| Algorithm | Time | Space | Stable | Best For |
|-----------|------|-------|--------|----------|
| Bubble Sort | `O(n^2)` | `O(1)` | Yes | Educational |
| Selection Sort | `O(n^2)` | `O(1)` | No | Minimizing writes |
| Insertion Sort | `O(n^2)` avg | `O(1)` | Yes | Small/sorted data |
| Go slices.Sort | `O(n log n)` | `O(log n)` | No | Production |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 19:</strong> Basic sorts run `O(n^2)`. Mostly educational. Insertion Sort remains relevant for small datasets as hybrid base case. Always prefer `slices` package for production.
{{% /alert %}}

## See Also
- [Chapter 20: Advanced Sorting Algorithms](/docs/part-v/chapter-20/)
- [Chapter 21: Searching Algorithms](/docs/part-v/chapter-21/)
- [Chapter 54: Counting, Radix, and Bucket Sort](/docs/part-xi/chapter-54/)
