---
weight: 20300
title: "Chapter 7: Hashing and Hash Tables"
description: "Hashing and Hash Tables"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The art of programming is the art of organizing complexity.</em>" — Niklaus Wirth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 7 covers Go maps, FNV hashes, SHA-256 digests, and consistent hashing for distributed systems.
{{% /alert %}}

## 7.1. Hash Tables

**Definition:** Hash table maps keys to values using hash function. Go `map[K]V` uses hash table.

**Mechanics:**
Hash table trades space for time. Extra memory footprint buys constant-time access. Search problem becomes index computation.

In Go, `map` is pointer to `hmap` struct. `hmap` stores array of `bmap` (buckets). Each bucket holds 8 key-value pairs. Hash low-order bits pick bucket. High-order bits cache equality check. Collision uses linked list of overflow buckets. Map iteration causes cache misses: buckets scatter in heap.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Insert | <code>O(1)</code> amortized | Rehashes when growing |
| Lookup | <code>O(1)</code> amortized | Worst case <code>O(n)</code> |
| Delete | <code>O(1)</code> amortized | Does not shrink memory |

### Pseudocode

```text
HashTable():
    m = empty hash table with capacity 100
    insert ("foo", 1) into m
    insert ("bar", 2) into m
    if "foo" exists in m:
        print value of "foo"
    delete "bar" from m
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func main() {
    m := make(map[string]int, 100) // pre-allocate
    m["foo"] = 1
    m["bar"] = 2

    if v, ok := m["foo"]; ok {
        fmt.Println(v)
    }
    delete(m, "bar")
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Need fast key lookups | Need ordered data |
| Keys are unique and comparable | Keys lack equality definition |

### Edge Cases & Pitfalls

- **Unordered:** Map iteration is not sequential.
- **Concurrent write:** Panics without synchronization.
- **Key mutability:** Slices and maps cannot be keys.

## 7.2. Custom Hash Functions

**Definition:** Use `hash/fnv` or FNV-1a for non-cryptographic hashing.

**Mechanics:**
Non-cryptographic hashes prioritize speed and low collision. FNV-1a XORs bytes and multiplies by prime. Logic runs in CPU registers. Spatial locality improves speed on contiguous byte slices.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| FNV-1a | <code>O(n)</code> | n = data length |
| Murmur3 | <code>O(n)</code> | Better distribution |

### Pseudocode

```text
HashString(s):
    h = initialize FNV-1a hash
    for each byte in s:
        update h with byte
    return final hash value
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "hash/fnv"
)

func hashString(s string) uint32 {
    h := fnv.New32a()
    h.Write([]byte(s))
    return h.Sum32()
}

func main() {
    fmt.Println(hashString("hello"))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Need fast, deterministic hash | Need cryptographic security |

### Edge Cases & Pitfalls

- **Collision:** Custom hash must distribute values evenly.
- **Seed:** Consider seeded hash for large tables.

## 7.3. Cryptographic Hashing

**Definition:** Cryptographic hash produces fixed-size digest. Infeasible to reverse. Go provides `crypto/sha256` and `crypto/sha512`.

**Mechanics:**
Digest resists preimage and collision attacks. SHA-256 processes 64-byte blocks. Logical operations tax ALU. Go uses assembly and Intel SHA extensions for speed.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| SHA-256 | <code>O(n)</code> | n = input size |
| Compare | <code>O(1)</code> | Fixed-length digest |

### Pseudocode

```text
SHA256(data):
    sum = cryptographic digest of data
    return sum as hex string
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/sha256"
    "fmt"
)

func main() {
    data := []byte("secret")
    sum := sha256.Sum256(data)
    fmt.Printf("%x\n", sum)
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Need data integrity | Need raw speed |
| Password storage (with salt) | Simple hashing |

### Edge Cases & Pitfalls

- **Timing attack:** Use `hmac.Equal` for comparison.
- **Passwords:** Use `bcrypt` or `argon2`. Raw SHA-256 is too fast.

## 7.4. Consistent Hashing

**Definition:** Consistent hashing maps keys and nodes to a ring. Minimizes remapping during node changes.

**Mechanics:**
Modulo hashing (`hash % N`) triggers mass migration when N changes. Consistent hashing decouples key from server count. Both map to circular integer space. Sorted slice in RAM implements ring. Binary search finds server.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Add node | <code>O(log n)</code> | Insert into sorted ring |
| Lookup | <code>O(log n)</code> | Binary search |
| Remove node | <code>O(log n)</code> | Delete from ring |

### Pseudocode

```text
HashKey(key):
    h = hash of key using FNV-1a
    return h

ConsistentHash(ring, key):
    h = HashKey(key)
    i = binary search first index in ring where ring[i] >= h
    if i not found:
        i = 0
    return i
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "hash/fnv"
    "sort"
)

type Ring []uint32

func (r Ring) Search(h uint32) int {
    return sort.Search(len(r), func(i int) bool { return r[i] >= h })
}

func hashKey(key string) uint32 {
    h := fnv.New32a()
    h.Write([]byte(key))
    return h.Sum32()
}

func main() {
    ring := Ring{10, 100, 1000}
    fmt.Println(ring.Search(hashKey("foo")))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Distributed caching | Single-node deployment |
| Dynamic node counts | Small datasets |

### Edge Cases & Pitfalls

- **Skew:** Use virtual nodes for even distribution.
- **Clockwise wrap:** Handle logic transition from ring end to start.

### Anti-Patterns

- **Unsynced Map Access:** Concurrent write causes fatal error. Use `sync.Mutex`.
- **Mutable Keys:** Slices cannot be keys. Convert to string first.
- **SHA-256 for Passwords:** Too fast for safety. Use `bcrypt`.
- **Modulo Hashing:** Triggers re-mapping. Use consistent hashing for clusters.
- **Stale Memory:** Map buckets do not shrink. Recreate map to reclaim RAM.
- **Unsafe Comparison:** `==` allows timing attacks. Use `hmac.Equal`.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Map | built-in | <code>O(1)</code> avg | . | Key-value store |
| FNV | `hash/fnv` | <code>O(n)</code> | . | Checksum |
| SHA-256 | `crypto/sha256` | <code>O(n)</code> | . | Integrity |
| Consistent Hash | custom | <code>O(log n)</code> | . | Clusters |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Use maps for lookups. Use FNV for checksums. Use SHA-256 for integrity. Use consistent hashing for distributed clusters.
{{% /alert %}}

## See Also

- [Chapter 5: Fundamental Data Structures in Go](/docs/part-ii/chapter-5/)
- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 46: Bloom Filters](/docs/part-ix/chapter-46/)
