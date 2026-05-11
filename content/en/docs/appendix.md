---
weight: 9000
title: "Appendix"
description: "Big-O Cheat Sheet"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

## Big-O Cheat Sheet

Quick reference for time and space complexity of common data structures and algorithms.

### Data Structures

| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
| Dynamic Array (Slice) | O(1) | O(n) | O(1) amortized | O(n) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Table | : | O(1) avg | O(1) avg | O(1) avg | O(n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Heap | O(n) | O(n) | O(log n) | O(log n) | O(n) |
| Trie | O(m) | O(m) | O(m) | O(m) | O(n·m) |
| Segment Tree | O(log n) | : | O(log n) | O(log n) | O(n) |
| B-Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Skip List | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Bloom Filter | : | O(k) | O(k) | : | O(n) |

### Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| Radix Sort | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes |
| Bucket Sort | O(n) | O(n) | O(n²) | O(n) | Yes |

### Graph Algorithms

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
| DFS | O(V + E) | O(V) | Connectivity, cycles |
| Dijkstra | O((V + E) log V) | O(V) | Shortest path (weighted, no negatives) |
| Bellman-Ford | O(V·E) | O(V) | Shortest path (with negatives) |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
| Kruskal | O(E log E) | O(V) | MST |
| Prim | O((V + E) log V) | O(V) | MST |
| Topological Sort | O(V + E) | O(V) | Dependency ordering |
| A* | O(E log V) typical, O(b^d) worst | O(V) | Pathfinding with heuristic |

### Array/String Techniques

| Technique | Time | Space | Use Case |
|-----------|------|-------|----------|
| Two Pointers | O(n) | O(1) | Sorted pair search |
| Sliding Window | O(n) | O(1) | Subarray/substring problems |
| Kadane's Algorithm | O(n) | O(1) | Maximum subarray |
| Prefix Sum | O(n) preprocessing, O(1) query | O(n) | Range sum queries |
| Mo's Algorithm | O((n + q)√n) | O(n) | Offline range queries |

---

{{% alert icon="🎯" context="success" %}}
This cheat sheet covers the most common data structures and algorithms. Refer to individual chapters for detailed analysis, Go implementations, and edge cases.
{{% /alert %}}

## See Also

- [Chapter 1: The Role of Algorithms in Modern Software](/docs/Part-I/Chapter-1/)
- [Chapter 6: Elementary Data Structures](/docs/Part-II/Chapter-6/)
- [Table of Contents](/docs/Table-of-Contents/)
