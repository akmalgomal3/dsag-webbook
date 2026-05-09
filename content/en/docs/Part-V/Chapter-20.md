---
weight: 50200
title: "Chapter 20 - Advanced Sorting Algorithms"
description: "Advanced Sorting Algorithms"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Intelligence is the ability to adapt to change.</em>" — Stephen Hawking</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 20 covers advanced sorting algorithms: Merge Sort, Quick Sort, and Heap Sort. These achieve <code>O(n log n)</code> complexity and form the backbone of real-world sorting systems.
{{% /alert %}}

## 20.1. Merge Sort

**Definition:** Merge Sort is a divide-and-conquer algorithm that divides the array into halves, recursively sorts each half, and merges the sorted halves.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Divide | <code>O(log n)</code> levels | Split array in half |
| Merge | <code>O(n)</code> per level | Combine sorted halves |
| Total | <code>O(n log n)</code> | Guaranteed |
| Space | <code>O(n)</code> | Auxiliary array |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func mergeSort(arr []int) []int {
	if len(arr) <= 1 { return arr }
	mid := len(arr) / 2
	left := mergeSort(arr[:mid])
	right := mergeSort(arr[mid:])
	return merge(left, right)
}

func merge(left, right []int) []int {
	result := make([]int, 0, len(left)+len(right))
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

func main() {
	arr := []int{38, 27, 43, 3, 9, 82, 10}
	fmt.Println(mergeSort(arr))
}
```

### Decision Matrix

| Use Merge Sort When... | Avoid If... |
|------------------------|-------------|
| Stability is required | Memory is constrained |
| Guaranteed <code>O(n log n)</code> needed | In-place sorting is mandatory |
| Linked list sorting | Random access pattern (slower cache) |

## 20.2. Quick Sort

**Definition:** Quick Sort selects a pivot, partitions the array into elements less than and greater than the pivot, and recursively sorts each partition.

### Operations & Complexity

| Case | Complexity | Condition |
|------|------------|-----------|
| Average | <code>O(n log n)</code> | Random pivot |
| Worst | <code>O(n^2)</code> | Bad pivot choices |
| Space | <code>O(log n)</code> | Recursion stack |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func quickSort(arr []int) {
	var sort func(left, right int)
	sort = func(left, right int) {
		if left >= right { return }
		pivot := partition(arr, left, right)
		sort(left, pivot-1)
		sort(pivot+1, right)
	}
	sort(0, len(arr)-1)
}

func partition(arr []int, left, right int) int {
	pivot := arr[right]
	i := left
	for j := left; j < right; j++ {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[right] = arr[right], arr[i]
	return i
}

func main() {
	arr := []int{10, 7, 8, 9, 1, 5}
	quickSort(arr)
	fmt.Println(arr)
}
```

## 20.3. Heap Sort

**Definition:** Heap Sort builds a max heap from the array, then repeatedly extracts the maximum element and places it at the end of the array.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Build heap | <code>O(n)</code> | Bottom-up heapify |
| Extract max | <code>O(log n)</code> | n times |
| Total | <code>O(n log n)</code> | Guaranteed |
| Space | <code>O(1)</code> | In-place |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func heapSort(arr []int) {
	n := len(arr)
	// Build max heap
	for i := n/2 - 1; i >= 0; i-- {
		heapify(arr, n, i)
	}
	// Extract elements
	for i := n - 1; i > 0; i-- {
		arr[0], arr[i] = arr[i], arr[0]
		heapify(arr, i, 0)
	}
}

func heapify(arr []int, n, i int) {
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

func main() {
	arr := []int{12, 11, 13, 5, 6, 7}
	heapSort(arr)
	fmt.Println(arr)
}
```

## 20.4. Decision Matrix

| Algorithm | Time | Space | Stable | Cache Friendly | Best For |
|-----------|------|-------|--------|----------------|----------|
| Merge Sort | <code>O(n log n)</code> | <code>O(n)</code> | Yes | Poor | External sorting, stability |
| Quick Sort | <code>O(n log n)</code> avg | <code>O(log n)</code> | No | Good | General purpose, in-place |
| Heap Sort | <code>O(n log n)</code> | <code>O(1)</code> | No | Poor | Memory-constrained systems |
| Go sort.Ints | <code>O(n log n)</code> | <code>O(log n)</code> | No | Excellent | Production code |

### Edge Cases & Pitfalls

- **Pivot selection:** Randomized pivot or median-of-three prevents <code>O(n^2)</code> worst case in Quick Sort.
- **Stability:** Neither Quick Sort nor Heap Sort is stable. Use Merge Sort if stability matters.
- **Go's sort:** Go uses a hybrid of Quick Sort, Heap Sort, and Insertion Sort (pdqsort in Go 1.19+).

## 20.5. Quick Reference

| Name | Go Type | Time | Space | Stable | Use Case |
|------|---------|------|-------|--------|----------|
| Merge Sort | Recursive | <code>O(n log n)</code> | <code>O(n)</code> | Yes | Linked lists, stability |
| Quick Sort | In-place | <code>O(n log n)</code> avg | <code>O(log n)</code> | No | General purpose |
| Heap Sort | In-place | <code>O(n log n)</code> | <code>O(1)</code> | No | Embedded systems |
| Go stdlib | Hybrid | <code>O(n log n)</code> | <code>O(log n)</code> | No | Always use this |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 20:</strong> Advanced sorting algorithms achieve <code>O(n log n)</code> through fundamentally different strategies: Merge Sort divides and conquers with guaranteed performance, Quick Sort partitions for cache-friendly in-place sorting, and Heap Sort uses a binary heap for minimal memory usage. In Go, always default to <code>sort.Ints()</code> or <code>slices.Sort()</code> for production.
{{% /alert %}}

## See Also

- [Chapter 19 — Basic Sorting Algorithms](/docs/Part-V/Chapter-19/)
- [Chapter 21 — Searching Algorithms](/docs/Part-V/Chapter-21/)
- [Chapter 55 — Counting, Radix, and Bucket Sort](/docs/Part-XI/Chapter-55/)

