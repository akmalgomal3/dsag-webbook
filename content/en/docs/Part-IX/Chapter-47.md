---
weight: 90400
title: "Chapter 47: LRU Cache"
description: "LRU Cache"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>There are only two hard things in Computer Science: cache invalidation and naming things.</em>" : Phil Karlton</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 48 covers the LRU (Least Recently Used) cache — the most common caching strategy, combining hash tables with linked lists for <code>O(1)</code> operations.
{{% /alert %}}

## 48.1. The Caching Problem

**Definition:** A <abbr title="A cache eviction policy that discards the least recently used items first when the cache is full.">Least Recently Used (LRU)</abbr> cache maintains a fixed-size collection where the least recently accessed item is evicted when space is needed.

**Background & Philosophy:**
The philosophy is <abbr title="The tendency to reuse recently accessed memory addresses">temporal locality</abbr>. If a piece of data was requested recently, it is statistically highly probable it will be requested again very soon. By explicitly keeping the "freshest" data readily available and discarding the stale data, an LRU cache creates a buffer that shields the slow backing store (database or disk) from repeated identical requests.

**Use Cases:**
Database query caching, CDN edge nodes, and CPU hardware caching (L1/L2 caches physically implement LRU logic).

**Memory Mechanics:**
An LRU cache couples a `map` (for <code>O(1)</code> lookups) with a doubly-linked list (for <code>O(1)</code> reordering). In Go, the map stores <abbr title="A variable that stores a memory address.">pointers</abbr> to the list nodes. This structure guarantees that cache memory size is strictly capped. However, every time an item is accessed (even a read), the doubly-linked list must update <abbr title="A variable that stores a memory address.">pointers</abbr> to move the node to the front. These pointer swaps trigger memory writes, meaning that in highly concurrent environments, read-heavy operations on an LRU cache can bottleneck severely due to mutex <abbr title="A situation where multiple threads attempt to modify the same memory address simultaneously.">lock contention</abbr> compared to lock-free caches.

### Why Caching Matters

| System | Without Cache | With Cache |
|--------|--------------|------------|
| CPU | ~100 ns (RAM) | ~1 ns (L1) |
| Web server | ~100 ms (database) | ~1 ms (Redis) |
| CDN | ~500 ms (origin) | ~20 ms (edge) |

## 48.2. The Data Structure

LRU cache requires:
- **O(1) lookup:** <abbr title="A data structure that implements an associative array using a hash function.">Hash table</abbr> maps key to node
- **O(1) eviction:** <abbr title="A linked list where each node points to both the next and previous nodes.">Doubly linked list</abbr> maintains usage order

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr>: LRU Cache

```go
package main

import "fmt"

type LRUCache struct {
    capacity int
    cache    map[int]*Node
    head     *Node // Most recent
    tail     *Node // Least recent
}

type Node struct {
    key, val   int
    prev, next *Node
}

func NewLRUCache(capacity int) *LRUCache {
    c := &LRUCache{
        capacity: capacity,
        cache:    make(map[int]*Node),
        head:     &Node{},
        tail:     &Node{},
    }
    c.head.next = c.tail
    c.tail.prev = c.head
    return c
}

func (c *LRUCache) removeNode(node *Node) {
    node.prev.next = node.next
    node.next.prev = node.prev
}

func (c *LRUCache) addToFront(node *Node) {
    node.prev = c.head
    node.next = c.head.next
    c.head.next.prev = node
    c.head.next = node
}

func (c *LRUCache) moveToFront(node *Node) {
    c.removeNode(node)
    c.addToFront(node)
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
        lru := c.tail.prev
        c.removeNode(lru)
        delete(c.cache, lru.key)
    }
    node := &Node{key: key, val: val}
    c.cache[key] = node
    c.addToFront(node)
}

func main() {
    lru := NewLRUCache(2)
    lru.Put(1, 10)
    lru.Put(2, 20)
    fmt.Println(lru.Get(1)) // 10
    lru.Put(3, 30) // evicts key 2
    fmt.Println(lru.Get(2)) // -1
}
```

## 48.3. Operations

| Operation | Time | Description |
|-----------|------|-------------|
| Get | <code>O(1)</code> | Hash lookup + list reorder |
| Put | <code>O(1)</code> | Insert or update + possible eviction |
| Evict | <code>O(1)</code> | Remove tail, delete from hash |

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
- **Concurrency:** Standard LRU is not thread-safe. You MUST use `sync.RWMutex` or sharded locks for concurrent access.
- **Memory overhead:** Each entry has ~48 bytes of <abbr title="A variable that stores a memory address.">pointer</abbr> overhead plus the map overhead.
- **Scan resistance:** LRU fails under sequential scans (all items become "recent" and flush the cache).

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
<strong>Summary Chapter 47:</strong> The LRU cache is a masterclass in combining data structures: hash tables for <code>O(1)</code> lookup and doubly linked lists for <code>O(1)</code> reordering. It powers databases, operating systems, and web servers. Understanding LRU means understanding that the best eviction strategy depends on your access patterns, not abstract perfection.
{{% /alert %}}

## See Also

- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 7: Hashing and Hash Tables](/docs/part-ii/chapter-7/)
- [Chapter 46: Bloom Filters](/docs/part-ix/chapter-46/)
