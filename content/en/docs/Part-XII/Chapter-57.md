---
weight: 120100
title: "Chapter 57: Minimax and Game Trees"
description: "Minimax and Game Trees"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
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
The philosophy is deterministic pessimism. <abbr title="A decision rule used in two-player zero-sum games that minimizes the possible loss for a worst-case scenario.">Minimax</abbr> assumes the opponent plays optimally. By mapping out possible futures and planning against the worst-case scenario, the algorithm guarantees it will never make a critical mistake.

**Use Cases:**
Classic turn-based, perfect-information board games like Chess, Checkers, and Tic-Tac-Toe, as well as business negotiation models in Game Theory.

**Memory Mechanics:**
<abbr title="A technique that eliminates branches in a game tree that cannot affect the final minimax decision.">Minimax</abbr> relies exclusively on the <abbr title="Memory used to execute functions and store local variables.">call stack</abbr> to navigate the game tree via depth-first search. Without <abbr title="An optimization technique for minimax that eliminates branches that cannot possibly influence the final decision.">Alpha-Beta pruning</abbr>, the tree expands exponentially, pushing millions of frames onto the <abbr title="Memory used to execute functions and store local variables.">stack</abbr> and threatening an <abbr title="An error caused by using more stack memory than allocated.">Out of Memory (OOM)</abbr> crash. Alpha-Beta pruning acts as a memory circuit breaker, abruptly stopping the recursion when a mathematical threshold is crossed. This drastically shrinks the active <abbr title="Memory used to execute functions and store local variables.">stack</abbr> depth and keeps the algorithm firmly within the physical limits of the L1/L2 caches.

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

// Board interface for two-player zero-sum games
type Board interface {
	isGameOver() bool
	evaluate() int
	getMoves() []int
	makeMove(move int)
	undoMove(move int)
}

// TicTacToe implements Board for a 3x3 board.
// 0=empty, 1=X (maximizer), 2=O (minimizer)
type TicTacToe struct {
	board [9]int
}

func (t *TicTacToe) isGameOver() bool {
	return t.evaluate() != 0 || len(t.getMoves()) == 0
}

func (t *TicTacToe) evaluate() int {
	lines := [8][3]int{
		{0, 1, 2}, {3, 4, 5}, {6, 7, 8},
		{0, 3, 6}, {1, 4, 7}, {2, 5, 8},
		{0, 4, 8}, {2, 4, 6},
	}
	for _, l := range lines {
		a, b, c := t.board[l[0]], t.board[l[1]], t.board[l[2]]
		if a != 0 && a == b && b == c {
			if a == 1 {
				return 10 // X wins
			}
			return -10 // O wins
		}
	}
	return 0
}

func (t *TicTacToe) getMoves() []int {
	var moves []int
	for i, v := range t.board {
		if v == 0 {
			moves = append(moves, i)
		}
	}
	return moves
}

func (t *TicTacToe) makeMove(move int) {
	xCount, oCount := 0, 0
	for _, v := range t.board {
		switch v {
		case 1:
			xCount++
		case 2:
			oCount++
		}
	}
	if xCount == oCount {
		t.board[move] = 1
	} else {
		t.board[move] = 2
	}
}

func (t *TicTacToe) undoMove(move int) {
	t.board[move] = 0
}

func (t *TicTacToe) String() string {
	s := "\n"
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			switch t.board[i*3+j] {
			case 0:
				s += "."
			case 1:
				s += "X"
			case 2:
				s += "O"
			}
			if j < 2 {
				s += " "
			}
		}
		s += "\n"
	}
	return s
}

