# ============================================================
# EXPERIMENT 11 - PLAYFAIR CIPHER KEY SPACE ANALYSIS
# ============================================================

import math

print("=" * 60)
print("PLAYFAIR KEY SPACE ANALYSIS")
print("=" * 60)

# Total arrangements of 25 letters in a 5x5 grid
total_keys = math.factorial(25)
print(f"\nTotal arrangements of 25 letters in 5x5 grid:")
print(f"  25! = {total_keys}")

log2_total = math.log2(total_keys)
print(f"  ≈ 2^{log2_total:.2f}")
print(f"  ≈ 2^58 (approximate power of 2)")

print("\n" + "-" * 60)
print("(a) Effectively Unique Keys")
print("-" * 60)

# Rotations: 5 rows * 5 columns = 25 equivalent rotations
# Reflections: the matrix can be reflected in multiple ways
# Cyclic row permutations: 5, cyclic column permutations: 5
# Together that's 5*5 = 25 equivalent rotations (cyclic shifts)

# More precisely:
# - The 5x5 grid has cyclic row shifts (5) × cyclic col shifts (5) = 25 equivalent representations
# Unique keys = 25! / 25 = 24!

unique_keys = math.factorial(25) // 25
log2_unique = math.log2(unique_keys)

print(f"\nDividing by 25 (cyclic row × col symmetries):")
print(f"  Unique keys = 25! / 25 = 24! = {unique_keys}")
print(f"  ≈ 2^{log2_unique:.2f}")
print(f"  ≈ 2^53 (approximate power of 2)")

print("\n" + "-" * 60)
print("Summary")
print("-" * 60)
print(f"  Total keys (ignoring equivalence) : 25! ≈ 2^58")
print(f"  Unique effective keys             : 24! ≈ 2^53")
print(f"\nNote: Even 2^53 ≈ 9 quadrillion keys — brute force is infeasible.")
