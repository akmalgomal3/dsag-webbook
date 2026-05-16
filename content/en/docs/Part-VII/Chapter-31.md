---
weight: 70400
title: "Chapter 31: Blockchain Data Structures and Algorithms"
description: "Blockchain Data Structures and Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>Blockchain is the tech. Bitcoin is merely the first mainstream manifestation of its potential.</em>" — Marc Kenigsberg</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 31 covers blockchain data structures. Hash chains. Merkle trees. Proof of Work. Go implementation.
{{% /alert %}}

## 31.1. Block Structure

**Definition:** Block holds transactions. Hash references previous block. Chain remains immutable.

**Mechanics:**
Cryptographic immutability ensures data integrity. Data modification invalidates subsequent chain. Trustless verification enabled.

**Use Cases:**
Bitcoin. Ethereum smart contracts. Supply chain tracking. Decentralized voting. Transparent ledger required.

**Memory Mechanics:**
SHA-256 uses CPU registers. Bitwise operations frequent. <abbr title="Memory used for dynamic allocation, distinct from the call stack.">Heap</abbr> usage minimal. ALU utilization maximized. Mining alters `nonce` integer in memory. Payload stays in L1 <abbr title="A smaller, faster memory closer to a processor core.">CPU cache</abbr>.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Create block | <code>O(t)</code> | t: transaction count |
| Hash block | <code>O(t)</code> | SHA-256 over data |
| Verification | <code>O(1)</code> | Hash comparison |
| Append | <code>O(1)</code> | Attach to end |

### Pseudocode

```text
CalculateHash(block):
    record = concat(block.Index, block.Timestamp, block.Data, block.PrevHash, block.Nonce)
    return SHA256(record)

CreateBlock(index, data, prevHash):
    block = new Block(index, current time, data, prevHash, nonce=0)
    block.Hash = CalculateHash(block)
    return block

IsValid(newBlock, prevBlock):
    if prevBlock.Index + 1 != newBlock.Index: return false
    if newBlock.PrevHash != prevBlock.Hash: return false
    if CalculateHash(newBlock) != newBlock.Hash: return false
    return true
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
    "time"
)

type Block struct {
    Index        int
    Timestamp    int64
    Data         string
    PrevHash     string
    Hash         string
    Nonce        int
}

func calculateHash(b Block) string {
    record := fmt.Sprintf("%d%d%s%s%d", b.Index, b.Timestamp, b.Data, b.PrevHash, b.Nonce)
    h := sha256.Sum256([]byte(record))
    return hex.EncodeToString(h[:])
}

func createBlock(index int, data string, prevHash string) Block {
    b := Block{
        Index:     index,
        Timestamp: time.Now().Unix(),
        Data:      data,
        PrevHash:  prevHash,
        Nonce:     0,
    }
    b.Hash = calculateHash(b)
    return b
}

func isValid(newBlock, prevBlock Block) bool {
    if prevBlock.Index+1 != newBlock.Index {
        return false
    }
    if newBlock.PrevHash != prevBlock.Hash {
        return false
    }
    if calculateHash(newBlock) != newBlock.Hash {
        return false
    }
    return true
}

func main() {
    genesis := createBlock(0, "Genesis", "0")
    block1 := createBlock(1, "Tx1", genesis.Hash)
    fmt.Println("Valid:", isValid(block1, genesis))
    fmt.Println("Genesis hash:", genesis.Hash)
}
```

{{% alert icon="📌" context="warning" %}}
Use `crypto/sha256` for hashing. `time.Now()` is manipulated easily. Prefer NTP sync or consensus timestamps.
{{% /alert %}}

### Decision Matrix

| Use Standard Arrays When... | Avoid If... |
|----------------------|------------------|
| Local single-node chain | Distributed consensus systems |
| Prototyping | Production without security audit |

### Edge Cases & Pitfalls

- **Genesis block:** Verify chain starts from trusted genesis.
- **Hash <abbr title="An event when two keys hash to the same index.">collision</abbr>:** SHA-256 <abbr title="An event when two keys hash to the same index.">collision</abbr> improbable. Theoretically possible.
- **Longest chain:** PoW follows chain with highest cumulative difficulty.

## 31.2. Merkle Tree

**Definition:** Hierarchical hash tree. <abbr title="A node with no children in a tree.">Leaf</abbr> is transaction hash. Parent is child hash concatenation.

### Operations & Complexity

| Operation | Complexity | Description |
|---------|--------------|------------|
| Build | <code>O(n)</code> | n: transaction count |
| <abbr title="The topmost node in a tree data structure.">Root</abbr> | <code>O(1)</code> | Peak hash |
| Proof inclusion | <code>O(log n)</code> | Process log n siblings |
| Verify proof | <code>O(log n)</code> | Recompute <abbr title="A sequence of edges connecting a sequence of distinct vertices.">path</abbr> to <abbr title="The topmost node in a tree data structure.">root</abbr> |

### Pseudocode

```text
BuildMerkleRoot(transactions):
    if length(transactions) == 0: return ""
    if length(transactions) == 1: return transactions[0]
    level = empty list
    for i from 0 to length(transactions)-1 step 2:
        left = transactions[i]
        right = transactions[i]
        if i+1 < length(transactions):
            right = transactions[i+1]
        level.append(HashPair(left, right))
    return BuildMerkleRoot(level)
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
)

func hashPair(a, b string) string {
    h := sha256.Sum256([]byte(a + b))
    return hex.EncodeToString(h[:])
}

func buildMerkleRoot(transactions []string) string {
    if len(transactions) == 0 {
        return ""
    }
    if len(transactions) == 1 {
        return transactions[0]
    }
    var level []string
    for i := 0; i < len(transactions); i += 2 {
        left := transactions[i]
        right := left
        if i+1 < len(transactions) {
            right = transactions[i+1]
        }
        level = append(level, hashPair(left, right))
    }
    return buildMerkleRoot(level)
}

func main() {
    txs := []string{
        "tx1-hash", "tx2-hash", "tx3-hash", "tx4-hash",
    }
    root := buildMerkleRoot(txs)
    fmt.Println("Merkle Root:", root)
}
```

