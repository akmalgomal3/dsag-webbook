---
weight: 90300
title: "Chapter 46: Bloom Filters"
description: "Bloom Filters"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A Bloom filter is a data structure that tells you an element is definitely not in a set, or maybe in a set.</em>"</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Bloom filters are space-efficient probabilistic structures. Set membership tests provide zero false negatives.
{{% /alert %}}

## 46.1. Purpose

**Definition:** A <abbr title="A space-efficient probabilistic data structure that is used to test whether an element is a member of a set, with possible false positives but no false negatives.">Bloom filter</abbr> answers: "Is element X in set S?"
- **"No"** : Definitely not in set (100% accurate).
- **"Maybe"** : Might be in set (possible <abbr title="An error where a test incorrectly indicates the presence of a condition when it is not present.">false positive</abbr>).

**Probabilistic Logic:**
Filter trades certainty for compression. Acceptable inaccuracy enables extreme data density. Guarantees zero false negatives.

**Use Cases:**
Malicious URL checks. CDN cache protection. Database disk-read optimization (Cassandra, RocksDB).

**Memory Mechanics:**
Relies on massive bit array (`[]uint64`). Item hashed k times. Hashes flip specific bits. Random bit jumps trigger <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>. RAM access still faster than disk seeks.

### Space Efficiency Comparison

| Structure | Bits per Element | False Positive Rate |
|-----------|-----------------|---------------------|
| Hash table | 64+ | 0% |
| Bloom filter | 10 | 1% |

1 billion URLs: hash table ≈ 8 GB. Bloom filter ≈ 1 GB.

## 46.2. Mechanics

Bit array of m bits. Initially 0. k independent hash functions.

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

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
	return &BloomFilter{
		bits: make([]uint64, (m+63)/64),
		m:    m,
		k:    k,
	}
}

func (bf *BloomFilter) hash(item []byte, i int) uint32 {
	h := fnv.New32a()
	h.Write(item)
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

## 46.3. Optimal Parameters

 ε = target false positive rate. n = expected elements.

| Parameter | Formula | Typical Value |
|-----------|---------|---------------|
| m (bits) | -n ln(ε) / (ln 2)² | ~10n for ε=1% |
| k (hashes) | m/n · ln 2 | ~7 for ε=1% |

### Error Rate Calculation

p ≈ (1 - e^(-kn/m))^k

## 46.4. Variants

| Variant | Feature | Use Case |
|---------|---------|----------|
| **Counting Bloom** | Supports deletion. | Network caching. |
| **Cuckoo filter** | Better cache behavior. | High-performance. |
| **Scalable Bloom** | Grows dynamically. | Unknown set sizes. |

## 46.5. Decision Matrix

| Use Bloom Filters When... | Use Hash Sets When... |
|---------------------------|-----------------------|
| Memory scarce | Memory abundant |
| False positives acceptable | Errors unacceptable |
| Deletions not needed | Deletions frequent |

### Edge Cases & Pitfalls

- **Hash Quality:** Poor functions increase collision rates.
- **Saturation:** Full filters return "maybe" for every query.
- **Deletion:** Standard filters cannot remove items. Bits map to multiple keys.
- **Overflow:** Counting filters fail if buckets exceed counter size.

### Anti-Patterns

- **Zero-Error Mandate:** Do not use for security or finance membership checks.
- **Overstuffing:** Error rates grow exponentially as load factor exceeds design.
- **Deleting Bits:** Clearing bits in standard filters creates false negatives.
- **Correlated Hashes:** Non-independent hash functions reduce filter effectiveness.

## 46.6. Quick Reference

| Setting | Bits/Element | Hashes | False Positive |
|---------|--------------|--------|----------------|
| Conservative | 16 | 11 | 0.01% |
| Balanced | 10 | 7 | 1% |
| Aggressive | 6 | 4 | 5% |

| Go stdlib | Usage |
|-----------|-------|
| `github.com/bits-and-blooms` | Production implementation. |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
Bloom filters save space by accepting tunable error. Zero false negatives. Ideal for high-scale avoidance of expensive disk lookups.
{{% /alert %}}

## See Also

- [Chapter 7: Hashing and Hash Tables](/docs/part-ii/chapter-7/)
- [Chapter 44: B-Trees](/docs/part-ix/chapter-44/)
- [Chapter 47: LRU Cache](/docs/part-ix/chapter-47/)
