# ============================================================
# EXPERIMENT 24 - RSA: FINDING PRIVATE KEY
# ============================================================

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("No modular inverse — gcd != 1")
    return x % phi

def find_factors(n):
    """Trial division to find p and q."""
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i, n // i
    return None, None

def rsa_encrypt(msg, e, n):
    return pow(msg, e, n)

def rsa_decrypt(cipher, d, n):
    return pow(cipher, d, n)

print("=" * 60)
print("RSA: FINDING PRIVATE KEY")
print("=" * 60)

e_default = 31
n_default = 3599

e_in = input(f"Enter public key e (default {e_default}): ").strip()
n_in = input(f"Enter modulus n   (default {n_default}): ").strip()

e = int(e_in) if e_in.isdigit() else e_default
n = int(n_in) if n_in.isdigit() else n_default

print(f"\nPublic key : e = {e}")
print(f"Modulus    : n = {n}")

# Step 1: Factor n
print("\nStep 1: Factoring n by trial division...")
p, q = find_factors(n)
if p is None:
    print("Could not factor n.")
else:
    print(f"  Found: p = {p}, q = {q}")
    print(f"  Verify: p × q = {p * q} {'✓' if p * q == n else '✗'}")

    # Step 2: Compute phi(n)
    phi_n = (p - 1) * (q - 1)
    print(f"\nStep 2: φ(n) = (p-1)(q-1) = ({p-1})({q-1}) = {phi_n}")

    # Step 3: Extended Euclidean to find d
    print(f"\nStep 3: Find d = e⁻¹ mod φ(n) using Extended Euclidean Algorithm")
    g, x, y = extended_gcd(e, phi_n)
    print(f"  gcd({e}, {phi_n}) = {g}")
    d = mod_inverse(e, phi_n)
    print(f"  Private key d = {d}")
    print(f"  Verify: (e × d) mod φ(n) = ({e} × {d}) mod {phi_n} = {(e * d) % phi_n} {'✓' if (e * d) % phi_n == 1 else '✗'}")

    print(f"\nPublic Key  : (e={e}, n={n})")
    print(f"Private Key : (d={d}, n={n})")

    # Demo encrypt/decrypt
    print("\n--- Demo Encryption / Decryption ---")
    msg_in = input("Enter a number to encrypt (must be < n): ").strip()
    msg    = int(msg_in) if msg_in.isdigit() else 42
    if msg >= n:
        print(f"Message must be < {n}. Using 42.")
        msg = 42

    cipher  = rsa_encrypt(msg, e, n)
    plain   = rsa_decrypt(cipher, d, n)
    print(f"  Original  : {msg}")
    print(f"  Encrypted : {cipher}")
    print(f"  Decrypted : {plain}")
    print(f"  Match     : {plain == msg}")
