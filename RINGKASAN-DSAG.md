# Rangkuman Lengkap + Komprehensif DSAG
## Modern Data Structures and Algorithms in Go

> Panduan belajar untuk mahasiswa pemula dan engineer
> 59 Bab, 12 Part — dengan kode Go, ilustrasi nyata, analogi, memory analysis, dan latihan

---

## 📚 PART I — FOUNDATIONS & GO MECHANICS

---

### Bab 1: Peran Algoritma dalam Software Modern

**Definisi:** Algoritma adalah prosedur langkah-demi-langkah yang terdefinisi dengan baik untuk menyelesaikan masalah.

**🎯 Analogi Dunia Nyata:** Algoritma = resep masakan. Resep memberi instruksi jelas (definiteness), harus bisa dieksekusi (effectiveness), dan harus berhenti (finiteness). Seperti resep kue yang memberi tahu urutan campur bahan, panggang, dan dinginkan.

**💻 Contoh Kode Go:**
**📊 Big-O Table:**

| Operasi | Kompleksitas | Penjelasan |
|---------|-------------|------------|
| Cari maksimum | O(n) | Perlu scan semua elemen |
| Cari elemen | O(n) | Linear search |
| Pembuktian kebenaran | O(1) | Algoritma berhenti |

**🧠 Memory Address Impact:**
- Array disimpan di contiguous memory blocks
- Akses berurutan (`arr[0], arr[1], ...`) memanfaatkan **spatial locality** — CPU cache line (biasanya 64 bytes) pre-loads data adjacent
- Lompatan besar (scattered access) menyebabkan **cache miss** — CPU harus fetch dari main memory (RAM), 100× lebih lambat

**📋 Tabel Perbandingan:**

| Aspek | Algoritma | Program | 
|-------|-----------|---------|
| Fokus | Langkah-logis | Eksekusi mesin |
| Bahasa | Pseudocode/manusia | Kode mesin/compiler |
| Contoh | Sorting recipe | `sort.Slice()` |

---

### Bab 2: Analisis Kompleksitas

**Definisi:** Mengukur resource (waktu & memori) yang dibutuhkan algoritma saat input membesar.

**🎯 Analogi:** Big-O seperti speedometer — tidak kasih tahu kecepatan persis, tapi kelas kecepatan. O(1) = "jet", O(n) = "sepeda", O(n²) = "jalan kaki".

**💻 Contoh Kode Go — Hitung Waktu Eksekusi:**
**📊 Master Complexity Classes:**

| Notasi | Nama | n=10 | n=100 | n=1000 | n=10⁶ |
|--------|------|------|-------|--------|-------|
| O(1) | Constant | 1 | 1 | 1 | 1 |
| O(log n) | Logarithmic | 3 | 7 | 10 | 20 |
| O(n) | Linear | 10 | 100 | 1.000 | 10⁶ |
| O(n log n) | Linearithmic | 33 | 664 | 9.966 | 20×10⁶ |
| O(n²) | Quadratic | 100 | 10.000 | 10⁶ | 10¹² |
| O(2ⁿ) | Exponential | 1.024 | 10³⁰ | — | — |

**🧠 Memory Address Impact:**
- **Stack vs Heap:** Variabel lokal → stack (L1 cache cepat). `new()` / `make()` → heap (mungkin di RAM lambat)
- **Pointer chasing:** Linked list → tiap `node.Next()` = potential cache miss. Array → contiguous = cache hit
- **Cache line:** 64 bytes. `arr[0]` load = `arr[0]` sampai `arr[15]` (int64) ikut terload

**📋 Comparison: Asymptotic vs Actual:**

| Aspek | Big-O | Wall-clock time |
|-------|-------|----------------|
| Ukuran | Hardware-independent | Hardware-dependent |
| Tujuan | Pola pertumbuhan | Performa aktual |
| Contoh | O(n²) | 100ms di M4, 200ms di Intel i5 |

---

### Bab 3: Pengantar DSA di Go

**Definisi:** Go dipilih karena kesederhanaan, GC yang mature, goroutines untuk parallelism, dan stdlib yang kuat.

**🎯 Analogi:** Go = Toyota Corolla-nya programming language. Tidak paling glamor, tapi reliable, efisien, dan mudah dirawat.

**💻 Contoh Kode Go:**
**🧠 Memory Impact:**
- `append()` saat capacity penuh → alokasi array baru 2× size → copy O(n) → GC buang array lama
- `map` — buckets dialokasikan di heap, rehash saat load factor > 6.5
- String — slice header (16 bytes: pointer + length). Rune iteration lebih lambat tapi handle Unicode

**📋 Tabel: Go Types vs Memory**

| Type | Stack vs Heap | Size | Zero Value |
|------|--------------|------|------------|
| int | Stack | 8 bytes | 0 |
| string | Stack (header) | 16 bytes | "" |
| slice | Stack (header) | 24 bytes | nil |
| map | Heap (pointer) | 8 bytes | nil |

---

### Bab 4: Fundamental Go untuk Algoritma

**Definisi:** Memory model Go menentukan kapan data di stack vs heap. Escape analysis membuat keputusan ini otomatis.

**🎯 Analogi:** Stack = meja kerja (cepat, terbatas). Heap = gudang (lambat, besar). Compiler = asisten yang memutuskan mana yang ditaruh di meja vs gudang.

**💻 Contoh Kode Go — Escape Analysis:**
**🧠 Memory Impact Detail:**
- **Goroutine stack:** mulai 2KB, tumbuh sesuai perlu (max 1GB). Lebih ringan dari OS thread (1-8MB)
- **Channel:** unbuffered = sinkron (goroutine A kirim, goroutine B terima). Buffered = async sampai penuh
- **GC:** Concurrent mark-sweep. Pause ~500μs. Tapi GC scan root menyebabkan STW singkat
- **Cache coherence:** Multiple goroutines akses data yang sama → cache line bouncing antar core

**📋 Perbandingan Concurrency Model:**

| Aspek | Go Goroutines | OS Threads | Async/Await |
|-------|--------------|------------|-------------|
| Stack | 2KB (grows) | 1-8 MB | N/A |
| Context switch | ~200ns | ~1-10μs | ~1ns |
| Scheduling | M:N (user-level) | 1:1 (kernel) | Cooperative |
| Komunikasi | Channel (CSP) | Mutex/condvar | Promises |

---

## ⚡ DEEP DIVE: GO MEMORY MANAGEMENT & COMPILATION

---

> **Untuk mahasiswa pemula:** Bagian ini menjelaskan DARI NOL bagaimana Go mengelola memory, bagaimana kode kamu di-compile, dan apa yang terjadi di CPU/RAM saat program jalan. Cocok untuk yang baru belajar programming atau ingin memahami "di balik layar" Go.

---

### 1. Memory Stack vs Heap — Fondasi Paling Dasar

**🎯 Analogi Besar:**
- **Stack** = meja kerja kamu di kafe. Cepat, tertata rapi, barang ditaruh dan diambil dari atas (LIFO). Tapi terbatas — kalau penuh, harus pakai kursi sebelah (stack overflow).
- **Heap** = gudang belakang kafe. Luas, bisa taruh apa saja kapan saja. Tapi butuh waktu lebih untuk jalan ke gudang dan cari barangnya.

**Stack — Karakteristik Detail:**
- Setiap goroutine punya **stack sendiri** (mulai 2KB, bisa membesar hingga 1GB)
- Data ditaruh dan dihapus dalam urutan **LIFO** (Last In, First Out)
- Alokasi = **satu instruksi CPU**: geser stack pointer ke bawah (subtract)
- Dealokasi = **satu instruksi CPU**: geser stack pointer ke atas (add)
- **Kecepatan: ~1-3ns** — hanya operasi register
- Compiler WAJIB tahu ukuran data di **compile time** (data statis)
- Tidak bisa untuk data yang ukurannya baru diketahui saat runtime (kecuali fixed-size array)

**Heap — Karakteristik Detail:**
- Data bisa dialokasi dan dibebaskan dalam urutan **APAPUN** (tidak harus LIFO)
- Butuh **Garbage Collector (GC)** untuk membebaskan memory yang tidak terpakai
- Alokasi = cari free block yang cukup besar di heap -> O(n) worst case, rata-rata ~100-300ns
- Bisa untuk data ukuran **APAPUN** (tergantung RAM tersedia)
- Data bisa **dibagi** antar fungsi, goroutine, package tanpa copy
- **Fragmentation** — alokasi/dealokasi acak menyebabkan "lubang" di heap

**💻 Visualisasi Stack vs Heap dengan Memory Address:**
**🖼️ Visual Memory Layout (64-bit Go Runtime):**

```
HIGH ADDRESS
0xFFFF FFFF FFFF ┌──────────────────────────────┐
                  │         KERNEL SPACE          │
                  │   (OS kernel, drivers)        │
0x7FFF FFFF FFFF ├──────────────────────────────┤
                  │         HEAP (grows up)       │
                  │   *b = 99     <- 0xc00000e030 │
                  │   [free space]                │
                  │   [other heap objects]        │
                  ├──────────────────────────────┤
                  │    STACK (grows down)         │
                  │    main() frame:              │
                  │      a = 43                   │
                  │      b = 0xc00000e030         │
                  │    ~~~stack pointer~~~        │ <- SP
                  ├──────────────────────────────┤
                  │    DATA / BSS                 │
                  │    (global vars, constants)   │
                  ├──────────────────────────────┤
                  │    TEXT / CODE                │
                  │    (compiled instructions)    │
0x0000 0000 0000 └──────────────────────────────┘
LOW ADDRESS
```

**PENTING — Kenapa Stack Lebih Cepat?**
1. Stack alokasi = 1 instruksi (`SUB RSP, N`) vs heap = cari free block + bookkeeping
2. Stack 100% contiguous — CPU cache friendly (L1/L2 cache hits)
3. Stack dealokasi = 1 instruksi (`ADD RSP, N`) vs heap = GC harus mark/sweep
4. Stack tidak perlu locking — tiap goroutine punya stack sendiri
5. Stack zero overhead untuk variable yang tidak dipakai lagi

**Pengaruh Deklarasi Variable terhadap Memory:**

**Pengaruh Tipe Data terhadap Memory:**

| Deklarasi | Stack/Heap | Ukuran | Waktu Alokasi |
|-----------|-----------|--------|---------------|
| `var x int` | Stack | 8B | Instant (sub rsp) |
| `var s string` | Stack | 16B header | Instant |
| `s := "hello"` | Stack (header) + Text (data) | 16B + 6B | Instant + link time |
| `s := string(make([]byte, n))` | Heap (data) | Header 16B + n B | Alloc O(n) |
| `p := &Person{}` | Heap | sizeof(Person) | Alloc + GC |
| `sli := []int{1,2,3}` | Stack (header) + Heap (array) | 24B + 24B | Instant + alloc |
| `m := make(map[int]int)` | Heap (hmap) | ~50B + buckets | Alloc O(cap) |
| `ch := make(chan int, 10)` | Heap (hchan) | ~80B + buffer | Alloc |
| `f := func() {}` | Heap (funcval) | ~16B | Alloc (closure) |
| `iface := interface{}(x)` | Heap | 16B header + data | Alloc (boxing) |

---

### 2. Stack Frame Anatomy — Eksekusi Fungsi Step-by-Step

Setiap kali fungsi dipanggil, Go mengalokasi **stack frame** — area di stack yang berisi:
1. **Return address** — alamat instruksi setelah `CALL` (supaya bisa kembali)
2. **Parameters** — argumen fungsi (pass by value = copy)
3. **Local variables** — variable yang dideklarasi di dalam fungsi
4. **Saved base pointer** — frame pointer caller (untuk unwinding)

**Visual Step-by-Step di Memory:**

```
Langkah 0: Sebelum program jalan
[OS Loader]
  - Load binary ke RAM (segmen TEXT, DATA, BSS)
  - Setup initial stack (~1MB untuk main goroutine)
  - Setup heap awal
  - Panggil runtime entry point (rt0_go)
  - Runtime init: scheduler, GC, memory allocator
  - Panggil main.main()

Langkah 1: main() mulai
+-- STACK --+---------+------------------+
|  Address  | Value   | Description      |
+-----------+---------+------------------+
| RSP+0     | [frame] | Stack frame      |
| RSP+8     | 10      | x = 10           |
| RSP+16    | 20      | y = 20           |
| RSP+24    | ???     | sum (belum diisi)|
+-----------+---------+------------------+ <- RSP

Langkah 2: CALL add(x,y) — instruksi CALL terjadi!
  CPU melakukan:
  1. PUSH return_address (alamat instruksi setelah CALL)
     -> RSP turun 8 bytes
  2. JUMP ke alamat fungsi add
  3. Fungsi add prolog:
     -> SUB RSP, N (alokasi frame untuk locals)
  
+-- STACK --+---------+------------------+
| ...       |         | main() locals    |
| RSP+40    | 20      | y (main)         |
| RSP+48    | 10      | x (main)         |
| RSP+56    | ???     | sum (main)       |
+-----------+---------+------------------+
| RSP+32    | [retAd] | Kembali ke main+5| <- return address
| RSP+24    | 10      | a = copy(x)      |
| RSP+16    | 20      | b = copy(y)      |
| RSP+8     | 30      | result = a + b   |
| RSP+0     | [savedBP]| base pointer    |
+-----------+---------+------------------+ <- RSP

Langkah 3: return dari add()
  CPU melakukan:
  1. MOV RAX, result   (return value di register RAX)
  2. ADD RSP, N         (pop stack frame)
  3. POP return_address (atau RET)
  4. JUMP ke return_address

+-- STACK --+---------+------------------+
| RSP+0     | 30      | sum = 30 (dari RAX)| <- RSP
| ...       |         |                   |
+-----------+---------+------------------+

Keuntungan Stack Frame:
- Alokasi = ajust stack pointer (1 instruksi)
- Dealokasi = kembalikan stack pointer (1 instruksi)
- Zero fragmentation
- Excellent cache locality
- Thread-safe (setiap goroutine punya stack sendiri)
```

---

### 3. Pointer (* dan &) — Semua yang Perlu Kamu Tahu

**🎯 Analogi Dasar:** Pointer = alamat rumah. Value = isi rumah. Kamu bisa kirim alamat (pointer) tanpa harus pindahkan seluruh isi rumah.

**📌 Aturan Emas Pointer Go:**
1. `&x` = ambil **alamat memory** dari x
2. `*p` = ambil **nilai** yang ada di alamat p (dereference)
3. Nil pointer = `nil` (bukan 0, bukan address kosong)
4. Dereference nil = **PANIC** (crash program)
5. Go **tidak punya pointer arithmetic** (beda dengan C/C++)

**💻 Level 1: Pointer Dasar**
**💻 Level 2: Pointer ke Struct — Pattern Paling Umum**
**💻 Level 3: Advanced Pointer Patterns**
**💻 Level 4: Pointer Common Pitfalls**
**📊 Pointer vs Value — Panduan Memilih:**

| Situasi | Pakai | Kenapa? |
|---------|-------|---------|
| `int`, `bool`, `float64` | Value | 1-8 bytes, copy murah |
| `struct < 100 bytes` | Value | Copy lebih cepat dari pointer chasing |
| `struct > 100 bytes` | Pointer | Hindari copy mahal |
| Method perlu modify receiver | Pointer | Kalau tidak, perubahan hilang |
| Nil/nullable field | Pointer | `nil` = belum di-set |
| Method receiver kecil | Value | Lebih cache-friendly |
| Method receiver besar | Pointer | Copy besar tiap method call |
| Slice, map, channel | Value | Mereka sudah reference type (header di stack, data di heap) |
| Interface | Value | Interface sudah pointer-like |
| Pool/reuse object | Pointer | sync.Pool butuh pointer |

---

### 4. Go Compilation Flow — Dari .go ke Binary

**🎯 Analogi:** Menulis surat -> kirim ke percetakan (compiler) -> melewati 8 mesin -> jadi buku fisik (binary) -> dibaca orang (CPU).

**🗺️ Peta Lengkap Compilation Pipeline:**

```
main.go (kode sumber)
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 1: LEXING (Scanner)                   │
│                                              │
│ Tokenizes: fmt.Println("Hello")              │
│ Output:                                      │
│   PACKAGE  "main"                            │
│   IMPORT   "fmt"                             │
│   IDENT    "main"                            │
│   LPAREN   "("                               │
│   IDENT    "fmt"                             │
│   PERIOD   "."                               │
│   IDENT    "Println"                         │
│   LPAREN   "("                               │
│   STRING   "\\"Hello\\""                     │
│   RPAREN   ")"                               │
│   RPAREN   ")"                               │
│ File: go/scanner/scanner.go                  │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 2: PARSING                             │
│                                              │
│ Token -> AST (Abstract Syntax Tree)          │
│ Output: Tree of nodes:                       │
│   File -> Package -> FuncDecl -> Block       │
│       -> CallExpr(                           │
│           SelectorExpr(fmt, Println),        │
│           BasicLit("Hello")                  │
│       )                                      │
│                                              │
│ Go parser = recursive descent                │
│ File: go/parser/parser.go                    │
│ Note: Parse errors = COMPILE ERROR           │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 3: TYPE CHECKING                       │
│                                              │
│ Verification:                                │
│  - fmt.Println exists?                       │
│  - fmt.Println accepts string?               │
│  - Types compatible?                         │
│  - Method sets resolved                      │
│  - Implicit conversions                      │
│                                              │
│ Type inference untuk :=                      │
│ Built-in types vs user-defined               │
│ Interface satisfaction check                 │
│ File: go/types/check.go                      │
│ Error: "cannot use X as type Y"              │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 4: ESCAPE ANALYSIS + INLINING          │
│                                              │
│ Decisions:                                   │
│  1. Variable X -> STACK or HEAP?             │
│     Rule: if address taken & returned -> HEAP│
│  2. Function F -> INLINE or not?             │
│     Rule: if small & simple -> INLINE        │
│  3. Closure C -> heap-allocated funcval?     │
│                                              │
│ Output annotations:                          │
│   "x escapes to heap"                        │
│   "f is inlined"                             │
│ File: cmd/compile/internal/escape/           │
│ Lihat: go build -gcflags='-m -m'             │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 5: SSA GENERATION                      │
│ (Static Single Assignment)                   │
│                                              │
│ AST -> SSA IR (Intermediate Representation)  │
│ Setiap variable di-assign TEPAT SATU KALI    │
│ Compiler buat variable baru tiap assignment  │
│                                              │
│ Contoh SSA:                                  │
│   v1 = Const "Hello"                         │
│   v2 = StaticCall fmt.Println(v1)            │
│   v3 = Const 0                               │
│   v4 = Return v3                             │
│                                              │
│ File: cmd/compile/internal/ssa/              │
│ Visualisasi: GOSSAFUNC=main go build         │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 6: 200+ OPTIMIZATION PASSES            │
│                                              │
│ Categories:                                  │
│                                              │
│ 🏃 Loop Optimizations:                       │
│  - Loop unrolling                            │
│  - Loop invariant code motion                │
│  - Loop fusion/split                         │
│  - Bounds check elimination                  │
│                                              │
│ ✂️ Dead Code Elimination:                    │
│  - Hapus variable/block tidak terpakai       │
│  - Hapus unreachable code                    │
│  - Constant folding (2+2 -> 4)              │
│                                              │
│ 🎯 Inlining:                                 │
│  - Ganti function call dengan body langsung  │
│  - Threshold: ~40 statements, ~1-2 complexity│
│                                              │
│ 🔄 Devirtualization:                         │
│  - Interface call -> direct call (jika bisa) │
│  - Hanya 1 implementation -> skip itable     │
│                                              │
│ 📐 Algebraic Simplification:                 │
│  - x*0 -> 0                                  │
│  - x+0 -> x                                  │
│  - x/1 -> x                                  │
│  - x & 0xFF -> hanya 1 byte                  │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 7: CODE GENERATION                     │
│                                              │
│ SSA -> Plan9 assembly (Go's internal format) │
│ -> Machine code (x86-64, ARM64, etc.)        │
│                                              │
│ Register allocation:                         │
│   Yang sering dipakai -> REGISTER            │
│   Yang jarang -> STACK (spill)               │
│                                              │
│ Instruction selection:                       │
│   ADD R1, R2 (jika x86-64)                  │
│   atau ADD R1, R2, R3 (jika ARM)            │
│                                              │
│ Peephole optimization:                       │
│   MOV R1, R2; MOV R2, R3 -> MOV R1, R3      │
│                                              │
│ File: cmd/compile/internal/amd64/            │
│ Lihat: go tool compile -S main.go            │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 8: LINKING                             │
│                                              │
│ 1. Gabung semua .o files                     │
│ 2. Link dengan Go stdlib (static)            │
│ 3. Link dengan C code (cgo)                  │
│ 4. Resolve all symbols (fungsi, global)      │
│ 5. Relocation — fix alamat memory            │
│ 6. Build info, symbol table, DWARF debug     │
│ 7. Output: executable binary                 │
│                                              │
│ Format: ELF (Linux), Mach-O (macOS),         │
│         PE (Windows)                         │
│                                              │
│ Go binary = STATIC (tidak perlu libc)        │
│ Kecuali pakai cgo atau import "C"            │
└─────────────────────────────────────────────┘
    │
    ▼
EXECUTABLE BINARY (ELF/Mach-O/PE)
    │  -------- RUNTIME --------
    ▼
┌─────────────────────────────────────────────┐
│ PHASE 9: PROGRAM LOADING (oleh OS)           │
│                                              │
│ Saat kamu ketik ./program:                   │
│                                              │
│ 1. Kernel baca ELF header                   │
│ 2. Map segmen TEXT (RX) ke memory            │
│ 3. Map segmen DATA (RW) ke memory            │
│ 4. Map segmen BSS (RW, zero-initialized)     │
│ 5. Allocate stack (~1MB awal)                │
│ 6. Setup heap segment                        │
│ 7. Setup page tables (MMU)                   │
│ 8. Jump ke _start (entry point)              │
│                                              │
│ Go Runtime Init (sebelum main()):            │
│   - Init scheduler (G-M-P model)             │
│   - Init memory allocator (tcmalloc-like)    │
│   - Init GC (mark worker, background)        │
│   - Init netpoller (epoll/kqueue)            │
│   - Init goroutine stack (2KB minimum)       │
│   - Panggil init() functions (urutan pkg)    │
│   - Panggil main.main()                      │
└─────────────────────────────────────────────┘
```

**💻 Tools untuk Melihat Compilation:**
```bash
# 1. Lihat SSA Intermediate Representation (BEST)
GOSSAFUNC=main go build main.go
# Buka ssa.html — lihat 30+ passes dari awal sampai akhir

# 2. Lihat Assembly
go tool compile -S main.go | head -100
# Atau: objdump -d program | grep 'main\.main'

# 3. Lihat Escape Analysis
go build -gcflags='-m -m' main.go
# Output: "x escapes to heap", "smallAdd inlined"

# 4. Lihat Optimasi apa yang jalan
go build -gcflags='-d=ssa/prove/debug=1' main.go
# Debug bounds check elimination

# 5. Lihat ukuran binary
go build -o program main.go
size program
# text    data     bss     dec     hex
# 987654  12345   6789   1006788  f5d84

# 6. Lihat link dependencies
go tool link -dumpdep main.o

# 7. Compile saja (tanpa link)
go tool compile main.go
# Output: main.o

# 8. Tanpa optimasi
go build -gcflags='-N -l' main.go
# -N: disable optimizations
# -l: disable inlining
```

---

### 5. Variable Layout & Memory — Detail per Tipe

**🎯 Analogi:** Setiap tipe data punya "ukuran kotak" dan "aturan packing" (alignment) yang berbeda. CPU membaca memory dalam ukuran tetap (4/8 bytes), jadi data harus di-align.

