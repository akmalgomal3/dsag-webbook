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
<strong>"<em>Chess wastes human intelligence. Equivalent to advertising agencies.</em>" — Raymond Chandler</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 57 explores minimax: foundational algorithm for two-player zero-sum games. Alpha-beta pruning makes it practical.
{{% /alert %}}

## 57.1. Game Trees

**Definition:** <abbr title="A directed graph representing all possible game states and moves in a two-player game.">Game tree</abbr> represents all possible move sequences. Two-player zero-sum games: one player's gain equals other's loss.

**Background & Philosophy:**
Deterministic pessimism guides <abbr title="A decision rule used in two-player zero-sum games that minimizes the possible loss for a worst-case scenario.">minimax</abbr>. Algorithm assumes optimal opponent play. Mapping futures and worst-case scenarios prevents critical mistakes.

**Use Cases:**
Turn-based perfect-information games: Chess, Checkers, Tic-Tac-Toe. Game Theory applies models to business negotiations.

**Memory Mechanics:**
<abbr title="A technique that eliminates branches in a game tree that cannot affect the final minimax decision.">Minimax</abbr> uses <abbr title="Memory used to execute functions and store local variables.">call stack</abbr> for depth-first search. Tree expands exponentially without pruning. <abbr title="An optimization technique for minimax that eliminates branches that cannot possibly influence the final decision.">Alpha-Beta pruning</abbr> acts as memory circuit breaker. Recursion stops at mathematical threshold. Active stack depth shrinks. Algorithm stays within L1/L2 cache limits.

### The Minimax Principle

- **Maximizer** (AI): Maximizes score.
- **Minimizer** (Opponent): Minimizes score.

Algorithm assumes opponent plays optimally: pessimistic but safe.

## 57.2. Minimax Algorithm

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

## 57.3. Alpha-Beta Pruning

**Definition:** <abbr title="An optimization technique for minimax that eliminates branches that cannot possibly influence the final decision.">Alpha-beta pruning</abbr> skips branches. Irrelevant branches do not affect final decision.

| Without Pruning | With Pruning |
|-----------------|--------------|
| <code>O(b^d)</code> | <code>O(b^(d/2))</code> in best case |
| Examines all nodes | Skips irrelevant subtrees |

### Key Insight

Maximizer finds move worth 5. Minimizer finds response worth 3. Minimizer avoids path allowing 5. Stop exploring branch.

## 57.4. Decision Matrix

| Use Minimax When... | Use Heuristics When... |
|---------------------|------------------------|
| Perfect information games | Imperfect information (poker, etc.) |
| Small <abbr title="The set of all possible states in a problem">state space</abbr> | <abbr title="The set of all possible states in a problem">State space</abbr> too large for full search |
| Deterministic moves | Stochastic elements |

### Edge Cases & Pitfalls

- **Horizon effect:** Bad moves beyond search depth remain invisible.
- **<abbr title="A function that assigns a score to a game state to determine how favorable it is for a player.">Evaluation function</abbr>:** Poor heuristic defeats perfect search.
- **Transpositions:** Different paths reach same position. Use transposition tables.
- **Memory:** Deep searches exhaust memory. Use iterative deepening.

### Anti-Patterns

- **Omitting alpha-beta pruning:** Full tree expands at <code>O(b^d)</code>. Pruning cuts expansion. Omission makes games intractable.
- **Using minimax for stochastic games:** Minimax requires deterministic perfect-information zero-sum games. Poker or backgammon yield flawed decisions.
- **Poor evaluation function:** Output depends on heuristic quality. Bad heuristic causes systematic blunders. Search depth cannot fix poor evaluation.
- **Ignoring transpositions:** Evaluate reached positions once and cache them. Recomputing multiplies work exponentially.

## 57.5. Quick Reference

| Enhancement | Benefit |
|-------------|---------|
| Alpha-beta pruning | Reduces nodes by ~50% |
| Iterative deepening | Time-bounded search |
| Transposition table | Avoids recomputing states |
| Move ordering | Better pruning with good moves first |

| Go stdlib | Usage |
|-----------|-------|
| No direct stdlib | Implement natively for game AI |


## Quick Reference

| Topic | Recommendation |
|------|-----------------|
| Primary strategy | Prefer the method with proven bounds for your workload. |
| Data size | Benchmark with realistic input distributions. |
| Memory behavior | Favor contiguous layouts where possible. |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 57:</strong> <abbr title="A decision rule used in two-player zero-sum games that minimizes possible loss for a worst-case scenario.">Minimax</abbr> embodies strategic thinking. Algorithm assumes opponent intelligence and plans accordingly. Alpha-beta pruning eliminates impossible branches. Minimax remains foundation of competitive game AI.
{{% /alert %}}

## See Also

- [Chapter 23: <abbr title="A method combining solutions to overlapping subproblems">Dynamic Programming</abbr>](/docs/part-vi/chapter-23/)
- [Chapter 25: <abbr title="Building candidates incrementally and abandoning dead ends">Backtracking</abbr>](/docs/part-vi/chapter-25/)
- [Chapter 58: Mo's Algorithm](/docs/part-xii/chapter-58/)
