---
weight: 9000
title: "Appendix"
description: "Big-O Cheat Sheet"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
---

## Big-O Cheat Sheet

Use the following tables as a quick reference to understand the time and space complexity of common data structures and algorithms.

### Data Structures

| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | <code>O(1)</code> | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> | <code>O(n)</code> |
| Linked List | <code>O(n)</code> | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | <code>O(n)</code> |
| Dynamic Array (Slice) | <code>O(1)</code> | <code>O(n)</code> | <code>O(1)</code> amortized | <code>O(n)</code> | <code>O(n)</code> |
| Stack | <code>O(n)</code> | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | <code>O(n)</code> |
| Queue | <code>O(n)</code> | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | <code>O(n)</code> |
| Hash Table | : | <code>O(1)</code> avg | <code>O(1)</code> avg | <code>O(1)</code> avg | <code>O(n)</code> |
| BST (balanced) | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Heap | <code>O(n)</code> | <code>O(n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Trie | <code>O(m)</code> | <code>O(m)</code> | <code>O(m)</code> | <code>O(m)</code> | <code>O(n·m)</code> |
| Segment Tree | <code>O(log n)</code> | : | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| B-Tree | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Skip List | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Bloom Filter | : | <code>O(k)</code> | <code>O(k)</code> | : | <code>O(n)</code> |

### Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Quicksort | <code>O(n log n)</code> | <code>O(n log n)</code> | <code>O(n²)</code> | <code>O(log n)</code> | No |
| Mergesort | <code>O(n log n)</code> | <code>O(n log n)</code> | <code>O(n log n)</code> | <code>O(n)</code> | Yes |
| Heapsort | <code>O(n log n)</code> | <code>O(n log n)</code> | <code>O(n log n)</code> | <code>O(1)</code> | No |
| <abbr title="A sorting algorithm building the final array one element at a time">Insertion Sort</abbr> | <code>O(n)</code> | <code>O(n²)</code> | <code>O(n²)</code> | <code>O(1)</code> | Yes |
| <abbr title="A sorting algorithm repeatedly finding the minimum element">Selection Sort</abbr> | <code>O(n²)</code> | <code>O(n²)</code> | <code>O(n²)</code> | <code>O(1)</code> | No |
| <abbr title="An integer sorting algorithm using frequency counting">Counting Sort</abbr> | <code>O(n + k)</code> | <code>O(n + k)</code> | <code>O(n + k)</code> | <code>O(k)</code> | Yes |
| <abbr title="A sorting algorithm processing digits individually">Radix Sort</abbr> | <code>O(d(n + k))</code> | <code>O(d(n + k))</code> | <code>O(d(n + k))</code> | <code>O(n + k)</code> | Yes |
| <abbr title="A sorting algorithm distributing elements into buckets">Bucket Sort</abbr> | <code>O(n)</code> | <code>O(n)</code> | <code>O(n²)</code> | <code>O(n)</code> | Yes |

### Graph Algorithms

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | <code>O(V + E)</code> | <code>O(V)</code> | Shortest path (unweighted) |
| DFS | <code>O(V + E)</code> | <code>O(V)</code> | Connectivity, cycles |
| Dijkstra | <code>O((V + E) log V)</code> | <code>O(V)</code> | Shortest path (weighted, no negatives) |
| Bellman-Ford | <code>O(V·E)</code> | <code>O(V)</code> | Shortest path (with negatives) |
| Floyd-Warshall | <code>O(V³)</code> | <code>O(V²)</code> | All-pairs shortest path |
| Kruskal | <code>O(E log E)</code> | <code>O(V)</code> | MST |
| Prim | <code>O((V + E) log V)</code> | <code>O(V)</code> | MST |
| Topological Sort | <code>O(V + E)</code> | <code>O(V)</code> | Dependency ordering |
| A* | <code>O(E log V)</code> typical, <code>O(b^d)</code> worst | <code>O(V)</code> | Pathfinding with heuristic |

### Array/String Techniques

| Technique | Time | Space | Use Case |
|-----------|------|-------|----------|
| Two Pointers | <code>O(n)</code> | <code>O(1)</code> | Sorted pair search |
| Sliding Window | <code>O(n)</code> | <code>O(1)</code> | Subarray/substring problems |
| Kadane's Algorithm | <code>O(n)</code> | <code>O(1)</code> | Maximum subarray |
| Prefix Sum | <code>O(n)</code> preprocessing, <code>O(1)</code> query | <code>O(n)</code> | Range sum queries |
| Mo's Algorithm | <code>O((n + q)√n)</code> | <code>O(n)</code> | Offline range queries |

---

{{% alert icon="🎯" context="success" %}}
Use this guide as a starting point for consultation and continuous learning through real-world implementation. Refer to the specific chapters for detailed implementations and edge-case handling.
{{% /alert %}}

## See Also

- [Chapter 1: The Role of Algorithms in Modern Software](/docs/part-i/chapter-1/)
- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Table of Contents](/docs/table-of-contents/)
ts](/docs/table-of-contents/)
