---
weight: 60600
title: "Chapter 27: Probabilistic and Randomized Algorithms"
description: "Probabilistic and Randomized Algorithms"
icon: "article"
date: "2024-08-24T23:42:52+07:00"
lastmod: "2024-08-24T23:42:52+07:00"
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

**Definition:** QuickSort utilizing a randomly selected pivot avoids the severe <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> <code>O(n^2)</code> on already sorted inputs.

**Background & Philosophy:**
The philosophy is trading absolute certainty for overwhelming probability. Deterministic algorithms often hit pathological worst-cases crafted by malicious inputs or unlucky sequential data. Injecting randomness (Las Vegas method) breaks these deterministic worst-cases mathematically, ensuring that <code>O(n log n)</code> execution is highly expected regardless of input distribution.

**Use Cases:**
Randomized QuickSort is the underlying default sorting strategy in modern standard libraries, used constantly when data comes from untrusted networks where users might submit intentionally sorted arrays to DDOS the server via worst-case CPU burn.

**Memory Mechanics:**
Randomization heavily relies on Pseudo-Random Number Generators (PRNGs). Fetching from a PRNG requires querying a shared internal state. If multiple <abbr title="A lightweight concurrent execution thread managed by the Go runtime.">goroutines</abbr> request random numbers from the global `rand.Seed`, it creates massive <abbr title="A situation where multiple threads attempt to modify the same memory address simultaneously.">lock contention</abbr> at the memory level. High-performance randomized algorithms allocate a distinct `rand.New(rand.NewSource())` per <abbr title="A lightweight concurrent execution thread managed by the Go runtime">goroutine</abbr> to maintain isolated <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> states, avoiding cross-thread memory stalling.

### Operations & Complexity

| Case | Deterministic QS | Randomized QS |
|-------|-----------------|---------------|
| Best | <code>O(n log n)</code> | <code>O(n log n)</code> |
| Average | <code>O(n log n)</code> | <code>O(n log n)</code> expected |
| Worst | <code>O(n^2)</code> | <code>O(n^2)</code> with prob 1/n! |
| Space | <code>O(log n)</code> | <code>O(log n)</code> expected |

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
Randomized QuickSort has an expected time of <code>O(n log n)</code> across all input varieties. For heavy production systems, Go's stdlib `sort.Ints` natively utilizes introsort (a robust hybrid of quicksort + heapsort + <abbr title="A sorting algorithm that builds the final sorted array one item at a time.">insertion sort</abbr>) which is already hyper-optimized.
{{% /alert %}}

### Decision Matrix

| Use Randomized QS When... | Avoid If... |
|------------------------------|------------------|
| Implementing a robust sort from absolute scratch | Operating in a production environment (always use the `sort` stdlib) |
| A solid expected guarantee is required | A strict, unflinching deterministic guarantee is legally mandatory |

### Edge Cases & Pitfalls

- **All equal elements:** The basic Lomuto partition degrades heavily. Utilize a 3-way partition (the Dutch national flag algorithm) instead.
- **<abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> <abbr title="The length of the path from the root to a node.">depth</abbr>:** For n > 10⁶, purely recursive quicksort runs the immense risk of a <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>. Switch to introsort or the stdlib.

## 28.2. <abbr title="A probabilistic data structure that allows fast search within an ordered sequence.">Skip List</abbr>

**Definition:** A <abbr title="A probabilistic data structure that allows fast search within an ordered sequence.">Skip List</abbr> acts as a probabilistic data structure that masterfully simulates a balanced <abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> utilizing multiple layered linked lists featuring randomized heights.

**Background & Philosophy:**
Balancing an AVL or Red-Black tree involves complex pointer manipulation and structural rotations. Skip lists take a different approach: instead of mathematically guaranteeing balance via rigid rules, they achieve statistical balance via probability. By randomly "promoting" elements to higher layers, they establish express lanes for searching.

**Use Cases:**
Highly effective in concurrent programming. Because inserting an element doesn't require massive structural rotations, it requires fewer memory locks. Skip lists famously power the backend sorted sets in Redis.

