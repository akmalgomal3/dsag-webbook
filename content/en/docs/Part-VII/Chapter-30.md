---
weight: 70300
title: "Chapter 30: Cryptographic Foundations Algorithms"
description: "Cryptographic Foundations Algorithms"
icon: "article"
date: "2026-05-12T00:00:00+07:00"
lastmod: "2026-05-12T00:00:00+07:00"
draft: false
toc: true
katex: true
---

{{% alert icon="💡" context="info" %}}
<strong>"<em>To keep a system secure, we need to be always on our toes. If we wait for the attackers to find vulnerabilities, it's already too late.</em>" — Whitfield Diffie</strong>
{{% /alert %}}

{{% alert icon="📘" context="success" %}}
Chapter 30 explores cryptographic primitives. Covers hash functions, symmetric encryption, asymmetric encryption, and digital signatures. Uses Go standard library.
{{% /alert %}}

## 30.1. Hash Functions

**Definition:** Hash function maps arbitrary input to fixed-size output. Cryptographic hashes must resist preimages and collisions.

**Background & Philosophy:**
Cryptography uses one-way functions. Trivial to compute forward. Computationally impossible to reverse without key. Relies on mathematical asymmetry.

**Use Cases:**
HTTPS encryption. Password security via bcrypt. Blockchain transaction verification.

**Memory Mechanics:**
Hash computation itself is deterministic and CPU-bound. Timing-sensitive paths usually arise during secret comparisons. Naive comparison exits early on mismatch and leaks byte position. `subtle.ConstantTimeCompare` forces full slice iteration and neutralizes this side-channel.

### Operations & Complexity

| Algorithm | Output Size | Security Level | Description |
|-----------|-------------|----------|------------|
| SHA-256 | 256 bits | Secure | Industry standard |
| SHA-512 | 512 bits | Secure | Slower: larger bounds |
| MD5 | 128 bits | Broken | Unsafe |
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
Use `crypto/sha256` or `crypto/sha512`. MD5 and SHA-1 are broken. Use `bcrypt` or `argon2` for passwords.
{{% /alert %}}

### Decision Matrix

| Use SHA-256 When... | Avoid If... |
|------------------------|------------------|
| Data integrity checks required | Storing passwords: use bcrypt/argon2 |
| Cryptographic checksums needed | Raw speed is priority: use xxhash |

### Edge Cases & Pitfalls

- **Length extension:** SHA-256 is vulnerable. Use HMACs for protection.
- **Timing attacks:** Avoid `==` for hash comparison. Use `hmac.Equal` or `subtle.ConstantTimeCompare`.

## 30.2. Symmetric Encryption

**Definition:** Symmetric encryption uses same key for encryption and decryption. AES-GCM is the standard mode.

### Operations & Complexity

| Algorithm | Key Size | Mode | Security Level |
|-----------|----------|------|----------|
| AES-128 | 128 bits | GCM | Secure |
| AES-256 | 256 bits | GCM | Secure |
| ChaCha20-Poly1305 | 256 bits | AEAD | Secure alternative |

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
    if length(ciphertext) < nonceSize: return error "ciphertext too short"
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
    if len(ciphertext) < nonceSize {
        return nil, fmt.Errorf("ciphertext too short")
    }
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
Nonce must be unique per encryption. Standard GCM nonce is 12 bytes. Nonce reuse breaks security.
{{% /alert %}}

### Decision Matrix

| Use AES-GCM When... | Avoid If... |
|------------------------|------------------|
| Encrypting data at rest/transit | Authentication missing: use AEAD mode |
| Hardware AES-NI available | Embedded systems lack AES: use ChaCha20 |

### Edge Cases & Pitfalls

- **Nonce reuse:** Fatal flaw for GCM. Use cryptographically random nonces.
- **Unauthenticated encryption:** ECB and CBC (without HMAC) allow tampering.
- **IV reuse:** Destroys security in CTR mode.

## 30.3. Asymmetric Encryption

**Definition:** Asymmetric encryption uses public/private key pairs. RSA and ECDSA are standards.

### Operations & Complexity

| Algorithm | Key Size | Sign | Verify | Description |
|-----------|----------|------|--------|------------|
| RSA-2048 | 2048 bits | <code>O(n^3)</code>$ | <code>O(n^2)</code>$ | Aging standard |
| RSA-4096 | 4096 bits | <code>O(n^3)</code>$ | <code>O(n^2)</code>$ | Secure: slow |
| ECDSA P-256 | 256 bits | <code>O(n^2)</code>$ | <code>O(n^2)</code>$ | Fast: short |
| Ed25519 | 256 bits | <code>O(n^2)</code>$ | <code>O(n^2)</code>$ | Modern: recommended |

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
    signature = DER encode (r, s)
    return signature, hash
```

### Idiomatic Go Implementation

```go
package main

import (
    "encoding/asn1"
    "crypto/ecdsa"
    "crypto/elliptic"
    "crypto/rand"
    "crypto/sha256"
    "crypto/x509"
    "encoding/pem"
    "fmt"
    "math/big"
)

