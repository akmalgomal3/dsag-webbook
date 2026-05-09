---
weight: 12100
title: "Chapter 59 - Mo's Algorithm"
description: "Mo's Algorithm"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Mo's algorithm: when you have many range queries, sort them cleverly.</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 59 introduces Mo's algorithm — a sqrt-decomposition technique for efficiently answering offline range queries by reordering them to minimize recalculation.
{{% /alert %}

## 59.1. The Offline Query Problem

**Definition:** Given an array and multiple range queries, <abbr title="An algorithm that answers range queries by sorting them in a specific order to minimize pointer movement.">Mo's algorithm</abbr> reorders queries so that each query's answer can be derived from the previous with minimal adjustment.

### Why Reorder Queries?

| Naive | Mo's Algorithm |
|-------|----------------|
| O(Q × range) | O((N + Q) × √N) |
| Process queries in given order | Sort queries by block, then endpoint |

## 59.2. The Algorithm

1. Divide array into blocks of size ≈ √N
2. Sort queries by (block index, right endpoint)
3. Maintain a "current window" [L, R] and its answer
4. Expand/shrink L and R to match each query

### Idiomatic Go: Mo's Algorithm

```go
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
        while curR < q.r {
            curR++
            add(arr[curR], &curAns)
        }
        while curL < q.l {
            remove(arr[curL], &curAns)
            curL++
        }
        while curR > q.r {
            remove(arr[curR], &curAns)
            curR--
        }
        results[q.idx] = curAns
    }
    
    return results
}
```

## 59.3. When It Works

| Problem | Add/Remove | Complexity |
|---------|-----------|------------|
| Distinct elements in range | Update frequency map | O((N+Q)√N) |
| Mode in range | Update frequency counts | O((N+Q)√N) |
| Sum of frequencies | Simple arithmetic | O((N+Q)√N) |

## 59.4. Decision Matrix

| Use Mo's When... | Use Segment Tree When... |
|-----------------|---------------------------|
| Offline queries (all known upfront) | Online queries (arrive dynamically) |
| Add/remove is O(1) or O(log n) | Queries need arbitrary combine |
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
| Complexity | O((N + Q) × √N × cost_add_remove) |

| Go stdlib | Usage |
|-----------|-------|
| `sort` | Query sorting |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 59:</strong> Mo's algorithm demonstrates that algorithmic efficiency sometimes comes not from smarter computation, but from smarter ordering. By sorting range queries to minimize boundary movement, it transforms O(Q × N) brute force into O((N+Q)√N). It is a niche but powerful technique for competitive programming and offline batch processing.
{{% /alert %}
