# DSAG — Terminology & Style Guide

## Capitalization

| Category | Rule | Example |
|---|---|---|
| Headings (`##`, etc.) | Title Case | `## Depth-First Search (DFS)` |
| Prose body text | lowercase (unless proper noun) | `depth-first search`, `binary heap`, `dynamic programming` |
| `<abbr title="...">` display text | Title Case (term definitions) | `<abbr title="...">Depth-First Search</abbr>` |
| `<abbr title="...">` attribute | lowercase descriptive | `title="A graph traversal algorithm..."` |

### Algorithm Names (prose)

- depth-first search (DFS)
- breadth-first search (BFS)
- divide and conquer
- dynamic programming
- greedy algorithms
- backtracking
- binary heap
- hash table

### Notation

- big-O notation: `O(1)`, `O(n log n)`
- big-Omega: Ω(n)
- big-Theta: Θ(n)

## Hyphenation

| Use | Avoid |
|---|---|
| hashmap | hash map |
| real-world | real world (when used as adjective) |
| trade-off | tradeoff |
| big-O | Big O, Big-O (in prose) |
| multithreaded | multi thread, multi-thread |
| subproblem | sub-problem |

## Word Choice

| Prefer | Avoid |
|---|---|
| runtime | run time |
| contiguous | — |
| cache line | — |

## Markdown Formatting

| Rule | Example |
|---|---|
| All Go code blocks must specify language | ```` ```go ```` |
| Use `<abbr>` for first definition of key terms | `<abbr title="...">BST</abbr>` |
| Code comments explain *why*, not *what* | `// Prefer sort.Ints for production` over `// sort the slice` |

## Emphasis

- **Bold**: reserved for key definitions, warnings, terminology, major takeaways
- *Italic*: sparingly, for emphasis or book titles
- Avoid bolding emotional or rhetorical statements

## Prose Style

- Avoid opening every chapter with abstract/philosophical prose
- Use direct technical transitions
- Avoid "just", "simply", "basically" in non-trivial explanations
- Vary sentence rhythm — mix short and long sentences
- Prefer measurable technical explanation over vague adjectives (powerful, elegant, beautiful)

## Code Comment Style

Comments should explain:
- WHY (design rationale)
- Invariants (what must hold)
- Edge cases (what breaks)
- Complexity trade-offs
- Non-obvious implementation decisions

Avoid:
```go
// increment i
i++

// create a new node
node := &Node{}
```
