---
weight: 70300
title: "Chapter 31 - Cryptographic Foundations Algorithms"
description: "Cryptographic Foundations Algorithms"
icon: "article"
date: "2024-08-24T23:42:47+07:00"
lastmod: "2024-08-24T23:42:47+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>To keep a system secure, we need to be always on our toes. If we wait for the attackers to find vulnerabilities, it's already too late.</em>" — Whitfield Diffie</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 31 explores cryptographic primitives: hash functions, symmetric encryption, asymmetric encryption, and digital signatures utilizing Go's standard <abbr title="A collection of precompiled routines that a program can use.">library</abbr>.
{{% /alert %}}

## 31.1. Hash Functions

**Definition:** A hash function maps arbitrary inputs to deterministic fixed-size outputs. Cryptographic hashes must be robustly preimage-resistant and collision-resistant.

### Operations & Complexity

| Algorithm | Output Size | Security <abbr title="The set of all nodes at a given depth.">Level</abbr> | Description |
|-----------|-------------|----------|------------|
| SHA-256 | 256 bits | Secure | Industry standard |
| SHA-512 | 512 bits | Secure | Slower, but larger bounds |
| MD5 | 128 bits | Broken | Do not use |
| SHA-1 | 160 bits | Broken | Deprecated |

### Pseudocode

```text
HashSHA256(data):
    h = SHA256(data)
    return encode hex(h)
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
)

func hashSHA256(data []byte) string {
    h := sha256.Sum256(data)
    return hex.EncodeToString(h[:])
}

func main() {
    data := []byte("hello world")
    fmt.Println("SHA-256:", hashSHA256(data))
}
```

{{% alert icon="📌" context="warning" %}}
Strictly rely on `crypto/sha256` or `crypto/sha512` from the stdlib. Avoid MD5 and SHA-1 for security contexts entirely. For password hashing, utilize `golang.org/x/crypto/bcrypt` or `argon2`.
{{% /alert %}}

### Decision Matrix

| Use SHA-256 When... | Avoid If... |
|------------------------|------------------|
| Performing data integrity checks | Storing passwords (use bcrypt/argon2 instead) |
| Generating cryptographic checksums | You need raw speed without security (use xxhash) |

### Edge Cases & Pitfalls

- **Length extension attacks:** SHA-256 is vulnerable to length extension attacks. Employ HMACs when necessary.
- **Timing attacks:** Never compare hashes utilizing the standard `==` operator. Always use `hmac.Equal` or `subtle.ConstantTimeCompare`.

## 31.2. Symmetric Encryption

**Definition:** Symmetric encryption utilizes the exact same <abbr title="A field or set of fields used to identify a record.">key</abbr> for both encryption and decryption. AES-GCM stands as the heavily recommended standard mode.

### Operations & Complexity

| Algorithm | <abbr title="A field or set of fields used to identify a record.">Key</abbr> Size | Mode | Security <abbr title="The set of all nodes at a given depth.">Level</abbr> |
|-----------|----------|------|----------|
| AES-128 | 128 bits | GCM | Secure |
| AES-256 | 256 bits | GCM | Secure |
| ChaCha20-Poly1305 | 256 bits | AEAD | Secure, strong alternative |

### Pseudocode

```text
EncryptAESGCM(plaintext, key):
    block = AES(key)
    gcm = GCM(block)
    nonce = random bytes of size gcm.NonceSize
    ciphertext = gcm.Seal(nonce, nonce, plaintext, nil)
    return encode hex(ciphertext), encode hex(nonce)

DecryptAESGCM(ciphertextHex, key):
    ciphertext = decode hex(ciphertextHex)
    block = AES(key)
    gcm = GCM(block)
    nonceSize = gcm.NonceSize
    nonce = ciphertext[0:nonceSize]
    ciphertext = ciphertext[nonceSize:]
    return gcm.Open(nil, nonce, ciphertext, nil)
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "encoding/hex"
    "fmt"
    "io"
)

func encryptAESGCM(plaintext, key []byte) (string, string, error) {
    block, err := aes.NewCipher(key)
    if err != nil {
        return "", "", err
    }
    gcm, err := cipher.NewGCM(block)
    if err != nil {
        return "", "", err
    }
    nonce := make([]byte, gcm.NonceSize())
    if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
        return "", "", err
    }
    ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
    return hex.EncodeToString(ciphertext), hex.EncodeToString(nonce), nil
}

func decryptAESGCM(ciphertextHex string, key []byte) ([]byte, error) {
    ciphertext, err := hex.DecodeString(ciphertextHex)
    if err != nil {
        return nil, err
    }
    block, err := aes.NewCipher(key)
    if err != nil {
        return nil, err
    }
    gcm, err := cipher.NewGCM(block)
    if err != nil {
        return nil, err
    }
    nonceSize := gcm.NonceSize()
    nonce, ciphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]
    return gcm.Open(nil, nonce, ciphertext, nil)
}

func main() {
    key := make([]byte, 32)
    if _, err := io.ReadFull(rand.Reader, key); err != nil {
        panic(err)
    }
    plain := []byte("secret message")
    ct, _, err := encryptAESGCM(plain, key)
    if err != nil {
        panic(err)
    }
    pt, err := decryptAESGCM(ct, key)
    if err != nil {
        panic(err)
    }
    fmt.Println("Decrypted:", string(pt))
}
```

