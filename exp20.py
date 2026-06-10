# ============================================================
# EXPERIMENT 20 - CBC MODE ERROR PROPAGATION
# ============================================================

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import os

BLOCK_SIZE = 8  # DES/3DES block size in bytes

def generate_key_iv():
    while True:
        key = os.urandom(24)
        try:
            DES3.adjust_key_parity(key)
            iv = os.urandom(BLOCK_SIZE)
            return key, iv
        except ValueError:
            continue

def cbc_encrypt_blocks(plaintext_bytes, key, iv):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded = pad(plaintext_bytes, BLOCK_SIZE)
    ct = cipher.encrypt(padded)
    blocks = [ct[i:i+BLOCK_SIZE] for i in range(0, len(ct), BLOCK_SIZE)]
    return blocks

def cbc_decrypt_blocks(cipher_blocks, key, iv):
    ct = b''.join(cipher_blocks)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    return [pt[i:i+BLOCK_SIZE] for i in range(0, len(pt), BLOCK_SIZE)]

def introduce_bit_error(block_bytes, bit_position=0):
    """Flip one bit in a block."""
    block = bytearray(block_bytes)
    byte_pos = bit_position // 8
    bit_pos  = 7 - (bit_position % 8)
    block[byte_pos] ^= (1 << bit_pos)
    return bytes(block)

def compare_blocks(original, corrupted, label):
    print(f"\n  {label}:")
    for i, (o, c) in enumerate(zip(original, corrupted)):
        match = "OK" if o == c else "CORRUPTED"
        print(f"    Block {i+1}: {o.hex()} | {c.hex()}  [{match}]")

key, iv = generate_key_iv()

plaintext = b"BLOCKONE" + b"BLOCKTWO" + b"BLOKTHRE" + b"BLOCKFOU"
print("=" * 60)
print("CBC MODE ERROR PROPAGATION")
print("=" * 60)
print(f"\nKey (hex): {key.hex()}")
print(f"IV  (hex): {iv.hex()}")
print(f"\nOriginal Plaintext Blocks:")
for i in range(0, len(plaintext), BLOCK_SIZE):
    print(f"  P{i//BLOCK_SIZE+1}: {plaintext[i:i+BLOCK_SIZE]}")

# Normal encryption
cipher_blocks = cbc_encrypt_blocks(plaintext, key, iv)
print(f"\nNormal Ciphertext Blocks:")
for i, b in enumerate(cipher_blocks):
    print(f"  C{i+1}: {b.hex()}")

# ---- Part (a): Error in transmitted C1 ----
print("\n" + "=" * 60)
print("(a) BIT ERROR IN TRANSMITTED C1")
print("=" * 60)
corrupted_c1 = list(cipher_blocks)
corrupted_c1[0] = introduce_bit_error(cipher_blocks[0], bit_position=3)

normal_dec   = cbc_decrypt_blocks(cipher_blocks,   key, iv)
corrupted_dec= cbc_decrypt_blocks(corrupted_c1,    key, iv)

print("\nCBC Decryption with error in C1:")
print("  In CBC: Pi = D(Ci) XOR C(i-1)")
print("  Error in C1 affects: P1 (direct) and P2 (via XOR with C1)")
print("  P3, P4... are NOT affected because they XOR with C2, C3... (undamaged)")
compare_blocks(normal_dec, corrupted_dec, "Decrypted blocks")

affected = sum(1 for o, c in zip(normal_dec, corrupted_dec) if o != c)
print(f"\n  Blocks affected: {affected} (P1 and P2 only)")
print("  Blocks beyond P2: NOT affected ✓")

# ---- Part (b): Bit error in source P1 ----
print("\n" + "=" * 60)
print("(b) BIT ERROR IN SOURCE P1 (before encryption)")
print("=" * 60)
corrupted_plain = bytearray(plaintext)
corrupted_plain[3] ^= 0x01   # flip one bit in P1
corrupted_plain = bytes(corrupted_plain)

normal_ct   = cbc_encrypt_blocks(plaintext,        key, iv)
corrupted_ct= cbc_encrypt_blocks(corrupted_plain,  key, iv)

print("\nEffect of P1 bit error on ciphertext blocks:")
print("  In CBC: Ci = E(Pi XOR C(i-1))")
print("  A change in P1 changes C1.")
print("  C1 is used in computing C2, so C2 also changes.")
print("  C2 affects C3, and so on... ALL subsequent ciphertext blocks change.")

print(f"\n  {'Block':<8} {'Normal CT':<20} {'Corrupted CT':<20} {'Match'}")
print("  " + "-" * 55)
for i, (n, c) in enumerate(zip(normal_ct, corrupted_ct)):
    match = "SAME" if n == c else "DIFFERENT"
    print(f"  C{i+1:<7} {n.hex():<20} {c.hex():<20} {match}")

print("""
  Conclusion for Part (b):
  - A bit error in P1 propagates through ALL ciphertext blocks (C1, C2, C3...).
  - At the RECEIVER: ALL plaintext blocks will be affected upon decryption.
  - This is because CBC chaining means each Ci depends on ALL previous blocks.
  - This is why data integrity checks (MAC/HMAC) are used alongside CBC.
""")
