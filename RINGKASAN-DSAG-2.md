# RINGKASAN DSAG 2 — Panduan Belajar Cepat
## Modern Data Structures and Algorithms in Go

> *Dari RINGKASAN-DSAG.md (10.532 baris) → diringkas untuk belajar dan review cepat*
> *Target: mahasiswa yang sudah baca materi dan butuh pengingat*

---

## 📋 PETA BUKU — 12 Part, 59 Bab

```
┌─────────────────────────────────────────────────────────────┐
│  PART   │  FOKUS                    │  BAB  │  TINGKAT      │
├─────────┼───────────────────────────┼───────┼───────────────┤
│  I      │  Foundations & Go         │  1-4  │  Pemula       │
│  ⚡     │  Deep Dive (Memory, GC…)  │  —    │  Intermediate  │
│  II     │  Basic Data Structures    │  5-8  │  Pemula       │
│  III    │  Trees & Graphs           │ 9-12  │  Intermediate  │
│  IV     │  Graph Algorithms         │ 13-18 │  Intermediate  │
│  V      │  Sorting & Searching      │ 19-21 │  Pemula       │
│  VI     │  Algorithmic Paradigms    │ 22-27 │  Advanced     │
│  VII    │  Advanced Topics          │ 28-38 │  Advanced     │
│  VIII   │  History & Philosophy     │ 39-43 │  Semua        │
│  IX     │  Advanced Data Structures │ 44-49 │  Advanced     │
│  X      │  Advanced Graph           │ 50-53 │  Advanced     │
│  XI     │  Specialized Sorting      │ 54-56 │  Advanced     │
│  XII    │  Advanced Topics          │ 57-59 │  Expert       │
│  🔬     │  Testing & Profiling      │  —    │  Semua        │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ DEEP DIVE: MEMORY & CONCURRENCY GO

### Stack vs Heap — Mana Variable Kamu Tinggal?

| Ciri | Stack | Heap |
|------|-------|------|
| **Kecepatan** | ~1-3ns (geser pointer) | ~100-300ns (cari free block) |
| **Urutan** | LIFO — otomatis | Acak — butuh GC |
| **Ukuran** | 2KB → max 1GB per goroutine | RAM tersedia |
| **Dealokasi** | Instan (SP naik) | Concurrent mark-sweep (~500µs) |
| **Akses CPU** | L1/L2 cache (contiguous) | Tersebar (cache miss) |
| **Keputusan** | Compiler (escape analysis) | Compiler (escape analysis) |

**Kapan variable ke Heap?**
1. Pointer direturn dari fungsi — `return &x`
2. Variable di-assign ke global/interface
3. Closure capture variable
4. Object > 64KB

**Cek sendiri:** `go build -gcflags='-m -m' main.go 2>&1 | grep escapes`

### Pointer Rules
- `&x` = alamat memory | `*p` = nilai di alamat
- Nil pointer dereference = **PANIC SELALU**
- Go **TIDAK** ada pointer arithmetic (beda C/C++)
- Pass by value: semua parameter di-**COPY**
- Mau modify original? Pakai pointer receiver

### Struct Alignment — Order Fields by Size (Largest First)
```go
// ❌ BAD: 24 bytes — 7 bytes padding wasted!
type Bad struct { A bool; B int64; C bool }
// ✅ GOOD: 16 bytes — hemat 33%!
type Good struct { B int64; A bool; C bool }
```

### Goroutine — G-M-P Model
```
G (Goroutine) ~2KB stack  →  M (OS Thread) ~8MB
                 ↑                  ↑
            Go scheduler         Kernel
                 ↓                  ↓
            P (Processor) — logical CPU, GOMAXPROCS (default = NumCPU)

