---
weight: 20200
title: "Chapter 6: Elementary Data Structures"
description: "Elementary Data Structures"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident.</em>" : Rob Pike</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 6 focuses on building elementary data structures (Stacks, Queues, Deques) utilizing Go 1.18+ Generics. Crucially, it explores hardware-level performance implications, demonstrating why <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous memory</abbr> drastically outperforms node-based memory.
{{% /alert %}}

## 6.1. Stacks (LIFO)

**Definition:** A LIFO data structure where the last element added is the first one removed.

**Background & Philosophy:**
The stack is one of the oldest and most natural data structures in computing, directly mirroring physical piles of objects. Its philosophy is restrictive access: by only allowing operations at one end, it provides incredibly predictable and fast behavior. In Go, stacks are almost entirely built using slices because the underlying array geometry perfectly matches the `Push` and `Pop` mechanics.

**Use Cases:**
Stacks are indispensable for tracking execution context (the call stack), parsing nested structures like JSON or HTML, evaluating mathematical expressions (Reverse Polish Notation), and implementing the "Undo" feature in text editors.

**Memory Mechanics:**
A slice-based stack allocates a contiguous block of RAM. Pushing an element modifies the next available byte and increments the length. Popping decreases the length pointer. This requires zero heap allocations (unless capacity is exceeded) and guarantees 100% CPU cache hits because the data is perfectly sequential.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Push | `O(1)` | Add to top |
| Pop | `O(1)` | Remove from top |
| Peek | `O(1)` | View top element |
| Values | `O(1)` overhead | Iterator (Go 1.23+) |

### Idiomatic Go 1.23+ Generic Implementation

Modern Go uses Generics `[T any]` and Iterators `iter.Seq[T]` to provide type-safe, efficient traversal.

```go
package main

import (
	"fmt"
	"iter"
)

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

// Values returns an iterator for LIFO traversal.
func (s *Stack[T]) Values() iter.Seq[T] {
	return func(yield func(T) bool) {
		for i := len(s.data) - 1; i >= 0; i-- {
			if !yield(s.data[i]) {
				return
			}
		}
	}
}

func main() {
	s := &Stack[string]{}
	s.Push("Hello")
	s.Push("Iterators")
	
	// Modern traversal using range-over-function
	for val := range s.Values() {
		fmt.Println(val)
	}
}
```

### Edge Cases & Pitfalls
- **Memory Leaks on Pop:** In a slice of pointers, executing `s.data = s.data[:lastIdx]` leaves the invisible trailing pointer in the underlying contiguous memory locations alive. The garbage collector cannot free it. You must explicitly zero out the index `s.data[lastIdx] = zero` before slicing.

## 6.2. Queues (FIFO)

**Definition:** A FIFO data structure. A naive queue implementation utilizing a slice shift (`s = s[1:]`) degrades performance to `O(n)` and inherently causes memory leaks. The idiomatic Go approach leverages a **Circular Ring Buffer**.

**Background & Philosophy:**
Queues enforce fairness through a "first come, first served" policy. While stacks are restrictive at one end, queues restrict access by splitting entry and exit points. The philosophy in Go is to implement this without sacrificing the contiguous memory benefits of arrays, which led to the widespread adoption of the Ring Buffer pattern rather than a linked list.

**Use Cases:**
Essential for rate limiting, job scheduling in worker pools (like handling HTTP requests), breadth-first search (BFS) in graph traversal, and buffering streams of data between asynchronous goroutines.

**Memory Mechanics:**
A Circular Ring Buffer pre-allocates a fixed array in RAM. Instead of shifting elements (which would cost `O(n)` memory writes), it uses two integer pointers (`head` and `tail`) that wrap around the array's capacity using the modulo operator `%`. This provides strict `O(1)` memory access and reuses the exact same contiguous memory block infinitely, preventing Garbage Collection churn.

### Idiomatic Go 1.23+ Generic Circular Buffer

```go
package main

import (
	"fmt"
	"iter"
)

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

// Values returns an iterator for FIFO traversal.
func (q *Queue[T]) Values() iter.Seq[T] {
	return func(yield func(T) bool) {
		for i := 0; i < q.size; i++ {
			idx := (q.head + i) % len(q.data)
			if !yield(q.data[idx]) {
				return
			}
		}
	}
}

func main() {
	q := NewQueue[int](3)
	q.Enqueue(100)
	q.Enqueue(200)
	
	for val := range q.Values() {
		fmt.Println("Value:", val)
	}
}
```

## 6.3. The Cache Locality War: Slice vs Linked List

**Background & Philosophy:**
Historically, computer science textbooks prescribe **Linked Lists** for Queues and Deques because insertions and deletions are theoretically `O(1)`. However, on modern CPU architectures, **this theory is dangerously misleading**. Go's standard library provides `container/list` (a doubly linked list), but pragmatic engineering favors slices. The philosophy shifts from theoretical operation counting to actual hardware sympathy.

**Use Cases:**
When choosing a data structure for a high-performance system like a game engine, a trading bot, or a database query planner, engineers must measure actual execution time rather than relying strictly on Big-O assumptions.

**Memory Mechanics:**
A slice occupies a contiguous memory block, leveraging CPU prefetching and L1 CPU cache. A Linked List allocates nodes randomly across the heap, causing cache misses and Garbage Collection pressure on traversal.

