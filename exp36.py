# ============================================================
# EXPERIMENT 36 - AFFINE CAESAR CIPHER (Extended)
# ============================================================

import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(plaintext, a, b):
    if gcd(a, 26) != 1:
        print(f"  ✗ Invalid: gcd({a}, 26) = {gcd(a,26)} ≠ 1. Not one-to-one.")
        return None
    result = ""
    for ch in plaintext.upper():
        if ch.isalpha():
            p = ord(ch) - ord('A')
            c = (a * p + b) % 26
            result += chr(c + ord('A'))
        else:
            result += ch
    return result

def affine_decrypt(ciphertext, a, b):
    a_inv = mod_inverse(a, 26)
    if not a_inv:
        return None
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            c = ord(ch) - ord('A')
            p = (a_inv * (c - b)) % 26
            result += chr(p + ord('A'))
        else:
            result += ch
    return result

def check_one_to_one(a, b):
    outputs = [(a * p + b) % 26 for p in range(26)]
    return len(set(outputs)) == 26

print("=" * 60)
print("AFFINE CAESAR CIPHER: C = (ap + b) mod 26")
print("=" * 60)

print("\n--- THEORY ---")
print("\n(a) Limitation on b:")
print("    b can be ANY integer 0–25.")
print("    It is a pure shift and does not affect the one-to-one property.")

print("\n(b) Values of 'a' that are NOT allowed:")
not_ok = [a for a in range(26) if gcd(a, 26) != 1]
ok     = [a for a in range(26) if gcd(a, 26) == 1]
print(f"    Not allowed (gcd(a,26) ≠ 1): {not_ok}")
print(f"    Allowed     (gcd(a,26) = 1): {ok}")
print(f"    Number of valid 'a' values : {len(ok)}")
print(f"    Total unique keys (a,b)    : {len(ok)} × 26 = {len(ok)*26}")

print("\n--- DEMONSTRATION: a=2, b=3 (INVALID) ---")
a, b = 2, 3
print(f"  E([{a},{b}], 0) = ({a}*0 + {b}) mod 26 = {(a*0+b)%26}")
print(f"  E([{a},{b}],13) = ({a}*13+ {b}) mod 26 = {(a*13+b)%26}")
print("  Both map to same output — NOT one-to-one!")

print("\n--- ENCRYPTION / DECRYPTION ---")
pt = input("\nEnter plaintext: ").strip()
a  = int(input("Enter a (must be coprime with 26): ").strip() or "5")
b  = int(input("Enter b (0–25): ").strip() or "8")

if gcd(a, 26) != 1:
    print(f"a={a} is invalid. gcd({a},26)={gcd(a,26)} ≠ 1")
else:
    ct = affine_encrypt(pt, a, b)
    if ct:
        dt = affine_decrypt(ct, a, b)
        print(f"\nPlaintext  : {pt.upper()}")
        print(f"Keys (a,b) : ({a}, {b})")
        print(f"Encrypted  : {ct}")
        print(f"Decrypted  : {dt}")
        print(f"One-to-one : {check_one_to_one(a,b)}")

print("\n--- ALL VALID 'a' VALUES WITH THEIR INVERSES ---")
print(f"{'a':<5} {'gcd(a,26)':<12} {'a⁻¹ mod 26'}")
print("-" * 30)
for a_val in range(1, 26):
    g = gcd(a_val, 26)
    inv = mod_inverse(a_val, 26) if g == 1 else "N/A"
    status = "✓" if g == 1 else "✗"
    print(f"  {a_val:<5} {g:<12} {str(inv):<10} {status}")
