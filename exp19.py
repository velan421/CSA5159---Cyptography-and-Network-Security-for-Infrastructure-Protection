# ============================================================
# EXPERIMENT 19 - 3DES IN CBC MODE
# ============================================================

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import os

def generate_3des_key():
    while True:
        key = os.urandom(24)
        try:
            DES3.adjust_key_parity(key)
            return key
        except ValueError:
            continue

def cbc_3des_encrypt(plaintext, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded = pad(plaintext.encode(), DES3.block_size)
    return cipher.encrypt(padded)

def cbc_3des_decrypt(ciphertext, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, DES3.block_size).decode()

print("=" * 60)
print("3DES IN CBC MODE")
print("=" * 60)

print("\n--- KEY INFORMATION ---")
key = generate_3des_key()
iv  = os.urandom(8)
print(f"3DES Key (hex) : {key.hex()}")
print(f"IV (hex)       : {iv.hex()}")
print(f"Key length     : {len(key)*8} bits (3x56 effective = 112 bits)")
print(f"Block size     : {DES3.block_size * 8} bits")

plaintext = input("\nEnter plaintext to encrypt: ").strip()
if not plaintext:
    plaintext = "Hello 3DES CBC Mode!"
    print(f"Using default: {plaintext}")

print("\n--- ENCRYPTION ---")
ciphertext = cbc_3des_encrypt(plaintext, key, iv)
print(f"Ciphertext (hex): {ciphertext.hex()}")

print("\n--- DECRYPTION ---")
decrypted = cbc_3des_decrypt(ciphertext, key, iv)
print(f"Decrypted: {decrypted}")

print("\n" + "=" * 60)
print("SECURITY vs PERFORMANCE ANALYSIS")
print("=" * 60)
print("""
(a) For SECURITY — Choose 3DES-CBC:
    - 3DES applies DES three times: E(K1) -> D(K2) -> E(K3)
    - Effective key length: 112 bits (meet-in-the-middle reduces 168 to 112)
    - CBC mode chains blocks: each block depends on previous ciphertext
    - Provides strong diffusion and confusion
    - IV prevents identical plaintexts producing identical ciphertexts
    - Resists brute-force and differential cryptanalysis well

(b) For PERFORMANCE — 3DES is slower than AES but acceptable:
    - 3DES runs 3x DES operations per block
    - Block size: 64 bits (less efficient than AES 128-bit blocks)
    - Modern systems prefer AES-CBC for performance
    - However, 3DES-CBC is hardware-accelerated on many platforms
    - If only 3DES is available: acceptable performance for most use cases
    
    Recommendation: Use AES-256-CBC for new systems (faster + more secure).
    Use 3DES-CBC only for legacy compatibility.
""")
