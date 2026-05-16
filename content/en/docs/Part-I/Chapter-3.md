---
weight: 10300
title: "Chapter 3: Introduction to Data Structures and Algorithms in Go"
description: "Introduction to Data Structures and Algorithms in Go"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Programs must be written for people to read, and only incidentally for machines to execute.</em>" : Harold Abelson</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 3 covers Go as a tool for algorithms. Topics: memory management, built-in collections, developer environment setup.
{{% /alert %}}

## 3.1. Go for Data Structures and Algorithms

**Definition:** Go provides memory safety, C-like speed, raw concurrency, strong tooling.

**Background & Philosophy:**
Built at Google for scale. Prioritizes simplicity over cleverness. Drops inheritance and pointer arithmetic. Focuses on composition, interfaces, goroutines.

**Use Cases:**
Microservices. API gateways. CLIs. Distributed infrastructure (Kubernetes).

**Memory Mechanics:**
Go uses concurrent Garbage Collector (GC). Tracks object references. Compiler escape analysis decides allocation location. Stack allocation bypasses GC. Heap allocation triggers GC. Keeping data on stack reduces GC pressure. Improves cache locality.

### Operations & Complexity

| Feature | Advantage | Trade-off |
|-------|------------|-----------|
| Garbage Collection | Automatic memory safety | Pause time (<1ms) |
| Slice | Amortized `O(1)` append | Triggers reallocation |
| Map | `O(1)` avg lookup | Unordered, non-concurrent |
| Goroutine | Cheap concurrency | Scheduling overhead |

### Edge Cases & Pitfalls
- **Array vs slice:** Arrays copy by value. Slices copy by reference (header only).
- **Nil slice:** Nil slice safe for `len()`, `cap()`, `append()`.
- **Map race:** Concurrent map access panics. Use `sync.Mutex`.

## 3.2. Essential Data Structures

**Definition:** Go built-ins: arrays, slices, maps. Custom structures: linked lists, trees, graphs.

**Background & Philosophy:**
Standard library provides minimal primitives. Avoids bloat. Developers build domain-specific structures using structs and pointers.

**Use Cases:**
Slices for lists. Maps for caches. Custom trees for parsers. Graphs for networks.

**Memory Mechanics:**
Slice is 24-byte struct (pointer, length, capacity). Passing slice copies 24 bytes. Fast operation. Sharing backing array causes side effects. Modifying one slice affects another.

### Operations & Complexity

| Structure | Go Type | Access | Insert | Search |
|----------|---------|--------|--------|--------|
| Array | `[N]T` | `O(1)` | N/A | `O(n)` |
| Slice | `[]T` | `O(1)` | `O(n)` avg | `O(n)` |
| Linked List | `list.List` | `O(n)` | `O(1)` | `O(n)` |
| Map | `map[K]V` | `O(1)` avg | `O(1)` avg | `O(1)` avg |
| Binary Tree | `struct` | `O(log n)` | `O(log n)` | `O(log n)` |

### Idiomatic Go Implementation

```go
package main

import (
    "container/list"
    "fmt"
)

func traverseList(lst *list.List) {
    for e := lst.Front(); e != nil; e = e.Next() {
        fmt.Println(e.Value)
    }
}

func main() {
    lst := list.New()
    lst.PushBack(1)
    lst.PushBack(2)
    traverseList(lst)
}
```

### Edge Cases & Pitfalls
- **Slice capacity:** Exceeding capacity copies array to heap.
- **Map keys:** Keys must be comparable. Slices and maps fail.
- **List iteration:** Mutating list during iteration breaks pointers.

## 3.3. Algorithmic Paradigms

**Definition:** Paradigms classify approaches: divide and conquer, dynamic programming, greedy, backtracking.

**Background & Philosophy:**
Categorize before coding. Maps complex problems to known archetypes. Reduces custom logic.

**Use Cases:**
DP for DNA alignment. Greedy for network routing. Divide and conquer for distributed MapReduce.

**Memory Mechanics:**
Paradigms rely on call stack. Recursion adds stack frames. Go goroutine stack starts at 2KB. Grows dynamically. Extreme recursion causes Out of Memory (OOM). DP trades space for time. Caches results in heap matrix (memoization).

### Operations & Complexity

| Paradigm | Characteristic | Example | Complexity |
|-----------|---------------|--------|--------------|
| Divide and Conquer | Split, solve, merge | Merge sort | `O(n log n)` |
| Dynamic Programming | Memoization | Knapsack | `O(nW)` |
| Greedy | Local optimal | Prim's MST | `O(E log V)` |
| Backtracking | Explore & prune | N-Queens | `O(n!)` |

### Idiomatic Go Implementation

```go
package main

import "fmt"

func mergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    mid := len(arr) / 2
    left := mergeSort(arr[:mid])
    right := mergeSort(arr[mid:])
    return merge(left, right)
}

func merge(left, right []int) []int {
    result := make([]int, 0, len(left)+len(right))
    i, j := 0, 0
    for i < len(left) && j < len(right) {
        if left[i] <= right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }
    result = append(result, left[i:]...)
    result = append(result, right[j:]...)
    return result
}

func main() {
    arr := []int{38, 27, 43, 3, 9}
    fmt.Println(mergeSort(arr))
}
```

### Edge Cases & Pitfalls
- **Stack overflow:** Missing base case panics runtime.
- **DP matrix size:** Large 2D slices cause OOM.
- **Greedy logic:** Local optimum ignores global optimum. Verify correctness.

## 3.4. Tooling

**Definition:** Go provides `go test`, `go fmt`, `go tool pprof`.

**Background & Philosophy:**
Tooling integrated into language. No third-party runner needed. Standardizes workflows.

**Use Cases:**
Unit testing. Code formatting. Benchmarking memory allocation.

**Memory Mechanics:**
`go test -benchmem` tracks heap allocations. High `allocs/op` ruins cache locality. Optimizing allocations increases speed.

### Idiomatic Go Implementation

```go
package main

import "testing"

func BenchmarkSum(b *testing.B) {
    data := make([]int, 10000)
    for i := range data {
        data[i] = i
    }
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        sum := 0
        for _, v := range data {
            sum += v
        }
        _ = sum
    }
}
```

### Anti-Patterns
- **Reinventing standard library:** Use `slices.Sort` instead of manual implementation.
- **LinkedList for speed:** Use slices. Contiguous memory beats pointer traversal.
- **Skipping Benchmarks:** Relying on Big-O. Measure actual memory layout impact.
- **Benchmark Without Reset:** Setup time corrupts result. Call `b.ResetTimer()`.
- **Ignoring Race Detector:** Deploying without `go test -race`. Causes silent data corruption.

## 3.5. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Array | `[N]T` | `O(1)` access | `O(n)` | Fixed buffer |
| Slice | `[]T` | `O(1)` access | `O(n)` | Dynamic collection |
| Map | `map[K]V` | `O(1)` avg | `O(n)` | Key-value lookup |
| Benchmark | `go test` | N/A | N/A | Measure speed |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 3:</strong> Go offers simplicity, fast execution, strong tooling. Leverage slices. Understand memory allocation. Measure with benchmarks.
{{% /alert %}}

## See Also
- [Chapter 1: The Role of Algorithms](/docs/part-i/chapter-1/)
- [Chapter 4: Fundamentals of Go Programming](/docs/part-i/chapter-4/)
