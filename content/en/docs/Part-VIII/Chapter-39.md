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
<strong>"<em>The question of whether a computer can think is no more interesting than the question of whether a submarine can swim.</em>" : Edsger Dijkstra</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 40 explores the ancient origins of algorithms — from Babylonian clay tablets to Euclid's Elements — revealing that algorithmic thinking predates computers by millennia.
{{% /alert %}}

## 40.1. What Is an Algorithm?

**Definition:** An <abbr title="A finite sequence of well-defined, computer-implementable instructions to solve a class of problems.">algorithm</abbr> is a finite sequence of well-defined instructions to solve a problem. The word derives from the Latinized name of the Persian mathematician <abbr title="A Persian polymath who lived c. 780–850 CE, considered the father of algebra.">al-Khwarizmi</abbr>.

**Background & Philosophy:**
Algorithms exist independently of computing machinery. The philosophy is procedural determinism: breaking a complex, overwhelming problem into mechanical, unambiguous steps that guarantee a result, regardless of the intelligence of the entity executing those steps.

**Use Cases:**
Translating human intent into reproducible mathematical models, enabling early astronomy, tax collection, and structural engineering.

**Memory Mechanics:**
Before electronic <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> existed, the "memory" for ancient algorithms was clay tablets, abacuses, or human short-term memory. The limitation of human working memory heavily influenced ancient algorithms to require tracking very few variables (state) simultaneously, directly analogous to an algorithm running with <code>O(1)</code> space complexity.

### The Three Pillars

| Pillar | Description | Example |
|--------|-------------|---------|
| Finiteness | Must terminate after finite steps | Euclid's GCD terminates when remainder is zero |
| Definiteness | Each step unambiguous | "Divide A by B" vs. "Make it smaller" |
| Effectiveness | Operations are executable | Arithmetic, comparison, assignment |

## 40.2. Ancient Algorithms (Before 500 CE)

### Babylonian Mathematics (c. 1800 BCE)

Babylonians on clay tablets computed square roots using iterative approximation — essentially the precursor to Newton's method:

```text
To find √A:
1. Guess x
2. Compute y = A / x
3. Update x = (x + y) / 2
4. Repeat until x ≈ y
```

### Euclid's Algorithm (c. 300 BCE)

**Definition:** An algorithm to find the greatest common divisor (GCD) of two numbers by repeatedly replacing the larger number by its remainder when divided by the smaller.

**Background & Philosophy:**
The philosophy is mathematical reduction. Euclid realized that `GCD(A, B) == GCD(B, A mod B)`, turning a massive search problem into a rapid geometric collapse, shrinking the problem space exponentially in each step.

**Use Cases:**
Essential today in cryptography (RSA key generation heavily relies on the Extended Euclidean Algorithm) and simplifying fractions in computer algebra systems.

**Memory Mechanics:**
Euclid's algorithm requires strictly <code>O(1)</code> memory. Because it only tracks two integer variables (`A` and `B`), these values never need to touch the <abbr title="Memory used for dynamic allocation, distinct from the call stack.">heap</abbr> or main <abbr title="Random Access Memory, the main volatile storage of a computer.">RAM</abbr> during execution. They reside entirely within the ultra-fast registers of the CPU, making the algorithm bound only by ALU (Arithmetic Logic Unit) instruction speed, not memory latency.

### Sieve of Eratosthenes (c. 200 BCE)

**Definition:** An ancient algorithm for finding all prime numbers up to any given limit by iteratively marking multiples.

**Background & Philosophy:**
The philosophy is elimination rather than verification. Instead of testing if a number is prime (which is computationally expensive), it assumes all numbers are prime and crosses out the guaranteed composites. This is the earliest manifestation of <abbr title="A method for solving complex problems by breaking them into simpler subproblems and storing solutions.">dynamic programming</abbr> and caching.

**Use Cases:**
Generating prime number lookup tables for scientific computing, factorization, and low-level mathematical sieving.

**Memory Mechanics:**
The Sieve fundamentally trades time for space. It requires an <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> of size `N`. In modern computers, representing this array as booleans takes N bytes, but representing it as a bit-vector (Bitset) compresses it heavily. Scanning the contiguous bit-vector to cross out multiples leverages perfect <abbr title="The tendency of a processor to access memory addresses that are near each other.">spatial locality</abbr>, allowing the CPU to execute the algorithm entirely inside the lightning-fast L1 <abbr title="A smaller, faster memory closer to a processor core.">cache</abbr> for ranges under a few million.

## 40.3. Medieval to Renaissance (500–1600)

| Contribution | Figure | Significance |
|-------------|--------|------------|
| Hindu-Arabic numerals | al-Khwarizmi | Enabled positional computation |
| Cryptography | Al-Kindi | First frequency analysis |
| Algebra | Omar Khayyam | Algorithmic equation solving |
| Mechanical calculators | Pascal, Leibniz | Physical computation devices |

## 40.4. The Algorithmic Revolution (1600–1900)

**Newton** (1671): Generalized iterative methods for roots and calculus.
**Gauss** (1809): Gaussian elimination — systematic linear equation solving.
**Babbage & Lovelace** (1830s): The <abbr title="Babbage's design for a general-purpose mechanical computer">Analytical Engine</abbr> + first algorithm intended for machine execution.

### Decision Matrix

| Study History When... | Focus on Modern When... |
|----------------------|------------------------|
| Understanding why structures exist | Under deadline pressure |
| Teaching foundational concepts | Solving immediate engineering problems |
| Designing novel algorithms | Implementing known solutions |

### Edge Cases & Pitfalls

- **Anachronism:** Don't judge ancient algorithms by modern complexity standards.
- **Attribution:** Many algorithms are misattributed; Euclid probably didn't invent "his" algorithm.
- **Cultural bias:** Algorithmic thinking developed independently in China, India, and the Islamic world.

## 40.5. Quick Reference

| Era | Key Development | Modern Equivalent |
|-----|----------------|-------------------|
| 1800 BCE | Babylonian square root | Newton-Raphson |
| 300 BCE | Euclid's GCD | Still used today |
| 200 BCE | Sieve of Eratosthenes | Segmented sieve variants |
| 820 CE | al-Khwarizmi's algebra | <abbr title="Computer manipulation of mathematical expressions symbolically">Symbolic computation</abbr> |
| 1830s | Babbage/Lovelace | Modern computer programs |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 39:</strong> Algorithms are not a modern invention — they are the crystallization of thousands of years of human problem-solving. From Babylonian clay tablets to Babbage's gears, the essential insight remains: break complex problems into simple, repeatable steps. Understanding this history prevents reinventing wheels and reveals the timeless nature of good algorithmic design.
{{% /alert %}}

## See Also

- [Chapter 40: The Algorithmic Revolution](/docs/part-viii/chapter-40/)
- [Chapter 41: Evolution of Data Structures](/docs/part-viii/chapter-41/)
- [Chapter 43: Philosophy of Computation](/docs/part-viii/chapter-43/)
