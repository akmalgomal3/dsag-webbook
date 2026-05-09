---
weight: 20100
title: "Chapter 5 - Fundamental Data Structures in Go"
description: "Fundamental Data Structures in Go"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="📘" context="success" %}}
Chapter 5 focuses on fundamental data structures in Go (arrays, slices, maps, linked lists). It contrasts their memory layouts and explains how slices leverage CPU <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> locality for superior performance.
{{% /alert %}}

## 5.1. Arrays and Slices

**Definition:** An <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> is a collection of elements with the same type and a fixed size. A slice is a dynamic view into an <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> that allows for variable sizing.

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

- **Slice header leak:** A small slice of a large <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> keeps a <abbr title="A value that enables a program to indirectly access a particular datum.">reference</abbr> to the entire backing <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> in memory.
- **Append aliasing:** Two slices sharing a backing <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>; appending to one might overwrite data in the other.
- **Out of bounds:** Accessing beyond `len()` causes a panic.

## 5.2. Maps

**Definition:** A map is Go's built-in <abbr title="A data structure that implements an associative array using a hash function.">hash table</abbr> that stores key-value pairs with an average <code>O(1)</code> access time.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Insert | <code>O(1)</code> amortized | Rehashes when growing |
| Lookup | <code>O(1)</code> amortized | Worst case <code>O(n)</code> during extreme collisions |
| Delete | <code>O(1)</code> amortized | Does not immediately free backing memory |

### Pseudocode

```text
MapOps():
    m = empty hash map with capacity 100
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
| Need a simple <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr>/<abbr title="A double-ended queue allowing insertion and deletion at both ends.">deque</abbr> | Need high <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> locality |

### Edge Cases & Pitfalls

- **Memory overhead:** Each <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> has the overhead of two pointers.
- **Type assertion:** `container/list` stores `any`; requires type assertions.
- **<abbr title="A hardware or software component that stores data so future requests can be served faster.">Cache</abbr> miss:** Linked lists are scattered in memory, resulting in poor <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> locality.

## 5.4. Structs and Methods

**Definition:** A struct is a composite <abbr title="A classification identifying one of various types of data.">data type</abbr> that groups fields. A method is a function attached to a specific type, serving as the equivalent of `impl` blocks or classes.

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

- **<abbr title="A variable that stores a memory address.">Pointer</abbr> vs <abbr title="The data associated with a key in a key-value pair.">value</abbr> receiver:** Use <abbr title="A variable that stores a memory address.">pointer</abbr> receivers for modifications; <abbr title="The data associated with a key in a key-value pair.">value</abbr> receivers create copies.
- **Nil receiver:** Methods can be called on nil pointers if handled properly inside the method.
- **Zero <abbr title="The data associated with a key in a key-value pair.">value</abbr>:** Structs have zero values; ensure initialization is handled if required.

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| <abbr title="A collection of items stored at contiguous memory locations.">Array</abbr> | `[N]T` | <code>O(1)</code> access | — | Fixed size, <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> |
| Slice | `[]T` | <code>O(1)</code> access | — | Dynamic <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> |
| Map | `map[K]V` | <code>O(1)</code> avg | — | Key-value store |
| <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">Linked List</abbr> | `container/list` | <code>O(n)</code> access | — | <abbr title="A FIFO (First In, First Out) abstract data type.">Queue</abbr>, <abbr title="A double-ended queue allowing insertion and deletion at both ends.">deque</abbr> |
| <abbr title="A LIFO (Last In, First Out) abstract data type.">Stack</abbr> | `[]T` + methods | <code>O(1)</code> push/pop | — | LIFO |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 5:</strong> This chapter covers fundamental data structures in Go: arrays, slices, maps, linked lists, and structs with methods. Use slices for dynamic collections, maps for fast key-value lookups, linked lists for frequent insertions/deletions at ends, and structs with methods to build custom abstractions like stacks.
{{% /alert %}}