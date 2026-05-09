---
weight: 10400
title: "Chapter 4 - Fundamentals of Go Programming for Algorithms"
description: "Fundamentals of Go Programming for Algorithms"
icon: "article"
date: "2024-08-24T23:41:36+07:00"
lastmod: "2024-08-24T23:41:36+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Programs must be written for people to read, and only incidentally for machines to execute.</em>" — Harold Abelson</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 4 focuses on the fundamentals of Go programming, discussing the memory model, type system, functional patterns, and concurrency primitives that form the foundation for safe algorithm implementation.
{{% /alert %}}

## 4.1. Understanding Go's Memory Model

**Definition:** Go manages memory via <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">garbage collection</abbr>; pointers are safe (no <abbr title="A variable that stores a memory address.">pointer</abbr> arithmetic), and slices are references to an underlying <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>.

### Operations & Complexity

| Operation | Go Construct | Complexity | Description |
|---------|--------------|------------|------------|
| <abbr title="A LIFO (Last In, First Out) abstract data type.">Stack</abbr> allocation | Local var | <code>O(1)</code> | Automatic, LIFO |
| <abbr title="A specialized tree-based data structure that satisfies the heap property.">Heap</abbr> allocation | `make`, `new`, `&T{}` | <code>O(1)</code> amortized | GC-managed |
| <abbr title="A variable that stores a memory address.">Pointer</abbr> dereference | `*p` | <code>O(1)</code> | Safe, no arithmetic |
| Slice re-slicing | `s[i:j]` | <code>O(1)</code> | Shares backing <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> |

### Pseudocode

```text
mutateSlice(s):
    s[0] = 99
    return

mutatePointer(p):
    dereference p and set value to 20
    return
```

### Idiomatic Go Implementation

<abbr title="A variable that stores a memory address.">Pointer</abbr> and slice behavior:

```go
package main

import "fmt"

func mutateSlice(s []int) {
	s[0] = 99
}

func main() {
	data := []int{1, 2, 3}
	mutateSlice(data)
	fmt.Println(data)

	x := 10
	p := &x
	*p = 20
	fmt.Println(x)
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Need to share data between functions without copying | Data is immutable and small (pass by <abbr title="The data associated with a key in a key-value pair.">value</abbr>) |
| Need to modify data in-place | Explicit ownership transfer is required |
| Linked/<abbr title="A hierarchical data structure with a root node and child nodes.">tree</abbr> data structures | <abbr title="A variable that stores a memory address.">Pointer</abbr> arithmetic is required |

### Edge Cases & Pitfalls
- **Case slice alias:** `s2 := s1[:]` shares the backing <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>; modifying `s2` affects `s1`.
- **Case append reallocate:** `s = append(s, v)` might allocate a new <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>; pointers to old elements become invalid.
- **Case nil <abbr title="A variable that stores a memory address.">pointer</abbr> dereference:** Dereferencing a `nil` <abbr title="A variable that stores a memory address.">pointer</abbr> causes a panic.

## 4.2. Go's Type System and Its Role in Algorithms

**Definition:** Go features static typing with type inference, generics (Go 1.18+), and interfaces to ensure type safety at compile time.

### Operations & Complexity

| Feature | Usage | Overhead |
|-------|----------|----------|
| Static typing | Catch errors at compile time | Zero <abbr title="The period during which a computer program is executing.">runtime</abbr> |
| Generics | Reusable algorithms | Monomorphization (compile time) |
| <abbr title="A shared boundary across which two or more separate components exchange information.">Interface</abbr> | Polymorphism | <abbr title="A variable that stores a memory address.">Pointer</abbr> indirection |
| Type assertion | <abbr title="The period during which a computer program is executing.">Runtime</abbr> type check | <code>O(1)</code> |

### Pseudocode

```text
find(arr, target):
    for i = 0 to len(arr)-1:
        if arr[i] == target:
            return (i, true)
    return (0, false)
```

### Idiomatic Go Implementation

Generic search with `comparable`:

```go
package main

import "fmt"

func find[T comparable](arr []T, target T) (int, bool) {
	for i, v := range arr {
		if v == target {
			return i, true
		}
	}
	return 0, false
}

