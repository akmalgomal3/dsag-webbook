---
weight: 90300
title: "Chapter 47: Bloom Filters"
description: "Bloom Filters"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A Bloom filter is a data structure that tells you an element is definitely not in a set, or maybe in a set.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 47 explores Bloom filters: a space-efficient probabilistic data structure for set membership testing with zero false negatives.
{{% /alert %}}

## 47.1. The Membership Problem

**Definition:** A <abbr title="A space-efficient probabilistic data structure that is used to test whether an element is a member of a set, with possible false positives but no false negatives.">Bloom filter</abbr> answers: "Is element X in set S?" with:
- **"No"** : Definitely not in set (100% accurate)
- **"Maybe"** : Might be in set (possible <abbr title="An error where a test incorrectly indicates the presence of a condition when it is not present.">false positive</abbr>)

**Background & Philosophy:**
The philosophy is acceptable inaccuracy. A Bloom Filter trades absolute certainty for extreme compression. It happily accepts a small margin of "False Positives" to mathematically guarantee zero "False Negatives", crushing gigabytes of data down into megabytes.

**Use Cases:**
Web browsers checking malicious URLs, CDNs preventing cache pollution, and databases (Cassandra, RocksDB) skipping expensive disk reads for non-existent keys.

**Memory Mechanics:**
A Bloom Filter relies on a single, massive bit array (often represented in Go as `[]uint64`). It hashes an item multiple times to flip specific bits. This requires jumping to completely random indices in the bit array. Because the array is usually several megabytes, these jumps constantly trigger <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>. However, executing 7 rapid cache misses in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> is still infinitely faster than executing a single mechanical seek on a physical hard drive.

### Space Efficiency

| Structure | Bits per Element | False Positive Rate |
|-----------|-----------------|---------------------|
| Hash table | 64+ | 0% |
| Bloom filter | 10 | 1% |

Storing 1 billion URLs: hash table ≈ 8 GB, Bloom filter ≈ 1 GB.

## 47.2. How It Works

A Bloom filter is a bit array of m bits, initially all 0, with k independent hash functions.

### Idiomatic Go Implementation

```go
package main

import (
	"fmt"
	"hash/fnv"
)

type BloomFilter struct {
	bits []uint64
	m    uint32
	k    int
}

func NewBloomFilter(m uint32, k int) *BloomFilter {
	// Allocate bits/64 elements
	return &BloomFilter{
		bits: make([]uint64, (m+63)/64),
		m:    m,
		k:    k,
	}
}

func (bf *BloomFilter) hash(item []byte, i int) uint32 {
	h := fnv.New32a()
	h.Write(item)
	// Mix in the hash index i
	h.Write([]byte{byte(i)})
	return h.Sum32()
}

func (bf *BloomFilter) Add(item []byte) {
	for i := 0; i < bf.k; i++ {
		idx := bf.hash(item, i) % bf.m
		bf.bits[idx/64] |= (1 << (idx % 64))
	}
}

func (bf *BloomFilter) Contains(item []byte) bool {
	for i := 0; i < bf.k; i++ {
		idx := bf.hash(item, i) % bf.m
		if (bf.bits[idx/64] & (1 << (idx % 64))) == 0 {
			return false // Definitely not present
		}
	}
	return true // Maybe present
}

func main() {
	bf := NewBloomFilter(1000, 3)
	bf.Add([]byte("golang"))
	fmt.Println(bf.Contains([]byte("golang"))) // true
	fmt.Println(bf.Contains([]byte("rust")))   // false (probably)
}
```

## 47.3. Optimal Parameters

For desired false positive rate ε and n expected elements:

| Parameter | Formula | Typical Value |
|-----------|---------|---------------|
| m (bits) | -n ln(ε) / (ln 2)² | ~10n for ε=1% |
| k (hashes) | m/n · ln 2 | ~7 for ε=1% |

### False Positive Rate

p ≈ (1 - e^(-kn/m))^k

## 47.4. Variants

| Variant | Feature | Use Case |
|---------|---------|----------|
| **Counting Bloom filter** | Supports deletion | Network caching |
| **Cuckoo filter** | Better cache behavior | High-performance systems |
| **Scalable Bloom filter** | Grows dynamically | Unknown set sizes |

## 47.5. Decision Matrix

| Use Bloom Filters When... | Use Hash Sets When... |
|---------------------------|-----------------------|
| Memory is severely constrained | Memory is abundant |
| False positives are acceptable | False positives are strictly unacceptable |
| No deletions are needed | Deletions are continually required |

### Edge Cases & Pitfalls

- **Hash quality:** Poor hash functions dramatically increase collision rates.
- **Saturation:** When perfectly full, every single query returns "maybe."
- **No deletion:** Standard Bloom filters cannot effectively remove items.
- **Counting overflow:** Counting Bloom filters can violently overflow with too many insertions.

## 47.6. Quick Reference

| Setting | Bits/Element | Hashes | False Positive |
|---------|--------------|--------|----------------|
| Conservative | 16 | 11 | 0.01% |
| Balanced | 10 | 7 | 1% |
| Aggressive | 6 | 4 | 5% |

| Go stdlib | Usage |
|-----------|-------|
| `github.com/bits-and-blooms` | Production-grade Bloom filters |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 47:</strong> Bloom filters sacrifice absolute certainty for massive space savings. They answer membership queries with no false negatives and tunable <abbr title="An error where a test incorrectly indicates the presence of a condition when it is not present.">false positives</abbr> — ideal when memory is scarce and a small error rate is acceptable. Every large-scale system from databases to CDNs uses Bloom filters to avoid expensive lookups.
{{% /alert %}}

## See Also

- [Chapter 7: Hashing and Hash Tables](/docs/Part-II/Chapter-7/)
- [Chapter 45: B-Trees](/docs/Part-IX/Chapter-45/)
- [Chapter 48: LRU Cache](/docs/Part-IX/Chapter-48/)
