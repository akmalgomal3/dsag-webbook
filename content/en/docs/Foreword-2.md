---
weight: 500
title: "Foreword: A Practitioner's Perspective"
description: "On the intersection of theory and practice"
icon: "school"
date: "2024-08-24T23:23:41+07:00"
lastmod: "2024-08-24T23:23:41+07:00"
draft: false
toc: true
---

In academia, we often teach data structures and algorithms as a ladder of abstraction: each concept building on the previous, each proof rigorous, each analysis asymptotically tight. But abstraction alone leaves gaps.

What we rarely teach is **judgment**: the ability to look at a real problem with real constraints and choose the right approach. Theory tells you that Dijkstra runs in <code>O((V + E) log V)</code>. Practice tells you that for a <abbr title="A graph with far fewer edges than the maximum possible">sparse graph</abbr> with millions of nodes, <abbr title="Heuristic-driven shortest path algorithm">A*</abbr> with a good heuristic will feel instant while Dijkstra will feel broken. Both statements are true. Both matter.

This book bridges that gap. It is rigorous where rigor helps: complexity analysis, correctness arguments, edge cases. And pragmatic where pragmatism wins: cache efficiency, Go's garbage collector, standard library trade-offs, when to approximate instead of optimize.

For students, this book provides context that textbooks often omit. For practitioners, it provides the theoretical foundations that experience alone cannot teach. And for educators, it offers a model for how to teach algorithms as **engineering decisions**, not just mathematical objects.

The 60 chapters span from ancient Babylonian computation to modern <abbr title="Data structures using randomization for efficiency">probabilistic data structures</abbr>. That breadth is intentional. Algorithms are not a recent invention: they are the accumulated wisdom of human civilization's attempts to think systematically. Understanding that history prevents the hubris of believing that every problem requires a novel solution.

Read this book. Question its decision matrices. Adapt its principles to your domain. And remember: the goal is not to know every algorithm, but to develop the judgment to choose wisely among them.

That is the true craft of computer science.
