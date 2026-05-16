---
weight: 60600
title: "Chapter 27: Probabilistic and Randomized Algorithms"
description: "Probabilistic and Randomized Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>A good algorithm is a beautiful thing, but its beauty is often in its simplicity. The most complex algorithms are those that use randomization effectively.</em>" : Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 28 covers probabilistic algorithms: Las Vegas, Monte Carlo, randomized quicksort, skip lists, and primality testing.
{{% /alert %}}

## 28.1. Randomized QuickSort

**Definition:** QuickSort using random pivot selection. Prevents $O(n^2)$ worst-case on sorted inputs.

**Background & Philosophy:**
Randomness trades absolute certainty for high probability. Deterministic algorithms fail on specific inputs. Las Vegas method breaks deterministic worst-cases. $O(n \log n)$ execution is expected regardless of input.

**Use Cases:**
Default sorting in modern libraries. Prevents CPU burn attacks from malicious sorted data.

**Memory Mechanics:**
Randomization uses Pseudo-Random Number Generators (PRNGs). Shared PRNG state causes lock contention in concurrent code. Go goroutines should use `rand.New(rand.NewSource())` per thread. Isolates RAM state. Avoids memory stalling.

### Operations & Complexity

| Case | Deterministic QS | Randomized QS |
|-------|-----------------|---------------|
| Best | $O(n \log n)$ | $O(n \log n)$ |
| Average | $O(n \log n)$ | $O(n \log n)$ expected |
| Worst | $O(n^2)$ | $O(n^2)$ with prob $1/n!$ |
| Space | $O(\log n)$ | $O(\log n)$ expected |

### Pseudocode

```text
RandomizedQuickSort(A):
    if length(A) <= 1: return
    pivotIdx = random index in A
    SWAP A[pivotIdx] with A[last]
    pivot = A[last]
    i = 0
    for j from 0 to length(A)-2:
        if A[j] < pivot:
            SWAP A[i] with A[j]
            i += 1
    SWAP A[i] with A[last]
    RandomizedQuickSort(A[0:i])
    RandomizedQuickSort(A[i+1:])
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math/rand"
)

func randomizedQuickSort(arr []int) {
    var sort func([]int)
    sort = func(a []int) {
        if len(a) <= 1 {
            return
        }
        pivotIdx := rand.Intn(len(a))
        a[pivotIdx], a[len(a)-1] = a[len(a)-1], a[pivotIdx]
        pivot := a[len(a)-1]
        i := 0
        for j := 0; j < len(a)-1; j++ {
            if a[j] < pivot {
                a[i], a[j] = a[j], a[i]
                i++
            }
        }
        a[i], a[len(a)-1] = a[len(a)-1], a[i]
        sort(a[:i])
        sort(a[i+1:])
    }
    sort(arr)
}

func main() {
    arr := []int{3, 6, 8, 10, 1, 2, 1}
    randomizedQuickSort(arr)
    fmt.Println("Sorted:", arr)
}
```

{{% alert icon="📌" context="warning" %}}
Randomized QuickSort gives $O(n \log n)$ expected time. Go stdlib `sort.Ints` uses introsort: a hybrid of quicksort, heapsort, and insertion sort. Introsort is preferred for production.
{{% /alert %}}

### Decision Matrix

| Use Randomized QS When... | Avoid If... |
|------------------------------|------------------|
| Scratch implementation required | Production environment: use `sort` stdlib |
| Expected performance is sufficient | Legal mandates require deterministic guarantees |

### Edge Cases & Pitfalls

- **Equal elements:** Lomuto partition fails. Use 3-way partition (Dutch National Flag).
- **Recursion depth:** Large $n$ causes stack overflow. Use introsort or iterative methods.

## 28.2. <abbr title="A probabilistic data structure that allows fast search within an ordered sequence.">Skip List</abbr>

**Definition:** Probabilistic data structure. Simulates balanced tree using layered linked lists. Nodes have randomized heights.

**Background & Philosophy:**
Trees use rotations for balance. Skip lists use probability. Elements promoted to higher layers randomly. Establishes express lanes for search.

**Use Cases:**
Concurrent programming. No structural rotations required. Used in Redis sorted sets.

**Memory Mechanics:**
Nodes store array of `next` pointers. Go uses `make([]*SkipNode, lvl)`. Higher memory overhead than binary trees. Causes heap fragmentation. Lack of rebalancing offset by simplified pointers.

