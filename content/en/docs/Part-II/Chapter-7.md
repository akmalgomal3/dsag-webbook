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
<strong>"<em>The art of programming is the art of organizing complexity.</em>" : Niklaus Wirth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 7 focuses on <abbr title="The process of mapping data of arbitrary size to fixed-size values.">hashing</abbr> and hash tables, covering Go's built-in map, custom non-cryptographic hashes (FNV), cryptographic digests (SHA-256), and <abbr title="Hashing that minimizes rehashing when the table resizes">consistent hashing</abbr> architectures for distributed systems.
{{% /alert %}}

## 7.1. Hash Tables

**Definition:** A <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr> maps keys to values using a <abbr title="A function mapping data of arbitrary size to fixed-size values">hash function</abbr>. Go provides the built-in `map[K]V` which is backed by a <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr>.

**Background & Philosophy:**
The primary philosophy of a hash table is trading space for time. By allocating a larger memory footprint than strictly necessary, we can probabilistically guarantee <code>O(1)</code> access time. Hash tables convert a search problem (which would otherwise require iterating through elements) into a direct mathematical computation of an index. 

**Use Cases:**
Hash tables are ubiquitous: from implementing caches (like Redis) and counting word frequencies in a text, to mapping database connections to active session IDs in a web server.

**Memory Mechanics:**
In Go, a `map` is a <abbr title="A variable that stores a memory address.">pointer</abbr> to a runtime `hmap` struct. The core of this struct is an array of `bmap` (buckets). Each bucket holds up to 8 key-value pairs. When a key is inserted, Go computes a <abbr title="The process of mapping data of arbitrary size to fixed-size values.">hash</abbr> and uses the low-order bits to pick a bucket. The high-order bits are cached inside the bucket array to rapidly check for equality without following <abbr title="A variable that stores a memory address.">pointers</abbr>. If multiple keys fall into the same bucket (a <abbr title="An event when two keys hash to the same index.">collision</abbr>), Go uses a <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">linked list</abbr> of overflow buckets. Because these buckets are scattered across the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>, map iteration causes frequent <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>.

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

**Background & Philosophy:**
A hash function is a one-way mathematical meat-grinder. The philosophy behind non-cryptographic hashes like FNV-1a (Fowler-Noll-Vo) or MurmurHash is to prioritize speed, excellent avalanche behavior (changing one input bit flips many output bits), and low <abbr title="An event when two keys hash to the same index.">collision</abbr> rates, explicitly sacrificing cryptographic security.

**Use Cases:**
Used when writing custom hash tables, distributing network packets evenly across servers (load balancing), or quickly comparing large files by generating checksums.

**Memory Mechanics:**
Non-cryptographic hash functions process bytes sequentially. FNV-1a, for example, XORs the incoming byte with the current hash value and then multiplies by a large prime number. This algorithm runs entirely in the CPU registers (without touching <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>) and utilizes <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr> if the input string is a <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> byte slice. Thus, it operates at memory-bandwidth speeds.

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

**Background & Philosophy:**
The philosophy here shifts from "speed" to "resistance". A cryptographic hash function is explicitly designed to resist preimage attacks (finding the input given the hash) and <abbr title="An event when two keys hash to the same index.">collision</abbr> attacks (finding two inputs that yield the same hash). 

**Use Cases:**
Essential for storing user passwords (using specialized slow hashes like bcrypt), generating digital signatures for JWT tokens, or verifying the integrity of downloaded binaries.

**Memory Mechanics:**
Algorithms like SHA-256 operate on fixed-size blocks (e.g., 64 bytes). They maintain an internal state array (working variables) that resides in the CPU registers. However, unlike FNV-1a, SHA-256 involves dozens of complex logical operations (rotations, XORs, additions) per block. This heavily taxes the ALU (Arithmetic Logic Unit) of the CPU, making it inherently slower. Go's standard library often uses assembly language to optimize these operations utilizing specific CPU instructions (like Intel SHA extensions).

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

**Background & Philosophy:**
In a traditional distributed hash table (`hash(key) % N_servers`), adding one server changes the modulo for almost every key, forcing massive data migrations. The philosophy of consistent hashing is to decouple the key's hash from the total number of servers. Instead, both keys and servers are mapped to a massive circular integer space (the "ring").

**Use Cases:**
The backbone of modern distributed systems, including load balancing in API gateways, data sharding in distributed databases (like Cassandra or DynamoDB), and cache clustering (like Memcached).

**Memory Mechanics:**
A consistent hashing ring is usually implemented as a sorted slice of integers in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. When a request arrives, the system hashes the key to produce a 32-bit or 64-bit integer, then performs a <abbr title="A search algorithm that finds the position of a target value within a sorted array.">binary search</abbr> <code>O(log n)</code> on the slice to find the first server whose hash is greater than the key's hash. Because the ring is a <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> array, the binary search is extremely <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> efficient.

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
| Map | built-in | <code>O(1)</code> avg | . | Key-value store |
| FNV | `hash/fnv` | <code>O(n)</code> | . | Checksum, <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr> |
| SHA-256 | `crypto/sha256` | <code>O(n)</code> | . | Integrity, signing |
| Consistent Hash | custom | <code>O(log n)</code> | . | Distributed systems |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 7:</strong> This chapter explores <abbr title="The process of mapping data of arbitrary size to fixed-size values.">hashing</abbr> and hash tables in Go, including built-in maps, custom non-cryptographic hashes (FNV), cryptographic digests (SHA-256), and <abbr title="Hashing that minimizes rehashing when the table resizes">consistent hashing</abbr> for distributed systems. Use built-in maps for general key-value storage, FNV for checksums, SHA-256 for data integrity, and <abbr title="Hashing that minimizes rehashing when the table resizes">consistent hashing</abbr> when nodes frequently join or leave a cluster.
{{% /alert %}}

## See Also

- [Chapter 5: Fundamental Data Structures in Go](/docs/part-ii/chapter-5/)
- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 46: Bloom Filters](/docs/part-ix/chapter-46/)
