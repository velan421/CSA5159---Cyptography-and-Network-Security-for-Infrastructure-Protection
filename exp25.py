# ============================================================
# EXPERIMENT 25 - RSA: COMMON FACTOR ATTACK
# ============================================================

import math
import random

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("No inverse")
    return x % phi

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def generate_small_rsa():
    primes = [p for p in range(10, 100) if is_prime(p)]
    p = random.choice(primes)
    q = random.choice([x for x in primes if x != p])
    n = p * q
    phi = (p-1)*(q-1)
    e = 3
    while math.gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)
    return p, q, n, e, d

print("=" * 60)
print("RSA: COMMON FACTOR ATTACK")
print("=" * 60)

# Setup: two users sharing a common prime factor
print("\nScenario: Attacker knows one plaintext block shares a factor with n")

p, q, n, e, d = generate_small_rsa()

print(f"\nRSA Setup:")
print(f"  p = {p}, q = {q}")
print(f"  n = p × q = {n}")
print(f"  e = {e}, d = {d}")

# A plaintext that shares factor p with n
msg = p * 2   # shares factor p
if msg >= n:
    msg = p

cipher = pow(msg, e, n)
print(f"\n  Plaintext block M = {msg}")
print(f"  (M shares factor {p} with n)")
print(f"  Ciphertext C = M^e mod n = {cipher}")

# Attack: compute gcd(M, n)
print("\n--- ATTACK ---")
common = math.gcd(msg, n)
print(f"  gcd(M, n) = gcd({msg}, {n}) = {common}")

if common > 1 and common != n:
    recovered_p = common
    recovered_q = n // common
    print(f"  Recovered p = {recovered_p}")
    print(f"  Recovered q = {recovered_q}")
    phi_n = (recovered_p - 1) * (recovered_q - 1)
    recovered_d = mod_inverse(e, phi_n)
    print(f"  Recovered φ(n) = {phi_n}")
    print(f"  Recovered d = {recovered_d}")
    print(f"  Match original d: {recovered_d == d}")
    print(f"\n  ATTACK SUCCESSFUL! Private key fully recovered.")
else:
    print("  gcd = 1 or n — no factor found.")

print("""
=== ANALYSIS ===

Yes, knowing a plaintext block shares a common factor with n HELPS enormously:

1. Computing gcd(M, n) immediately gives us p or q.
2. Once p is known, q = n/p, and φ(n) = (p-1)(q-1) is trivial.
3. The private key d = e⁻¹ mod φ(n) is then recovered using Extended Euclidean.
4. This breaks the ENTIRE RSA system — not just one message.

This is why RSA plaintexts must be random-padded (OAEP) before encryption.
Raw RSA (textbook RSA) is vulnerable to this and other attacks.
""")
