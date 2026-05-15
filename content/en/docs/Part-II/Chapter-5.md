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
<strong>"<em>Simplicity is prerequisite for reliability.</em>" : Edsger Dijkstra</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 5 focuses on fundamental data structures in Go (arrays, slices, maps, linked lists). It contrasts their memory layouts and explains how slices leverage <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality for superior performance.
{{% /alert %}}

## 5.1. Arrays and Slices

**Definition:** An <abbr title="A collection of items stored at <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous memory</abbr> locations.">array</abbr> is a collection of elements with the same type and a fixed size. A slice is a dynamic view into an array that allows for variable sizing.

**Background & Philosophy:**
In C and C++, arrays and pointers are tightly coupled, which often leads to buffer overflow vulnerabilities. Go's philosophy introduces the "slice" as a safe, first-class citizen. A slice abstracts away manual <abbr title="Performing mathematical operations on memory addresses.">pointer arithmetic</abbr> and bounds checking, providing the flexibility of dynamic arrays with the safety of modern programming languages.

**Use Cases:**
Slices are the default choice for almost all ordered collections in Go, used in everything from reading lines of a file, buffering network packets, to returning rows from a database query.

**Memory Mechanics:**
An array is a single, <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> block of memory allocated either on the <abbr title="Memory used to execute functions and store local variables.">stack</abbr> or the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>. A slice is a small 24-byte struct (on 64-bit architectures) consisting of a <abbr title="A variable that stores a memory address.">pointer</abbr> to the backing array, an integer representing the current length, and an integer for the capacity. Appending to a slice whose capacity is full forces the runtime to allocate a new, larger contiguous block of <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> and copy the old elements over, which is an <code>O(n)</code> operation in memory but amortizes to <code>O(1)</code>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| <abbr title="A data structure that improves the speed of data retrieval operations.">Index</abbr> access | <code>O(1)</code> | Random access |
| Append | <code>O(1)</code> amortized | Re-allocation if capacity is full |
| Copy | <code>O(n)</code> | Element by element |

### Pseudocode

```text
ArrayAndSlice():
    arr = fixed array of size 5
    slice = view of arr from index 1 to 3
    dyn = dynamic slice [10, 20]
    append 30 to dyn
    return arr, slice, dyn
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func main() {
    var arr [5]int = [5]int{1, 2, 3, 4, 5}
    slice := arr[1:4]           // slice of an array
    dyn := []int{10, 20}        // dynamic slice
    dyn = append(dyn, 30)       // add element

    fmt.Println(arr, slice, dyn)
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Data size is definitively known | Data size is unknown (use slices) |
| Need a zero-copy view | Need frequent insertions in the middle |

### Edge Cases & Pitfalls

- **Slice header leak:** A small slice of a large array keeps a <abbr title="A value that enables a program to indirectly access a particular datum.">reference</abbr> to the entire backing array in memory.
- **Append aliasing:** Two slices sharing a backing array; appending to one might overwrite data in the other.
- **Out of bounds:** Accessing beyond `len()` causes a panic.

## 5.2. Maps

**Definition:** A map is Go's built-in <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr> that stores key-value pairs with an average <code>O(1)</code> access time.

**Background & Philosophy:**
The philosophy behind Go maps is to provide a highly optimized, built-in associative data structure so developers do not need to rely on external libraries for basic key-value storage. By embedding it in the language, the Go runtime can optimize memory allocation, rehashing, and <abbr title="The process of mapping data of arbitrary size to fixed-size values.">hash</abbr> seed generation to prevent security vulnerabilities like hash collision denial-of-service attacks.

**Use Cases:**
Used for caching database query results, counting frequency of elements, and building fast lookup tables like routing registries in web frameworks.

**Memory Mechanics:**
Maps in Go are implemented as an array of buckets. Each bucket typically holds up to 8 key-value pairs. Because maps are <abbr title="Memory blocks allocated in fragmented, separate locations.">non-contiguous</abbr> data structures, they scatter data across the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>. When the map grows beyond its <abbr title="Ratio of stored entries to bucket count">load factor</abbr>, Go allocates a new array of buckets twice the size and incrementally moves the data over. This incremental rehashing prevents massive latency spikes during map insertion, but it still incurs <abbr title="Input/Output operations involving reading from or writing to a physical disk.">memory allocation</abbr> overhead.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Insert | <code>O(1)</code> amortized | Rehashes when growing |
| Lookup | <code>O(1)</code> amortized | Worst case <code>O(n)</code> during extreme collisions |
| Delete | <code>O(1)</code> amortized | Does not immediately free backing memory |

### Pseudocode

```text
MapOps():
    m = empty hashmap with capacity 100
    insert ("foo", 1) into m
    insert ("bar", 2) into m
    if "foo" exists in m:
        output value of "foo"
    remove "bar" from m
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
| Need fast <abbr title="A field or set of fields used to identify a record.">key</abbr> lookups | Need ordered data (use <abbr title="The process of arranging elements in a specific order.">sorting</abbr>) |
| Keys are unique and comparable | Complex keys lack equality definitions |