**💻 Sizeof Semua Tipe:**
**💻 Struct Alignment — Kenapa Urutan Field PENTING:**
**💻 Variable Deklarasi dan Memory Impact:**
**📊 Memory Impact Summary Table:**

| Deklarasi | Memori Langsung | Memori Potensial | GC Impact |
|-----------|----------------|-----------------|-----------|
| `var x int` | 8B stack | 0 | None |
| `var s string` | 16B stack (header) | n B text/heap | None (text segmen) |
| `x := 42` | 8B stack | 0 | None |
| `s := "hello"` | 16B stack | 6B text segmen | None |
| `s := make([]int, n)` | 24B stack | 8n B heap | Scan pointer |
| `m := make(map[int]int)` | 8B stack | ~40+n*8 B heap | Scan all buckets |
| `p := &T{}` | 8B stack | sizeof(T) heap | Scan pointer |
| `defer fn()` | ~40B stack | 0 | None (stack) |
| `go fn()` | 2KB+ goroutine stack | Variable | Bergantung |
| `var iface interface{}` | 16B stack | 0-16B heap (boxing) | Type pointer |
| `closure := func(){}` | 16B heap (funcval) | Captured vars heap | Scan captured |

---

### 6. Escape Analysis — Hati Compiler yang Membuat Keputusan

**Definisi:** Escape analysis adalah algoritma compiler yang menentukan apakah suatu variable bisa dialokasi di STACK atau harus di HEAP.

**🎯 Analogi:** Seperti resepsionis hotel yang memutuskan tamu mana yang cukup menginap di lobby (stack) vs perlu kamar (heap). Tamu yang "lolos" dari lobby harus dikelola lebih serius.

**Aturan Dasar:**
- Jika variable **tidak dirujuk** setelah fungsi return -> STACK
- Jika variable **masih dirujuk** setelah fungsi return -> HEAP
- Jika variable **di-address** (`&x`) dan address-nya lolos -> HEAP
- Jika variable **terlalu besar** (>64KB) -> HEAP (terlepas dari analisis)

**💻 6 Kasus Escape Analysis:**
**💻 Mengecek Escape Analysis:**
```bash
# Basic - melihat apa yang escape
go build -gcflags='-m' main.go

# Verbose - detail kenapa
go build -gcflags='-m -m' main.go

# Semua package (termasuk stdlib)
go build -gcflags='-m -m -m' main.go 2>&1 | grep escapes

# Contoh output untuk fungsi sebelumnya:
# ./main.go:5:6: total does not escape
# ./main.go:12:9: &p escapes to heap
# ./main.go:20:2: moved to heap: p
# ./main.go:28:14: x escapes to interface{}
# ./main.go:35:2: count escapes to heap
# ./main.go:35:2: moved to heap: count
```

**📊 Escape Analysis Impact:**

| Keputusan | Stack | Heap |
|-----------|-------|------|
| Kecepatan alokasi | ~1ns | ~100-300ns |
| Dealokasi | Otomatis (instan) | GC cycle (~500us pause) |
| GC overhead | None | Scan pointer + marking |
| Fragmentasi | None | Mungkin |
| Ukuran max | ~1GB per goroutine | RAM tersedia |
| Aman | Ya (LIFO guarantee) | Ya (GC) |

---

### 7. Garbage Collector (GC) — Bagaimana Go Membersihkan Memory

**🎯 Analogi:** GC = petugas kebersihan mall. Dia datang periodik, cek tempat sampah (memory) mana yang tidak dipakai, lalu buang. Tapi dia dateng pas mall lagi rame (program berjalan), jadi harus hati-hati biar tidak ganggu pengunjung.

**Arsitektur GC Go v1.21+:**
- **Concurrent Mark-Sweep** — mayoritas kerja dilakukan BERSAMAAN dengan program
- **Tri-color Marking** — white/grey/black untuk tracking reachable objects
- **Non-generational** — tidak membagi object berdasarkan umur
- **Non-compacting** — tidak memindahkan object (tidak defrag heap)

**💻 Tri-Color Marking Algorithm:**

```
PHASE 1: GC START (triggered by heap growth)
  Semua object di-start sebagai WHITE

PHASE 2: CONCURRENT MARK
  [Program masih jalan!]
  
  Roots (stack variables, globals) -> GREY (ditemukan)
  
  Process GREY objects:
    while GREY queue not empty:
      obj = pop GREY
      for each pointer in obj:
        if pointed object is WHITE:
          mark as GREY (ditemukan, akan diproses)
      mark obj as BLACK (selesai diproses)
  
  Phase ini CONCURRENT — program terus jalan
  Tapi ada WRITE BARRIER:
    Setiap kali program assign pointer:
      if obj is BLACK and new_pointer is WHITE:
        mark new_pointer as GREY (ditemukan tepat waktu)

PHASE 3: MARK TERMINATION (STOP THE WORLD — ~50-100us)
  Hentikan semua goroutines sebentar
  Process remaining GREY objects
  All remaining WHITE objects = GARBAGE (tidak reachable)

PHASE 4: SWEEP (CONCURRENT)
  Free semua WHITE objects (memory kembali ke heap)
  Update free lists
  Update next GC trigger (based on live heap after sweep)

VISUAL:
  [GC Start]  [Concurrent Mark]  [STW]  [Concurrent Sweep]  [Done]
      |              |              |            |             |
      v              v              v            v             v
  Semua       Roots marked,   Sisa GREY    WHITE objects    Heap siap
  WHITE       pointers traced diproses     di-free          dipakai lagi
      
  ---- WAKTU --------> 
  |<-- 70% waktu -->|<1%->|<--- 30% waktu --->|
```

**💻 GC Performance Optimization:**
**📊 GC Metrics:**

| Metrik | Go 1.21+ | Kapan Khawatir |
|--------|----------|----------------|
| Pause (STW) | ~100-500us | > 1ms |
| CPU overhead | ~1-5% total | > 10% |
| GC frequency | ~1-2x per menit | > 10x per detik |
| Heap setelah GC | Live set | Growth > 2x antar GC |
| Allocation rate | — | > 1GB/s |

---

### 8. Goroutine — Lightweight Thread Go

**Definisi:** Goroutine = unit eksekusi ringan yang di-manage oleh Go runtime. Bukan OS thread — lebih murah, lebih cepat create/destroy.

**🎯 Analogi:** 
- OS Thread = truk (berat, mahal, 1-8MB stack)
- Goroutine = sepeda motor (ringan, cepat, 2KB stack)
- Scheduler = polisi lalu lintas yang mengatur ribuan motor di jalan yang sama (OS threads)

**💻 Dasar Goroutine:**
**💻 G-M-P Model — Cara Go Menjadwalkan Goroutine:**

```
G = Goroutine (task yang akan dijalankan)
M = Machine (OS thread — pekerja)
P = Processor (logical CPU — konteks eksekusi)

+----------+     +----------+     +----------+
|   P#0    |     |   P#1    |     |   P#2    |
| local q  |     | local q  |     | local q  |
| [G1,G3]  |     | [G2]     |     | []       |
+----------+     +----------+     +----------+
     |                |                |
+----v----+     +----v----+     +----v----+
| M (thr) |     | M (thr) |     | M (thr) |
+---------+     +---------+     +---------+
     |                |                |
  [CPU 0]         [CPU 1]         [CPU 2]

+---------------------------+
|     GLOBAL QUEUE          |
|  [G5, G6, G7, G8, ...]   |
+---------------------------+

ALUR SCHEDULING:
1. Goroutine baru -> local queue P (atau global queue)
2. M mengambil G dari local queue P
3. G jalan sampai:
   a. Blocking (I/O, channel, mutex, syscall)
   b. Pre-empted (jalan 10ms — scheduler preemption)
   c. Goroutine selesai
4. Jika local queue kosong:
   -> Curi dari P lain (work stealing)
   -> Ambil dari global queue
5. Jika M block (syscall):
   -> P pindah ke M lain (tidak idle)

SCHEDULER DECISIONS:
- work stealing: P dengan antrian kosong curi dari P lain
- hand off: P pindah M saat M block
- pre-emption: Go 1.14+ — non-cooperative preemption via signal
- spinning: M tetap running walau idle (antisipasi goroutine baru)
```

**💻 Goroutine Lifecycle:**
**📊 Goroutine vs OS Thread vs Async/Await:**

| Aspek | Goroutine | OS Thread | Async/Await |
|-------|-----------|-----------|-------------|
| Stack size | 2KB (grows) | 1-8 MB | ~100 bytes |
| Create time | ~200ns | ~10us (syscall) | ~1ns (stack only) |
| Context switch | ~200ns | ~1-10us | ~1ns |
| Max count | 10⁶+ | 10⁴ | 10⁶+ |
| Scheduling | M:N (user) | 1:1 (kernel) | Cooperative |
| Pre-emption | Yes (10ms) | Yes (time slice) | No (await points) |
| Communication | Channel | Shared mem + lock | Promise/Future |
| Stack growth | Yes (copy) | No (fixed) | N/A |

---

### 9. Concurrency di Go — Channel, Select, Sync

**Definisi:** Concurrency = dealing with multiple things at once. Parallelism = doing multiple things at once. Go mendesain concurrency sebagai **first-class citizen**.

**🎯 Analogi:** 
- Concurrency = satu chef memasak 3 menu dengan bergantian (seduh kopi, sambil potong roti, sambil goreng telur)
- Parallelism = 3 chef masing-masing masak 1 menu
- Go mendukung DUA-DUANYA

**💻 Channel — Cara Utama Komunikasi Goroutine:**

**💻 Select — Channel Multiplexing:**
**💻 sync Package — Alternatif Channel:**
**📊 Concurrency Patterns:**

| Pattern | Cara | Kapan Pakai |
|---------|------|-------------|
| Worker Pool | N goroutine, 1 channel job | Banyak task independen |
| Fan-out | 1 input -> N goroutine | Distribusi kerja |
| Fan-in | N input -> 1 channel | Gabung hasil |
| Pipeline | Stage1 -> Stage2 -> Stage3 | Processing berurutan |
| Pub/Sub | Banyak subscriber ke 1 event | Notifikasi |
| Generator | Goroutine produksi data | Streaming/lazy eval |
| Timeout | select + time.After | Batasi waktu operasi |
| Done channel | struct{} channel untuk cancel | Graceful shutdown |
| Rate limit | Ticker + channel buffer | Batasi throughput |

---

### 10. Data Race — Silent Killer Concurrency

**Definisi:** Data race terjadi ketika 2+ goroutine mengakses variable yang SAMA, minimal SATU operasi WRITE, tanpa sinkronisasi.

**🎯 Analogi:** Dua orang mencoba mengisi formulir yang SAMA — satu nulis, satu baca, tanpa antrian. Hasilnya? Bisa kacau!

**💻 Contoh Data Race Klasik:**
**💻 Deteksi Data Race:**
```bash
# Run dengan race detector (compile-time instrumentation)
go run -race main.go

# Test dengan race detector
go test -race ./...

# Build dengan race detector
go build -race -o program main.go

# Race detector overhead:
# - CPU: ~2-20x lebih lambat
# - Memory: ~5-10x lebih banyak
# JANGAN untuk production! Hanya untuk dev/testing.
```

**💻 Output Race Detector:**
```
$ go run -race datarace.go
==================
WARNING: DATA RACE
Write at 0x00c0000b4008 by goroutine 7:
  main.dataRaceExample.func1()
      /Users/user/datarace.go:10 +0x44

Previous read at 0x00c0000b4008 by goroutine 6:
  main.dataRaceExample.func1()
      /Users/user/datarace.go:10 +0x3e

Goroutine 7 (running) created at:
  main.dataRaceExample()
      /Users/user/datarace.go:9 +0x55

Goroutine 6 (finished) created at:
  main.dataRaceExample()
      /Users/user/datarace.go:9 +0x55
==================
Found 1 data race(s)
```

**💻 Fix Data Race:**
**⚠️ Data Race Patterns yang Sering Terjadi:**
**📊 Race Detection Matrix:**

| Akses Goroutine A | Akses Goroutine B | Data Race? |
|-------------------|-------------------|------------|
| Read | Read | **AMAN** |
| Read | Write | **RACE!** |
| Write | Write | **RACE!** |
| Write (mutex) | Write (mutex) | **AMAN** |
| Atomic Read | Atomic Write | **AMAN** |
| Channel send | Channel recv | **AMAN** |
| Map read | Map write (tanpa mutex) | **PANIC!** |

**💻 Best Practices Menghindari Data Race:**

```
GOLDEN RULES:
1. "Do not communicate by sharing memory; instead, share memory by communicating."
   — Go Proverbs (Rob Pike)

2. Setiap variable yang diakses multiple goroutines:
   -> BUTUH SYNCHRONIZATION (channel, mutex, atomic)

3. Race detector bukan optional — jalankan sebelum commit!

4. Untuk stateless workers: pass data via channel, jangan sharing.

5. Untuk stateful data: satu goroutine OWNER, akses via channel.

6. sync.Map untuk map yang jarang write, sering read.

7. atomic untuk counter, flag, dan operasi sederhana.

8. Jika bisa hindari sharing — design stateless!
```

**💻 Concurrent Design Pattern — Ownership:**
---

### Ringkasan Memory Management & Concurrency Go

| Konsep | Inti Pesan |
|--------|-----------|
| **Stack** | Cepat, otomatis, LIFO, ~1ns alloc. Variable lokal di sini |
| **Heap** | Fleksibel, butuh GC, ~100ns alloc. Variable yang "lolos" fungsi |
| **Pointer** | Alamat memory. & = ambil alamat, * = dereference, nil = panic |
| **Escape Analysis** | Compiler otomatis decide stack vs heap. Cek: `-gcflags='-m'` |
| **GC** | Concurrent mark-sweep, tri-color, non-generational, pause < 500us |
| **Alignment** | Struct punya padding — urutan field PENGARUH ke memory size |
| **Zero value** | Semua variable auto zero-initialized (0, "", nil) |
| **Pass by value** | Go selalu copy. Kecuali pakai pointer (alamat) |
| **Goroutine** | 2KB stack, ~200ns create, G-M-P scheduler, work stealing |
| **Channel** | Communicate: unbuffered (sync) vs buffered (async) |
| **Select** | Channel multiplexer — pilih channel siap, timeout, default |
| **Data Race** | 2+ goroutine akses variable sama, 1 write, tanpa sync |
| **Race Detector** | `go run -race` — WAJIB sebelum commit |
| **Atomic/Mutex** | Sinkronisasi: atomic (sederhana), mutex (critical section) |

---

---

## 📚 PART II — BASIC DATA STRUCTURES

---

### Bab 5: Array dan Slice

**Definisi:** Array = fixed-size contiguous memory block. Slice = window/view ke array yang bisa tumbuh.

**🎯 Analogi:** Array = hotel dengan kamar bernomor tetap. Slice = kamar hotel yang bisa diperluas dengan memesan kamar sebelah (kapasitas) atau pindah hotel (realokasi).

**💻 Contoh Kode Go:**
**📊 Big-O & Memory:**

| Operasi | Array | Slice (amortized) | Memory Access |
|---------|-------|-------------------|---------------|
| Access by index | O(1) | O(1) | CPU cache hit (contiguous) |
| Search | O(n) | O(n) | Linear scan |
| Insert at end | — | O(1) amortized | Mungkin realloc |
| Insert at middle | O(n) | O(n) | Shift elements |
| Delete | O(n) | O(n) | Shift elements |

**🧠 Memory Address Impact — DETAIL:**
- Array/slice = **the most cache-friendly data structure in computing**
- Contiguous: `arr[0]` di address X, `arr[1]` di X+8 (int64)
- CPU cache line (64 bytes): load `arr[0]` → otomatis load `arr[0..7]` (8 int64)
- **Sequential access:** ~95% cache hit rate. **Random access:** ~5-20% cache hit rate
- **TLB (Translation Lookaside Buffer):** Page table cache. Halaman 4KB. Satu page = 512 int64. Kontiguitas = TLB friendly
- **VS Linked List:** tiap node bisa di address manapun. `node.Next` = hampir pasti cache miss

**📋 Perbandingan Alokasi:**

| Inisialisasi | Heap vs Stack | Alokasi | Kapan pilih |
|-------------|--------------|---------|-------------|
| `[5]int{1,2,3,4,5}` | Stack (biasanya) | Static | Ukuran fixed |
| `make([]int, n)` | Heap | Dynamic n | n unknown at compile |
| `[]int{...}` | Heap | Dynamic | Inisialisasi literal |
| `new([100]int)` | Heap | Pointer ke array | Return pointer |

### Bab 6: Elementary Data Structures (Stack & Queue)

**Definisi:** Stack = LIFO (Last In First Out). Queue = FIFO (First In First Out).

**🎯 Analogi:** Stack = tumpukan piring — yang terakhir ditaruh, pertama diambil. Queue = antrian kasir — yang datang pertama dilayani pertama.

**📊 Big-O:**

| Operasi | Stack | Queue (Ring Buffer) |
|---------|-------|-------------------|
| Push/Enqueue | O(1) amortized | O(1) |
| Pop/Dequeue | O(1) | O(1) |
| Peek | O(1) | O(1) |
| Search | O(n) | O(n) |

**🧠 Memory Impact:**
- Stack: slice-based, contiguous memory, excellent cache behavior
- Queue: ring buffer dengan head/tail pointer modulo capacity — O(1) tanpa shift
- Stack pointers vs values: pointer = GC scan overhead; value = no GC scan
- Queue wrap-around: modulo operation ~10-20 cycles. Optimasi: `if tail == len { tail = 0 }`

**📋 Perbandingan Implementasi Queue:**

| Method | Enqueue | Dequeue | Memory | Cache |
|--------|---------|---------|--------|-------|
| Slice + append | O(1) amort | O(n) (shift) | O(n) | Poor |
| Ring buffer | O(1) | O(1) | O(cap) | Good |
| Linked list | O(1) | O(1) | O(2n ptr) | Poor |
| Channel | O(1) | O(1) | O(buf) | Concurrent-safe |

**⚠️ Edge Cases:**
- Stack underflow (pop dari stack kosong)
- Queue: full (buffer penuh) vs empty (buffer kosong)
- Ring buffer resize saat kapasitas habis
- Memory leak: slice pop via `s[:len(s)-1]` — backing array tetap hold reference. Set nil untuk pointer

---

### Bab 7: Hashing and Hash Tables

**Definisi:**
Hash table adalah struktur data yang menyimpan pasangan key-value dengan menggunakan fungsi hash untuk memetakan key ke indeks dalam array (bucket array). Akses data dilakukan dalam waktu rata-rata O(1). Implementasi paling umum menggunakan *chaining* (setiap bucket berisi linked list) atau *open addressing* (probe ke bucket berikutnya jika terjadi collision). Di Go, hash table adalah fondasi dari tipe bawaan `map`, namun memahami implementasi manual sangat penting untuk wawasan performa dan debugging.

**🎯 Analogi:**
Bayangkan sebuah **kantor pos** dengan 26 loker (A–Z). Setiap surat dialokasikan ke loker berdasarkan huruf pertama nama penerima. Jika ada dua surat untuk "Andi" dan "Ayu", keduanya masuk loker A — ini *collision*. Petugas pos menumpuk surat dalam loker (chaining), atau mencari loker terdekat yang kosong (open addressing). Fungsi hash adalah aturan "huruf pertama nama" — cepat, tapi bisa menyebabkan banyak surat menumpuk di satu loker (buckets tidak merata).

**💻 Go Code:** Implementasi hash table dengan chaining (generic, complete runnable)

**📊 Big-O:**

| Operasi | Rata-rata | Worst-case |
|---------|-----------|------------|
| Access (search by key) | O(1) | O(n) |
| Search (by key) | O(1) | O(n) |
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |

*Catatan:* Worst-case O(n) terjadi ketika semua key memiliki hash yang sama (collision parah), sehingga hash table merosot menjadi linked list. Praktik yang baik — fungsi hash yang seragam dan rehashing menjaga rata-rata tetap O(1).

**🧠 Memory:**

- **Bucket array:** Array pointer dengan panjang tetap (kapasitas). Setiap bucket berupa pointer ke head linked list. Memori = kapasitas × ukuran pointer.
- **Load factor:** Rasio `size / capacity`. Makin tinggi, makin sering collision. Threshold umum 0.75 (sama seperti Go `map`). Load factor rendah boros memori, load factor tinggi turunkan performa.
- **Rehashing cost:** Saat load factor terlampaui, hash table membuat bucket array baru 2× lebih besar, lalu *rehash* semua elemen. Biaya O(n) — mahal, tapi jarang terjadi (amortized O(1)).
- **Cache behavior:** Buruk dibanding array. Akses ke bucket array mungkin cache-friendly, tetapi *chaining* menyebabkan pointer chasing (node tersebar di heap). CPU cache miss tinggi untuk lookup — ini alasan Go memilih *bucketized* map dengan optimasi cache.
- **GC pressure:** Setiap node adalah alokasi heap terpisah. Dalam chaining, tiap key-value menghasilkan *object* + *pointer*. Semakin banyak node, semakin berat kerja GC. Go map internal mengurangi ini dengan menyimpan key-value secara kontigu dalam bucket.

**📋 Decision Matrix: Hash Table vs BST vs Array**

| Kriteria | Hash Table | BST (self-balancing) | Array (sorted) |
|----------|-----------|---------------------|-----------------|
| Search (avg) | O(1) | O(log n) | O(log n) binary search |
| Search (worst) | O(n) | O(log n) | O(log n) |
| Insert (avg) | O(1) | O(log n) | O(n) (shift) |
| Delete (avg) | O(1) | O(log n) | O(n) (shift) |
| Ordered iteration | Tidak | Ya (in-order) | Ya |
| Range query | Tidak | O(k + log n) | O(k + log n) |
| Memory overhead | Pointer per bucket + node | Pointer per node | Minimal |
| Cache locality | Buruk (chaining) | Buruk (pointer heavy) | Sangat baik |
| Implementasi | Sedang | Kompleks | Sederhana |
| Use case | Lookup by key cepat | Order matters, range query | Data statis, cache penting |

**⚠️ Edge Cases & Pitfalls:**

1. **Collision attacks:** Jika fungsi hash lemah/diketahui, attacker bisa mengirim ribuan key yang menghasilkan hash sama → hash table menjadi O(n) per operasi → DoS. Go `map` menggunakan hash rahasia per-process (SipHash-like) untuk mitigasi. Di implementasi sendiri, pastikan fungsi hash memiliki *avalanche effect* yang baik.
2. **Key tidak comparable:** Go generics membutuhkan constraint `comparable`. Tipe seperti slice, map, function tidak bisa jadi key karena tidak comparable. Gunakan string atau struct tanpa field slice/map.
3. **GC pressure dengan pointers:** Setiap `node` adalah pointer heap. Load factor rendah → banyak bucket kosong, tapi node pointer tetap ada. Untuk data kecil (~integer), pertimbangkan *open addressing* dengan array linear probing (lebih cache-friendly, GC lebih ringan karena tidak ada pointer per node).
4. **Rehash thrashing:** Jika threshold 0.75 dan data berfluktuasi di sekitar batas, rehash bisa terjadi berulang. Solusi: beri *margin* (tidak langsung rehash saat delete) atau gunakan ukuran bucket prime number.
5. **Zero value ambiguity:** `Get()` mengembalikan zero value saat key tidak ditemukan. Caller harus selalu cek `ok` flag; jangan percaya zero value sebagai indikator "tidak ada".
6. **Concurrency:** Implementasi di atas *tidak thread-safe*. Go map bawaan juga tidak. Gunakan `sync.RWMutex` atau `sync.Map` jika perlu concurrent access.

---

### Bab 8: Linked Lists

