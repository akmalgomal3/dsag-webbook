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
<strong>"<em>Simplicity is the ultimate sophistication.</em>" — Leonardo da Vinci</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 8 covers singly, doubly, and circular linked lists. Learn to choose between linked lists and slices based on garbage collector pressure and cache locality.
{{% /alert %}}

## 8.1. Singly Linked List

**Definition:** Singly linked list stores nodes in non-contiguous memory. Each node contains data and pointer to next node.

**Mechanics:**
Singly linked list optimizes dynamic growth. Element isolation allows insertion without copying full memory block. Update one pointer to add element.

Nodes sit scattered on heap. Memory fragmentation destroys spatial locality. Traversal triggers cache misses. Performance is lower than slice iteration.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Access | <code>O(n)</code> | Sequential traversal |
| Insert head | <code>O(1)</code> | Update head pointer |
| Delete head | <code>O(1)</code> | Update head pointer |
| Insert tail | <code>O(n)</code> | Must traverse to end |
| Search | <code>O(n)</code> | Linear scan |

### Idiomatic Go Implementation

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
| Frequent head edits | Random access needed (use slice) |
| Unknown final size | Cache locality matters (slice is faster) |
| Building stacks/queues | Memory overhead per element is high |

### Edge Cases & Pitfalls

- **Nil pointer:** Check `Head == nil` before traversal.
- **Memory leaks:** Clear references to deleted nodes.
- **GC pressure:** Many small allocations tax garbage collector.

## 8.2. Doubly Linked List

**Definition:** Doubly linked list adds `Prev` pointer. Enables bidirectional traversal and O(1) deletion from any node reference.

**Mechanics:**
Doubly linked list allows complete operational freedom. Extra pointer allows updating preceding node without full traversal. Sacrifice memory for speed at arbitrary points.

On 64-bit systems, `DNode` takes 24 bytes. 66% of allocation is pointer overhead. High overhead reduces data density in cache lines.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Access | <code>O(n)</code> | Sequential traversal |
| Insert head/tail | <code>O(1)</code> | With tail pointer |
| Delete node | <code>O(1)</code> | Given node reference |
| Reverse travel | <code>O(n)</code> | Using Prev pointers |

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

**Definition:** Circular linked list connects last node to first. No logical end.

**Mechanics:**
Circular list models infinite continuity. Eliminates nil-pointer checks at boundaries.

Tail links to head. Memory usage matches singly linked list. Garbage collector reclaims cycles if unreachable from root.

### Idiomatic Go Implementation

```go
package main

import "fmt"

type CNode struct {
	Val  int
	Next *CNode
}

type CircularList struct {
	Tail *CNode // Tail.Next is head
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

- **Cache Ignorance:** Using linked list for sequence when slice is 10-50x faster. Use `[]T` first.
- **Head-Only Doubly List:** Forces O(n) tail access. Store `Head` and `Tail` for O(1).
- **Missing Nil Guard:** Traversing `Next` without check causes panic. Guard all pointers.
- **Infinite Loop:** Iterating circular list without cycle check. Compare `cur` to `head`.
- **Dangling Refs:** Deleted nodes keep memory if pointers remain. Zero out pointers.
- **Type Casting:** `container/list` uses `any`. Prefer generic structs for safety.

## 8.4. Quick Reference

| Structure | Go Type | Access | Insert Head | Delete Head | Memory |
|-----------|---------|--------|-------------|-------------|--------|
| Singly List | `struct{ Val; Next }` | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × node |
| Doubly List | `struct{ Val; Prev; Next }` | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × node |
| Circular List | `struct{ Val; Next }` + Tail | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × node |
| Slice | `[]T` | <code>O(1)</code> | <code>O(n)</code> | <code>O(n)</code> | Contiguous |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary:</strong> Linked lists provide O(1) edits at known positions. Random access is slow. Slices are better for most Go code due to cache performance.
{{% /alert %}}

## See Also

- [Chapter 5: Fundamental Data Structures in Go](/docs/part-ii/chapter-5/)
- [Chapter 6: Elementary Data Structures](/docs/part-ii/chapter-6/)
- [Chapter 9: Trees and Balanced Trees](/docs/part-iii/chapter-9/)
