---
weight: 70600
title: "Chapter 33: Polynomial and FFT"
description: "Polynomial and FFT"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Algorithms are the backbone of modern computing. Without them, even the most powerful hardware would be rendered useless.</em>" : Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 34 explores polynomials and the Fast Fourier Transform (FFT). Go's stdlib lacks a native FFT; utilize `math/cmplx` for complex operations or rely on external libraries.
{{% /alert %}}

## 34.1. Polynomial Representation

**Definition:** A polynomial of <abbr title="The number of edges incident to a vertex.">degree</abbr> n is gracefully represented as a slice of coefficients: `[a₀, a₁, ..., aₙ]`.

**Background & Philosophy:**
The philosophy is the dual representation of data. A polynomial can be represented either by its coefficients or by its evaluated points. Multiplying coefficients takes <code>O(n^2)</code> time, but multiplying evaluated points takes <code>O(n)</code> time. FFT translates coefficients into points in <code>O(n log n)</code>, enabling fast multiplication.

**Use Cases:**
Digital signal processing (audio/image compression), quantum mechanics, and multiplying incredibly large numbers (e.g., 100,000 digits) efficiently.

**Memory Mechanics:**
FFT's memory access pattern is governed by the "butterfly" operation, which intertwines elements mathematically using a bit-reversal permutation. This creates a highly <abbr title="Memory blocks allocated in fragmented, separate locations.">non-contiguous</abbr> memory read pattern that brutally thrashes the <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr> if implemented naively. High-performance FFT libraries pre-calculate and cache the sine/cosine "twiddle factors" into an array and heavily optimize memory strides to keep data trapped in the L1/L2 caches.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Evaluation (Horner's) | <code>O(n)</code> | Highly optimal |
| Naive Evaluation | <code>O(n^2)</code> | Features repetitive exponentiation |
| Addition | <code>O(n)</code> | Strict element-wise addition |
| Naive Multiplication | <code>O(n^2)</code> | Standard mathematical convolution |
| FFT Multiplication | <code>O(n log n)</code> | Rapid DFT-based execution |

### Pseudocode

```text
EvaluatePolynomial(p, x):
    result = 0
    for i from length(p)-1 down to 0:
        result = result * x + p[i]
    return result

AddPolynomials(a, b):
    maxLen = max(length(a), length(b))
    result = new array of size maxLen initialized to 0
    for i from 0 to maxLen-1:
        if i < length(a): result[i] += a[i]
        if i < length(b): result[i] += b[i]
    return result

MultiplyNaive(a, b):
    result = new array of size length(a)+length(b)-1 initialized to 0
    for i from 0 to length(a)-1:
        for j from 0 to length(b)-1:
            result[i+j] += a[i] * b[j]
    return result
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

// Polynomials are strictly represented as coefficients [a0, a1, a2, ...]
type Polynomial []float64

func (p Polynomial) Evaluate(x float64) float64 {
    result := 0.0
    for i := len(p) - 1; i >= 0; i-- {
        result = result*x + p[i]
    }
    return result
}

func (p Polynomial) Add(other Polynomial) Polynomial {
    maxLen := len(p)
    if len(other) > maxLen {
        maxLen = len(other)
    }
    result := make(Polynomial, maxLen)
    for i := 0; i < maxLen; i++ {
        if i < len(p) {
            result[i] += p[i]
        }
        if i < len(other) {
            result[i] += other[i]
        }
    }
    return result
}

func multiplyNaive(a, b Polynomial) Polynomial {
    result := make(Polynomial, len(a)+len(b)-1)
    for i := range a {
        for j := range b {
            result[i+j] += a[i] * b[j]
        }
    }
    return result
}

func main() {
    p := Polynomial{1, -3, 2} // Represents 2x² - 3x + 1
    fmt.Println("P(2) =", p.Evaluate(2))
    q := Polynomial{1, 1} // Represents x + 1
    fmt.Println("P * Q =", multiplyNaive(p, q))
}
```

{{% alert icon="📌" context="warning" %}}
Go inherently lacks operator overloading. Always employ explicit method receivers for polynomial operations. A flat slice representation operates much more efficiently than a struct relying on pointers.
{{% /alert %}}

### Decision Matrix

| Use Slice Representation When... | Avoid If... |
|----------------------|------------------|
| Degrees are small to medium (< 10⁴) | You are managing sparse polynomials (use a map instead) |
| All coefficients are fundamentally non-zero | The degree is massive yet remains highly sparse |

### Edge Cases & Pitfalls

- **Leading zeros:** Rigorously trim trailing zeros in the array to prevent generating a false, artificially high degree.
- **Zero polynomial:** It is represented by `[]float64{0}`, not a completely empty slice `nil`.

## 34.2. FFT and Convolution

**Definition:** The Fast Fourier Transform (FFT) calculates the Discrete Fourier Transform with a complexity of <code>O(n log n)</code>. It is heavily utilized for executing polynomial multiplication via convolution.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| Naive DFT | <code>O(n²)</code> | <code>O(n)</code> | Direct mathematical execution |
| Cooley-Tukey FFT | <code>O(n log n)</code> | <code>O(n)</code> | Standard recursive method |
| Iterative FFT | <code>O(n log n)</code> | <code>O(1)</code> in-place | Memory-efficient in-place execution |
| Bluestein | <code>O(n log n)</code> | <code>O(n)</code> | Supports arbitrary input sizes |