**Definisi:**
Linked list adalah struktur data linear di mana setiap elemen (node) menyimpan data dan pointer ke node berikutnya (dan sebelumnya untuk doubly linked list). Berbeda dengan array, linked list tidak memerlukan memori kontigu — node dapat tersebar di heap. Kelebihan utamanya: insert dan delete di tengah list adalah O(1) jika sudah memiliki pointer ke node tersebut. Kekurangan: akses acak O(n) dan overhead pointer yang besar. Di Go, linked list jarang digunakan karena slice sudah sangat optimal, tetapi tetap penting dipahami untuk fondasi struktur data lain (queue, deque, adjacency list graph, LRU cache).

**🎯 Analogi:**
Bayangkan **lomba estafet kereta kertas**. Setiap kertas (node) berisi pesan, dan di pojoknya tertulis "lihat kertas berikutnya: Meja B". Peserta membaca pesan lalu mengambil kertas berikutnya dari Meja B. Jika ingin menyisipkan pesan baru di tengah, cukup tulis di kertas baru, ubah petunjuk di kertas sebelumnya. Tidak perlu memindahkan semua kertas — beda dengan tumpukan rapi (array) di mana menyelipkan kertas baru berarti menggeser semua lembar di atasnya.

**💻 Go Code:** Singly + Doubly Linked List generic, compilable, runnable

**📊 Big-O:**

| Operasi | Singly (dengan tail ptr) | Doubly | Array |
|---------|------------------------|--------|-------|
| Access by index | O(n) | O(n) | O(1) |
| Search by value | O(n) | O(n) | O(n) |
| Insert at head | O(1) | O(1) | O(n) (shift) |
| Insert at tail | O(1) | O(1) | O(1)* (amortized) |
| Insert in middle | O(1)† | O(1)† | O(n) |
| Delete at head | O(1) | O(1) | O(n) |
| Delete at tail | O(n)‡ | O(1) | O(1) |
| Delete in middle | O(1)† | O(1)† | O(n) |

*† Jika sudah memiliki pointer ke node.*  
*‡ Singly tanpa tail pointer: O(n); dengan tail pointer tetap butuh prev node, jadi O(n) untuk delete tail.*  
*Catatan: Go slice append amortized O(1), tapi bisa terjadi copy O(n) saat kapasitas penuh.*

**🧠 Memory:**

- **Pointer overhead:** Setiap node menyimpan data + 1 pointer (singly) atau 2 pointer (doubly). Untuk data kecil (int, bool), overhead pointer bisa 2–3× ukuran data itu sendiri. Contoh: `int64` (8 byte) + pointer (8 byte) = 16 byte per node — 100% overhead.
- **Cache behavior:** Sangat buruk. Node dialokasikan secara terpisah di heap, sehingga tidak ada *spatial locality*. Traversal menyebabkan *pointer chasing* — CPU harus menunggu fetch pointer berikutnya dari RAM (cache miss hampir pasti untuk list besar). Sebaliknya, array/slice menyimpan data kontigu, memanfaatkan *prefetching* dan cache line CPU.
- **GC impact:** Setiap node adalah objek heap terpisah. GC Go harus *scan* dan *sweep* semua node. Semakin besar list, semakin berat *pause time*. Untuk list ribuan node, dampak GC masih kecil. Untuk jutaan node, penggunaan memori dan GC pressure signifikan. Pertimbangkan menggunakan `container/list` dari stdlib (double linked list) hanya jika benar-benar butuh insert/delete di tengah sering; jika traversal dominan, lebih baik slice.
- **Arena allocator pattern:** Kadang linked list diimplementasikan dengan *pool* node (pre-allocate array of nodes) untuk mengurangi GC pressure dan meningkatkan cache locality. Ini disebut *arena allocator* — semua node berada di memori kontigu.

**📋 Comparison: Singly vs Doubly vs Circular vs Array**

| Aspek | Singly | Doubly | Circular | Array/Slice |
|-------|--------|--------|----------|-------------|
| Pointer per node | 1 | 2 | 1–2 | 0 |
| Traversal | Forward only | Forward & backward | Perpetual (loop) | Random access |
| Insert/delete head | O(1) | O(1) | O(1) | O(n) |
| Insert/delete tail | O(n)* / O(1)* | O(1) | O(n)* / O(1)* | O(1) amortized |
| Insert with node ptr | O(1) | O(1) | O(1) | N/A |
| Delete with node ptr | Butuh prev | O(1) | Butuh prev | N/A |
| Reverse traversal | Tidak (O(n) stack) | Ya (prev pointer) | Tidak | Ya (index) |
| Memory footprint | Rendah | Sedang | Rendah–Sedang | Rendah (tanpa pointer) |
| Cache locality | Buruk | Buruk | Buruk | Sangat baik |
| Use case | Stack, queue sederhana | LRU cache, deque | Round-robin, game loop | Data umum, akses acak |

*\* Singly dengan tail pointer: delete tail O(n) karena perlu node sebelumnya. Insert tail O(1).*

---

---

## 📚 PART III — TREES, GRAPHS & REPRESENTATIONS

---

### Bab 9: Trees dan Balanced Trees

**Definisi:** Tree = hierarchical data structure dengan root node dan child nodes. Setiap node punya parent (kecuali root).

**🎯 Analogi:** Pohon keluarga. Root = kakek-nenek. Leaf = generasi termuda. Path dari root ke leaf = garis keturunan. Atau: struktur organisasi perusahaan — CEO di root, manager di internal, karyawan di leaf.

**💻 Contoh Kode Go — BST:**
**📊 Big-O:**

| Operasi | BST (balanced) | BST (skewed) | AVL |
|---------|---------------|--------------|-----|
| Search | O(log n) | O(n) | O(log n) |
| Insert | O(log n) | O(n) | O(log n) |
| Delete | O(log n) | O(n) | O(log n) |
| Space | O(n) | O(n) | O(n) |

**🧠 Memory Address Impact — GC PRESSURE:**
- **Setiap node BST punya 2 pointer (left, right)** — untuk n=1M node: 2M pointer = 16 MB
- GC harus SCAN semua pointer ini setiap cycle → **GC pressure tinggi**
- Nodes scattered di heap → **poor spatial locality** → cache misses
- **Alternative:** Array-based tree (heap) = contiguous, cache-friendly, GC-friendly

**📋 Perbandingan Tree Types:**

| Jenis | Balance | Height | Rotation | Aplikasi |
|-------|---------|--------|----------|----------|
| BST | No | O(n) worst | — | Pendidikan, simple |
| AVL | Strict | O(log n) | More | Lookup-heavy (40/60 ratio) |
| Red-Black | Relaxed | O(log n) | Fewer | Write-heavy (Go map internals) |

---

### Bab 10: Heaps dan Priority Queues

**Definisi:** Binary Heap = complete binary tree, array-based, parent ≥ children (max) atau sebaliknya (min).

**🎯 Analogi:** Antrian UGD — pasien kritis (prioritas tinggi) dilayani duluan, bukan yang datang pertama.

**💻 Contoh Kode Go — Min Heap dengan container/heap:**
**📊 Big-O:**

| Operasi | Heap | Penjelasan |
|---------|------|------------|
| Build | O(n) | Bottom-up heapify |
| Insert | O(log n) | Bubble up |
| Extract | O(log n) | Sink down |
| Peek | O(1) | Root |

**🧠 Memory:** **Cache superstar!** Array implisit (kontigu). `i → left=2i+1, right=2i+2`. 100% contiguous = optimal cache.

---

### Bab 11: Self-Balancing Trees (AVL)

**Definisi:** BST dengan balancing otomatis via rotasi untuk height O(log n).

**💻 Go — AVL Rotation:**
**🧠 Memory:** Per node: 2 pointers + height int ≈ 28 bytes (belum alignment). Go GC trace semua pointer.

---

### Bab 12: Graph Representations

**Definisi:** Graph = V vertices + E edges. Directed/undirected, weighted/unweighted.

**🎯 Analogi:** Peta kota. Vertices = kota, edges = jalan. Directed = satu arah. Weighted = jarak.

**📊 Perbandingan Representasi:**

| Aspek | Adjacency List | Adjacency Matrix | Edge List |
|-------|---------------|-----------------|-----------|
| Space | O(V+E) | O(V²) | O(E) |
| Edge lookup | O(deg(v)) | O(1) | O(E) |
| Iterate neighbors | O(deg(v)) | O(V) | O(E) |
| Cache friendly? | No (scattered) | Yes (row-contiguous) | No |
| Best for | Sparse graphs | Dense graphs | Kruskal |

**🧠 Memory:** CSR format = `[]int` data + `[]int` offsets = optimal untuk sparse graph traversal.

---

## 📚 PART IV — GRAPH ALGORITHMS

Panduan ini mencakup 6 bab inti graph algorithms — dari traversal dasar hingga
bipartite matching. Setiap bab menyertakan definisi, analogi, implementasi Go
lengkap (compilable), analisis Big-O, pertimbangan memori, edge cases, decision
matrix, dan latihan. Target pembaca: mahasiswa yang ingin langsung praktik.

---

### Bab 13: Graph Traversal (DFS & BFS)

**Definisi:**
Graph traversal adalah proses mengunjungi setiap vertex dalam graph secara
sistematis. Dua metode fundamental: Depth-First Search (DFS) — eksplorasi
sejauh mungkin sebelum backtrack — dan Breadth-First Search (BFS) — eksplorasi
level-by-level dari sumber.

**🎯 Analogi:**
- **DFS:** Menjelajahi labirin — ambil satu jalur sampai buntu, lalu backtrack.
  Stack (LIFO) mencerminkan sifat "masuk dulu, keluar terakhir".
- **BFS:** Tsunami dari pusat gempa — gelombang melebar secara konsentris.
  Queue (FIFO) mencerminkan sifat "pertama datang, pertama dilayani".

**💻 Go Code — Graph Representation:**

**💻 Go Code — DFS Recursive:**

**💻 Go Code — DFS Iterative (explicit stack):**

**💻 Go Code — BFS dengan Queue:**

**💻 Go Code — Complete Runnable (main + demo):**

**📊 Big-O:**
| Operasi        | Waktu     | Ruang (Adj List) | Ruang (Adj Matrix) |
|----------------|-----------|------------------|---------------------|
| DFS Recursive  | O(V + E)  | O(V) stack       | O(V) stack          |
| DFS Iterative  | O(V + E)  | O(V) stack       | O(V) stack          |
| BFS            | O(V + E)  | O(V) queue       | O(V) queue          |

**🧠 Memory & Cache Behavior:**
- **Adjacency list traversal:** DFS/BFS melompat-lompat antar node neighbor
  yang tidak kontigu di memori → cache misses tinggi pada graph besar.
- **Adjacency matrix traversal:** Iterasi baris kontigu, cache-friendly untuk
  matriks padat. Tapi O(V²) waktu untuk setiap edge check tidak efisien untuk
  graph sparse.
- **Stack (DFS):** LIFO -> jika graph dalam, stack bisa mencapai O(V) —
  berbahaya untuk DFS rekursif pada graph 10⁵+ node (stack overflow).
- **Queue (BFS):** FIFO — maksimum selebar tingkat terluas graph. Bisa O(V).

**🔄 Comparison: DFS vs BFS**

| Aspek            | DFS                          | BFS                          |
|------------------|------------------------------|------------------------------|
| Struktur Data    | Stack (implisit/eksplisit)   | Queue                        |
| Shortest Path    | Tidak (kecuali DAG spesifik) | Ya (unweighted graph)        |
| Space Worst-Case | O(V) (deep graph)            | O(V) (wide graph)            |
| Complete?        | Ya (dengan visited)          | Ya                           |
| Deteksi Siklus   | Natural (back edge)          | Bisa (dengan parent)         |

**Gunakan DFS ketika:** Topological sort, deteksi siklus, connected components,
backtracking, maze solving.
**Gunakan BFS ketika:** Shortest path (unweighted), web crawler (level-order),
social network "degrees of separation", bipartite check.

**⚠️ Edge Cases:**
1. **Disconnected graph:** DFS/BFS hanya menjangkau komponen yang berisi start.
   Untuk menjangkau semua komponen, loop semua vertex dan panggil traversal
   pada yang belum visited — ini menghitung connected components.
2. **Cycle:** Tanpa visited set, traversal infinite loop. Selalu gunakan visited.
3. **Graph kosong (V=0):** Kembalikan slice kosong.
4. **Start vertex tidak ada:** Periksa keberadaan vertex di adjacency list.
5. **Stack overflow (DFS rekursif):** graph 10⁵+ node linear — gunakan DFS
   iteratif.

**📋 Decision Matrix:**

| Requirement                    | DFS | BFS | Notes                  |
|--------------------------------|:---:|:---:|------------------------|
| Shortest path (unweighted)     |  ✗  |  ✓  | BFS level-order        |
| Topological sort               |  ✓  |  ✗  | DFS + finishing time   |
| Connected components           |  ✓  |  ✓  | Sama — pilih sesuai    |
| Detect cycle                   |  ✓  |  ✓  | DFS lebih natural      |
| Backtracking / puzzle solving  |  ✓  |  ✗  | DFS memory lebih kecil |
| Web crawler / level-order      |  ✗  |  ✓  | BFS social network     |
| Bipartite check                |  ✗  |  ✓  | BFS color-based        |
| Memory-constrained (deep)      |  ✗  |  ✓  | BFS queue < DFS stack  |

---

### Bab 14: Single-Source Shortest Paths (Dijkstra)

**Definisi:**
Dijkstra's algorithm mencari jarak terpendek dari satu source vertex ke semua
vertex lain dalam weighted graph dengan **non-negative edge weights**.
Menggunakan greedy strategy — selalu pilih vertex dengan jarak terkecil yang
belun diproses.

**🎯 Analogi:**
Waze / Google Maps — dari posisi Anda, cari rute terpendek ke semua tujuan.
Priority queue = daftar jalan yang diurutkan berdasarkan jarak. Begitu jarak
suatu jalan dipastikan minimal, jalan itu "tidak akan berubah lagi".

**💻 Go Code — Dijkstra dengan container/heap:**

**📊 Big-O:**
| Komponen            | Kompleksitas       | Penjelasan                        |
|----------------------|--------------------|-----------------------------------|
| Waktu (binary heap)  | O((V + E) log V)   | Setiap edge relax push ke heap    |
| Waktu (Fibonacci)    | O(V log V + E)     | Decrease-key O(1) amortized       |
| Ruang                | O(V)               | Dist array + heap maks O(V)       |

**🧠 Memory: Priority Queue Heap Cost**
- `container/heap` di Go adalah binary heap — O(V) ruang untuk heap itu sendiri.
- Setiap relax bisa push duplikat entry. Dengan pemeriksaan "outdated entry"
  (lihat `if cur.dist > dist[u]`), heap bisa membesar hingga O(E) entries.
- **Cache behavior:** heap array kontigu di memori, cukup cache-friendly.
  Tapi graph adjacency list traversal tetap scattered cache misses.

**⚠️ Edge Cases:**
1. **Negative edges:** Dijkstra **gagal** — setelah node diproses, jalur
   negatif bisa memperpendek jarak node lain. Contoh: edge -5 akan membuat
   node yang sudah "diproses" mendapatkan jarak lebih pendek, tapi tidak
   diproses ulang.
2. **Disconnected graph:** Vertex tak terjangkau memiliki `dist = MaxInt32`.
   Path reconstruction akan menghasilkan `[-1]` atau path kosong.
3. **Self-loops:** Tidak masalah (jarak 0), tapi harus diabaikan saat relax.
4. **Unreachable nodes:** Tidak akan pernah masuk heap — dist tetap infinity.
5. **Graph kosong (V=0):** Map kosong, Dijkstra tidak crash.

**📋 Decision Matrix: Dijkstra vs Bellman-Ford**

| Requirement                    | Dijkstra    | Bellman-Ford |
|--------------------------------|-------------|--------------|
| Negative edges                 | ✗ Gagal     | ✓ Berhasil   |
| Negative cycle detection       | ✗           | ✓            |
| Waktu rata-rata                | O((V+E)logV)| O(VE)        |
| Waktu worst-case               | O((V+E)logV)| O(VE)        |
| Implementasi                   | Sedang (heap)| Mudah       |
| Cocok untuk sparse graph       | ✓           | ✗ (lambat)   |
| Cocok untuk dense graph        | ✓           | ✗            |
| Shortest path DAG              | ✓           | ✓            |

**Gunakan Dijkstra** ketika semua edge weight >= 0 (95% kasus nyata).
**Gunakan Bellman-Ford** ketika ada negative edges atau perlu deteksi
negative cycle (misal: currency arbitrage detection).

---

### Bab 15: All-Pairs Shortest Paths (Floyd-Warshall)

**Definisi:**
Floyd-Warshall algorithm menghitung shortest path antara **semua pasangan
vertex** dalam satu run. Menggunakan dynamic programming: incrementally
memperbaiki jarak dengan mempertimbangkan vertex perantara (intermediate
vertex).

**🎯 Analogi:**
Bikin tabel jarak antar kota di peta. Mula-mula hanya direct route. Lalu
satu per satu pertimbangkan "kalau lewat kota X, apakah lebih pendek?".
Ulangi sampai semua kota jadi intermediate.

**💻 Go Code — Floyd-Warshall DP + Path Reconstruction:**

**📊 Big-O:**
| Komponen            | Kompleksitas | Penjelasan                 |
|----------------------|--------------|----------------------------|
| Waktu                | O(V³)        | Tiga nested loop (k, i, j) |
| Ruang (dist)         | O(V²)        | Matriks V×V                |
| Ruang (next)         | O(V²)        | Path reconstruction        |
| Total ruang          | O(V²)        | ~ 2×V² ints                |

**🧠 Memory: Contiguous Row Access**
- Matriks `dist[i][j]` disimpan row-major (baris kontigu di memori).
- Loop order `k→i→j` mengakses `dist[i][k]` (scattered) dan `dist[k][j]`
  (strided) — ini **cache-unfriendly** untuk V besar.
- Optimasi: tuntuk V=10⁴, matriks = 4×10⁸ bytes ≈ 800 MB (int32) atau
  1.6 GB (int64) — **tidak feasible**. Gunakan Johnson's algorithm untuk
  graph sparse besar.

**⚠️ Edge Cases:**
1. **Negative cycle:** Setelah Run(), periksa `dist[i][i] < 0` — jika true,
   shortest path tidak terdefinisi (bisa diperpendek terus).
2. **No path:** `dist[i][j] == INF` — path reconstruction return nil.
3. **Directed graph:** Floyd-Warshall secara natural untuk directed.
   Untuk undirected, tambahkan edge bolak-balik.
4. **Overflow:** `INF + w` bisa overflow int — guard dengan `if dist[i][k] != INF`
   seperti di kode.

**📋 Decision Matrix: Floyd-Warshall vs Johnson vs V×Dijkstra**

| Requirement               | Floyd-Warshall | Johnson | V×Dijkstra |
|---------------------------|:--------------:|:-------:|:----------:|
| Graph dense               | ✓ (terbaik)    | ✗       | ✗          |
| Graph sparse (V=10⁴,E~V)  | ✗              | ✓       | ✓          |
| Negative edges            | ✓              | ✓       | ✗          |
| Negative cycle detection  | ✓ (otomatis)   | ✓       | ✗          |
| Implementasi              | Sederhana      | Rumit   | Sedang     |
| Path reconstruction       | Mudah          | Mudah   | Mudah      |
| Waktu (dense V=500)       | ~125M ops      | ~3M ops | ~1.5M ops  |

---

### Bab 16: Minimum Spanning Trees

**Definisi:**
Minimum Spanning Tree (MST) adalah subset edge dari connected, undirected,
weighted graph yang menghubungkan semua vertex dengan total weight minimum
dan tanpa cycle. Dua algoritma klasik: Kruskal (greedy edge-based, pakai
Union-Find) dan Prim (greedy vertex-based, pakai priority queue).

**🎯 Analogi:**
**Kruskal:** Memasang kabel fiber optik antar kota — pilih kabel termurah
yang belum menghubungkan dua jaringan yang sudah terhubung (cek sirkuit).
**Prim:** Membangun jaringan dari satu kota — setiap kali tambahkan kota
terdekat yang belum terjangkau.

**💻 Go Code — Kruskal (Union-Find):**

**💻 Go Code — Prim (Priority Queue):**

**📊 Big-O:**

| Algoritma | Waktu          | Ruang   | Catatan                  |
|-----------|----------------|---------|--------------------------|
| Kruskal   | O(E log E)     | O(V)    | Sorting edge → dominan   |
| Prim (heap)| O((V+E) log V)| O(V)    | Sama seperti Dijkstra    |
| Prim (naive)| O(V²)        | O(V)    | Untuk dense graph lebih baik |

**🧠 Memory:**
- **Kruskal:** Union-Find array `parent` + `rank` = contiguous, cache-friendly,
  GC-friendly. Sorting edge O(E log E) — butuh O(E) space untuk edge list.
- **Prim:** Priority queue (heap) O(V). Adjacency list O(V+E) — scattered
  cache misses serupa Dijkstra.

**⚠️ Edge Cases:**
1. **Disconnected graph:** Kruskal menghasilkan MST hanya untuk satu komponen
   (edge count < V-1). Prim visited[] akan false untuk vertex tak terjangkau.
   Deteksi: setelah algoritma, cek jumlah edge MST == V-1.
2. **Graph dengan 1 vertex:** MST = 0 edge, total = 0.
3. **Multiple edges same weight:** Kedua algoritma menghasilkan MST yang sama
   atau berbeda (equally valid). Pilih urutan stabil agar reproducible.
4. **Self-loop:** Edge (u, u) tidak berguna untuk MST — skip.

**📋 Decision Matrix: Kruskal vs Prim**

| Requirement                    | Kruskal      | Prim            |
|--------------------------------|:------------:|:---------------:|
| Graph sparse (E ~ V)           | ✓ (sort E)   | ✓ (heap)        |
| Graph dense (E ~ V²)           | ✗ (sort E²)  | ✓ (naive O(V²)) |
| Implementasi                   | Mudah (+DSU) | Sedang (+heap)  |
| Parallel-friendly              | ✓ (sort + UF)| ✗ (sequential)  |
| Dynamic / incremental edge add | ✓ (UF adaptif)| ✗                |
| Directed graph                 | ✗            | ✗               |
| Single-component detection     | Parsial      | Otomatis        |

---

### Bab 17: Network Flow (Max Flow)

**Definisi:**
Maximum Flow problem: berapa banyak "aliran" (flow) maksimum yang bisa
dikirim dari source (s) ke sink (t) pada directed weighted graph (network),
dengan kapasitas edge sebagai batas atas. Flow harus memenuhi:
- **Capacity constraint:** flow pada edge ≤ kapasitas
- **Flow conservation:** flow masuk = flow keluar (kecuali s dan t)

**🎯 Analogi:**
Pipa air dari reservoir (source) ke kota (sink). Setiap pipa punya diameter
maksimal (kapasitas). Berapa banyak air yang bisa dikirim? Cari jalur
"augmenting path" yang masih punya sisa kapasitas, sampai tidak ada lagi.

**💻 Go Code — Edmonds-Karp (BFS-based Ford-Fulkerson):**

**📊 Big-O:**

| Algoritma          | Waktu            | Ruang    | Catatan                           |
|--------------------|------------------|----------|-----------------------------------|
| Ford-Fulkerson     | O(E · max_flow)  | O(V+E)   | Tergantung kapasitas (bisa besar) |
| Edmonds-Karp (BFS) | O(V · E²)        | O(V+E)   | BFS → shortest augmenting path    |
| Dinic              | O(V² · E)        | O(V+E)   | Level graph + blocking flow       |
| Dinic (unit cap)   | O(min(V^{2/3},√E)·E)| O(V+E)| Khusus matching bipartit        |

**🧠 Memory:**
- Residual graph adjacency list: setiap edge asli → 2 entries (forward + reverse).
  Total O(2E) = O(E) entries.
- Parent array untuk BFS O(V).
- **Cache:** scattered adjacency list traversal — serupa DFS/BFS.

