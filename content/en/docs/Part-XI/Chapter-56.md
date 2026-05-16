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
<strong>"<em>Maximum subarray problem asks: extend previous subarray or start fresh?</em>" — Jay Kadane</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 57 presents <abbr title="An O(n) algorithm that finds the maximum sum of any contiguous subarray using dynamic programming.">Kadane's algorithm</abbr>: an <code>O(n)</code> solution for maximum subarray problem and foundation for <abbr title="A method combining solutions to overlapping subproblems">dynamic programming</abbr>.
{{% /alert %}}

## 56.1. The Maximum Subarray Problem

**Definition:** Find contiguous subarray with largest sum in integer array. Solved in <code>O(n)</code> by Jay Kadane in 1984.

**Background & Philosophy:**
Kadane's algorithm applies <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>. Algorithm asks localized question at each step. Running sum below current element forces fresh start.

**Use Cases:**
Algorithmic finance identifies profitable trade sequences. Genomic sequence analysis uses negative scores for mutations and positive scores for matches.

**Memory Mechanics:**
<abbr title="An O(n) algorithm that finds the maximum sum of any contiguous subarray using dynamic programming.">Kadane's Algorithm</abbr> achieves theoretical maximum performance. <code>O(1)</code> memory requires two integer variables (`maxEndingHere` and `maxSoFar`). Single forward scan avoids <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocations and <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> triggers. Variables reside in CPU registers for maximum bandwidth.

### The Insight

At each position: extend previous subarray or start new one.

```text
maxEndingHere = max(arr[i], maxEndingHere + arr[i])
maxSoFar = max(maxSoFar, maxEndingHere)
```

## 56.2. Algorithm

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

## 56.3. Why It Works

| State | Meaning |
|-------|---------|
| maxEndingHere | Best sum of the subarray strictly ending at the current index |
| maxSoFar | Absolute best sum witnessed anywhere so far |

Recurrence defines <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr>: optimal solution at position i depends solely on optimal solution at position i-1.

## 56.4. Variations

| Variation | Modification |
|-----------|-------------|
| **Track indices** | Record start/end positions when maxSoFar updates |
| **All negative** | Returns least negative element |
| **2D version** | Maximum submatrix typically requires <code>O(n^3)</code> or <code>O(n^4)</code> |
| **Circular array** | Yields max of Kadane's against total sum minus min subarray |

## 56.5. Decision Matrix

| Use Kadane's When... | Use Prefix Sum When... |
|----------------------|------------------------|
| Contiguous subarray is mandatory | Addressing arbitrary query-based subarray |
| Single pass is structurally acceptable | Conducting multiple queries on same array |
| Raw simplicity is paramount | Handling arbitrary range sums |

### Edge Cases & Pitfalls

- **All negatives:** Standard implementation returns maximum element.
- **Empty subarray:** Initialize trackers to 0 if sum of 0 is permitted.
- **Integer overflow:** Use <code>int64</code> for handling large sums.

### Anti-Patterns

- **Returning 0 for all-negative arrays:** Document choice explicitly if empty subarray is valid.
- **Non-contiguous problems:** Kadane's solves contiguous subarray only. Sum positive numbers for subsequence.
- **Subarray vs subsequence:** Subarray is contiguous. Subsequence is not. Kadane's yields incorrect results for subsequences.
- **Integer overflow:** Running sum exceeds int bounds. Use <code>int64</code> or <code>math/big</code> for large values.

## 56.6. Quick Reference

| Aspect | Value |
|--------|-------|
| Time | <code>O(n)</code> |
| Space | <code>O(1)</code> |
| Technique | <abbr title="A method combining solutions to overlapping subproblems">Dynamic programming</abbr> paradigm |
| Key idea | Transform <abbr title="A solution better than neighbors but not globally best">local optimum</abbr> into <abbr title="The best possible solution over the entire search space">global optimum</abbr> |

| Go stdlib | Usage |
|-----------|-------|
| No direct equivalent | Requires manual implementation |


{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 56:</strong> Kadane's algorithm demonstrates <abbr title="A method combining solutions to overlapping subproblems">dynamic programming</abbr> principles. Single pass with <code>O(1)</code> space solves <code>O(n^2)</code> problem. Core lesson: derive optimal state at position i from position i-1.
{{% /alert %}}

## See Also

- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/part-vi/chapter-23/)
- [Chapter 54: Counting, Radix, and <abbr title="A sorting algorithm distributing elements into buckets">Bucket Sort</abbr>](/docs/part-xi/chapter-54/)
- [Chapter 55: Sliding Window and Two Pointers](/docs/part-xi/chapter-55/)