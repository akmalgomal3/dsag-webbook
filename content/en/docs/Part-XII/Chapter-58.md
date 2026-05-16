---
weight: 120200
title: "Chapter 58: Mo's Algorithm"
description: "Mo's Algorithm"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
Mo's algorithm sorts range queries cleverly. Reordering minimizes recalculation.
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Mo's algorithm uses <abbr title="A technique that divides a problem into blocks of size sqrt(N) to optimize query processing.">sqrt-decomposition</abbr> for offline range queries. Reordering queries minimizes pointer movement.
{{% /alert %}}

## 59.1. The Offline Query Problem

**Definition:** <abbr title="An algorithm that answers range queries by sorting them in a specific order to minimize pointer movement.">Mo's algorithm</abbr> reorders queries. It derives answers from previous states via minimal adjustment.

**Mechanics:**
Geometric sorting caches queries. Batching queries into blocks prevents random array traversal. Moving pointers is faster than full recomputation.

**Use Cases:**
Competitive programming, batched offline data analytics, and historical database queries. All query requests must be known in advance.

**Memory Mechanics:**
Batching queries into `√N` blocks reduces memory sweeps. Incremental pointer movement along the <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> array creates predictable access patterns. CPU prefetchers load segments into <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr>. Cache misses decrease.

### Why Reorder Queries?

| Naive | Mo's Algorithm |
|-------|----------------|
| <code>O(Q × range)</code> | <code>O((N + Q) × √N)</code> |
| Process queries in given order | Sort queries by block, then endpoint |

## 59.2. Algorithm Steps

1. Divide array into blocks of size ≈ √N.
2. Sort queries by block index, then right endpoint.
3. Maintain current window [L, R] and answer.
4. Expand or shrink L and R to match next query.

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr>: Mo's Algorithm

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

// freq tracks element occurrences for distinct count queries
var freq = make(map[int]int)

// add increments frequency and bumps curAns when a new distinct element appears
func add(val int, curAns *int) {
	freq[val]++
	if freq[val] == 1 {
		*curAns++
	}
}

// remove decrements frequency and drops curAns when the last copy is removed
func remove(val int, curAns *int) {
	freq[val]--
	if freq[val] == 0 {
		*curAns--
	}
}

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
	// Reset global frequency map before processing
	freq = make(map[int]int)

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
	arr := []int{1, 2, 1, 3, 2, 4, 1, 5}
	queries := []Query{
		{l: 0, r: 3, idx: 0}, // [1,2,1,3] distinct: 3
		{l: 2, r: 5, idx: 1}, // [1,3,2,4] distinct: 4
		{l: 1, r: 4, idx: 2}, // [2,1,3,2] distinct: 3
		{l: 0, r: 7, idx: 3}, // full array distinct: 5
	}
	results := mosAlgorithm(arr, queries)
	fmt.Println("Array:", arr)
	fmt.Println("Distinct element counts per range query:")
	for _, q := range queries {
		fmt.Printf("  [%d, %d]: %d\n", q.l, q.r, results[q.idx])
	}
}
```

## 59.3. Functionality

| Problem | Add/Remove | Complexity |
|---------|-----------|------------|
| Distinct elements in range | Update frequency map | <code>O((N+Q)√N)</code> |
| Mode in range | Update frequency counts | <code>O((N+Q)√N)</code> |
| Sum of frequencies | Simple arithmetic | <code>O((N+Q)√N)</code> |

## 59.4. Decision Matrix

| Use Mo's When... | Use Segment Tree When... |
|-----------------|---------------------------|
| Offline queries | Online queries |
| Add/remove is <code>O(1)</code> or <code>O(log n)</code> | Queries need arbitrary combine |
| Static array | Frequent array updates |

### Edge Cases & Pitfalls

- **Online queries:** Method requires all queries upfront.
- **Update operations:** Point updates require algorithm modifications.
- **Block size tuning:** √N is theoretical. Experiment with N^0.5 to N^0.7.

### Anti-Patterns

- **Online execution:** Using Mo's for dynamic queries causes failure. Segment trees are required.
- **State persistence:** Failing to reset frequency maps between cases corrupts data.
- **Expensive updates:** Slow add or remove operations balloon complexity to O(Q × N × √N).
- **Suboptimal sorting:** Simple block sorting causes cache misses. Hilbert curves preserve spatial locality.

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
**Summary Chapter 58:** Mo's algorithm reorders queries to minimize boundary movement. It transforms <code>O(Q × N)</code> <abbr title="A straightforward approach trying all possible solutions">brute force</abbr> into <code>O((N+Q)√N)</code>. 
{{% /alert %}}

## See Also

- [Chapter 54: Counting, Radix, and <abbr title="A sorting algorithm distributing elements into buckets">Bucket Sort</abbr>](/docs/part-xi/chapter-54/)
- [Chapter 56: Kadane's Algorithm](/docs/part-xi/chapter-56/)
- [Chapter 57: Minimax and Game Trees](/docs/part-xii/chapter-57/)
