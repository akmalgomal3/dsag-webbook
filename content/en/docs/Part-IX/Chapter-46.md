---
weight: 9100
title: "Chapter 46 - Skip Lists"
description: "Skip Lists"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Skip lists are a probabilistic alternative to balanced trees.</em>" — William Pugh</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 46 introduces skip lists — a randomized linked list structure achieving O(log n) search without complex rebalancing logic.
{{% /alert %}}

## 46.1. The Problem with Balanced Trees

**Definition:** <abbr title="A data structure that allows fast search within an ordered sequence of elements using a hierarchy of linked lists that skip over intermediate elements.">Skip lists</abbr> offer the performance of balanced trees with the simplicity of linked lists. Invented by William Pugh in 1989 as a simpler alternative to red-black trees.

### Why Skip Lists?

| Aspect | Balanced Tree | Skip List |
|--------|---------------|-----------|
| Code complexity | High (rotations) | Low (randomized levels) |
| Deterministic | Yes | Probabilistic |
| Concurrency | Hard (tree restructuring) | Easier (local updates) |
| Cache performance | Poor (pointer chasing) | Moderate |

## 46.2. Structure

A skip list is a hierarchy of linked lists. The bottom level contains all elements. Each higher level acts as an "express lane" skipping over elements below.

### Level Assignment

Each element's level is determined by coin flips:
- Level 1: probability 1/2
- Level 2: probability 1/4
- Level k: probability 1/2^k

Expected number of levels: O(log n).

## 46.3. Operations

### Search

Start at the top-left, move right while current ≤ target, drop down when exceeded.

### Insertion

```go
func (sl *SkipList) insert(key int) {
    update := make([]*Node, sl.maxLevel)
    current := sl.head
    
    for i := sl.level - 1; i >= 0; i-- {
        for current.forward[i] != nil && 
            current.forward[i].key < key {
            current = current.forward[i]
        }
        update[i] = current
    }
    
    level := sl.randomLevel()
    node := &Node{key: key, forward: make([]*Node, level)}
    
    for i := 0; i < level; i++ {
        node.forward[i] = update[i].forward[i]
        update[i].forward[i] = node
    }
}
```

| Operation | Average | Worst |
|-----------|---------|-------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

## 46.4. Analysis

With high probability (1 - 1/n^c), skip lists maintain O(log n) height. The expected number of pointers is 2n — space-efficient.

### Comparison

| Structure | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|-------|
| Skip list | O(log n) | O(log n) | O(log n) | O(n) |
| Red-black tree | O(log n) | O(log n) | O(log n) | O(n) |
| AVL tree | O(log n) | O(log n) | O(log n) | O(n) |

## 46.5. Decision Matrix

| Choose Skip Lists When... | Choose Trees When... |
|---------------------------|---------------------|
| Simplicity is paramount | Deterministic guarantees needed |
| Concurrent modifications | Cache efficiency critical |
| Teaching/learning | Production with strict SLAs |

### Edge Cases & Pitfalls

- **Bad randomness:** A deterministic pseudo-random generator is essential.
- **Max level:** Set max level to ~log₂(max_elements) + 1.
- **Worst case:** Extremely unlikely but possible — all elements at level 1.

## 46.6. Quick Reference

| Parameter | Typical Value |
|-----------|---------------|
| p (promotion probability) | 0.5 |
| Max level | 16–32 |
| Expected pointers | 2n |

| Go stdlib | Usage |
|-----------|-------|
| `sync.Map` | Inspired by skip list principles |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 46:</strong> Skip lists prove that randomization can replace deterministic complexity. By flipping coins to build express lanes through a linked list, they achieve balanced-tree performance with code simple enough to write in minutes. When you need O(log n) with minimal implementation risk, skip lists are often the right choice.
{{% /alert %}}