{{% alert icon="📌" context="warning" %}}
The nonce MUST be completely unique per encryption event when utilizing the same <abbr title="A field or set of fields used to identify a record.">key</abbr>. The standard GCM nonce size is 12 bytes. Never reuse nonces under any circumstance.
{{% /alert %}}

### Decision Matrix

| Use AES-GCM When... | Avoid If... |
|------------------------|------------------|
| Encrypting data at rest or in transit | Lacking authentication (use CBC+HMAC, or strictly GCM) |
| Hardware AES-NI is physically available | Operating on embedded systems lacking AES support (use ChaCha20 instead) |

### Edge Cases & Pitfalls

- **<abbr title="A field or set of fields used to identify a record.">Key</abbr> reuse with identical nonce:** A fatal security flaw for GCM. Consistently generate cryptographically random nonces.
- **Unauthenticated encryption:** ECB and CBC modes (without HMAC) are vulnerable to tampering and modifications.
- **IV reuse in CTR mode:** This error completely shatters the encryption's security.

## 31.3. Asymmetric Encryption

**Definition:** Asymmetric encryption utilizes a specific pair of public (encryption) and private (decryption) keys. RSA and ECDSA serve as the established standards.

### Operations & Complexity

| Algorithm | <abbr title="A field or set of fields used to identify a record.">Key</abbr> Size | Sign | Verify | Description |
|-----------|----------|------|--------|------------|
| RSA-2048 | 2048 bits | <code>O(n³)</code> | <code>O(n^2)</code> | Aging standard |
| RSA-4096 | 4096 bits | <code>O(n³)</code> | <code>O(n^2)</code> | More secure, much slower |
| ECDSA P-256 | 256 bits | <code>O(n^2)</code> | <code>O(n^2)</code> | Considerably faster, shorter |
| Ed25519 | 256 bits | <code>O(n^2)</code> | <code>O(n^2)</code> | Modern, heavily recommended |

### Pseudocode

```text
GenerateECDSAKey():
    privateKey = generate key on curve P256
    privBytes = marshal private key
    privPEM = PEM encode privBytes
    return privateKey, privPEM

SignECDSA(privateKey, message):
    hash = SHA256(message)
    r, s = ECDSA sign(privateKey, hash)
    signature = concat(r bytes, s bytes)
    return signature, hash
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/ecdsa"
    "crypto/elliptic"
    "crypto/rand"
    "crypto/sha256"
    "crypto/x509"
    "encoding/pem"
    "fmt"
)

func generateECDSAKey() (*ecdsa.PrivateKey, []byte, error) {
    priv, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
    if err != nil {
        return nil, nil, err
    }
    privBytes, err := x509.MarshalECPrivateKey(priv)
    if err != nil {
        return nil, nil, err
    }
    privPEM := pem.EncodeToMemory(&pem.Block{Type: "EC PRIVATE KEY", Bytes: privBytes})
    return priv, privPEM, nil
}

func signECDSA(priv *ecdsa.PrivateKey, msg []byte) ([]byte, []byte, error) {
    hash := sha256.Sum256(msg)
    r, s, err := ecdsa.Sign(rand.Reader, priv, hash[:])
    if err != nil {
        return nil, nil, err
    }
    sig := append(r.Bytes(), s.Bytes()...)
    return sig, hash[:], nil
}

func main() {
    priv, _, err := generateECDSAKey()
    if err != nil {
        panic(err)
    }
    msg := []byte("authenticate this")
    sig, hash, err := signECDSA(priv, msg)
    if err != nil {
        panic(err)
    }
    valid := ecdsa.Verify(&priv.PublicKey, hash, nil, nil)
    fmt.Println("Signature valid (placeholder):", len(sig) > 0 && valid)
}
```

{{% alert icon="📌" context="warning" %}}
`crypto/ecdsa` yields a raw signature (r, s) that frequently requires encoding (ASN.1 DER) for broad interoperability. For modern applications, strongly prefer `crypto/ed25519` as it's considerably simpler.
{{% /alert %}}

### Decision Matrix

| Use Ed25519 When... | Avoid If... |
|------------------------|------------------|
| Needing new digital signatures | Working within legacy systems demanding RSA |
| Performance is highly critical | Actually needing raw encryption (Ed25519 only signs data) |

### Edge Cases & Pitfalls

