---
weight: 2400
title: "Chapter 8 - Linked Lists"
description: "Linked Lists"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Simplicity is the ultimate sophistication.</em>" — Leonardo da Vinci</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 8 covers linked list data structures in Go: singly linked lists, doubly linked lists, and circular linked lists. Understand when linked lists outperform slices and when they fall short due to Go's garbage collector and cache locality.
{{% /alert %}}

## 8.1. Singly Linked List

**Definition:** A singly linked list is a linear collection of nodes where each node contains data and a pointer to the next node. Unlike slices, linked lists do not require contiguous memory.

### Operations & Complexity

| Operation | Complexity | Description |
|-----------|------------|-------------|
| Access | <code>O(n)</code> | Sequential traversal required |
| Insert head | <code>O(1)</code> | Update a single pointer |
| Delete head | <code>O(1)</code> | Update a single pointer |
| Insert tail | <code>O(n)</code> | Must traverse to end |
| Search | <code>O(n)</code> | Linear scan |

### Idiomatic Go Implementation

Use structs with pointer fields to build linked lists. Go's garbage collector handles memory management automatically.

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

**Definition:** A doubly linked list extends the singly linked list by adding a `Prev` pointer, enabling bidirectional traversal and <code>O(1)</code> deletion from any position.

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

## 8.4. Quick Reference

| Structure | Go Type | Access | Insert Head | Delete Head | Memory |
|-----------|---------|--------|-------------|-------------|--------|
| Singly Linked List | `struct{ Val; Next }` | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × node size |
| Doubly Linked List | `struct{ Val; Prev; Next }` | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × 2 pointers |
| Circular List | `struct{ Val; Next }` + Tail | <code>O(n)</code> | <code>O(1)</code> | <code>O(1)</code> | n × node size |
| Slice (for comparison) | `[]T` | <code>O(1)</code> | <code>O(n)</code> | <code>O(n)</code> | Contiguous |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 8:</strong> Linked lists provide flexible <code>O(1)</code> insertion and deletion at known positions but sacrifice random access and cache locality. In Go, prefer slices for most use cases due to superior cache performance and simpler memory layout. Use linked lists only when frequent insertions/deletions at arbitrary positions are required.
{{% /alert %}}
