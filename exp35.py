# ============================================================
# EXPERIMENT 35 - ONE-TIME PAD VIGENERE CIPHER (Extended)
# ============================================================

import os
import random

def otp_encrypt(plaintext, key_stream):
    text = ''.join(filter(str.isalpha, plaintext.upper()))
    if len(key_stream) < len(text):
        print("Error: Key stream must be at least as long as the plaintext.")
        return None, None
    result = ""
    print(f"\n{'Char':<6} {'p':<5} {'k':<5} {'(p+k)%26':<10} {'Cipher'}")
    print("-" * 35)
    for i, ch in enumerate(text):
        p = ord(ch) - ord('A')
        k = key_stream[i] % 26
        c = (p + k) % 26
        result += chr(c + ord('A'))
        print(f"  {ch:<6} {p:<5} {k:<5} {c:<10} {chr(c+ord('A'))}")
    return result, text

def otp_decrypt(ciphertext, key_stream):
    text = ''.join(filter(str.isalpha, ciphertext.upper()))
    result = ""
    for i, ch in enumerate(text):
        c = ord(ch) - ord('A')
        k = key_stream[i] % 26
        p = (c - k) % 26
        result += chr(p + ord('A'))
    return result

def generate_random_key(length):
    return [random.randint(0, 25) for _ in range(length)]

def find_key_for_target(ciphertext, target):
    c_clean = ''.join(filter(str.isalpha, ciphertext.upper()))
    p_clean = ''.join(filter(str.isalpha, target.upper()))
    if len(c_clean) != len(p_clean):
        print(f"Length mismatch: cipher={len(c_clean)}, target={len(p_clean)}")
        return None
    return [(ord(c) - ord(p)) % 26
            for c, p in zip(c_clean, p_clean)]

print("=" * 60)
print("ONE-TIME PAD VIGENERE CIPHER")
print("=" * 60)

print("\nOptions:")
print("  1. Encrypt with custom key stream")
print("  2. Encrypt with random key stream")
print("  3. Find key for alternate plaintext (OTP malleability demo)")

choice = input("\nChoice (1/2/3): ").strip()

if choice == "1":
    pt  = input("Enter plaintext: ").strip()
    ks_input = input("Enter key stream (space-separated numbers, e.g. 3 19 5): ").strip()
    ks = list(map(int, ks_input.split()))
    ct, clean = otp_encrypt(pt, ks)
    if ct:
        print(f"\nCiphertext: {ct}")
        dt = otp_decrypt(ct, ks)
        print(f"Decrypted : {dt}")

elif choice == "2":
    pt  = input("Enter plaintext: ").strip()
    clean = ''.join(filter(str.isalpha, pt.upper()))
    ks  = generate_random_key(len(clean))
    print(f"Random key stream: {ks}")
    ct, _ = otp_encrypt(pt, ks)
    if ct:
        print(f"\nCiphertext: {ct}")
        dt = otp_decrypt(ct, ks)
        print(f"Decrypted : {dt}")

elif choice == "3":
    pt   = input("Enter original plaintext: ").strip()
    ks_input = input("Enter key stream (space-separated): ").strip()
    ks   = list(map(int, ks_input.split()))
    ct, _ = otp_encrypt(pt, ks)
    if ct:
        print(f"\nCiphertext: {ct}")
        target = input("Enter target plaintext (same length, alpha only): ").strip()
        new_key = find_key_for_target(ct, target)
        if new_key:
            print(f"Key to decrypt to '{target}': {new_key}")
            verify = otp_decrypt(ct, new_key)
            print(f"Verification: {verify}")
            print("\nThis proves OTP has PERFECT SECRECY —")
            print("any ciphertext can decode to any plaintext with the right key!")

else:
    print("Invalid choice.")
