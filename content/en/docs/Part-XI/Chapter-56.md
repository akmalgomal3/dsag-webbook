---
weight: 110300
title: "Chapter 56: Kadane's Algorithm"
description: "Kadane's Algorithm"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The maximum subarray problem is solved by asking: do I extend the previous subarray or start fresh?</em>" : Jay Kadane</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 57 presents <abbr title="An O(n) algorithm that finds the maximum sum of any contiguous subarray using dynamic programming.">Kadane's algorithm</abbr> — an <code>O(n)</code> solution for the maximum subarray problem, serving as a foundation for <abbr title="A method combining solutions to overlapping subproblems">dynamic programming</abbr> thinking.
{{% /alert %}}

## 57.1. The Maximum Subarray Problem

**Definition:** Given an array of integers (often containing negative numbers), find the contiguous subarray with the largest sum. First solved in <code>O(n)</code> by Jay Kadane in 1984.

**Background & Philosophy:**
The philosophy is aggressive amnesia. Kadane's algorithm is a clean application of <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>: it asks a localized question at each step. "Is the accumulated baggage of the past dragging me down so much that I'm better off starting fresh right now?" If the running sum drops below the current element, it cuts ties with the past.

**Use Cases:**
Identifying the most profitable sequence of trades in algorithmic finance, and genomic sequence analysis where negative scores represent mutations and positive scores represent matches.

**Memory Mechanics:**
<abbr title="An O(n) algorithm that finds the maximum sum of any contiguous subarray using dynamic programming.">Kadane's Algorithm</abbr> achieves maximum theoretical performance. It requires precisely <code>O(1)</code> memory—merely two integer variables (`maxEndingHere` and `maxSoFar`). Because it only performs a single, forward-only scan over the `[]int` slice, it requires zero <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocations and never triggers the Go <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr>. These variables reside completely within the CPU registers, allowing the algorithm to execute at the sheer maximum bandwidth of the memory bus.

### The Insight

At each precise position, confidently ask: "Is it mathematically better to extend the previous subarray or start a completely new one precisely here?"

```text
maxEndingHere = max(arr[i], maxEndingHere + arr[i])
maxSoFar = max(maxSoFar, maxEndingHere)
```

## 57.2. Algorithm

### Idiomatic Go Implementation

```go
package main

import "fmt"

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

func main() {
    arr := []int{-2, 1, -3, 4, -1, 2, 1, -5, 4}
    fmt.Println("Max subarray sum:", maxSubArray(arr)) // 6 (subarray: [4, -1, 2, 1])
}
```

## 57.3. Why It Works

| State | Meaning |
|-------|---------|
| maxEndingHere | Best sum of the subarray strictly ending at the current index |
| maxSoFar | Absolute best sum witnessed anywhere so far |

The recurrence captures the unyielding essence of <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr>: the optimal solution exactly at position i depends completely and only on the optimal solution firmly established at position i-1.

## 57.4. Variations

| Variation | Modification |
|-----------|-------------|
| **Track indices** | Accurately record start/end positions whenever maxSoFar updates |
| **All negative** | Mathematically returns the least negative element (or must be handled distinctly) |
| **2D version** | Maximum submatrix typically requiring <code>O(n^3)</code> or <code>O(n^4)</code> |
| **Circular array** | Yields the max of Kadane's against total sum - min subarray |

## 57.5. Decision Matrix

| Use Kadane's When... | Use Prefix Sum When... |
|----------------------|------------------------|
| A strictly contiguous subarray is mandatory | Addressing any arbitrary subarray, strictly query-based |
| A solitary single pass is structurally acceptable | Conducting multiple varied queries on the exact same array |
| Raw, unchecked simplicity is paramount | Handling requirements for mathematically arbitrary range sums |

### Edge Cases & Pitfalls

- **All negatives:** The standard implementation of Kadane's algorithm confidently returns the absolute maximum (least negative) element.
- **Empty subarray allowed:** If a totally empty subarray (summing to 0) is permitted by business logic, initialize the trackers rigidly to 0.
- **Integer overflow:** Utilize wider 64-bit integer tracking types (`int64`) for handling exceptionally huge sums safely.

## 57.6. Quick Reference

| Aspect | Value |
|--------|-------|
| Time | <code>O(n)</code> |
| Space | <code>O(1)</code> |
| Technique | <abbr title="A method combining solutions to overlapping subproblems">Dynamic programming</abbr> paradigm |
| Key idea | Transform <abbr title="A solution better than neighbors but not globally best">local optimum</abbr> cleanly into <abbr title="The best possible solution over the entire search space">global optimum</abbr> |

| Go stdlib | Usage |
|-----------|-------|
| No direct equivalent | Requires manual implementation specifically tailored for financial or stock tracking |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 56:</strong> Kadane's algorithm is a clean demonstration of <abbr title="A method combining solutions to overlapping subproblems">dynamic programming</abbr> principles. In a single pass with <code>O(1)</code> auxiliary space, it solves a problem that intuitively seems to require examining all <code>O(n^2)</code> possible subarrays. The core lesson: whenever tackling "best subarray" questions, ask if the optimal state ending at position i can be derived from position i-1. If it can, Kadane's insight applies.
{{% /alert %}}

## See Also

- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/part-vi/chapter-23/)
- [Chapter 54: Counting, Radix, and <abbr title="A sorting algorithm distributing elements into buckets">Bucket Sort</abbr>](/docs/part-xi/chapter-54/)
- [Chapter 55: Sliding Window and Two Pointers](/docs/part-xi/chapter-55/)
