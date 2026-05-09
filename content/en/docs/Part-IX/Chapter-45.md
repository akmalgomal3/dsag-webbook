---
weight: 90100
title: "Chapter 45 - B-Trees"
description: "B-Trees"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The B-tree is the data structure that made modern databases possible.</em>" — Rudolf Bayer</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 45 covers B-trees — the multi-way search tree optimized for disk access, powering every major database and file system.
{{% /alert %}}

## 45.1. Why B-Trees?

**Definition:** A <abbr title="A self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.">B-tree</abbr> is a self-balancing multi-way search tree designed to minimize disk I/O. Unlike binary trees with one key per node, B-trees store hundreds of keys per node, matching disk block sizes.

### The Disk I/O Problem

| Operation | RAM Latency | Disk Latency |
|-----------|-------------|--------------|
| Random access | 100 ns | 10 ms |
| Sequential read | 10 GB/s | 200 MB/s |

A binary tree with 1 million items requires ~20 disk seeks. A B-tree with 500 keys/node requires only ~3.

## 45.2. B-Tree Properties

For a B-tree of order <abbr title="The maximum number of children a node can have in a B-tree.">m</abbr>:

- Every node has at most m children
- Every internal node (except root) has at least ⌈m/2⌉ children
- The root has at least 2 children if it is not a leaf
- All leaves appear on the same level
- A non-leaf node with k children contains k-1 keys

### Idiomatic Go: B-Tree Node

```go
type BTreeNode struct {
    keys     []int
    children []*BTreeNode
    leaf     bool
}

func (n *BTreeNode) search(k int) bool {
    i := 0
    for i < len(n.keys) && k > n.keys[i] {
        i++
    }
    if i < len(n.keys) && k == n.keys[i] {
        return true
    }
    if n.leaf {
        return false
    }
    return n.children[i].search(k)
}
```

## 45.3. Operations

| Operation | Time | Description |
|-----------|------|-------------|
| Search | O(log_m n) | Traverse from root to leaf |
| Insert | O(log_m n) | May split nodes bottom-up |
| Delete | O(log_m n) | May merge or redistribute |

### Insertion with Split

When a node overflows (exceeds m-1 keys), it splits into two nodes and promotes the median key to the parent — keeping the tree perfectly balanced.

## 45.4. B+ Trees

**Definition:** In a <abbr title="A variant of B-tree where all data is stored in leaves and internal nodes only store keys for navigation.">B+ tree</abbr>, all data lives in leaves; internal nodes are pure navigation. Leaves are linked for fast range scans.

| Feature | B-Tree | B+ Tree |
|---------|--------|---------|
| Data in internal nodes | Yes | No |
| Sequential scan | O(n log n) | O(n) |
| Space utilization | Lower | Higher |
| Use case | General | Databases, file systems |

## 45.5. Decision Matrix

| Use B-Trees When... | Use Hash Tables When... |
|---------------------|-------------------------|
| Data exceeds RAM | Data fits in memory |
| Range queries needed | Only point lookups |
| Sequential access matters | Random access only |

### Edge Cases & Pitfalls

- **Small m:** Undermines the purpose — disk blocks are usually 4KB.
- **Concurrency:** Locking a node vs. the entire tree requires careful latching protocols.
- **Write amplification:** Each insert may cascade splits up the tree.

## 45.6. Quick Reference

| Concept | Value | Rationale |
|---------|-------|-----------|
| Typical order | 100–500 | Matches disk block size |
| Height for 1B items | 3–4 | Minimizes disk seeks |
| Fill factor | ~67% | After deletions |

| Go stdlib | Usage |
|-----------|-------|
| `database/sql` | Backed by B-trees |
| `go.etcd.io/bbolt` | Pure Go B+ tree |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 45:</strong> B-trees bridge the gap between algorithmic theory and physical reality — optimizing not for CPU cycles but for disk seeks. By matching node size to disk blocks and keeping all leaves at the same depth, B-trees transformed database performance. The B+ tree variant, with its linked leaves, makes range queries as fast as sequential scans.
{{% /alert %}}

## See Also

- [Chapter 9 — Trees and Balanced Trees](/docs/Part-III/Chapter-9/)
- [Chapter 11 — Disjoint Sets](/docs/Part-III/Chapter-11/)
- [Chapter 47 — Bloom Filters](/docs/Part-IX/Chapter-47/)

