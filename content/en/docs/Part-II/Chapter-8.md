---
weight: 20400
title: "Chapter 8: Linked Lists"
description: "Linked Lists"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Simplicity is the ultimate sophistication.</em>" : Leonardo da Vinci</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 8 covers linked list data structures in Go: singly linked lists, doubly linked lists, and circular linked lists. Understand when linked lists outperform slices and when they fall short due to Go's garbage collector and <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> locality.
{{% /alert %}}

## 8.1. <abbr title="A linked list where each node points only to the next node">Singly Linked List</abbr>

**Definition:** A <abbr title="A linked list where each node points only to the next node">singly linked list</abbr> is a linear collection of nodes where each node contains data and a <abbr title="A variable that stores a memory address.">pointer</abbr> to the next node. Unlike slices, linked lists do not require <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous memory</abbr>.

**Background & Philosophy:**
The philosophy of the <abbr title="A linked list where each node points only to the next node">singly linked list</abbr> is to optimize for dynamic growth. Before languages had automatically resizing arrays (like Go's slices), expanding an array required manually copying the entire memory block. Linked lists solved this by isolating each element, meaning an insertion only requires updating a single memory address rather than moving thousands of existing elements.

**Use Cases:**
Used fundamentally in hash table collision resolution (chaining), building immutable data structures in functional programming, and lock-free concurrent algorithms where updating a single `next` pointer via an atomic swap operation guarantees <abbr title="Property ensuring correct code under concurrent execution">thread safety</abbr>.

**Memory Mechanics:**
Each `Node` is allocated independently on the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>, scattering memory across <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>. This destroys <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. Traversing a linked list triggers <abbr title="A state where the data requested for processing is not found in the cache memory.">cache misses</abbr>, making it significantly slower than iterating a slice.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Access | <code>O(n)</code> | Sequential traversal required |
| Insert head | <code>O(1)</code> | Update a single pointer |
| Delete head | <code>O(1)</code> | Update a single pointer |
| Insert tail | <code>O(n)</code> | Must traverse to end |
| Search | <code>O(n)</code> | Linear scan |

### <abbr title="Code style considered standard and natural for Go">Idiomatic Go</abbr> Implementation

Use structs with pointer fields to build linked lists. Go's <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">garbage collector</abbr> handles memory management automatically.

```go
package main

import "fmt"

type Node struct {
	Val  int
	Next *Node
}

type LinkedList struct {
	Head *Node
	Size int
}

func (ll *LinkedList) InsertHead(val int) {
	ll.Head = &Node{Val: val, Next: ll.Head}
	ll.Size++
}

func (ll *LinkedList) DeleteHead() bool {
	if ll.Head == nil { return false }
	ll.Head = ll.Head.Next
	ll.Size--
	return true
}

func (ll *LinkedList) Search(val int) bool {
	for cur := ll.Head; cur != nil; cur = cur.Next {
		if cur.Val == val { return true }
	}
	return false
}

func (ll *LinkedList) Display() {
	for cur := ll.Head; cur != nil; cur = cur.Next {
		fmt.Printf("%d -> ", cur.Val)
	}
	fmt.Println("nil")
}

func main() {
	ll := &LinkedList{}
	ll.InsertHead(3)
	ll.InsertHead(2)
	ll.InsertHead(1)
	ll.Display() // 1 -> 2 -> 3 -> nil
}
```

### Decision Matrix

| Use Linked List When... | Avoid If... |
|-------------------------|-------------|
| Frequent head insertions/deletions | Random access is needed (use slice) |
| Unknown final size with frequent growth | Cache locality matters (slice is faster) |
| Implementing other structures (stacks, queues) | Memory overhead per element is a concern |

### Edge Cases & Pitfalls

- **Nil pointer dereference:** Always check `Head == nil` before operations.
- **Memory leaks:** Ensure no references remain to deleted nodes.
- **Go GC pressure:** Each node is a separate allocation, causing GC tracing overhead for large lists.

## 8.2. Doubly Linked List

**Definition:** A <abbr title="A linked list where each node points to both the next and previous nodes.">doubly linked list</abbr> extends the singly linked list by adding a `Prev` pointer, enabling bidirectional traversal and <code>O(1)</code> deletion from any position.

**Background & Philosophy:**
The philosophy here is expanding operational freedom at the cost of memory bloat. A singly linked list cannot easily delete a node if you only have a pointer to that node, because you cannot update the preceding node's `Next` pointer. A doubly linked list sacrifices space (an extra pointer per node) to provide complete <code>O(1)</code> operational freedom from any reference point.

**Use Cases:**
Essential for implementing LRU (Least Recently Used) caches, where you must instantly detach a heavily used item from the middle of the list and attach it to the front, and managing browser history (navigating backward and forward).

**Memory Mechanics:**
In Go, a 64-bit architecture requires 8 bytes per pointer. A `DNode` storing a 64-bit integer takes 24 bytes (8 bytes for `Val`, 8 bytes for `Prev`, 8 bytes for `Next`). Thus, 66% of the memory allocation is pure structural overhead. This drastically reduces the amount of actual data that can fit into the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> line, exacerbating the performance penalty of linked lists.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Access | <code>O(n)</code> | Sequential traversal |
| Insert head/tail | <code>O(1)</code> | With tail pointer |
| Delete any node | <code>O(1)</code> | Given node reference |
| Reverse traversal | <code>O(n)</code> | Using Prev pointers |

### Idiomatic Go Implementation

```go
package main

import "fmt"

type DNode struct {
	Val  int
	Prev *DNode
	Next *DNode
}

type DoublyLinkedList struct {
	Head *DNode
	Tail *DNode
	Size int
}

func (dll *DoublyLinkedList) InsertTail(val int) {
	newNode := &DNode{Val: val, Prev: dll.Tail}
	if dll.Tail != nil {
		dll.Tail.Next = newNode
	} else {
		dll.Head = newNode
	}
	dll.Tail = newNode
	dll.Size++
}

func (dll *DoublyLinkedList) DeleteNode(node *DNode) {
	if node == nil { return }
	if node.Prev != nil { node.Prev.Next = node.Next }
	if node.Next != nil { node.Next.Prev = node.Prev }
	if node == dll.Head { dll.Head = node.Next }
	if node == dll.Tail { dll.Tail = node.Prev }
	dll.Size--
}

func (dll *DoublyLinkedList) DisplayForward() {
	for cur := dll.Head; cur != nil; cur = cur.Next {
		fmt.Printf("%d <-> ", cur.Val)
	}
	fmt.Println("nil")
}

func main() {
	dll := &DoublyLinkedList{}
	dll.InsertTail(1)
	dll.InsertTail(2)
	dll.InsertTail(3)
	dll.DisplayForward() // 1 <-> 2 <-> 3 <-> nil
}
```

## 8.3. Circular Linked List

**Definition:** A circular linked list connects the last node back to the first, forming a cycle. Useful for round-robin scheduling and cyclic buffers.

**Background & Philosophy:**
The philosophy of a circular list is infinite continuity. It models systems that have no logical beginning or end, eliminating the edge case of checking for `nil` pointers at boundaries. 

**Use Cases:**
Used heavily in operating system task scheduling (round-robin thread execution), multiplayer board game turn management, and buffering continuous audio/video streams.

**Memory Mechanics:**
By linking the tail back to the head, there are no `nil` pointers in a fully populated circular list. The memory footprint matches a singly linked list. If the `CircularList` struct is destroyed but the nodes still reference each other, Go's mark-and-sweep <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">GC</abbr> detects they are unreachable and reclaims them.

### Idiomatic Go Implementation

```go
package main

import "fmt"

type CNode struct {
	Val  int
	Next *CNode
}

type CircularList struct {
	Tail *CNode // Points to last node; Tail.Next is head
	Size int
}

func (cl *CircularList) InsertHead(val int) {
	newNode := &CNode{Val: val}
	if cl.Tail == nil {
		newNode.Next = newNode
		cl.Tail = newNode
	} else {
		newNode.Next = cl.Tail.Next
		cl.Tail.Next = newNode
	}
	cl.Size++
}

func (cl *CircularList) Display() {
	if cl.Tail == nil { return }
	cur := cl.Tail.Next
	for {
		fmt.Printf("%d -> ", cur.Val)
		cur = cur.Next
		if cur == cl.Tail.Next { break }
	}
	fmt.Println("(cycle)")
}

func main() {
	cl := &CircularList{}
	cl.InsertHead(3)
	cl.InsertHead(2)
	cl.InsertHead(1)
	cl.Display() // 1 -> 2 -> 3 -> (cycle)
}
```

### Anti-Patterns

- **Using Linked Lists for Cache-Friendly Data:** Choosing a linked list for sequential iteration when a slice provides 10-50x better throughput due to CPU cache prefetching. Reach for `[]T` first; use linked lists only for frequent arbitrary insertions/deletions.
- **Head-Only Pointer in Doubly Linked List:** Maintaining only a `Head` pointer forces O(n) tail insertions. Always store both `Head` and `Tail` pointers for O(1) operations at both ends.
- **Forgetting Nil Checks:** Dereferencing `node.Next` or `node.Prev` without checking for `nil` first causes panics. Guard every pointer traversal.
- **Circular List Infinite Loops:** Iterating a circular list without detecting the cycle point (comparing back to `head`). Always use a `do-while` pattern: start at `head`, advance, and stop when `cur == head` again.
- **Retaining Dropped Node References:** After deleting a node, remaining references to it prevent the garbage collector from reclaiming its memory. Zero out `Prev` and `Next` pointers explicitly if the node may be long-lived.
- **container/list with Type Assertions:** Using `container/list` requires `any` and runtime type assertions (`elem.Value.(MyType)`), sacrificing type safety and adding overhead. Prefer generic structs with `[T any]`.

## 8.4. Quick Reference

| Structure | Go Type | Access | Insert Head | Delete Head | Memory |
|-----------|---------|--------|-------------|-------------|--------|
| Singly Linked List | `struct{ Val; Next }` | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × node size |
| Doubly Linked List | `struct{ Val; Prev; Next }` | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × 2 pointers |
| Circular List | `struct{ Val; Next }` + Tail | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × node size |
| Slice (for comparison) | `[]T` | <code>O(1)</code> | <code>O(n)</code> | <code>O(n)</code> | <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">Contiguous</abbr> |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 8:</strong> Linked lists provide flexible <code>O(1)</code> insertion and deletion at known positions but sacrifice random access and <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> locality. In Go, prefer slices for most use cases due to superior <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> performance and simpler memory layout. Use linked lists only when frequent insertions/deletions at arbitrary positions are required.
{{% /alert %}}

## See Also

- [Chapter 5: Fundamental Data Structures in Go](/docs/part-ii/chapter-5/)
- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)