### Edge Cases & Pitfalls

- **Unordered:** Map <abbr title="The repetition of a process, typically using loops.">iteration</abbr> is not sequential.
- **Concurrent write:** Causes a panic if written concurrently without synchronization.
- **<abbr title="A field or set of fields used to identify a record.">Key</abbr> mutability:** Slices or maps cannot be used as keys.

## 5.3. Linked Lists

**Definition:** A <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">linked list</abbr> is a linear data structure where each <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> points to the next <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr>. Go provides `container/list` for a <abbr title="A linked list where each node points to both the next and previous nodes.">doubly linked list</abbr> implementation.

**Background & Philosophy:**
Before dynamic arrays were highly optimized, linked lists were the standard for variable-length data. The philosophy of a linked list is to optimize for insertions and deletions at arbitrary positions without shifting elements. However, in modern computing, the poor <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr> of linked lists often makes slices faster even for insertions, relegating linked lists to highly specialized use cases.

**Use Cases:**
Used in implementing <abbr title="Least Recently Used cache eviction policy">LRU</abbr> (Least Recently Used) caches where elements are constantly moved to the front, or in lock-free concurrent queues where node pointers can be atomically swapped.

**Memory Mechanics:**
Every element in a linked list is a separate struct allocated independently on the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>. This means traversing a linked list forces the CPU to constantly chase pointers across completely random memory addresses, resulting in frequent <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>. Additionally, a doubly linked list requires an extra 16 bytes per node just for the `next` and `prev` pointers, introducing significant memory bloat compared to slices.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| PushFront/Back | <code>O(1)</code> | <abbr title="A linked list where each node points to both the next and previous nodes.">Doubly linked list</abbr> |
| Remove | <code>O(1)</code> | If you hold a <abbr title="A variable that stores a memory address.">pointer</abbr> to the element |
| Traverse | <code>O(n)</code> | Sequential access |

### Pseudocode

```text
LinkedList():
    l = empty doubly linked list
    append 1 to back of l
    prepend 2 to front of l
    for each element e in l:
        output e.value
```

### Idiomatic Go Implementation

