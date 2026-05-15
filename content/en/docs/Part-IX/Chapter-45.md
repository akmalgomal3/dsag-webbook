---
weight: 90200
title: "Chapter 45: Skip Lists"
description: "Skip Lists"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Skip lists are a probabilistic alternative to balanced trees.</em>" : William Pugh</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 46 introduces skip lists: a randomized linked list structure achieving <code>O(log n)</code> search without complex rebalancing logic.
{{% /alert %}}

## 46.1. The Problem with Balanced Trees

**Definition:** <abbr title="A data structure that allows fast search within an ordered sequence of elements using a hierarchy of linked lists that skip over intermediate elements.">Skip lists</abbr> offer the performance of balanced trees with the absolute simplicity of linked lists. Invented by William Pugh in 1989 as a simpler alternative to red-black trees.

**Background & Philosophy:**
The philosophy is probabilistic simplicity. Balancing an AVL or Red-Black tree involves incredibly complex rotations and edge cases. A Skip List abandons rigid mathematical guarantees, replacing them with coin flips. By randomly promoting elements to "express lanes," it achieves <code>O(log n)</code> performance statistically, drastically simplifying the code.

**Use Cases:**
Concurrent databases (Redis Sorted Sets, LevelDB) and in-memory indexing where lock contention must be minimized.

**Memory Mechanics:**
Skip lists avoid the massive, locked restructuring events required by B-Trees. However, they allocate nodes with variable-length arrays of `next` <abbr title="A variable that stores a memory address.">pointers</abbr>. In Go, `make([]*Node, level)` triggers <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocation for every single insertion. This scatters memory nodes wildly across the heap, completely destroying <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> coherence during a traversal. Thus, while algorithmically <code>O(log n)</code>, Skip Lists often lose to B-Trees purely due to <abbr title="Inefficient RAM usage creating small unusable blocks">memory fragmentation</abbr>.

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

Expected number of levels is securely bounded by <code>O(log n)</code>.

## 46.3. Operations

### Search

Start at the top-left, move right while current ≤ target, drop down when exceeded.

### Insertion

```go
package main

import (
	"fmt"
	"math/rand"
)

type Node struct {
	key     int
	forward []*Node
}

type SkipList struct {
	head     *Node
	level    int
	maxLevel int
}

func NewSkipList(maxLevel int) *SkipList {
	return &SkipList{
		head:     &Node{forward: make([]*Node, maxLevel)},
		level:    1,
		maxLevel: maxLevel,
	}
}

func (sl *SkipList) randomLevel() int {
	lvl := 1
	for rand.Float64() < 0.5 && lvl < sl.maxLevel {
		lvl++
	}
	return lvl
}

func (sl *SkipList) Insert(key int) {
	update := make([]*Node, sl.maxLevel)
	current := sl.head

	for i := sl.level - 1; i >= 0; i-- {
		for current.forward[i] != nil && current.forward[i].key < key {
			current = current.forward[i]
		}
		update[i] = current
	}

	level := sl.randomLevel()
	if level > sl.level {
		for i := sl.level; i < level; i++ {
			update[i] = sl.head
		}
		sl.level = level
	}

	node := &Node{key: key, forward: make([]*Node, level)}
	for i := 0; i < level; i++ {
		node.forward[i] = update[i].forward[i]
		update[i].forward[i] = node
	}
}

func main() {
	sl := NewSkipList(16)
	sl.Insert(10)
	fmt.Println("Skip list functional.")
}
```

| Operation | Average | Worst |
|-----------|---------|-------|
| Search | <code>O(log n)</code> | <code>O(n)</code> |
| Insert | <code>O(log n)</code> | <code>O(n)</code> |
| Delete | <code>O(log n)</code> | <code>O(n)</code> |

## 46.4. Analysis

With incredibly high probability, skip lists maintain <code>O(log n)</code> height. The expected number of pointers is 2n, ensuring strong space efficiency.

### Comparison

| Structure | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|-------|
| Skip list | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Red-black tree | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| AVL tree | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |

## 46.5. Decision Matrix

| Choose Skip Lists When... | Choose Trees When... |
|---------------------------|---------------------|
| Simplicity is paramount | Strict deterministic guarantees are mandated |
| Concurrent modifications exist | Peak cache efficiency is critical |
| Teaching or learning the concept | Running production with strict SLAs |

### Edge Cases & Pitfalls

- **Bad randomness:** A deterministic pseudo-random generator is essential for predictability.
- **Max level:** Always securely set the max level to `log₂(max_elements) + 1`.
- **Worst case:** Extremely unlikely but theoretically possible: all elements settle at level 1.

## 46.6. Quick Reference

| Parameter | Typical Value |
|-----------|---------------|
| p (promotion probability) | 0.5 |
| Max level | 16 to 32 |
| Expected pointers | 2n |

| Go stdlib | Usage |
|-----------|-------|
| `sync.Map` | Heavily inspired by skip list principles |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 44:</strong> Skip lists prove that randomization can replace deterministic complexity. By flipping coins to build express lanes through a linked list, they achieve balanced-tree performance with code simple enough to write in minutes. When you need <code>O(log n)</code> with minimal implementation risk, skip lists are often the right choice.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/Chapter-9/)
- [Chapter 27: Probabilistic and Randomized Algorithms](/docs/part-vi/Chapter-27/)
- [Chapter 44: B-Trees](/docs/part-ix/Chapter-44/)