**Memory Mechanics:**
Skip lists require an array of `next` pointers per node depending on their randomized "height". In Go, `make([]*SkipNode, lvl)` dynamically allocates this array. This makes skip lists heavier in memory usage than standard binary trees and introduces unpredictable memory fragmentation across the <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>. However, the absence of complex <code>O(log n)</code> rebalancing operations offsets the cache misses encountered during forward traversal.

### Operations & Complexity

| Operation | Expected | Worst | Description |
|---------|----------|-------|------------|
| Search | <code>O(log n)</code> | <code>O(n)</code> | Solved with remarkably high probability |
| Insert | <code>O(log n)</code> | <code>O(n)</code> | Relies upon randomized <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> <abbr title="The length of the longest path from a node to a leaf.">height</abbr> |
| Delete | <code>O(log n)</code> | <code>O(n)</code> | Carefully updates linking pointers |
| Space | <code>O(n)</code> | <code>O(n log n)</code> | Expected memory layout |

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
A <abbr title="A probabilistic data structure that allows fast search within an ordered sequence.">Skip list</abbr> demands an expected space of <code>O(n)</code> primarily because E[<abbr title="The set of all nodes at a given depth.">level</abbr>] = 1/(1-p) = 2 for p=0.5. Never use a p <abbr title="The data associated with a key in a key-value pair.">value</abbr> that is overwhelmingly large (it brutally consumes memory) or exceedingly small (forces low heights, making searches agonizingly slow).
{{% /alert %}}

### Decision Matrix

| Use <abbr title="A probabilistic data structure that allows fast search within an ordered sequence.">Skip List</abbr> When... | Avoid If... |
|--------------------------|------------------|
| Need heavy concurrent access (via a lock-free variant) | Raw memory overhead represents a critical bottleneck |
| Seeking an implementation fundamentally simpler than AVL/RB trees | Executing a massive volume of range queries |

### Edge Cases & Pitfalls

- **Deterministic random:** Skip lists fundamentally require extremely good randomness. Never use a constant seed in a production environment.
- **Max <abbr title="The set of all nodes at a given depth.">level</abbr>:** p=0.5 coupled with maxLevel=16 is perfectly sufficient for n=2^16=65536. Vigorously adjust this limit for dramatically larger n values.

## 28.3. Miller-Rabin Primality Test

**Definition:** Miller-Rabin stands as a Monte Carlo algorithm utilized for fierce primality testing boasting an error probability firmly ≤ 4^(-k) across k continuous rounds.

**Background & Philosophy:**
The philosophy is "guilt by association." Since testing true primality for massive 2048-bit numbers takes astronomically long deterministically, Miller-Rabin uses Monte Carlo rules: it randomly selects "witnesses" to testify if a number is composite. If it finds a witness, it is 100% sure the number is not prime. If it fails to find one after `k` random trials, it declares the number "probably prime" with a mathematical certainty near absolute.

**Use Cases:**
Generating massive RSA or Diffie-Hellman encryption keys safely.

**Memory Mechanics:**
Miller-Rabin uses modular exponentiation. Since 2048-bit numbers greatly exceed the 64-bit size of standard CPU registers, Go uses the `math/big` package. `big.Int` allocates arrays of underlying `Word` slices in <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap memory</abbr>. These allocations create <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">Garbage Collection</abbr> churn. However, because the operations are mathematically heavy, CPU compute vastly dominates memory IO costs.

### Operations & Complexity

| Parameter | Time | Error Probability |
|-----------|------|-------------------|
| k rounds | <code>O(k log³ n)</code> | ≤ 4^(-k) |
| k=5 | <code>O(log³ n)</code> | < 0.1% |
| k=20 | <code>O(log³ n)</code> | < 10^(-12) |
| k=40 | <code>O(log³ n)</code> | < 10^(-24) |

### Idiomatic Go Implementation

Miller-Rabin (probabilistic primality test) is available natively in `crypto/rand`. Use `big.NewInt()` and `big.Int.ProbablePrime()` for production.

### Decision Matrix

| Use Miller-Rabin When... | Avoid If... |
|-----------------------------|------------------|
| Conducting large number primality checks | A strict deterministic guarantee is fully mandatory (employ AKS, though it runs agonizingly slow) |
| Performing cryptographic key generation | n < 2^64 (run a heavily optimized deterministic test instead) |