func main() {
	nums := []int{10, 20, 30}
	if i, ok := find(nums, 20); ok {
		fmt.Println("Found at", i)
	}
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Need type-safe reusable code | Performance-critical inner loops |
| Various data types share the same logic | Only one type is used, generics add complexity |
| <abbr title="A shared boundary across which two or more separate components exchange information.">Interface</abbr> abstraction is needed | <abbr title="A shared boundary across which two or more separate components exchange information.">Interface</abbr> call overhead is significant |

### Edge Cases & Pitfalls
- **Case type assertion panic:** `x.(int)` on the wrong type causes a panic; use `v, ok := x.(int)`.
- **Case nil <abbr title="A shared boundary across which two or more separate components exchange information.">interface</abbr>:** An <abbr title="A shared boundary across which two or more separate components exchange information.">interface</abbr> <abbr title="The data associated with a key in a key-value pair.">value</abbr> with a `nil` concrete <abbr title="A variable that stores a memory address.">pointer</abbr> is not equal to a `nil` <abbr title="A shared boundary across which two or more separate components exchange information.">interface</abbr>.
- **Case generic instantiation:** Generics increase binary size due to monomorphization.

## 4.3. Slices and Functional Programming in Go

**Definition:** Slices in Go are references to arrays that support functional-style operations like map, filter, and reduce through manual <abbr title="The repetition of a process, typically using loops.">iteration</abbr>.

### Operations & Complexity

| Operation | Go Idiom | Complexity |
|---------|----------|--------------|
| Map | Loop + append | <code>O(n)</code> |
| Filter | Loop + conditional append | <code>O(n)</code> |
| Reduce | Loop + accumulator | <code>O(n)</code> |
| Slicing | `s[i:j]` | <code>O(1)</code> |

### Pseudocode

```text
filter(arr, predicate):
    out = empty array
    for each element in arr:
        if predicate(element):
            append element to out
    return out
```

### Idiomatic Go Implementation

Higher-order function with closure:

```go
package main

import "fmt"

func filter(nums []int, predicate func(int) bool) []int {
	var out []int
	for _, n := range nums {
		if predicate(n) {
			out = append(out, n)
		}
	}
	return out
}

func main() {
	even := filter([]int{1, 2, 3, 4, 5}, func(n int) bool {
		return n%2 == 0
	})
	fmt.Println(even)
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Need data transformation pipelines | Performance is critical (manual loops are faster) |
| Readability is more important than micro-optimization | High memory pressure (intermediate slices) |

### Edge Cases & Pitfalls
- **Case nil slice append:** `append(nil, 1)` works and returns a new slice.
- **Case slice sharing:** Modifying elements in a slice passed to a function affects the caller.
- **Case capacity leak:** `s[:0]` reuses the backing <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>, but old elements are still referenced, preventing <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">garbage collection</abbr>.

## 4.4. Concurrency in Go for Parallel Algorithms

**Definition:** Goroutines, channels, and sync primitives enable parallel algorithms in Go with memory safety through communication (channels) or synchronization (mutexes).

### Operations & Complexity

| Primitive | Overhead | Use Case |
|-----------|----------|----------|
| Goroutine | ~2KB <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> | Lightweight concurrency |
| Channel | Blocking/unblocking | Communication between goroutines |
| Mutex | Contention cost | Shared mutable state |
| Atomic | Hardware-level | Counter, flag |

### Pseudocode

```text
parallelMergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) / 2
    spawn sort(left = arr[0:mid])
    spawn sort(right = arr[mid:])
    wait for both
    return merge(left, right)

merge(a, b):
    result = empty array
    while a and b not empty:
        append smaller front element
    append remaining elements
    return result
```

### Idiomatic Go Implementation

Parallel <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">merge sort</abbr> with goroutines:

```go
package main

import (
	"fmt"
	"sync"
)

func merge(a, b []int) []int {
	r := make([]int, 0, len(a)+len(b))
	for len(a) > 0 && len(b) > 0 {
		if a[0] < b[0] {
			r = append(r, a[0])
			a = a[1:]
		} else {
			r = append(r, b[0])
			b = b[1:]
		}
	}
	return append(append(r, a...), b...)
}

func pSort(a []int) []int {
	if len(a) <= 1 {
		return a
	}
	mid := len(a) / 2
	var l, r []int
	var wg sync.WaitGroup
	wg.Add(2)
	go func() { l = pSort(a[:mid]); wg.Done() }()
	go func() { r = pSort(a[mid:]); wg.Done() }()
	wg.Wait()
	return merge(l, r)
}

func main() {
	fmt.Println(pSort([]int{3, 1, 4, 1, 5, 9, 2, 6}))
}
```

### Decision Matrix

| Use This When... | Avoid If... |
|--------------------|------------------|
| Need parallelism for CPU-bound tasks | Goroutine overhead > speedup (small n) |
| I/O-bound concurrency | Shared state without synchronization |
| Natural data parallelism | Tasks with many dependencies |

### Edge Cases & Pitfalls
- **Case data race:** `go test -race` is mandatory for concurrent code; the race detector slows execution by 10-20x but is crucial for <abbr title="The process of finding and resolving defects within a computer program.">debugging</abbr>.
- **Case goroutine leak:** A goroutine blocked on a channel without a receiver causes a leak.
- **Case closing channel:** Only the sender should close a channel; a receiver closing it will cause a panic.
- **Case WaitGroup reuse:** Reusing a `WaitGroup` without ensuring `Wait` has completed can cause a race condition.

## 4.5. Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| <abbr title="A variable that stores a memory address.">Pointer</abbr> | `*T` | <code>O(1)</code> | — | No arithmetic |
| Slice | `[]T` | <code>O(1)</code> access | — | Shared backing <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> |
| Map | `map[K]V` | <code>O(1)</code> avg | — | Not ordered |
| Generic | `func f[T comparable]` | Compile time | — | Monomorphization |
| Goroutine | `go func()` | <code>O(1)</code> start | ~2KB <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> | Concurrent execution |
| Channel | `chan T` | Blocking | varies | CSP communication |
| Mutex | `sync.Mutex` | Contention | Lock/Unlock |
| Atomic | `sync/atomic` | Hardware | For int, <abbr title="A variable that stores a memory address.">pointer</abbr> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 4:</strong> This chapter covers Go's memory model, type system with generics, functional programming patterns with slices, and concurrency primitives for parallel algorithms. It explains how pointers, slices, goroutines, channels, and mutexes enable efficient and safe algorithm implementations in Go.
{{% /alert %}}