---
weight: 70200
title: "Chapter 30 - Parallel and Distributed Algorithms"
description: "Parallel and Distributed Algorithms"
icon: "article"
date: "2024-08-24T23:42:46+07:00"
lastmod: "2024-08-24T23:42:46+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Parallel programming is not about making programs faster, but about creating solutions that can solve larger problems.</em>" — Jeff Dean</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 30 discusses parallel and distributed algorithms employing goroutines, channels, synchronization primitives, and worker pools in Go.
{{% /alert %}}

## 30.1. Parallelism in Go

**Definition:** Parallelism involves executing computations simultaneously across multiple CPU cores. Go provides goroutines (lightweight threads) and channels for inter-process communication.

### Operations & Complexity

| Model | Time | Overhead | Description |
|-------|------|----------|------------|
| Sequential | <code>O(T)</code> | 0 | Baseline |
| Goroutine | <code>O(T/p)</code> | ~2μs spawn | Lightweight thread |
| Worker Pool | <code>O(T/p)</code> | Fixed pool | Reuses goroutines |
| SIMD (Go asm) | <code>O(T/vec)</code> | Manual | AVX/SSE |

### Pseudocode

```text
ParallelSum(arr):
    numWorkers = number of CPU cores
    chunk = ceil(length(arr) / numWorkers)
    partials = new array of size numWorkers
    for each worker i:
        start = i * chunk
        end = min(start + chunk, length(arr))
        spawn worker:
            sum = 0
            for each v in arr[start:end]:
                sum += v
            partials[i] = sum
    wait for all workers
    total = sum of all partials
    return total
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "runtime"
    "sync"
)

func parallelSum(arr []int) int {
    numCPU := runtime.NumCPU()
    n := len(arr)
    chunk := (n + numCPU - 1) / numCPU
    var wg sync.WaitGroup
    partials := make([]int, numCPU)

    for i := 0; i < numCPU; i++ {
        start := i * chunk
        end := start + chunk
        if start >= n {
            break
        }
        if end > n {
            end = n
        }
        wg.Add(1)
        go func(idx, s, e int) {
            defer wg.Done()
            sum := 0
            for _, v := range arr[s:e] {
                sum += v
            }
            partials[idx] = sum
        }(i, start, end)
    }
    wg.Wait()
    total := 0
    for _, v := range partials {
        total += v
    }
    return total
}

func main() {
    arr := make([]int, 1000000)
    for i := range arr {
        arr[i] = i + 1
    }
    fmt.Println("Parallel sum:", parallelSum(arr))
}
```

{{% alert icon="📌" context="warning" %}}
Go's <abbr title="The period during which a computer program is executing.">runtime</abbr> scheduler utilizes an M:N scheduling model. Do not spawn goroutines for microscopic tasks; enforce a minimum threshold for tasks to yield a tangible benefit.
{{% /alert %}}

### Decision Matrix

| Use Goroutines When... | Avoid If... |
|--------------------------|------------------|
| The task is CPU-bound and execution time > 1ms | The task is excessively small (< 100μs) |
| Dealing with independent sub-problems | Dealing with highly shared state lacking synchronization |
| Constructing pipeline stages | There is a strict, strong sequential dependency |

### Edge Cases & Pitfalls

- **Goroutine leak:** Always verify that channels are closed or ... is guaranteed to be called.
- **Data race:** Extensively use ... for detection. Rely on ... or channels for safety.
- **Too many goroutines:** While millions of goroutines are permissible, they can consume massive amounts of stack memory (starting at 2KB each).

## 30.2. Synchronization and Concurrency

**Definition:** Synchronization coordinates access to shared states. Go supplies standard tools such as Mutex, RWMutex, WaitGroup, and channels for orchestration.

### Operations & Complexity

| Primitive | Lock | Unlock | Description |
|-----------|------|--------|------------|
| sync.Mutex | ... | ... | Absolute mutual exclusion |
| sync.RWMutex | ... R, ... W | ... | Multiple concurrent readers, single writer |
| sync.Map | ... avg | — | Specialized concurrent-safe map |
| Channel | ... send/recv | — | Pure CSP-style communication |

### Pseudocode


### Idiomatic Go Implementation


Hierarchical preference: channels > `sync/atomic` > `sync.Mutex`. Utilize `sync.Map` exclusively for intensely read-heavy concurrent access; otherwise, standard maps protected by a mutex are generally faster.

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Channels: coordination, building pipelines | Only needing a basic counter (use atomic instead) |
| Mutex: complex state updates | Simple counter updates (atomic is much faster) |
| sync.Map: many readers, infrequent writes | Write-heavy workloads |

### Edge Cases & Pitfalls