### The Benchmark Code (`_test.go`)

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
1. **Cache Locality:** A slice is a contiguous block of memory. A Linked List allocates nodes randomly across the heap, triggering massive cache misses.
2. **Escape Analysis & GC Pressure:** `list.PushBack()` dynamically allocates `&Element{}`. For 1 million items, it triggers 1,000,000 individual heap allocations. The Go Garbage Collector must traverse and trace every single node. The slice, conversely, only reallocates ~40 times.
3. **Generics Penalty:** `container/list` relies entirely on `any`. Retrieving a value requires a runtime type assertion `val := elem.Value.(int)`, adding massive overhead compared to a strongly typed Generic slice `[T any]`.

**Verdict:** In Go, favor slices and circular ring buffers. Only use linked lists for heavy insertions and deletions in the middle of large sequences.

## 6.4. Generic Deque (Double-Ended Queue)

**Definition:** A Deque is a generalized queue that allows insertions and deletions at both the front and the rear.

**Background & Philosophy:**
The Deque serves as a hybrid structure. It is born from the philosophy that sometimes algorithms need both stack-like and queue-like behavior simultaneously. 

**Use Cases:**
Essential for work-stealing algorithms in thread scheduling (where a thread processes its own tasks LIFO but steals from others FIFO), palindrome checking algorithms, and managing undo/redo logs with a maximum capacity constraint.

**Memory Mechanics:**
Knowing that `container/list` is notoriously slow, we construct a high-performance Deque utilizing a generic circular buffer. The Deque controls two pointers inside a single contiguous RAM allocation. `PushFront` decrements the head pointer (wrapping around to the end of the array using modulo), while `PushBack` increments the tail pointer. This ensures strict `O(1)` performance at both ends without sacrificing CPU cache locality.

```go
package main

import (
	"fmt"
	"iter"
)

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

// Values returns an iterator for the deque (front to back)
func (d *Deque[T]) Values() iter.Seq[T] {
	return func(yield func(T) bool) {
		for i := 0; i < d.size; i++ {
			idx := (d.head + i) % len(d.data)
			if !yield(d.data[idx]) {
				return
			}
		}
	}
}

func main() {
	d := NewDeque[string](5)
	d.PushBack("Backend")
	d.PushFront("Go")
	d.PushBack("Iterators")
	
	for val := range d.Values() {
		fmt.Println("Deque Value:", val)
	}
}
```

## Decision Matrix

| Use This When... | Avoid When... |
|------------------|---------------|
| Stack (`[]T`) : LIFO access only | Need FIFO or random access |
| Queue (`[]T` circular) : strict FIFO, high throughput | Need access to middle elements |
| Deque (`[]T` circular) : double-ended ops | Simple stack/queue suffices |
| `container/list` : standard library needed | Performance critical (GC pressure) |

### Edge Cases & Pitfalls

- **Empty structure:** Always check length before Pop/Peek.
- **Slice growth:** `append` may reallocate, capacity planning matters for queues.
- **Memory leaks:** Naive `slice[1:]` queues leak memory; use circular buffers.
- **Zero-capacity:** Operations on zero-cap structures panic if not handled.
- **Type constraints:** Generics `[T any]` fine for stacks; ordered constraints needed for priority queues.

### Anti-Patterns

- **Naive Slice Queue (`s = s[1:]`):** Slicing off the front of a slice never releases the beginning of the backing array, causing a memory leak. Use a circular ring buffer instead.
- **Pointer Leaks on Pop:** Removing an element from a slice of pointers/interfaces without zeroing the old slot keeps the reference alive, preventing garbage collection. Always set `s[lastIdx] = zero` before truncating.
- **Unbounded Stack Growth:** Using `append`-based stacks without capacity limits. A stack that grows unbounded can exhaust memory. Consider pre-sizing with `make([]T, 0, cap)`.
- **container/list for Production Queues:** Using `container/list` for queues deques causes O(n) allocation overhead per element and massive GC pressure. A slice-based circular buffer is idiomatic and far faster.
- **Ignoring Generic Type Constraints:** Using `[T any]` when your algorithm requires ordering (e.g., a min-heap or priority queue). Use `[T constraints.Ordered]` or a custom `Less` method to guarantee correctness at compile time.
- **Zero-Size Circular Buffer:** Operating on a ring buffer with `capacity == 0` causes division-by-zero panics in the modulo operation. Always validate `capacity > 0` in the constructor.

## Quick Reference

| Structure | Go Implementation | Time (Push/Pop) | Memory Allocations | Verdict |
|------|---------|------|-------|----------|
| Stack | `[]T` with `append` | `O(1)` amortized | Extremely low | The Go standard |
| Queue | `[]T` as Circular Buffer | `O(1)` | Extremely low | Ideal for strict FIFO |
| Queue | Naive `slice[1:]` | `O(n)` | Zero (but causes Memory Leaks) | **Anti-Pattern** |
| Deque | `container/list` | `O(1)` | Massive (1 alloc per node) | Avoid for high performance |
| Deque | `[]T` as Circular Buffer | `O(1)` | Extremely low | Highest performance |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 6:</strong> Elementary data structures in Go must be built with **Generics** to maintain strict type safety and eliminate interface boxing overhead. Due to CPU cache locality and Go's Garbage Collector architecture, contiguous slice-based ring buffers outperform pointer-based linked lists. With Go 1.23+, these structures should implement **Iterators** for idiomatic traversal.
{{% /alert %}}

## See Also

- [Chapter 5: Fundamental Data Structures in Go](/docs/part-ii/chapter-5/)
- [Chapter 7: Hashing and Hash Tables](/docs/part-ii/chapter-7/)
- [Chapter 47: LRU Cache](/docs/part-ix/chapter-47/)
