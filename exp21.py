# ============================================================
# EXPERIMENT 21 - ECB, CBC, CFB MODES: PADDING EXPLANATION
# ============================================================

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import os

BLOCK_SIZE = 8  # bytes (64 bits)

def generate_key():
    while True:
        key = os.urandom(24)
        try:
            DES3.adjust_key_parity(key)
            return key
        except ValueError:
            continue

def add_iso_padding(data, block_size):
    """ISO/IEC 7816-4 padding: append 0x80 then zeros to fill block."""
    padded = bytearray(data)
    padded.append(0x80)
    while len(padded) % block_size != 0:
        padded.append(0x00)
    return bytes(padded)

def remove_iso_padding(data):
    data = bytearray(data)
    idx = len(data) - 1
    while idx >= 0 and data[idx] == 0x00:
        idx -= 1
    if data[idx] == 0x80:
        return bytes(data[:idx])
    raise ValueError("Invalid padding")

def ecb_encrypt(plaintext_bytes, key):
    padded = pad(plaintext_bytes, BLOCK_SIZE)
    cipher = DES3.new(key, DES3.MODE_ECB)
    return cipher.encrypt(padded)

def ecb_decrypt(ciphertext_bytes, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext_bytes), BLOCK_SIZE)

def cbc_encrypt(plaintext_bytes, key, iv):
    padded = pad(plaintext_bytes, BLOCK_SIZE)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return cipher.encrypt(padded)

def cbc_decrypt(ciphertext_bytes, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext_bytes), BLOCK_SIZE)

def cfb_encrypt(plaintext_bytes, key, iv):
    cipher = DES3.new(key, DES3.MODE_CFB, iv, segment_size=64)
    return cipher.encrypt(plaintext_bytes)

def cfb_decrypt(ciphertext_bytes, key, iv):
    cipher = DES3.new(key, DES3.MODE_CFB, iv, segment_size=64)
    return cipher.decrypt(ciphertext_bytes)

key = generate_key()
iv  = os.urandom(BLOCK_SIZE)

plaintext = input("Enter plaintext: ").strip()
pt_bytes  = plaintext.encode()

print(f"\nKey (hex)     : {key.hex()}")
print(f"IV  (hex)     : {iv.hex()}")
print(f"Plaintext     : {plaintext}")
print(f"Plaintext len : {len(pt_bytes)} bytes")
print(f"Block size    : {BLOCK_SIZE} bytes")
print(f"Needs padding : {'Yes' if len(pt_bytes) % BLOCK_SIZE != 0 else 'No (but added anyway)'}")

print("\n--- ECB MODE ---")
ecb_ct = ecb_encrypt(pt_bytes, key)
ecb_dt = ecb_decrypt(ecb_ct, key)
print(f"Encrypted : {ecb_ct.hex()}")
print(f"Decrypted : {ecb_dt.decode()}")

print("\n--- CBC MODE ---")
cbc_ct = cbc_encrypt(pt_bytes, key, iv)
cbc_dt = cbc_decrypt(cbc_ct, key, iv)
print(f"Encrypted : {cbc_ct.hex()}")
print(f"Decrypted : {cbc_dt.decode()}")

print("\n--- CFB MODE ---")
# CFB works on full blocks only (pad to block boundary)
cfb_pt = pad(pt_bytes, BLOCK_SIZE)
cfb_ct = cfb_encrypt(cfb_pt, key, iv)
cfb_dt = cfb_decrypt(cfb_ct, key, iv)
print(f"Encrypted : {cfb_ct.hex()}")
print(f"Decrypted : {unpad(cfb_dt, BLOCK_SIZE).decode()}")

print("""
=== WHY PAD EVEN WHEN NOT NEEDED? ===

Motivation for always adding a padding block:

1. AMBIGUITY REMOVAL:
   Without always padding, the receiver cannot tell whether the last block
   is genuine data or padding. If the last byte is 0x08 (PKCS#7), is it
   data or padding? Always padding removes this ambiguity.

2. UNPADDING SAFETY:
   If a message's final block is already full and no extra block is added,
   the unpadding algorithm might incorrectly strip legitimate data bytes.
   Adding a full dummy padding block guarantees safe removal.

3. ORACLE ATTACK PREVENTION:
   Consistent padding prevents padding oracle attacks where the attacker
   learns information based on whether padding was valid or not.

4. DETERMINISM:
   Always padding ensures a consistent, predictable output length, which
   simplifies protocol design and interoperability.
""")
