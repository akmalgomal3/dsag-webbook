# DSAG — Data Structures and Algorithms in Go

[![Chapters](https://img.shields.io/badge/Chapters-60-blue)](./)
[![Parts](https://img.shields.io/badge/Parts-12-blue)](./)
[![Hugo](https://img.shields.io/badge/Hugo-0.161%2B-ff4088)](https://gohugo.io/)
[![Go](https://img.shields.io/badge/Go-1.21%2B-00ADD8)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A comprehensive, practitioner-focused book on data structures and algorithms, implemented idiomatically in Go. Built as a Hugo static site.

---

## Overview

**DSAG** (Data Structures and Algorithms in Go) is a 60-chapter technical book designed for software engineers who want to:

- Understand how data structures and algorithms work under the hood
- Implement them idiomatically in Go
- Know **when** to use (and when **not** to use) specific structures and algorithms
- Recognize edge cases, anti-patterns, and Go-specific pitfalls

Each chapter is written for a 7–10 minute reading time, with practical code examples, decision matrices, Big-O tables, and references to Go's standard library.

---

## Book Structure

The book is organized into **12 parts** and **60 chapters**:

| Part | Title | Chapters |
|------|-------|----------|
| **I** | Foundations & Go Mechanics | 1–4 |
| **II** | Basic Data Structures | 5–8 |
| **III** | Trees, Graphs & Representations | 9–12 |
| **IV** | Graph Algorithms | 13–18 |
| **V** | Sorting & Searching | 19–22 |
| **VI** | Algorithmic Paradigms | 23–28 |
| **VII** | Advanced Topics | 29–39 |
| **VIII** | History & Philosophy of Algorithms | 40–44 |
| **IX** | Advanced Data Structures | 45–50 |
| **X** | Advanced Graph Algorithms | 51–54 |
| **XI** | Specialized Sorting & Techniques | 55–57 |
| **XII** | Advanced Topics | 58–60 |

### Chapter Topics

- **Fundamentals:** Time/space complexity, Go basics, benchmarking
- **Data Structures:** Arrays, linked lists, stacks, queues, hash tables, BST, heaps, tries, segment trees, B-trees, skip lists, Bloom filters
- **Graphs:** Representations, BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, MST, max flow, topological sort, SCC, A*, bridge-finding
- **Sorting & Searching:** Quicksort, mergesort, heapsort, counting/radix/bucket sort, binary search, interpolation search
- **Paradigms:** Dynamic programming, greedy algorithms, backtracking, divide & conquer
- **Advanced:** Parallel algorithms, cryptography, blockchain, bit manipulation, persistent structures, suffix arrays
- **History & Philosophy:** Origins of algorithms, Turing, complexity theory, modern algorithmic thinking

---

## Philosophy

- **Brevity over verbosity** — No fluff, no unnecessary proofs
- **Intuition over formalism** — Understand why, not just how
- **Go idiomatic** — No pseudocode, no language mixing
- **Practical** — Decision matrices for real-world choices
- **Honest** — Edge cases and when NOT to use something

---

## Building Locally

### Prerequisites

- [Hugo](https://gohugo.io/) v0.161+ (extended version)
- Go 1.21+ (for code examples)

### Development

```bash
# Clone the repository
git clone https://github.com/akmalgomal3/dsag-webbook.git
cd dsag-webbook

# Start development server
hugo server --port 1313

# Build the site
hugo --quiet
```

The site will be available at `http://localhost:1313`.

---

## Project Structure

```
dsag/
├── content/en/docs/          # Book chapters
│   ├── Part-I/               # Chapters 1-4
│   ├── Part-II/              # Chapters 5-8
│   ├── ...
│   └── Part-XII/             # Chapters 58-60
├── layouts/                  # Hugo templates
│   ├── _default/             # Page layouts
│   ├── partials/             # Reusable components
│   └── shortcodes/           # Custom shortcodes
├── static/                   # Static assets
│   ├── css/                  # Custom styles
│   └── js/                   # Scripts
├── hugo.toml                 # Site configuration
├── go.mod                    # Go module
└── AGENTS.md                 # Development guide
```

---

## Contributing

This book is developed with AI assistance. For development guidelines, shortcode usage, and chapter templates, see [AGENTS.md](AGENTS.md).

### Key Guidelines

- Follow the chapter template in `AGENTS.md`
- Include decision matrices and Big-O tables
- Write idiomatic Go code (max 40 lines per block)
- Include edge cases and anti-patterns
- Ensure `hugo --quiet` builds without errors

---

## License

This project is open source. See the repository for license details.

---

## Acknowledgments

- Built with [Hugo](https://gohugo.io/)
- Go standard library documentation
- Inspired by *Introduction to Algorithms* (CLRS) and *The Algorithm Design Manual*

---

**Repository:** [github.com/akmalgomal3/dsag-webbook](https://github.com/akmalgomal3/dsag-webbook)
