---
weight: 110100
title: "Chapter 54: Counting, Radix, and Bucket Sort"
description: "Counting, Radix, and Bucket Sort"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Linear-time sorting requires data assumptions: reward of strong constraints.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Linear-time sorting beats <code>O(n log n)</code> bound: counting sort, radix sort, and bucket sort exploit data structure.
{{% /alert %}}

## 55.1. Beyond Comparison Sorting

**Definition:** <abbr title="Sorting algorithms that do not rely on comparing elements, instead using assumptions about the data distribution.">Non-comparison sorts</abbr> achieve <code>O(n)</code> time. Assumptions trade generality for speed.

**Background & Philosophy:**
Comparison-based sorting (Merge, Quick) has <code>O(n log n)</code> limit. Non-comparison sorts bypass limits. Algorithms assume data constraints: raw speed results.

**Use Cases:**
3D rendering sorts polygons by depth. Network routers organize packets by priority. Systems sort massive date arrays.

**Memory Mechanics:**
Non-comparison sorts consume high memory. Counting Sort needs <code>O(k)</code> array. Radix Sort uses multiple bucket passes. Cache misses and GC overhead impact Go performance. Quicksort often faster for small cached data.

| Algorithm | Assumption | Time | Space |
|-----------|-----------|------|-------|
| <abbr title="An integer sorting algorithm using frequency counting">Counting sort</abbr> | Integers in range [0, k] | <code>O(n + k)</code> | <code>O(k)</code> |
| <abbr title="A sorting algorithm processing digits individually">Radix sort</abbr> | d-digit integers | <code>O(d(n + k))</code> | <code>O(n + k)</code> |
| <abbr title="A sorting algorithm distributing elements into buckets">Bucket sort</abbr> | Uniform distribution | <code>O(n)</code> avg | <code>O(n)</code> |

## 55.2. <abbr title="An integer sorting algorithm using frequency counting">Counting Sort</abbr>

Counting Sort tracks occurrences. Prefix sums determine indices.

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

```go
package main

import "fmt"

func countingSort(arr []int, max int) []int {
    count := make([]int, max+1)
    for _, v := range arr {
        count[v]++
    }
    
    // Prefix sum gives exact sequential positions
    for i := 1; i <= max; i++ {
        count[i] += count[i-1]
    }
    
    output := make([]int, len(arr))
    for i := len(arr) - 1; i >= 0; i-- {
        v := arr[i]
        count[v]--
        output[count[v]] = v
    }
    
    return output
}

func main() {
    arr := []int{4, 2, 2, 8, 3, 3, 1}
    fmt.Println(countingSort(arr, 8)) // [1 2 2 3 3 4 8]
}
```

## 55.3. Radix Sort

Radix Sort sorts digit by digit. Least significant first: uses stable counting sort subroutine.

| Variant | Order | Stable? |
|---------|-------|---------|
| LSD | Least significant digit first | Yes |
| MSD | Most significant digit first | Yes (with recursion) |

### Idiomatic Go: LSD Radix Sort

```go
package main

import "fmt"

func maxElement(arr []int) int {
    max := arr[0]
    for _, v := range arr {
        if v > max {
            max = v
        }
    }
    return max
}

func countingSortByDigit(arr []int, exp int) {
    n := len(arr)
    output := make([]int, n)
    count := make([]int, 10)

    for i := 0; i < n; i++ {
        index := (arr[i] / exp) % 10
        count[index]++
    }

    for i := 1; i < 10; i++ {
        count[i] += count[i-1]
    }

    for i := n - 1; i >= 0; i-- {
        index := (arr[i] / exp) % 10
        output[count[index]-1] = arr[i]
        count[index]--
    }

    for i := 0; i < n; i++ {
        arr[i] = output[i]
    }
}

func radixSort(arr []int) {
    if len(arr) == 0 {
        return
    }
    max := maxElement(arr)
    for exp := 1; max/exp > 0; exp *= 10 {
        countingSortByDigit(arr, exp)
    }
}

func main() {
    arr := []int{170, 45, 75, 90, 802, 24, 2, 66}
    radixSort(arr)
    fmt.Println(arr)
}
```

## 55.4. Bucket Sort

Bucket Sort distributes elements to ranges. Individual buckets sort separately. Concat results in linear time.

| Step | Time |
|------|------|
| Distribute to buckets | <code>O(n)</code> |
| Sort each bucket | <code>O(n)</code> avg (if uniformly distributed) |
| Concatenate | <code>O(n)</code> |

## 55.5. Decision Matrix

| Use Counting Sort When... | Use Radix Sort When... | Use Bucket Sort When... |
|---------------------------|------------------------|------------------------|
| Small integer range exists | Large integers, fixed digits | Uniform distribution known |
| k = <code>O(n)</code> | d is small | Processing floating-point numbers |

### Edge Cases & Pitfalls

- **Counting sort:** Large <code>k</code> range ruins performance.
- **Radix sort:** Large numbers increase digit count pass overhead.
- **Bucket sort:** Skewed distribution leads to <code>O(n^2)</code>.
- **Stability:** Radix sort requires stable subroutine.

### Anti-Patterns

- **Large k range:** Wastes memory. Comparison sort preferred if <code>k >> n</code>.
- **Floating-point numbers:** Radix sort needs bit-level manipulation.
- **Non-uniform data:** Skewed input breaks <code>O(n)</code> guarantee.
- **Ignoring constants:** Comparison sorts often beat <code>O(n)</code> for small sets.

## 55.6. Quick Reference

| Algorithm | Best Case | Worst Case | Stable? |
|-----------|-----------|------------|---------|
| Counting | <code>O(n + k)</code> | <code>O(n + k)</code> | Yes |
| Radix (LSD) | <code>O(d(n + k))</code> | <code>O(d(n + k))</code> | Yes |
| Bucket | <code>O(n)</code> | <code>O(n^2)</code> | Yes |

| Go stdlib | Usage |
|-----------|-------|
| <code>sort.Ints</code> | Standard comparison sort: quicksort/heap sort hybrid. |
| No native non-comparison sort | Implement manually for specialized, integer-bound cases. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 54:</strong> Linear-time sorting proves <code>O(n log n)</code> limit is conditional. Exploiting range or structure yields <code>O(n)</code> efficiency. Performance comes from domain knowledge.
{{% /alert %}}

## See Also

- [Chapter 19: Basic Sorting Algorithms](/docs/part-v/chapter-19/)
- [Chapter 20: Advanced Sorting Algorithms](/docs/part-v/chapter-20/)
- [Chapter 56: Kadane's Algorithm](/docs/part-xi/chapter-56/)
