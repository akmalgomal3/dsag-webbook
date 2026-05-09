---
weight: 90300
title: "Chapter 47 - Bloom Filters"
description: "Bloom Filters"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A Bloom filter is a data structure that tells you an element is definitely not in a set, or maybe in a set.</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 47 explores Bloom filters — a space-efficient probabilistic data structure for set membership testing with no false negatives.
{{% /alert %}}

## 47.1. The Membership Problem

**Definition:** A <abbr title="A space-efficient probabilistic data structure that is used to test whether an element is a member of a set, with possible false positives but no false negatives.">Bloom filter</abbr> answers: "Is element X in set S?" with:
- **"No"** → Definitely not in set (100% accurate)
- **"Maybe"** → Might be in set (possible false positive)

### Space Efficiency

| Structure | Bits per Element | False Positive Rate |
|-----------|-----------------|---------------------|
| Hash table | 64+ | 0% |
| Bloom filter | 10 | 1% |

Storing 1 billion URLs: hash table ≈ 8 GB, Bloom filter ≈ 1 GB.

## 47.2. How It Works

A Bloom filter is a bit array of m bits, initially all 0, with k independent hash functions.

### Insertion

```go
func (bf *BloomFilter) Add(item []byte) {
    for i := 0; i < bf.k; i++ {
        idx := bf.hash(item, i) % bf.m
        bf.bits[idx] = 1
    }
}

func (bf *BloomFilter) Contains(item []byte) bool {
    for i := 0; i < bf.k; i++ {
        idx := bf.hash(item, i) % bf.m
        if bf.bits[idx] == 0 {
            return false // Definitely not present
        }
    }
    return true // Maybe present
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
| Memory is constrained | Memory is abundant |
| False positives acceptable | False positives unacceptable |
| No deletions needed | Deletions required |

### Edge Cases & Pitfalls

- **Hash quality:** Poor hash functions increase collision rates.
- **Saturation:** When full, every query returns "maybe."
- **No deletion:** Standard Bloom filters cannot remove items.
- **Counting overflow:** Counting Bloom filters can overflow with many insertions.

## 47.6. Quick Reference

| Setting | Bits/Element | Hashes | False Positive |
|---------|--------------|--------|----------------|
| Conservative | 16 | 11 | 0.01% |
| Balanced | 10 | 7 | 1% |
| Aggressive | 6 | 4 | 5% |

| Go stdlib | Usage |
|-----------|-------|
| `github.com/bits-and-blooms` | Production Bloom filters |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 47:</strong> Bloom filters sacrifice absolute certainty for massive space savings. They answer membership queries with no false negatives and tunable false positives — ideal when memory is scarce and a small error rate is acceptable. Every large-scale system from databases to CDNs uses Bloom filters to avoid expensive lookups.
{{% /alert %}}