- **Deadlock:** Absolutely ensure locks are always unlocked; utilize `defer mu.Unlock()`.
- **Priority inversion:** An `RWMutex` writer can suffer from starvation if readers perpetually acquire the lock.
- **Copying sync primitives:** Never copy a `sync.Mutex` by <abbr title="The data associated with a key in a key-value pair.">value</abbr> (always pass it by <abbr title="A variable that stores a memory address.">pointer</abbr>).

## 30.3. Parallel Algorithms

**Definition:** Algorithms designed specifically to run efficiently across multiple processors through diligent task or data decomposition.

### Operations & Complexity

| Algorithm | Sequential | Parallel (p processors) |
|-----------|------------|-----------------------|
| Parallel Prefix Sum | <code>O(n)</code> | <code>O(n/p + log p)</code> |
| Parallel <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> | <code>O(n log n)</code> | <code>O(n/p log(n/p))</code> |
| Parallel BFS | <code>O(V+E)</code> | <code>O((V+E)/p + d·log p)</code> |
| Map-Reduce | <code>O(n)</code> | <code>O(n/p)</code> |

### Pseudocode

```text
ParallelMap(arr, f):
    n = length(arr)
    result = new array of size n
    numWorkers = number of CPU cores
    chunk = ceil(n / numWorkers)
    for each worker i:
        start = i * chunk
        end = min(start + chunk, n)
        spawn worker:
            for j from start to end-1:
                result[j] = f(arr[j])
    wait for all workers
    return result
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "runtime"
    "sync"
)

func parallelMap(arr []int, f func(int) int) []int {
    n := len(arr)
    result := make([]int, n)
    numCPU := runtime.NumCPU()
    chunk := (n + numCPU - 1) / numCPU
    var wg sync.WaitGroup
    for i := 0; i < numCPU; i++ {
        start := i * chunk
        end := start + chunk
        if start >= n {
            break
        }
        if end > n {
            end = n
        }
        wg.Add(1)
        go func(s, e int) {
            defer wg.Done()
            for j := s; j < e; j++ {
                result[j] = f(arr[j])
            }
        }(start, end)
    }
    wg.Wait()
    return result
}

func main() {
    arr := []int{1, 2, 3, 4, 5, 6, 7, 8}
    squared := parallelMap(arr, func(x int) int { return x * x })
    fmt.Println("Squared:", squared)
}
```

{{% alert icon="📌" context="warning" %}}
**Amdahl's Law:** If 90% of your codebase is parallelizable, the absolute maximum theoretical speedup is 10×. Parallelizing tiny fragments is rarely worth the overhead.
{{% /alert %}}

### Decision Matrix

| Use Parallel Map When... | Avoid If... |
|-----------------------------|------------------|
| The function is pure with zero side effects | The function performs I/O operations |
| The <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> is massive, > 10K elements | The <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> is small (< 1K elements) |

### Edge Cases & Pitfalls

- **False sharing:** Goroutines writing to adjacent array elements force cache coherence updates, severely degrading performance.
- **Uneven workload:** Dynamic work stealing proves vastly superior when dealing with severe load imbalances.

## 30.4. Worker Pools and Pipelines

**Definition:** A worker pool strictly limits the maximum number of running goroutines; a pipeline seamlessly connects processing stages through channels.

### Operations & Complexity

| Pattern | Throughput | Latency | Description |
|---------|------------|---------|------------|
| Worker Pool | ... | ... | Bounds concurrency |
| Pipeline | ... | ... | Stream processing architecture |
| Fan-out/Fan-in | ... | ... | Highly parallel stages |

### Pseudocode


### Idiomatic Go Implementation


Channel buffer sizes dramatically influence throughput. For I/O-bound tasks, large buffers mitigate blocking. For purely CPU-bound tasks, very small buffers often suffice.

### Decision Matrix

| Use Worker Pool When... | Use Pipeline When... |
|----------------------------|-------------------------|
| Resources are strictly limited (DB connections, file descriptors) | Engaging in stream processing |
| Tasks are completely homogeneous | Executing multi-stage transformations |

### Edge Cases & Pitfalls

- **Channel deadlock:** Guarantee that there is always an active goroutine reading from every channel.
- **Panic propagation:** Proactively use ... within worker goroutines or utilize dedicated error channels.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Mutex | ... | — | — | Shared state protection |
| RWMutex | ... | — | — | Read-heavy caching |
| WaitGroup | ... | — | — | Barrier synchronization |
| Atomic | ... | ... | — | Lock-free counters and flags |
| Channel | ... | Blocking | varies | Pure CSP communication |
| sync.Map | ... | — | — | Highly concurrent maps |
| Context | ... | — | — | Cancellations and timeouts |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 30:</strong> This chapter discusses parallelism in Go using goroutines, synchronization primitives (Mutex, RWMutex, atomic, WaitGroup), channels, as well as worker pool and pipeline patterns. Utilize goroutines for independent CPU-bound tasks, channels for coordination, and worker pools to strictly bound concurrency when resources are limited.
{{% /alert %}}