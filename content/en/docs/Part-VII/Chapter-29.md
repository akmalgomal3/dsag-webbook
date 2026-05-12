---
weight: 70100
title: "Chapter 29: Vector, Matrix, and Tensor Operations"
description: "Vector, Matrix, and Tensor Operations"
icon: "article"
date: "2024-08-24T23:42:45+07:00"
lastmod: "2024-08-24T23:42:45+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Linear algebra is the mathematics of data. Matrices and vectors are the language in which modern algorithms speak.</em>" : Gilbert Strang</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 29 covers vector, matrix, and tensor operations with <abbr title="Code style considered standard and natural for Go">idiomatic Go</abbr> implementations utilizing slices and `gonum`.
{{% /alert %}}

## 29.1. Vector Operations

**Definition:** A vector is a one-dimensional <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> representing a directed magnitude. Basic operations include addition, scalar multiplication, <abbr title="An operation returning the scalar product of two vectors">dot product</abbr>, and <abbr title="An operation on vectors producing a perpendicular vector">cross product</abbr>.

**Background & Philosophy:**
The philosophy is representing data mathematically. Instead of isolated variables, numbers are grouped into spatial structures (Vectors, Matrices), enabling batch transformations that hardware GPUs and <abbr title="Single Instruction Multiple Data - parallel processing technique.">SIMD</abbr> CPU instructions are structurally designed to optimize flawlessly.

**Use Cases:**
Core foundation for 3D Graphics programming, deep learning backpropagation, and PageRank algorithms determining internet search results.

**Memory Mechanics:**
Vectors map perfectly to 1D slices in Go. Because `[]float64` is a strictly <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> block of <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr>, operations like <abbr title="An operation returning the scalar product of two vectors">dot product</abbr> exhibit perfect <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. The CPU prefetcher can rapidly stream the bytes into the L1 <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Addition | <code>O(n)</code> | Element-wise |
| <abbr title="An operation returning the scalar product of two vectors">Dot Product</abbr> | <code>O(n)</code> | Σ(aᵢ × bᵢ) |
| Norm (L2) | <code>O(n)</code> | √(Σaᵢ²) |
| <abbr title="An operation on vectors producing a perpendicular vector">Cross Product</abbr> | <code>O(1)</code> | Specific to 3D |

### Pseudocode

```text
AddVectors(a, b):
    if length(a) != length(b):
        error "dimension mismatch"
    result = new array of length(a)
    for i from 0 to length(a)-1:
        result[i] = a[i] + b[i]
    return result

DotProduct(a, b):
    if length(a) != length(b):
        error "dimension mismatch"
    sum = 0
    for i from 0 to length(a)-1:
        sum += a[i] * b[i]
    return sum

Norm(a):
    sum = 0
    for each v in a:
        sum += v * v
    return sqrt(sum)
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math"
)

func addVectors(a, b []float64) []float64 {
    if len(a) != len(b) {
        panic("dimension mismatch")
    }
    result := make([]float64, len(a))
    for i := range a {
        result[i] = a[i] + b[i]
    }
    return result
}

func dotProduct(a, b []float64) float64 {
    if len(a) != len(b) {
        panic("dimension mismatch")
    }
    var sum float64
    for i := range a {
        sum += a[i] * b[i]
    }
    return sum
}

func norm(a []float64) float64 {
    var sum float64
    for _, v := range a {
        sum += v * v
    }
    return math.Sqrt(sum)
}

func main() {
    a := []float64{1, 2, 3}
    b := []float64{4, 5, 6}
    fmt.Println("Add:", addVectors(a, b))
    fmt.Println("Dot:", dotProduct(a, b))
    fmt.Println("Norm:", norm(a))
}
```

{{% alert icon="📌" context="warning" %}}
Go lacks operator overloading. Define explicit functions for every vector operation. Consider using `gonum.org/v1/gonum/floats` for large-scale vector manipulations.
{{% /alert %}}

### Decision Matrix

| Use Slices When... | Avoid If... |
|----------------------|------------------|
| Dimensions are small to medium (< 10⁶) | Operations are complex matrices (use gonum) |
| Using custom logic or sparse data | Relying on highly optimized BLAS/LAPACK |

### Edge Cases & Pitfalls

- **Dimension mismatch:** Always rigorously validate slice lengths.
- **NaN propagation:** Carefully handle and mitigate undefined values.
- **Precision loss:** For massive vectors, implement Kahan summation to prevent float drift.

## 29.2. Matrix Operations

**Definition:** A matrix is a two-dimensional array. Critical operations include transposition, multiplication, determinant calculation, and inversion.

**Memory Mechanics:**
In Go, matrices are often modeled naively as `[][]float64`, which creates `V` slice headers scattered across the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr>. High-performance numerical packages like `gonum` use a 1D flat slice `[]float64` for a matrix and manually index via `stride * row + col`. This ensures strict <abbr title="Memory blocks allocated in a single unbroken sequence of addresses.">contiguous</abbr> memory layout, enabling the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> to prefetch matrix rows efficiently and preventing <abbr title="Automatic memory management that attempts to reclaim memory occupied by objects no longer in use.">GC</abbr> fragmentation.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Transpose | <code>O(n²)</code> | Rows ↔ Columns |
| Matrix Multiply | <code>O(n³)</code> naive, <code>O(n^2.81)</code> Strassen | Standard multiplication |
| Determinant | <code>O(n³)</code> | LU decomposition |
| Inverse | <code>O(n³)</code> | Gauss-Jordan elimination |

