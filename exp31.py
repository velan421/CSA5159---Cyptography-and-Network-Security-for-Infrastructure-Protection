# ============================================================
# EXPERIMENT 31 - CMAC SUBKEY GENERATION
# ============================================================

def left_shift_1(bits):
    """Left shift a bit array by 1."""
    return bits[1:] + [0]

def xor_bits(a, b):
    return [x ^ y for x, y in zip(a, b)]

def int_to_bits(n, length):
    return [(n >> (length - 1 - i)) & 1 for i in range(length)]

def bits_to_hex(bits):
    val = 0
    for b in bits:
        val = (val << 1) | b
    return format(val, f'0{len(bits)//4}X')

def generate_cmac_subkeys(L_bits, block_size):
    """
    Generate K1 and K2 from L = E_K(0^b).
    Constants Rb: 64-bit -> 0x1B, 128-bit -> 0x87
    """
    if block_size == 64:
        Rb_val = 0x1B
    elif block_size == 128:
        Rb_val = 0x87
    else:
        raise ValueError("Only 64 or 128-bit blocks supported")

    Rb = int_to_bits(Rb_val, block_size)

    print(f"\nL (block cipher output for all-zero input): {bits_to_hex(L_bits)}")
    print(f"Rb constant for {block_size}-bit block: {bits_to_hex(Rb)}")

    # Generate K1
    msb_L = L_bits[0]
    K1 = left_shift_1(L_bits)
    if msb_L == 1:
        K1 = xor_bits(K1, Rb)
        print(f"\nMSB of L = 1 → K1 = (L << 1) XOR Rb")
    else:
        print(f"\nMSB of L = 0 → K1 = (L << 1)")
    print(f"K1 = {bits_to_hex(K1)}")

    # Generate K2
    msb_K1 = K1[0]
    K2 = left_shift_1(K1)
    if msb_K1 == 1:
        K2 = xor_bits(K2, Rb)
        print(f"\nMSB of K1 = 1 → K2 = (K1 << 1) XOR Rb")
    else:
        print(f"\nMSB of K1 = 0 → K2 = (K1 << 1)")
    print(f"K2 = {bits_to_hex(K2)}")

    return K1, K2

print("=" * 60)
print("CMAC SUBKEY GENERATION")
print("=" * 60)

print("""
=== CONSTANTS FOR EACH BLOCK SIZE ===

(a) Block size = 64 bits:
    Irreducible polynomial: x^64 + x^4 + x^3 + x + 1
    Rb = 0x1B (binary: 0...011011)

    Block size = 128 bits:
    Irreducible polynomial: x^128 + x^7 + x^2 + x + 1
    Rb = 0x87 (binary: 0...10000111)

(b) How left shift + XOR works:
    - Treat the 64/128-bit string as an element in GF(2^b).
    - Left shift by 1 = multiply by x in GF(2^b).
    - If MSB=1, the result overflows degree b-1, so we XOR with Rb
      (the irreducible polynomial constant) to reduce back into the field.
    - This ensures K1 and K2 stay as b-bit values with algebraic properties
      that guarantee security of CMAC.
""")

print("--- DEMO: 64-bit block ---")
# Use a sample L value for 64-bit
L_64 = int_to_bits(0x2B7E151628AED2A6 & 0xFFFFFFFFFFFFFFFF, 64)
K1_64, K2_64 = generate_cmac_subkeys(L_64, 64)

print("\n--- DEMO: 128-bit block ---")
L_128 = int_to_bits(0x2B7E151628AED2A6ABF7158809CF4F3C, 128)
K1_128, K2_128 = generate_cmac_subkeys(L_128, 128)

print("""
USAGE IN CMAC:
  - For a message whose last block is COMPLETE: XOR last block with K1 before encrypting.
  - For a message whose last block is INCOMPLETE: pad it, then XOR with K2 before encrypting.
  This prevents length-extension attacks that affect basic CBC-MAC.
""")