Schedule: work stealing + pre-emption (10ms) + hand-off (syscall)
Create: ~200ns | Switch: ~200ns | Max: 10⁶+ goroutines
```

### Data Race — Silent Killer
```go
counter++ // ❌ DATA RACE: 2 goroutine baca/tulis tanpa sync
// Fix 1: mutex    Fix 2: atomic    Fix 3: channel   Fix 4: ownership
```
**Golden Rule:** `go test -race ./...` **WAJIB** sebelum commit!

---

## 📊 BIG-O QUICK REFERENCE

### Struktur Data — Time & Cache Complexity

```
STRUKTUR         ACCESS   SEARCH   INSERT   DELETE   SPACE    CACHE-FRIENDLY?
──────────────   ───────  ───────  ───────  ───────  ───────  ───────────────
Array            O(1)     O(n)     O(n)     O(n)     O(n)     ✅ Excellent
Stack (slice)    O(n)     O(n)     O(1)*    O(1)     O(n)     ✅ Good
Queue (ring)     O(n)     O(n)     O(1)     O(1)     O(cap)   ✅ Good
Singly Linked    O(n)     O(n)     O(1)     O(1)     O(n)     ❌ Poor (chasing)
Doubly Linked    O(n)     O(n)     O(1)     O(1)     O(n)     ❌ Poor
Hash Table       —        O(1)avg   O(1)avg  O(1)avg  O(n)     ⚠️ Random
BST              O(log n) O(log n) O(log n) O(log n) O(n)     ❌ Poor
AVL/RB Tree      O(log n) O(log n) O(log n) O(log n) O(n)     ❌ Poor
B-Tree (m=100)   O(log n) O(log n) O(log n) O(log n) O(n)     ✅ Good
Binary Heap      O(1)†    O(n)     O(log n) O(log n) O(n)     ✅ Excellent!
Fenwick Tree     —        O(log n) O(log n) —        O(n)     ✅ Excellent!
Segment Tree     —        O(log n) O(log n) O(log n) O(4n)    ✅ Good
Trie             O(L)     O(L)     O(L)     O(L)     O(Σⁿ)    ❌ Random
Bloom Filter     —        O(k)     O(k)     —        O(m)     ❌ Random
Suffix Array     —        O(m log n) —       —        O(n)    ✅ Good
```

*† = peek only | * = amortized

### Sorting — Kapan Pakai yang Mana?

```
SORT             BEST      AVG       WORST     SPACE     STABLE   COCOK UNTUK
──────────────   ────────  ────────  ────────  ────────  ───────  ───────────────────
Bubble           O(n)      O(n²)     O(n²)     O(1)      ✅       Hampir tidak pernah
Selection        O(n²)     O(n²)     O(n²)     O(1)      ❌       Data sangat kecil
Insertion        O(n)      O(n²)     O(n²)     O(1)      ✅       Nearly-sorted ✅
Merge Sort       O(n log n)O(n log n)O(n log n)O(n)      ✅       Linked list, stable
Quick Sort       O(n log n)O(n log n)O(n²)     O(log n)  ❌       Array in-place ✅
Heap Sort        O(n log n)O(n log n)O(n log n)O(1)      ❌       Memory terbatas
Counting         O(n+k)    O(n+k)    O(n+k)    O(k)      ✅       Integer range kecil
Radix            O(dn)     O(dn)     O(dn)     O(n+d)    ✅       Fixed-length string
Bucket           O(n+k)    O(n+k)    O(n²)     O(n)      ✅       Uniform distribution
```

**Go stdlib:** `sort.Slice()` = **pdqsort** — hybrid: quick + heap + insertion sort

### Graph Algorithms

```
ALGORITMA                  TIME              SPACE       KEGUNAAN UTAMA
─────────────────────────  ────────────────  ──────────  ─────────────────────────
DFS                        O(V + E)          O(V)        Cycle detection, topo sort
BFS                        O(V + E)          O(V)        Shortest path (unweighted)
Dijkstra                   O((V+E) log V)    O(V)        Shortest path (non-negative)
Bellman-Ford               O(VE)             O(V)        Negative cycle detection
Floyd-Warshall             O(V³)             O(V²)       All-pairs shortest paths
Kruskal (MST)              O(E log E)        O(V)        MST dengan Union-Find
Prim (MST)                 O((V+E) log V)    O(V)        MST growth-based
Ford-Fulkerson             O(E·max_flow)     O(V²)       Max flow
Edmonds-Karp               O(VE²)            O(V²)       Max flow (BFS augment)
Topological Sort           O(V+E)            O(V)        DAG ordering (Kahn/DFS)
SCC (Kosaraju)             O(V+E)            O(V)        Mutual reachability
SCC (Tarjan)               O(V+E)            O(V)        Single-pass SCC
A* Search                  O(E) h-dep        O(V)        Heuristic shortest path
Bipartite Matching         O(VE)             O(V)        Assignment problems
Tarjan's Bridge            O(V+E)            O(V)        Network reliability
```

### Paradigma Algoritma — Inti

```
PARADIGMA          APPROACH              KAPAN PAKAI              CONTOH KLASIK
─────────────────  ────────────────────  ───────────────────────  ─────────────────
Divide & Conquer   Break→Recur→Combine   Independent subproblems  Merge Sort, Karatsuba
Dynamic Program.   Memoize subproblems   Overlapping subproblems  Knapsack, LCS, Fibonacci
Greedy             Local optimum         Greedy-choice property   Huffman, Activity Selection
Backtracking       Try→backtrack         Constraint satisfaction  N-Queens, Sudoku
Recursion          Self-call             Hierarchical problems    Tree traversal, DFS
Randomized         Probability           Average-case perf        RandQS, Miller-Rabin
```

---

## 📚 RINGKASAN PER PART — INTISARI + KODE + TIPS

### PART I — Foundations (Bab 1-4)
**🧠 Inti:** Algoritma = solusi sistematis. Big-O = alat ukur skalabilitas. Go = bahasa pragmatis untuk DSA.

**💻 Go Vital:**
```go
// Slice itu segalanya di Go
s := make([]int, 0, n)       // Pre-allocate capacity
s = append(s, x)              // May realloc if cap exceeded
sub := s[1:3]                 // SUB-SLICE — shares backing array!
sub[0] = 99                   // MODIFIES s[1]! — side effect berbahaya
// Safe copy:
safe := make([]int, len(sub))
copy(safe, sub)