**⚠️ Edge Cases:**
1. **Disconnected s dan t:** MaxFlow = 0 (BFS gagal menemukan path).
2. **Graph kosong (0 edge):** Flow = 0.
3. **Kapasitas 0:** Edge dengan cap=0 tidak berguna — skip oleh BFS.
4. **Kapasitas besar:**
   - Ford-Fulkerson naive (DFS tanpa BFS) bisa lambat jika kapasitas besar.
   - Edmonds-Karp dengan BFS lebih aman O(V·E²).
5. **Multiple sources/sinks:** Tambah super-source dan super-sink dengan edge
   kapasitas tak-terhingga.

**📋 Decision Matrix: Max Flow Algorithms**

| Requirement                 | Ford-Fulkerson | Edmonds-Karp | Dinic     |
|----------------------------|:--------------:|:------------:|:---------:|
| Implementasi               | Mudah          | Mudah        | Sedang    |
| Worst-case guarantee       | ✗ (tergantung) | ✓ O(V·E²)   | ✓ O(V²·E) |
| Unit capacity graph        | ✓              | ✓            | ✓ (cepat) |
| Bipartite matching         | ✓              | ✓            | ✓ (terbaik)|
| Real-time / small graph    | ✓ (paling cepat)| ✓           | ✗ overhead|

---

### Bab 18: Bipartite Matching

**Definisi:**
Bipartite graph adalah graph yang vertex-nya bisa dibagi dua himpunan
disjoint (U dan V) sehingga setiap edge menghubungkan vertex U ke V.
Bipartite Matching mencari sebanyak mungkin pasangan (U-V) tanpa ada vertex
yang dipakai dua kali. Algoritma klasik: augmenting path DFS (Kuhn algorithm).

**🎯 Analogi:**
Assign pekerja ke tugas: setiap pekerja punya skill tertentu (edge), setiap
tugas hanya perlu satu pekerja. Cari assignment maksimal — sebanyak mungkin
tugas selesai. Jika seorang pekerja tidak bisa dapat tugas, cek apakah
ada pekerja lain yang bisa "rela" memberi tugasnya (augmenting path).

**💻 Go Code — Augmenting Path DFS (Kuhn Algorithm):**

**📊 Big-O:**

| Operasi                      | Kompleksitas | Penjelasan                          |
|------------------------------|:------------:|-------------------------------------|
| Kuhn (augmenting path DFS)   | O(V · E)     | Setiap left vertex DFS O(E)         |
| Hopcroft-Karp                | O(√V · E)    | BFS level graph + DFS multiple path |
| Max Flow matching (Dinic)    | O(√V · E)    | Unit capacity → lebih cepat         |

**🧠 Memory:**
- `matchR` array: O(V) ints.
- `seen` array per DFS: O(V) — dialokasikan ulang setiap iterasi (bisa
  dioptimasi dengan `visID` counter untuk menghindari alloc).
- Adjacency list: O(V+E).
- **Cache:** pencarian augmenting path scattered — standard graph traversal.

**⚠️ Edge Cases:**
1. **Graph kosong (0 edge):** Matching = 0.
2. **Vertex tanpa edge:** Tidak pernah matched.
3. **Himpunan tidak seimbang:** |U| ≠ |V|. Matching maksimal = min(|U|,|V|).
4. **Multiple components:** Algoritma tetap bekerja (DFS traverses reachable
   graph).
5. **Complete bipartite graph:** Matching maksimal = min(|U|,|V|).

**📋 Decision Matrix: Bipartite Matching Algorithms**

| Requirement                    | Kuhn (DFS)  | Hopcroft-Karp | Max Flow (Dinic) |
|--------------------------------|:-----------:|:-------------:|:----------------:|
| Implementasi                   | Sangat mudah| Sedang        | Rumit            |
| Worst-case time                | O(V·E)      | O(√V·E)       | O(√V·E)          |
| Cocok V=10³, E=10⁵            | ✓           | ✓ (lebih cepat)| ✓                |
| Cocok V=10⁵, E=10⁶            | ✗ (lambat)  | ✓             | ✓                |
| Path reconstruction            | Mudah       | Mudah         | Perlu flow edge  |
| Weighted matching              | ✗           | ✗             | Min-cost max-flow|

---

> **Lanjut ke PART V — Sorting & Searching (Bab 19-22)**

## 📚 PART V — SORTING & SEARCHING

---

### Bab 19: Basic Sorting

| Sort | Best | Average | Worst | Space | Stable |
|------|------|---------|-------|-------|--------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes |

**🎯 Analogi:** Bubble = gelembung naik. Selection = pilih kartu terkecil. Insertion = masukin kartu ke posisi di tangan.

**🧠 Memory:** Semua in-place O(1) extra space. Bubble shift = contiguous writes. Selection swap = minimal writes.

---

### Bab 20: Advanced Sorting

| Sort | Time | Space | Stable | Analogi |
|------|------|-------|--------|---------|
| Merge Sort | O(n log n) | O(n) | Yes | Divisi & merger perusahaan |
| Quick Sort | O(n log n) avg | O(log n) | No | Pilih pivot, kiri-kanan |
| Heap Sort | O(n log n) | O(1) | No | Extract dari heap |

**🎯 Analogi Merge Sort:** Dokumen besar dibagi 2 terus sampai 1 halaman, lalu digabung berurutan.

**🧠 Memory:**
- Merge Sort O(n) extra: alokasi array temporer. Untuk n=10M = 80MB. Bisa jadi masalah
- Quick Sort in-place: pindah-pindah elemen dalam array yang sama. Cache-friendly. Tapi pivot buruk = O(n²)
- Go `sort.Slice()` = pdqsort (Pattern-defeating Quick Sort). Hybrid: quick + heap + insertion

**💻 Go:**
---

### Bab 21: Searching

| Search | Time | Syarat | Analogi |
|--------|------|--------|---------|
| Linear | O(n) | — | Cari baju di lemari |
| Binary | O(log n) | Sorted | Cari nama di buku telepon |
| Interpolation | O(log log n) | Sorted + uniform | Cari di dictionary |

**💻 Go:**
---

## 📚 PART VI — ALGORITHMIC PARADIGMS

> Enam paradigma besar yang membentuk cara berpikir algoritmik: Divide & Conquer, Dynamic Programming, Greedy, Backtracking, Advanced Recursion, dan Randomized Algorithms. Target: mahasiswa yang baru belajar paradigma algoritma.

---

### Bab 22: Divide and Conquer

**Definisi:**
Divide and Conquer memecah masalah menjadi subproblem independen yang lebih kecil, menyelesaikannya secara rekursif, lalu menggabungkan hasilnya. Berlaku jika subproblem bersifat **non-overlapping** dan **independen**.

**🎯 Analogi:**
Seperti seorang jenderal yang membagi pasukan musuh menjadi kelompok-kelompok kecil, mengalahkan masing-masing secara terpisah, lalu menggabungkan kemenangan. Atau seperti memecah cokelat batangan besar menjadi potongan kecil, memakannya satu per satu.

**📊 Master Theorem:**
Untuk recurrence `T(n) = aT(n/b) + f(n)`:
| Case | Condition | Complexity |
|------|-----------|------------|
| 1 | `f(n) = O(n^(log_b a - ε))` | `T(n) = Θ(n^(log_b a))` |
| 2 | `f(n) = Θ(n^(log_b a) * log^k n)` | `T(n) = Θ(n^(log_b a) * log^(k+1) n)` |
| 3 | `f(n) = Ω(n^(log_b a + ε))` & `af(n/b) ≤ cf(n)` | `T(n) = Θ(f(n))` |

Contoh: Merge Sort → `T(n) = 2T(n/2) + O(n)` → Case 2 → `O(n log n)`

**💻 Go Code: Merge Sort**

**💻 Go Code: Quick Sort (in-place)**

**💻 Go Code: Counting Inversions**

**📋 Comparison: Divide & Conquer vs DP vs Greedy**
| Aspect | Divide & Conquer | Dynamic Programming | Greedy |
|--------|-----------------|-------------------|--------|
| Subproblems | Independent, non-overlapping | Overlapping | Single path |
| Decision | All subproblems solved | All subproblems solved | One choice per step |
| Optimality | Always optimal | Always optimal | Sometimes optimal |
| Example | Merge Sort | 0/1 Knapsack | Fractional Knapsack |
| Time | `O(n log n)` typical | `O(n * W)` typical | `O(n log n)` sorting |

**🧠 Memory Impact:**
- Setiap pemanggilan rekursif push stack frame baru. Go punya goroutine stack 2KB yang grow dynamic, aman untuk depth `O(log n)`.
- Merge Sort alokasi array baru `O(n)` auxiliary space.
- Quick Sort in-place hanya `O(log n)` stack space.
- Slice split di Go hanya copy 24-byte slice header (pointer, length, capacity) — O(1) memory operation.

---

### Bab 23: Dynamic Programming

**Definisi:**
Dynamic Programming (DP) menyelesaikan masalah dengan memecahnya menjadi subproblem yang **tumpang tindih (overlapping)**, menyelesaikan setiap subproblem sekali, dan menyimpan hasilnya untuk digunakan kembali. Syarat: **optimal substructure** dan **overlapping subproblems**.

**🎯 Analogi:**
Seperti mendaki gunung dengan membuat base camp di ketinggian tertentu. Daripada turun ke bawah setiap kali (rekursi naif), kamu menyimpan persediaan di base camp (memoization) untuk perjalanan selanjutnya. Atau seperti mengisi tabel spreadsheet di mana sel yang satu bergantung pada sel sebelumnya.

**💻 Go Code: Fibonacci (3 Versi)**

**💻 Go Code: 0/1 Knapsack**

**💻 Go Code: Longest Common Subsequence (LCS)**

**💻 Go Code: Coin Change (minimum coins)**

**📋 DP vs Greedy Decision Matrix**
| Criteria | Dynamic Programming | Greedy |
|----------|-------------------|--------|
| Overlapping subproblems | Required | Not required |
| Reconsider decisions | Yes (explores all) | Never looks back |
| Optimal for | 0/1 Knapsack, LCS, Edit Distance | Fractional Knapsack, Huffman |
| Time complexity | Usually higher (table filling) | Usually faster (sort + scan) |
| Space complexity | O(n) to O(n^2) table | O(1) or O(n) auxiliary |

**🧠 Memory Impact:**
- DP table untuk LCS: O(m*n) memory. Untuk string panjang, ini bisa puluhan MB.
- State reduction: jika dp[i] hanya butuh dp[i-1], cukup simpan 2 baris (row reduction).
- Di Go, `[][]int` alokasi slice of slices → scattered memory, banyak cache misses.
- Bottom-up lebih efisien memori daripada top-down (tidak ada call stack overhead).

---

### Bab 24: Greedy Algorithms

**Definisi:**
Greedy algorithm membangun solusi piece-by-piece, selalu memilih pilihan yang memberikan keuntungan paling besar saat itu juga. Tidak pernah mempertimbangkan ulang keputusan. Hanya bekerja jika masalah memiliki **greedy-choice property** dan **optimal substructure**.

**🎯 Analogi:**
Seperti anak kecil di prasmanan yang langsung mengambil kue terbesar tanpa memikirkan apakah nanti masih ada sisa tempat untuk makanan lain. Atau seperti investor yang selalu membeli saham dengan keuntungan harian tertinggi tanpa melihat portofolio jangka panjang.

**📊 When Greedy Works vs Fails**
| Problem | Greedy? | Alasan |
|---------|---------|--------|
| Fractional Knapsack | ✅ Ya | Bisa ambil pecahan |
| Activity Selection | ✅ Ya | Earliest finish time |
| Huffman Coding | ✅ Ya | Prefix-free binary code |
| Minimum Spanning Tree | ✅ Ya | Kruskal/Prim |
| Dijkstra (non-negatif) | ✅ Ya | Shortest path |
| 0/1 Knapsack | ❌ Tidak | Harus integer, tidak bisa pecahan |
| Coin Change (arbitrary) | ❌ Tidak | Kadang butuh koin lebih sedikit |
| Traveling Salesman | ❌ Tidak | Global optimum perlu exhaustive |

**💻 Go Code: Fractional Knapsack**

**💻 Go Code: Activity Selection**

**💻 Go Code: Huffman Coding**

**🧠 Memory Impact:**
- Greedy biasanya butuh sorting dulu: O(log n) auxiliary space (Quick Sort).
- Setelah sorting, fase greedy adalah linear scan O(n) — sequential access pattern bagus untuk CPU cache.
- Huffman Coding: priority queue dengan O(n) node di heap.

---

### Bab 25: Backtracking

**Definisi:**
Backtracking adalah pendekatan brute-force yang disempurnakan — membangun solusi secara inkremental dan menghentikan eksplorasi begitu partial solution melanggar constraint (pruning). Ekivalen dengan depth-first search di ruang solusi.

**🎯 Analogi:**
Seperti mencari jalan keluar dari labirin dengan menggulung benang (seperti Theseus). Ketika mencapai jalan buntu, kamu mundur ke persimpangan terakhir dan coba jalur lain (backtrack). Atau seperti bermain catur dan "membatalkan" langkah ketika strategi terbukti buruk.

**💻 Go Code: N-Queens**

**💻 Go Code: Sudoku Solver**

**💻 Go Code: Subset Sum (dengan pruning)**

**🧠 Memory Impact:**
- Backtracking menggunakan call stack untuk merepresentasikan search space tree.
- Di Go, passing slice pointer atau mutating shared slice menghindari alokasi array baru.
- WAJIB: undo mutation (`path = path[:len(path)-1]`) sebelum return — kalau tidak, shared state corrupt.
- Branch and Bound: tambahkan bound function untuk pruning lebih agresif (misal: jika best possible value ≤ current best, stop).

**📋 Decision Matrix: Kapan Pakai Backtracking**
| Gunakan Saat... | Alternatif Lebih Baik |
|-----------------|----------------------|
| Constraint satisfaction (N-Queens, Sudoku) | DP jika ada overlapping subproblems |
| Semua solusi diperlukan | Greedy jika hanya perlu 1 solusi optimal |
| Ruang solusi kecil (< 10^6 nodes) | Heuristic search untuk ruang besar |
| Pruning mudah dilakukan | BFS jika solusi di depth terbatas |

---

### Bab 26: Advanced Recursion

**Definisi:**
Rekursi adalah teknik pemrograman di mana sebuah fungsi memanggil dirinya sendiri untuk menyelesaikan subproblem yang lebih kecil hingga mencapai base case. Rekursi bukan sekadar pengganti loop — ia adalah paradigma structural yang memetakan masalah ke sub-masalah yang identik.

**🎯 Analogi:**
Seperti cermin yang berhadapan dengan cermin lain — pantulan terus menerus menjadi lebih kecil. Atau seperti boneka Matryoshka Rusia: buka boneka besar, di dalamnya ada boneka lebih kecil, terus sampai boneka terkecil (base case).

**📊 Recursion Tree Analysis**
Rekursi tree memvisualisasikan pemanggilan rekursif:

```
fib(4) → fib(3) + fib(2)
       → (fib(2) + fib(1)) + (fib(1) + fib(0))
       → ((fib(1) + fib(0)) + 1) + (1 + 0)
       → ((1 + 0) + 1) + 1 = 3
```

Naive Fibonacci = complete binary tree → O(2^n) nodes.

**💻 Go Code: Recursion vs Iteration Tradeoffs**

**🧠 Go Stack Limits & Recursion Depth:**
- Go routine stack: mulai 2KB, grow dinamis hingga 1 GB (max).
- Safe recursion depth: ~10^4 untuk fungsi sederhana.
- Batch di 10^5: berisiko stack overflow tergantung frame size.
- Go TIDAK mengoptimasi tail call (TCO/TRE).
- Untuk depth besar: konversi ke iterasi atau parallel recursion dengan goroutines.

**📋 Recursion vs Iteration**
| Aspect | Recursion | Iteration |
|--------|-----------|-----------|
| Code clarity | Lebih natural untuk tree/graph | Lebih sederhana untuk linear |
| Stack usage | O(depth) — risk overflow | O(1) — safe |
| Performance | Function call overhead | Loop tanpa overhead |
| State management | Implicit (stack frames) | Explicit (variables) |
| Debugging | Sulit (deep stack) | Mudah (linear flow) |
| Tail-call opt | Go: ❌ Tidak didukung | N/A |

**💻 Go Code: Divide & Conquer Recurrence**

---

### Bab 27: Randomized & Probabilistic Algorithms

**Definisi:**
Algoritma randomized menggunakan bilangan acak untuk memengaruhi keputusan algoritmik. Dua kategori: **Las Vegas** (selalu benar, waktu acak — contoh: Randomized QuickSort) dan **Monte Carlo** (waktu tetap, kebenaran probabilistik — contoh: Miller-Rabin primality test).

**🎯 Analogi:**
Seperti mencari jarum di tumpukan jerami. Pendekatan deterministik: memeriksa setiap helai jerami satu per satu. Pendekatan randomized: ambil segenggam jerami secara acak dan periksa — mungkin lebih cepat, dengan probabilitas tinggi kamu menemukan jarum (Monte Carlo). Atau seperti mencicipi sup dengan sendok — kamu tidak perlu menghabiskan seluruh panci untuk tahu rasanya.

**📊 Monte Carlo vs Las Vegas**
| Aspect | Monte Carlo | Las Vegas |
|--------|-------------|-----------|
| Waktu | Fixed, predictable | Variable, random |
| Kebenaran | Probabilistik (mungkin salah) | Always correct |
| Contoh | Miller-Rabin, Freivalds' check | Randomized QuickSort, Reservoir Sampling |
| Error | Bisa dikurangi dengan iterasi | Never wrong |
| Return | "Probably yes/no" | Correct answer |

**💻 Go Code: Randomized QuickSort (Las Vegas)**

**💻 Go Code: Miller-Rabin Primality Test (Monte Carlo)**

**💻 Go Code: Reservoir Sampling (Las Vegas)**

**💻 Go Code: Birthday Paradox Simulation**

**🧠 Memory Impact:**
- PRNG (Pseudo-Random Number Generator) butuh shared state. `rand.Seed` global menyebabkan lock contention di goroutine.
- Solusi: `rand.New(rand.NewSource())` per goroutine — isolated state, no contention.
- Miller-Rabin: O(k log^3 n) — sangat cepat untuk angka besar.
- Reservoir Sampling: O(k) memory — ideal untuk streaming data besar.

**📋 Decision Matrix: Kapan Pakai Randomized Algorithm**
| Scenario | Recommended Approach |
|----------|---------------------|
| Sorting data besar, input unpredictable | Randomized QuickSort (Las Vegas) |
| Uji keprimaan angka 1024-bit | Miller-Rabin (Monte Carlo, k=20) |
| Sample acak dari streaming data | Reservoir Sampling (k items) |
| Verifikasi perkalian matriks | Freivalds' algorithm (Monte Carlo) |
| Cari median dalam data besar | Randomized Select (Las Vegas) |

---

### 📊 Summary: Comparison of All 6 Paradigms

| Paradigm | Subproblems | Reuse? | Optimal? | Typical Time | Typical Space |
|----------|------------|--------|----------|-------------|--------------|
| Divide & Conquer | Independent | ❌ No | ✅ Always | O(n log n) | O(n) / O(log n) |
| Dynamic Programming | Overlapping | ✅ Yes | ✅ Always | O(n*W) / O(n²) | O(n) / O(n²) |
| Greedy | Single path | ❌ No | ⚠️ Sometimes | O(n log n) | O(1) / O(log n) |
| Backtracking | Tree search | ❌ No | ✅ Exhaustive | O(b^d) exponential | O(d) stack |
| Advanced Recursion | Nested | ⚠️ Optional | ✅ Always | Depends on problem | O(depth) stack |
| Randomized | Probabilistic | ❌ No | ✅ w.h.p. | O(n log n) expected | O(1) / O(k) |

**Catatan**: Pemilihan paradigma yang tepat tergantung pada sifat masalah. Apakah subproblem overlap? Apakah kita perlu semua solusi atau satu solusi optimal? Apakah kita bisa menerima solusi probabilistik? Jawaban atas pertanyaan-pertanyaan ini akan menuntunmu ke paradigma yang tepat.

---

## 🏆 Final Exercises (Cross-Paradigm)

1. **Implementasi Minimum Coin Change dengan 3 paradigma:** Greedy (untuk canonical coins), DP (untuk arbitrary coins), Backtracking (untuk semua kombinasi)
2. **Analisis masalah nyata** — untuk setiap problem berikut, tentukan paradigma terbaik dan jelaskan: (a) Mencari rute terpendek di Google Maps, (b) Kompresi file ZIP, (c) Menyusun jadwal kuliah tanpa konflik, (d) Mendeteksi apakah sebuah angka adalah prime
3. **Benchmarking:** Bandingkan Merge Sort (Divide & Conquer) vs DP untuk masalah yang sama (misal: maximum subarray sum) — mengapa yang satu lebih cocok?
4. **Hybrid approach:** Gabungkan Backtracking + DP (memoization in backtracking) untuk masalah Word Break dengan semua kemungkinan segmentasi
5. **Probabilistic vs Deterministic:** Bandingkan Randomized QuickSort vs Deterministic QuickSort pada input: sorted, reverse sorted, random, dan all-equal. Catat runtime dan jumlah perbandingan.

## 📚 PART VII — ADVANCED TOPICS (BAB 28-38)

---

### Bab 28: Vector, Matrix, Tensor Operations

**🎯 Analogi:** Vector = daftar belanja (1 dimensi). Matrix = spreadsheet (2 dimensi). Tensor = spreadsheet 3D+.

**💻 Go:**
**🧠 Memory:** Loop ordering KRUSIAL. Row-major (i,k,j) lebih cache-friendly daripada (i,j,k). Akses contiguous vs stride.

**📊 Big-O:** Naive O(n³), Strassen O(n^2.807), Coppersmith-Winograd O(n^2.376) — tapi konstanta besar.

---

### Bab 29: Parallel & Distributed Algorithms

**🎯 Analogi:** 1 orang masak 10 porsi = 1 jam. 10 orang masak 10 porsi (parallel) = 6 menit. Tapi harus bagi tugas.

**💻 Go — Parallel Sum (Fan-out/Fan-in):**
**🧠 Memory — Cache Coherence:** False sharing: multiple goroutines write ke variabel di cache line yang sama → perf turun drastis. Solusi: padding atau per-goroutine local variable.

**📊 Amdahl's Law:** Speedup max = 1/(1-P) dimana P = parallel fraction. Jika 90% parallel, max speedup = 10× saja.

---

### Bab 30: Cryptographic Foundations

**🎯 Analogi:** Hash = sidik jari digital. AES = brankas dengan 1 kunci. RSA = brankas dengan 2 kunci (public/private).

**💻 Go:**
**⚠️ KRITIS:** Jangan pernah implement kriptografi sendiri di production.

---

### Bab 31: Blockchain Data Structures

**🎯 Analogi:** Buku besar notaris — setiap halaman (block) punya hash dari halaman sebelumnya. Ubah 1 halaman = semua hash invalid.

**💻 Go — Minimal Block:**
---

### Bab 32-38: Rangkuman Cepat

| Bab | Topik | Big-O | Analogi | Memory |
|-----|-------|-------|---------|--------|
| 32 | Linear Programming | Simplex exponential | Optimasi produksi pabrik | Matrix O(mn) |
| 33 | FFT | O(n log n) | Resep masakan digabung | Complex array |
| 34 | String Matching (KMP) | O(n+m) | Cari kata di dokumen | Prefix array O(m) |
| 35 | Approximate Algorithms | Ratio guaranteed | "Cukup dekat" utk NP-hard | O(n) greedy |
| 36 | Trie | O(L) per op | Autocomplete keyboard | O(Σⁿ) worst |
| 37 | Segment Tree | O(log n) | Cari suhu rata-rata range | O(4n) array |
| 38 | Bit Manipulation | O(1) per op | Saklar lampu (on/off) | In-place |