// minimax with alpha-beta pruning
func minimaxAB(board Board, depth int, alpha, beta int, isMaximizing bool) int {
	if depth == 0 || board.isGameOver() {
		return board.evaluate()
	}
	if isMaximizing {
		maxEval := math.MinInt64
		for _, move := range board.getMoves() {
			board.makeMove(move)
			eval := minimaxAB(board, depth-1, alpha, beta, false)
			board.undoMove(move)
			if eval > maxEval {
				maxEval = eval
			}
			if eval > alpha {
				alpha = eval
			}
			if beta <= alpha {
				break
			}
		}
		return maxEval
	}
	minEval := math.MaxInt64
	for _, move := range board.getMoves() {
		board.makeMove(move)
		eval := minimaxAB(board, depth-1, alpha, beta, true)
		board.undoMove(move)
		if eval < minEval {
			minEval = eval
		}
		if eval < beta {
			beta = eval
		}
		if beta <= alpha {
			break
		}
	}
	return minEval
}

func bestMove(board Board) int {
	bestVal := math.MinInt64
	bestIdx := -1
	for _, move := range board.getMoves() {
		board.makeMove(move)
		val := minimaxAB(board, len(board.getMoves()), math.MinInt64, math.MaxInt64, false)
		board.undoMove(move)
		if val > bestVal {
			bestVal = val
			bestIdx = move
		}
	}
	return bestIdx
}

func main() {
	game := &TicTacToe{}
	// X (AI, maximizer) plays first at center (move 4)
	game.makeMove(4)
	fmt.Println("X (AI) plays center:", game)
	// O (opponent, minimizer) plays top-left (move 0)
	game.makeMove(0)
	fmt.Println("O responds at top-left:", game)
	// X computes and plays the best move using alpha-beta minimax
	move := bestMove(game)
	game.makeMove(move)
	fmt.Printf("X's best response is move %d:%s\n", move, game)
	if game.evaluate() > 0 {
		fmt.Println("X wins!")
	} else if game.evaluate() < 0 {
		fmt.Println("O wins!")
	} else if len(game.getMoves()) == 0 {
		fmt.Println("Draw!")
	} else {
		fmt.Println("Game continues...")
	}
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
| Small <abbr title="The set of all possible states in a problem">state space</abbr> | <abbr title="The set of all possible states in a problem">State space</abbr> too large for full search |
| Deterministic moves | Stochastic elements |

### Edge Cases & Pitfalls

- **Horizon effect:** Bad moves beyond search depth are invisible.
- **<abbr title="A function that assigns a score to a game state to determine how favorable it is for a player.">Evaluation function</abbr>:** A poor heuristic defeats perfect search.
- **Transpositions:** Same position via different paths — use transposition tables.
- **Memory:** Deep searches exhaust memory — iterative deepening helps.

### Anti-Patterns

- **Running minimax without alpha-beta pruning:** Without pruning, the full game tree expands at O(b^d); alpha-beta cuts this by roughly half per level — omitting it makes even moderate games intractable.
- **Using minimax for non-zero-sum or stochastic games:** Minimax assumes a deterministic, perfect-information, zero-sum game; applying it to poker, backgammon, or cooperative games produces strategically flawed decisions.
- **Poor evaluation function:** Minimax's output is only as good as its heuristic; a bad evaluation function causes systematic blunders that no amount of search depth can fix.
- **Ignoring transpositions:** The same board position reached by different move sequences should be evaluated once and cached; recomputing it every time multiplies work exponentially.

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
<strong>Summary Chapter 57:</strong> <abbr title="A decision rule used in two-player zero-sum games that minimizes possible loss for a worst-case scenario.">Minimax</abbr> is the algorithmic embodiment of strategic thinking: assume your opponent is as smart as you, and plan accordingly. Alpha-beta pruning proves that even in exhaustive search, clever ordering can eliminate the impossible. From chess engines to checkers bots, minimax remains the conceptual foundation of competitive game AI.
{{% /alert %}}

## See Also

- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/part-vi/chapter-23/)
- [Chapter 25: <abbr title="Building candidates incrementally and abandoning dead ends">Backtracking</abbr>](/docs/part-vi/chapter-25/)
- [Chapter 58: Mo's Algorithm](/docs/part-xii/chapter-58/)
