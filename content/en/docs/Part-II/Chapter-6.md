---
weight: 2200
title: "Chapter 6 - Elementary Data Structures"
description: "Elementary Data Structures"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident.</em>" — Rob Pike</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 6 focuses on building elementary data structures (Stacks, Queues, Deques) utilizing Go 1.18+ Generics. Crucially, it explores hardware-level performance implications, demonstrating why contiguous memory drastically outperforms node-based memory.
{{% /alert %}}

## 6.1. Stacks (LIFO)

**Definition:** A LIFO (Last-In-First-Out) data structure where the last element added is the first one removed. 

### Idiomatic Go 1.18+ Generic Implementation

Before Go 1.18, developers relied on `interface{}` which sacrificed type safety and incurred boxing/unboxing overhead. Modern Go elegantly solves this with Generics `[T any]`.

```go
package main

import "fmt"

// Stack is a generic LIFO data structure.
type Stack[T any] struct {
	data []T
}

func (s *Stack[T]) Push(v T) {
	s.data = append(s.data, v)
}

func (s *Stack[T]) Pop() (T, bool) {
	var zero T // Retrieves the zero value for type T
	if len(s.data) == 0 {
		return zero, false
	}
	lastIdx := len(s.data) - 1
	v := s.data[lastIdx]
	
	// Prevent memory leaks by explicitly clearing the pointer
	s.data[lastIdx] = zero 
	
	// Slice truncation
	s.data = s.data[:lastIdx]
	return v, true
}

func main() {
	s := &Stack[string]{}
	s.Push("Hello")
	s.Push("Generics")
	
	if val, ok := s.Pop(); ok {
		fmt.Println(val) // "Generics"
	}
}
```

### Edge Cases & Pitfalls
- **Memory Leaks on Pop:** In a slice of pointers, executing `s.data = s.data[:lastIdx]` leaves the invisible trailing <abbr title="A variable that stores a memory address.">pointer</abbr> in the underlying <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> alive. The garbage collector cannot free it. You must explicitly zero out the <abbr title="A data structure that improves the speed of data retrieval operations.">index</abbr> `s.data[lastIdx] = zero` before slicing.

## 6.2. Queues (FIFO)

**Definition:** A FIFO (First-In-First-Out) data structure. A naive <abbr title="A FIFO (First In, First Out) abstract data type.">queue</abbr> implementation utilizing a slice shift (`s = s[1:]`) degrades performance to <code>O(n)</code> and inherently causes memory leaks. The idiomatic Go approach leverages a **Circular Ring Buffer**.

### Idiomatic Go 1.18+ Generic Circular Buffer

```go
package main

import "fmt"

// Queue is a generic, fixed-size circular buffer.
type Queue[T any] struct {
	data []T
	head int
	tail int
	size int
}

func NewQueue[T any](capacity int) *Queue[T] {
	return &Queue[T]{
		data: make([]T, capacity),
	}
}

func (q *Queue[T]) Enqueue(v T) bool {
	if q.size == len(q.data) {
		return false // Queue is completely full
	}
	q.data[q.tail] = v
	q.tail = (q.tail + 1) % len(q.data)
	q.size++
	return true
}

func (q *Queue[T]) Dequeue() (T, bool) {
	var zero T
	if q.size == 0 {
		return zero, false // Queue is empty
	}
	v := q.data[q.head]
	
	// Zero out to prevent GC memory leaks
	q.data[q.head] = zero 
	
	q.head = (q.head + 1) % len(q.data)
	q.size--
	return v, true
}

func main() {
	q := NewQueue[int](3)
	q.Enqueue(100)
	q.Enqueue(200)
	
	if val, ok := q.Dequeue(); ok {
		fmt.Println("Dequeued:", val) // 100
	}
}
```

## 6.3. The <abbr title="A hardware or software component that stores data so future requests can be served faster.">Cache</abbr> Locality War: Slice vs <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">Linked List</abbr>

Historically, computer science textbooks prescribe **Linked Lists** for Queues and Deques because insertions and deletions are theoretically <code>O(1)</code>. However, on modern CPU architectures, **this theory is dangerously misleading**.

Go's standard <abbr title="A collection of precompiled routines that a program can use.">library</abbr> provides `container/list` (a <abbr title="A linked list where each node points to both the next and previous nodes.">doubly linked list</abbr>). Let's explicitly <abbr title="A test used to compare the performance of computer hardware or software.">benchmark</abbr> an <code>O(1)</code> <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">Linked List</abbr> insertion against an <code>O(1)</code> amortized Slice append.

### The <abbr title="A test used to compare the performance of computer hardware or software.">Benchmark</abbr> Code (`_test.go`)

```go
package benchmark

import (
	"container/list"
	"testing"
)

const N = 1_000_000

// Benchmark pushing 1 million elements into a slice
func BenchmarkSliceAppend(b *testing.B) {
	for i := 0; i < b.N; i++ {
		var s []int
		for j := 0; j < N; j++ {
			s = append(s, j)
		}
	}
}

// Benchmark pushing 1 million elements into a linked list
func BenchmarkLinkedListPush(b *testing.B) {
	for i := 0; i < b.N; i++ {
		l := list.New()
		for j := 0; j < N; j++ {
			l.PushBack(j)
		}
	}
}
```