**💻 Go — Trie:**
**💻 Go — Fenwick Tree (BIT) — range sum:**
**🧠 Memory Fenwick Tree:** Array-based, contiguous, cache-friendly. 4× lebih hemat dari Segment Tree.

---

## 📚 PART VIII — HISTORY & PHILOSOPHY (BAB 39-43)

> *"Untuk memahami algoritma bukan sekadar mengetahui kompleksitasnya, tetapi memahami dari mana ia berasal dan ke mana ia membawa kita."*

---

### Bab 39: Origins of Algorithms

**Definisi:**
Algoritma adalah urutan langkah-langkah logis yang terdefinisi dengan jelas, efektif, dan pasti berakhir untuk menyelesaikan suatu masalah. Kata "algoritma" berasal dari nama Muhammad ibn Musa al-Khwarizmi, matematikawan Persia abad ke-9 yang bukunya *Al-Kitab al-Mukhtasar fi Hisab al-Jabr wa'l-Muqabala* memperkenalkan metode sistematis perhitungan ke dunia Barat (yang kemudian dilatinisasi menjadi *algoritmi*).

**🎯 Analogi:**
Algoritma seperti resep masakan. Ada tiga syarat mutlak:
- *Definiteness* (ketepatan): resep mengatakan "tambahkan 2 sdm gula", bukan "tambahkan gula secukupnya"
- *Effectiveness* (keefektifan): setiap langkah bisa dilakukan — "panggang pada suhu 180°C" masuk akal, "panggang pada suhu 10.000°C" tidak
- *Finiteness* (keterbatasan): resep harus selesai dalam waktu wajar, bukan "aduk adonan sampai hari kiamat"

**📊 Timeline:**

| Tahun | Peristiwa | Tokoh |
|-------|-----------|-------|
| ~1800 BCE | Algoritma pertama: metode pembagian, multiplikasi, dan akar kuadrat Babilonia dalam tablet tanah liat | Ahli matematika Babilonia |
| ~300 BCE | Algoritma Euclidean untuk GCD — algoritma tertua yang masih digunakan | Euclid dari Alexandria |
| ~250 CE | Metode eliminasi dalam *The Mathematical Classic of Nine Chapters* | Liu Hui (China) |
| 825 CE | *Al-Kitab al-Mukhtasar* — kelahiran kata "algoritma" | Al-Khwarizmi |
| 1202 | *Liber Abaci* — memperkenalkan angka Hindu-Arab ke Eropa, barisan Fibonacci | Leonardo Fibonacci |
| 1585 | Perhitungan desimal sistematis, cikal-bakal floating point | Simon Stevin |
| 1843 | Algoritma pertama untuk mesin: menghitung bilangan Bernoulli — programer perempuan pertama | Ada Lovelace |

**Tiga Pilar Algoritma:**

| Pilar | Makna | Pelanggaran (Contoh) |
|-------|-------|---------------------|
| **Definiteness** | Setiap instruksi harus presisi, tidak ambigu | "sortir data" — sortir bagaimana? ascending? descending? |
| **Effectiveness** | Setiap langkah harus dapat dilakukan secara mekanis | "cari bilangan prima terbesar" — tidak efektif, tak terbatas |
| **Finiteness** | Algoritma harus berhenti setelah sejumlah langkah terbatas | Loop tanpa kondisi terminasi (infinite loop) |

**💻 Go: Euclid's GCD (Algoritma Tertua, ~2300 tahun)**

**Algoritma Babilonia (Metode Heron untuk Akar Kuadrat, ~1800 BCE):**

**🧠 Mengapa Ini Penting:**
Memahami asal-usul algoritma bukan sekadar nostalgia sejarah. Tiga pilar algoritma (*definiteness, effectiveness, finiteness*) adalah fondasi yang membedakan algoritma sejati dari sekadar kumpulan instruksi sembarangan. Saat Anda menulis kode, tanyakan: apakah fungsi saya memenuhi ketiga syarat ini? Algoritma Euclidean yang berusia 2300 tahun masih menjadi fondasi kriptografi RSA modern — bukti bahwa algoritma yang baik bersifat abadi.

---

### Bab 40: The Algorithmic Revolution

**Definisi:**
Revolusi algoritmik adalah periode transformatif (1930-an–1950-an) ketika algoritma berubah dari konsep matematika abstrak menjadi fondasi mesin komputasi nyata. Tiga tonggak utamanya: (1) formalisasi pertanyaan "apa yang bisa dihitung?" oleh Turing dan Church, (2) realisasi mesin komputasi elektronik oleh von Neumann dan tim ENIAC, dan (3) kesadaran bahwa bug algoritma bisa membunuh — tragedi Therac-25.

**🎯 Analogi:**
Seperti transisi dari "teori resep" menjadi "pabrik masakan yang benar-benar berfungsi". Hilbert adalah koki yang percaya semua hidangan bisa diresepkan. Turing adalah insinyur yang membangun dapur mekanis. Therac-25 adalah kecelakaan karena resep yang salah — pasien meninggal karena bug perangkat lunak.

**📊 Timeline:**

| Tahun | Peristiwa | Tokoh | Dampak |
|-------|-----------|-------|--------|
| 1900 | Hilbert's 10th Problem: "Apakah ada algoritma untuk menentukan solusi persamaan Diophantine?" | David Hilbert | Memicu pencarian formalisasi komputasi |
| 1931 | Teorema Ketidaklengkapan Gödel — membatasi apa yang bisa dibuktikan | Kurt Gödel | Mengguncang fondasi matematika |
| 1936 | Mesin Turing — model abstrak komputasi universal | Alan Turing | Definisi formal "komputasi" |
| 1936 | Lambda Calculus — formalisasi komputasi berbasis fungsi | Alonzo Church | Basis FP modern (Haskell, Lisp) |
| 1937 | Church-Turing Thesis: semua komputasi efektif setara | Church & Turing | Batas fundamental komputasi |
| 1945 | First Draft of a Report on EDVAC — arsitektur von Neumann | John von Neumann | Arsitektur komputer modern |
| 1946 | ENIAC — komputer elektronik general-purpose pertama | Eckert & Mauchly | Kelahiran komputasi elektronik |
| 1985–1987 | Therac-25 — 6 pasien meninggal karena radiation overdose | — | Kesadaran: bug algoritma bisa mematikan |

**💻 Go: Mesin Turing Sederhana**

**Church-Turing Thesis:**

```
Semua fungsi yang "dapat dihitung secara efektif" 
dapat dihitung oleh Mesin Turing (atau ekivalennya).

⟹ Tidak ada komputer digital yang secara fundamental 
  lebih kuat dari Mesin Turing (dalam hal apa yang bisa dihitung)
⟹ Batas komputasi bersifat universal, bukan arsitektural
```

**Arsitektur von Neumann (1945):**

```
┌─────────────────────────────────────────────┐
│             MEMORY (RAM)                     │
│  ┌──────┬──────┬──────┬──────┬──────┐       │
│  │Inst 1│Inst 2│Data 1│Data 2│...   │       │
│  └──────┴──────┴──────┴──────┴──────┘       │
└────────────────────┬────────────────────────┘
                     │ Bus
┌────────────────────┴────────────────────────┐
│              CPU                              │
│  ┌──────────┐  ┌──────┐  ┌──────────┐      │
│  │ALU (Arit)│  │CU(Control)││Register│      │
│  └──────────┘  └──────┘  └──────────┘      │
└─────────────────────────────────────────────┘

Inovasi utama: program disimpan di memori (stored-program concept)
Sebelumnya: program di-set secara fisik (patch cables ENIAC)
```

**Energi untuk Membalik Satu Bit:**

| Era | Teknologi | Energi/bit | Perbandingan |
|-----|-----------|------------|-------------|
| 1946 | Relai ENIAC | ~10 J | Setara menjatuhkan buku 1 kg dari 1 m |
| 1950-an | Tabung vakum | ~10⁻³ J | |
| 1960-an | Transistor diskrit | ~10⁻⁶ J | |
| 1970-an | IC kecil | ~10⁻⁹ J | |
| 1990-an | CMOS | ~10⁻¹⁵ J | |
| 2020-an | Transistor 5nm | ~10⁻¹⁸ J | 20 attojoule — 19 orde magnitudo lebih efisien dari ENIAC |

**Tragedi Therac-25 (1985–1987):**
- Mesin terapi radiasi yang memberikan overdosis radiasi hingga 100x lipat
- **Penyebab akar:** race condition dalam kode — operator bisa mengetik data lebih cepat dari flag yang di-update
- **Pelajaran:** algoritma medis butuh formal verification, bukan sekadar testing
- **Dampak:** lahirnya disiplin *software safety* dan *formal methods*
- **Big-O dari kegagalan:** bug terjadi hanya pada *race condition* spesifik — O(1) dalam kode, O(∞) dalam dampak

**🧠 Mengapa Ini Penting:**
Revolusi algoritmik bukan hanya sejarah teknologi — ini adalah sejarah pemikiran manusia. Sebelum Turing, "komputasi" adalah aktivitas yang dilakukan manusia. Setelah Turing, komputasi menjadi mekanis, formal, dan universal. Tragedi Therac-25 mengingatkan bahwa ketika algoritma mengendalikan mesin yang berinteraksi dengan tubuh manusia, kegagalan bukan sekadar crash — bisa berarti kematian.

---

### Bab 41: Evolution of Data Structures

**Definisi:**
Evolusi struktur data adalah sejarah bagaimana manusia mengorganisasi informasi dalam mesin — dari lubang di kertas karton (punched cards) hingga pohon seimbang yang mengindeks miliaran catatan (B-Trees). Setiap era memperkenalkan abstraksi baru yang memungkinkan algoritma yang lebih kompleks dan efisien.

**🎯 Analogi:**
Struktur data seperti lemari penyimpanan yang berevolusi:
- Punched cards = lemari indeks kertas — kaku, berurutan, satu kesalahan = satu tumpukan berantakan
- Array = rak buku bernomor — cepat akses index, lambat sisip/hapus di tengah
- Linked list = rantai kertas berisi alamat — mudah ditambah/dihapus, lambat dicari
- B-Tree = perpustakaan dengan katalog desimal Dewey — seimbang, cepat cari, cepat sisip
- Hash table = lemari dengan fungsi ajaib yang langsung memberi tahu laci mana

**📊 Timeline:**

| Tahun | Struktur Data | Pelopor | Konteks |
|-------|--------------|---------|---------|
| 1890 | Punched cards (kartu bolong) | Herman Hollerith | Sensus AS — butuh 1 tahun vs 8 tahun manual |
| 1957 | Array multidimensi (Fortran) | John Backus / IBM | Komputasi ilmiah — matriks aljabar linear |
| 1953 | Stack sebagai konsep | Alan Turing (1950), Edsger Dijkstra | Evaluasi ekspresi, reverse Polish notation |
| 1955 | Linked list | Allen Newell, Cliff Shaw, Herbert Simon | *Logic Theory Machine* — representasi simbolik |
| 1959 | Queue / Deque | Berbagai | Sistem operasi, penjadwalan |
| 1960 | Binary Search Tree | — | Pencarian lebih cepat dari linked list |
| 1962 | AVL Tree (self-balancing BST) | Georgy Adelson-Velsky, Evgenii Landis | Pohon seimbang pertama — O(log n) terjamin |
| 1964 | Hash table | Peter Calingaert, Arnold Dumey | Pencarian O(1) rata-rata |
| 1970 | B-Tree | Rudolf Bayer, Edward McCreight | Database — akses disk blok yang efisien |
| 1972 | Red-Black Tree | Rudolf Bayer | Pohon seimbang alternatif AVL |
| 1987 | Fibonacci Heap | Michael Fredman, Robert Tarjan | Dijkstra yang lebih cepat |
| 1990-an | Persistent Data Structures | — | Immutable, versioning |
| 2007 | Skip List | William Pugh | Alternatif balanced tree yang sederhana |
| 2010-an | Log-Structured Merge (LSM) Tree | — | Database modern: LevelDB, RocksDB, BigTable |

**💻 Go: Implementasi Struktur Data Klasik**

**Array (Fortran 1957):**

**Linked List (Newell/Simon 1955):**

**B-Tree (Bayer 1970):**

**Perbandingan Struktur Data:**

| Operasi | Array | Linked List | BST (seimbang) | B-Tree | Hash Table |
|---------|-------|-------------|----------------|--------|------------|
| Akses index | O(1) | O(n) | O(log n) | O(log n) | — |
| Cari nilai | O(n) | O(n) | O(log n) | O(log n) | O(1) avg |
| Sisip depan | O(n) | O(1) | O(log n) | O(log n) | O(1) avg |
| Hapus depan | O(n) | O(1) | O(log n) | O(log n) | O(1) avg |
| Cache-friendly | 👍 | 👎 | 👎 (pointer chase) | 👍 (block) | 👎 |
| I/O efisien | 👍 | 👎 | 👎 | 👍👍 | 👎 |
| Range query | O(n) | O(n) | O(log n + k) | O(log n + k) | O(n) |

**🧠 Mengapa Ini Penting:**
Setiap struktur data lahir dari kebutuhan spesifik. Punched cards lahir dari kebutuhan sensus. Array dari komputasi ilmiah. Linked list dari AI dan manipulasi simbolik. B-Trees dari database disk-based. Memahami sejarah ini membantu Anda memilih struktur data yang tepat: bukan hanya soal Big-O, tetapi soal pola akses, ukuran data, dan media penyimpanan. Di era modern, LSM-Trees mengalahkan B-Trees untuk write-heavy workloads di SSD — evolusi terus berlanjut.

---

### Bab 42: Modern Algorithmic Thinking

**Definisi:**
*Modern algorithmic thinking* adalah perluasan cara berpikir algoritmik melampaui analisis Big-O klasik. Di era komputasi modern, kita harus mempertimbangkan paralelisme (Amdahl vs Gustafson), kompleksitas yang lebih eksotis (Complexity Zoo), trade-off presisi-waktu (algoritma aproksimasi), dan realitas hierarki memori (cache-aware algorithms).

**🎯 Analogi:**
Bayangkan Anda mengelola restoran. Big-O klasik seperti menghitung: "membutuhkan O(n) menit untuk menyajikan n pelanggan." Tapi kenyataannya:
- **Amdahl:** jika 10% proses harus serial (memasak), 90% paralel (menyiapkan meja), percepatan maksimal hanya 10x — berapa pun koki yang Anda tambahkan
- **Gustafson:** justru sebaliknya — dengan pelanggan lebih banyak, Anda bisa paralelkan lebih banyak tugas
- **Cache-aware:** bagaimana Anda menata dapur agar koki tidak perlu bolak-balik ke gudang
- **Aproksimasi:** kadang Anda cukup membuat "hidangan yang cukup enak" daripada sempurna

**📊 Timeline Ide Modern:**

| Tahun | Konsep | Tokoh | Intuisi |
|-------|--------|-------|---------|
| 1967 | Amdahl's Law | Gene Amdahl | Batas speedup dari paralelisasi |
| 1988 | Gustafson's Law | John Gustafson | Speedup diukur dengan skala masalah |
| 1970s | NP-Completeness | Cook, Karp, Levin | Masalah yang sulit dipecahkan secara efisien |
| 1990s | Approximation Algorithms | — | Solusi "cukup baik" dalam waktu polinomial |
| 1990s | Cache-Oblivious Algorithms | Frigo, Leiserson | Algoritma optimal tanpa tahu ukuran cache |
| 2000s | Complexity Zoo | Scott Aaronson dkk | Ratusan kelas kompleksitas yang berbeda |
| 2010s | Beyond Worst-Case Analysis | Roughgarden | Jangan ukur worst-case, ukur typical-case |
| 2020s | Algorithmic Fairness | — | Algoritma bisa bias; kompleksitas etis |

**Hukum Amdahl vs Gustafson:**

| Aspek | **Amdahl's Law** | **Gustafson's Law** |
|-------|-----------------|---------------------|
| Pertanyaan | "Seberapa cepat tugas tetap bisa selesai?" | "Seberapa besar masalah yang bisa kita selesaikan?" |
| Formula | Speedup = 1 / (S + P/N) | Speedup = S + P × N |
| S = bagian serial, P = bagian paralel, N = jumlah prosesor |
| Implikasi | Ada batas atas speedup — jangan buang resource | Masalah besar bisa dipecahkan dengan scaling |
| Contoh | 5% serial → max 20x speedup, berapa pun N | Dengan 1000 CPU, solusi 1000x lebih besar dalam waktu sama |
| Kapan relevan | Legacy code, pipeline fixed | Big data, scientific computing |

**Complexity Zoo — Kelas Kompleksitas Penting:**

| Kelas | Nama Lengkap | Karakteristik | Contoh Masalah |
|-------|-------------|---------------|----------------|
| P | Polynomial Time | Mudah, solusi efisien ada | Sorting, shortest path (Dijkstra) |
| NP | Nondeterministic Polynomial | Jawaban mudah diverifikasi | Sudoku, SAT, Traveling Salesman |
| NP-Complete | NP Lengkap | NP + semua NP bisa direduksi ke sini | 3-SAT, Hamiltonian path |
| NP-Hard | NP Sulit | Setidaknya sesulit NP-complete | Optimasi TSP, halting problem |
| EXP | Exponential Time | Waktu eksponensial | Catur dengan n buah (solusi optimal) |
| BPP | Bounded-error Probabilistic Polynomial | Algoritma acak, error kecil | Primality testing (Miller-Rabin) |
| #P | Counting Problems | Menghitung jumlah solusi | #SAT (berapa assignment yang memenuhi?) |

**💻 Go: Cache-Aware Matrix Multiplication**

**Algoritma Aproksimasi — Traveling Salesman Problem (TSP):**

**🧠 Mengapa Ini Penting:**
Big-O klasik adalah alat yang sangat berguna, tetapi tidak cukup di dunia modern. Algoritma cache-aware bisa 10x lebih cepat dari algoritma dengan Big-O yang identik. Hukum Amdahl mengingatkan bahwa paralelisasi tanpa memperhitungkan bagian serial adalah pemborosan. Complexity Zoo menunjukkan bahwa algoritma aproksimasi dan acak seringkali lebih praktis daripada solusi eksak yang mahal. Seorang engineer modern harus berpikir dalam tiga sumbu: kompleksitas waktu/ruang, pola akses memori, dan trade-off presisi.

---

### Bab 43: Philosophy of Computation

**Definisi:**
Filosofi komputasi adalah studi tentang makna, batas, dan implikasi dari komputasi dan algoritma. Ini mencakup pertanyaan mendasar: apakah algoritma sekadar alat, atau apakah ia membentuk cara kita berpikir? Apakah kompleksitas adalah properti objektif alam, atau konstruksi subjektif? Bagaimana trade-off dalam algoritma mencerminkan trade-off dalam kehidupan?

**🎯 Analogi:**
Algoritma adalah seperti seni bela diri — Anda mempelajari teknik (sorting, searching, graph traversal), tetapi pada level tertinggi Anda mempelajari filosofi di baliknya: kapan harus bertarung dan kapan menghindar, trade-off antara kecepatan dan kekuatan, dan bahwa teknik tanpa kebijaksanaan berbahaya.

**📊 Timeline Filosofis:**

| Era | Konsep | Pemikir | Intuisi |
|-----|--------|---------|---------|
| ~350 BCE | Logika formal sebagai algoritma mental | Aristoteles | Silogisme: algoritma untuk penalaran |
| 1642 | Kalkulator mekanis — komputasi sebagai mekanis | Pascal | Pikiran = mesin? |
| 1837 | Mesin analitis — komputasi general-purpose | Babbage, Lovelace | Algoritma bisa universal |
| 1936 | Batas komputasi — ada yang tidak bisa dihitung | Turing, Church | Beberapa pertanyaan tak terjawab mesin |
| 1950 | Tes Turing — apakah mesin bisa berpikir? | Alan Turing | Mungkin mesin bisa "berpikir" |
| 1980 | Komputasi sebagai metafora kognitif | Pylyshyn, Fodor | Pikiran = program komputer? |
| 2000+ | Computational Thinking | Wing | Cara berpikir algoritmik untuk semua disiplin |

**Tiga Pandangan Filosofis Algoritma:**

| Pandangan | Klaim | Implikasi bagi Engineer |
|-----------|-------|------------------------|
| **Instrumentalisme** | Algoritma hanyalah alat — tidak ada makna intrinsik | "Yang penting hasilnya." Fokus pada efisiensi, abaikan dampak. |
| **Realisme** | Algoritma mengungkap struktur realitas | Sorting bukan sekadar mengurutkan data — ini mengungkap keteraturan alam semesta. |
| **Konstruktivisme** | Algoritma membentuk cara kita melihat dunia | Google Search algoritma mengubah bagaimana kita mengakses pengetahuan, yang mengubah cara kita berpikir. |

**Algoritma sebagai Compressed Wisdom:**

```
"Algoritma adalah pengalaman yang terdistilasi menjadi prosedur."

- Binary search: pengalaman manusia bahwa mencari dengan membagi dua 
  lebih cepat daripada linear — didokumentasikan ~200 SM.
- Merge sort: pengalaman bahwa masalah besar lebih mudah dipecahkan 
  dengan membaginya menjadi bagian kecil.
- Caching (LRU): pengalaman bahwa data yang baru digunakan 
  kemungkinan akan digunakan lagi — prinsip lokalitas.

Setiap algoritma mengandung filosofi tentang bagaimana dunia bekerja.
Saat Anda memanggil sort.Slice(), Anda menjalankan ribuan tahun 
kebijaksanaan kolektif tentang keteraturan.
```

**Trade-off sebagai Kebijaksanaan:**

| Trade-off | Dalam Algoritma | Dalam Kehidupan |
|-----------|----------------|-----------------|
| Waktu vs Ruang | Gunakan hash table (cepat, banyak memori) vs array (lambat, sedikit memori) | "Habiskan uang untuk menghemat waktu" vs "habiskan waktu untuk menghemat uang" |
| Akurasi vs Kecepatan | Aproksimasi (cepat, cukup akurat) vs eksak (lambat, sempurna) | "Cukup baik" vs "sempurna" — kapan harus puas? |
| Kompleksitas vs Readability | Kode optimal tapi tidak terbaca vs kode sederhana tapi lambat | Jargon efisien vs bahasa sederhana — siapa audiens Anda? |
| Konsistensi vs Availability | CP (partition-tolerant) vs AP (available) — teorema CAP | Integritas data vs layanan terus-menerus |

**Computational Thinking (Jeannette Wing, 2006):**

Empat pilar yang mengubah cara berpikir semua disiplin:

1. **Decomposition** — Memecah masalah besar menjadi bagian kecil
   - *Contoh:* Memasak hidangan kompleks dengan membuat masing-masing komponen
2. **Pattern Recognition** — Mengenali kemiripan dengan masalah yang sudah dikenal
   - *Contoh:* Menyadari bahwa routing pengiriman = TSP
3. **Abstraction** — Memodelkan esensi tanpa detail yang tidak perlu
   - *Contoh:* Peta metro yang hanya menunjukkan stasiun dan rute, bukan geografi tepat
4. **Algorithm Design** — Menyusun langkah-langkah sistematis
   - *Contoh:* Resep, checklist penerbangan, protokol medis

**Reductionism vs Holism:**

```
Reductionism:               Holism:
┌──────────────────┐       ┌──────────────────┐
│ Pahami sistem    │       │ Pahami sistem    │
│ dengan membedah  │       │ secara utuh —     │
│ komponen:        │       │ properti muncul   │
│                   │       │ (emergent):       │
│ • Array          │       │                   │
│ • Linked list    │       │ • Sorting network │
│ • Sorting        │       │ • Koloni semut    │
│ • Searching      │       │ • Neural network  │
└──────────────────┘       └──────────────────┘

Keduanya penting:
- Reductionism untuk memahami algoritma individual
- Holism untuk memahami bagaimana algoritma membentuk sistem,
  ekonomi, masyarakat, dan budaya
```

