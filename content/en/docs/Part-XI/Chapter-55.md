---
weight: 110100
title: "Chapter 55 - Counting, Radix, and Bucket Sort"
description: "Counting, Radix, and Bucket Sort"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Linear-time sorting is not magic — it is the reward of making strong assumptions about your data.</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 55 explores linear-time sorting algorithms — counting sort, radix sort, and bucket sort — that beat the O(n log n) comparison bound by exploiting data structure.
{{% /alert %}}

## 55.1. Beyond Comparison Sorting

**Definition:** <abbr title="Sorting algorithms that do not rely on comparing elements, instead using assumptions about the data distribution.">Non-comparison sorts</abbr> achieve O(n) time by making assumptions about the input domain. They trade generality for speed.

| Algorithm | Assumption | Time | Space |
|-----------|-----------|------|-------|
| Counting sort | Integers in range [0, k] | O(n + k) | O(k) |
| Radix sort | d-digit integers | O(d(n + k)) | O(n + k) |
| Bucket sort | Uniform distribution | O(n) avg | O(n) |

## 55.2. Counting Sort

Count occurrences, then compute prefix sums for positions.

```go
func countingSort(arr []int, max int) []int {
    count := make([]int, max+1)
    for _, v := range arr {
        count[v]++
    }
    
    // Prefix sum gives positions
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
```

## 55.3. Radix Sort

Sort digit by digit from least significant to most significant, using counting sort as the stable subroutine.

| Variant | Order | Stable? |
|---------|-------|---------|
| LSD | Least significant digit first | Yes |
| MSD | Most significant digit first | Yes (with recursion) |

### Idiomatic Go: LSD Radix Sort

```go
func radixSort(arr []int) {
    max := maxElement(arr)
    for exp := 1; max/exp > 0; exp *= 10 {
        countingSortByDigit(arr, exp)
    }
}
```

## 55.4. Bucket Sort

Distribute elements into buckets based on range, sort each bucket individually (often with insertion sort), then concatenate.

| Step | Time |
|------|------|
| Distribute to buckets | O(n) |
| Sort each bucket | O(n) avg (if uniform) |
| Concatenate | O(n) |

## 55.5. Decision Matrix

| Use Counting Sort When... | Use Radix Sort When... | Use Bucket Sort When... |
|---------------------------|------------------------|------------------------|
| Small integer range | Large integers, fixed digits | Uniform distribution known |
| k = O(n) | d is small | Floating-point numbers |

### Edge Cases & Pitfalls

- **Counting sort:** k >> n makes it worse than comparison sort.
- **Radix sort:** d log n may exceed log n for very large numbers.
- **Bucket sort:** Skewed distribution degenerates to O(n²).
- **Stability:** Required for radix sort; counting sort is naturally stable.

## 55.6. Quick Reference

| Algorithm | Best Case | Worst Case | Stable? |
|-----------|-----------|------------|---------|
| Counting | O(n + k) | O(n + k) | Yes |
| Radix (LSD) | O(d(n + k)) | O(d(n + k)) | Yes |
| Bucket | O(n) | O(n²) | Yes |

| Go stdlib | Usage |
|-----------|-------|
| `sort.Ints` | Comparison sort (quicksort/heap sort) |
| No native non-comparison sort | Implement for specialized cases |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 55:</strong> Linear-time sorting algorithms prove that the O(n log n) comparison lower bound applies only when you know nothing about your data. By exploiting integer ranges, digit structure, or uniform distributions, counting, radix, and bucket sort achieve O(n) — a powerful reminder that algorithmic efficiency often comes from understanding your problem domain, not just your algorithm textbook.
{{% /alert %}}

## See Also

- [Chapter 19 — Basic Sorting Algorithms](/docs/Part-V/Chapter-19/)
- [Chapter 20 — Advanced Sorting Algorithms](/docs/Part-V/Chapter-20/)
- [Chapter 57 — Kadane's Algorithm](/docs/Part-XI/Chapter-57/)

