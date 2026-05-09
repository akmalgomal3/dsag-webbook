---
weight: 10200
title: "Chapter 2 - Complexity Analysis"
description: "Complexity Analysis"
icon: "article"
date: "2024-08-24T23:42:25+07:00"
lastmod: "2024-08-24T23:42:25+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>The best way to predict the future is to invent it.</em>" — Alan Kay</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 2 focuses on complexity analysis, exploring time and space boundaries, <abbr title="Relating to values or properties approached as a limit, used in algorithm analysis.">asymptotic</abbr> notations (<abbr title="A mathematical notation describing the limiting behavior of a function when the argument tends towards a particular value or infinity.">Big-O</abbr>, <abbr title="A mathematical notation describing the lower bound of an algorithm's growth rate.">Big-Ω</abbr>, <abbr title="A mathematical notation describing the tight bound of an algorithm's growth rate.">Big-Θ</abbr>), and evaluating performance scaling across different data sizes.
{{% /alert %}}

## 2.1. Introduction to Complexity Analysis

**Definition:** Complexity analysis measures the efficiency of an algorithm in terms of execution time and memory usage as a function of the input size.

### Operations & Complexity

| Metric | Notation | Description |
|--------|--------|------------|
| <abbr title="A computational complexity that describes the amount of computer time taken by an algorithm.">Time Complexity</abbr> | <code>T(n)</code> | Execution time vs input size |
| <abbr title="A computational complexity that describes the amount of memory space taken by an algorithm.">Space Complexity</abbr> | <code>S(n)</code> | Memory used |
| Auxiliary Space | <code>O(1)</code>, <code>O(n)</code> | Extra memory excluding the input |

### Decision Matrix

| Use This Analysis When... | Avoid If... |
|-----------------------|------------------|
| Comparing algorithms | A solution is proven optimal and has no alternatives |
| Predicting scalability | Input size is always small and constant |
| Optimizing bottlenecks | Development time is more valuable than minor gains |

### Edge Cases & Pitfalls

- **Constant factors:** <abbr title="A mathematical notation describing the limiting behavior of a function when the argument tends towards a particular value or infinity.">Big-O</abbr> ignores constants; an <code>O(n)</code> algorithm with a massive constant factor might be slower than an <code>O(n log n)</code> algorithm for practical inputs.
- **Hardware dependency:** Complexity analysis is abstract; actual implementation speed depends heavily on <abbr title="A hardware or software component that stores data so future requests can be served faster.">cache</abbr>, CPU, and <abbr title="A program that translates source code into machine code.">compiler</abbr> optimizations.

## 2.2. Analyzing <abbr title="A computational complexity that describes the amount of computer time taken by an algorithm.">Time Complexity</abbr>

**Definition:** <abbr title="A computational complexity that describes the amount of computer time taken by an algorithm.">Time complexity</abbr> measures the number of basic operations an algorithm performs as the input size grows.

### Operations & Complexity

| Class | Notation | Example |
|-------|--------|--------|
| Constant | <code>O(1)</code> | <abbr title="A collection of items stored at contiguous memory locations.">Array</abbr> <abbr title="A data structure that improves the speed of data retrieval operations.">index</abbr> access |
| Logarithmic | <code>O(log n)</code> | <abbr title="A search algorithm that finds the position of a target value within a sorted array.">Binary search</abbr> |
| Linear | <code>O(n)</code> | <abbr title="A search algorithm that checks each element sequentially until the target is found.">Linear search</abbr> |
| Linearithmic | <code>O(n log n)</code> | <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge sort</abbr>, QuickSort avg |
| Quadratic | <code>O(n^{2})</code> | <abbr title="A simple sorting algorithm that repeatedly steps through the list, comparing adjacent elements.">Bubble sort</abbr>, nested loops |
| Exponential | <code>O(2^n)</code> | Subset generation, <abbr title="A straightforward approach trying all possible solutions.">brute force</abbr> TSP |

### Pseudocode

