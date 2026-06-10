# ============================================================
# EXPERIMENT 26 - RSA: IS IT SAFE TO REUSE MODULUS AFTER KEY LEAK?
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

def factor_from_d(e, d, n):
    """
    Given e, d, n — recover p and q.
    Uses the fact that e*d - 1 = k*phi(n).
    """
    k = e * d - 1
    for _ in range(100):
        g = random.randint(2, n - 1)
        t = k
        while t % 2 == 0:
            t //= 2
            x = pow(g, t, n)
            if x > 1 and math.gcd(x - 1, n) > 1:
                p = math.gcd(x - 1, n)
                q = n // p
                if p * q == n and p != 1 and q != 1:
                    return p, q
    return None, None

primes = [p for p in range(50, 200) if is_prime(p)]
p = random.choice(primes)
q = random.choice([x for x in primes if x != p])
n = p * q
phi = (p - 1) * (q - 1)
e1 = 7
while math.gcd(e1, phi) != 1:
    e1 += 2
d1 = mod_inverse(e1, phi)

print("=" * 60)
print("RSA: REUSING MODULUS AFTER PRIVATE KEY LEAK")
print("=" * 60)
print(f"\nOriginal RSA Setup:")
print(f"  p={p}, q={q}, n={n}")
print(f"  e1={e1} (public key), d1={d1} (private key — LEAKED)")

# Bob generates new keypair but KEEPS n
e2 = e1 + 2
while math.gcd(e2, phi) != 1 or e2 == e1:
    e2 += 2
d2 = mod_inverse(e2, phi)

print(f"\nBob keeps same n={n}, generates new keys:")
print(f"  New e2={e2}, new d2={d2}")

print("\n--- ATTACK: Using leaked d1 to recover p and q ---")
recovered_p, recovered_q = factor_from_d(e1, d1, n)

if recovered_p:
    print(f"  Recovered p = {recovered_p}, q = {recovered_q}")
    phi_recovered = (recovered_p - 1) * (recovered_q - 1)
    d2_recovered  = mod_inverse(e2, phi_recovered)
    print(f"  Computed φ(n) = {phi_recovered}")
    print(f"  Recovered NEW d2 = {d2_recovered}")
    print(f"  Matches actual d2: {d2_recovered == d2}")
    print("\n  ATTACK SUCCESSFUL! New private key broken too.")
else:
    print("  Factoring attempt failed (try again — randomized algorithm)")

print("""
=== IS IT SAFE? NO! ===

When Bob leaks d1 but keeps the same modulus n:

1. Eve uses the known relationship: e1 * d1 ≡ 1 (mod φ(n))
   => e1 * d1 - 1 = k * φ(n) for some integer k.

2. Using a probabilistic algorithm (Miller-Rabin style), Eve factors n
   into p and q using only (e1, d1, n).

3. Once p and q are known, φ(n) = (p-1)(q-1) is trivial to compute.

4. Any NEW private key d2 = e2⁻¹ mod φ(n) is immediately computable.

CONCLUSION: Reusing the modulus n after a key leak is COMPLETELY UNSAFE.
Bob MUST generate a new modulus (new p and q) entirely.
""")
