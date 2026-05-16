---
weight: 90100
title: "Chapter 44: B-Trees"
description: "B-Trees"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The B-tree is the data structure that made modern databases possible.</em>" — Rudolf Bayer</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
B-trees optimize disk access. Multi-way search trees power databases and file systems.
{{% /alert %}}

## 44.1. Purpose

**Definition:** <abbr title="A self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.">B-tree</abbr> minimizes disk I/O. Multi-way search tree stores hundreds of keys per node to match disk block sizes.

**Structure:**
B-Tree grows wide. Nodes pack hundreds of keys. Width reduces tree height and disk jumps.

**Use Cases:**
Database indices (PostgreSQL, MySQL). File systems (NTFS, ext4). High-latency storage bottlenecks.

**Memory Mechanics:**
Nodes match hardware block size (4KB or 8KB). CPU pulls entire blocks into <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. Algorithm achieves 100% data utilization per seek. Scanning keys in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> leverages <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr> and L1 <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr>.

### Disk I/O Bottleneck

| Operation | RAM Latency | Disk Latency |
|-----------|-------------|--------------|
| Random access | 100 ns | 10 ms |
| Sequential read | 10 GB/s | 200 MB/s |

Binary trees require ~20 seeks for 1M items. B-trees require ~3.

## 44.2. B-Tree Properties

Order <abbr title="The maximum number of children a node can have in a B-tree.">m</abbr> rules:

- Nodes have max m children.
- Internal nodes (except root) have min ⌈m/2⌉ children.
- Root has min 2 children if not a leaf.
- Leaves appear on same level.
- Non-leaf node with k children contains k-1 keys.

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
    // Structural demonstration
}
```

## 44.3. Operations

| Operation | Time | Description |
|-----------|------|-------------|
| Search | <code>O(log_m n)</code> | Root to leaf traversal. |
| Insert | <code>O(log_m n)</code> | Split nodes bottom-up. |
| Delete | <code>O(log_m n)</code> | Merge or redistribute. |

### Insertion with Split

Nodes overflow at m keys. Node splits in two. Median key promotes to parent. Tree stays balanced.

## 44.4. B+ Trees

**Definition:** <abbr title="A variant of B-tree where all data is stored in leaves and internal nodes only store keys for navigation.">B+ tree</abbr> stores all data in leaves. Internal nodes navigate. Leaves link for fast range scans.

| Feature | B-Tree | B+ Tree |
|---------|--------|---------|
| Internal Data | Yes | No |
| Sequential Scan | <code>O(n log n)</code> | <code>O(n)</code> |
| Space Utilization | Lower | Higher |
| Primary Use | General | DBs, File Systems |

## 44.5. Decision Matrix

| Use B-Trees When... | Use Hash Tables When... |
|---------------------|-------------------------|
| Data exceeds RAM | Data fits in memory |
| Range queries needed | Point lookups only |
| Sequential access matters | Random access only |

### Edge Cases & Pitfalls

- **Small m:** Nodes smaller than blocks waste I/O bandwidth.
- **Concurrency:** Requires latching protocols (crabbing).
- **Write Amplification:** Inserts may trigger cascading splits.

### Anti-Patterns

- **Small Data:** Hash tables beat B-trees for in-memory data.
- **Mismatched m:** Node size must match disk block size (4KB/8KB).
- **Deletions:** Fragmented trees waste reads. Rebalance required.
- **Point Lookups:** B+ Trees overhead slows single-key lookups.

## 44.6. Quick Reference

| Concept | Value | Rationale |
|---------|-------|-----------|
| Order | 100 to 500 | Matches disk block size. |
| Height (1B items) | 3 to 4 | Minimizes physical seeks. |
| Fill factor | ~67% | Expected density. |

| Go stdlib | Usage |
|-----------|-------|
| `database/sql` | Uses B-trees internally. |
| `go.etcd.io/bbolt` | B+ tree implementation. |


{{% alert icon="🎯" context="success" %}}
B-trees optimize for massive disk seeks. Nodes match disk blocks. B+ trees enable fast range queries via linked leaves.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
- [Chapter 11: Disjoint Sets](/docs/part-iii/chapter-11/)
- [Chapter 46: Bloom Filters](/docs/part-ix/chapter-46/)