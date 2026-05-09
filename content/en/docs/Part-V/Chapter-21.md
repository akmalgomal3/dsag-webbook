---
weight: 50300
title: "Chapter 21 - Searching Algorithms"
description: "Searching Algorithms"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The art of programming is the art of organizing complexity.</em>" — Edsger Dijkstra</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 21 covers searching algorithms: linear search, binary search, and interpolation search. Learn when each algorithm is appropriate and how to implement them idiomatically in Go using the standard library.
{{% /alert %}}

## 21.1. Linear Search

**Definition:** Linear search sequentially checks each element until the target is found or the end is reached. It works on any data structure supporting traversal.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Search | <code>O(n)</code> | Scan every element |
| Best case | <code>O(1)</code> | Target at first position |
| Space | <code>O(1)</code> | No extra memory |

### Idiomatic Go Implementation

Use a simple loop. For slices, the built-in approach is often sufficient.

```go
package main

import "fmt"

func linearSearch(arr []int, target int) int {
	for i, v := range arr {
		if v == target { return i }
	}
	return -1
}

func main() {
	arr := []int{5, 2, 8, 1, 9, 3}
	fmt.Println(linearSearch(arr, 8)) // 2
	fmt.Println(linearSearch(arr, 7)) // -1
}
```

## 21.2. Binary Search

**Definition:** Binary search repeatedly divides a sorted array in half, eliminating half of the remaining elements with each comparison. It requires the data to be sorted.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Search | <code>O(log n)</code> | Halve search space each step |
| Precondition | Sorted data | Must sort first if unsorted |
| Space | <code>O(1)</code> | Iterative version |

### Idiomatic Go Implementation

Use `sort.Search` from the standard library for production code.

```go
package main

import (
	"fmt"
	"sort"
)

func binarySearch(arr []int, target int) int {
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
	fmt.Println(binarySearch(arr, 7)) // 3
	
	// Idiomatic: use sort.Search
	idx := sort.Search(len(arr), func(i int) bool { return arr[i] >= 7 })
	fmt.Println(idx) // 3
}
```

### Decision Matrix

| Use Binary Search When... | Avoid If... |
|---------------------------|-------------|
| Data is sorted (or can be sorted once) | Data changes frequently |
| Need multiple searches on same dataset | Only searching once on small data |
| Memory is constrained | Data is unsorted and sorting cost exceeds benefit |

### Edge Cases & Pitfalls

- **Integer overflow:** Use `mid := left + (right-left)/2`, not `(left+right)/2`.
- **Off-by-one:** Ensure loop condition is `left <= right` for inclusive bounds.
- **Duplicates:** Standard binary search returns any matching index, not first/last.

## 21.3. Interpolation Search

**Definition:** Interpolation search estimates the position of the target value using linear interpolation, making it <code>O(log log n)</code> for uniformly distributed data.

### Operations & Complexity

| Case | Complexity | Condition |
|------|------------|-----------|
| Average | <code>O(log log n)</code> | Uniformly distributed data |
| Worst | <code>O(n)</code> | Exponentially distributed data |
| Best | <code>O(1)</code> | Target at interpolated position |

### Idiomatic Go Implementation

```go
package main

import "fmt"

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

func main() {
	arr := []int{10, 20, 30, 40, 50, 60, 70, 80}
	fmt.Println(interpolationSearch(arr, 50)) // 4
}
```

## 21.4. Quick Reference

| Algorithm | Go Type | Time | Space | Precondition |
|-----------|---------|------|-------|--------------|
| Linear Search | Loop over `[]T` | <code>O(n)</code> | <code>O(1)</code> | None |
| Binary Search | `sort.Search` | <code>O(log n)</code> | <code>O(1)</code> | Sorted data |
| Interpolation Search | Custom | <code>O(log log n)</code> avg | <code>O(1)</code> | Sorted + uniform |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 21:</strong> Choose linear search for unsorted or small datasets, binary search for sorted data requiring repeated queries, and interpolation search for large uniformly distributed datasets. In Go, always prefer `sort.Search` for binary search in production code.
{{% /alert %}}
