# ============================================================
# EXPERIMENT 18 - DES SUBKEY BIT SOURCE ANALYSIS
# ============================================================

PC1 = [57,49,41,33,25,17, 9,
        1,58,50,42,34,26,18,
       10, 2,59,51,43,35,27,
       19,11, 3,60,52,44,36,
       63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
       14, 6,61,53,45,37,29,
       21,13, 5,28,20,12, 4]

PC2 = [14,17,11,24, 1, 5,
        3,28,15, 6,21,10,
       23,19,12, 4,26, 8,
       16, 7,27,20,13, 2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

SHIFT_SCHEDULE = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

# After PC-1:
# Positions 1-28  -> C half (from first subset of key bits)
# Positions 29-56 -> D half (from second subset of key bits)

c_source_bits = set(PC1[:28])   # key bit positions feeding into C
d_source_bits = set(PC1[28:])   # key bit positions feeding into D

print("=" * 60)
print("DES SUBKEY BIT SOURCE ANALYSIS")
print("=" * 60)

print(f"\nPC-1 C half (positions 1-28 of permuted key):")
print(f"  Original key bit positions: {sorted(c_source_bits)}")

print(f"\nPC-1 D half (positions 29-56 of permuted key):")
print(f"  Original key bit positions: {sorted(d_source_bits)}")

print(f"\nAre C and D source sets disjoint? {c_source_bits.isdisjoint(d_source_bits)}")

# PC-2 analysis: first 24 bits come from C half (positions 1-28 of CD)
# second 24 bits come from D half (positions 29-56 of CD)
pc2_first_24  = PC2[:24]
pc2_second_24 = PC2[24:]

first_from_c  = all(p <= 28 for p in pc2_first_24)
second_from_d = all(p > 28  for p in pc2_second_24)

print("\n--- PC-2 Analysis ---")
print(f"First 24 bits of each subkey  (PC-2 positions 1-24) : {pc2_first_24}")
print(f"  All from C half (<=28)?  : {first_from_c}")

print(f"\nSecond 24 bits of each subkey (PC-2 positions 25-48): {pc2_second_24}")
print(f"  All from D half (>28)?   : {second_from_d}")

print("\n--- Subkey Bit Tracing ---")
print(f"{'Round':<8} {'First 24 bits from':<25} {'Second 24 bits from'}")
print("-" * 55)
for r in range(16):
    print(f"  K{r+1:>2}    C half (key bits {sorted(c_source_bits)[:3]}...)   "
          f"D half (key bits {sorted(d_source_bits)[:3]}...)")

print("\nConclusion:")
print("  - First 24 bits of ALL subkeys come from the C half (28-bit subset of key)")
print("  - Second 24 bits of ALL subkeys come from the D half (disjoint 28-bit subset)")
print("  - This is a fixed structural property of DES key scheduling.")