// Map = hash table built-in
m := make(map[string]int)
val, ok := m["key"]           // ok=false jika tidak ada
delete(m, "key")

// String immutable
s := "Hello, 世界"            // UTF-8
for i, r := range s {         // i = byte offset, r = rune
    fmt.Printf("%c at %d\n", r, i)
}
```

**💡 Tips:**
- Selalu cek `len(arr) == 0` sebelum akses
- Pre-allocate slice dengan `make([]T, 0, n)` — 6× lebih cepat
- Map concurrent access = **PANIC** — pakai `sync.RWMutex` atau `sync.Map`
- Cek escape analysis: `go build -gcflags='-m'`

---

### PART II — Basic Data Structures (Bab 5-8)
**🧠 Inti:** Pilih struktur data berdasarkan ACCESS PATTERN, bukan soal "yang paling keren".

**📋 Decision Matrix Cepat:**

| Kebutuhan | Pilih | Jangan Pilih |
|-----------|-------|--------------|
| Fast index access | **Array/Slice** | Linked List |
| Fast insert/delete middle | **Linked List** | Array |
| Fast lookup by key | **Hash Table (map)** | Array/BST |
| Ordered data | **BST / Slice + sort** | Hash Table |
| FIFO queue | **Ring Buffer** | Slice (shift = O(n)) |
| Memory terbatas | **Array** | Linked List (pointer overhead) |

**💻 Go:**
```go
// Stack
stack := []int{}
stack = append(stack, 42)      // push
val := stack[len(stack)-1]     // peek
stack = stack[:len(stack)-1]   // pop

