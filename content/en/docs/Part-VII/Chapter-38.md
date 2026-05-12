---
weight: 71100
title: "Chapter 38: Bit Manipulation"
description: "Bit Manipulation"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>There are 10 types of people in the world: those who understand binary and those who don't.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 39 covers <abbr title="Operations performed directly on individual bits of integers.">bit manipulation</abbr> techniques in Go: <abbr title="Operations performed directly on individual bits of binary numbers.">bitwise</abbr> operators, common tricks, and algorithms that exploit binary representation for efficiency.
{{% /alert %}}

## 39.1. Bitwise Operators

**Definition:** Bitwise operators manipulate individual bits of integers. They are fundamental for low-level optimization, flags, and compact data representation.

**Background & Philosophy:**
The philosophy is mechanical sympathy. High-level languages abstract numbers into base-10 logic. Bit manipulation strips away the abstraction to directly instruct the CPU's ALU (Arithmetic Logic Unit) using native hardware gates (AND, OR, XOR). It trades code readability for maximum execution speed.

**Use Cases:**
Writing network protocol parsers, configuring hardware registers, cryptographic hashing, and compressing 64 boolean flags into a single 64-bit integer using <abbr title="A pattern of bits used to select or modify specific bits within a value.">bitmasks</abbr>.

**Memory Mechanics:**
Bitwise operations execute exclusively inside the CPU registers. They bypass the <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> entirely once the variable is loaded. A `uint64` takes 8 bytes of memory but can store 64 distinct boolean states. An array of 64 `bool` in Go would take 64 bytes (plus slice headers). Using bitmasks heavily compresses memory footprints, making it the supreme choice for memory-constrained embedded systems or massive graph traversal arrays.

### Go Bitwise Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `&` | AND | `5 & 3` | `1` (0101 & 0011 = 0001) |
| `\|` | OR | `5 \| 3` | `7` (0101 \| 0011 = 0111) |
| `^` | XOR | `5 ^ 3` | `6` (0101 ^ 0011 = 0110) |
| `&^` | AND NOT | `5 &^ 3` | `4` (clears bits) |
| `<<` | Left Shift | `1 << 3` | `8` |
| `>>` | Right Shift | `8 >> 2` | `2` |

## 39.2. Common Bit Tricks

### Check if Power of Two

A power of two has exactly one bit set. `n & (n-1)` clears the lowest set bit.

```go
package main

import "fmt"

func isPowerOfTwo(n int) bool {
	return n > 0 && (n&(n-1)) == 0
}

func main() {
	fmt.Println(isPowerOfTwo(16)) // true
	fmt.Println(isPowerOfTwo(18)) // false
}
```

### Count Set Bits (Hamming Weight)

```go
package main

import "fmt"

func countBits(n int) int {
	count := 0
	for n != 0 {
		n &= n - 1 // clear lowest set bit
		count++
	}
	return count
}

func main() {
	fmt.Println(countBits(0b101101)) // 4
}
```

### Get Lowest Set Bit

```go
func lowestSetBit(n int) int {
	return n & -n
}
```

### Swap Without Temporary Variable

```go
func swap(a, b int) (int, int) {
	a = a ^ b
	b = a ^ b
	a = a ^ b
	return a, b
}
```

## 39.3. Bit Masking Applications

### Subset Enumeration

Generate all subsets of a set using bit masks.

```go
package main

import "fmt"

func subsets(nums []int) [][]int {
	n := len(nums)
	var result [][]int
	for mask := 0; mask < (1 << n); mask++ {
		var subset []int
		for i := 0; i < n; i++ {
			if mask&(1<<i) != 0 {
				subset = append(subset, nums[i])
			}
		}
		result = append(result, subset)
	}
	return result
}

func main() {
	fmt.Println(len(subsets([]int{1, 2, 3}))) // 8
}
```

### Toggle Bit

```go
func toggleBit(n, i int) int {
	return n ^ (1 << i)
}

func setBit(n, i int) int {
	return n | (1 << i)
}

func clearBit(n, i int) int {
	return n &^ (1 << i)
}

func isBitSet(n, i int) bool {
	return (n & (1 << i)) != 0
}
```

## 39.4. Decision Matrix

| Use Bit Manipulation When... | Avoid If... |
|------------------------------|-------------|
| Need compact boolean flags | Code readability is more important than micro-optimization |
| Solving subset/combination problems | Operations involve non-integer data |
| Optimizing known bottlenecks | Premature optimization without profiling |
| Working with hardware/Protocol flags | Team unfamiliar with bitwise operations |

### Edge Cases & Pitfalls

- **Sign extension:** Right shift of negative numbers preserves sign bit in Go (arithmetic shift).
- **Overflow:** Left shift can overflow; use `uint` for bit manipulation to avoid sign issues.
- **Precedence:** Bitwise operators have lower precedence than arithmetic; use parentheses.
- **Go's `int` size:** `int` is 32 or 64 bits depending on architecture; use explicit sizes when needed.

## 39.5. Quick Reference

| Operation | Expression | Use Case |
|-----------|-----------|----------|
| Power of two | `(n & (n-1)) == 0` | Capacity checks |
| Count bits | `n & (n-1)` loop | Hamming distance |
| Isolate lowest bit | `n & -n` | Fenwick tree |
| Clear lowest bit | `n & (n-1)` | Bit counting |
| Toggle bit | `n ^ (1 << i)` | Flag flipping |
| Subset enumeration | `for mask := 0; mask < (1<<n); mask++` | Combinatorics |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 37:</strong> Bit manipulation provides compact and efficient solutions for specific problem classes. Master the core tricks: power-of-two checks, bit counting, and subset enumeration. In Go, prefer `uint` for bitwise operations to avoid sign extension surprises, and always prioritize code clarity over clever bit tricks unless performance is critical.
{{% /alert %}}

## See Also

- [Chapter 28: Vector, Matrix, and Tensor Operations](/docs/Part-VII/Chapter-28/)
- [Chapter 33: Polynomial and FFT](/docs/Part-VII/Chapter-33/)
- [Chapter 42: Modern Algorithmic Thinking](/docs/Part-VIII/Chapter-42/)
