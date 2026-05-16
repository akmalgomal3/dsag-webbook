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
<strong>"<em>There are only two hard things in Computer Science: cache invalidation and naming things.</em>" — Phil Karlton</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
LRU (Least Recently Used) cache is the standard eviction strategy. Combines hash tables with linked lists for <code>O(1)</code> operations.
{{% /alert %}}

## 47.1. Purpose

**Definition:** <abbr title="A cache eviction policy that discards the least recently used items first when the cache is full.">Least Recently Used (LRU)</abbr> cache holds fixed-size data. Discards oldest accessed item when capacity reached.

**Temporal Locality:**
Recent data likely requested again soon. Freshest data stays in RAM. Stale data evicted to shield slow databases or disks.

**Use Cases:**
Database query caching. CDN edge nodes. CPU hardware (L1/L2 caches).

**Memory Mechanics:**
Couples `map` (O(1) lookup) with doubly-linked list (O(1) reordering). Memory size strictly capped. Access triggers pointer swaps. Mutex <abbr title="A situation where multiple threads attempt to modify the same memory address simultaneously.">lock contention</abbr> bottlenecks concurrent reads.

### Caching Impact

| System | Without Cache | With Cache |
|--------|--------------|------------|
| CPU | ~100 ns (RAM) | ~1 ns (L1) |
| Web server | ~100 ms (DB) | ~1 ms (Redis) |
| CDN | ~500 ms (Origin) | ~20 ms (Edge) |

## 47.2. Data Structure

LRU requirements:
- **O(1) lookup:** <abbr title="A data structure that implements an associative array using a hash function.">Hash table</abbr> maps key to node.
- **O(1) eviction:** <abbr title="A linked list where each node points to both the next and previous nodes.">Doubly linked list</abbr> tracks usage order.

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

## 47.3. Operations

| Operation | Time | Description |
|-----------|------|-------------|
| Get | <code>O(1)</code> | Hash lookup + list reorder. |
| Put | <code>O(1)</code> | Insert/update + eviction check. |
| Evict | <code>O(1)</code> | Remove tail node and map entry. |

## 47.4. Eviction Strategies

| Strategy | Eviction Target | Use Case |
|----------|----------------|----------|
| **LRU** | Least recently used. | General purpose. |
| **LFU** | Least frequently used. | Popular item persistence. |
| **FIFO** | First in, first out. | Streaming buffers. |
| **Random** | Random item. | Adversarial protection. |
| **TTL** | Time-based expiry. | Session data. |

## 47.5. Decision Matrix

| Use LRU When... | Use LFU When... |
|-----------------|-----------------|
| Recency predicts future requests. | Frequency matters more than recency. |
| Workload has temporal locality. | Some items stay consistently hot. |

### Edge Cases & Pitfalls

- **Thread Safety:** Standard implementation requires `sync.RWMutex` or sharding.
- **Overhead:** High pointer counts increase memory consumption (~48 bytes/node).
- **Sequential Scans:** Full scans flush hot data (cache pollution).

### Anti-Patterns

- **Scan Thrashing:** sequential reads push useful data out. Use LRU-2 or ARC to resist.
- **Global Locks:** Unprotected maps fail in concurrent Go. wrap in mutex or use sharded caches.
- **Blind Capacity:** Too small kills hit rate. Too large triggers GC pressure.
- **Frequency Ignore:** Use LFU if item popularity stays static over long windows.

## 47.6. Quick Reference

| Parameter | Value |
|-----------|-------|
| Hit Rate Target | > 80% |
| Pointer Overhead | ~48 bytes/entry |
| Memory usage | ~2x entry size |

| Go stdlib | Usage |
|-----------|-------|
| `container/list` | Generic doubly linked list. |
| `github.com/hashicorp/golang-lru` | Production-ready implementation. |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
LRU caches combine hash tables for speed and linked lists for order. Powers database query layers and web servers.
{{% /alert %}}

## See Also

- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 7: Hashing and Hash Tables](/docs/part-ii/chapter-7/)
- [Chapter 46: Bloom Filters](/docs/part-ix/chapter-46/)
