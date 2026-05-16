---
weight: 20100
title: "Chapter 5: Fundamental Data Structures in Go"
description: "Fundamental Data Structures in Go"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Simplicity is prerequisite for reliability.</em>" — Edsger Dijkstra</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 5 covers Go fundamental data structures. Topics: arrays, slices, maps, linked lists. Explores memory layouts. Demonstrates slice cache locality advantages. Integrates modern `slices` and `maps` packages.
{{% /alert %}}

## 5.1. Arrays and Slices

**Definition:** Array is fixed-size collection. Slice is dynamic view into array.

**Background & Philosophy:**
C/C++ arrays lack bounds checking. Go introduces "slice" as safe, first-class citizen. Abstracts pointer arithmetic. Retains dynamic array flexibility. Ensures safety.

**Use Cases:**
Default choice for ordered collections. Read file lines. Buffer network packets. Store database query rows.

**Memory Mechanics:**
Array uses single contiguous RAM block. Allocates on stack or heap. Slice uses 24-byte struct (64-bit). Holds pointer, length, capacity. Appending beyond capacity forces reallocation. Copies elements to new, larger contiguous memory block. Reallocation costs `O(n)` time, amortizes to `O(1)`.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Index access | `O(1)` | Random access |
| Append | `O(1)` amortized | Re-allocation if capacity full |
| Copy | `O(n)` | Element by element |
| Sort | `O(n log n)` | `slices.Sort` (pdqsort) |
| Binary Search | `O(log n)` | `slices.BinarySearch` |

### Idiomatic Go 1.21+ Implementation

Use `slices` package for safe, fast operations.

```go
package main

import (
	"fmt"
	"slices"
)

func main() {
    nums := []int{30, 10, 20}
    nums = append(nums, 40)

    slices.Sort(nums)
    fmt.Println("Sorted:", nums)

    idx, found := slices.BinarySearch(nums, 20)
    fmt.Printf("Found 20 at index %d: %v\n", idx, found)

    if slices.Contains(nums, 30) {
        fmt.Println("Slice contains 30")
    }
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Data size is known | Data size unknown (use slice) |
| Need zero-copy view | Frequent middle insertions required |
| Prioritize cache locality | Frequent resizing expected |

### Edge Cases & Pitfalls
- **Slice header leak:** Small slice on large backing array prevents GC. Use `slices.Clone`.
- **Append aliasing:** Slices sharing backing array overwrite each other on append.
- **Out of bounds:** Accessing beyond `len()` panics.

## 5.2. Maps

**Definition:** Go built-in hash table. Stores key-value pairs. Average `O(1)` access.

**Background & Philosophy:**
Provides optimized, built-in associative storage. Eliminates third-party dependencies. Runtime optimizes allocation, rehashing, hash seeds. Prevents hash collision DoS attacks.

**Use Cases:**
Cache database query results. Count element frequencies. Build fast lookup tables (routing registries).

**Memory Mechanics:**
Implemented as array of buckets. Each bucket holds up to 8 key-value pairs. Non-contiguous. Scatters data across heap. Exceeding load factor triggers incremental rehashing. Go allocates new array twice the size. Moves data incrementally. Prevents latency spikes. Incurs allocation overhead.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Insert | `O(1)` amortized | Rehashes when growing |
| Lookup | `O(1)` amortized | Worst case `O(n)` |
| Delete | `O(1)` amortized | Memory not freed immediately |
| Clear | `O(n)` | `clear(m)` (Go 1.21+) |

### Idiomatic Go 1.21+ Implementation

Use `maps` package and `clear` builtin.

```go
package main

import (
	"fmt"
	"maps"
)