```go
package main

import (
    "container/list"
    "fmt"
)

func main() {
    l := list.New()
    l.PushBack(1)
    l.PushFront(2)

    for e := l.Front(); e != nil; e = e.Next() {
        fmt.Println(e.Value)
    }
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Frequent inserts/deletes at the ends | Need random access (use slices) |
| Need a simple <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr>/<abbr title="A double-ended queue allowing insertion and deletion at both ends.">deque</abbr> | Need high <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality |

### Edge Cases & Pitfalls

- **Memory overhead:** Each <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> has the overhead of two pointers.
- **Type assertion:** `container/list` stores `any`; requires type assertions.
- **Cache miss:** Linked lists are scattered in memory, resulting in poor <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> locality.

## 5.4. Structs and Methods

**Definition:** A <abbr title="Composite data type grouping fields">struct</abbr> is a composite <abbr title="A classification identifying one of various types of data.">data type</abbr> that groups fields. A method is a function attached to a specific type, serving as the equivalent of `impl` blocks or classes.

**Background & Philosophy:**
Go abandons traditional class-based inheritance in favor of composition. Structs group data, and methods attach behaviors to that data. The philosophy is to keep data structures as plain, transparent records, while interfaces define behaviors. This prevents the deep, tangled inheritance hierarchies common in Java or C++.

**Use Cases:**
Structs are the building blocks of every complex type in Go: from representing a User model in an ORM, to defining the nodes of a Binary Tree, or holding the configuration state of an HTTP server.

**Memory Mechanics:**
Fields in a struct are laid out sequentially in <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. The Go compiler automatically aligns fields to memory word boundaries (e.g., 8 bytes on a 64-bit system). Changing the order of fields in a struct definition can actually reduce its overall memory footprint by minimizing alignment padding. When a method uses a <abbr title="A variable that stores a memory address.">pointer</abbr> receiver (`*Struct`), no data is copied. When it uses a <abbr title="The data associated with a key in a key-value pair.">value</abbr> receiver, the entire struct is copied byte-by-byte into a new memory location on the <abbr title="Memory used to execute functions and store local variables.">stack</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Field access | <code>O(1)</code> | Direct memory offset |
| Method call | <code>O(1)</code> | Static dispatch |
| Copy by <abbr title="The data associated with a key in a key-value pair.">value</abbr> | <code>O(n)</code> | n = struct size |

### Pseudocode

```text
StackPush(s, v):
    append v to s.items

StackPop(s):
    if s.items is empty:
        return error
    v = last element of s.items
    remove last element
    return v
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

type Stack struct {
    items []int
}

func (s *Stack) Push(v int) {
    s.items = append(s.items, v)
}

func (s *Stack) Pop() (int, bool) {
    if len(s.items) == 0 {
        return 0, false
    }
    v := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return v, true
}

func main() {
    s := &Stack{}
    s.Push(10)
    v, ok := s.Pop()
    fmt.Println(v, ok)
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|---------------------|------------------|
| Need data abstraction | Need inheritance (Go does not support it) |
| Logic is tied directly to the data | Need complex generics (though Go 1.18+ supports basic generics) |

### Edge Cases & Pitfalls

- **Pointer vs value receiver:** Use <abbr title="A variable that stores a memory address.">pointer</abbr> receivers for modifications; <abbr title="The data associated with a key in a key-value pair.">value</abbr> receivers create copies.
- **Nil receiver:** Methods can be called on nil pointers if handled properly inside the method.
- **Zero value:** Structs have zero values; ensure initialization is handled if required.

## 5.5. Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| <abbr title="A collection of items stored at <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous memory</abbr> locations.">Array</abbr> | `[N]T` | <code>O(1)</code> access | . | Fixed size, <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> |
| Slice | `[]T` | <code>O(1)</code> access | . | Dynamic array |
| Map | `map[K]V` | <code>O(1)</code> avg | . | Key-value store |
| <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">Linked List</abbr> | `container/list` | <code>O(n)</code> access | . | <abbr title="A FIFO (First In, First Out) abstract data type.">Queue</abbr>, <abbr title="A double-ended queue allowing insertion and deletion at both ends.">deque</abbr> |
| <abbr title="A LIFO (Last In, First Out) abstract data type.">Stack</abbr> | `[]T` + methods | <code>O(1)</code> push/pop | . | <abbr title="Last In, First Out stack discipline">LIFO</abbr> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 5:</strong> This chapter covers fundamental data structures in Go: arrays, slices, maps, linked lists, and structs with methods. Use slices for dynamic collections, maps for fast key-value lookups, linked lists for frequent insertions/deletions at ends, and structs with methods to build custom abstractions like stacks.
{{% /alert %}}

## See Also

- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 7: Hashing and Hash Tables](/docs/part-ii/chapter-7/)
- [Chapter 8: Linked Lists](/docs/part-ii/chapter-8/)
