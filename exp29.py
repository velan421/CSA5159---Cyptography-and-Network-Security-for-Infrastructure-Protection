# ============================================================
# EXPERIMENT 29 - SHA-3: NONZERO BIT PROPAGATION IN CAPACITY LANES
# ============================================================

# SHA-3 (Keccak) parameters for 1024-bit block size (SHA3-256 variant with r=1024)
# State: 5x5 matrix of 64-bit lanes = 1600 bits total
# Rate (r) = 1024 bits = 16 lanes
# Capacity (c) = 576 bits = 9 lanes
# Lane size = 64 bits

LANE_SIZE_BITS = 64
STATE_LANES    = 25     # 5x5
RATE_BITS      = 1024
CAPACITY_BITS  = 576
RATE_LANES     = RATE_BITS    // LANE_SIZE_BITS   # 16
CAPACITY_LANES = CAPACITY_BITS // LANE_SIZE_BITS  # 9

print("=" * 60)
print("SHA-3: NONZERO BIT PROPAGATION IN CAPACITY LANES")
print("=" * 60)

print(f"\nSHA-3 Parameters (block size = {RATE_BITS} bits):")
print(f"  State size    : {STATE_LANES * LANE_SIZE_BITS} bits ({STATE_LANES} lanes of {LANE_SIZE_BITS} bits)")
print(f"  Rate (r)      : {RATE_BITS} bits = {RATE_LANES} lanes  (absorb portion)")
print(f"  Capacity (c)  : {CAPACITY_BITS} bits = {CAPACITY_LANES} lanes  (zero initially)")

print(f"\nInitial State:")
print(f"  Rate lanes (0–{RATE_LANES-1})         : all initialized from message (may be nonzero)")
print(f"  Capacity lanes ({RATE_LANES}–{STATE_LANES-1})  : all ZERO initially")

print(f"\nAssumption: Each of the {RATE_LANES} rate lanes in P0 has at least one nonzero bit.")

print("""
Analysis (ignoring permutation):

In the Keccak absorb step, the state S is XOR'd with the padded message block P0:
    S[i] = S[i] XOR P0[i]   for i in 0..RATE_LANES-1

Since all initial state bits are 0:
    S[i] = 0 XOR P0[i] = P0[i]   for rate lanes

The CAPACITY lanes (indices 16–24) are NOT touched by the XOR absorption.
They only change through the PERMUTATION (θ, ρ, π, χ, ι steps).

Without the permutation:
  - After absorbing the first block, capacity lanes remain ALL ZEROS.
  - No message bits ever directly touch the capacity lanes.
  - Capacity lanes stay zero FOREVER without the permutation.

With the permutation (real SHA-3):
  - After 1 round of Keccak-f[1600], the θ step mixes all columns.
  - The θ step XORs each lane with the parities of neighboring columns.
  - Nonzero rate lanes propagate nonzero bits into capacity lanes.
  - After just 1 permutation round, ALL capacity lanes typically become nonzero.
""")

print("Simulation (tracking which rounds make capacity lanes nonzero):")

# Simplified model: track which capacity lanes become nonzero
# In each round, nonzero rate lanes propagate to capacity via theta
nonzero_capacity = set()
total_capacity   = set(range(RATE_LANES, STATE_LANES))

print(f"\n  Capacity lanes to fill: {sorted(total_capacity)}")
print(f"\n  Round 0 (after absorb, before permute): capacity lanes = all zero")

for rnd in range(1, 6):
    # θ step: each lane gets XOR of neighbors across all rows
    # Simplified: after 1 round, all capacity lanes receive nonzero contribution
    # because rate lanes have nonzero bits and θ propagates across columns
    new_nonzero = set()
    for lane in total_capacity:
        col = lane % 5
        # θ connects this lane to columns of rate lanes
        if any((rate_lane % 5) == col or (rate_lane % 5) == (col-1) % 5
               for rate_lane in range(RATE_LANES)):
            new_nonzero.add(lane)

    nonzero_capacity |= new_nonzero
    print(f"  After round {rnd}: {len(nonzero_capacity)}/{CAPACITY_LANES} "
          f"capacity lanes nonzero — {sorted(nonzero_capacity)}")
    if nonzero_capacity == total_capacity:
        print(f"\n  All capacity lanes nonzero after round {rnd}!")
        break

print(f"""
Conclusion:
  Ignoring the permutation: capacity lanes NEVER become nonzero.
  With 1 permutation round : all {CAPACITY_LANES} capacity lanes become nonzero
                            due to the θ (theta) diffusion step.
  This is fundamental to SHA-3's security — the permutation mixes rate
  and capacity portions thoroughly.
""")
