---
weight: 70100
title: "Chapter 28: Vector, Matrix, and Tensor Operations"
description: "Vector, Matrix, and Tensor Operations"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Linear algebra is the mathematics of data. Matrices and vectors are the language in which modern algorithms speak.</em>" — Gilbert Strang</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 28 covers vector, matrix, and tensor operations. Implementations use Go slices and `gonum`.
{{% /alert %}}

## 28.1. Vector Operations

**Definition:** Vector is 1D array. Represents directed magnitude. Operations: addition, scalar multiplication, dot product, cross product.

**Background & Philosophy:**
Vectors group numbers into spatial structures. Enables batch transformations. GPUs and SIMD instructions process these efficiently.

**Use Cases:**
3D Graphics. Deep learning backpropagation. PageRank algorithms.

**Memory Mechanics:**
Vectors map to 1D Go slices. `[]float64` uses contiguous RAM. Dot product has perfect spatial locality. CPU prefetcher streams bytes into L1 cache.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Addition | <code>O(n)</code>$ | Element-wise operation |
| Dot Product | <code>O(n)</code>$ | $\sum(a_i \times b_i)$ |
| Norm (L2) | <code>O(n)</code>$ | $\sqrt{\sum a_i^2}$ |
| Cross Product | <code>O(1)</code>$ | 3D specific operation |

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
Go lacks operator overloading. Define explicit functions. Use `gonum.org/v1/gonum/floats` for large-scale work.
{{% /alert %}}

### Decision Matrix

| Use Slices When... | Avoid If... |
|----------------------|------------------|
| Small to medium dimensions ($< 10^6$) | Matrix operations are complex: use gonum |
| Custom logic or sparse data needed | BLAS/LAPACK optimization required |

### Edge Cases & Pitfalls

- **Dimension mismatch:** Validate slice lengths.
- **NaN propagation:** Undefined values break results.
- **Precision loss:** Large vectors need Kahan summation. Prevents float drift.

## 28.2. Matrix Operations

**Definition:** Matrix is 2D array. Operations: transposition, multiplication, determinant, inversion.

**Memory Mechanics:**
Nested slices `[][]float64` scatter headers across heap. `gonum` uses flat `[]float64`. Indexing via `stride * row + col`. Contiguous layout allows efficient CPU cache prefetching. Prevents GC fragmentation.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Transpose | <code>O(n^2)</code>$ | Rows ↔ Columns |
| Matrix Multiply | <code>O(n^3)</code>$ | Standard multiplication |
| Determinant | <code>O(n^3)</code>$ | LU decomposition |
| Inverse | <code>O(n^3)</code>$ | Gauss-Jordan elimination |

### Idiomatic Go Implementation

Use `gonum.org/v1/gonum/mat`. It is the de-facto external library for linear algebra in Go and is production-tested.

### Decision Matrix

| Use Gonum When... | Implement Manually When... |
|----------------------|------------------------------|
| Dense matrices and standard ops used | Custom sparse matrices required |
| SVD or eigenvalue decomposition needed | Extreme memory constraints exist |

### Edge Cases & Pitfalls

- **Singular matrix:** Inverses do not exist. Check errors consistently.
- **Floating-point error:** Avoid `==`. Use epsilon delta.
- **Memory layout:** Go slices are row-major. Maintain cache locality.

## 28.3. Tensors and Multidimensional Data

**Definition:** Tensor generalizes matrix to arbitrary dimensions. Rank-3 tensor represents image batches (B × H × W × C).

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Tensor Add | <code>O(n)</code>$ | Element-wise addition |
| Tensor Contraction | <code>O(n^k)</code>$ | Sum over specific indices |
| Reshape | <code>O(1)</code>$ | View memory without copy |

Nested slices cause pointer overhead. Large tensors should use flat 1D slice. Indexing: `flat[i*H*W + j*W + k]`.

### Decision Matrix

| Use Nested Slices When... | Use Flat Slices When... |
|-----------------------------|---------------------------|
| Small dimensions: intuitive access | Massive tensors: performance focus |
| Prototyping rapidly | GPU transfers or SIMD required |

### Edge Cases & Pitfalls

- **Nil slices:** Verify `len(slice) > 0` before access.
- **Jagged arrays:** Slices of slices can be non-uniform. Tensors must be uniform.
- **GC pressure:** Nested slices create many objects. Flat slices ease Garbage Collection.

## 28.4. Matrix Computation Optimization

**Definition:** Strategies to accelerate matrix operations. Uses cache locality, blocking, and parallelization.

### Operations & Complexity

| Technique | Speedup | Description |
|--------|---------|------------|
| Loop reordering | 2-10x | Enhances cache locality |
| Block matrix | 2-5x | Fits operations in L1/L2 |
| Parallelization | $p \times$ cores | Row-wise decomposition |
| Strassen | 0.8-2x | Rare practical utility |

Loop order `i-k-j` is faster than `i-j-k`. Optimizes cache locality on second matrix rows. Profile before final optimization.

### Decision Matrix

| Use Parallel When... | Avoid If... |
|-------------------------|------------------|
| Dimensions exceed 256×256 | Tiny matrix: goroutine overhead |
| CPU-bound on dense matrix | Sparse matrix: use CSR/CSC |

### Edge Cases & Pitfalls

- **False sharing:** Segregate data by cache lines (64 bytes).
- **Load imbalance:** Use dynamic task queues for non-uniform structures.
- **Numerical stability:** Parallel summation increases float inaccuracies.

### Anti-Patterns

- **Jagged slices for performance:** Creates pointer-chasing overhead. Use flat `[]float64`.
- **Strict float equality:** Arithmetic accumulates error. Use `math.Abs(a-b) < epsilon`.
- **Ignoring gonum:** Manual implementations are error-prone. Use established libraries.

## Quick Reference

| Name | Go Type | Complexity | Access | Use Case |
|------|---------|------------|--------|----------|
| Vector | `[]float64` | <code>O(1)</code>$ | . | 1D Data |
| Matrix | `[][]float64` | <code>O(1)</code>$ | . | 2D Data |
| Tensor | `[][][]float64` | <code>O(1)</code>$ | . | ML batching |
| Dense Matrix | `[]float64` flat | <code>O(1)</code>$ | . | Linear algebra |
| Sparse | `map[int]map[int]float64` | <code>O(1)</code>$ avg | . | Graphs, NLP |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 28:</strong> Vectors use standard slices. Matrices use `gonum` for scale. Tensors use flat slices for performance. Parallelize with goroutines for dimensions above 256×256.
{{% /alert %}}

## See Also

- [Chapter 29: Parallel and Distributed Algorithms](/docs/part-vii/chapter-29/)
- [Chapter 33: Polynomial and FFT](/docs/part-vii/chapter-33/)
- [Chapter 38: Bit Manipulation](/docs/part-vii/chapter-38/)
