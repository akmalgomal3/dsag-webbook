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
Chapter 19 covers basic sorting algorithms: <abbr title="A simple O(n²) sorting algorithm using adjacent swaps.">Bubble Sort</abbr>, <abbr title="An O(n²) sorting algorithm selecting the minimum repeatedly.">Selection Sort</abbr>, and <abbr title="An O(n²) sorting algorithm inserting each element into correct position.">Insertion Sort</abbr>. Understand their mechanics, complexity, and when they remain relevant in modern Go.
{{% /alert %}}

## 19.1. <abbr title="A simple sorting algorithm repeatedly swapping adjacent elements">Bubble Sort</abbr>

**Definition:** <abbr title="A simple sorting algorithm repeatedly swapping adjacent elements">Bubble Sort</abbr> repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. Each pass places the next largest element in its correct position.

**Background & Philosophy:**
The philosophy is naive local optimization: by repeatedly fixing adjacent inversions, the largest elements naturally "bubble" to the top. It represents the simplest possible translation of the concept of sorting into code.

**Use Cases:**
Almost exclusively educational. Occasionally used to detect if an array is already sorted (with an early exit optimization) or in computer graphics to sort nearly-sorted polygons in frame rendering.

**Memory Mechanics:**
<abbr title="A simple sorting algorithm repeatedly swapping adjacent elements">Bubble sort</abbr> operates entirely in-place (<code>O(1)</code> auxiliary space). Because it only swaps adjacent elements, it perfectly exploits <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. The <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> prefetcher can load the <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> array block into L1 cache, meaning that while algorithmically slow (<code>O(n^2)</code>), the actual CPU cycles spent on memory fetches are minimal.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Comparisons | <code>O(n^2)</code> | n(n-1)/2 comparisons |
| Swaps | <code>O(n^2)</code> worst | Adjacent elements swapped |
| Best case | <code>O(n)</code> | Already sorted (with optimization) |
| Space | <code>O(1)</code> | In-place |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

```go
package main

import "fmt"

func bubbleSort(arr []int) {
	n := len(arr)
	for i := 0; i < n; i++ {
		swapped := false
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
				swapped = true
			}
		}
		if !swapped { break }
	}
}

func main() {
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	bubbleSort(arr)
	fmt.Println(arr)
}
```

## 19.2. Selection Sort

**Definition:** Selection Sort divides the array into a sorted and unsorted region. It repeatedly selects the smallest element from the unsorted region and appends it to the sorted region.

**Background & Philosophy:**
The philosophy is absolute minimization of writes. It scans the entire unsorted region to find the absolute minimum, and only then performs a single swap.

**Use Cases:**
Used in embedded systems where writing to <abbr title="A type of non-volatile memory that wears out with repeated writes.">Flash memory</abbr> or EEPROM is extremely costly or degrades hardware life, as it guarantees exactly `n-1` writes.

**Memory Mechanics:**
Selection sort reads extensively but writes minimally. It scans the <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> array repeatedly, which is <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> friendly for reading. However, the swap operation involves jumping to an arbitrary minimum index, which causes minor <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr> compared to the strictly adjacent swaps of Bubble Sort.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Comparisons | <code>O(n^2)</code> | Always n(n-1)/2 |
| Swaps | <code>O(n)</code> | Exactly n-1 swaps |
| Best/Worst | <code>O(n^2)</code> | No adaptive behavior |
| Space | <code>O(1)</code> | In-place |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func selectionSort(arr []int) {
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
	arr := []int{64, 25, 12, 22, 11}
	selectionSort(arr)
	fmt.Println(arr)
}
```

## 19.3. Insertion Sort

**Definition:** Insertion Sort builds the sorted array one element at a time by taking each element and inserting it into its correct position within the already-sorted portion.

**Background & Philosophy:**
The philosophy mirrors how humans sort playing cards in their hands: take one card at a time and insert it into its correct position among the already sorted cards. It adapts intelligently to partially sorted input.

**Use Cases:**
The absolute best algorithm for small datasets (e.g., `n < 20`). It is the heavily optimized base case for hybrid algorithms like Timsort (used in Python and Rust) and pdqsort (used in Go 1.19+).

**Memory Mechanics:**
Insertion sort continuously shifts elements one position to the right. In <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>, this translates to overlapping memory move operations. Because it shifts elements sequentially in a <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> block, it is very hardware-friendly. On modern CPUs, the branch predictor and cache prefetcher anticipate this linear memory access pattern, making it fast for small arrays.

### Operations & Complexity

| Case | Complexity | Condition |
|------|------------|-----------|
| Best | <code>O(n)</code> | Already sorted |
| Average | <code>O(n^2)</code> | Random order |
| Worst | <code>O(n^2)</code> | Reverse sorted |
| Space | <code>O(1)</code> | In-place |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func insertionSort(arr []int) {
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
	fmt.Println(arr)
}
```

