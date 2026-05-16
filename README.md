# DSAG: Data Structures and Algorithms in Go

[![Chapters](https://img.shields.io/badge/Chapters-59-blue)](./)
[![Parts](https://img.shields.io/badge/Parts-12-blue)](./)
[![Hugo](https://img.shields.io/badge/Hugo-0.161%2B-ff4088)](https://gohugo.io/)
[![Go](https://img.shields.io/badge/Go-1.21%2B-00ADD8)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Technical book. Implement data structures. Use idiomatic Go. Hugo static site.

---

## Overview

**DSAG**: 59-chapter technical book. Target software engineers. Goals:

- Understand internals. Core mechanics.
- Implement logic. Idiomatic Go.
- Select structures. Know trade-offs.
- Identify edge cases. Avoid anti-patterns.

Format: 7-10 minute read. Practical code. Decision matrices. Big-O tables.

---

## Book Structure

12 parts. 59 chapters.

| Part | Title | Chapters |
|------|-------|----------|
| **I** | Foundations & Go Mechanics | 1–4 |
| **II** | Basic Data Structures | 5–8 |
| **III** | Trees, Graphs & Representations | 9–12 |
| **IV** | Graph Algorithms | 13–18 |
| **V** | Sorting & Searching | 19–21 |
| **VI** | Algorithmic Paradigms | 22–27 |
| **VII** | Advanced Topics | 28–38 |
| **VIII** | History & Philosophy of Algorithms | 39–43 |
| **IX** | Advanced Data Structures | 44–49 |
| **X** | Advanced Graph Algorithms | 50–53 |
| **XI** | Specialized Sorting & Techniques | 54–56 |
| **XII** | Advanced Topics | 57–59 |

### Chapter Topics

- **Fundamentals:** Complexity. Go basics. Benchmarking.
- **Data Structures:** Arrays. Lists. Trees. Filters.
- **Graphs:** Representations. Search. Pathfinding. Max flow.
- **Sorting & Searching:** Quicksort. Mergesort. Binary search.
- **Paradigms:** Dynamic programming. Greedy. Backtracking. Divide & conquer.
- **Advanced:** Parallel. Cryptography. Blockchain. Bits.
- **History:** Origins. Turing. Complexity.

---

## Philosophy

- **Brevity**: No fluff. No proofs.
- **Intuition**: Focus logic. Deep understanding.
- **Go Idiomatic**: No pseudocode. Pure Go.
- **Practical**: Decision matrices. Real-world use.
- **Honest**: Edge cases. Safety limits.

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

Access site: `http://localhost:1313`.

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

AI assisted development. Read [AGENTS.md](AGENTS.md). Follow guidelines.

### Guidelines

- Use template.
- Include matrices. Detail Big-O.
- Write Go. Max 40 lines.
- Document edge cases. List anti-patterns.
- Verify build. Run `hugo --quiet`.

---

## License

Open source. Check license file.

---

## Acknowledgments

- Built with [Hugo](https://gohugo.io/).
- Go standard library docs.
- Inspired by CLRS and Algorithm Design Manual.

---

**Repository:** [github.com/akmalgomal3/dsag-webbook](https://github.com/akmalgomal3/dsag-webbook)