func main() {
    m := make(map[string]int, 100)
    m["foo"] = 1
    m["bar"] = 2

    if v, ok := m["foo"]; ok {
        fmt.Println("foo:", v)
    }

    m2 := maps.Clone(m)
    
    if maps.Equal(m, m2) {
        fmt.Println("Maps are equal")
    }

    clear(m)
    fmt.Println("Length after clear:", len(m))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Fast key lookups needed | Ordered data required (maps are unordered) |
| Unique, comparable keys | Complex uncomparable keys |

### Edge Cases & Pitfalls
- **Unordered:** Iteration sequence random. Sort keys using `slices.Sort` for consistency.
- **Concurrent write:** Unsynchronized concurrent writes cause fatal panic. Use `sync.Mutex`.
- **Key mutability:** Slices, maps, functions are uncomparable. Cannot act as keys.

## 5.3. Linked Lists

**Definition:** Linear structure. Nodes point to next node. `container/list` provides doubly linked list.

**Background & Philosophy:**
Historically standard for variable-length data. Optimizes arbitrary insertions/deletions without shifting elements. Modern CPU architecture changes reality. Poor spatial locality makes slices faster. Relegates linked lists to specialized niches.

**Use Cases:**
LRU caches (frequent front moves). Lock-free concurrent queues (atomic pointer swaps).

**Memory Mechanics:**
Node structs allocate independently on heap. Traversal chases pointers across random memory addresses. Causes frequent cache misses. Doubly linked list adds 16-byte overhead (next, prev) per node. Bloats memory footprint vs slices.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| PushFront/Back | `O(1)` | Doubly linked list |
| Remove | `O(1)` | Requires pointer to element |
| Traverse | `O(n)` | Sequential access |

### Edge Cases & Pitfalls
- **Memory overhead:** High pointer overhead per node.
- **Type assertion:** `container/list` stores `any`. Runtime type assertions add overhead.
- **Cache miss:** Scattered memory breaks CPU prefetcher.

## 5.4. Structs and Methods

**Definition:** Struct groups fields. Method attaches function to specific type.

**Background & Philosophy:**
Favors composition over inheritance. Structs group data. Methods attach behaviors. Keeps data plain. Prevents deep inheritance hierarchies.

**Use Cases:**
ORM User models. Binary Tree nodes. HTTP server configuration state.

**Memory Mechanics:**
Struct fields sit sequentially in RAM. Compiler aligns fields to memory boundaries (8 bytes on 64-bit). Reordering fields reduces alignment padding. Pointer receiver (`*Struct`) avoids copying. Value receiver copies struct byte-by-byte to new stack location.

### Idiomatic Go Implementation

```go
package main

import "fmt"

type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(v T) {
    s.items = append(s.items, v)
}

func (s *Stack[T]) Pop() (T, bool) {
    var zero T
    if len(s.items) == 0 {
        return zero, false
    }
    v := s.items[len(s.items)-1]
    s.items[len(s.items)-1] = zero // avoid memory leak
    s.items = s.items[:len(s.items)-1]
    return v, true
}

func main() {
    s := &Stack[int]{}
    s.Push(42)
    if v, ok := s.Pop(); ok {
        fmt.Println("Popped:", v)
    }
}
```

### Anti-Patterns
- **Slice Reslicing Memory Leak:** `big[:2]` retains reference to entire array. Use `slices.Clone`.
- **Append to Nil Map:** Write to uninitialized map panics. Use `make(map[K]V)`.
- **Linked List for Speed:** Using `container/list` over slices. Slices outperform due to cache locality.
- **Value Receiver Mutation:** `(s Stack)` drops mutations. Use pointer receiver `(s *Stack)`.
- **Not Pre-allocating Maps:** Incremental growth triggers repeated rehashing. Hint capacity `make(map[K]V, n)`.

## 5.5. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Array | `[N]T` | `O(1)` access | . | Fixed size, stack |
| Slice | `[]T` | `O(1)` access | . | Dynamic array (default) |
| Map | `map[K]V` | `O(1)` avg | . | Key-value store |
| Linked List | `container/list` | `O(n)` access | . | Specialized FIFO/Deque |
| Stack | `[]T` + Generics | `O(1)` pop | . | LIFO |


{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 5:</strong> Slices remain primary Go collection. Maps provide fast `O(1)` lookup. Modern `slices` and `maps` packages simplify usage. Structs maintain hardware sympathy via contiguous memory layout.
{{% /alert %}}

## See Also
- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 7: Hashing and Hash Tables](/docs/part-ii/chapter-7/)
- [Chapter 8: Linked Lists](/docs/part-ii/chapter-8/)