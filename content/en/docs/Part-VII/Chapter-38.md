---
weight: 71100
title: "Chapter 38: Bit Manipulation"
description: "Bit Manipulation"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>There are 10 types of people in the world: those who understand binary and those who don't.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 38 covers <abbr title="Operations performed directly on individual bits of integers.">bit manipulation</abbr> techniques in Go. Includes bitwise operators and binary efficiency algorithms.
{{% /alert %}}

## 39.1. Bitwise Operators

**Definition:** Operators manipulate individual integer bits. Fundamental for optimization, flags, and data compression.

**Background:**
Mechanical sympathy achieved. CPU ALU uses hardware gates (AND, OR, XOR) directly. High-level abstraction removed for execution speed.

**Use Cases:**
Network protocol parsers. Hardware register configuration. Cryptographic hashing. Storing 64 flags in one 64-bit integer using <abbr title="A pattern of bits used to select or modify specific bits within a value.">bitmasks</abbr>.

**Memory Mechanics:**
Operations occur in CPU registers. RAM bypassed during execution. `uint64` uses 8 bytes for 64 boolean states. Standard `bool` array uses 64 bytes. Memory footprints compressed for embedded systems and graph traversal.

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

Power of two has one bit set. `n & (n-1)` clears it.

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

Generate all subsets using bit masks.

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
| Compact boolean flags needed | Readability prioritized over optimization |
| Subset/combination problems | Data is non-integer |
| Bottlenecks identified | Profiling data is missing |
| Protocol flags used | Team lacks bitwise expertise |

### Edge Cases & Pitfalls

- **Sign extension:** Go uses arithmetic shift for negative signed integers.
- **Overflow:** Left shift overflows. Use `uint` types.
- **Precedence:** Use parentheses. Bitwise operators rank lower than arithmetic.
- **Int size:** Platform dependent (32/64 bit). Use explicit sizes.

### Anti-Patterns

- **Signed integers for bitwise:** Arithmetic shifts cause sign extension. Use `uint` or `uint64`.
- **Operator precedence errors:** `&`, `|`, `^` rank below `+`, `-`, `==`. Always wrap in parentheses.
- **Shifting beyond word size:** Shifting `uint64` by 64+ causes panics or zeroed results. Mask shift counts.

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
<strong>Summary Chapter 38:</strong> Bit manipulation enables efficient solutions. Tricks include power-of-two checks, bit counting, and subset enumeration. Use `uint` in Go to avoid sign extension. Prioritize clarity unless performance is critical.
{{% /alert %}}

## See Also

- [Chapter 28: Vector, Matrix, and Tensor Operations](/docs/part-vii/chapter-28/)
- [Chapter 33: Polynomial and FFT](/docs/part-vii/chapter-33/)
- [Chapter 42: Modern Algorithmic Thinking](/docs/part-viii/chapter-42/)
