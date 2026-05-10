---
weight: 120200
title: "Chapter 59: Mo's Algorithm"
description: "Mo's Algorithm"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Mo's algorithm: when you have many range queries, sort them cleverly.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 59 introduces Mo's algorithm: a sqrt-decomposition technique for efficiently answering offline range queries by reordering them to minimize recalculation.
{{% /alert %}}

## 59.1. The Offline Query Problem

**Definition:** Given an array and multiple range queries, <abbr title="An algorithm that answers range queries by sorting them in a specific order to minimize pointer movement.">Mo's algorithm</abbr> reorders queries so that each query's answer can be derived from the previous with minimal adjustment.

**Background & Philosophy:**
The philosophy is query caching via geometric sorting. Instead of processing queries exactly as the user inputs them (which might bounce randomly from the start of the array to the end and back), Mo's algorithm batches them together into blocks. It embraces the philosophy that moving pointers slightly left or right is infinitely faster than restarting a search from zero.

**Use Cases:**
Competitive programming, batched offline data analytics, and historical database queries where all query requests are known entirely in advance.

**Memory Mechanics:**
Mo's Algorithm drastically minimizes `O(N)` memory sweeps. By grouping the queries structurally into `√N` blocks and sorting them, the `curL` and `curR` pointers only creep incrementally forward and backward along the <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> array. This creates a beautifully predictable memory access pattern. The CPU hardware prefetcher recognizes this creeping movement and reliably loads the required array segments into the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> proactively, virtually eliminating performance-killing <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>.

### Why Reorder Queries?

| Naive | Mo's Algorithm |
|-------|----------------|
| <code>O(Q × range)</code> | <code>O((N + Q) × √N)</code> |
| Process queries in given order | Sort queries by block, then endpoint |

## 59.2. The Algorithm

1. Divide array into blocks of size ≈ √N
2. Sort queries by (block index, right endpoint)
3. Maintain a "current window" [L, R] and its answer
4. Expand/shrink L and R to match each query

### Idiomatic Go: Mo's Algorithm

```go
package main

import (
	"fmt"
	"math"
	"sort"
)

type Query struct {
	l, r, idx int
}

// Pseudo-functions representing specific problem logic
func add(val int, curAns *int)    { /* Specific problem logic */ }
func remove(val int, curAns *int) { /* Specific problem logic */ }

func mosAlgorithm(arr []int, queries []Query) []int {
    blockSize := int(math.Sqrt(float64(len(arr))))
    
    sort.Slice(queries, func(i, j int) bool {
        bi := queries[i].l / blockSize
        bj := queries[j].l / blockSize
        if bi != bj {
            return bi < bj
        }
        return queries[i].r < queries[j].r
    })
    
    results := make([]int, len(queries))
    curL, curR := 0, -1
    curAns := 0
    
    for _, q := range queries {
        for curL > q.l {
            curL--
            add(arr[curL], &curAns)
        }
        for curR < q.r {
            curR++
            add(arr[curR], &curAns)
        }
        for curL < q.l {
            remove(arr[curL], &curAns)
            curL++
        }
        for curR > q.r {
            remove(arr[curR], &curAns)
            curR--
        }
        results[q.idx] = curAns
    }
    
    return results
}

func main() {
    // Demonstration
    fmt.Println("Mo's Algorithm initialized")
}
```

## 59.3. When It Works

| Problem | Add/Remove | Complexity |
|---------|-----------|------------|
| Distinct elements in range | Update frequency map | <code>O((N+Q)√N)</code> |
| Mode in range | Update frequency counts | <code>O((N+Q)√N)</code> |
| Sum of frequencies | Simple arithmetic | <code>O((N+Q)√N)</code> |

## 59.4. Decision Matrix

| Use Mo's When... | Use Segment Tree When... |
|-----------------|---------------------------|
| Offline queries (all known upfront) | Online queries (arrive dynamically) |
| Add/remove is <code>O(1)</code> or <code>O(log n)</code> | Queries need arbitrary combine |
| Array is static | Array updates frequently |

### Edge Cases & Pitfalls

- **Online queries:** Mo's only works offline — all queries must be known.
- **Update operations:** Standard Mo's doesn't handle point updates (use Mo's with modifications).
- **Block size tuning:** √N is theoretical; experiment with N^0.5 to N^0.7.

## 59.5. Quick Reference

| Parameter | Formula |
|-----------|---------|
| Block size | √N (or N/√Q) |
| Sort order | Block(L), then R (alternating direction) |
| Complexity | <code>O((N + Q) × √N × cost_add_remove)</code> |

| Go stdlib | Usage |
|-----------|-------|
| `sort` | Query sorting |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 59:</strong> Mo's algorithm demonstrates that algorithmic efficiency sometimes comes not from smarter computation, but from smarter ordering. By sorting range queries to minimize boundary movement, it transforms <code>O(Q × N)</code> brute force into <code>O((N+Q)√N)</code>. It is a niche but powerful technique for competitive programming and offline batch processing.
{{% /alert %}}

## See Also

- [Chapter 55: Counting, Radix, and Bucket Sort](/docs/Part-XI/Chapter-55/)
- [Chapter 57: Kadane's Algorithm](/docs/Part-XI/Chapter-57/)
- [Chapter 58: Minimax and Game Trees](/docs/Part-XII/Chapter-58/)
