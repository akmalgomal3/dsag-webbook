---
weight: 9500
title: "Chapter 50 - Persistent Data Structures"
description: "Persistent Data Structures"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Persistence is the path to immutability.</em>" — Chris Okasaki</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 50 explores persistent data structures — structures that preserve previous versions when modified, enabling time-travel debugging and functional programming paradigms.
{{% /alert %}}

## 50.1. What Is Persistence?

**Definition:** A <abbr title="A data structure that always preserves the previous version of itself when it is modified, enabling access to any version.">persistent data structure</abbr> preserves all previous versions after modification. There are two flavors:

| Type | Behavior | Example |
|------|----------|---------|
| **Partial persistence** | Read all versions, write only latest | Versioned logs |
| **Full persistence** | Read and write any version | Functional data structures |

## 50.2. Path Copying

The key technique: when updating a node, copy the path from root to that node, sharing unchanged subtrees.

### Persistent Linked List

```go
type List struct {
    val  int
    next *List
}

// Prepend returns a NEW list, original unchanged
func (l *List) Prepend(v int) *List {
    return &List{val: v, next: l}
}

// Original list still valid
list1 := &List{val: 1}
list2 := list1.Prepend(2)
// list1: [1], list2: [2, 1]
```

## 50.3. Persistent Binary Tree

Update a leaf → copy the leaf, then copy every ancestor up to the root. Unchanged siblings are shared.

| Operation | Time | Space |
|-----------|------|-------|
| Update | O(log n) | O(log n) new nodes |
| Access | O(log n) | O(1) |

## 50.4. Applications

| Application | Why Persistence |
|-------------|-----------------|
| **Git** | Every commit is a persistent snapshot |
| **Undo/redo** | Each state preserved automatically |
| **Functional programming** | Immutability by default |
| **Time-travel debugging** | Inspect any past program state |
| **Concurrent structures** | No locks needed for read-only versions |

## 50.5. Decision Matrix

| Use Persistence When... | Use Mutation When... |
|-------------------------|---------------------|
| History matters | Only latest state needed |
| Functional style | Imperative style |
| Concurrent reads | Single-threaded performance |
| Undo functionality | Memory is constrained |

### Edge Cases & Pitfalls

- **Space growth:** n updates create O(n log n) nodes — garbage collection essential.
- **Node sharing:** Modifying a "shared" node corrupts all versions — immutability must be enforced.
- **Amortization:** Some persistent structures (queues) use lazy evaluation for efficiency.

## 50.6. Quick Reference

| Structure | Persistent Variant | Overhead |
|-----------|-------------------|----------|
| Linked list | Fully persistent | O(1) per update |
| Binary tree | Path copying | O(log n) per update |
| Array | Fat nodes / copy-on-write | O(1)–O(n) |
| Queue | Banker's method | O(1) amortized |

| Go stdlib | Usage |
|-----------|-------|
| Immutable by convention | Slices share arrays (but not truly persistent) |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 50:</strong> Persistent data structures trade space for time travel — preserving every version of data by sharing unchanged parts and copying only modified paths. They enable the functional programming paradigm, version control systems, and undo functionality. The insight is profound: immutability is not a limitation but a superpower that eliminates entire classes of bugs.
{{% /alert %}}