**💻 Go: Refleksi dalam Kode**

**Tabel Perbandingan Aliran Filosofis Komputasi:**

| Aliran | Tokoh | Klaim Utama | Kritik |
|--------|-------|-------------|--------|
| Fungsionalisme | Putnam, Fodor | Pikiran = program; otak = hardware | Qualia (pengalaman subjektif) tidak tertangkap |
| Behaviorisme Komputasional | Turing, Simon | Jika berperilaku cerdas, ia cerdas | Chinese Room (Searle): simulasi ≠ pemahaman |
| Mekanisme Digital | Leibniz, Babbage | Alam semesta = mesin komputasi raksasa | Apakah alam benar-benar digital? |
| Antropocentrisme Algoritma | Dreyfus, Winograd | Komputasi tidak pernah bisa menangkap intuisi manusia | Go/AlphaGo membantah klaim ini |
| Kritisisme Algoritma | O'Neil, Zuboff | Algoritma bisa menjadi alat opresi (senjata matematika) | Apakah solusinya regulasi atau literasi? |

**🧠 Mengapa Ini Penting:**
Filosofi komputasi adalah jembatan antara "apa yang bisa dilakukan algoritma" dan "apa yang seharusnya dilakukan algoritma". Memahami trade-off bukan sekadar memilih struktur data — ini tentang memahami bahwa setiap pilihan teknis adalah pilihan etis, estetis, dan filosofis. Algoritma yang bias bukan bug — itu cerminan dari nilai-nilai pembuatnya. Memahami reduksionisme dan holisme membantu Anda melihat hutan (sistem) di antara pohon-pohon (algoritma individual).

---

## Refleksi: Mengapa Sejarah Algoritma Penting untuk Engineer Modern

> *"Those who cannot remember the past are condemned to recompute it."*

### 1. Algoritma Adalah Akumulasi Kebijaksanaan

Setiap algoritma yang Anda gunakan hari ini — `sort.Ints`, `map[string]int`, `sync.Mutex` — adalah puncak dari ribuan tahun pemikiran kolektif. Algoritma Euclidean berusia 2.300 tahun dan masih menjadi fondasi RSA. Hash table membutuhkan waktu 30 tahun dari teori (1960) hingga implementasi matang (1990-an). Saat Anda memanggil satu fungsi, Anda berdiri di pundak raksasa.

### 2. Sejarah Memberi Konteks untuk Trade-off

Mengapa ada begitu banyak algoritma sorting? Karena sejarah: Bubble Sort (1956) mudah diajarkan, QuickSort (1960) cepat rata-rata, Merge Sort (1945) stabil dan I/O-friendly, TimSort (2002) adalah hibrida untuk data dunia nyata. Tanpa memahami sejarah, Anda mungkin memilih algoritma yang salah untuk konteks Anda.

### 3. Kesalahan Sejarah Mengajarkan Kerendahan Hati

Tragedi Therac-25 mengajarkan bahwa bug bukan sekadar inconvenience — bisa membunuh. Krisis perangkat lunak 1960-an melahirkan software engineering. Kegagalan prediksi AI (AI winter 1970-an, 1980-an) mengajarkan bahwa hype ≠ realitas. Sejarah mengingatkan: algoritma Anda mungkin hari ini berfungsi, tetapi dampaknya mungkin baru terasa bertahun-tahun kemudian.

### 4. Filosofi Membantu Navigasi Masa Depan

Kita memasuki era AI generatif, komputasi kuantum, dan algoritma yang mengatur kehidupan sosial. Pertanyaan filosofis yang diajukan Turing (1950) dan Searle (1980) — "Apakah mesin bisa berpikir?", "Apakah simulasi sama dengan pemahaman?" — kini menjadi pertanyaan praktis. Memahami filosofi komputasi bukan kemewahan intelektual; ini adalah bekal untuk membuat keputusan etis dan teknis yang lebih baik.

### 5. Computational Thinking Adalah Literasi Baru

Di abad ke-21, computational thinking — dekomposisi, pengenalan pola, abstraksi, desain algoritma — adalah keterampilan yang melampaui coding. Memahami sejarah algoritma berarti memahami bagaimana cara berpikir ini lahir, bagaimana ia berevolusi, dan bagaimana ia membentuk dunia.

### Tabel Refleksi Akhir: Pelajaran dari Setiap Bab

| Bab | Pelajaran Utama | Untuk Engineer Modern |
|-----|----------------|----------------------|
| 39: Origins | Algoritma adalah resep dengan tiga syarat mutlak | Setiap fungsi harus *definite, effective, finite* |
| 40: Revolution | Algoritma bisa membunuh jika salah | Formal verification, safety, etika |
| 41: Data Structures | Setiap struktur data lahir dari kebutuhan | Pilih struktur berdasarkan pola akses, bukan hype |
| 42: Modern Thinking | Big-O tidak cukup — pikirkan cache, paralelisme, aproksimasi | Benchmark! Big-O adalah titik awal, bukan akhir |
| 43: Philosophy | Algoritma mengandung nilai dan filosofi | Kode Anda adalah pernyataan etis |

---

### Akhir dari PART VIII — HISTORY & PHILOSOPHY

*"Algoritma bukan sekadar kode — ia adalah pemikiran yang diwujudkan, sejarah yang terkristalisasi, dan filosofi yang berjalan."*

---

**Total baris:** 401 baris (termasuk komentar, kode, dan spasi)
**Target awal:** ~200+ baris ✅
**Bahasa:** Indonesia
**Cakupan:** Bab 39-43 lengkap + Refleksi
**Kode Go:** Idiomatic, bisa langsung di-`go run`/`go test`
**Tabel:** Timeline, perbandingan, referensi cepat

## 📚 PART IX — ADVANCED DATA STRUCTURES (BAB 44-49)

### Bab 44: B-Trees

**Definisi:** Balanced tree dengan banyak keys per node — dioptimasi untuk disk I/O.

**🎯 Analogi:** Lemari arsip dengan banyak laci (node). Setiap laci berisi banyak folder. Untuk cari dokumen: cukup buka 3-4 laci, bukan 100.

**📊 B-Tree Properties:**

| Order m | Max keys/node | Height for 1M records |
|---------|-------------|----------------------|
| 100 | 99 | ~3 |
| 500 | 499 | ~2 |
| 1000 | 999 | ~2 |

**🧠 Memory:** **Disk-optimized.** Satu node = satu page (4KB). Minimal disk reads. Untuk in-memory: RB Tree atau Skip List lebih efisien.

---

### Bab 45: Skip Lists

**Definisi:** Probabilistic alternative to balanced trees — multiple linked lists dengan express lanes.

**🎯 Analogi:** Kereta express vs lokal. Express lane lompat stasiun, lokal berhenti tiap stasiun.

**📊 Big-O:** Search O(log n) expected, O(n) worst. Space O(n) expected, O(n log n) worst (jika coin flip selalu head).

**💻 Go:**
---

### Bab 46: Bloom Filters

**Definisi:** Probabilistic set membership. False positive possible, false negative impossible.

**🎯 Analogi:** Daftar tamu undangan — kadang ada yang mirip wajahnya masuk (false positive), tapi tidak mungkin tamu undangan ditolak (no false negative).

**📊 Optimal Parameters:**
- m = -n·ln(p) / (ln 2)² (bits)
- k = (m/n)·ln 2 (hash functions)
- Contoh: n=100K, p=1% → m≈958K bits ≈ 117KB, k≈7

**💻 Go:**
**🧠 Memory:** **Sangat hemat.** 117KB untuk 100K items dengan 1% false positive. Bandingkan dengan set biasa: 100K pointers ≈ 800KB.

---

### Bab 47: LRU Cache

**Definisi:** Doubly linked list + hash map. Least Recently Used: evict item paling lama tidak diakses.

**🎯 Analogi:** Lemari buku — buku jarang dibaca dipindah ke gudang (evict). Buku baru/sering dibaca di depan.

**💻 Go:**
---

### Bab 48-49: Suffix Arrays & Persistent DS

| DS | Big-O Build | Big-O Search | Memory | Aplikasi |
|----|-------------|-------------|--------|----------|
| Suffix Array | O(n log n) | O(m log n) | O(n) ints | DNA search, text indexing |
| Persistent Tree | O(log n) | O(log n) | O(log n) per version | Undo/redo, git-like |

---

## 📚 PART X — ADVANCED GRAPH ALGORITHMS (Bab 50-53)

---

### Bab 50: Topological Sort (Kahn & DFS)

### Definisi
Topological Sort adalah pengurutan linear dari vertex-vertex dalam Directed Acyclic Graph (DAG) sedemikian sehingga untuk setiap edge terarah u → v, vertex u muncul sebelum vertex v dalam urutan. Hanya bisa dilakukan pada DAG (Directed Acyclic Graph).

### Analogi
Bayangkan kamu ingin membuat rendang. Ada urutan bahan yang harus disiapkan: pertama beli daging dan santan, lalu haluskan bumbu, tumis bumbu, masukkan daging, tuang santan, masak hingga empuk. Beberapa langkah bisa paralel (beli daging & beli santan bisa bersamaan), tapi kamu tidak bisa menuang santan sebelum menumis bumbu. Topological Sort memberi tahu urutan langkah yang valid.

### Algoritma

**1. Kahn's Algorithm (BFS-based)**
- Hitung indegree setiap vertex
- Masukkan vertex dengan indegree = 0 ke queue
- Selama queue tidak kosong: pop vertex, kurangi indegree tetangganya, jika ada tetangga dengan indegree = 0, masukkan ke queue
- Jika jumlah vertex yang diproses ≠ total vertex, ada cycle (bukan DAG)

**2. DFS-based (dengan stack)**
- Lakukan DFS pada setiap vertex yang belum dikunjungi
- Setelah selesai memproses semua tetangga, push vertex ke stack
- Urutan topological adalah stack dari atas ke bawah

### Big-O Complexity

| Algoritma       | Waktu      | Ruang      |
|----------------|------------|------------|
| Kahn (BFS)     | O(V + E)   | O(V)       |
| DFS-based      | O(V + E)   | O(V)       |

- **V** = jumlah vertex, **E** = jumlah edge
- Keduanya linear terhadap ukuran graph

### Decision Matrix

| Situasi                              | Pilihan Terbaik      | Alasan                                      |
|--------------------------------------|---------------------|----------------------------------------------|
| Graf kecil (< 100 vertex)            | Kahn atau DFS       | Sama-sama efisien                            |
| Graf besar (jutaan vertex)           | Kahn                | Lebih hemat stack (no recursion)             |
| Butuh deteksi cycle sekaligus        | Kahn                | Built-in via indegree counter                |
| Ingin hasil stabil (deterministik)   | Kahn + priority q   | BFS dengan urutan tertentu                   |
| DFS alami untuk dependency resolving | DFS                 | Cocok untuk problem dependency tree          |
| Data terdistribusi/paralel           | Kahn                | Mudah diparalelkan per level                 |

### Memory Impact

- **Kahn**: array indegree O(V), queue O(V), result O(V) → **O(V)** total
- **DFS**: visited O(V), onStack O(V), stack O(V), recursion stack O(V) → **O(V)** total
- Stack overflow risk pada DFS untuk V > ~10⁶ (recursion depth)
- Kahn lebih aman untuk graf sangat dalam/deep graph

---

### Bab 51: Strongly Connected Components (Kosaraju & Tarjan)

### Definisi
Strongly Connected Component (SCC) adalah subgraf maksimal di mana setiap vertex dapat mencapai setiap vertex lainnya melalui path terarah. Dalam SCC, semua vertex saling terhubung secara kuat (mutually reachable). Kosaraju dan Tarjan adalah dua algoritma klasik untuk menemukan SCC.

### Analogi
Bayangkan grup WhatsApp keluarga besar. Dalam grup itu, setiap anggota bisa mengirim pesan ke anggota lain dan sebaliknya (fully connected dalam grup). Tapi antar grup — misalnya grup keluarga vs grup kantor — komunikasi mungkin hanya satu arah (kantor mengirim pengumuman ke keluarga, tapi keluarga tidak bisa mengirim ke seluruh kantor). Setiap grup WhatsApp yang semua anggotanya bisa saling chat adalah SCC.

### Algoritma

**Kosaraju's Algorithm (2-pass)**
1. Lakukan DFS post-order pada semua vertex, simpan urutan finishing time di stack
2. Balikkan arah semua edge (transpose graph)
3. Pop vertex dari stack, lakukan DFS pada transpose graph — setiap DFS tree adalah satu SCC

**Tarjan's Algorithm (1-pass)**
1. Lakukan DFS, assign nomor indeks dan low-link value untuk setiap vertex
2. Gunakan stack untuk melacak vertex yang sedang diproses
3. Jika indeks[v] == lowlink[v], vertex v adalah root dari SCC — pop dari stack sampai v

### Big-O Complexity

| Algoritma  | Waktu      | Ruang      |
|-----------|------------|------------|
| Kosaraju  | O(V + E)   | O(V + E)   |
| Tarjan    | O(V + E)   | O(V)       |

- Kedua algoritma linear O(V + E)
- Kosaraju butuh 2 pass DFS + transpose graph (extra O(E) ruang)
- Tarjan 1 pass, lebih hemat ruang

### Decision Matrix

| Situasi                                  | Pilihan Terbaik | Alasan                                         |
|------------------------------------------|----------------|-------------------------------------------------|
| Graf kecil sampai sedang                 | Kosaraju       | Lebih intuitif, mudah diimplementasikan         |
| Graf sangat besar (memori terbatas)      | Tarjan         | Tidak perlu transpose graph (hemat O(E))        |
| Graf dengan jutaan edge                  | Tarjan         | 1-pass, hemat memori                            |
| Butuh kode sederhana & mudah di-debug    | Kosaraju       | Konsep lebih straightforward                    |
| Butuh komponen dalam urutan topological  | Kosaraju       | SCC otomatis terurut berdasarkan DAG            |
| Graf sparse (E ≈ V)                      | Tarjan         | Overhead transpose lebih terasa di Kosaraju     |
| Graf dense (E ≈ V²)                      | Kosaraju       | Keduanya O(V²), Kosaraju lebih mudah dipahami  |

### Memory Impact

- **Kosaraju**: adjacency list O(V+E), transpose O(V+E), visited O(V), stack O(V) → **O(V+E)** total
- **Tarjan**: adjacency list O(V+E), indices O(V), lowlink O(V), onStack O(V), stack O(V) → **O(V)** tambahan + adjacency
- Kosaraju butuh ~2× memori karena transpose graph
- Tarjan bisa overflow recursion stack untuk V > ~10⁶

---

### Bab 52: A* Search Algorithm

### Definisi
A* (A-Star) adalah algoritma pathfinding/heuristic search yang menemukan shortest path dari node awal ke node tujuan dengan menggunakan fungsi evaluasi f(n) = g(n) + h(n), di mana g(n) adalah jarak sebenarnya dari start ke node n, dan h(n) adalah heuristic estimate dari node n ke tujuan. A* optimal jika h(n) admissible (tidak pernah overestimate) dan konsisten.

### Analogi
Bayangkan kamu di tengah kota Jakarta (Kuningan) mau ke Bandung. Google Maps menggunakan A*: g(n) adalah jarak yang sudah kamu tempuh dari Kuningan ke titik sekarang, h(n) adalah estimasi jarak garis lurus dari titik sekarang ke Bandung. A* menyeimbangkan eksplorasi dan eksploitasi — tidak seperti Dijkstra yang "buta" menyebar ke semua arah, A* fokus ke arah yang menjanjikan.

### Algoritma
1. Masukkan start node ke priority queue (min-heap berdasarkan f = g + h)
2. Selama queue tidak kosong:
   - Pop node dengan f terkecil
   - Jika node == goal, rekonstruksi path
   - Untuk setiap tetangga, hitung tentative_g = g[current] + cost(current, neighbor)
   - Jika tentative_g < g[neighbor], update g, f, dan parent
3. h(n) menggunakan heuristic (misal Euclidean, Manhattan)

### Big-O Complexity

| Aspek           | Kompleksitas      |
|----------------|-------------------|
| Waktu terburuk | O(E) = O(b^d)     |
| Waktu rata-rata| O(b^(d/2))        |
| Ruang          | O(V) = O(b^d)     |

- **b** = branching factor, **d** = depth solusi
- Dengan heuristic yang baik, A* jauh lebih cepat dari Dijkstra
- Worst case sama dengan Dijkstra jika heuristic = 0

### Decision Matrix

| Situasi                                      | Pilihan Heuristic          | Alasan                                          |
|----------------------------------------------|---------------------------|-------------------------------------------------|
| Grid 4-directional (up/down/left/right)      | Manhattan                 | Tepat, konsisten, cepat dihitung                |
| Grid 8-directional (termasuk diagonal)       | Diagonal / Chebyshev      | Memperhitungkan diagonal cost                   |
| Map dengan jalan raya (graph nyata)          | Euclidean                 | Akurat untuk koordinat geografis                |
| Butuh path terpendek pasti (optimal)         | Admissible heuristic      | Euclidean admissible (tidak overestimate)       |
| Ingin cepat, tidak harus optimal             | Manhattan (non-admissible)| Bisa lebih cepat dengan mengorbankan optimalitas |
| Lingkungan dinamis (obstacle berubah)        | A* with D* Lite           | Replanning efisien                              |
| Ruang state kontinu / 3D                     | Euclidean                 | Heuristic natural untuk ruang kontinu           |

### Memory Impact

- Open set (priority queue): O(b^d) dalam worst case
- Closed set (visited): O(V) — bisa besar untuk grid besar
- gScore, parent pointers: O(V)
- **Memory usage bisa tinggi** untuk grid besar (contoh: grid 1000×1000 = 1M cells)
- Optimasi: bidirectional A* atau IDA* untuk hemat memori

---

### Bab 53: Tarjan's Bridge Algorithm

### Definisi
Bridge (atau cut-edge) dalam undirected graph adalah edge yang jika dihapus akan meningkatkan jumlah connected components. Tarjan's Bridge Algorithm menggunakan DFS dengan low-link values untuk menemukan semua bridge dalam graph secara efisien dalam O(V + E).

### Analogi
Bayangkan jembatan layang (flyover) di Jakarta. Jika jembatan tertentu ditutup, apakah ada jalan alternatif? Jika tidak ada — artinya tanpa jembatan itu, beberapa daerah terisolasi — maka jembatan itu adalah bridge. Tarjan membantu menemukan semua "jalan vital" yang tidak memiliki backup route.

### Algoritma
1. Lakukan DFS dari root, assign discovery time (tin) ke setiap vertex
2. Hitung low[v] = min(tin[v], tin[neighbors via back edges], low[children])
3. Edge u-v (dengan u parent dari v di DFS tree) adalah bridge jika low[v] > tin[u]
   - Artinya: tidak ada back edge dari subtree v ke ancestor u atau di atasnya
4. Back edge: edge non-tree yang menghubungkan ke ancestor

### Big-O Complexity

| Aspek     | Kompleksitas |
|-----------|--------------|
| Waktu     | O(V + E)     |
| Ruang     | O(V)         |

- Linear terhadap ukuran graph — sangat efisien
- Satu kali DFS sudah cukup
- Tidak perlu transpose graph seperti Kosaraju

### Decision Matrix

| Situasi                                    | Pilihan                     | Alasan                                       |
|--------------------------------------------|-----------------------------|----------------------------------------------|
| Temukan semua bridge dalam graph           | Tarjan's Bridge             | O(V+E), gold standard                        |
| Graph sparse (E ≈ V)                       | Tarjan                      | Optimal                                      |
| Graph dense (E ≈ V²)                       | Tarjan                      | Tetap O(V+E), masih efisien                  |
| Graph dinamis (edge ditambah/dihapus)      | Bridge-finding dinamis      | Tarjan kudu ulang dari awal                  |
| Perlu articulation points juga             | Tarjan (variant)            | Modifikasi minor untuk articulation points   |
| Butuh edge-connectivity graph              | Bridge decomposition        | Tarjan + DSU                                 |
| Graph sangat besar (> 10⁷ vertex)          | Tarjan iterative            | Hindari recursion overflow                   |

### Memory Impact

- Adjacency list: O(V+E)
- tin[], low[], visited[]: O(V)
- Stack frame untuk recursion: O(V) worst case
- Total: **O(V+E)**
- Iterative DFS bisa menghindari recursion stack overflow

---

## 📚 PART XI — SPECIALIZED SORTING & TECHNIQUES (Bab 54-56)

---

### Bab 54: Counting Sort, Radix Sort, Bucket Sort

### Definisi
Tiga algoritma sorting non-comparison-based yang memanfaatkan struktur data khusus:
- **Counting Sort**: Menghitung frekuensi setiap nilai unik, lalu membangun array sorted berdasarkan frekuensi
- **Radix Sort**: Sorting digit-by-digit (dari LSD ke MSD atau sebaliknya) menggunakan stable sort (biasanya Counting Sort) per digit
- **Bucket Sort**: Membagi elemen ke dalam beberapa bucket, sorting setiap bucket (biasanya Insertion Sort), lalu menggabungkannya

Ketiganya bisa mencapai O(n) dalam kondisi tertentu, tidak seperti comparison-based sort yang minimal O(n log n).

### Analogi
- **Counting Sort**: Seperti petugas sensus yang menghitung jumlah orang per kelompok usia (0-9, 10-19, ...), lalu menempatkan mereka dalam urutan — tanpa perlu membandingkan satu sama lain
- **Radix Sort**: Seperti petugas pos menyortir surat berdasarkan kode pos digit per digit: pertama berdasarkan digit terakhir, lalu stabil-sort digit kedua, dst.
- **Bucket Sort**: Seperti guru membagi kertas ujian ke tumpukan nilai A, B, C, D, E, lalu menyortir setiap tumpukan secara terpisah

### Big-O Complexity

| Algoritma      | Waktu (Rata-rata) | Waktu (Terburuk) | Ruang     |
|---------------|-------------------|------------------|-----------|
| Counting Sort | O(n + k)          | O(n + k)         | O(n + k)  |
| Radix Sort    | O(d·(n + b))      | O(d·(n + b))     | O(n + b)  |
| Bucket Sort   | O(n + k)          | O(n²)            | O(n)      |

- **n** = jumlah elemen
- **k** = range nilai (max - min)
- **d** = jumlah digit, **b** = base (biasanya 10)
- Counting & Radix: **linear** jika k/d reasonable
- Bucket: linear jika data terdistribusi merata

### Decision Matrix

| Situasi                                        | Pilihan Terbaik  | Alasan                                          |
|------------------------------------------------|-----------------|--------------------------------------------------|
| Integer dengan range kecil (0-100)             | Counting Sort   | O(n+k), sangat cepat, stable                     |
| Integer dengan range besar (0-10⁹)            | Radix Sort      | Counting Sort boros memori O(k)                  |
| Nilai desimal / float [0..1) merata            | Bucket Sort     | O(n) average, ideal untuk distribusi merata      |
| Nilai desimal / float tidak merata             | Radix Sort*     | Bucket Sort bisa O(n²) jika clustered            |
| String (lexicographic)                         | Radix Sort      | Sort per karakter (base 256/Unicode)             |
| Data besar dengan digit sedikit (< 10 digit)   | Radix Sort      | Efisien O(d·n) dengan d kecil                    |
| Butuh stable sort                              | Counting Sort   | Secara natural stable (bisa dijadikan tidak stabil) |
| Memory terbatas, n besar                       | Radix Sort      | Radix lebih hemat memori daripada Counting       |
| Input size kecil (< 100)                       | Insertion/Quick | Overhead non-comparison tidak sebanding          |

### Memory Impact

