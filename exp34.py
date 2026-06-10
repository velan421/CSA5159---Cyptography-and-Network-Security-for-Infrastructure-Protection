# ============================================================
# EXPERIMENT 34 - ECB, CBC, CFB: PADDING (Same topic as Exp 21)
# ============================================================
# Note: Experiment 34 covers the same topic as Experiment 21.
# This file provides a standalone demonstration with a focus
# on the ISO 7816-4 padding scheme specifically.

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
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

def iso_pad(data, block_size):
    """ISO 7816-4: append 1-bit (0x80) then zero bytes."""
    padded = bytearray(data) + b'\x80'
    while len(padded) % block_size != 0:
        padded += b'\x00'
    return bytes(padded)

def iso_unpad(data):
    data = bytearray(data)
    i = len(data) - 1
    while i >= 0 and data[i] == 0x00:
        i -= 1
    if data[i] == 0x80:
        return bytes(data[:i])
    raise ValueError("Invalid ISO padding")

key = generate_key()
iv  = os.urandom(BLOCK_SIZE)

print("=" * 60)
print("PADDING IN ECB, CBC, CFB MODES (ISO 7816-4)")
print("=" * 60)

for test in ["HELLO", "HELLO!!!", "HELLO WO"]:  # 5 bytes, 8 bytes (full), 8 bytes (full)
    pt = test.encode()
    padded = iso_pad(pt, BLOCK_SIZE)
    print(f"\nPlaintext  : {test!r:12} ({len(pt)} bytes)")
    print(f"Padded     : {padded.hex()} ({len(padded)} bytes)")
    unpadded = iso_unpad(padded)
    print(f"Unpadded   : {unpadded.decode()!r}")

print("""
WHY ALWAYS PAD EVEN WHEN NOT NEEDED?

1. CONSISTENT UNPADDING:
   If messages are sometimes padded and sometimes not,
   the receiver doesn't know whether the last byte is data or padding.
   Always adding a full extra padding block removes this ambiguity.

2. BOUNDARY SAFETY:
   A full block of 0x80 0x00... is unambiguously padding.
   No data byte pattern can be mistaken for it.

3. SECURITY:
   Always-padding prevents padding oracle attacks by removing
   special-case handling at message boundaries.

4. INTEROPERABILITY:
   Standards like PKCS#7 and ISO 7816-4 mandate always padding,
   making implementations predictable and compatible.
""")
