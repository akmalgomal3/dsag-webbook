---
weight: 11200
title: "Chapter 57 - Kadane's Algorithm"
description: "Kadane's Algorithm"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The maximum subarray problem is solved by asking: do I extend the previous subarray or start fresh?</em>" — Jay Kadane</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 57 presents Kadane's algorithm — the elegant O(n) solution to the maximum subarray problem, foundational to dynamic programming thinking.
{{% /alert %}

## 57.1. The Maximum Subarray Problem

**Definition:** Given an array of integers (possibly negative), find the contiguous subarray with the largest sum. First solved in O(n) by Jay Kadane in 1984.

### The Insight

At each position, ask: "Is it better to extend the previous subarray or start a new one here?"

```
maxEndingHere = max(arr[i], maxEndingHere + arr[i])
maxSoFar = max(maxSoFar, maxEndingHere)
```

## 57.2. Algorithm

```go
func maxSubArray(arr []int) int {
    if len(arr) == 0 {
        return 0
    }
    
    maxEndingHere := arr[0]
    maxSoFar := arr[0]
    
    for i := 1; i < len(arr); i++ {
        if maxEndingHere+arr[i] > arr[i] {
            maxEndingHere = maxEndingHere + arr[i]
        } else {
            maxEndingHere = arr[i]
        }
        
        if maxEndingHere > maxSoFar {
            maxSoFar = maxEndingHere
        }
    }
    
    return maxSoFar
}
```

## 57.3. Why It Works

| State | Meaning |
|-------|---------|
| maxEndingHere | Best sum of subarray ending at current index |
| maxSoFar | Best sum seen anywhere so far |

The recurrence captures the essence of dynamic programming: the optimal solution at position i depends only on the optimal solution at position i-1.

## 57.4. Variations

| Variation | Modification |
|-----------|-------------|
| **Track indices** | Record start/end when maxSoFar updates |
| **All negative** | Return least negative (or handle separately) |
| **2D version** | Maximum submatrix — O(n³) or O(n⁴) |
| **Circular array** | Max of Kadane's or total - min subarray |

## 57.5. Decision Matrix

| Use Kadane's When... | Use Prefix Sum When... |
|----------------------|------------------------|
| Contiguous subarray required | Any subarray, query-based |
| Single pass acceptable | Multiple queries on same array |
| Simplicity paramount | Need arbitrary range sums |

### Edge Cases & Pitfalls

- **All negatives:** Kadane's returns the maximum (least negative) element.
- **Empty subarray allowed:** If empty subarray (sum 0) is allowed, initialize to 0.
- **Integer overflow:** Use larger types for big sums.

## 57.6. Quick Reference

| Aspect | Value |
|--------|-------|
| Time | O(n) |
| Space | O(1) |
| Technique | Dynamic programming |
| Key idea | Local optimum → global optimum |

| Go stdlib | Usage |
|-----------|-------|
| No direct equivalent | Implement for financial/stock analysis |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 57:</strong> Kadane's algorithm is a masterpiece of dynamic programming simplicity. In a single pass with O(1) space, it solves a problem that seems to require examining all O(n²) subarrays. The lesson transcends the specific problem: when facing "best subarray" questions, always ask if the optimal ending at position i can be derived from position i-1. If so, Kadane's insight applies.
{{% /alert %}}