### Operations & Complexity

| Operation | Expected | Worst | Description |
|---------|----------|-------|------------|
| Search | $O(\log n)$ | $O(n)$ | High probability success |
| Insert | $O(\log n)$ | $O(n)$ | Depends on randomized height |
| Delete | $O(\log n)$ | $O(n)$ | Updates linking pointers |
| Space | $O(n)$ | $O(n \log n)$ | Expected memory layout |

### Pseudocode

```text
SkipListSearch(head, key):
    node = head
    for level from maxLevel down to 0:
        while node.next[level] exists and node.next[level].key < key:
            node = node.next[level]
    node = node.next[0]
    if node exists and node.key == key:
        return node.value
    return not found

SkipListInsert(head, key, value):
    update = array of nodes at each level
    node = head
    for level from maxLevel down to 0:
        while node.next[level] exists and node.next[level].key < key:
            node = node.next[level]
        update[level] = node
    node = node.next[0]
    if node exists and node.key == key:
        node.value = value
        return
    newLevel = random level with probability p
    newNode = new node with key, value, and next array of size newLevel
    for level from 0 to newLevel-1:
        newNode.next[level] = update[level].next[level]
        update[level].next[level] = newNode
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math/rand"
)

const maxLevel = 16
const p = 0.5

type SkipNode struct {
    key   int
    value string
    next  []*SkipNode
}

type SkipList struct {
    head  *SkipNode
    level int
}

func NewSkipList() *SkipList {
    return &SkipList{
        head:  &SkipNode{next: make([]*SkipNode, maxLevel)},
        level: 1,
    }
}

func (sl *SkipList) randomLevel() int {
    lvl := 1
    for rand.Float64() < p && lvl < maxLevel {
        lvl++
    }
    return lvl
}

func (sl *SkipList) Search(key int) (string, bool) {
    curr := sl.head
    for i := sl.level - 1; i >= 0; i-- {
        for curr.next[i] != nil && curr.next[i].key < key {
            curr = curr.next[i]
        }
    }
    curr = curr.next[0]
    if curr != nil && curr.key == key {
        return curr.value, true
    }
    return "", false
}

func (sl *SkipList) Insert(key int, value string) {
    update := make([]*SkipNode, maxLevel)
    curr := sl.head
    for i := sl.level - 1; i >= 0; i-- {
        for curr.next[i] != nil && curr.next[i].key < key {
            curr = curr.next[i]
        }
        update[i] = curr
    }
    curr = curr.next[0]
    if curr != nil && curr.key == key {
        curr.value = value
        return
    }

    lvl := sl.randomLevel()
    if lvl > sl.level {
        for i := sl.level; i < lvl; i++ {
            update[i] = sl.head
        }
        sl.level = lvl
    }
    node := &SkipNode{key: key, value: value, next: make([]*SkipNode, lvl)}
    for i := 0; i < lvl; i++ {
        node.next[i] = update[i].next[i]
        update[i].next[i] = node
    }
}

func main() {
    sl := NewSkipList()
    for i := 0; i < 10; i++ {
        sl.Insert(i, fmt.Sprintf("val%d", i))
    }
    if v, ok := sl.Search(5); ok {
        fmt.Println("Found:", v)
    }
}
```

{{% alert icon="📌" context="warning" %}}
Skip list space is $O(n)$ expected. Average height is 2 for $p=0.5$. Large $p$ consumes memory. Small $p$ slows search.
{{% /alert %}}

### Decision Matrix

| Use <abbr title="A probabilistic data structure that allows fast search within an ordered sequence.">Skip List</abbr> When... | Avoid If... |
|--------------------------|------------------|
| Lock-free concurrency required | Memory overhead is a bottleneck |
| Simple implementation needed | High volume of range queries expected |

### Edge Cases & Pitfalls

- **Weak RNG:** Probability logic fails without good randomness. Use robust seeds.
- **Max Level:** $p=0.5$ and maxLevel=16 supports $n \approx 65536$. Increase limit for larger data.

## 28.3. Miller-Rabin Primality Test

**Definition:** Monte Carlo algorithm. Tests primality. Error probability $\le 4^{-k}$ after $k$ rounds.

**Background & Philosophy:**
True primality testing for large numbers is slow. Miller-Rabin uses random witnesses. Witness found: 100% composite. No witness found: probably prime. Mathematical certainty increases with trials.