type ecdsaSignature struct {
    R, S *big.Int
}

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
    sig, err := asn1.Marshal(ecdsaSignature{R: r, S: s})
    if err != nil {
        return nil, nil, err
    }
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
    var parsed ecdsaSignature
    if _, err := asn1.Unmarshal(sig, &parsed); err != nil {
        panic(err)
    }
    valid := ecdsa.Verify(&priv.PublicKey, hash, parsed.R, parsed.S)
    fmt.Println("Signature valid:", valid)
}
```

{{% alert icon="📌" context="warning" %}}
`crypto/ecdsa` uses raw (r, s) signatures. Modern apps should prefer `crypto/ed25519`.
{{% /alert %}}

### Decision Matrix

| Use Ed25519 When... | Avoid If... |
|------------------------|------------------|
| New digital signatures needed | Legacy systems require RSA |
| Performance is critical | Raw encryption required: Ed25519 only signs |

### Edge Cases & Pitfalls

- **Randomness quality:** Keys depend on `crypto/rand`. Avoid `math/rand`.
- **Timing attacks:** Verification must be constant-time. Go stdlib handles this.

## 30.4. Digital Signatures and HMAC

**Definition:** HMAC uses secret key to authenticate data. Digital signatures use asymmetric keys for non-repudiation.

### Operations & Complexity

| Primitive | Key Type | Size | Description |
|----------|----------|------|------------|
| HMAC-SHA256 | Symmetric | 256 bits | Message authentication |
| ECDSA | Asymmetric | 512 bits signature | Non-repudiation |
| Ed25519 | Asymmetric | 64 bytes signature | Modern: fast |

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
Use `hmac.Equal` for constant-time comparison. Avoid `==` for MACs.
{{% /alert %}}

### Decision Matrix

| Use HMAC When... | Use Digital Signature When... |
|---------------------|----------------------------------|
| Shared secret key exists | Non-repudiation is mandatory |
| Performance is critical | Third-party verification required |

### Edge Cases & Pitfalls

- **Short keys:** HMAC hashes keys shorter than block size automatically.
- **Truncated MAC:** Avoid truncation without security analysis.

## 30.5. Password Hashing

**Definition:** Slow one-way function. Designed to thwart brute-force attacks.

### Operations & Complexity

| Algorithm | Work Factor | Memory | Description |
|-----------|-------------|--------|------------|
| bcrypt | Cost 10-14 | Low | Legacy standard |
| scrypt | N, r, p | Configurable | Memory-hard |
| Argon2 | Time, Memory | High | Modern: recommended |

### Idiomatic Go Implementation

```go
package main

import (
	"fmt"
	"golang.org/x/crypto/bcrypt"
)

func main() {
	password := []byte("my-secure-password")
	hashed, _ := bcrypt.GenerateFromPassword(password, 12)
	fmt.Printf("bcrypt hash: %s\n", hashed)
	err := bcrypt.CompareHashAndPassword(hashed, password)
	if err == nil {
		fmt.Println("Verified")
	}
}
```

{{% alert icon="📌" context="warning" %}}
Avoid SHA-256 for passwords. Use bcrypt, scrypt, or Argon2. These are slow and memory-hard.
{{% /alert %}}

Prefer `golang.org/x/crypto/argon2` for production.

### Anti-Patterns

- **Broken algorithms:** MD5/SHA-1 have collisions. Use SHA-256 for integrity. Use bcrypt/Argon2 for passwords.
- **Nonce reuse:** Destroys GCM security. Generate fresh 12-byte nonce per encryption.
- **Timing leaks:** `==` allows side-channel attacks. Use `hmac.Equal` or `subtle.ConstantTimeCompare`.

## Quick Reference

| Name | Go Type | Time | Space | Use Case |
|------|---------|------|-------|----------|
| SHA-256 | `crypto/sha256` | <code>O(n)</code>$ | 32 bytes | Data integrity |
| AES-GCM | `crypto/aes` | <code>O(n)</code>$ | . | Symmetric encryption |
| HMAC | `crypto/hmac` | <code>O(n)</code>$ | . | Message authentication |
| ECDSA | `crypto/ecdsa` | <code>O(n)</code>$ | . | Digital signatures |
| Ed25519 | `crypto/ed25519` | <code>O(n)</code>$ | . | Modern signatures |
| bcrypt | `bcrypt` | <code>O(cost)</code>$ | . | Password hashing |
| Argon2 | `argon2` | . | . | Advanced password hashing |
| TLS | `crypto/tls` | . | . | Secure transport |

{{% alert icon="🎯" context="success" %}}
<strong>Summary Chapter 30:</strong> Use SHA-256 for integrity. AES-GCM for symmetric encryption. ECDSA/Ed25519 for signatures. bcrypt/Argon2 for passwords. Rely on `crypto/` package. Avoid MD5/SHA-1.
{{% /alert %}}

## See Also

- [Chapter 29: Parallel and Distributed Algorithms](/docs/part-vii/chapter-29/)
- [Chapter 31: Blockchain Data Structures and Algorithms](/docs/part-vii/chapter-31/)
- [Chapter 46: Bloom Filters](/docs/part-ix/chapter-46/)
