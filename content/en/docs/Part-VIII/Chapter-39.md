---
weight: 80100
title: "Chapter 39: Origins of Algorithms"
description: "Origins of Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The question of whether a computer can think is no more interesting than the question of whether a submarine can swim.</em>" — Edsger Dijkstra</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 39 covers algorithm origins: Babylonian tablets to Euclid. Algorithmic thinking exists since millennia.
{{% /alert %}}

## 39.1. Definition

**Algorithm:** Finite sequence of well-defined instructions. Solves specific problems. Name derives from Persian mathematician <abbr title="A Persian polymath who lived c. 780–850 CE, considered the father of algebra.">al-Khwarizmi</abbr>.

**Philosophy:** Procedural determinism. Breaks complex problems into mechanical, unambiguous steps. Guarantees results regardless of executor intelligence.

**Use Cases:** Translates human intent into mathematical models. Enabled early astronomy, tax collection, and engineering.

**Memory Mechanics:** Ancient "memory" used clay tablets, abacuses, or human short-term memory. Human working memory limits forced trackers for few variables. Modern equivalent: <code>O(1)</code> space complexity.

### The Three Pillars

| Pillar | Requirement | Example |
|--------|-------------|---------|
| Finiteness | Must terminate | Euclid's GCD stops at zero remainder |
| Definiteness | Unambiguous steps | "Divide A by B" |
| Effectiveness | Executable operations | Arithmetic, assignment |

## 39.2. Ancient Algorithms (Before 500 CE)

### Babylonian Mathematics (c. 1800 BCE)

Babylonians used iterative approximation for square roots. Precursor to Newton's method.

```text
To find √A:
1. Guess x
2. Compute y = A / x
3. Update x = (x + y) / 2
4. Repeat until x ≈ y
```

### Euclid's Algorithm (c. 300 BCE)

**Definition:** Finds greatest common divisor (GCD). Replaces larger number with remainder of division by smaller.

**Philosophy:** Mathematical reduction. `GCD(A, B) == GCD(B, A mod B)`. Shrinks problem space exponentially.

**Use Cases:** RSA cryptography key generation. Simplifying fractions in computer algebra.

**Memory Mechanics:** Requires <code>O(1)</code> memory. Tracks two integer variables. No <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> allocation needed. Values stay in CPU registers. Bound by ALU speed: not memory latency.

### Sieve of Eratosthenes (c. 200 BCE)

**Definition:** Finds primes by marking multiples.

**Philosophy:** Elimination: not verification. Assume all prime: cross out composites. Early form of <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr> and caching.

**Use Cases:** Prime lookup tables for science. Factorization.

**Memory Mechanics:** Trades space for time. Requires <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> size `N`. Compressed bit-vectors (Bitset) save space. Contiguous scanning leverages <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>. Runs in L1 <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> for ranges under millions.

## 39.3. Medieval to Renaissance (500–1600)

| Contribution | Figure | Significance |
|-------------|--------|------------|
| Hindu-Arabic numerals | al-Khwarizmi | Enabled positional computation |
| Cryptography | Al-Kindi | First frequency analysis |
| Algebra | Omar Khayyam | Algorithmic equation solving |
| Mechanical calculators | Pascal, Leibniz | Physical computation devices |

## 39.4. Modern Foundation (1600–1900)

**Newton (1671):** Iterative methods for roots.
**Gauss (1809):** Gaussian elimination for linear equations.
**Babbage & Lovelace (1830s):** <abbr title="Babbage's design for a general-purpose mechanical computer">Analytical Engine</abbr>. First machine-executable algorithm.

### Decision Matrix

| Choose History When... | Choose Modern When... |
|----------------------|------------------------|
| Understanding architecture | Under deadline pressure |
| Teaching foundations | Solving immediate bugs |
| Designing novel logic | Implementing known solutions |

### Edge Cases & Pitfalls

- **Anachronism:** Do not judge ancient speed by modern standards.
- **Attribution:** Many algorithms misattributed. Euclid likely compiled existing methods.
- **Cultural bias:** Algorithmic logic developed globally: China, India, Islamic world.

### Anti-Patterns

- **Historical Presentism:** Judging ancient logic by Big-O. Ancient constraints: human memory, clay. Babylonian iteration was optimal for its medium.
- **Reinvention Illusion:** Assuming novelty without study. Divide-and-conquer and memoization have millennial roots.
- **Whig History Fallacy:** Viewing history as linear progress. Knowledge cycles. Islamic scholars preserved logic lost to Europe.

## 39.5. Quick Reference

| Era | Key Development | Modern Equivalent |
|-----|----------------|-------------------|
| 1800 BCE | Babylonian square root | Newton-Raphson |
| 300 BCE | Euclid's GCD | Still used today |
| 200 BCE | Sieve of Eratosthenes | Segmented sieve variants |
| 820 CE | al-Khwarizmi's algebra | <abbr title="Computer manipulation of mathematical expressions symbolically">Symbolic computation</abbr> |
| 1830s | Babbage/Lovelace | Modern programs |


{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 39:</strong> Algorithms are ancient problem-solving tools. Break complex problems into simple, repeatable steps. History reveals timeless nature of good design.
{{% /alert %}}

## See Also

- [Chapter 40: The Algorithmic Revolution](/docs/part-viii/chapter-40/)
- [Chapter 41: Evolution of Data Structures](/docs/part-viii/chapter-41/)
- [Chapter 43: Philosophy of Computation](/docs/part-viii/chapter-43/)