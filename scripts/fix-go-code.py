#!/usr/bin/env python3
"""Fix Go code blocks that don't compile."""
import re
import os

def fix_ch11():
    with open('content/en/docs/Part-III/Chapter-11.md', 'r') as f:
        content = f.read()
    
    # Fix block 2 (AVL): fmt imported but not used, no main
    # Find the AVL block and add a main() that uses fmt
    content = content.replace(
        '''```go
package main

import (
	"fmt"
	"cmp"
)

type AVLNode''',
        '''```go
package main

import (
	"fmt"
	"cmp"
)

func main() {
	// AVL tree demonstration
	fmt.Println("AVL tree operations")
}

type AVLNode'''
    )
    
    # Fix block 3 (Augmented): no main
    content = content.replace(
        '''```go
package main

import "cmp"

type AugNode''',
        '''```go
package main

import (
	"fmt"
	"cmp"
)

func main() {
	fmt.Println("Augmented BST rank operations")
}

type AugNode'''
    )
    
    with open('content/en/docs/Part-III/Chapter-11.md', 'w') as f:
        f.write(content)
    print("Fixed Ch11")

def fix_ch12():
    with open('content/en/docs/Part-III/Chapter-12.md', 'r') as f:
        content = f.read()
    
    # Fix block 0: add main() to Graph definition block
    content = content.replace(
        '''func (g *Graph) Neighbors(u int) []int {
    return g.adj[u]
}
```''',
        '''func (g *Graph) Neighbors(u int) []int {
    return g.adj[u]
}

func main() {
    g := NewGraph(5)
    g.AddEdge(0, 1)
}
```'''
    )
    
    # Fix block 1: DFS/BFS methods - add Graph type and main
    content = content.replace(
        '''```go
package main

import "container/list"

func (g *Graph) DFS''',
        '''```go
package main

import "container/list"

type Graph struct {
    adj [][]int
}

func (g *Graph) DFS'''
    )
    
    # Fix block 3: Dijkstra - add main
    content = content.replace(
        '''func (h *MinHeap) Pop() any {
    old := *h
    n := len(old)
    *h = old[:n-1]
    return old[n-1]
}
```''',
        '''func (h *MinHeap) Pop() any {
    old := *h
    n := len(old)
    *h = old[:n-1]
    return old[n-1]
}

func main() {
    // Dijkstra demonstration
}
```'''
    )
    
    with open('content/en/docs/Part-III/Chapter-12.md', 'w') as f:
        f.write(content)
    print("Fixed Ch12")

def fix_ch28():
    with open('content/en/docs/Part-VI/Chapter-28.md', 'r') as f:
        content = f.read()
    
    # Fix block 1: remove unused "math" import
    content = content.replace(
        '''import (
    "fmt"
    "math"
    "math/rand"
    "time"
)''',
        '''import (
    "fmt"
    "math/rand"
    "time"
)'''
    )
    
    with open('content/en/docs/Part-VI/Chapter-28.md', 'w') as f:
        f.write(content)
    print("Fixed Ch28")

def fix_ch37():
    with open('content/en/docs/Part-VII/Chapter-37.md', 'r') as f:
        content = f.read()
    
    # Fix block 1: AutoComplete method - add Trie types
    content = content.replace(
        '''```go
package main

import "fmt"

func (t *Trie) AutoComplete''',
        '''```go
package main

import "fmt"

type TrieNode struct {
	Children map[rune]*TrieNode
	IsEnd    bool
}

type Trie struct {
	Root *TrieNode
}

func NewTrie() *Trie {
	return &Trie{Root: &TrieNode{Children: make(map[rune]*TrieNode)}}
}

func (t *Trie) AutoComplete'''
    )
    
    with open('content/en/docs/Part-VII/Chapter-37.md', 'w') as f:
        f.write(content)
    print("Fixed Ch37")

fix_ch11()
fix_ch12()
fix_ch28()
fix_ch37()
print("Done fixing code blocks.")
