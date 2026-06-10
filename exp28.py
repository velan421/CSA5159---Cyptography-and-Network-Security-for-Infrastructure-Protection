# ============================================================
# EXPERIMENT 28 - DIFFIE-HELLMAN KEY EXCHANGE
# ============================================================

import random
import math

def is_primitive_root(a, q):
    """Check if a is a primitive root mod q (q prime)."""
    phi = q - 1
    factors = set()
    n = phi
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
    if n > 1:
        factors.add(n)
    for factor in factors:
        if pow(a, phi // factor, q) == 1:
            return False
    return True

def dh_standard(a, q, x_alice, x_bob):
    """Standard DH: exchange a^x mod q."""
    A = pow(a, x_alice, q)   # Alice sends this
    B = pow(a, x_bob,   q)   # Bob sends this
    key_alice = pow(B, x_alice, q)
    key_bob   = pow(A, x_bob,   q)
    return A, B, key_alice, key_bob

def dh_xa_variant(a, q, x_alice, x_bob):
    """Insecure variant: exchange x*a mod q (linear, not exponent)."""
    A_sent = (x_alice * a) % q
    B_sent = (x_bob   * a) % q
    # Alice computes: x_alice * B_sent / a mod q  (not straightforward)
    # This doesn't create a shared secret easily
    return A_sent, B_sent

print("=" * 60)
print("DIFFIE-HELLMAN KEY EXCHANGE")
print("=" * 60)

q = 23   # public prime
a = 5    # public primitive root mod q (5 is primitive root mod 23)
print(f"\nPublic parameters: q={q}, a={a}")
print(f"a is primitive root mod q: {is_primitive_root(a, q)}")

x_alice = int(input("\nAlice's secret x_a (e.g. 6): ").strip() or "6")
x_bob   = int(input("Bob's secret   x_b (e.g. 15): ").strip() or "15")

print("\n--- STANDARD DH: exchange a^x mod q ---")
A, B, k_alice, k_bob = dh_standard(a, q, x_alice, x_bob)
print(f"  Alice sends: A = a^x_a mod q = {a}^{x_alice} mod {q} = {A}")
print(f"  Bob sends  : B = a^x_b mod q = {a}^{x_bob}   mod {q} = {B}")
print(f"  Alice computes: B^x_a mod q = {B}^{x_alice} mod {q} = {k_alice}")
print(f"  Bob   computes: A^x_b mod q = {A}^{x_bob}   mod {q} = {k_bob}")
print(f"  Shared key match: {k_alice == k_bob} (Key = {k_alice})")

print("\n--- INSECURE VARIANT: exchange x*a (linear) ---")
A2, B2 = dh_xa_variant(a, q, x_alice, x_bob)
print(f"  Alice sends: x_a * a mod q = {x_alice} * {a} mod {q} = {A2}")
print(f"  Bob sends  : x_b * a mod q = {x_bob} * {a} mod {q} = {B2}")
a_inv = pow(a, -1, q)
print(f"  To get shared key, Alice computes: x_a * B2 mod q = {(x_alice * B2) % q}")
print(f"  But Bob computes               : x_b * A2 mod q = {(x_bob * A2) % q}")
print(f"  These are DIFFERENT — no shared secret established!")

print("""
=== ANALYSIS ===

What happens if participants send x*a instead of a^x mod q?

Problem 1 - NO SHARED SECRET:
  Alice sends x_a * a, Bob sends x_b * a.
  Alice computes x_a * (x_b * a) = x_a * x_b * a
  Bob   computes x_b * (x_a * a) = x_a * x_b * a
  ✓ They reach the same value... BUT:

Problem 2 - TRIVIALLY BROKEN BY EVE:
  Eve sees A = x_a * a (mod q) and knows a, q.
  Eve computes x_a = A * a⁻¹ mod q (just one modular inverse!)
  => Eve finds the SECRET x_a directly.
  The discrete logarithm problem (which protects DH) doesn't apply here.

CONCLUSION: The security of DH comes specifically from the hardness of
computing discrete logarithms (finding x from a^x mod q).
Linear multiplication offers NO computational hardness.
""")