Go's stdlib does not furnish an FFT algorithm. A comprehensive implementation demands roughly 100 lines of code. For production integrity, depend on libraries like `github.com/mjibson/go-dsp` or `github.com/cpmech/fftx`.

### Decision Matrix

| Use FFT When... | Avoid If... |
|--------------------|------------------|
| Multiplying massive polynomials (degree > 100) | Dealing with very small degrees (naive is far quicker) |
| Running signal convolutions | An exact, flawless integer result is heavily required (due to rounding errors) |

### Edge Cases & Pitfalls

- **Non-power-of-2 constraints:** Pad the input with trailing zeros. For completely arbitrary sizes, integrate Bluestein's or Rader's algorithms.
- **Floating point error:** The mathematical outcome of an FFT may harbor an error margin of ~1e-9. Actively round the outcome to achieve pristine integer results.
- **Inverse scaling oversight:** Never forget to vigorously divide the outcome by n immediately following the inverse FFT phase.

## 34.3. Polynomial Interpolation

**Definition:** Interpolation derives a polynomial of <abbr title="The number of edges incident to a vertex.">degree</abbr> n that intersects n+1 designated points.

### Operations & Complexity

| Method | Time | Space | Description |
|--------|------|-------|------------|
| Lagrange | <code>O(n^2)</code> | <code>O(n)</code> | Operates via a direct mathematical formula |
| Newton Divided Diff | <code>O(n^2)</code> | <code>O(n)</code> | Facilitates an incremental buildup |
| FFT Interpolation | <code>O(n log n)</code> | <code>O(n)</code> | Evaluated at the roots of unity |

### Pseudocode

```text
LagrangeInterpolation(x, y, xi):
    n = length(x)
    result = 0
    for i from 0 to n-1:
        term = y[i]
        for j from 0 to n-1:
            if i != j:
                term *= (xi - x[j]) / (x[i] - x[j])
        result += term
    return result
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func lagrangeInterpolation(x []float64, y []float64, xi float64) float64 {
    n := len(x)
    result := 0.0
    for i := 0; i < n; i++ {
        term := y[i]
        for j := 0; j < n; j++ {
            if i != j {
                term *= (xi - x[j]) / (x[i] - x[j])
            }
        }
        result += term
    }
    return result
}

func main() {
    x := []float64{0, 1, 2}
    y := []float64{1, 3, 2}
    fmt.Println("P(1.5) =", lagrangeInterpolation(x, y, 1.5))
}
```

{{% alert icon="📌" context="warning" %}}
Lagrange interpolation holds remarkable stability solely for a sparse number of equidistant points. For a large volume of points or Chebyshev nodes, transition immediately to divided differences or barycentric interpolation.
{{% /alert %}}

### Decision Matrix

| Use Lagrange When... | Avoid If... |
|-------------------------|------------------|
| The volume of points is tiny (< 50) | The volume of points is large (triggers the Runge phenomenon) |
| Evaluating a single specific coordinate | Evaluating a massive number of points (evaluate via basis polynomials instead) |

### Edge Cases & Pitfalls

- **Runge phenomenon:** Interpolation over many equidistant nodes causes oscillation. Switch to Chebyshev nodes.
- **Identical x coordinates:** Evaluating two distinct points sharing an identical x coordinate forces an undefined mathematical outcome (division by zero).

### Anti-Patterns

- **Input size not a power of two:** Cooley-Tukey FFT requires power-of-two input lengths. Always zero-pad the coefficient array to the next power of two before calling FFT.
- **Forgetting inverse FFT scaling:** The inverse FFT must divide all output values by n. Omitting this produces results that are n times too large.
- **Using float64 for exact integer convolution:** FFT-based polynomial multiplication introduces floating-point rounding errors. Round results to the nearest integer and verify; for exact results, use NTT (Number Theoretic Transform) instead.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Polynomial | `[]float64` | <code>O(n)</code> | <code>O(n)</code> | Standard coefficient storage |
| Horner evaluation | func | <code>O(n)</code> | <code>O(1)</code> | Hyper-fast value evaluation |
| Naive multiply | nested loop | <code>O(n²)</code> | <code>O(n)</code> | Handling tiny polynomial degrees |
| FFT multiply | <code>O(n log n)</code> | <code>O(n log n)</code> | <code>O(n)</code> | Handling massive polynomial degrees |
| Interpolation | func | <code>O(n²)</code> | <code>O(n)</code> | Precise data curve fitting |
| DFT | <code>O(n²)</code> | <code>O(n²)</code> | <code>O(n)</code> | Thorough signal analysis |
| FFT | custom/3rd party | <code>O(n log n)</code> | <code>O(n)</code> | Extreme high-speed transformation |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 33:</strong> This chapter dissects polynomial representation employing coefficient slices, hyper-fast Horner evaluation occurring in <code>O(n)</code>, and both naive <code>O(n^2)</code> and advanced FFT <code>O(n log n)</code> multiplications, alongside Lagrange interpolation. Rely on FFT strictly for massive <abbr title="The number of edges incident to a vertex.">degree</abbr> polynomial multiplications and Horner for rapid evaluations.
{{% /alert %}}

## See Also

- [Chapter 28: Vector, Matrix, and Tensor Operations](/docs/part-vii/chapter-28/)
- [Chapter 34: <abbr title="Finding occurrences of a pattern within a text">String Matching</abbr> Algorithms](/docs/part-vii/chapter-34/)
- [Chapter 38: Bit Manipulation](/docs/part-vii/chapter-38/)
