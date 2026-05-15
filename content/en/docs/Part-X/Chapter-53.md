---
weight: 100400
title: "Chapter 54 - Tarjan's Bridge-Finding Algorithm"
description: "Tarjan's Bridge-Finding Algorithm"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Bridges are the weakest links in any network.</em>" — Unknown</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 54 covers Tarjan's algorithm for finding bridges (cut edges) in undirected graphs — edges whose removal disconnects the graph.
{{% /alert %}}

## 54.1. Bridges and Articulation Points

**Definition:** A <abbr title="An edge in an undirected graph whose removal increases the number of connected components.">bridge</abbr> (cut edge) is an edge whose removal disconnects the graph. An <abbr title="A vertex whose removal increases the number of connected components.">articulation point</abbr> (cut vertex) is a vertex with the same property.

### Why They Matter

| Domain | Bridge Significance |
|--------|---------------------|
| Network design | Single points of failure |
| Road networks | Critical roads |
| Social networks | Key connectors |
| Electrical grids | Vulnerable transmission lines |

## 54.2. Tarjan's Bridge Algorithm

Using DFS discovery times and low values:

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

## 54.3. Algorithm Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(V + E) |
| Space | O(V) |
| Visits each edge | Once |

### Key Insight

Edge (u, v) is a bridge if and only if no back edge connects v's subtree to u or above. This is precisely what `low[v] > disc[u]` checks.

## 54.4. Articulation Points

Similar logic: vertex u is an articulation point if:
- Root with ≥2 children in DFS tree
- Non-root with `low[v] ≥ disc[u]` for some child v

## 54.5. Decision Matrix

| Find Bridges When... | Find Articulation Points When... |
|---------------------|----------------------------------|
| Edge failures matter | Node failures matter |
| Network links analyzed | Server/router failures analyzed |
| Road segments critical | Intersections critical |

### Edge Cases & Pitfalls

- **Multiple edges:** Parallel edges between two vertices mean neither is a bridge.
- **Self-loops:** Ignore for bridge finding.
- **<abbr title="A graph with vertices not connected by any path">Disconnected graph</abbr>:** Run DFS from each component.

## 54.6. Quick Reference

| Condition | Meaning |
|-----------|---------|
| low[v] > disc[u] | Edge u-v is a bridge |
| low[v] ≥ disc[u] | Vertex u is articulation point (non-root) |
| Root with 2+ children | Root is articulation point |

| Go stdlib | Usage |
|-----------|-------|
| No direct stdlib | Implement for network analysis |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 53:</strong> Tarjan's bridge-finding algorithm exemplifies the power of DFS: a single linear traversal reveals the critical vulnerabilities of an entire network. By tracking discovery times and lowest reachable ancestors, it identifies every bridge in O(V + E) time. In network reliability, infrastructure planning, and system design, knowing your bridges is knowing your risks.
{{% /alert %}}

## See Also

- [Chapter 51 — Topological Sort](/docs/part-x/Chapter-50/)
- [Chapter 52 — Strongly Connected Components](/docs/part-x/Chapter-51/)
- [Chapter 12 — Graphs and Graph Representations](/docs/part-iii/Chapter-12/)

