---
weight: 120100
title: "Chapter 58: Minimax and Game Trees"
description: "Minimax and Game Trees"
icon: "article"
date: "2024-08-24T23:42:09+07:00"
lastmod: "2024-08-24T23:42:09+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Chess is as elaborate a waste of human intelligence as you can find outside an advertising agency.</em>" : Raymond Chandler</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 58 explores minimax — the foundational algorithm for two-player zero-sum games, and alpha-beta pruning that makes it practical.
{{% /alert %}}

## 58.1. Game Trees

**Definition:** A <abbr title="A directed graph representing all possible game states and moves in a two-player game.">game tree</abbr> represents all possible sequences of moves. In two-player zero-sum games, one player's gain is the other's loss.

**Background & Philosophy:**
The philosophy is deterministic pessimism. Minimax assumes the opponent is flawlessly intelligent and infinitely malicious. By mapping out every possible future and aggressively planning against the absolute worst-case scenario, the algorithm guarantees it will never make a catastrophic mistake.

**Use Cases:**
Classic turn-based, perfect-information board games like Chess, Checkers, and Tic-Tac-Toe, as well as business negotiation models in Game Theory.

**Memory Mechanics:**
Minimax relies exclusively on the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr> to navigate the game tree via Depth-First Search. Without Alpha-Beta pruning, the tree expands exponentially, pushing millions of frames onto the <abbr title="Memory used to execute functions and store local variables.">stack</abbr> and threatening an <abbr title="An error caused by using more stack memory than allocated.">Out of Memory (OOM)</abbr> crash. Alpha-Beta pruning acts as a memory circuit breaker, abruptly stopping the recursion when a mathematical threshold is crossed. This drastically shrinks the active <abbr title="Memory used to execute functions and store local variables.">stack</abbr> depth and keeps the algorithm firmly within the physical limits of the L1/L2 caches.

### The Minimax Principle

- **Maximizer** (AI): Tries to maximize the score
- **Minimizer** (Opponent): Tries to minimize the score

Assume the opponent plays optimally — pessimistic but safe.

## 58.2. Minimax Algorithm

```go
package main

import (
	"fmt"
	"math"
)

// Minimal interfaces for demonstration
type Board interface {
	isGameOver() bool
	evaluate() int
	getMoves() []int
	makeMove(move int)
	undoMove(move int)
}

func minimax(board Board, depth int, isMaximizing bool) int {
    if depth == 0 || board.isGameOver() {
        return board.evaluate()
    }
    
    if isMaximizing {
        maxEval := math.MinInt64
        for _, move := range board.getMoves() {
            board.makeMove(move)
            eval := minimax(board, depth-1, false)
            board.undoMove(move)
            if eval > maxEval {
                maxEval = eval
            }
        }
        return maxEval
    }
    
    minEval := math.MaxInt64
    for _, move := range board.getMoves() {
        board.makeMove(move)
        eval := minimax(board, depth-1, true)
        board.undoMove(move)
        if eval < minEval {
            minEval = eval
        }
    }
    return minEval
}

func main() {
    // Demonstration stub
    fmt.Println("Minimax algorithm framework")
}
```

## 58.3. Alpha-Beta Pruning

**Definition:** <abbr title="An optimization technique for minimax that eliminates branches that cannot possibly influence the final decision.">Alpha-beta pruning</abbr> skips evaluating branches that cannot affect the final decision.

| Without Pruning | With Pruning |
|-----------------|--------------|
| <code>O(b^d)</code> | <code>O(b^(d/2))</code> in best case |
| Examines all nodes | Skips irrelevant subtrees |

### Key Insight

If the maximizer already has a move worth 5, and the minimizer finds a response worth 3, the minimizer will never choose a path allowing 5 — so stop exploring that branch.

## 58.4. Decision Matrix

| Use Minimax When... | Use Heuristics When... |
|---------------------|------------------------|
| Perfect information games | Imperfect information (poker, etc.) |
| Small state space | State space too large for full search |
| Deterministic moves | Stochastic elements |

### Edge Cases & Pitfalls

- **Horizon effect:** Bad moves beyond search depth are invisible.
- **Evaluation function:** A poor heuristic defeats perfect search.
- **Transpositions:** Same position via different paths — use transposition tables.
- **Memory:** Deep searches exhaust memory — iterative deepening helps.

## 58.5. Quick Reference

| Enhancement | Benefit |
|-------------|---------|
| Alpha-beta pruning | Reduces nodes by ~50% |
| Iterative deepening | Time-bounded search |
| Transposition table | Avoids recomputing states |
| Move ordering | Better pruning with good moves first |

| Go stdlib | Usage |
|-----------|-------|
| No direct stdlib | Implement natively for game AI |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 58:</strong> Minimax is the algorithmic embodiment of strategic thinking: assume your opponent is as smart as you, and plan accordingly. Alpha-beta pruning proves that even in exhaustive search, clever ordering can eliminate the impossible. From chess engines to checkers bots, minimax remains the conceptual foundation of competitive game AI.
{{% /alert %}}

## See Also

- [Chapter 24: Dynamic Programming](/docs/Part-VI/Chapter-24/)
- [Chapter 26: Backtracking](/docs/Part-VI/Chapter-26/)
- [Chapter 59: Mo's Algorithm](/docs/Part-XII/Chapter-59/)
