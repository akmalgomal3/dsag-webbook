---
weight: 11100
title: "Chapter 56 - Sliding Window and Two Pointers"
description: "Sliding Window and Two Pointers"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>If brute force is O(n²), two pointers or sliding window often reduce it to O(n).</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 56 covers sliding window and two pointers — two fundamental techniques for solving subarray/substring problems in linear time.
{{% /alert %}

## 56.1. The Two Pointers Technique

**Definition:** The <abbr title="A technique using two indices to traverse a data structure, typically one starting from each end or both from the start.">two pointers</abbr> technique maintains two indices moving through a sequence to find pairs, triplets, or partitions satisfying a condition.

### Classic: Pair Sum

Given sorted array, find pair summing to target:

```go
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
```

| Variation | Pointer Movement |
|-----------|-----------------|
| Opposite ends | Converge inward |
| Same direction | Fast/slow (cycle detection) |
| Partitioning | Based on condition |

## 56.2. Sliding Window

**Definition:** The <abbr title="A technique for finding a subarray or substring that satisfies a condition by maintaining a window of elements and adjusting its bounds.">sliding window</abbr> maintains a subarray/substring that satisfies a condition, expanding and contracting as needed.

### Fixed-Size Window

Maximum sum of k consecutive elements:

```go
func maxSumWindow(arr []int, k int) int {
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
```

### Variable-Size Window

Longest substring without repeating characters:

```go
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
```

## 56.3. Decision Matrix

| Use Two Pointers When... | Use Sliding Window When... |
|--------------------------|---------------------------|
| Sorted data with pair conditions | Contiguous subarray/substring |
| Partitioning arrays | Sum/average constraints |
| Cycle detection | Frequency/diversity constraints |

### Edge Cases & Pitfalls

- **Empty input:** Handle gracefully.
- **Window bounds:** Off-by-one errors are common.
- **Monotonicity:** Sliding window only works when expanding/shrinking is monotonic.
- **Duplicate elements:** Map frequency counts for "at most K distinct" problems.

## 56.4. Quick Reference

| Problem Type | Technique | Time |
|--------------|-----------|------|
| Pair sum in sorted array | Two pointers | O(n) |
| 3Sum | Two pointers nested | O(n²) |
| Container with most water | Two pointers | O(n) |
| Longest substring K distinct | Sliding window | O(n) |
| Minimum window substring | Sliding window | O(n) |

| Go stdlib | Usage |
|-----------|-------|
| `strings` | `Contains`, `Index` for substring ops |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 56:</strong> Two pointers and sliding window are the bread and butter of linear-time array and string processing. They replace nested loops with elegant single passes, exploiting ordering or contiguous structure. Mastering these patterns means recognizing when a problem asks for "pairs," "subarrays," or "substrings" — then choosing the right traversal strategy.
{{% /alert %}}
