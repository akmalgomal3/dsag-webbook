---
weight: 90100
title: "Chapter 45: B-Trees"
description: "B-Trees"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The B-tree is the data structure that made modern databases possible.</em>" : Rudolf Bayer</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 45 covers B-trees, the multi-way search tree optimized for disk access, powering every major database and file system.
{{% /alert %}}

## 45.1. Why B-Trees?

**Definition:** A <abbr title="A self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.">B-tree</abbr> is a self-balancing multi-way search tree designed to minimize disk I/O. Unlike binary trees with one key per node, B-trees store hundreds of keys per node, matching disk block sizes.

**Background & Philosophy:**
The philosophy is structural density. Binary trees grow tall quickly, meaning many node traversals. A B-Tree grows wide instead of tall. By packing hundreds of keys into a single node, it mathematically slashes the tree's height, drastically reducing the number of jumps required to find data.

**Use Cases:**
Database indices (PostgreSQL, MySQL), file systems (NTFS, ext4), and any system where retrieving data from a disk drive is the primary bottleneck.

**Memory Mechanics:**
Disk I/O is notoriously slow. A B-Tree node is specifically sized to perfectly match the hardware's block size (usually 4KB or 8KB). When the CPU requests a single key from disk, the OS pulls the entire 4KB block into <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> regardless. By ensuring the B-Tree node fits exactly inside this block, the algorithm achieves 100% data utilization per disk seek. Furthermore, scanning the keys inside that 4KB node in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> leverages flawless <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>, maximizing the L1 <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr>.

### The Disk I/O Problem

| Operation | RAM Latency | Disk Latency |
|-----------|-------------|--------------|
| Random access | 100 ns | 10 ms |
| Sequential read | 10 GB/s | 200 MB/s |

A <abbr title="A tree where each node has at most two children">binary tree</abbr> with 1 million items requires ~20 disk seeks. A B-tree with 500 keys/node requires only ~3.

## 45.2. B-Tree Properties

For a B-tree of order <abbr title="The maximum number of children a node can have in a B-tree.">m</abbr>:

- Every node has at most m children
- Every internal node (except root) has at least ⌈m/2⌉ children
- The root has at least 2 children if it is not a leaf
- All leaves appear on the same level
- A non-leaf node with k children contains k-1 keys

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr>: B-Tree Node

```go
package main

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

func main() {
    // Placeholder for structural demonstration
}
```

## 45.3. Operations

| Operation | Time | Description |
|-----------|------|-------------|
| Search | <code>O(log_m n)</code> | Traverse from root to leaf |
| Insert | <code>O(log_m n)</code> | May split nodes bottom-up |
| Delete | <code>O(log_m n)</code> | May merge or redistribute |

### Insertion with Split

When a node overflows (exceeds m-1 keys), it splits into two nodes and promotes the median key to the parent, keeping the tree perfectly balanced.

## 45.4. B+ Trees

**Definition:** In a <abbr title="A variant of B-tree where all data is stored in leaves and internal nodes only store keys for navigation.">B+ tree</abbr>, all data lives in leaves; internal nodes are pure navigation. Leaves are linked for fast range scans.

| Feature | B-Tree | B+ Tree |
|---------|--------|---------|
| Data in internal nodes | Yes | No |
| Sequential scan | <code>O(n log n)</code> | <code>O(n)</code> |
| Space utilization | Lower | Higher |
| Use case | General | Databases, file systems |

## 45.5. Decision Matrix

| Use B-Trees When... | Use Hash Tables When... |
|---------------------|-------------------------|
| Data exceeds RAM | Data fits entirely in memory |
| Range queries are needed | Only point lookups are executed |
| Sequential access matters | Random access only is acceptable |

### Edge Cases & Pitfalls

- **Small m:** Undermines the entire purpose. Disk blocks are usually 4KB.
- **Concurrency:** Locking a node vs. the entire tree requires careful latching protocols (e.g., crabbing).
- **Write amplification:** Each single insert may cascade splits entirely up the tree.

## 45.6. Quick Reference

| Concept | Value | Rationale |
|---------|-------|-----------|
| Typical order | 100 to 500 | Matches disk block size |
| Height for 1B items | 3 to 4 | Minimizes physical disk seeks |
| Fill factor | ~67% | Expected density after deletions |

| Go stdlib | Usage |
|-----------|-------|
| `database/sql` | Backed deeply by B-trees |
| `go.etcd.io/bbolt` | Pure Go B+ tree implementation |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 45:</strong> B-trees bridge the gap between algorithmic theory and physical reality by optimizing not for CPU cycles but for massive disk seeks. By matching node size to disk blocks and keeping all leaves at the identical depth, B-trees transformed database performance. The B+ tree variant, with its linked leaves, ensures range queries execute as fast as sequential scans.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/Part-III/Chapter-9/)
- [Chapter 11: Disjoint Sets](/docs/Part-III/Chapter-11/)
- [Chapter 47: Bloom Filters](/docs/Part-IX/Chapter-47/)
