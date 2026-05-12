---
weight: 110100
title: "Chapter 55: Counting, Radix, and Bucket Sort"
description: "Counting, Radix, and Bucket Sort"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Linear-time sorting is not magic — it is the reward of making strong assumptions about your data.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 55 explores linear-time sorting algorithms — <abbr title="An integer sorting algorithm using frequency counting">counting sort</abbr>, <abbr title="A sorting algorithm processing digits individually">radix sort</abbr>, and <abbr title="A sorting algorithm distributing elements into buckets">bucket sort</abbr> — that beat the <code>O(n log n)</code> comparison bound by exploiting data structure.
{{% /alert %}}

## 55.1. Beyond Comparison Sorting

**Definition:** <abbr title="Sorting algorithms that do not rely on comparing elements, instead using assumptions about the data distribution.">Non-comparison sorts</abbr> achieve <code>O(n)</code> time by making assumptions about the input domain. They aggressively trade general applicability for raw speed.

**Background & Philosophy:**
The philosophy is breaking the comparison barrier. Mathematical proofs guarantee that comparison-based sorting (Merge, Quick) can never be faster than <code>O(n log n)</code>. Non-comparison sorts (Counting, Radix) completely bypass this law by making strict assumptions about the data (e.g., "all elements are integers between 0 and k"). They trade universal applicability for raw, linear speed.

**Use Cases:**
Rendering engines sorting 3D polygons by depth, network routers organizing packets by priority flags, and sorting massive arrays of dates/timestamps.

**Memory Mechanics:**
Non-comparison sorts are notoriously memory-hungry. <abbr title="An integer sorting algorithm using frequency counting">Counting Sort</abbr> allocates an auxiliary array of size `k`. If `k` is 1 billion, it allocates a massive chunk of <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> just to count. <abbr title="A sorting algorithm processing digits individually">Radix Sort</abbr> performs multiple passes, often allocating and copying data into 10 or 256 distinct "buckets" during each pass. While algorithmically <code>O(n)</code>, the constant <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr> and heavy <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> tracing caused by these bucket arrays in Go can make them ironically slower than a highly-optimized in-place Quick Sort for datasets that easily fit within the L1/L2 caches.

| Algorithm | Assumption | Time | Space |
|-----------|-----------|------|-------|
| <abbr title="An integer sorting algorithm using frequency counting">Counting sort</abbr> | Integers in range [0, k] | <code>O(n + k)</code> | <code>O(k)</code> |
| <abbr title="A sorting algorithm processing digits individually">Radix sort</abbr> | d-digit integers | <code>O(d(n + k))</code> | <code>O(n + k)</code> |
| <abbr title="A sorting algorithm distributing elements into buckets">Bucket sort</abbr> | Uniform distribution | <code>O(n)</code> avg | <code>O(n)</code> |

## 55.2. <abbr title="An integer sorting algorithm using frequency counting">Counting Sort</abbr>

Count occurrences, then compute <abbr title="An array where each element is the sum of all preceding elements, enabling O(1) range sum queries.">prefix sums</abbr> for exact array positions.

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

Sort digit by digit from least significant to most significant, rigidly utilizing counting sort as the stable mathematical subroutine.

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

Distribute elements into distinct physical buckets based entirely on range, sort each bucket individually (often utilizing <abbr title="A sorting algorithm that builds the final sorted array one item at a time.">insertion sort</abbr>), then sequentially concatenate them.

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

- **Counting sort:** k >> n completely ruins performance, causing it to run vastly slower than comparison sorts.
- **Radix sort:** `d log n` may easily exceed `log n` for remarkably large numbers.
- **Bucket sort:** A highly skewed distribution rapidly degenerates performance to <code>O(n^2)</code>.
- **Stability:** Absolutely mandatory for radix sort to function; counting sort natively provides this stability.

## 55.6. Quick Reference

| Algorithm | Best Case | Worst Case | Stable? |
|-----------|-----------|------------|---------|
| Counting | <code>O(n + k)</code> | <code>O(n + k)</code> | Yes |
| Radix (LSD) | <code>O(d(n + k))</code> | <code>O(d(n + k))</code> | Yes |
| Bucket | <code>O(n)</code> | <code>O(n^2)</code> | Yes |

| Go stdlib | Usage |
|-----------|-------|
| `sort.Ints` | Standard <abbr title="A sorting algorithm that only compares elements">comparison sort</abbr> (quicksort/heap sort hybrid) |
| No native non-<abbr title="A sorting algorithm that only compares elements">comparison sort</abbr> | Implement manually for specialized, integer-bound cases |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 55:</strong> Linear-time sorting algorithms prove that the <code>O(n log n)</code> comparison <abbr title="A function that grows no faster than the given function">lower bound</abbr> applies only when you know nothing about your data. By deliberately exploiting integer ranges, digit structure, or uniform distributions, counting, radix, and <abbr title="A sorting algorithm distributing elements into buckets">bucket sort</abbr> achieve <code>O(n)</code> — a powerful reminder that algorithmic efficiency consistently emerges from deeply understanding your specific problem domain.
{{% /alert %}}

## See Also

- [Chapter 19: Basic Sorting Algorithms](/docs/Part-V/Chapter-19/)
- [Chapter 20: Advanced Sorting Algorithms](/docs/Part-V/Chapter-20/)
- [Chapter 57: Kadane's Algorithm](/docs/Part-XI/Chapter-57/)
