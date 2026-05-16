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
<strong>"<em>Algorithms are the backbone of modern computing. Without them, even the most powerful hardware would be rendered useless.</em>" — Donald Knuth</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 33 covers polynomials and Fast Fourier Transform (FFT). Go lacks native FFT. Use `math/cmplx` or external libraries.
{{% /alert %}}

## 33.1. Polynomial Representation

**Definition:** Polynomial of <abbr title="The number of edges incident to a vertex.">degree</abbr> n is slice of coefficients: `[a₀, a₁, ..., aₙ]`.

**Mechanics:**
Dual representation exists: coefficients or points. Multiplying points is <code>O(n)</code>. Multiplying coefficients is <code>O(n^2)</code>. FFT converts between them in <code>O(n log n)</code>. Enables fast multiplication.

**Use Cases:**
Digital signal processing. Audio/image compression. Quantum mechanics. Large number multiplication.

**Memory Mechanics:**
FFT uses butterfly operation. Bit-reversal permutation required. Non-contiguous access thrashes <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr>. Pre-calculate twiddle factors. Optimize memory strides for L1/L2 cache.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Evaluation (Horner's) | <code>O(n)</code> | Optimal evaluation |
| Addition | <code>O(n)</code> | Element-wise |
| Naive Multiplication | <code>O(n^2)</code> | Mathematical convolution |
| FFT Multiplication | <code>O(n log n)</code> | DFT-based execution |

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
    p := Polynomial{1, -3, 2}
    fmt.Println("P(2) =", p.Evaluate(2))
    q := Polynomial{1, 1}
    fmt.Println("P * Q =", multiplyNaive(p, q))
}
```

{{% alert icon="📌" context="warning" %}}
Go lacks operator overloading. Use explicit method receivers. Slice representation is more efficient than struct with pointers.
{{% /alert %}}

### Decision Matrix

| Use Slice Representation When... | Avoid If... |
|----------------------|------------------|
| Degrees small to medium (< 10⁴) | Sparse polynomials. Use map. |
| Non-zero coefficients dominant | Massive sparse degree. |

## 33.2. FFT and Convolution

**Definition:** Fast Fourier Transform (FFT) computes DFT in <code>O(n log n)</code>. Enables polynomial multiplication via convolution.

### Operations & Complexity

| Algorithm | Time | Space | Description |
|-----------|------|-------|------------|
| Naive DFT | <code>O(n²)</code> | <code>O(n)</code> | Direct execution |
| Cooley-Tukey FFT | <code>O(n log n)</code> | <code>O(n)</code> | Recursive method |
| Iterative FFT | <code>O(n log n)</code> | <code>O(1)</code> | In-place execution |
| Bluestein | <code>O(n log n)</code> | <code>O(n)</code> | Arbitrary input size |

### Decision Matrix

| Use FFT When... | Avoid If... |
|--------------------|------------------|
| Large polynomial degree (> 100) | Small degree. Naive is faster. |
| Signal convolution | Flawless integer precision required. Rounding error risk. |

### Edge Cases & Pitfalls

- **Power-of-2 constraint:** Pad input with trailing zeros. Use Bluestein for arbitrary sizes.
- **Floating point error:** Error margin ~1e-9. Round outcome for integers.
- **Inverse scaling:** Divide results by n after inverse FFT.

## 33.3. Polynomial Interpolation

**Definition:** Find degree n polynomial through n+1 points.

### Operations & Complexity

| Method | Time | Space | Description |
|--------|------|-------|------------|
| Lagrange | <code>O(n^2)</code> | <code>O(n)</code> | Direct formula |
| Newton | <code>O(n^2)</code> | <code>O(n)</code> | Incremental buildup |
| FFT Interpolation | <code>O(n log n)</code> | <code>O(n)</code> | Roots of unity evaluation |

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
Lagrange is stable for few points. Use divided differences or barycentric interpolation for many points.
{{% /alert %}}

### Decision Matrix

| Use Lagrange When... | Avoid If... |
|-------------------------|------------------|
| Point count low (< 50) | Point count high. Runge phenomenon risk. |
| Single point evaluation | Massive point count evaluation. |

### Anti-Patterns

- **Input size not power-of-2:** Cooley-Tukey requires it. Zero-pad coefficient array.
- **Skip inverse FFT scaling:** Division by n mandatory. Omitting yields n-times larger results.
- **Float64 for integer convolution:** Rounding errors occur. Round to nearest integer. Use NTT for exact results.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Polynomial | `[]float64` | <code>O(n)</code> | <code>O(n)</code> | Coefficient storage |
| Horner evaluation | func | <code>O(n)</code> | <code>O(1)</code> | Fast evaluation |
| Naive multiply | loop | <code>O(n²)</code> | <code>O(n)</code> | Small degrees |
| FFT multiply | FFT | <code>O(n log n)</code> | <code>O(n)</code> | Large degrees |
| Interpolation | func | <code>O(n²)</code> | <code>O(n)</code> | Curve fitting |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 33:</strong> Polynomials use coefficient slices. Horner evaluation is <code>O(n)</code>. FFT enables <code>O(n log n)</code> multiplication. Lagrange performs <code>O(n^2)</code> interpolation. Use FFT for large degrees.
{{% /alert %}}

## See Also

- [Chapter 28: Vector, Matrix, and Tensor Operations](/docs/part-vii/chapter-28/)
- [Chapter 34: String Matching Algorithms](/docs/part-vii/chapter-34/)
- [Chapter 38: Bit Manipulation](/docs/part-vii/chapter-38/)