```text
LinearSearch(arr, target):
    for i from 0 to length(arr)-1:
        if arr[i] == target:
            return i
    return -1

BinarySearch(arr, target):
    left = 0
    right = length(arr) - 1
    while left <= right:
        mid = left + (right - left) / 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "time"
)

func linearSearch(arr []int, target int) int {
    for i, v := range arr {
        if v == target {
            return i
        }
    }
    return -1
}

func binarySearch(arr []int, target int) int {
    left, right := 0, len(arr)-1
    for left <= right {
        mid := left + (right-left)/2
        if arr[mid] == target {
            return mid
        }
        if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}

func main() {
    arr := []int{1, 3, 5, 7, 9, 11, 13}
    start := time.Now()
    fmt.Println(binarySearch(arr, 7))
    fmt.Println("Elapsed:", time.Since(start))
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Large input → choose <code>O(log n)</code> or <code>O(n log n)</code> | <code>O(n^{2})</code> for <code>n > 10^4</code> |
| Real-time system → choose <code>O(1)</code> or <code>O(log n)</code> | Algorithms with unbounded worst cases |

### Edge Cases & Pitfalls

- **Best vs worst case:** QuickSort is <code>O(n log n)</code> average but <code>O(n^{2})</code> worst case.
- **Amortized cost:** Some operations are occasionally expensive (e.g., dynamic <abbr title="A collection of items stored at contiguous memory locations.">array</abbr> resize), but the average remains <code>O(1)</code>.
- **Empty input:** Always validate `len(arr) == 0`.

## 2.3. Analyzing <abbr title="A computational complexity that describes the amount of memory space taken by an algorithm.">Space Complexity</abbr>

**Definition:** <abbr title="A computational complexity that describes the amount of memory space taken by an algorithm.">Space complexity</abbr> measures the total memory used by an algorithm, including input and auxiliary space.

### Operations & Complexity

| Class | Notation | Example |
|-------|--------|--------|
| In-place | <code>O(1)</code> | QuickSort (iterative partition) |
| Linear | <code>O(n)</code> | <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> (temporary arrays) |
| Logarithmic | <code>O(log n)</code> | <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> (<abbr title="A search algorithm that finds the position of a target value within a sorted array.">binary search</abbr>) |
| Quadratic | <code>O(n^{2})</code> | DP table for LCS |

### Pseudocode

```text
QuickSort(arr, low, high):
    if low < high:
        pivot = Partition(arr, low, high)
        QuickSort(arr, low, pivot-1)
        QuickSort(arr, pivot+1, high)

Partition(arr, low, high):
    pivot = arr[high]
    i = low
    for j from low to high-1:
        if arr[j] < pivot:
            SWAP arr[i] and arr[j]
            i = i + 1
    SWAP arr[i] and arr[high]
    return i
```

### Idiomatic Go Implementation

```go
package main

import "fmt"

func inPlaceQuickSort(arr []int, low, high int) {
    if low < high {
        pi := partition(arr, low, high)
        inPlaceQuickSort(arr, low, pi-1)
        inPlaceQuickSort(arr, pi+1, high)
    }
}

func partition(arr []int, low, high int) int {
    pivot := arr[high]
    i := low
    for j := low; j < high; j++ {
        if arr[j] < pivot {
            arr[i], arr[j] = arr[j], arr[i]
            i++
        }
    }
    arr[i], arr[high] = arr[high], arr[i]
    return i
}