// Queue (ring buffer — implementasi manual)
type Queue[T any] struct {
    buf  []T
    head, tail, size int
}

// Hash table with chaining
type HashTable[K comparable, V any] struct {
    buckets [][]entry[K, V]
    size    int
}
func (h *HashTable[K, V]) Put(key K, val V) { /* hash → bucket → append */ }
func (h *HashTable[K, V]) Get(key K) (V, bool) { /* hash → bucket → search */ }

// Linked list
type Node[T any] struct {
    Val  T
    Next *Node[T]
}
```

**🐌 Cache Performance:** Array > Ring Buffer > Linked List (pointer chase = 10-100× lebih lambat)

---

### PART III — Trees & Graphs (Bab 9-12)
**🧠 Inti:** Tree = hierarchy. Graph = hubungan bebas. Representasi menentukan performa.

**⚠️ Go GC Pressure:** Setiap node tree = 2 pointer (left, right). 1M node = 2M pointer = GC scan overhead besar. **Alternative:** array-based tree (heap).

**📋 Representasi Graph:**

| Representasi | Space | Edge Lookup | Iterate Neighbors | Cache |
|-------------|-------|-------------|-------------------|-------|
| Adjacency List | O(V+E) | O(deg(v)) | O(deg(v)) | ❌ Scattered |
| Adjacency Matrix | O(V²) | O(1) | O(V) | ✅ Row-contiguous |
| CSR (Compressed) | O(V+E) | O(log deg) | O(deg(v)) | ✅ Sequential |

**💻 BST:**
```go
type TreeNode struct {
    Val   int
    Left  *TreeNode
    Right *TreeNode
}
func insert(root *TreeNode, val int) *TreeNode {
    if root == nil { return &TreeNode{Val: val} }
    if val < root.Val { root.Left = insert(root.Left, val) }
    else if val > root.Val { root.Right = insert(root.Right, val) }
    return root
}
// In-order = sorted!
func inorder(root *TreeNode) {
    if root == nil { return }
    inorder(root.Left)
    fmt.Print(root.Val, " ")
    inorder(root.Right)
}
```

---

### PART IV — Graph Algorithms (Bab 13-18)
**🧠 Inti:** Graph algorithms = shortest path + connectivity + flow. Pilih representasi graph dulu, baru algoritma.

**💻 Dijkstra (Priority Queue):**
```go
func Dijkstra(graph map[int]map[int]int, start int) map[int]int {
    dist := make(map[int]int)
    for v := range graph { dist[v] = math.MaxInt32 }
    dist[start] = 0
    pq := &minHeap{}; heap.Init(pq); heap.Push(pq, item{start, 0})
    for pq.Len() > 0 {
        u := heap.Pop(pq).(item).val
        for v, w := range graph[u] {
            if dist[u]+w < dist[v] {
                dist[v] = dist[u] + w
                heap.Push(pq, item{v, dist[v]})
            }
        }
    }
    return dist
}
```

**💻 Union-Find (Kruskal):**
```go
type DSU struct { parent, rank []int }
func (d *DSU) Find(x int) int {
    if d.parent[x] != x { d.parent[x] = d.Find(d.parent[x]) } // path compression
    return d.parent[x]
}
func (d *DSU) Union(x, y int) {
    x, y = d.Find(x), d.Find(y)
    if d.rank[x] < d.rank[y] { d.parent[x] = y } else { d.parent[y] = x } // union by rank
    if d.rank[x] == d.rank[y] { d.rank[x]++ }
}
```

**📋 Decision Matrix Graph:**

| Masalah | Algoritma | Syarat |
|---------|-----------|--------|
| Shortest path (1 source) | Dijkstra | Non-negative edges |
| Shortest path (negative) | Bellman-Ford | No negative cycle |
| All-pairs shortest | Floyd-Warshall | Dense graph OK |
| Minimum spanning tree | Kruskal / Prim | Undirected |
| Max flow | Ford-Fulkerson / EK | Directed |
| Bipartite matching | Kuhn (DFS) | Bipartite |

---

### PART V — Sorting & Searching (Bab 19-21)
**🧠 Inti:** Sorting fundamental. Go punya `sort.Slice` (pdqsort — jangan tulis ulang). Searching: sorted → binary, unsorted → hash.

**💻 Go Sorting:**
```go
// — Langsung pakai ini, jangan implement manual —
sort.Slice(arr, func(i, j int) bool { return arr[i] < arr[j] })
sort.Ints(arr)                           // untuk []int
sort.Search(n, func(i int) bool { ... }) // binary search
sort.Find(n, func(i int) int { ... })    // Go 1.21+
```

**💡 Kapan implementasi sendiri?** Only for learning. Production = `sort.Slice`.

**Edge Cases Binary Search:**
- Empty array → return 0 (insert position)
- Duplicates → first vs last occurrence
- Target not found → insertion point

---

### PART VI — Algorithmic Paradigms (Bab 22-27)
**🧠 Inti:** 6 cara berpikir untuk menyelesaikan masalah. **DP vs Greedy** = paling sering tertukar.

**📋 Kapan Pilih Paradigma:**

| Ciri Problem | Paradigma |
|-------------|-----------|
| Bisa di-break jadi subproblem INDEPENDEN | Divide & Conquer |
| Subproblem TUMPANG TINDIH + optimal substructure | **Dynamic Programming** |
| Local optimum = global optimum | **Greedy** |
| Cari solusi di ruang pencarian dengan constraint | Backtracking |
| Struktur alami hierarkis | Recursion |
| Deterministic terlalu lambat | Randomized |

**💻 DP — 0/1 Knapsack:**
```go
func knapsack(weights, values []int, cap int) int {
    dp := make([][]int, len(weights)+1)
    for i := range dp { dp[i] = make([]int, cap+1) }
    for i := 1; i <= len(weights); i++ {
        for w := 0; w <= cap; w++ {
            if weights[i-1] <= w {
                dp[i][w] = max(values[i-1]+dp[i-1][w-weights[i-1]], dp[i-1][w])
            } else {
                dp[i][w] = dp[i-1][w]
            }
        }
    }
    return dp[len(weights)][cap]
}
```

**💻 Greedy — Fractional Knapsack:**
```go
type Item struct { Value, Weight int; Ratio float64 }
// Sort by value/weight ratio descending
sort.Slice(items, func(i, j int) bool { return items[i].Ratio > items[j].Ratio })
// Take items in order, fractional if partial
```

**🏋️ Latihan Wajib per Paradigma:**
- D&C: Merge Sort, Quick Sort, Karatsuba
- DP: Fibonacci (3 versi), Knapsack, Coin Change, LCS
- Greedy: Huffman, Activity Selection, Fractional Knapsack
- Backtracking: N-Queens, Sudoku, Subset Sum
- Randomized: Randomized QuickSort, Reservoir Sampling

---

### PART VII — Advanced Topics (Bab 28-38)
**🧠 Inti:** 11 bab dari vektor sampai bit manipulation — ini yang membedakan engineer intermediate dari advanced.

**💻 Fenwick Tree (BIT) — Range Sum Query O(log n):**
```go
type BIT []int
func (t BIT) Update(idx int, delta int) {
    for idx < len(t) { t[idx] += delta; idx += idx & -idx }
}
func (t BIT) Query(idx int) (sum int) {
    for idx > 0 { sum += t[idx]; idx -= idx & -idx }
    return
}
```

**💻 Trie — Prefix Tree:**
```go
type TrieNode struct {
    children [26]*TrieNode  // atau map[rune]*TrieNode untuk Unicode
    isEnd    bool
}
```

**💻 KMP — String Matching O(n+m):**
```go
func buildPrefix(pattern string) []int {
    lps := make([]int, len(pattern))
    for i := 1; i < len(pattern); i++ {
        j := lps[i-1]
        for j > 0 && pattern[i] != pattern[j] { j = lps[j-1] }
        if pattern[i] == pattern[j] { j++ }
        lps[i] = j
    }
    return lps
}
```

**⚠️ Crypto:** Jangan pernah implement kriptografi sendiri di production. Selalu pakai stdlib.

**Cache-Friendly Matrix Multiply:**
```go
// ❌ BAD: i-j-k = stride access (cache miss)
for i := 0; i < n; i++ { for j := 0; j < n; j++ { for k := 0; k < n; k++ { C[i][j] += A[i][k] * B[k][j] } } }
// ✅ GOOD: i-k-j = contiguous access (cache hit)
for i := 0; i < n; i++ { for k := 0; k < n; k++ { for j := 0; j < n; j++ { C[i][j] += A[i][k] * B[k][j] } } }
```

---

### PART VIII — History & Philosophy (Bab 39-43)
**🧠 Inti:** Algoritma = **compressed wisdom** — akumulasi pengalaman ribuan tahun problem-solver.

| Bab | Tokoh/ Konsep | Pelajaran |
|-----|--------------|-----------|
| 39 | Euclid (300 BCE), Al-Khwarizmi (825 CE) | Algoritma bukan penemuan modern |
| 40 | Turing Machine, Therac-25 | Batas komputasi — dan kegagalan bisa fatal |
| 41 | Array (Fortran) → Linked List (1955) → B-Tree (1970) | Abstraksi = tools, bukan tujuan |
| 42 | Amdahl vs Gustafson, Complexity Zoo | Big-O bukan segalanya — cache & I/O juga penting |
| 43 | Reductionism vs Holism | Trade-offs universal. Computational thinking untuk semua |

---

### PART IX — Advanced Data Structures (Bab 44-49)
**🧠 Inti:** Struktur data yang memecahkan masalah spesifik — kapan not found, kapan perlu versioning, kapan harus hemat memory.

| Struktur | Key Concept | Keunggulan | Kelemahan |
|----------|-------------|------------|-----------|
| B-Tree | Banyak keys per node | Disk I/O optimized (height ≤ 3) | Kompleks implementasi |
| Skip List | Random level | Simple, O(log n) expected | Worst-case O(n) |
| Bloom Filter | Bit array + k hashes | Sangat hemat memory | False positive |
| LRU Cache | HashMap + Doubly LL | O(1) get/put | Concurrency needs lock |
| Suffix Array | Sorted suffixes | DNA/text indexing | O(n log n) build |
| Persistent DS | Path copying | Undo/redo, versioning | Memory per version |

**💻 Bloom Filter — Rumus:**
```go
// n = items, p = false positive rate
m := -float64(n) * math.Log(p) / (math.Ln2 * math.Ln2)  // bits
k := m / float64(n) * math.Ln2                           // hash functions
// Contoh: n=100K, p=1% → m≈117KB, k≈7
```

---

### PART X-XII — Advanced Graph, Sorting, Topics (Bab 50-59)
**🧠 Inti:** Algoritma specialized untuk problem tertentu — topological ordering, heuristic search, non-comparison sort, game AI, offline query, dan geometric.

**💻 Kadane — Max Subarray O(n):**
```go
func kadane(arr []int) int {
    maxEnd, maxSoFar := arr[0], arr[0]
    for i := 1; i < len(arr); i++ {
        maxEnd = max(arr[i], maxEnd + arr[i])
        maxSoFar = max(maxSoFar, maxEnd)
    }
    return maxSoFar
}
```

**💻 Sliding Window:**
```go
// Max sum subarray of size k
func maxSumWindow(arr []int, k int) int {
    sum := 0
    for i := 0; i < k; i++ { sum += arr[i] }
    maxSum := sum
    for i := k; i < len(arr); i++ {
        sum += arr[i] - arr[i-k]  // slide: +right, -left
        maxSum = max(maxSum, sum)
    }
    return maxSum
}
```

**💻 A* Search:**
```go
// f(n) = g(n) + h(n)
// g = actual cost from start
// h = estimated cost to goal (heuristic — Manhattan/Euclidean)
// h must be ADMISSIBLE (≤ actual cost) for optimality
```

**💻 Convex Hull — Andrew's Monotone Chain:**
```go
func cross(o, a, b Point) int {
    return (a.X-o.X)*(b.Y-o.Y) - (a.Y-o.Y)*(b.X-o.X)
}
// Sort by X, then Y
// Build lower hull (left→right, cross ≤ 0 = pop)
// Build upper hull (right→left, same rule)
```

---

## 🔬 BONUS: TESTING, BENCHMARKING, PROFILING

### Command Cheatsheet

```
Tujuan                          Perintah
──────────────────────────────  ────────────────────────────────────────────
Test semua modul                go test ./...
Test dengan race detector       go test -race ./...          ← WAJIB!
Test verbose                    go test -v ./...
Test spesifik fungsi            go test -run TestFuncName
Benchmark                       go test -bench=. -benchmem
CPU profile                     go test -cpuprofile=cpu.out
Memory profile                  go test -memprofile=mem.out
Trace                           go test -trace=trace.out
Fuzz testing                    go test -fuzz=. -fuzztime=30s
Coverage                        go test -coverprofile=cover.out
Lihat escape analysis           go build -gcflags='-m' 2>&1
Lihat SSA IR                    GOSSAFUNC=main go build
Lihat assembly                  go tool compile -S main.go
pprof web                       go tool pprof -http=:8080 cpu.out
pprof flame graph               go tool pprof -http=:8080 mem.out
```

### Table-Driven Test Pattern
```go
func TestBinarySearch(t *testing.T) {
    tests := []struct {
        name string
        arr  []int
        target int
        want  int
    }{
        {"found", []int{1,2,3,4,5}, 3, 2},
        {"not found", []int{1,2,3,4,5}, 6, -1},
        {"empty", []int{}, 1, -1},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := binarySearch(tt.arr, tt.target); got != tt.want {
                t.Errorf("got %d, want %d", got, tt.want)
            }
        })
    }
}
```

---

## 🧠 TOP 10 WAJIB DIINGAT UNTUK INTERVIEW

1. **Array vs Linked List** — Array: contiguous O(1) access, cache-friendly. LinkedList: pointer chase O(n), cache-hostile.
2. **HashMap vs BST** — HashMap O(1) avg lookup, unordered. BST O(log n), ordered, range query.
3. **DFS vs BFS** — DFS: stack, deep exploration. BFS: queue, shortest path (unweighted).
4. **DP vs Greedy** — DP: optimal substructure + overlapping. Greedy: local optimum = global (buktikan!).
5. **Quick Sort vs Merge Sort** — Quick: in-place, not stable. Merge: stable, O(n) extra space.
6. **Dijkstra vs Bellman-Ford** — Dijkstra: non-negative only. Bellman-Ford: negative OK, but slower.
7. **Stack vs Heap** — Stack: 1ns, LIFO, no GC. Heap: 100ns, GC, shared.
8. **Pointer vs Value receiver** — Pointer: can modify. Value: copy — lebih cepat untuk data kecil.
9. **Channel vs Mutex** — Channel: communicate. Mutex: protect shared state.
10. **Race detector** — `go test -race ./...` — jalankan selalu.

---

> *"An algorithm must be seen to be believed."* — Donald Knuth
> 
> *RINGKASAN-DSAG-2.md — 16 Mei 2026*
> *Full version: RINGKASAN-DSAG.md (10.532 baris)*