- **Randomness quality:** Keys and signatures depend intensely upon `crypto/rand`. Never utilize the insecure `math/rand`.
- **Timing attacks:** ECDSA verification must run in strict constant-time. Go's standard <abbr title="A collection of precompiled routines that a program can use.">library</abbr> reliably handles this.

## 31.4. Digital Signatures and HMAC

**Definition:** HMAC (Hash-based Message Authentication Code) leverages a secret <abbr title="A field or set of fields used to identify a record.">key</abbr> to authenticate data integrity. Digital signatures use asymmetric keys to ensure robust non-repudiation.

### Operations & Complexity

| Primitive | <abbr title="A field or set of fields used to identify a record.">Key</abbr> Type | Size | Description |
|----------|----------|------|------------|
| HMAC-SHA256 | Symmetric | 256 bits | Message authentication |
| ECDSA | Asymmetric | 512 bits signature | Ensures non-repudiation |
| Ed25519 | Asymmetric | 64 bytes signature | Modern, exceptionally fast |

### Pseudocode

```text
HMACSHA256(message, key):
    h = HMAC(SHA256, key)
    h.update(message)
    return encode hex(h.digest())

VerifyHMAC(message, key, mac):
    expected = HMACSHA256(message, key)
    return constant time compare(expected, mac)
```

### Idiomatic Go Implementation

```go
package main

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "fmt"
)

func hmacSHA256(message, key []byte) string {
    h := hmac.New(sha256.New, key)
    h.Write(message)
    return hex.EncodeToString(h.Sum(nil))
}

func verifyHMAC(message, key []byte, mac string) bool {
    expected := hmacSHA256(message, key)
    return hmac.Equal([]byte(expected), []byte(mac))
}

func main() {
    key := []byte("super-secret-key")
    msg := []byte("authenticated message")
    mac := hmacSHA256(msg, key)
    fmt.Println("HMAC:", mac)
    fmt.Println("Verify:", verifyHMAC(msg, key, mac))
}
```

{{% alert icon="📌" context="warning" %}}
Always utilize `hmac.Equal` to perform constant-time comparisons. Never execute a standard `==` to evaluate a MAC.
{{% /alert %}}

### Decision Matrix

| Use HMAC When... | Use Digital Signature When... |
|---------------------|----------------------------------|
| Both involved parties possess the shared secret <abbr title="A field or set of fields used to identify a record.">key</abbr> | Genuine non-repudiation is mandatory |
| Performance is highly critical | The verification step occurs via a third party |

### Edge Cases & Pitfalls

- **<abbr title="A field or set of fields used to identify a record.">Key</abbr> length < hash size:** HMAC automatically hashes the key first. Keys shorter than the block size are acceptable.
- **Truncated MAC:** Do not truncate an HMAC signature without undergoing a rigorous security analysis.

## 31.5. Password Hashing

**Definition:** Password hashing (distinct from encryption) represents a deliberately slow one-way function engineered specifically to thwart brute-force attacks.

### Operations & Complexity

| Algorithm | Work Factor | Memory | Description |
|-----------|-------------|--------|------------|
| bcrypt | Cost 10-14 | Low | Legacy standard, sufficiently secure |
| scrypt | N, r, p | Configurable | Memory-hard defense |
| Argon2 | Time, Memory | High | PHC winner, highly recommended |

### Pseudocode


### Idiomatic Go Implementation


... (10) might be insufficient for modern computing speeds. Consider bumping the cost to 12-14. For entirely greenfield projects, employ Argon2id.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| SHA-256 | ... | ... | — | Data integrity |
| AES-GCM | ... + cipher | ... | — | Standard symmetric encryption |
| HMAC | ... | ... | — | Authenticate messages |
| ECDSA | ... | ... | — | Standard digital signatures |
| Ed25519 | ... | ... | — | Fast, modern signatures |
| bcrypt | ... | ... | — | Hash passwords |
| Argon2 | golang.org/x/crypto/argon2 | — | — | Advanced password hashing |
| TLS | ... | — | — | Secure transport layers |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 31:</strong> This chapter dissects cryptographic primitives in Go: hashing (SHA-256), symmetric encryption (AES-GCM), asymmetric encryption (ECDSA/Ed25519), HMACs, digital signatures, and password hashing (bcrypt/Argon2). Rely exclusively on the standard <abbr title="A collection of precompiled routines that a program can use.">library</abbr> `crypto/` package for cryptographic operations and rigorously avoid MD5/SHA-1 for anything security-related.
{{% /alert %}}

## See Also

- [Chapter 30 — Parallel and Distributed Algorithms](/docs/Part-VII/Chapter-30/)
- [Chapter 32 — Blockchain Data Structures and Algorithms](/docs/Part-VII/Chapter-32/)
- [Chapter 47 — Bloom Filters](/docs/Part-IX/Chapter-47/)

