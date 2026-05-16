---
weight: 100400
title: "Chapter 53: Tarjan's Bridge-Finding Algorithm"
description: "Tarjan's Bridge-Finding Algorithm"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Bridges are the weakest links in any network.</em>" : Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 53 covers Tarjan's algorithm for finding bridges (cut edges) in undirected graphs. Edges whose removal disconnects the graph are bridges.
{{% /alert %}}

## 53.1. Bridges and Articulation Points

**Definition:** Bridge (cut edge) disconnects graphs upon removal. Articulation point (cut vertex) has identical properties for vertices.

### Why They Matter

| Domain | Bridge Significance |
|--------|---------------------|
| Network design | Single points of failure |
| Road networks | Critical roads |
| Social networks | Key connectors |
| Electrical grids | Vulnerable transmission lines |

## 53.2. Tarjan's Bridge Algorithm

DFS discovery times and low values identify bridges.

```go
func findBridges(graph [][]int, n int) [][]int {
    visited := make([]bool, n)
    disc := make([]int, n)  // Discovery times
    low := make([]int, n)   // Lowest reachable discovery time
    bridges := [][]int{}
    time := 0
    
    var dfs func(u, parent int)
    dfs = func(u, parent int) {
        visited[u] = true
        disc[u] = time
        low[u] = time
        time++
        
        for _, v := range graph[u] {
            if v == parent {
                continue
            }
            if !visited[v] {
                dfs(v, u)
                low[u] = min(low[u], low[v])
                
                // If lowest reachable from v is below u, edge u-v is a bridge
                if low[v] > disc[u] {
                    bridges = append(bridges, []int{u, v})
                }
            } else {
                low[u] = min(low[u], disc[v])
            }
        }
    }
    
    for i := 0; i < n; i++ {
        if !visited[i] {
            dfs(i, -1)
        }
    }
    
    return bridges
}
```

## 53.3. Algorithm Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(V + E) |
| Space | O(V) |
| Visits each edge | Once |

### Key Insight

Edge (u, v) is a bridge if no back edge connects v's subtree to u or higher. Expression `low[v] > disc[u]` validates condition.

## 53.4. Articulation Points

Logic: Vertex u is articulation point if:
- Root has ≥2 children in DFS tree.
- Non-root child v satisfies `low[v] ≥ disc[u]`.

## 53.5. Decision Matrix

| Find Bridges When... | Find Articulation Points When... |
|---------------------|----------------------------------|
| Edge failures matter | Node failures matter |
| Network links analyzed | Server/router failures analyzed |
| Road segments critical | Intersections critical |

### Edge Cases & Pitfalls

- **Multiple edges:** Parallel edges prevent bridge status.
- **Self-loops:** Ignore for bridge detection.
- **Disconnected graph:** Run DFS from every component.

### Anti-Patterns

- **Parent edge confusion:** Skip `v == parent` in DFS. Parent edges are not back edges.
- **Swapping conditions:** Bridges require `low[v] > disc[u]`. Articulation points require `low[v] ≥ disc[u]`.
- **Multi-edge neglect:** Parallel edges negate bridge status. Multiplicity must be handled.
- **Single-source limit:** DFS from all unvisited vertices. Disconnected components require individual seeding.

## 53.6. Quick Reference

| Condition | Meaning |
|-----------|---------|
| low[v] > disc[u] | Edge u-v is a bridge |
| low[v] ≥ disc[u] | Vertex u is articulation point (non-root) |
| Root with 2+ children | Root is articulation point |

| Go stdlib | Usage |
|-----------|-------|
| No direct stdlib | Implement for network analysis |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 53:</strong> Tarjan's algorithm identifies network vulnerabilities. Linear traversal finds every bridge. Algorithm enables reliability planning.
{{% /alert %}}

## See Also

- [Chapter 50: Topological Sort](/docs/part-x/chapter-50/)
- [Chapter 51: Strongly Connected Components](/docs/part-x/chapter-51/)
- [Chapter 12: Graphs and Graph Representations](/docs/part-iii/chapter-12/)