### Idiomatic Go Implementation

`gonum.org/v1/gonum/mat` serves as the de facto standard <abbr title="A collection of precompiled routines that a program can use.">library</abbr> for linear algebra in Go. Do not implement matrix operations from scratch unless specifically for educational purposes.

### Decision Matrix

| Use Gonum When... | Implement Manually When... |
|----------------------|------------------------------|
| Working with dense matrices and standard operations | Building custom sparse matrices |
| Needing SVD or eigenvalue decomposition | Running under extremely strict memory constraints |

### Edge Cases & Pitfalls

- **Singular matrix:** Inverses do not exist; you must consistently check for errors.
- **Floating-point error:** Never perform a strict `==` check; always use an epsilon delta.
- **Memory layout:** Go slices are row-major. Maintain an awareness of cache locality.

## 29.3. Tensors and Multidimensional Data

**Definition:** A tensor generalizes a matrix to arbitrary dimensions. Within Machine Learning, a rank-3 tensor frequently represents a batch of images (B × H × W × C).

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Tensor Add | <code>O(n)</code> | Element-wise addition |
| Tensor Contraction | <code>O(n^k)</code> | Sum over specific indices |
| Reshape | <code>O(1)</code> | Viewing memory without a copy |

Rank-3 tensors formulated via nested slices in Go carry heavy <abbr title="A variable that stores a memory address.">pointer</abbr> overhead. For significantly large tensors, utilize a flat 1D slice with manual indexing: `flat[i*H*W + j*W + k]`.

### Decision Matrix

| Use Nested Slices When... | Use Flat Slices When... |
|-----------------------------|---------------------------|
| Dimensions are small and intuitive access matters | Tensors are massive, focusing purely on performance |
| Rapidly prototyping | Facilitating GPU transfers or SIMD optimizations |

### Edge Cases & Pitfalls

- **Nil slices:** Always verify `len(slice) > 0` before attempting to access `slice[0]`.
- **Jagged arrays:** Go slices of slices are not inherently uniform. Mathematical tensors *must* be uniform.
- **GC pressure:** Deeply nested slices yield countless individual objects. Flat slices dramatically ease Garbage Collection.

## 29.4. Matrix Computation Optimization

**Definition:** Techniques strategically designed to accelerate matrix operations via leveraging cache locality, data blocking, and explicit parallelization.

### Operations & Complexity

| Technique | Speedup | Description |
|--------|---------|------------|
| Loop reordering | 2-10x | Dramatically enhances cache locality |
| Block matrix | 2-5x | Ensure operations fit nicely within L1/L2 caches |
| Goroutine parallel | p× (cores) | Apply row-wise decomposition |
| Strassen | 0.8-2x | Theoretical limit, rarely practical for everyday n |

A loop ordering of `i-k-j` proves significantly faster than `i-j-k` specifically due to <abbr title="The tendency of a processor to access memory addresses that are near each other.">cache</abbr> locality on matrix b's rows. Thoroughly profile your code prior to declaring a complete optimization.

### Decision Matrix

| Use Parallel When... | Avoid If... |
|-------------------------|------------------|
| The matrix exceeds 256×256 dimensions | The matrix is tiny (goroutine overhead kills performance) |
| The problem is CPU-bound on a dense matrix | You have a sparse matrix (leverage CSR/CSC arrays instead) |

### Edge Cases & Pitfalls

- **False sharing:** Strongly segregate data chunks by at least a few cache lines (e.g., 64 bytes).
- **Load imbalance:** Rely upon a dynamic task queue for heavily non-uniform matrix structures.
- **Numerical stability:** Aggressive parallel summation can potentially aggravate floating-point inaccuracies.

## Quick Reference

| Name | Go Type | Complexity | Access | Use Case |
|------|---------|------------|--------|----------|
| Vector | `[]float64` | <code>O(1)</code> access | varies | 1D Data |
| Matrix | `[][]float64` | <code>O(1)</code> access | varies | 2D Data |
| Tensor | `[][][]float64` | <code>O(1)</code> access | varies | ML batching |
| Dense Matrix | `[]float64` flat | <code>O(1)</code> access | varies | Heavy linear algebra |
| Sparse | `map[int]map[int]float64` | <code>O(1)</code> access avg | varies | Graphs, NLP sparse arrays |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 29:</strong> This chapter covers vector, matrix, and tensor operations with idiomatic Go implementations. Utilize standard slices for vectors, the `gonum` package for large-scale linear algebra, nested slices for small-scale tensors, and manually indexed flat slices for large tensors. Parallelizing code with goroutines becomes highly effective when matrix dimensions exceed 256×256.
{{% /alert %}}

## See Also

- [Chapter 30: Parallel and Distributed Algorithms](/docs/Part-VII/Chapter-30/)
- [Chapter 34: Polynomial and FFT](/docs/Part-VII/Chapter-34/)
- [Chapter 39: Bit Manipulation](/docs/Part-VII/Chapter-39/)