func main() {
    arr := []int{10, 7, 8, 9, 1, 5}
    inPlaceQuickSort(arr, 0, len(arr)-1)
    fmt.Println(arr)
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Memory is strictly limited → in-place <code>O(1)</code> | Stability is required (<abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> uses <code>O(n)</code> space) |
| <abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> <abbr title="The length of the path from the root to a node.">depth</abbr> is small | <abbr title="A LIFO (Last In, First Out) abstract data type.">Stack</abbr> is constrained → use <abbr title="The repetition of a process, typically using loops.">iteration</abbr> |

### Edge Cases & Pitfalls

- **<abbr title="A method where the solution to a problem depends on solutions to smaller instances of the same problem.">Recursion</abbr> <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr>:** Every recursive call adds a <abbr title="A LIFO (Last In, First Out) abstract data type.">stack</abbr> frame; huge depths can cause <abbr title="An error caused by using more stack memory than allocated.">stack overflow</abbr>.
- **Slice aliasing:** In Go, slices are references; in-place modifications affect the original slice.
- **Memory leak:** Goroutines that never terminate cause leaks.

## 2.4. <abbr title="A method of describing limiting behavior of functions, used in algorithm analysis.">Asymptotic Analysis</abbr> and Tight Bounds

**Definition:** <abbr title="A method of describing limiting behavior of functions, used in algorithm analysis.">Asymptotic analysis</abbr> describes the growth of complexity as the input size approaches infinity, using <abbr title="A mathematical notation describing the limiting behavior of a function when the argument tends towards a particular value or infinity.">Big-O</abbr>, <abbr title="A mathematical notation describing the lower bound of an algorithm's growth rate.">Big-Ω</abbr>, and <abbr title="A mathematical notation describing the tight bound of an algorithm's growth rate.">Big-Θ</abbr> notations.

### Operations & Complexity

| Notation | Meaning | Example |
|--------|-------|--------|
| <code>O(f(n))</code> | <abbr title="A function that grows at least as fast as the given function.">Upper bound</abbr> (worst case) | <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> <code>O(n log n)</code> |
| <code>Ω(f(n))</code> | <abbr title="A function that grows no faster than the given function.">Lower bound</abbr> (best case) | <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> <code>Ω(n log n)</code> |
| <code>Θ(f(n))</code> | <abbr title="A function that grows at the same rate as the given function, both upper and lower.">Tight bound</abbr> (best = worst) | <abbr title="A divide-and-conquer sorting algorithm that divides the array into halves and merges them.">Merge Sort</abbr> <code>Θ(n log n)</code> |

### Decision Matrix

| Use Notation When... | Avoid If... |
|-------------------------|------------------|
| <code>O</code> → guaranteed performance limit | Relying only on <code>O</code> without considering <code>Ω</code> |
| <code>Θ</code> → consistent complexity | Best and worst cases are significantly different |

### Edge Cases & Pitfalls

- **Loose bound:** Providing an <code>O(n^{3})</code> bound for an <code>O(n)</code> algorithm is technically correct but not informative.
- **Small inputs:** <abbr title="A method of describing limiting behavior of functions, used in algorithm analysis.">Asymptotic analysis</abbr> does not always reflect performance on small inputs.
- **Average case:** <abbr title="A mathematical notation describing the limiting behavior of a function when the argument tends towards a particular value or infinity.">Big-O</abbr> typically refers to the worst case; the average case can be much better.

## 2.5. Advanced Complexity Topics

**Definition:** Advanced topics include <abbr title="A method for analyzing a given algorithm's complexity by averaging time over a sequence of operations.">amortized analysis</abbr>, probabilistic analysis, complexity classes (P, NP, <abbr title="A class of problems that are at least as hard as the hardest problems in NP.">NP-Complete</abbr>), and parameterized complexity.

### Operations & Complexity

| Topic | Concept | Complexity |
|-------|--------|--------------|
| <abbr title="A method for analyzing a given algorithm's complexity by averaging time over a sequence of operations.">Amortized Analysis</abbr> | Average cost of a sequence | <code>O(1)</code> per operation (dynamic <abbr title="A collection of items stored at contiguous memory locations.">array</abbr>) |
| Probabilistic | Expected performance | Randomized QuickSort <code>O(n log n)</code> expected |
| P-Class | <abbr title="An algorithm whose running time is upper bounded by a polynomial expression.">Polynomial time</abbr> solvable | <code>O(n^k)</code> |
| <abbr title="A class of problems that are at least as hard as the hardest problems in NP.">NP-Complete</abbr> | Verifiable in poly time | No known poly-time algorithm exists |
| Parameterized | Fixed-parameter tractable | <code>O(f(k) \cdot n^c)</code> |

### Pseudocode

```text
RandomizedQuickSort(arr):
    if length(arr) <= 1:
        return
    pick pivot index
    SWAP pivot with last element
    p = Partition(arr)
    RandomizedQuickSort(arr[0:p])
    RandomizedQuickSort(arr[p+1:end])
```

### Idiomatic Go Implementation

```go
package main

import (
    "fmt"
    "math/rand"
    "time"
)

func randomizedQuickSort(arr []int) {
    if len(arr) <= 1 {
        return
    }
    rand.Seed(time.Now().UnixNano())
    pivotIdx := rand.Intn(len(arr))
    arr[pivotIdx], arr[len(arr)-1] = arr[len(arr)-1], arr[pivotIdx]
    p := partition(arr)
    randomizedQuickSort(arr[:p])
    randomizedQuickSort(arr[p+1:])
}

func partition(arr []int) int {
    pivot := arr[len(arr)-1]
    i := 0
    for j := 0; j < len(arr)-1; j++ {
        if arr[j] < pivot {
            arr[i], arr[j] = arr[j], arr[i]
            i++
        }
    }
    arr[i], arr[len(arr)-1] = arr[len(arr)-1], arr[i]
    return i
}

func main() {
    arr := []int{3, 6, 8, 10, 1, 2, 1}
    randomizedQuickSort(arr)
    fmt.Println(arr)
}
```

### Decision Matrix

| Use When... | Avoid If... |
|----------------|------------------|
| Amortized → data structures with occasional expensive operations | Hard real-time guarantees per operation are required |
| Randomized → worst cases are extremely rare | Deterministic guarantees are required |
| Parameterized → parameter is small, input is large | Parameter <code>k</code> is large → it remains exponential |

### Edge Cases & Pitfalls

- **Amortized vs average:** Amortized is the <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">worst-case</abbr> average over a sequence, not the expected <abbr title="The data associated with a key in a key-value pair.">value</abbr> over random inputs.
- **Randomized seed:** In Go, the global `rand.Seed` is not thread-safe; use `rand.NewSource` per goroutine if needed.
- **<abbr title="A class of problems that are at least as hard as the hardest problems in NP.">NP-Complete</abbr>:** Don't waste time looking for a polynomial algorithm for <abbr title="A class of problems that are at least as hard as the hardest problems in NP.">NP-Complete</abbr> problems; focus on approximation or heuristics.

### Quick <abbr title="A value that enables a program to indirectly access a particular datum.">Reference</abbr>

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Big-O (<code>O</code>) | <abbr title="A function that grows at least as fast as the given function.">Upper bound</abbr> | — | — | <abbr title="The maximum runtime or resource usage of an algorithm over all possible inputs.">Worst-case</abbr> guarantee |
| Omega (<code>Ω</code>) | <abbr title="A function that grows no faster than the given function.">Lower bound</abbr> | — | — | <abbr title="The minimum runtime or resource usage of an algorithm over all possible inputs.">Best-case</abbr> analysis |
| Theta (<code>Θ</code>) | <abbr title="A function that grows at the same rate as the given function, both upper and lower.">Tight bound</abbr> | — | — | Best = worst case |
| Amortized | Average over sequence | — | — | Data structures analysis |
| Probabilistic | Expected over randomness | — | — | Randomized algorithms |
| Polynomial (P) | Tractable | — | — | Polynomial solvable problems |
| <abbr title="A class of problems that are at least as hard as the hardest problems in NP.">NP-Complete</abbr> | No known poly algorithm | Use approximation/heuristic |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 2:</strong> This chapter explains complexity analysis fundamentals, including time and <abbr title="A computational complexity that describes the amount of memory space taken by an algorithm.">space complexity</abbr>, <abbr title="Relating to values or properties approached as a limit, used in algorithm analysis.">asymptotic</abbr> notation (<abbr title="A mathematical notation describing the limiting behavior of a function when the argument tends towards a particular value or infinity.">Big-O</abbr>, <abbr title="A mathematical notation describing the lower bound of an algorithm's growth rate.">Big-Ω</abbr>, <abbr title="A mathematical notation describing the tight bound of an algorithm's growth rate.">Big-Θ</abbr>), and advanced topics like amortized and probabilistic analysis. Use these tools to compare algorithms, predict scalability, and identify performance bottlenecks before optimizing.
{{% /alert %}}

## See Also

- [Chapter 3 — Introduction to Data Structures and Algorithms in Go](/docs/Part-I/Chapter-3/)
- [Chapter 4 — Fundamentals of Go Programming for Algorithms](/docs/Part-I/Chapter-4/)
- [Chapter 33 — Linear Programming](/docs/Part-VII/Chapter-33/)
