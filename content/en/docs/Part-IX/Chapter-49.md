---
weight: 90600
title: "Chapter 49: Persistent Data Structures"
description: "Persistent Data Structures"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Persistence is the path to immutability.</em>" — Chris Okasaki</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Persistent data structures preserve previous versions. Modification enables time-travel debugging and immutability.
{{% /alert %}}

## 49.1. Purpose

**Definition:** A <abbr title="A data structure that always preserves the previous version of itself when it is modified, enabling access to any version.">persistent data structure</abbr> keeps all previous versions accessible after modification.

**Immutability Logic:**
Updates do not overwrite data. New versions created as deltas. Old parts shared structurally. Immutability prevents data races. Read-only versions need no locks.

**Use Cases:**
Git version control. Functional programming (Clojure, Haskell). Time-travel debugging tools.

**Memory Mechanics:**
Relies on <abbr title="A technique where only the nodes along the path from root to the modified node are copied, sharing unchanged subtrees.">"Path Copying"</abbr>. Copies only <code>O(log n)</code> nodes along modified paths. Shares unchanged subtrees. Garbage Collector reclaims unreferenced versions.

| Type | Behavior | Example |
|------|----------|---------|
| **Partial persistence** | Read all, write latest. | Versioned logs. |
| **Full persistence** | Read and write any. | Functional data structures. |

## 49.2. Path Copying

Primary technique: update node by copying path from root to modified node. Share all unchanged siblings.

### Persistent Linked List: Go Implementation

```go
package main

import "fmt"

type List struct {
    val  int
    next *List
}

// Prepend returns NEW list. Original unchanged.
func (l *List) Prepend(v int) *List {
    return &List{val: v, next: l}
}

func main() {
    list1 := &List{val: 1}
    list2 := list1.Prepend(2)
    
    fmt.Println(list1.val) // 1
    fmt.Println(list2.val) // 2
}
```

## 49.3. Persistent <abbr title="A tree where each node has at most two children">Binary Tree</abbr>

Leaf update triggers copying leaf and all ancestors to root. Non-modified siblings stay shared.

| Operation | Time | Space |
|-----------|------|-------|
| Update | <code>O(log n)</code> | <code>O(log n)</code> new nodes. |
| Access | <code>O(log n)</code> | <code>O(1)</code>. |

## 49.4. Applications

| Application | Function |
|-------------|-----------------|
| **Git** | Commits as persistent snapshots. |
| **Undo/Redo** | State preservation. |
| **Functional Programming** | Default immutability. |
| **Debugging** | Past state inspection. |
| **Concurrency** | Lock-free reading. |

## 49.5. Decision Matrix

| Use Persistence When... | Use Mutation When... |
|-------------------------|---------------------|
| Version history required. | Only latest state needed. |
| Functional paradigms. | Imperative performance. |
| Read-heavy concurrency. | Single-threaded speed. |
| Undo logic needed. | Memory is constrained. |

### Edge Cases & Pitfalls

- **Space Growth:** n updates produce <code>O(n log n)</code> nodes. GC required.
- **Node Sharing:** Modifying shared nodes corrupts all versions.
- **Amortization:** Queues use lazy evaluation for efficiency.

### Anti-Patterns

- **Single Version Work:** Path copying overhead wastes memory if history is ignored.
- **In-place Mutation:** Changing shared subtrees corrupts history. Immutability is mandatory.
- **Flat Array Persistence:** Updating arrays via path copying is <code>O(n)</code>. Use trees.
- **GC Neglect:** Millions of updates stress Garbage Collection. Use version pruning.

## 49.6. Quick Reference

| Structure | Variant | Overhead |
|-----------|-------------------|----------|
| Linked list | Fully persistent. | <code>O(1)</code> / update. |
| Binary tree | Path copying. | <code>O(log n)</code> / update. |
| Array | Copy-on-write. | <code>O(1)</code> to <code>O(n)</code>. |
| Queue | Banker's method. | <code>O(1)</code> amortized. |

| Go stdlib | Usage |
|-----------|-------|
| Slice sharing | Array sharing without full persistence. |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
Persistence trades space for history. Structural sharing minimizes overhead. Immutability prevents mutation-based bugs.
{{% /alert %}}

## See Also

- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
- [Chapter 48: Suffix Arrays](/docs/part-ix/chapter-48/)
- [Chapter 41: Evolution of Data Structures](/docs/part-viii/chapter-41/)
