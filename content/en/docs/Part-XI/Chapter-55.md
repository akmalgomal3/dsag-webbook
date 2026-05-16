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
<strong>"<em>Brute force is <code>O(n^2)</code>. Two pointers or sliding window yield <code>O(n)</code>.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 56 covers sliding window and two pointers: fundamental techniques for solving subarray and substring problems in <code>O(n)</code> time.
{{% /alert %}}

## 56.1. The Two Pointers Technique

**Definition:** <abbr title="A technique using two indices to traverse a data structure, typically one starting from each end or both from the start.">Two pointers</abbr> technique uses two indices. Sequence traversal isolates pairs, triplets, or partitions satisfying conditions.

**Background & Philosophy:**
Dynamic bounds management avoids <code>O(n^2)</code> nested loops. Algorithms maintain previous state. Incremental updates reduce search space to <code>O(n)</code>.

**Use Cases:**
TCP sliding windows manage network congestion. Video streaming manages buffers. Market data parsing calculates moving averages.

**Memory Mechanics:**
Techniques are hardware-friendly. <code>O(1)</code> memory: uses two indices. Sequential scan leverages spatial locality. Hardware prefetcher loads L1 cache early.

### Classic: Pair Sum

Pair Sum: find two elements in sorted array matching target.

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
| Same direction | Fast and slow tracking |
| Partitioning | Segregation based on mathematical condition |

## 56.2. Sliding Window

**Definition:** <abbr title="A technique for finding a subarray or substring that satisfies a condition by maintaining a window of elements and adjusting its bounds.">Sliding window</abbr> maintains subarray/substring satisfying condition. Bounds expand and contract.

### Fixed-Size Window

Fixed-Size Window: calculate maximum sum of <code>k</code> consecutive elements.

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

Variable-Size Window: find longest substring without repeating characters.

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
| Sorted data requiring pair conditions | Contiguous subarray or substring processing |
| Partitioning diverse arrays | Summing or averaging constraints |
| Cycle detection (fast/slow) | Frequency or diversity constraints |

### Edge Cases & Pitfalls

- **Empty input:** Handle gracefully to avoid panics.
- **Window bounds:** Off-by-one boundary errors are common.
- **Monotonicity:** Concept relies on monotonic expansion/contraction.
- **Duplicate elements:** Use maps for frequency tracking.

### Anti-Patterns

- **Unsorted data:** Two pointers requires sorting for pair-sum.
- **Off-by-one errors:** Check boundaries with dry runs.
- **Stale map entries:** Invalidate old positions in frequency tracking.
- **Non-monotonic constraints:** Techniques fail if property is lost.

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
| <code>strings</code> | <code>Contains</code> and <code>Index</code> provide basic substring operations. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 55:</strong> Two pointers and sliding window yield linear-time processing. Single passes replace nested loops. Patterns apply to pairs, subarrays, and substrings.
{{% /alert %}}

## See Also

- [Chapter 54: Counting, Radix, and Bucket Sort](/docs/part-xi/chapter-54/)
- [Chapter 56: Kadane's Algorithm](/docs/part-xi/chapter-56/)
- [Chapter 23: Dynamic Programming](/docs/part-vi/chapter-23/)
