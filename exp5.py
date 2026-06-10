# ============================================================
# EXPERIMENT 5 - AFFINE CAESAR CIPHER
# ============================================================

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
        print(f"Invalid key: gcd({a}, 26) = {gcd(a,26)} != 1. 'a' must be coprime with 26.")
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
    if a_inv is None:
        print("No modular inverse exists for a. Decryption impossible.")
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

# Theory answers
print("=" * 55)
print("THEORY")
print("=" * 55)

print("\n(a) Limitations on b:")
print("    b can be any value from 0 to 25.")
print("    It acts as a simple shift and does not affect")
print("    the one-to-one property of the cipher.")

not_allowed = [a for a in range(26) if gcd(a, 26) != 1]
allowed     = [a for a in range(26) if gcd(a, 26) == 1]
print(f"\n(b) Values of 'a' NOT allowed: {not_allowed}")
print(f"    Values of 'a' allowed     : {allowed}")
print("    'a' must be coprime with 26 (gcd(a,26)=1)")

print("\n" + "=" * 55)
print("ENCRYPTION / DECRYPTION")
print("=" * 55)

plaintext = input("\nEnter plaintext: ")
a = int(input("Enter key 'a' (must be coprime with 26): "))
b = int(input("Enter key 'b' (0-25): "))

encrypted = affine_encrypt(plaintext, a, b)
if encrypted:
    decrypted = affine_decrypt(encrypted, a, b)
    print(f"\nPlaintext  : {plaintext.upper()}")
    print(f"Keys (a,b) : ({a}, {b})")
    print(f"Encrypted  : {encrypted}")
    print(f"Decrypted  : {decrypted}")
