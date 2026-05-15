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
<strong>"<em>Persistence is the path to immutability.</em>" : Chris Okasaki</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 50 explores persistent data structures — structures that preserve previous versions when modified, enabling time-travel debugging and functional programming paradigms.
{{% /alert %}}

## 50.1. What Is Persistence?

**Definition:** A <abbr title="A data structure that always preserves the previous version of itself when it is modified, enabling access to any version.">persistent data structure</abbr> preserves all previous versions after modification. There are two flavors:

**Background & Philosophy:**
The philosophy is absolute immutability. In standard data structures, an update destroys the past. Persistent structures treat data like a timeline: an update does not overwrite the old data; it creates a new "version" of the world that points back to the unchanged parts of the old world.

**Use Cases:**
Git version control (trees and blobs), functional programming languages (Clojure, Haskell), and time-travel debugging tools.

**Memory Mechanics:**
Persistent structures rely heavily on <abbr title="A technique where only the nodes along the path from root to the modified node are copied, sharing unchanged subtrees.">"Path Copying"</abbr>. Instead of deep-copying an entire 1-million node tree (which would instantly exhaust memory), they only copy the <code>O(log n)</code> nodes along the path from the root to the modified leaf. This structural sharing heavily depends on the <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collector</abbr> to reclaim versions that are no longer referenced. Because nodes are never modified in-place, persistent structures completely eliminate data races, making them inherently thread-safe without any memory locks.

| Type | Behavior | Example |
|------|----------|---------|
| **Partial persistence** | Read all versions, write only latest | Versioned logs |
| **Full persistence** | Read and write any version | Functional data structures |

## 50.2. Path Copying

The key technique: when updating a node, copy the path from root to that node, sharing unchanged subtrees.

### Persistent Linked List

```go
package main

import "fmt"

type List struct {
    val  int
    next *List
}

// Prepend returns a NEW list, original unchanged
func (l *List) Prepend(v int) *List {
    return &List{val: v, next: l}
}

func main() {
    // Original list still valid
    list1 := &List{val: 1}
    list2 := list1.Prepend(2)
    
    fmt.Println(list1.val) // 1
    fmt.Println(list2.val) // 2
}
```

## 50.3. Persistent <abbr title="A tree where each node has at most two children">Binary Tree</abbr>

Update a leaf → copy the leaf, then copy every ancestor up to the root. Unchanged siblings are shared.

| Operation | Time | Space |
|-----------|------|-------|
| Update | <code>O(log n)</code> | <code>O(log n)</code> new nodes |
| Access | <code>O(log n)</code> | <code>O(1)</code> |

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

- **Space growth:** n updates create <code>O(n log n)</code> nodes — garbage collection essential.
- **Node sharing:** Modifying a "shared" node corrupts all versions — immutability must be stringently enforced.
- **Amortization:** Some persistent structures (queues) use lazy evaluation for efficiency.

## 50.6. Quick Reference

| Structure | Persistent Variant | Overhead |
|-----------|-------------------|----------|
| Linked list | Fully persistent | <code>O(1)</code> per update |
| <abbr title="A tree where each node has at most two children">Binary tree</abbr> | Path copying | <code>O(log n)</code> per update |
| Array | Fat nodes / copy-on-write | <code>O(1)</code>–<code>O(n)</code> |
| Queue | Banker's method | <code>O(1)</code> amortized |

| Go stdlib | Usage |
|-----------|-------|
| Immutable by convention | Slices share arrays (but not truly persistent) |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 48:</strong> Persistent data structures trade space for time travel — preserving every version of data by sharing unchanged parts and copying only modified paths. They enable functional programming, version control systems, and undo functionality. The key insight: immutability eliminates entire classes of bugs by preventing unexpected mutation.
{{% /alert %}}

## See Also

- [Chapter 36: Trie Data Structures](/docs/part-vii/Chapter-36/)
- [Chapter 48: Suffix Arrays](/docs/part-ix/Chapter-48/)
- [Chapter 41: Evolution of Data Structures](/docs/part-viii/Chapter-41/)