### The Results

If you run `go test -bench=. -benchmem`, the results will shock textbook purists:

```text
BenchmarkSliceAppend-10       1000      1.12 ms/op      40 MB/op       40 allocs/op
BenchmarkLinkedListPush-10      50     24.50 ms/op      56 MB/op  1000000 allocs/op
```

### The "Go Engineering" Analysis
1. **<abbr title="A hardware or software component that stores data so future requests can be served faster.">Cache</abbr> Locality:** A slice is a contiguous block of memory. When the CPU fetches `slice[0]`, it pulls the next 64 bytes into the L1 <abbr title="A hardware or software component that stores data so future requests can be served faster.">Cache</abbr> (pre-fetching). The CPU reads the slice at lightning speed. A <abbr title="A linear collection of data elements whose order is not given by physical placement in memory.">Linked List</abbr> allocates nodes randomly across the <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr>, triggering massive **<abbr title="A hardware or software component that stores data so future requests can be served faster.">Cache</abbr> Misses**.
2. **Escape Analysis & GC Pressure:** `list.PushBack()` dynamically allocates `&Element{}`. For 1 million items, it triggers **1,000,000 individual <abbr title="A specialized tree-based data structure that satisfies the heap property.">heap</abbr> allocations**. The Go Garbage Collector must traverse and trace every single <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr>. The slice, conversely, only reallocates ~40 times.
3. **Generics Penalty:** `container/list` relies entirely on `interface{}` / `any`. Retrieving a <abbr title="The data associated with a key in a key-value pair.">value</abbr> requires a <abbr title="The period during which a computer program is executing.">runtime</abbr> type assertion `val := elem.Value.(int)`, adding massive overhead compared to a strongly typed Generic slice `[T any]`.

**Verdict:** In Go, relentlessly favor slices and circular ring buffers. Only resort to linked lists if you are performing heavy insertions and deletions identically in the *middle* of an immense sequence.

## 6.4. Generic <abbr title="A double-ended queue allowing insertion and deletion at both ends.">Deque</abbr> (Double-Ended <abbr title="A FIFO (First In, First Out) abstract data type.">Queue</abbr>)

Knowing that `container/list` is notoriously slow, we construct a high-performance <abbr title="A double-ended queue allowing insertion and deletion at both ends.">Deque</abbr> utilizing a generic circular buffer, ensuring strict <code>O(1)</code> performance at both ends without sacrificing <abbr title="A hardware or software component that stores data so future requests can be served faster.">Cache</abbr> Locality.

```go
package main

import "fmt"

type Deque[T any] struct {
	data []T
	head int
	tail int
	size int
}

func NewDeque[T any](capacity int) *Deque[T] {
	return &Deque[T]{
		data: make([]T, capacity),
	}
}

// PushFront inserts at the head, wrapping backwards
func (d *Deque[T]) PushFront(v T) bool {
	if d.size == len(d.data) {
		return false
	}
	d.head = (d.head - 1 + len(d.data)) % len(d.data)
	d.data[d.head] = v
	d.size++
	return true
}

// PushBack inserts at the tail, wrapping forwards
func (d *Deque[T]) PushBack(v T) bool {
	if d.size == len(d.data) {
		return false
	}
	d.data[d.tail] = v
	d.tail = (d.tail + 1) % len(d.data)
	d.size++
	return true
}

func main() {
	d := NewDeque[string](5)
	d.PushBack("Backend")
	d.PushFront("Go")
	
	// Buffer visually looks like: [ "Go", "Backend", nil, nil, nil ]
	fmt.Println("Deque operational.")
}
```

## Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Structure | Go Implementation | Time (Push/Pop) | Memory Allocations | Verdict |
|------|---------|------|-------|----------|
| <abbr title="A LIFO (Last In, First Out) abstract data type.">Stack</abbr> | `[]T` with `append` | <code>O(1)</code> amortized | Extremely low | The Go standard |
| <abbr title="A FIFO (First In, First Out) abstract data type.">Queue</abbr> | `[]T` as Circular Buffer | <code>O(1)</code> | Extremely low | Ideal for strict FIFO |
| <abbr title="A FIFO (First In, First Out) abstract data type.">Queue</abbr> | Naive `slice[1:]` | <code>O(n)</code> | Zero (but causes Memory Leaks) | **Anti-Pattern** |
| <abbr title="A double-ended queue allowing insertion and deletion at both ends.">Deque</abbr> | `container/list` | <code>O(1)</code> | Massive (1 alloc per <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr>) | Avoid for high performance |
| <abbr title="A double-ended queue allowing insertion and deletion at both ends.">Deque</abbr> | `[]T` as Circular Buffer | <code>O(1)</code> | Extremely low | Highest performance |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 6:</strong> Elementary data structures in Go must be built with **Generics** to maintain strict type safety and eliminate <abbr title="A shared boundary across which two or more separate components exchange information.">interface</abbr> boxing overhead. Due to CPU <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr> locality and Go's Garbage Collector architecture, contiguous slice-based ring buffers ruthlessly outperform pointer-based linked lists.
{{% /alert %}}