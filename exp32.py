# ============================================================
# EXPERIMENT 32 - DSA vs RSA: SIGNATURE UNIQUENESS
# ============================================================

import random
import hashlib
import math

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("No inverse")
    return x % m

# ── Small DSA ──
def dsa_sign(msg, p, q, g, x):
    """Sign message with DSA. k is random per signature."""
    h = int(hashlib.sha256(msg.encode()).hexdigest(), 16) % q
    while True:
        k = random.randint(1, q - 1)
        r = pow(g, k, p) % q
        if r == 0:
            continue
        k_inv = mod_inverse(k, q)
        s = (k_inv * (h + x * r)) % q
        if s != 0:
            return r, s, k    # returning k only for educational display

def dsa_verify(msg, r, s, p, q, g, y):
    h    = int(hashlib.sha256(msg.encode()).hexdigest(), 16) % q
    w    = mod_inverse(s, q)
    u1   = (h * w) % q
    u2   = (r * w) % q
    v    = (pow(g, u1, p) * pow(y, u2, p)) % p % q
    return v == r

# ── Small RSA ──
def rsa_sign(msg, d, n):
    h = int(hashlib.sha256(msg.encode()).hexdigest(), 16) % n
    return pow(h, d, n)

def rsa_verify(msg, sig, e, n):
    h        = int(hashlib.sha256(msg.encode()).hexdigest(), 16) % n
    h_verify = pow(sig, e, n)
    return h == h_verify

print("=" * 60)
print("DSA vs RSA: SIGNATURE UNIQUENESS")
print("=" * 60)

# DSA small parameters (educational only — not secure)
p = 23117   # prime
q = 89      # prime divisor of p-1
g = pow(2, (p-1)//q, p)  # generator
x = 37      # private key
y = pow(g, x, p)         # public key

print(f"\nDSA Parameters: p={p}, q={q}, g={g}")
print(f"Private key x={x}, Public key y={y}")

message = input("\nEnter message to sign: ").strip() or "hello"

print(f"\n--- DSA: Sign '{message}' TWICE ---")
sig1 = dsa_sign(message, p, q, g, x)
sig2 = dsa_sign(message, p, q, g, x)
print(f"  Signature 1: (r={sig1[0]}, s={sig1[1]})  [k={sig1[2]}]")
print(f"  Signature 2: (r={sig2[0]}, s={sig2[1]})  [k={sig2[2]}]")
print(f"  Same signature? {sig1[:2] == sig2[:2]}")
v1 = dsa_verify(message, sig1[0], sig1[1], p, q, g, y)
v2 = dsa_verify(message, sig2[0], sig2[1], p, q, g, y)
print(f"  Both valid?   {v1} and {v2}")

# RSA small
rsa_p, rsa_q = 61, 53
rsa_n = rsa_p * rsa_q
rsa_phi = (rsa_p-1)*(rsa_q-1)
rsa_e = 17
rsa_d = mod_inverse(rsa_e, rsa_phi)

print(f"\n--- RSA: Sign '{message}' TWICE ---")
rsa_sig1 = rsa_sign(message, rsa_d, rsa_n)
rsa_sig2 = rsa_sign(message, rsa_d, rsa_n)
print(f"  Signature 1: {rsa_sig1}")
print(f"  Signature 2: {rsa_sig2}")
print(f"  Same signature? {rsa_sig1 == rsa_sig2}")
rv1 = rsa_verify(message, rsa_sig1, rsa_e, rsa_n)
rv2 = rsa_verify(message, rsa_sig2, rsa_e, rsa_n)
print(f"  Both valid? {rv1} and {rv2}")

print("""
=== IMPLICATIONS ===

DSA (Non-deterministic):
  ✓ Each signature is UNIQUE (different random k each time).
  ✓ Privacy: observers cannot link two signatures to the same signer
    (beyond the public key).
  ✗ DANGER: If k is ever REUSED for two different messages,
    the private key x can be RECOVERED:
    x = (s1*k - H(m1)) * r1⁻¹ mod q
    This happened in Sony PS3 (same k used for all firmware) — key leaked!
  ✗ Requires secure random k per signature.

RSA (Deterministic):
  ✓ Same message + same key = same signature (verifiable, reproducible).
  ✗ No per-signature randomness — same input always gives same output.
  ✓ Simpler: no need to manage random k.
  ✓ No risk of k-reuse attack.

Practical note: Modern deterministic DSA (RFC 6979) derives k from
the message and key using HMAC — avoiding the k-reuse risk while
keeping signatures unique per message-key pair.
""")