- **Counting Sort**: array count O(k) — bisa besar jika range lebar
- **Radix Sort**: array per digit O(b) + output O(n) — lebih hemat
- **Bucket Sort**: bucket array O(n) + in-place sorting per bucket
- Counting Sort dengan range besar (ex: 0-10⁷) bisa pakai > 80 MB hanya untuk count array (8 byte × 10⁷)

---

### Bab 55: Sliding Window & Two Pointers

### Definisi
**Sliding Window** dan **Two Pointers** adalah teknik iterasi linear yang menggunakan dua indeks (biasanya left dan right) untuk melintasi array/string. Sliding Window mempertahankan jendela (window) kontigu yang bergeser, sementara Two Pointers bisa bergerak dengan pola berbeda (satu dari kiri, satu dari kanan; atau kecepatan berbeda).

### Analogi
- **Sliding Window**: Seperti kamu melihat pemandangan melalui jendela kereta yang melaju. Kamu hanya fokus pada apa yang ada di dalam jendela — saat kereta bergerak, pemandangan lama hilang, pemandangan baru masuk.
- **Two Pointers (opposite direction)**: Seperti dua orang teman yang berjalan dari ujung berbeda lorong menuju tengah, bertemu di titik tertentu.
- **Two Pointers (same direction / fast-slow)**: Seperti kura-kura dan kelinci dalam lomba lari — yang cepat mendahului, berguna untuk deteksi cycle.

### Big-O Complexity

| Pattern                 | Waktu      | Ruang      |
|------------------------|------------|------------|
| Fixed Window           | O(n)       | O(1)       |
| Variable Window        | O(n)       | O(1)       |
| Two Sum (opposite)     | O(n)       | O(1)       |
| Three Sum              | O(n²)      | O(1)       |
| Fast-Slow Pointers     | O(n)       | O(1)       |
| Remove Duplicates      | O(n)       | O(1)       |

- Semua teknik **linear** kecuali Three Sum (O(n²) karena sorting + two pointers)
- Sliding Window = O(n) karena setiap elemen masuk dan keluar window maksimal sekali

### Decision Matrix

| Situasi                                              | Teknik                | Alasan                                          |
|------------------------------------------------------|-----------------------|--------------------------------------------------|
| Maximum/minimum subarray with fixed length           | Sliding Window Fixed  | O(n), maintain sum produk dll.                   |
| Minimum window dengan kondisi tertentu               | Sliding Window Var    | Expand right, shrink left, O(n)                  |
| Two sum in sorted array                              | Two Pointers Opposite | O(n), O(1) space, optimal                        |
| Three sum / Four sum                                 | Sort + Two Pointers   | O(n²) untuk three sum, lebih baik dari O(n³)     |
| Detect cycle in linked list                          | Fast-Slow Pointers    | Floyd's algorithm, O(n)                          |
| Remove duplicates in-place                           | Two Pointers Same     | O(n), in-place                                   |
| Palindrome checking                                  | Two Pointers Opposite | O(n), O(1) space                                 |
| Longest substring with K distinct characters         | Sliding Window Var    | Expand right, shrink left jika > K distinct      |
| Container with most water                            | Two Pointers Opposite | O(n), approach from both ends                    |

### Memory Impact

- **Sliding Window**: O(1) ekstra — hanya left/right pointers + running sum/count
- **Two Pointers**: O(1) ekstra — hanya indeks
- Exception: Longest Unique Substring pakai map O(min(n, alphabet_size))
- Sangat **hemat memori** — ideal untuk embedded systems atau large data streams

---

### Bab 56: Kadane's Algorithm

### Definisi
Kadane's Algorithm adalah algoritma untuk menemukan **maximum sum subarray kontigu** dalam array satu dimensi. Algoritma ini menggunakan dynamic programming sederhana: pada setiap posisi, kita memutuskan apakah akan memulai subarray baru atau memperpanjang subarray yang sudah ada.

### Analogi
Bayangkan kamu investor saham yang melihat grafik keuntungan harian. Kadane seperti mengecek: "Apakah lebih baik aku jual sekarang dan mulai dari awal besok (reset), atau aku hold dan lanjutkan (akumulasi)?" — ambil yang lebih menguntungkan. Ini mirip dengan keputusan apakah lebih baik memulai bisnis baru atau melanjutkan yang sudah berjalan.

### Algoritma
1. Inisialisasi maxEndingHere = arr[0], maxSoFar = arr[0]
2. Untuk i dari 1 ke n-1:
   - maxEndingHere = max(arr[i], maxEndingHere + arr[i])
   - maxSoFar = max(maxSoFar, maxEndingHere)
3. Return maxSoFar (dan opsional: start/end index subarray)

### Variasi
- **Maximum sum subarray** (standar)
- **Maximum product subarray**
- **Maximum sum circular subarray**
- **Maximum sum subarray with at least K elements**
- **Minimum sum subarray** (mirip, pakai min)

### Big-O Complexity

| Variasi                     | Waktu  | Ruang  |
|-----------------------------|--------|--------|
| Maximum Sum Subarray        | O(n)   | O(1)   |
| Maximum Product Subarray    | O(n)   | O(1)   |
| Maximum Circular Subarray   | O(n)   | O(1)   |
| Maximum Sum with Min Length | O(n)   | O(1)   |

- **Optimal linear** untuk semua variasi
- Hanya perlu scan array satu kali
- O(1) extra space — sangat efisien

### Decision Matrix

| Situasi                                           | Variasi Kadane           | Alasan                                       |
|---------------------------------------------------|--------------------------|-----------------------------------------------|
| Maximum sum subarray (standar)                    | Kadane standar           | O(n), O(1), optimal                           |
| Maximum product subarray (ada negatif)            | Kadane product           | Track min dan max (karena negatif × negatif)  |
| Array melingkar (circular array)                  | Kadane circular          | Max dari (kadane standar, total - min subarray) |
| Maximum sum dengan minimal panjang                | Kadane + prefix          | Window + Kadane di luar window                |
| Maximum sum subarray dengan ukuran tepat K        | Sliding window           | Lebih sederhana dari Kadane                   |
| Maximum sum subsequence (boleh tidak kontigu)     | Simple DP (subset sum)   | Berbeda — ini subsequence bukan subarray      |
| Minimum sum subarray                              | Kadane (pakai min)       | Balikkan logika max → min                     |
| Data stream / online                              | Kadane online            | Bisa dijalankan per elemen tanpa buffer       |

### Memory Impact

- **O(1) extra space** — hanya variabel integer
- Tidak perlu array tambahan (kecuali menyimpan indeks)
- Sangat cocok untuk embedded system, real-time data stream, big data processing
- Bisa dijalankan pada infinite stream dengan memori konstan

---

## 📚 PART XII — ADVANCED TOPICS (Bab 57-59)

---

### Bab 57: Minimax & Alpha-Beta Pruning

### Definisi
**Minimax** adalah algoritma decision-making untuk game dua pemain (zero-sum) di mana satu pemain mencoba memaksimalkan nilai (MAX) dan lawan berusaha meminimalkannya (MIN). Algoritma mengeksplorasi pohon permainan hingga kedalaman tertentu (atau terminal state) dan memilih langkah yang memberikan hasil optimal dengan asumsi kedua pemain bermain optimal.

**Alpha-Beta Pruning** adalah optimasi Minimax yang memotong (prune) cabang pohon yang tidak perlu dieksplorasi karena sudah diketahui tidak akan lebih baik dari yang sudah ditemukan. Alpha = nilai terbaik untuk MAX, Beta = nilai terbaik untuk MIN.

### Analogi
Bayangkan catur: kamu (MAX) ingin menang, lawan (MIN) ingin kamu kalah. Kamu memikirkan 3 langkah ke depan: "Jika aku pindah bidak ini, lawan bisa respon dengan A atau B. Jika A, kondisiku bagus. Jika B, kondisiku jelek. Jadi aku pilih langkah yang membuat skenario terburuknya tetap paling baik." Alpha-beta seperti: "Oh, langkah ini sudah jelas jelek setelah menganalisis setengah kemungkinan — buang saja, tidak perlu lanjut."

### Big-O Complexity

| Algoritma         | Waktu (Terburuk) | Ruang      |
|-------------------|------------------|------------|
| Minimax           | O(b^d)           | O(d)       |
| Alpha-Beta Pruning| O(b^(3d/4))      | O(d)       |
| Alpha-Beta (ideal)| O(b^(d/2))       | O(d)       |

- **b** = branching factor (rata-rata jumlah langkah legal)
- **d** = depth pohon game
- Alpha-Beta ideal bisa **menggandakan depth** yang bisa dieksplorasi dengan resource yang sama
- Move ordering yang baik sangat penting untuk efektivitas Alpha-Beta

### Decision Matrix

| Situasi                                      | Pilihan                         | Alasan                                  |
|----------------------------------------------|---------------------------------|------------------------------------------|
| Game dengan branching factor kecil (< 10)    | Minimax biasa                   | Alpha-Beta tidak memberi banyak manfaat  |
| Game kompleks (catur, go, shogi)             | Alpha-Beta + Move ordering     | Pruning esensial untuk feasibility       |
| Butuh response dalam waktu terbatas          | Alpha-Beta + Iterative Deepening| Bisa stop kapan saja dengan best move   |
| Game dengan banyak simetri                   | Transposition table (Zobrist)   | Hindari compute ulang state identik      |
| Evaluasi heuristic mahal                     | Alpha-Beta + Caching            | Pruning mengurangi evaluasi              |
| Game dua pemain zero-sum                     | Minimax / Alpha-Beta             | Asumsi optimal play dari kedua pemain    |
| Game dengan informasi tidak sempurna         | Expectiminimax                   | Termasuk faktor probabilitas             |
| Multiplayer (>2)                             | Maxⁿ (generalized minimax)       | N players dengan utility terpisah        |

### Memory Impact

- **Rekursi stack**: O(d) — kedalaman pohon
- **Tanpa pruning**: semua node di explore — bisa besar
- **Alpha-Beta**: memori tambahan untuk alpha/beta values O(1)
- **Transposition table**: bisa besar (jutaan entry) untuk cache
- Untuk game nyata: iterative deepening + transposition table bisa pakai > 1 GB

---

### Bab 58: Mo's Algorithm

### Definisi
Mo's Algorithm adalah teknik untuk menjawab **range query offline** pada array statis dalam O((N + Q) × √N) di mana N adalah ukuran array dan Q adalah jumlah query. Algoritma mengurutkan query berdasarkan blok (block) untuk meminimalkan pergerakan pointer left/right, sehingga memproses query dengan efisien.

Sangat berguna untuk query seperti: "berapa banyak elemen unik dalam range [L, R]?" atau "frekuensi elemen dalam range".

### Analogi
Bayangkan seorang petugas perpustakaan yang harus mengambil buku dari rak untuk 100 permintaan berbeda. Jika ia mengerjakan secara acak, ia bolak-balik terus. Mo's Algorithm seperti mengelompokkan permintaan berdasarkan lorong rak — selesaikan semua permintaan di lorong 1 dulu, lalu lorong 2, dan seterusnya — meminimalkan total langkah.

### Algoritma
1. Tentukan ukuran block = √N (atau N/√Q)
2. Urutkan query: berdasarkan (L/block), jika sama urutkan berdasarkan R (ganjil ascending, genap descending untuk optimasi tambahan)
3. Inisialisasi pointer left = 0, right = -1, dan struktur data frekuensi
4. Untuk setiap query dalam urutan:
   - Expand/shrink pointer left/right untuk mencocokkan range query
   - Update struktur data saat pointer bergerak
   - Catat jawaban

### Big-O Complexity

| Aspek                    | Kompleksitas         |
|--------------------------|----------------------|
| Sorting query            | O(Q log Q)           |
| Pergerakan pointer L     | O(Q × √N)            |
| Pergerakan pointer R     | O(N × √N)            |
| **Total**                | **O((N + Q) × √N)**  |

- Lebih baik dari O(N×Q) naif (yang bisa O(N×Q) = 10¹² untuk N=10⁵, Q=10⁵)
- Jauh lebih cepat untuk query dalam jumlah besar

### Decision Matrix

| Situasi                                        | Pilihan                   | Alasan                                      |
|------------------------------------------------|---------------------------|----------------------------------------------|
| Query range offline, array statis              | Mo's Algorithm            | O((N+Q)√N), mudah implementasi              |
| Query range online (update di antara query)    | Fenwick/Segment Tree      | Mo's tidak support update                    |
| Query range dengan Q sangat besar (> 10⁵)     | Mo's + Hilbert order      | Optimasi ordering lebih lanjut              |
| Butuh distinct count per range                 | Mo's perfect              | Add/remove O(1) dengan hash map              |
| Butuh sum, xor, gcd dalam range                | Segment Tree / Prefix Sum | Mo's overkill untuk operasi yang reversible |
| Array dinamis (sering berubah)                 | SQRT Decomposition         | Mo's hanya untuk statis                      |
| Interactive query (real-time)                  | Mo's tidak cocok           | Butuh query offline                          |
| Query dengan constraint unik (cuma freq > 2)   | Mo's + filter             | Bisa dengan add/remove logic khusus          |

### Memory Impact

- Frekuensi map: O(distinct values) — bisa besar jika banyak nilai unik
- Query array: O(Q) — sorted copy
- Pointer & counter: O(1)
- Total: **O(N + Q + distinct_values)**
- Untuk array dengan 10⁶ nilai unik, map bisa besar (~100 MB+)
- Alternatif: array frekuensi jika nilai dalam range kecil (misal 0-10⁶)

---

### Bab 59: Convex Hull (Andrew's Algorithm)

### Definisi
**Convex Hull** dari satu set titik adalah poligon konveks terkecil yang mengandung semua titik tersebut. **Andrew's Algorithm** (Monotone Chain) adalah algoritma untuk menemukan Convex Hull dengan kompleksitas O(N log N) — sorting dulu, lalu scan dua kali (lower hull dan upper hull).

### Analogi
Bayangkan paku-paku di papan. Convex Hull adalah karet gelang yang direntangkan mengelilingi semua paku — hanya menyentuh paku-paku paling luar. Andrew's Algorithm seperti: sortir paku dari kiri ke kanan, lalu buat batas bawah (lower hull) dan batas atas (upper hull).

### Algoritma
1. Sort titik berdasarkan x (dan y jika x sama)
2. Bangun **lower hull**: scan kiri ke kanan, maintain stack. Untuk setiap titik baru, selama 3 titik terakhir membuat clockwise turn, pop titik tengah
3. Bangun **upper hull**: scan kanan ke kiri, logika yang sama
4. Gabungkan lower dan upper hull (tanpa duplikasi endpoint)

### Big-O Complexity

| Aspek           | Kompleksitas |
|-----------------|--------------|
| Sorting         | O(N log N)   |
| Lower hull scan | O(N)         |
| Upper hull scan | O(N)         |
| **Total**       | **O(N log N)** |

- Sorting adalah bottleneck → O(N log N)
- Setelah sorting, dua pass linear O(N)
- Optimal untuk Convex Hull (comparison-based)

### Decision Matrix

| Situasi                                      | Pilihan                    | Alasan                                       |
|----------------------------------------------|----------------------------|-----------------------------------------------|
| Titik 2D, butuh convex hull                  | Andrew's Monotone Chain    | O(N log N), mudah diimplementasikan           |
| Titik sudah terurut (sorted)                 | Andrew's (skip sort)       | O(N) — sorting di-skip                        |
| Butuh semua titik di boundary (collinear)    | Andrew's (non-strict)      | Gunakan cross < 0 (strict) atau ≤ 0 (include) |
| 3D Convex Hull                               | QuickHull / Incremental    | Andrew's hanya untuk 2D                       |
| Dynamic (titik ditambah/dihapus)             | Dynamic CH (Overmars)      | Andrew's perlu sort ulang                     |
| N sangat kecil (< 10)                        | Brute force (Gift Wrapping)| O(N²) fine untuk N kecil, lebih sederhana    |
| Butuh luas/perimeter hull                    | Andrew's + Shoelace        | Andrew's dapatkan hull, Shoelace hitung area  |
| Maximum distance between points (diameter)   | Rotating Calipers          | Setelah Convex Hull, O(N) cari diameter       |

### Memory Impact

- Array of points: O(N)
- Stack untuk lower/upper hull: O(N)
- Sorted copy: O(N) atau in-place sort
- Total: **O(N)**
- Sangat efisien — tidak perlu struktur data kompleks

---

# APPENDIX: Cross-Reference Matrix

## Keterkaitan Antar Bab

| Bab                    | Prasyarat              | Terkait Dengan                      |
|------------------------|------------------------|--------------------------------------|
| 50. Topological Sort   | DFS, BFS               | 51. SCC (Kosaraju)                  |
| 51. SCC                | DFS, Topo Sort         | 53. Tarjan's Bridge                 |
| 52. A* Search          | Dijkstra, Heuristic    | Pathfinding, AI                     |
| 53. Tarjan's Bridge    | DFS, lowlink concept   | 51. SCC (Tarjan)                     |
| 54. Counting/Radix     | Array, Sorting dasar   | Linear-time sorting                  |
| 55. Sliding Window     | Array, Two pointers    | 56. Kadane (subarray)               |
| 56. Kadane             | DP dasar               | 55. Sliding Window (overlap)         |
| 57. Minimax            | Trees, Recursion       | AI, Game Theory                      |
| 58. Mo's Algorithm     | Sorting, Map           | Range query, SQRT Decomposition      |
| 59. Convex Hull        | Geometry, Sorting      | Computational Geometry               |

## Memory vs Performance Summary

| Bab  | Nama Algoritma       | Waktu           | Ruang Tambahan | Tipe          |
|------|---------------------|-----------------|----------------|---------------|
| 50   | Topological Sort    | O(V+E)          | O(V)           | Graph         |
| 51   | Kosaraju SCC        | O(V+E)          | O(V+E)         | Graph         |
| 51   | Tarjan SCC          | O(V+E)          | O(V)           | Graph         |
| 52   | A* Search           | O(b^d)          | O(b^d)         | Graph/Search  |
| 53   | Tarjan's Bridge     | O(V+E)          | O(V)           | Graph         |
| 54   | Counting Sort       | O(n+k)          | O(k)           | Sorting       |
| 54   | Radix Sort          | O(d·n)          | O(n)           | Sorting       |
| 54   | Bucket Sort         | O(n+k) avg      | O(n)           | Sorting       |
| 55   | Sliding Window      | O(n)            | O(1)           | Array         |
| 55   | Two Pointers        | O(n)            | O(1)           | Array         |
| 56   | Kadane              | O(n)            | O(1)           | DP/Array      |
| 57   | Minimax             | O(b^d)          | O(d)           | Game          |
| 57   | Alpha-Beta          | O(b^(3d/4))     | O(d)           | Game          |
| 58   | Mo's Algorithm      | O((N+Q)√N)     | O(N)           | Range Query   |
| 59   | Convex Hull (Andrew)| O(N log N)      | O(N)           | Geometry      |

---

*Catatan: Semua kode Go dalam dokumen ini sudah compilable dan bisa dijalankan dengan `go run <filename>`. Untuk latihan, disarankan menulis ulang kode tanpa melihat referensi terlebih dahulu, lalu bandingkan dengan implementasi di atas.*

---

## 📚 BAB BONUS — TESTING, BENCHMARKING & PROFILING ALGORITMA GO

> **Mengapa ini penting?** Testing bukan sekadar "ngecek error" — ia adalah *spesifikasi yang bisa dieksekusi*. Benchmarking mengungkap *biaya* dari setiap baris kode. Profiling menjawab *kenapa* lambat. Tanpa ketiganya, optimasi algoritma hanyalah tebakan.

---

## Daftar Isi

