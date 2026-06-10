# ============================================================
# EXPERIMENT 17 - DES KEY GENERATION (ENCRYPTION & DECRYPTION)
# ============================================================

# Permutation Choice 1 (PC-1): selects 56 bits from 64-bit key
PC1 = [57,49,41,33,25,17, 9,
        1,58,50,42,34,26,18,
       10, 2,59,51,43,35,27,
       19,11, 3,60,52,44,36,
       63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
       14, 6,61,53,45,37,29,
       21,13, 5,28,20,12, 4]

# Permutation Choice 2 (PC-2): selects 48 bits from 56-bit combined halves
PC2 = [14,17,11,24, 1, 5,
        3,28,15, 6,21,10,
       23,19,12, 4,26, 8,
       16, 7,27,20,13, 2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

# Number of left shifts for each of the 16 rounds (encryption)
SHIFT_SCHEDULE = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def permute(block, table):
    return [block[i-1] for i in table]

def left_shift(half, n):
    return half[n:] + half[:n]

def generate_subkeys(key_64bit):
    """Generate 16 subkeys from 64-bit key."""
    key_56 = permute(key_64bit, PC1)
    C = key_56[:28]
    D = key_56[28:]
    subkeys = []
    for i, shift in enumerate(SHIFT_SCHEDULE):
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        CD = C + D
        Ki = permute(CD, PC2)
        subkeys.append(Ki)
        print(f"  K{i+1:>2}: {''.join(map(str, Ki[:24]))}  {''.join(map(str, Ki[24:]))}")
    return subkeys

def bits_to_hex(bits):
    val = 0
    for b in bits:
        val = (val << 1) | b
    return format(val, f'0{len(bits)//4}X')

# Example 64-bit key (as list of bits)
key_hex = input("Enter 64-bit key in hex (16 hex chars, e.g. 133457799BBCDFF1): ").strip()
if not key_hex:
    key_hex = "133457799BBCDFF1"
    print(f"Using default key: {key_hex}")

key_int   = int(key_hex, 16)
key_64bit = [(key_int >> (63 - i)) & 1 for i in range(64)]

print(f"\nKey (hex)  : {key_hex}")
print(f"Key (bits) : {''.join(map(str, key_64bit))}")

print("\n--- ENCRYPTION SUBKEYS (K1 to K16) ---")
subkeys = generate_subkeys(key_64bit)
subkeys_hex = [bits_to_hex(k) for k in subkeys]

print("\n--- DECRYPTION SUBKEYS (K16 to K1, reversed) ---")
print("For decryption, use subkeys in reverse order:")
for i, k in enumerate(reversed(subkeys_hex)):
    print(f"  Round {i+1:>2} uses K{16-i:>2} = {k}")

print(f"\nShift schedule (encryption): {SHIFT_SCHEDULE}")
print(f"Shift schedule (decryption): {list(reversed(SHIFT_SCHEDULE))}")
print("\nNote: Decryption simply applies the same subkeys in reverse order (K16..K1).")
