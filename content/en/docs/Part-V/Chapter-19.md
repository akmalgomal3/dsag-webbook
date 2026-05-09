---
weight: 5100
title: "Chapter 19 - Basic Sorting Algorithms"
description: "Basic Sorting Algorithms"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Sorting is the process of arranging elements in a specific order, typically ascending or descending.</em>"</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 19 covers basic sorting algorithms: Bubble Sort, Selection Sort, and Insertion Sort. Understand their mechanics, complexity, and when they remain relevant in modern Go.
{{% /alert %}}

## 19.1. Bubble Sort

**Definition:** Bubble Sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. Each pass places the next largest element in its correct position.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Comparisons | <code>O(n^2)</code> | n(n-1)/2 comparisons |
| Swaps | <code>O(n^2)</code> worst | Adjacent elements swapped |
| Best case | <code>O(n)</code> | Already sorted (with optimization) |
| Space | <code>O(1)</code> | In-place |

### Idiomatic Go Implementation

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

- **Stability:** Bubble Sort and Insertion Sort are stable; Selection Sort is not.
- **Adaptive:** Insertion Sort performs well on nearly sorted data (e.g., <code>O(n)</code> for sorted input).
- **Go's built-in:** For production, always use `sort.Ints()` or `slices.Sort()` (Go 1.21+).

## 19.4. Quick Reference

| Algorithm | Time | Space | Stable | Best For |
|-----------|------|-------|--------|----------|
| Bubble Sort | <code>O(n^2)</code> | <code>O(1)</code> | Yes | Educational only |
| Selection Sort | <code>O(n^2)</code> | <code>O(1)</code> | No | Minimizing writes |
| Insertion Sort | <code>O(n^2)</code> avg | <code>O(1)</code> | Yes | Small/nearly sorted |
| Go sort.Ints | <code>O(n log n)</code> | <code>O(log n)</code> | No | Production |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 19:</strong> Basic sorting algorithms have <code>O(n^2)</code> complexity and are primarily of educational value. Insertion Sort remains practically relevant for small or nearly sorted datasets and serves as the base case in optimized quicksort implementations. In Go, always prefer the standard library's <code>sort</code> package for production code.
{{% /alert %}}
