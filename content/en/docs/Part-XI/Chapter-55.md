---
weight: 110200
title: "Chapter 55: Sliding Window and Two Pointers"
description: "Sliding Window and Two Pointers"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>If <abbr title="A straightforward approach trying all possible solutions">brute force</abbr> is <code>O(n^2)</code>, two pointers or sliding window often reduce it to <code>O(n)</code>.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 56 covers sliding window and two pointers — two fundamental techniques for solving subarray and substring problems in optimal <abbr title="An algorithm whose running time grows linearly with input size">linear time</abbr>.
{{% /alert %}}

## 56.1. The Two Pointers Technique

**Definition:** The <abbr title="A technique using two indices to traverse a data structure, typically one starting from each end or both from the start.">two pointers</abbr> technique explicitly maintains two indices moving through a sequence to isolate pairs, triplets, or partitions perfectly satisfying a set mathematical condition.

**Background & Philosophy:**
The philosophy is dynamic bounds management. Instead of running a nested loop <code>O(n^2)</code> to re-evaluate every possible sub-array combination, these algorithms maintain a "memory" of the previous state. By incrementally adding to the front and removing from the back, they reduce a quadratic <abbr title="The set of all candidate solutions in a problem">search space</abbr> into a linear <code>O(n)</code> stroll.

**Use Cases:**
Network congestion control (TCP sliding windows), video streaming buffer management, and parsing continuous streams of market data for moving averages.

**Memory Mechanics:**
Sliding Window and Two Pointers are exceptionally hardware-friendly. They operate entirely in-place (<code>O(1)</code> memory) utilizing just two integer indices (`left` and `right`). As these indices scan sequentially across a slice, they capitalize perfectly on the CPU's <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. The hardware prefetcher predicts the memory access pattern, ensuring the data is already waiting in the L1 <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> before the Go runtime even executes the loop.

### Classic: Pair Sum

Given a sorted array, find a precise pair summing exactly to a target:

```go
package main

import "fmt"

func twoSumSorted(arr []int, target int) []int {
    left, right := 0, len(arr)-1
    for left < right {
        sum := arr[left] + arr[right]
        if sum == target {
            return []int{left, right}
        } else if sum < target {
            left++
        } else {
            right--
        }
    }
    return nil
}

func main() {
    arr := []int{2, 7, 11, 15}
    fmt.Println(twoSumSorted(arr, 9)) // [0 1]
}
```

| Variation | Pointer Movement |
|-----------|-----------------|
| Opposite ends | Converge inward simultaneously |
| Same direction | Fast and slow tracking (cycle detection) |
| Partitioning | Segregation based strictly upon a mathematical condition |

## 56.2. Sliding Window

**Definition:** The <abbr title="A technique for finding a subarray or substring that satisfies a condition by maintaining a window of elements and adjusting its bounds.">sliding window</abbr> paradigm maintains a subarray/substring that satisfies a condition, expanding and contracting the window bounds as needed.

### Fixed-Size Window

Calculate the maximum sum of exactly `k` consecutive elements:

```go
package main

import "fmt"

func maxSumWindow(arr []int, k int) int {
    if len(arr) < k {
        return 0
    }
    maxSum, windowSum := 0, 0
    for i := 0; i < len(arr); i++ {
        windowSum += arr[i]
        if i >= k {
            windowSum -= arr[i-k]
        }
        if i >= k-1 && windowSum > maxSum {
            maxSum = windowSum
        }
    }
    return maxSum
}

func main() {
    arr := []int{1, 4, 2, 10, 2, 3, 1, 0, 20}
    fmt.Println(maxSumWindow(arr, 4)) // 24
}
```

### Variable-Size Window

Determine the longest substring fundamentally lacking any repeating characters:

```go
package main

import "fmt"

func lengthOfLongestSubstring(s string) int {
    charIndex := map[byte]int{}
    maxLen := 0
    start := 0
    
    for i := 0; i < len(s); i++ {
        if idx, ok := charIndex[s[i]]; ok && idx >= start {
            start = idx + 1
        }
        charIndex[s[i]] = i
        if i-start+1 > maxLen {
            maxLen = i - start + 1
        }
    }
    return maxLen
}

func main() {
    fmt.Println(lengthOfLongestSubstring("abcabcbb")) // 3
}
```

## 56.3. Decision Matrix

| Use Two Pointers When... | Use Sliding Window When... |
|--------------------------|---------------------------|
| Dealing with sorted data requiring pair conditions | Processing a strictly contiguous subarray or substring |
| Partitioning diverse arrays | Summing or averaging distinct constraints |
| Cycle detection (fast/slow algorithms) | Identifying frequency or diversity constraints |

### Edge Cases & Pitfalls

- **Empty input:** Handle empty slices or strings gracefully to prevent panics.
- **Window bounds:** Off-by-one boundary tracking errors remain profoundly common.
- **Monotonicity:** The sliding window concept relies completely on the fact that expanding/shrinking scales monotonically.
- **Duplicate elements:** Use a map to track heavy frequency counts for "at most K distinct" variants.

### Anti-Patterns

- **Two pointers on unsorted data for pair-sum:** The two-pointer pair-sum technique requires a sorted array; running it on unsorted input silently misses valid pairs.
- **Off-by-one window bounds:** Expanding `right` before checking the window constraint or shrinking `left` too aggressively are the most common sliding-window bugs — always verify index boundaries with a dry run.
- **Forgetting to handle duplicates in "longest substring" variants:** When tracking character frequency in a hash map, stale entries from earlier positions must be invalidated; skipping this produces overcounted window lengths.
- **Applying sliding window to non-monotonic constraints:** Sliding window relies on the property that expanding/shrinking monotonically satisfies/violates the constraint; if the constraint is not monotonic, the technique collapses.

## 56.4. Quick Reference

| Problem Type | Technique | Time |
|--------------|-----------|------|
| Pair sum in sorted array | Two pointers | <code>O(n)</code> |
| 3Sum | Two pointers nested | <code>O(n^2)</code> |
| Container with most water | Two pointers | <code>O(n)</code> |
| Longest substring K distinct | Sliding window | <code>O(n)</code> |
| Minimum window substring | Sliding window | <code>O(n)</code> |

| Go stdlib | Usage |
|-----------|-------|
| `strings` | Use `Contains` and `Index` for simplistic, pre-packaged substring operations |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 55:</strong> Two pointers and sliding window are fundamental patterns for linear-time array and string processing. They replace nested loops with single passes, exploiting ordering or contiguous structure. Mastering these patterns means recognizing when a problem asks for "pairs," "subarrays," or "substrings" and choosing the right traversal strategy.
{{% /alert %}}

## See Also

- [Chapter 54: Counting, Radix, and <abbr title="A sorting algorithm distributing elements into buckets">Bucket Sort</abbr>](/docs/part-xi/chapter-54/)
- [Chapter 56: Kadane's Algorithm](/docs/part-xi/chapter-56/)
- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/part-vi/chapter-23/)
