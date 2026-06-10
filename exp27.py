# ============================================================
# EXPERIMENT 27 - RSA: ENCRYPTING CHARACTERS SEPARATELY (INSECURE)
# ============================================================

import math

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)
    return x % phi

def rsa_encrypt_char(p_val, e, n):
    return pow(p_val, e, n)

def rsa_decrypt_char(c_val, d, n):
    return pow(c_val, d, n)

# Small RSA for demo
p, q = 61, 53
n    = p * q          # 3233
phi  = (p-1)*(q-1)    # 3120
e    = 17
d    = mod_inverse(e, phi)

print("=" * 60)
print("RSA: CHARACTER-BY-CHARACTER ENCRYPTION — IS IT SECURE?")
print("=" * 60)
print(f"\nRSA params: p={p}, q={q}, n={n}, e={e}, d={d}")

message = input("\nEnter a message (letters only): ").strip().upper()
message = ''.join(filter(str.isalpha, message))

print(f"\nEncrypting '{message}' letter by letter (A=0, B=1, ...Z=25):")
print(f"\n{'Char':<6} {'Value':<8} {'Ciphertext'}")
print("-" * 30)

ciphertext_vals = []
for ch in message:
    val = ord(ch) - ord('A')
    ct  = rsa_encrypt_char(val, e, n)
    ciphertext_vals.append(ct)
    print(f"  {ch:<6} {val:<8} {ct}")

print(f"\nCiphertext values: {ciphertext_vals}")

# Attack: build codebook (only 26 possible plaintexts!)
print("\n--- CODEBOOK ATTACK ---")
print("Since plaintext is always A-Z (only 26 values),")
print("attacker pre-computes all 26 encryptions:")
codebook = {}
for i in range(26):
    ct = rsa_encrypt_char(i, e, n)
    codebook[ct] = chr(i + ord('A'))
    print(f"  {chr(i+ord('A'))}({i}) -> {ct}")

print("\nAttacker decodes ciphertext using codebook:")
decoded = ''.join(codebook.get(ct, '?') for ct in ciphertext_vals)
print(f"  Decoded: {decoded}")
print(f"  Match  : {decoded == message}")

# Actual decryption with private key
print("\n--- LEGITIMATE DECRYPTION (with private key) ---")
decrypted = ''.join(chr(rsa_decrypt_char(ct, d, n) + ord('A')) for ct in ciphertext_vals)
print(f"  Decrypted: {decrypted}")

print("""
=== IS THIS METHOD SECURE? NO! ===

Problem: Only 26 possible plaintext values (A–Z mapped to 0–25).

Attack: The attacker builds a CODEBOOK by encrypting all 26 values
        using the PUBLIC key (which is public!). This costs only 26
        modular exponentiations — trivially fast.

Then: Any ciphertext is broken in O(1) time by lookup.

This is a known-plaintext / exhaustive-plaintext attack.
RSA is DETERMINISTIC — same input always gives same output.
So the codebook works perfectly.

Solution: Encrypt the ENTIRE message as one block, or use
          OAEP padding which introduces randomness per encryption.
""")
