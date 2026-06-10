# ============================================================
# EXPERIMENT 30 - CBC-MAC LENGTH EXTENSION ATTACK
# ============================================================

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
import os

BLOCK_SIZE = 8

def generate_key():
    while True:
        key = os.urandom(24)
        try:
            DES3.adjust_key_parity(key)
            return key
        except ValueError:
            continue

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def cbc_mac(key, message_block):
    """Compute CBC-MAC of a single-block message."""
    iv = b'\x00' * BLOCK_SIZE
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ct = cipher.encrypt(message_block)
    return ct  # last block = MAC

def cbc_mac_two_blocks(key, block1, block2):
    """Compute CBC-MAC of a two-block message."""
    iv = b'\x00' * BLOCK_SIZE
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ct = cipher.encrypt(block1 + block2)
    return ct[BLOCK_SIZE:]   # MAC = last block

key = generate_key()

print("=" * 60)
print("CBC-MAC LENGTH EXTENSION ATTACK")
print("=" * 60)

# Choose a single-block message X
X = input(f"\nEnter 8-char message X (default 'HELLOWLD'): ").strip()
X = (X + "        ")[:BLOCK_SIZE]
X_bytes = X.encode()[:BLOCK_SIZE]

print(f"\nMessage X (1 block) : {X_bytes.hex()}")
T = cbc_mac(key, X_bytes)
print(f"CBC-MAC T = MAC(K, X): {T.hex()}")

# Attacker knows: X and T = MAC(K, X)
# Attacker creates: X || (X XOR T) — a 2-block message
X2 = xor_bytes(X_bytes, T)
print(f"\nAttacker computes X2 = X XOR T = {X2.hex()}")
print(f"Attacker's forged message: X || (X XOR T) = {X_bytes.hex()} {X2.hex()}")

# Compute MAC of forged 2-block message
forged_mac = cbc_mac_two_blocks(key, X_bytes, X2)
print(f"\nCBC-MAC of forged 2-block message: {forged_mac.hex()}")
print(f"Original T                       : {T.hex()}")
print(f"MACs match (forgery works)       : {forged_mac == T}")

print("""
=== WHY DOES THIS WORK? ===

CBC-MAC of a 1-block message X:
  T = E_K(X XOR 0) = E_K(X)

CBC-MAC of the 2-block message X || (X XOR T):
  Step 1: C1 = E_K(X XOR 0)      = E_K(X) = T
  Step 2: C2 = E_K((X XOR T) XOR C1)
             = E_K((X XOR T) XOR T)
             = E_K(X)
             = T

So MAC(K, X || (X XOR T)) = T = MAC(K, X)  ← FORGERY!

DEFENSE:
  Use CMAC (adds subkey XOR to the last block before final encryption).
  Use HMAC (keyed hash — resistant to length extension attacks).
  Use authenticated encryption (AES-GCM, ChaCha20-Poly1305).
""")
