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
<strong>"<em>Skip lists are a probabilistic alternative to balanced trees.</em>" — William Pugh</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Skip lists achieve <code>O(log n)</code> search via randomization. Randomized linked lists avoid complex rebalancing logic.
{{% /alert %}}

## 45.1. Purpose

**Definition:** <abbr title="A data structure that allows fast search within an ordered sequence of elements using a hierarchy of linked lists that skip over intermediate elements.">Skip lists</abbr> match balanced tree performance using linked list simplicity. Invented by William Pugh in 1989.

**Probabilistic Simplicity:**
Balanced trees (AVL, Red-Black) require complex rotations. Skip lists use coin flips to promote elements to "express lanes." Statistical <code>O(log n)</code> performance simplifies code.

**Use Cases:**
Concurrent databases (Redis Sorted Sets, LevelDB). In-memory indexing. Systems requiring low lock contention.

**Memory Mechanics:**
Skip lists avoid B-Tree restructuring. Nodes use variable-length arrays of `next` <abbr title="A variable that stores a memory address.">pointers</abbr>. `make([]*Node, level)` in Go triggers <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocation. Scatters nodes wildly. Fragmented memory destroys <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> coherence.

### Comparison: Trees vs. Skip Lists

| Aspect | Balanced Tree | Skip List |
|--------|---------------|-----------|
| Complexity | High (rotations) | Low (randomized) |
| Determinism | Yes | Probabilistic |
| Concurrency | Hard (restructuring) | Easier (local updates) |
| Cache Fit | Poor | Moderate |

## 45.2. Structure

Hierarchy of linked lists. Bottom level contains all elements. Higher levels are "express lanes" skipping intermediate nodes.

### Level Assignment

Coin flips determine element level:
- Level 1: p = 1/2
- Level 2: p = 1/4
- Level k: p = 1/2^k

Expected levels bounded by <code>O(log n)</code>.

## 45.3. Operations

### Search

Start top-left. Move right while current ≤ target. Drop down when exceeded.

### Implementation: Go Skip List

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

## 45.4. Analysis

Skip lists maintain <code>O(log n)</code> height with high probability. Expected pointers are 2n. Space efficiency is strong.

### Complexity Comparison

| Structure | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|-------|
| Skip list | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| Red-black | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |
| AVL tree | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(log n)</code> | <code>O(n)</code> |

## 45.5. Decision Matrix

| Choose Skip Lists When... | Choose Trees When... |
|---------------------------|---------------------|
| Simplicity is critical | Determinism is mandated |
| Concurrency is high | Peak cache efficiency required |
| Teaching concepts | Production with strict SLAs |

### Edge Cases & Pitfalls

- **Randomness:** Requires deterministic pseudo-random generator.
- **Max Level:** Set to `log₂(max_elements) + 1`.
- **Worst Case:** Elements settling at Level 1 causes linear performance.

### Anti-Patterns

- **Real-time SLAs:** Worst case <code>O(n)</code> risks avionics or high-speed trading.
- **Wrong maxLevel:** Low levels saturate lanes. High levels waste memory.
- **Cache Sensitivity:** Pointer chasing scatters heap. B-trees beat skip lists in RAM latency tests.
- **Weak PRNG:** Biased coin flips void probabilistic guarantees.

## 45.6. Quick Reference

| Parameter | Typical Value |
|-----------|---------------|
| p (promotion) | 0.5 |
| Max level | 16 to 32 |
| Expected pointers | 2n |

| Go stdlib | Usage |
|-----------|-------|
| `sync.Map` | Inspired by skip list principles. |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
Randomization replaces deterministic complexity. Coin flips build express lanes. <code>O(log n)</code> performance with minimal implementation risk.
{{% /alert %}}

## See Also

- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
- [Chapter 27: Probabilistic and Randomized Algorithms](/docs/part-vi/chapter-27/)
- [Chapter 44: B-Trees](/docs/part-ix/chapter-44/)