### Edge Cases & Pitfalls

- **Carmichael numbers:** Miller-Rabin successfully identifies these, unlike a naive Fermat test.
- **Modular multiplication overflow:** Utilize `math/big.Int.ModMul` vigorously for any n > 2^32.
- **Deterministic variant:** For any n < 2^64, testing strictly against the base set {2, 3, 5, 7, 11, 13, 17} is provably deterministic.

## 28.4. Reservoir Sampling

**Definition:** Reservoir sampling selects k items uniformly randomly from an infinite stream without requiring prior knowledge of the total volume.

**Background & Philosophy:**
The philosophy is stream intelligence. When data is infinite or too large to fit in memory (like all logs generated by a server today), you cannot store it to randomly select `k` items later. Reservoir sampling processes items exactly once, maintaining a "reservoir" of size `k`, probabilistically replacing items as new ones stream in, ensuring fair representation continuously.

**Use Cases:**
Providing live, random analytics samples from continuous Kafka streams or massive network logs.

**Memory Mechanics:**
It requires strictly <code>O(k)</code> memory. A single <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> slice of size `k` is allocated in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. As new data streams in, it reads one item at a time, making it incredibly hardware friendly since it uses minimal <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> and causes virtually zero <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr> during sequential data ingestion.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| Reservoir k | <code>O(k)</code> per item | <code>O(k)</code> | Handles a stream of completely unknown size |
| Weighted | <code>O(k log k)</code> per item | <code>O(k)</code> | Executes priority-based sampling |

Reservoir sampling guarantees that every single item possesses an exact mathematical probability of k/n of being selected. For heavily weighted streams, implement exponential random variates.

### Decision Matrix

| Use Reservoir When... | Avoid If... |
|--------------------------|------------------|
| The stream is too massive to fit entirely in memory | Total N is strictly known upfront (use a standard random shuffle) |
| Conducting real-time analytical sampling | Complex stratified sampling is heavily required |

### Edge Cases & Pitfalls

- **k > n:** Always reliably handle the scenario where the raw stream is ultimately shorter than k.
- **Biased RNG:** Strictly utilize `crypto/rand` if cryptographic-level randomness is vitally critical.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Randomized QuickSort | Las Vegas | <code>O(n log n)</code> | <code>O(log n)</code> | General <abbr title="The process of arranging elements in a specific order.">Sorting</abbr> |
| <abbr title="A probabilistic data structure that allows fast search within an ordered sequence.">Skip List</abbr> | Las Vegas | <code>O(log n)</code> | <code>O(n)</code> | Ordered data set |
| Miller-Rabin | Monte Carlo | <code>O(k log^3 n)</code> | <code>O(1)</code> | Advanced Primality testing |
| Reservoir Sampling | . | <code>O(n)</code> | <code>O(k)</code> | Infinite Stream sampling |
| Randomized Select | Las Vegas | <code>O(n)</code> | <code>O(1)</code> | Isolating the k-th order statistic |
| <abbr title="A data structure that implements an associative array using a hash function.">Hash Table</abbr> | Las Vegas | <code>O(1)</code> avg | <code>O(n)</code> | High-speed Dictionary |
| Bloom Filter | Monte Carlo | <code>O(k)</code> | <code>O(m)</code> | Rapid Membership test |
| Treap | Las Vegas | <code>O(log n)</code> | <code>O(n)</code> | Fused BST + <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 26:</strong> This chapter dissects probabilistic algorithms: randomized quicksort yielding <code>O(n log n)</code> expected, skip lists hitting <code>O(log n)</code> expected, the Miller-Rabin primality test (a Monte Carlo approach), and reservoir sampling for boundless streams. Leverage skip lists for creating a straightforward ordered set, Miller-Rabin for evaluating large primes, and reservoir sampling to manage streaming data.
{{% /alert %}}

## See Also

- [Chapter 25: <abbr title="Building candidates incrementally and abandoning dead ends">Backtracking</abbr>](/docs/Part-VI/Chapter-25/)
- [Chapter 26: Advanced Recursive Algorithms](/docs/Part-VI/Chapter-26/)
- [Chapter 45: Skip Lists](/docs/Part-IX/Chapter-45/)