**Use Cases:**
Generating RSA keys. Diffie-Hellman key generation.

**Memory Mechanics:**
Modular exponentiation required. Large numbers exceed 64-bit registers. Go uses `math/big`. Allocates underlying Word slices in heap. CPU compute cost dominates GC churn.

### Operations & Complexity

| Parameter | Time | Error Probability |
|-----------|------|-------------------|
| $k$ rounds | $O(k \log^3 n)$ | $\le 4^{-k}$ |
| $k=5$ | $O(\log^3 n)$ | $< 0.1\%$ |
| $k=20$ | $O(\log^3 n)$ | $< 10^{-12}$ |
| $k=40$ | $O(\log^3 n)$ | $< 10^{-24}$ |

### Idiomatic Go Implementation

Use `math/big.Int.ProbablePrime()` for production.

### Decision Matrix

| Use Miller-Rabin When... | Avoid If... |
|-----------------------------|------------------|
| Testing large primes | Deterministic guarantee required: use AKS (slow) |
| Cryptographic key generation | $n < 2^{64}$: use optimized deterministic test |

### Edge Cases & Pitfalls

- **Carmichael numbers:** Miller-Rabin identifies these correctly.
- **Modular overflow:** Use `math/big.Int.ModMul` for $n > 2^{32}$.
- **Deterministic variant:** Testing against base {2, 3, 5, 7, 11, 13, 17} is deterministic for $n < 2^{64}$.

## 28.4. Reservoir Sampling

**Definition:** Selects $k$ random items from infinite stream. No total size knowledge required.

**Background & Philosophy:**
Stream intelligence. Large data cannot fit in memory. Processes items once. Maintains reservoir of size $k$. Probability of replacement ensures fairness.

**Use Cases:**
Analytics on live streams (Kafka). Sampling massive logs.

**Memory Mechanics:**
Strictly $O(k)$ memory. Single slice allocated in RAM. Sequential data read. Minimal RAM usage. Zero cache misses during ingestion.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| Reservoir $k$ | $O(1)$ per item | $O(k)$ | Infinite stream handling |
| Weighted | $O(\log k)$ per item | $O(k)$ | Priority-based sampling |

Guarantees $k/n$ selection probability for all items. Weighted streams use exponential random variates.

### Decision Matrix

| Use Reservoir When... | Avoid If... |
|--------------------------|------------------|
| Stream exceeds memory | $N$ is known: use random shuffle |
| Real-time sampling needed | Complex stratified sampling required |

### Edge Cases & Pitfalls

- **$k > n$:** Handle streams shorter than $k$.
- **Biased RNG:** Use `crypto/rand` for high-stakes randomness.

### Anti-Patterns

- **Using `math/rand` for security:** Predictable. Use `crypto/rand` for tokens/crypto.
- **Static seeds:** Identical results hide bugs. Use dynamic source.
- **Misplaced trust:** 99% correctness is not 100%. Avoid in financial settlements.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Randomized QuickSort | Las Vegas | $O(n \log n)$ | $O(\log n)$ | General Sorting |
| Skip List | Las Vegas | $O(\log n)$ | $O(n)$ | Ordered data set |
| Miller-Rabin | Monte Carlo | $O(k \log^3 n)$ | $O(1)$ | Primality testing |
| Reservoir Sampling | . | $O(n)$ | $O(k)$ | Infinite Stream sampling |
| Randomized Select | Las Vegas | $O(n)$ | $O(1)$ | k-th order statistic |
| Hash Table | Las Vegas | $O(1)$ avg | $O(n)$ | High-speed Dictionary |
| Bloom Filter | Monte Carlo | $O(k)$ | $O(m)$ | Rapid Membership test |
| Treap | Las Vegas | $O(\log n)$ | $O(n)$ | Fused BST + heap |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 27:</strong> Probabilistic algorithms use randomness for efficiency. Randomized quicksort avoids $O(n^2)$. Skip lists provide $O(\log n)$ search. Miller-Rabin tests large primes. Reservoir sampling handles infinite streams.
{{% /alert %}}

## See Also

- [Chapter 25: Backtracking](/docs/part-vi/chapter-25/)
- [Chapter 26: Advanced Recursive Algorithms](/docs/part-vi/chapter-26/)
- [Chapter 45: Skip Lists](/docs/part-ix/chapter-45/)
