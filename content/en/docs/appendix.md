     1|---
     2|weight: 9000
     3|title: "Appendix"
     4|description: "Supplementary Material"
     5|icon: "article"
     6|date: "2024-08-24T23:42:09+07:00"
     7|lastmod: "2024-08-24T23:42:09+07:00"
     8|draft: false
     9|toc: true
    10|---
    11|
    12|This appendix contains supplementary material from chapters that were integrated into other sections.
    13|
    14|---
    15|
    16|## Big-O Cheat Sheet
    17|
    18|Quick reference for time and space complexity of common data structures and algorithms.
    19|
    20|### Data Structures
    21|
    22|| Structure | Access | Search | Insert | Delete | Space |
    23||-----------|--------|--------|--------|--------|-------|
    24|| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
    25|| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
    26|| Dynamic Array (Slice) | O(1) | O(n) | O(1) amortized | O(n) | O(n) |
    27|| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
    28|| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
    29|| Hash Table |: | O(1) avg | O(1) avg | O(1) avg | O(n) |
    30|| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
    31|| Heap | O(n) | O(n) | O(log n) | O(log n) | O(n) |
    32|| Trie | O(m) | O(m) | O(m) | O(m) | O(n·m) |
    33|| Segment Tree | O(log n) |: | O(log n) | O(log n) | O(n) |
    34|| B-Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
    35|| Skip List | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
    36|| Bloom Filter |: | O(k) | O(k) |: | O(n) |
    37|
    38|### Sorting Algorithms
    39|
    40|| Algorithm | Best | Average | Worst | Space | Stable |
    41||-----------|------|---------|-------|-------|--------|
    42|| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
    43|| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
    44|| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
    45|| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
    46|| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
    47|| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
    48|| Radix Sort | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes |
    49|| Bucket Sort | O(n) | O(n) | O(n²) | O(n) | Yes |
    50|
    51|### Graph Algorithms
    52|
    53|| Algorithm | Time | Space | Use Case |
    54||-----------|------|-------|----------|
    55|| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
    56|| DFS | O(V + E) | O(V) | Connectivity, cycles |
    57|| Dijkstra | O((V + E) log V) | O(V) | Shortest path (weighted, no negatives) |
    58|| Bellman-Ford | O(V·E) | O(V) | Shortest path (with negatives) |
    59|| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
    60|| Kruskal | O(E log E) | O(V) | MST |
    61|| Prim | O((V + E) log V) | O(V) | MST |
    62|| Topological Sort | O(V + E) | O(V) | Dependency ordering |
    63|| A* | O(E log V) typical, O(b^d) worst | O(V) | Pathfinding with heuristic |
    64|
    65|### Array/String Techniques
    66|
    67|| Technique | Time | Space | Use Case |
    68||-----------|------|-------|----------|
    69|| Two Pointers | O(n) | O(1) | Sorted pair search |
    70|| Sliding Window | O(n) | O(1) | Subarray/substring problems |
    71|| Kadane's Algorithm | O(n) | O(1) | Maximum subarray |
    72|| Prefix Sum | O(n) preprocessing, O(1) query | O(n) | Range sum queries |
    73|| Mo's Algorithm | O((n + q)√n) | O(n) | Offline range queries |
    74|
    75|---
    76|
    77|
{{% alert icon="🎯" context="success" %}}
This cheat sheet covers the most common data structures and algorithms. Refer to individual chapters for detailed analysis, Go implementations, and edge cases.
{{% /alert %}}

## See Also

- [Chapter 1: The Role of Algorithms in Modern Software](/docs/Part-I/Chapter-1/)
- [Chapter 6: Elementary Data Structures](/docs/Part-II/Chapter-6/)
- [Table of Contents](/docs/Table-of-Contents/)
