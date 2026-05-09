---
weight: 90400
title: "Chapter 48 - LRU Cache"
description: "LRU Cache"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>There are only two hard things in Computer Science: cache invalidation and naming things.</em>" — Phil Karlton</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 48 covers the LRU (Least Recently Used) cache — the most common caching strategy, combining hash tables with linked lists for O(1) operations.
{{% /alert %}}

## 48.1. The Caching Problem

**Definition:** A <abbr title="A cache eviction policy that discards the least recently used items first when the cache is full.">Least Recently Used (LRU)</abbr> cache maintains a fixed-size collection where the least recently accessed item is evicted when space is needed.

### Why Caching Matters

| System | Without Cache | With Cache |
|--------|--------------|------------|
| CPU | ~100 ns (RAM) | ~1 ns (L1) |
| Web server | ~100 ms (database) | ~1 ms (Redis) |
| CDN | ~500 ms (origin) | ~20 ms (edge) |

## 48.2. The Data Structure

LRU cache requires:
- **O(1) lookup:** Hash table maps key to node
- **O(1) eviction:** Doubly linked list maintains usage order

### Idiomatic Go: LRU Cache

```go
type LRUCache struct {
    capacity int
    cache    map[int]*Node
    head     *Node // Most recent
    tail     *Node // Least recent
}

type Node struct {
    key, val  int
    prev, next *Node
}

func (c *LRUCache) Get(key int) int {
    if node, ok := c.cache[key]; ok {
        c.moveToFront(node)
        return node.val
    }
    return -1
}

func (c *LRUCache) Put(key, val int) {
    if node, ok := c.cache[key]; ok {
        node.val = val
        c.moveToFront(node)
        return
    }
    if len(c.cache) >= c.capacity {
        delete(c.cache, c.tail.key)
        c.removeNode(c.tail)
    }
    node := &Node{key: key, val: val}
    c.cache[key] = node
    c.addToFront(node)
}
```

## 48.3. Operations

| Operation | Time | Description |
|-----------|------|-------------|
| Get | O(1) | Hash lookup + list reorder |
| Put | O(1) | Insert or update + possible eviction |
| Evict | O(1) | Remove tail, delete from hash |

## 48.4. Cache Eviction Strategies

| Strategy | Eviction Target | Use Case |
|----------|----------------|----------|
| **LRU** | Least recently used | General-purpose, temporal locality |
| **LFU** | Least frequently used | Popular items stay |
| **FIFO** | First in, first out | Simple streaming |
| **Random** | Random item | Avoiding adversarial patterns |
| **TTL** | Expired by time | Session data |

## 48.5. Decision Matrix

| Use LRU When... | Use LFU When... |
|-----------------|-----------------|
| Recent access predicts future access | Popularity matters more than recency |
| Workload has temporal locality | Some items are consistently hot |

### Edge Cases & Pitfalls

- **Capacity 0:** Handle as no-op or error.
- **Concurrency:** Standard LRU is not thread-safe — use `sync.RWMutex` or sharded caches.
- **Memory overhead:** Each entry has ~48 bytes of pointer overhead.
- **Scan resistance:** LRU fails under sequential scans (all items become "recent").

## 48.6. Quick Reference

| Parameter | Typical Value |
|-----------|---------------|
| Capacity | Application-dependent |
| Hit rate target | > 80% |
| Memory overhead | ~2x entry size |

| Go stdlib | Usage |
|-----------|-------|
| `container/list` | Can build LRU (but custom list is faster) |
| `github.com/hashicorp/golang-lru` | Production LRU implementation |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 48:</strong> The LRU cache is a masterclass in combining data structures — hash tables for O(1) lookup and doubly linked lists for O(1) reordering. It powers databases, operating systems, and web servers. Understanding LRU means understanding that the best eviction strategy depends on your access patterns, not abstract perfection.
{{% /alert %}}

## See Also

- [Chapter 6 — Elementary Data Structures](/docs/Part-II/Chapter-6/)
- [Chapter 7 — Hashing and Hash Tables](/docs/Part-II/Chapter-7/)
- [Chapter 47 — Bloom Filters](/docs/Part-IX/Chapter-47/)

