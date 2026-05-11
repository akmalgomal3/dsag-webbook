---
weight: 110300
title: "Chapter 57: Kadane's Algorithm"
description: "Kadane's Algorithm"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The maximum subarray problem is solved by asking: do I extend the previous subarray or start fresh?</em>" : Jay Kadane</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 57 presents <abbr title="An O(n) algorithm that finds the maximum sum of any contiguous subarray using dynamic programming.">Kadane's algorithm</abbr> — the mathematically elegant <code>O(n)</code> solution resolving the maximum subarray problem, serving as an outstanding foundation to dynamic programming thinking.
{{% /alert %}}

## 57.1. The Maximum Subarray Problem

**Definition:** Given an array of integers (often containing negative numbers), seamlessly find the strictly contiguous subarray offering the absolute largest internal sum. First solved flawlessly in <code>O(n)</code> by Jay Kadane in 1984.

**Background & Philosophy:**
The philosophy is aggressive amnesia. Kadane’s is the ultimate distillation of Dynamic Programming. It constantly asks a localized question: "Is the accumulated baggage of the past dragging me down so much that I'm better off starting entirely fresh right now?" If the running sum drops below the current element, it fiercely cuts ties with the past.

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
| Technique | Dynamic programming paradigm |
| Key idea | Transform local optimum cleanly into global optimum |

| Go stdlib | Usage |
|-----------|-------|
| No direct equivalent | Requires manual implementation specifically tailored for financial or stock tracking |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 57:</strong> Kadane's algorithm acts as an absolute masterpiece of dynamic programming simplicity. In a blistering single pass executing with merely <code>O(1)</code> auxiliary space, it cleanly solves a complex problem that intuitively seems to mandate rigorously examining all <code>O(n^2)</code> possible subarrays. The core mathematical lesson flawlessly transcends the specific problem: whenever tackling "best subarray" questions, instantly ask if the optimal state ending at position i can be efficiently derived directly from position i-1. If it genuinely can, Kadane's profound insight applies.
{{% /alert %}}

## See Also

- [Chapter 24: Dynamic Programming](/docs/Part-VI/Chapter-24/)
- [Chapter 55: Counting, Radix, and Bucket Sort](/docs/Part-XI/Chapter-55/)
- [Chapter 56: Sliding Window and Two Pointers](/docs/Part-XI/Chapter-56/)