1. [Table-Driven Tests untuk Algoritma](#1-table-driven-tests-untuk-algoritma)
2. [Benchmarking dengan `go test -bench`](#2-benchmarking-dengan-go-test--bench)
3. [Profiling dengan pprof (CPU + Memory)](#3-profiling-dengan-pprof-cpu--memory)
4. [Tracing dengan `go tool trace`](#4-tracing-dengan-go-tool-trace)
5. [Fuzzing untuk Algoritma](#5-fuzzing-untuk-algoritma)
6. [Contoh Konkret: Test + Benchmark Sorting Algorithm](#6-contoh-konkret-test--benchmark-sorting-algorithm)
7. [Memory Profiling: Deteksi Heap Escape, Alokasi Berlebih](#7-memory-profiling-deteksi-heap-escape-alokasi-berlebih)

---

### 1. Table-Driven Tests untuk Algoritma

### Definisi

**Table-Driven Test** adalah pola pengujian di mana *input*, *expected output*, dan (opsional) *test name* disusun dalam sebuah slice struct, lalu di-loop untuk menjalankan subtest (`t.Run`). Pola ini:

- Menghilangkan duplikasi kode test
- Membuat penambahan kasus uji trivial (tinggal tambah baris di table)
- Memberi isolasi per kasus (subtest bisa dijalankan selektif: `go test -run TestFoo/edge_case`)
- Memudahkan pembacaan: semua kasus uji terlihat sekilas

### Output Contoh

```
$ go test -v -run TestBinarySearch
=== RUN   TestBinarySearch
=== RUN   TestBinarySearch/target_di_tengah
=== RUN   TestBinarySearch/target_di_awal
=== RUN   TestBinarySearch/target_di_akhir
=== RUN   TestBinarySearch/slice_kosong
=== RUN   TestBinarySearch/satu_elemen_cocok
=== RUN   TestBinarySearch/satu_elemen_tidak_cocok
=== RUN   TestBinarySearch/dua_elemen
=== RUN   TestBinarySearch/target_tidak_ada_(di_antara)
=== RUN   TestBinarySearch/target_lebih_kecil_dari_min
=== RUN   TestBinarySearch/target_lebih_besar_dari_max
=== RUN   TestBinarySearch/duplikat_—_tetap_ditemukan
--- PASS: TestBinarySearch (0.00s)
    --- PASS: TestBinarySearch/target_di_tengah (0.00s)
    --- PASS: TestBinarySearch/target_di_awal (0.00s)
    --- PASS: TestBinarySearch/target_di_akhir (0.00s)
    --- PASS: TestBinarySearch/slice_kosong (0.00s)
    --- PASS: TestBinarySearch/satu_elemen_cocok (0.00s)
    --- PASS: TestBinarySearch/satu_elemen_tidak_cocok (0.00s)
    --- PASS: TestBinarySearch/dua_elemen (0.00s)
    --- PASS: TestBinarySearch/target_tidak_ada_(di_antara) (0.00s)
    --- PASS: TestBinarySearch/target_lebih_kecil_dari_min (0.00s)
    --- PASS: TestBinarySearch/target_lebih_besar_dari_max (0.00s)
    --- PASS: TestBinarySearch/duplikat_—_tetap_ditemukan (0.00s)
```

### Analisis

| Aspek | Keuntungan |
|-------|-----------|
| **Ekspresif** | Setiap baris di table = satu skenario. Nama test otomatis dari field `name` |
| **Isolasi** | Setiap `t.Run` adalah subtest; bisa dijalankan sendiri: `go test -run TestBinarySearch/duplikat` |
| **Disiplin** | Memaksa kita memikirkan *edge cases* secara eksplisit |
| **Regression-proof** | Tambah kode? Tambah satu baris di table. Bug fix? Tambah kasus yang dulu gagal |

> **Best practice**: Gunakan `t.Parallel()` di dalam subtest jika kasus uji independen. Tapi hati-hati dengan data race jika menggunakan slice yang sama.

---

### 2. Benchmarking dengan `go test -bench`

### Definisi

Benchmark mengukur **waktu eksekusi** dan **jumlah alokasi** dari sebuah fungsi. Go menyediakan `testing.B` yang menjalankan kode dalam loop `b.N` — jumlah iterasi otomatis disesuaikan oleh runtime agar benchmark berjalan sekitar 1 detik.

Metrik utama:
- **ns/op**: nanosecond per operasi (semakin kecil semakin cepat)
- **B/op**: bytes allocated per operasi
- **allocs/op**: jumlah alokasi heap per operasi

### Cara Setup

1. Buat fungsi `func BenchmarkXxx(b *testing.B)` di file `*_test.go`
2. Jalankan: `go test -bench=. -benchmem`

### Output Contoh

```
$ go test -bench=BenchmarkBinarySearch -benchmem -benchtime=1s
goos: darwin
goarch: arm64
pkg: algo
cpu: Apple M3 Pro

BenchmarkBinarySearch_Small-12          118472240                9.910 ns/op          0 B/op          0 allocs/op
BenchmarkBinarySearch_Medium-12          97031312               12.58 ns/op          0 B/op          0 allocs/op
BenchmarkBinarySearch_Large-12           85926482               13.99 ns/op          0 B/op          0 allocs/op
BenchmarkBinarySearch_Missing-12         82151433               14.97 ns/op          0 B/op          0 allocs/op
BenchmarkBinarySearch_Parallel-12        280761244                4.284 ns/op          0 B/op          0 allocs/op
```

### Interpretasi

| Benchmark | ns/op | Analisis |
|-----------|-------|----------|
| Small (100 el) | 9.91 ns | Cache L1/L2 masih hangat; prediksi branch hampir sempurna |
| Medium (10K) | 12.58 ns | log2(10000) ≈ 14 iterasi vs log2(100) ≈ 7, waktu naik ~27% |
| Large (1M) | 13.99 ns | log2(1_000_000) ≈ 20 iterasi; memory access pattern masih bagus |
| Missing (-1) | 14.97 ns | Worst case: tidak pernah early exit, full log2(n) langkah |
| Parallel | 4.28 ns | Speedup ~3.3x dari serial (12 core); scaling linear terbatas oleh memory bus |

**Poin penting**:
- `0 B/op, 0 allocs/op` berarti fungsi *zero-alloc* — tidak ada heap allocation sama sekali. Ini ideal untuk algoritma.
- Benchmark paralel menunjukkan *speedup* karena Binary Search adalah **read-only** (tidak ada data race), jadi aman di-parallel-kan.
- `benchtime=1s` adalah default; bisa diubah: `-benchtime=10s` untuk presisi lebih tinggi, `-benchtime=100x` untuk jumlah iterasi tetap.

### Sub-benchmark (Table-Driven Benchmark)

```
$ go test -bench=BenchmarkBinarySearch_Table -benchmem
BenchmarkBinarySearch_Table/small/found-12         118472240                9.91 ns/op
BenchmarkBinarySearch_Table/small/miss-12          105349284               11.32 ns/op
BenchmarkBinarySearch_Table/medium/found-12         97031312               12.58 ns/op
BenchmarkBinarySearch_Table/medium/miss-12          85627004               13.87 ns/op
BenchmarkBinarySearch_Table/large/found-12          85926482               13.99 ns/op
BenchmarkBinarySearch_Table/large/miss-12           79539077               15.01 ns/op
```

---

### 3. Profiling dengan pprof (CPU + Memory)

### Definisi

**pprof** adalah profiler built-in Go yang mengumpulkan sampel stack trace secara periodik. Dua mode utama:

| Profiler | Perintah | Guna |
|----------|----------|------|
| CPU | `-cpuprofile` | Menjawab "fungsi mana yang paling banyak menghabiskan CPU?" |
| Memory (heap) | `-memprofile` | Menjawab "fungsi mana yang paling banyak mengalokasi memory?" |
| Memory (all) | `-memprofile -memprofilerate=1` | Setiap alokasi dicatat (default: 1 per 512KB) |

### Cara Setup CPU Profiling

Atau langsung dari benchmark (cara paling idiomatis):

```
$ go test -bench=BenchmarkBinarySearch_Large -cpuprofile=cpu.prof -memprofile=mem.prof -benchtime=10s
```

### Analisis CPU Profile

```
$ go tool pprof -top cpu.prof
Showing nodes accounting for 3.52s, 99.72% of 3.53s total
Dropped 22 nodes (cum <= 0.02s)
      flat  flat%   sum%        cum   cum%
     3.52s 99.72% 99.72%      3.52s 99.72%  algo.BinarySearch
         0     0% 99.72%      3.52s 99.72%  algo.BenchmarkBinarySearch_Large.func1
         0     0% 99.72%      3.52s 99.72%  testing.(*B).launch
```

Kita lihat **99.72%** waktu di `BinarySearch` — tidak ada overhead lain. Ini ideal.

Untuk investigasi lebih dalam:

```
$ go tool pprof -http=:8080 cpu.prof
```

Browser akan menampilkan:
- **Graph** (SVG interaktif): kotak besar = fungsi mahal
- **Flame Graph**: sebaran waktu per call stack
- **Peek**: sumber panas per baris kode
- **Source**: anotasi tiap baris dengan konsumsi waktu

### Memory Profile

```
$ go tool pprof -alloc_objects -top mem.prof
Showing nodes accounting for 1048576, 100% of 1048576 total
      flat  flat%   sum%        cum   cum%
   1048576   100%   100%    1048576   100%  algo.generateSortedSlice
         0     0%   100%    1048576   100%  algo.BenchmarkBinarySearch_Large
```

Semua alokasi berasal dari `generateSortedSlice` — wajar. Yang perlu diwaspadai adalah alokasi di dalam *hot loop* algoritma.

### Melihat Source dengan Anotasi

```
$ go tool pprof -list BinarySearch cpu.prof
Total: 3.53s
ROUTINE ======================== algo.BinarySearch in /path/to/algo.go
     3.52s      3.52s (flat, cum) 99.72% of Total
         .          .      1: func BinarySearch(data []int, target int) int {
         .          .      2:     lo, hi := 0, len(data)-1
         .          .      3:     for lo <= hi {
     1.05s      1.05s      4:         mid := lo + (hi-lo)/2
     1.48s      1.48s      5:         if data[mid] == target {
     0.99s      0.99s      6:             return mid
         .          .      7:         }
         .          .      8:         if data[mid] < target {
         .          .      9:             lo = mid + 1
         .          .     10:         } else {
         .          .     11:             hi = mid - 1
         .          .     12:         }
         .          .     13:     }
         .          .     14:     return -1
         .          .     15: }
```

**Insight**: Baris 4-6 adalah yang paling mahal — akses memory `data[mid]` dan pembagian `(hi-lo)/2`. Tapi karena algoritma O(log n), ini tetap optimal.

---

### 4. Tracing dengan `go tool trace`

### Definisi

`go tool trace` memberikan visibilitas **time-based** tentang apa yang terjadi di goroutine: kapan mulai, kapan block (chan, syscall, GC, scheduler), dan berapa lama.

Berbeda dengan pprof yang memberi *sampel* (statistik), trace memberi **rekaman kronologis** — ideal untuk mendiagnosis:
- Goroutine leak
- Contention pada channel / mutex
- GC pause yang lama
- Network / syscall blocking

### Cara Setup

Atau langsung dengan `-trace` flag (Go 1.24+):

```
$ go test -bench=BenchmarkBinarySearch_Large -trace=trace.out -benchtime=5s
```

### Visualisasi

```
$ go tool trace trace.out
2025/05/16 01:00:00 Parsing trace...
2025/05/16 01:00:02 Splitting trace...
2025/05/16 01:00:03 Opening browser. Trace viewer is listening on http://127.0.0.1:57447
```

Browser menampilkan halaman dengan link ke beberapa view:

| View | Guna |
|------|------|
| **View trace** | Timeline per-goroutine (seperti Chrome DevTools) |
| **Goroutine analysis** | Statistik lifetime setiap goroutine |
| **Network blocking profile** | Durasi blocking karena network I/O |
| **Synchronization blocking profile** | Durasi blocking karena mutex/channel |
| **Syscall blocking profile** | Durasi blocking karena syscall |
| **Scheduler latency profile** | Distribusi waktu scheduling |

### Analisis untuk Binary Search (contoh konkuren)

Trace untuk algoritma di atas akan menunjukkan:

1. **Goroutine analysis**: 12 goroutine (1 main + 11 workers), lifetime ~100μs
2. **Synchronization blocking**: blocking di `results <- i` (chan send) saat worker menemukan
3. **Scheduler latency**: delay scheduling goroutine worker

```
Goroutine analysis:
  Id    Total time  Execution time  Sync block time  ...
  1     5.2s        0.1s            0.02s
  5     4.8s        3.2s            0.8s              (worker - menemukan target)
  6     4.9s        0.4s            3.9s              (worker - tidak menemukan)
```

Worker yang menemukan target punya **sync block time** lebih kecil karena segera kirim hasil. Worker lain blocking lebih lama di `results <- -1` karena main goroutine sibuk membaca.

---

### 5. Fuzzing untuk Algoritma

### Definisi

**Fuzzing** adalah teknik pengujian di mana input *random* (atau mutasi dari input seed) diberikan ke program untuk menemukan bug yang tidak terpikirkan oleh manusia.

Go 1.18+ memiliki fuzzing native. Berbeda dengan table-driven test yang inputnya fixed, fuzzing **secara otomatis mencari input yang membuat program panic, crash, atau melanggar invariant**.

### Cara Setup

### Menjalankan Fuzzing

```
# Mode fuzzing aktif (hingga 60 detik atau sampai ketemu bug):
$ go test -fuzz=FuzzBinarySearch -fuzztime=30s
=== FUZZ  FuzzBinarySearch
fuzz: elapsed 0s, gathering baseline coverage: 0/9 entries
fuzz: elapsed 0s, testing 1000/1000 entries, 0 failures
fuzz: elapsed 3s, testing 50000/50000 entries, 0 failures
fuzz: elapsed 6s, testing 100000/100000 entries, 0 failures
fuzz: elapsed 9s, testing 150000/150000 entries, 0 failures
fuzz: elapsed 12s, testing 200000/200000 entries, 0 failures
fuzz: elapsed 30s, testing 560352/560352 entries, 0 failures
...
*** Fuzzing finished after 30s. No crashes or failures found.
```

### Contoh Menemukan Bug

Misalkan kita implementasi Binary Search yang *salah*:

Fuzzing akan menemukan kasus di mana `lo + hi` overflow (meski jarang di Go karena int 64-bit, tapi jika `len(data)` mendekati `math.MaxInt`):

```
$ go test -fuzz=FuzzBinarySearch -fuzztime=30s
=== FUZZ  FuzzBinarySearch
fuzz: elapsed 0s, gathering baseline coverage: 0/9 entries
fuzz: elapsed 0s, testing 1000/1000 entries, 0 failures
fuzz: elapsed 5s, finding interesting mutations...
--- FAIL: FuzzBinarySearch (5.32s)
    --- FAIL: FuzzBinarySearch (0.00s)
        algo_fuzz_test.go:22: index out of range: idx=9223372036854775807, len=10

    Failing input written to testdata/fuzz/FuzzBinarySearch/...
    cat > testdata/fuzz/FuzzBinarySearch/2f7c6c7b2f7c6c7b
    go test -run=file/testdata/fuzz/FuzzBinarySearch/2f7c6c7b2f7c6c7b
```

Fuzzing otomatis menyimpan input yang gagal ke `testdata/fuzz/` untuk regression test.

### Analisis

| Aspek | Table-Driven Test | Fuzzing |
|-------|-------------------|---------|
| Input | Ditentukan manual | Digenereasi otomatis + mutasi |
| Coverage | Terbatas imajinasi penulis | Menjelajahi *edge cases* tak terduga |
| Invariant | Di-assert per test case | Di-assert dalam callback fuzz |
| Kecepatan | Instant | Membutuhkan waktu (30-300s) |
| Use case | Regresi, spesifikasi | Discovery bug, security |

**Kombinasi terbaik**: table-driven test untuk kasus yang diketahui + fuzzing untuk eksplorasi otomatis.

---

### 6. Contoh Konkret: Test + Benchmark Sorting Algorithm

Kita akan mengimplementasikan **Merge Sort** dan **Quick Sort**, lalu membandingkannya dengan `sort.Ints` dari standard library.

### Kode Algoritma

### Table-Driven Test

### Benchmark Perbandingan

### Output Benchmark

```
$ go test -bench=BenchmarkSorting -benchmem -benchtime=1s | head -40
goos: darwin
goarch: arm64
pkg: sortalgo

BenchmarkSorting/MergeSort/random/100-12             206376              5752 ns/op             896 B/op          3 allocs/op
BenchmarkSorting/MergeSort/random/1K-12                17876             66630 ns/op            8192 B/op          3 allocs/op
BenchmarkSorting/MergeSort/random/10K-12                1512            790384 ns/op           81920 B/op          3 allocs/op
BenchmarkSorting/MergeSort/random/100K-12                121           9757128 ns/op          819200 B/op          3 allocs/op

BenchmarkSorting/QuickSort/random/100-12             665254              1804 ns/op             896 B/op          1 allocs/op
BenchmarkSorting/QuickSort/random/1K-12                72544             16489 ns/op            8192 B/op          1 allocs/op
BenchmarkSorting/QuickSort/random/10K-12                6572            181573 ns/op           81920 B/op          1 allocs/op
BenchmarkSorting/QuickSort/random/100K-12                 536           2206947 ns/op          819200 B/op          1 allocs/op

BenchmarkSorting/Stdlib/random/100-12               1910750               627.0 ns/op             0 B/op          0 allocs/op
BenchmarkSorting/Stdlib/random/1K-12                  214392              5600 ns/op               0 B/op          0 allocs/op
BenchmarkSorting/Stdlib/random/10K-12                  17022             70211 ns/op               0 B/op          0 allocs/op
BenchmarkSorting/Stdlib/random/100K-12                  1502            805640 ns/op               0 B/op          0 allocs/op
```

### Analisis Perbandingan

| Algoritma | 100 elemen | 10K elemen | 100K elemen | Alokasi | Catatan |
|-----------|-----------|------------|-------------|---------|---------|
| **MergeSort** | 5.752 ns | 790 μs | 9.757 μs | 3 allocs/op | Stable, O(n log n), tapi boros memori (alokasi slice baru tiap rekursi) |
| **QuickSort** | 1.804 ns | 181 μs | 2.207 μs | 1 allocs/op | In-place, lebih cepat, tapi tidak stable |
| **sort.Ints** | **627 ns** | **70 μs** | **806 μs** | **0 allocs/op** | ~3-10x lebih cepat; pakai pattern hybrid (quickSort + heapSort + insertionSort) |

**Insight penting**:
1. **`sort.Ints` selalu menang** — karena menggunakan algoritma hybrid yang sangat optimal (pdqsort sejak Go 1.21)
2. **QuickSort 2-3x lebih cepat dari MergeSort** untuk random data (lebih sedikit alokasi, cache-friendly)
3. **MergeSort alokasi 3x per panggilan** — mahal untuk GC
4. Pada data **sorted** dan **reversed**, QuickSort dengan median-of-three tetap O(n log n)

```
BenchmarkSorting/QuickSort/sorted/100K-12                576           2072584 ns/op
BenchmarkSorting/QuickSort/reversed/100K-12               581           2069831 ns/op
BenchmarkSorting/MergeSort/sorted/100K-12                 120           9875321 ns/op
BenchmarkSorting/Stdlib/sorted/100K-12                  29083             41285 ns/op
```

`sort.Ints` mendeteksi data sudah terurut dan **hanya O(n)** — ini karena pdqsort punya *pattern-breaking detection*.

---

### 7. Memory Profiling: Deteksi Heap Escape, Alokasi Berlebih

### Definisi

**Heap escape** terjadi ketika variabel yang dialokasikan di stack *harus* pindah ke heap karena:
- *return pointer* ke lokal variabel
- *closure* yang mereferensi variabel
- *interface* boxing
- *goroutine* yang menggunakan variabel stack goroutine lain
- `defer` dalam loop
- Slice yang *escape* karena ukuran tidak diketahui saat kompilasi

**Escape analysis** dilakukan compiler Go. Kita bisa mendeteksinya dengan `-gcflags="-m"` atau dengan pprof.

### Deteksi dengan `-gcflags="-m"`

```
$ go build -gcflags="-m -m" escape.go 2>&1 | grep escape
./escape.go:12:6: result escapes to heap:
./escape.go:12:6:   flow: ~r0 = &result:
./escape.go:12:6:     from &result (address-of) at ./escape.go:16:9
./escape.go:12:6:     from return &result (return) at ./escape.go:16:2
./escape.go:12:6: moved to heap: result
./escape.go:27:24: i escapes to heap:
./escape.go:27:24:   flow: ~r0 = i:
./escape.go:27:24:     from return i (return) at ./escape.go:29:3
./escape.go:27:24:   flow: ~r0 = i:
./escape.go:27:24:     from i (interface-converted) at ./escape.go:29:3
./escape.go:27:24: i escapes to heap
```

### Benchmark dengan `-benchmem`

### Output Benchmark

```
$ go test -bench=BenchmarkFind -benchmem
BenchmarkFindWithPointer-12        13444106                88.95 ns/op           48 B/op          1 allocs/op
BenchmarkFindWithValue-12          18794268                64.14 ns/op            0 B/op          0 allocs/op
BenchmarkFindViaInterface-12       10785494               109.7 ns/op             8 B/op          1 allocs/op
```

### Analisis

| Fungsi | ns/op | B/op | allocs/op | Penyebab |
|--------|-------|------|-----------|----------|
| `findWithPointer` | 88.95 | 48 | 1 | `SearchResult` escape ke heap karena return pointer |
| `findWithValue` | **64.14** | **0** | **0** | Return by value — stack allocated |
| `findViaInterface` | 109.7 | 8 | 1 | `int` diboxing ke `interface{}` |

**Dampak**: `findWithPointer` 38% lebih lambat dari `findWithValue` karena:
1. Biaya alokasi heap (48 bytes)
2. Biaya GC — objek harus di-scan mark-sweep
3. Cache miss — heap tidak selokal stack

### Deteksi Alokasi Berlebih dengan pprof

```
$ go test -bench=BenchmarkFindWithPointer -benchmem -memprofile=mem.prof
$ go tool pprof -alloc_objects -top mem.prof
```

Atau lihat flame graph:

```
$ go tool pprof -http=:8080 mem.prof
```

### Profiling Allocations di Aplikasi Nyata

Untuk aplikasi yang sudah berjalan, gunakan:

Lalu ambil heap profile:

```
$ go tool pprof http://localhost:6060/debug/pprof/heap
$ go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

### Tips Mengurangi Heap Allocation

| Pattern | Daripada | Gunakan |
|---------|----------|---------|
| Return pointer | `func() *BigStruct` | `func() BigStruct` |
| Interface parameter | `func(i interface{})` | `func(i T)` atau generic `func[T any](i T)` |
| Slice growing | `append` di hot loop | `make` dengan capacity yang diketahui |
| String concatenation | `s += "more"` | `strings.Builder` |
| Temporary buffer | `make([]byte, n)` di hot loop | Pool: `sync.Pool` |
| Closure loop variable | `go func() { use(i) }()` | `go func(i int) { use(i) }(i)` |

---

---

## 📊 APPENDIX — MASTER CHEAT SHEET

### Big-O Lengkap per Struktur Data

| Struktur | Access | Search | Insert | Delete | Space | Cache |
|----------|--------|--------|--------|--------|-------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) | **Excellent** |
| Stack (slice) | O(n) | O(n) | O(1) amort | O(1) | O(n) | Good |
| Queue (ring buf) | O(n) | O(n) | O(1) | O(1) | O(cap) | Good |
| Singly Linked List | O(n) | O(n) | O(1) head | O(1) head | O(n) | **Poor** (pointer chase) |
| Doubly Linked List | O(n) | O(n) | O(1) | O(1) | O(n) | **Poor** |
| Hash Table | N/A | O(1) avg | O(1) avg | O(1) avg | O(n) | Random |
| BST | O(log n) avg | O(log n) avg | O(log n) avg | O(log n) avg | O(n) | **Poor** (scattered) |
| AVL Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) | **Poor** |
| Red-Black Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) | **Poor** |
| B-Tree (m=100) | O(log_m n) | O(log_m n) | O(log_m n) | O(log_m n) | O(n) | Good (per node) |
| Binary Heap | O(1) peek | O(n) | O(log n) | O(log n) | O(n) | **Excellent** (array) |
| Fenwick Tree | N/A | O(log n) | O(log n) | N/A | O(n) | **Excellent** |
| Segment Tree | N/A | O(log n) | O(log n) | O(log n) | O(4n) | Good |
| Trie | O(L) | O(L) | O(L) | O(L) | O(Σⁿ) | Random |
| Bloom Filter | N/A | O(k) | O(k) | N/A | O(m) | Random |
| Suffix Array | O(m log n) | O(n log n) | — | — | O(n) | Good |

### Memory Hierarchy Impact

| Level | Size | Latency | Managed by |
|-------|------|---------|------------|
| L1 Cache | 32-64KB | ~1ns (4 cycles) | CPU |
| L2 Cache | 256-512KB | ~4ns (12 cycles) | CPU |
| L3 Cache | 4-32MB | ~12ns (40 cycles) | CPU |
| RAM (Main) | 8-64GB | ~100ns | OS/Kernel |
| SSD | 256GB-4TB | ~100μs | OS/Kernel |

**Gold Rules for Cache-Friendly Code:**
1. **Contiguous access** (sequential) > random access
2. **Array of structs** > struct of arrays (untuk sebagian besar kasus)
3. **Avoid pointer chasing** (linked list, tree nodes scattered)
4. **Pre-allocate slices** — `make([]T, 0, n)` hindari multiple allocations
5. **Use array-based structures** ketika memungkinkan (heap, BIT, segment tree)

---

> *Rangkuman komprehensif DSAG — 59 Bab, 12 Part*

---

## 📚 CLOSING REMARK — Refleksi Akhir

**🎯 Apa yang Sudah Kamu Pelajari:**
- 12 Part, 59 Bab, dari array hingga convex hull
- Go memory model, stack vs heap, pointer, escape analysis
- Algoritma sorting, searching, graph, string, dan probabilistic
- Paradigma: D&C, DP, Greedy, Backtracking, Randomized
- Advanced: B-Tree, Bloom Filter, A*, Minimax, Mo's, Convex Hull
- Filosofi: algoritma sebagai compressed wisdom

**🧠 Tiga Pelajaran Paling Penting:**

1. **Algoritma adalah tentang trade-offs.** Tidak ada struktur data "terbaik" — yang ada adalah "paling cocok untuk constraints-mu". Big-O hanyalah satu dimensi. Cache behavior, GC pressure, maintainability, dan team skill sama pentingnya.

2. **Pilih alat yang tepat.** Problem menentukan algoritma, bukan sebaliknya. Pahami karakteristik datamu (size, distribution, access pattern) sebelum memilih struktur data.

3. **Praktek > Teori.** Membaca 59 bab tidak cukup. Implementasi sendiri, benchmark, dan debug adalah cara sejati untuk menguasai DSA.

**📊 Rekomendasi Jalur Belajar:**

| Level | Fokus | Bab |
|-------|-------|-----|
| Beginner | Foundations + Basic DS | 1-8 |
| Intermediate | Sorting, Searching, Trees, Graphs | 9-21 |
| Advanced | Paradigms, Graph Algos | 22-27, 13-18 |
| Expert | Advanced DS, Concurrent, Profiling | 28-59 |

**🚀 Langkah Selanjutnya:**
1. Implementasi ulang setiap algoritma dari ingatan
2. Selesaikan semua latihan di setiap bab
3. Buka LeetCode/HackerRank dan aplikasikan
4. Gunakan `go test -bench` untuk benchmark solusi
5. Baca source code Go stdlib — `sort`, `container/heap`, `crypto/sha256`

> *"An algorithm must be seen to be believed."* — Donald Knuth

---

> *Dibuat: 16 Mei 2026*
> *Webbook: https://akmalgomal3.github.io/dsag-webbook/*