{{% alert icon="📌" context="warning" %}}
Duplicate last hash for odd counts. Parity required between build and verify logic.
{{% /alert %}}

### Decision Matrix

| Use Merkle Tree When... | Avoid If... |
|----------------------------|------------------|
| Verify transaction subset | All transactions required immediately |
| Build light clients | Micro datasets. Tree overhead high. |

### Edge Cases & Pitfalls

- **Odd leaves:** Duplicate final hash before pairing.
- **Second preimage attack:** Prefix <abbr title="A node with no children in a tree.">leaf</abbr> and internal <abbr title="A basic unit of a data structure, containing data and possibly links to other nodes.">node</abbr> hashes.

## 31.3. Proof of Work

**Definition:** Miner finds nonce. Resulting hash matches difficulty target.

### Operations & Complexity

| Parameter | Complexity | Description |
|-----------|--------------|------------|
| Mining | <code>O(2^d)</code> | d: difficulty bits |
| Verification | <code>O(1)</code> | Single hash execution |
| Difficulty adjust | <code>O(1)</code> | Calculated per block epoch |

### Pseudocode

```text
Mine(data, prevHash, difficulty):
    prefix = string of difficulty zeros
    nonce = 0
    loop:
        record = concat(data, prevHash, nonce)
        hash = SHA256(record)
        if hash starts with prefix:
            return hash, nonce
        nonce += 1
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
    "strings"
)

func mine(data string, prevHash string, difficulty int) (string, int) {
    prefix := strings.Repeat("0", difficulty)
    var nonce int
    for {
        record := fmt.Sprintf("%s%s%d", data, prevHash, nonce)
        hash := sha256.Sum256([]byte(record))
        hashStr := hex.EncodeToString(hash[:])
        if strings.HasPrefix(hashStr, prefix) {
            return hashStr, nonce
        }
        nonce++
    }
}

func main() {
    hash, nonce := mine("hello", "prev123", 4)
    fmt.Printf("Hash: %s, Nonce: %d\n", hash, nonce)
}
```

{{% alert icon="📌" context="warning" %}}
Production PoW requires dynamic difficulty. P2P consensus required. Go suboptimal for GPU mining.
{{% /alert %}}

### Decision Matrix

| Use PoW When... | Avoid If... |
|--------------------|------------------|
| Uncompromising decentralization | Energy efficiency required |
| Byzantine fault tolerance | High <abbr title="The amount of data processed in a given amount of time.">throughput</abbr> required |

### Edge Cases & Pitfalls

- **Difficulty too low:** Susceptible to rapid attacks.
- **Timestamp manipulation:** Miners skew difficulty via timestamps.

## 31.4. Basic Consensus Algorithms

**Definition:** Distributed nodes agree on state.

### Operations & Complexity

| Algorithm | Communication | Fault Tolerance | Description |
|-----------|------------|-----------------|------------|
| PoW | Broadcast | 51% | Bitcoin style |
| PoS | Broadcast | 33% | Ethereum style |
| PBFT | <code>O(n²)</code> | f < n/3 | Permissioned systems |
| Raft | <code>O(n)</code> | Leader failure | Key-value stores |

### Decision Matrix

| Use Raft/PBFT When... | Use PoW/PoS When... |
|--------------------------|------------------------|
| Network permissioned | Network permissionless |
| Validators known | Anonymous participants |
| Low latency required | Maximum decentralization priority |

### Edge Cases & Pitfalls

- **Nothing-at-stake:** PoS validator votes on multiple forks. Severe slashing punishes behavior.
- **Long-range attack:** Old private keys build alternative chain.

### Anti-Patterns

- **`time.Now()` for timestamps:** Miners manipulate time. System clocks skew. Use consensus timestamps.
- **Ignore longest-chain rule:** PoW follows highest cumulative difficulty. Short chain with many blocks is weak.
- **Odd leaf Merkle:** Parity failure breaks root consistency. Duplicate last hash.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| Block | `struct` | <code>O(1)</code> create | <code>O(1)</code> | Transaction container |
| Merkle Tree | recursive hash | <code>O(n)</code> build | <code>O(n)</code> | Subset verification |
| PoW Mining | brute-force loop | <code>O(2^k)</code> | . | Consensus foundation |
| Chain | `[]Block` | <code>O(1)</code> append | grows | Ledger backbone |
| Hash | `crypto/sha256` | <code>O(n)</code> | 32 bytes | Data integrity |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 31:</strong> Blockchain uses linked blocks with SHA-256. Merkle trees enable subset verification. PoW provides decentralization. PoS improves energy efficiency. Consensus ensures distributed state agreement.
{{% /alert %}}

## See Also

- [Chapter 29: Parallel and Distributed Algorithms](/docs/part-vii/chapter-29/)
- [Chapter 30: Cryptographic Foundations Algorithms](/docs/part-vii/chapter-30/)
- [Chapter 36: Trie Data Structures](/docs/part-vii/chapter-36/)
