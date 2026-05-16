---
weight: 70200
title: "Chapter 29: Parallel and Distributed Algorithms"
description: "Parallel and Distributed Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Parallel programming is not about making programs faster, but about creating solutions that can solve larger problems.</em>" — Jeff Dean</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 30 discusses parallel and distributed algorithms. Uses goroutines, channels, and worker pools in Go.
{{% /alert %}}

## 29.1. Parallelism in Go

**Definition:** Simultaneous computation across multiple CPU cores. Go provides goroutines and channels for coordination.

**Background & Philosophy:**
Hardware clock speeds plateaued. Computing must go wider. Parallelism trades simplicity for coordination complexity. Follows Amdahl's Law.

**Use Cases:**
Asynchronous log processing. Distributed HTTP requests. Parallel matrix multiplication.

**Memory Mechanics:**
Exposes hardware cache coherence issues. Adjacent array writes cause "False Sharing". CPU locks and invalidates L1 cache lines. Performance drops. Padding memory structures avoids this. Isolating data chunks is mandatory for speedup.

### Operations & Complexity

| Model | Time | Overhead | Description |
|-------|------|----------|------------|
| Sequential | $O(T)$ | 0 | Baseline execution |
| Goroutine | $O(T/p)$ | ~2μs spawn | Lightweight thread |
| Worker Pool | $O(T/p)$ | Fixed pool | Goroutine reuse |
| SIMD (Go asm) | $O(T/vec)$ | Manual | AVX/SSE instructions |

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
Go runtime uses M:N scheduling. Avoid goroutines for microscopic tasks. Tasks should exceed 1ms for tangible benefit.
{{% /alert %}}

### Decision Matrix

| Use Goroutines When... | Avoid If... |
|--------------------------|------------------|
| Task is CPU-bound: $> 1$ms | Task is too small: $< 100$μs |
| Independent sub-problems exist | Shared state lacks synchronization |
| Building pipeline stages | Strict sequential dependency exists |

### Edge Cases & Pitfalls

- **Goroutine leak:** Verify channels close. Use `defer close()`.
- **Data race:** Use `go test -race`. Protect with `sync.Mutex` or channels.
- **Excessive goroutines:** Millions are allowed. Stack starts at 2KB. Memory exhaustion possible.

## 29.2. Synchronization and Concurrency

**Definition:** Coordination of access to shared state. Go provides Mutex, RWMutex, WaitGroup, and channels.

### Operations & Complexity

| Primitive | Lock | Unlock | Description |
|-----------|------|--------|------------|
| sync.Mutex | `Lock()` | `Unlock()` | Mutual exclusion |
| sync.RWMutex | `RLock()` R, `Lock()` W | `RUnlock()` / `Unlock()` | Concurrent readers, single writer |
| sync.Map | `Load()` avg | . | Concurrent-safe map |
| Channel | `<-ch` | . | CSP-style communication |

Preference: channels > `sync/atomic` > `sync.Mutex`. Use `sync.Map` for read-heavy access. Standard maps with mutex are generally faster.

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Channels: coordination, pipelines | Simple counter needed: use atomic |
| Mutex: complex state updates | Simple counter updates: use atomic |
| sync.Map: many readers, rare writes | Write-heavy workloads |

### Edge Cases & Pitfalls

- **Deadlock:** Ensure unlock calls. Use `defer mu.Unlock()`.
- **Priority inversion:** RWMutex writers can starve if readers persist.
- **Primitive copying:** Never copy `sync.Mutex` by value. Pass by pointer.

## 29.3. Parallel Algorithms

**Definition:** Algorithms for multi-processor efficiency. Use task or data decomposition.

### Operations & Complexity

| Algorithm | Sequential | Parallel ($p$ processors) |
|-----------|------------|-----------------------|
| Parallel Prefix Sum | $O(n)$ | $O(n/p + \log p)$ |
| Parallel Merge Sort | $O(n \log n)$ | $O(n/p \log(n/p))$ |
| Parallel BFS | $O(V+E)$ | $O((V+E)/p + d \cdot \log p)$ |
| Map-Reduce | $O(n)$ | $O(n/p)$ |

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
**Amdahl's Law:** Parallelizable part limits speedup. Parallelizing tiny fragments adds overhead without gain.
{{% /alert %}}

### Decision Matrix

| Use Parallel Map When... | Avoid If... |
|-----------------------------|------------------|
| Pure function used: no side effects | Function performs I/O |
| Array is massive: $> 10$K elements | Array is small: $< 1$K elements |

### Edge Cases & Pitfalls

- **False sharing:** Adjacent array writes force cache updates. Degrades performance.
- **Uneven workload:** Use dynamic work stealing for load imbalance.

## 29.4. Worker Pools and Pipelines

**Definition:** Worker pool bounds running goroutines. Pipeline connects stages via channels.

### Operations & Complexity

| Pattern | Throughput | Latency | Description |
|---------|------------|---------|------------|
| Worker Pool | High | Low | Concurrency bounding |
| Pipeline | Medium | Low | Stream processing |
| Fan-out/Fan-in | Very High | Medium | Parallel stages |

Buffer sizes affect throughput. I/O-bound tasks need large buffers. CPU-bound tasks need small buffers.

### Decision Matrix

| Use Worker Pool When... | Use Pipeline When... |
|----------------------------|-------------------------|
| Resources limited: DB, files | Stream processing needed |
| Homogeneous tasks | Multi-stage transformations required |

### Edge Cases & Pitfalls

- **Channel deadlock:** Ensure active readers for every channel.
- **Panic propagation:** Use `defer/recover()` in workers. Use error channels.

### Anti-Patterns

- **Unbounded goroutines:** Spawning one per item overwhelms scheduler. Use pools.
- **Missing synchronization:** Concurrent map/slice writes cause races. Run `-race` test.
- **Blocking channels:** Deadlock possible in producer/consumer mismatch. Size buffers. Use `WaitGroup`.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Mutex | `sync.Mutex` | . | 1 word | State protection |
| RWMutex | `sync.RWMutex` | . | 1 word | Read-heavy caching |
| WaitGroup | `sync.WaitGroup` | . | 1 word | Barrier sync |
| Atomic | `sync/atomic` | $O(1)$ | . | Lock-free counters |
| Channel | `chan T` | . | . | CSP communication |
| sync.Map | `sync.Map` | . | . | Concurrent maps |
| Context | `context.Context` | . | . | Timeouts |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 29:</strong> Go uses goroutines and synchronization primitives. Mutex and channels coordinate state. Worker pools bound concurrency. Pipelines process streams.
{{% /alert %}}

## See Also

- [Chapter 28: Vector, Matrix, and Tensor Operations](/docs/part-vii/chapter-28/)
- [Chapter 30: Cryptographic Foundations Algorithms](/docs/part-vii/chapter-30/)
- [Chapter 31: Blockchain Data Structures and Algorithms](/docs/part-vii/chapter-31/)
