---
weight: 20300
title: "Chapter 7 - Hashing and Hash Tables"
description: "Hashing and Hash Tables"
icon: "article"
date: "2024-08-24T23:42:10+07:00"
lastmod: "2024-08-24T23:42:10+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="📘" context="success" %}}
Chapter 7 focuses on hashing and hash tables, covering Go's built-in map, custom non-cryptographic hashes (FNV), cryptographic digests (SHA-256), and consistent hashing architectures for distributed systems.
{{% /alert %}}

## 7.1. Hash Tables

**Definition:** A <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr> maps keys to values using a hash function. Go provides the built-in `map[K]V` which is backed by a <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Insert | <code>O(1)</code> amortized | Rehashes when growing |
| Lookup | <code>O(1)</code> amortized | Worst case <code>O(n)</code> |
| Delete | <code>O(1)</code> amortized | Does not automatically shrink |

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
| Need fast <abbr title="A field or set of fields used to identify a record.">key</abbr> lookups | Need ordered data |
| Keys are unique and comparable | Complex keys lack equality definitions |

### Edge Cases & Pitfalls

- **Unordered:** Map <abbr title="The repetition of a process, typically using loops.">iteration</abbr> is not sequential.
- **Concurrent write:** Causes a panic if written concurrently without synchronization.
- **<abbr title="A field or set of fields used to identify a record.">Key</abbr> mutability:** Slices or maps cannot be used as keys.

## 7.2. Custom Hash Functions

**Definition:** For non-cryptographic hashing needs, use the `hash/fnv` package or implement a manual hash like FNV-1a.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| FNV-1a | <code>O(n)</code> | n = data length |
| Murmur3 | <code>O(n)</code> | Better distribution (requires external <abbr title="A collection of precompiled routines that a program can use.">library</abbr>) |

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
| Need a fast, deterministic hash | Cryptographic security is required |

### Edge Cases & Pitfalls

- **<abbr title="An event when two keys hash to the same index.">Collision</abbr>:** A custom hash must distribute values evenly.
- **Seed:** FNV does not require a seed; for large hash tables, consider a seeded hash.

## 7.3. Cryptographic Hashing

**Definition:** A cryptographic hash function produces a fixed-size digest that is computationally infeasible to reverse. Go provides `crypto/sha256` and `crypto/sha512`.

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
| Need data integrity | Need raw speed (non-crypto hashes are faster) |
| Password hashing (with a salt/KDF) | Simple hashing without security needs |

### Edge Cases & Pitfalls

- **Timing attack:** Use `hmac.Equal` to compare digests safely.
- **Passwords:** Never use raw SHA-256 for passwords; use `bcrypt` or `argon2`.

## 7.4. Consistent Hashing

**Definition:** Consistent hashing minimizes <abbr title="A field or set of fields used to identify a record.">key</abbr> remapping when nodes are added or removed by placing both nodes and keys on a hash ring.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Add <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> | <code>O(log n)</code> | Insert into a sorted ring |
| Lookup | <code>O(log n)</code> | <abbr title="A search algorithm that finds the position of a target value within a sorted array.">Binary search</abbr> |
| Remove <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> | <code>O(log n)</code> | Delete from the ring |

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
| Nodes frequently go up/down | Very small datasets |

### Edge Cases & Pitfalls

- **Skew:** Use virtual nodes to ensure even distribution.
- **Clockwise wrap:** Ensure logic correctly handles wrapping around from the last ring <abbr title="A data structure that improves the speed of data retrieval operations.">index</abbr> to the first.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Map | built-in | <code>O(1)</code> avg | — | Key-value store |
| FNV | `hash/fnv` | <code>O(n)</code> | — | Checksum, <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr> |
| SHA-256 | `crypto/sha256` | <code>O(n)</code> | — | Integrity, signing |
| Consistent Hash | custom | <code>O(log n)</code> | — | Distributed systems |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 7:</strong> This chapter explores hashing and hash tables in Go, including built-in maps, custom non-cryptographic hashes (FNV), cryptographic digests (SHA-256), and consistent hashing for distributed systems. Use built-in maps for general key-value storage, FNV for checksums, SHA-256 for data integrity, and consistent hashing when nodes frequently join or leave a cluster.
{{% /alert %}}

## See Also

- [Chapter 5 — Fundamental Data Structures in Go](/docs/Part-II/Chapter-5/)
- [Chapter 6 — Elementary Data Structures](/docs/Part-II/Chapter-6/)
- [Chapter 47 — Bloom Filters](/docs/Part-IX/Chapter-47/)
