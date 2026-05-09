---
weight: 80100
title: "Chapter 40 - Origins of Algorithms"
description: "Origins of Algorithms"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The question of whether a computer can think is no more interesting than the question of whether a submarine can swim.</em>" — Edsger Dijkstra</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 40 explores the ancient origins of algorithms — from Babylonian clay tablets to Euclid's Elements — revealing that algorithmic thinking predates computers by millennia.
{{% /alert %}}

## 40.1. What Is an Algorithm?

**Definition:** An <abbr title="A finite sequence of well-defined, computer-implementable instructions to solve a class of problems.">algorithm</abbr> is a finite sequence of well-defined instructions to solve a problem. The word derives from the Latinized name of the Persian mathematician <abbr title="A Persian polymath who lived c. 780–850 CE, considered the father of algebra.">al-Khwarizmi</abbr>.

### The Three Pillars

| Pillar | Description | Example |
|--------|-------------|---------|
| Finiteness | Must terminate after finite steps | Euclid's GCD terminates when remainder is zero |
| Definiteness | Each step unambiguous | "Divide A by B" vs. "Make it smaller" |
| Effectiveness | Operations are executable | Arithmetic, comparison, assignment |

## 40.2. Ancient Algorithms (Before 500 CE)

### Babylonian Mathematics (c. 1800 BCE)

Babylonians on clay tablets computed square roots using iterative approximation — essentially the precursor to Newton's method:

```
To find √A:
1. Guess x
2. Compute y = A / x
3. Update x = (x + y) / 2
4. Repeat until x ≈ y
```

### Euclid's Algorithm (c. 300 BCE)

The oldest non-trivial algorithm still in use. Euclid's <abbr title="Greatest Common Divisor: the largest positive integer that divides each of the integers.">GCD</abbr> algorithm demonstrates the power of reduction — transforming a hard problem into a smaller instance of itself.

### Sieve of Eratosthenes (c. 200 BCE)

The first <abbr title="An algorithmic paradigm that solves problems by breaking them into smaller subproblems and storing solutions.">dynamic programming</abbr>-like algorithm: iteratively mark multiples to find primes, avoiding redundant work.

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
**Babbage & Lovelace** (1830s): The Analytical Engine + first algorithm intended for machine execution.

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
| 820 CE | al-Khwarizmi's algebra | Symbolic computation |
| 1830s | Babbage/Lovelace | Modern computer programs |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 40:</strong> Algorithms are not a modern invention — they are the crystallization of thousands of years of human problem-solving. From Babylonian clay tablets to Babbage's gears, the essential insight remains: break complex problems into simple, repeatable steps. Understanding this history prevents reinventing wheels and reveals the timeless nature of good algorithmic design.
{{% /alert %}}