### Decision Matrix

| Algorithm | Use When... | Avoid If... |
|-----------|-------------|-------------|
| Bubble Sort | Never in production | Any real application |
| Selection Sort | Minimizing swaps is critical | Performance matters |
| Insertion Sort | Small or nearly sorted data | Large, random datasets |

### Edge Cases & Pitfalls

- **<abbr title="A property where equal elements maintain their relative order after sorting.">Stability</abbr>:** Bubble Sort and Insertion Sort are stable; Selection Sort is not.
- **Adaptive:** Insertion Sort performs well on nearly sorted data (e.g., <code>O(n)</code> for sorted input).
- **Go's built-in:** For production, always use `sort.Ints()` or `slices.Sort()` (Go 1.21+).

### Anti-Patterns

- **Writing custom Bubble/Selection Sort for production:** These O(n²) algorithms are never the right choice in Go. Use `slices.Sort` (pdqsort hybrid) for any real workload.
- **Implementing `sort.Interface` when `cmp.Ordered` suffices:** Since Go 1.21, `slices.SortFunc` with `cmp.Compare` is cleaner than defining a three-method `sort.Interface` struct.
- **Sorting a slice already in order:** Go's pdqsort detects nearly-sorted input and runs in O(n), but a hand-written Quick Sort without pivot randomization degrades to O(n²).

## 19.4. Quick Reference

| Algorithm | Time | Space | Stable | Best For |
|-----------|------|-------|--------|----------|
| <abbr title="A simple sorting algorithm repeatedly swapping adjacent elements">Bubble Sort</abbr> | <code>O(n^2)</code> | <code>O(1)</code> | Yes | Educational only |
| <abbr title="A sorting algorithm repeatedly finding the minimum element">Selection Sort</abbr> | <code>O(n^2)</code> | <code>O(1)</code> | No | Minimizing writes |
| <abbr title="A sorting algorithm building the final array one element at a time">Insertion Sort</abbr> | <code>O(n^2)</code> avg | <code>O(1)</code> | Yes | Small/nearly sorted |
| Go sort.Ints | <code>O(n log n)</code> | <code>O(log n)</code> | No | Production |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 19:</strong> Basic sorting algorithms have <code>O(n^2)</code> complexity and are primarily of educational value. <abbr title="A sorting algorithm building the final array one element at a time">Insertion Sort</abbr> remains practically relevant for small or nearly sorted datasets and serves as the base case in optimized quicksort implementations. In Go, always prefer the standard library's <code>sort</code> package for production code.
{{% /alert %}}

## See Also

- [Chapter 20: Advanced Sorting Algorithms](/docs/part-v/chapter-20/)
- [Chapter 21: Searching Algorithms](/docs/part-v/chapter-21/)
- [Chapter 54: Counting, Radix, and <abbr title="A sorting algorithm distributing elements into buckets">Bucket Sort</abbr>](/docs/part-xi/chapter-54/)
