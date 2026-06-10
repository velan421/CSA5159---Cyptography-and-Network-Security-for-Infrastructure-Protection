# ============================================================
# EXPERIMENT 38 - HILL CIPHER: KNOWN PLAINTEXT ATTACK
# ============================================================

import numpy as np

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def mod_matrix_inverse(matrix, mod):
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        return None
    adj = np.array([[matrix[1,1], -matrix[0,1]],
                    [-matrix[1,0], matrix[0,0]]])
    return ((det_inv * adj) % mod).astype(int)

def text_to_nums(text):
    return [ord(c) - ord('A') for c in ''.join(filter(str.isalpha, text.upper()))]

def nums_to_text(nums):
    return ''.join(chr(int(n) % 26 + ord('A')) for n in nums)

def hill_encrypt(plaintext, key):
    nums = text_to_nums(plaintext)
    while len(nums) % 2:
        nums.append(23)  # pad with X
    result = []
    for i in range(0, len(nums), 2):
        v   = np.array([[nums[i]], [nums[i+1]]])
        out = np.dot(key, v) % 26
        result.extend(out.flatten().astype(int))
    return nums_to_text(result)

def known_plaintext_attack(pt_pairs):
    (p1, c1), (p2, c2) = pt_pairs
    P = np.array([[p1[0], p2[0]], [p1[1], p2[1]]])
    C = np.array([[c1[0], c2[0]], [c1[1], c2[1]]])
    print(f"\n  P matrix:\n{P}")
    print(f"  C matrix:\n{C}")
    P_inv = mod_matrix_inverse(P, 26)
    if P_inv is None:
        return None
    print(f"  P⁻¹ mod 26:\n{P_inv}")
    K = (np.dot(C, P_inv) % 26).astype(int)
    return K

def chosen_plaintext_attack(key):
    """Use identity-based chosen plaintext."""
    cp1 = [1, 0]
    cp2 = [0, 1]
    cc1 = list((np.dot(key, np.array([[1],[0]])) % 26).flatten().astype(int))
    cc2 = list((np.dot(key, np.array([[0],[1]])) % 26).flatten().astype(int))
    print(f"\n  Chosen P1={cp1} → C1={cc1}")
    print(f"  Chosen P2={cp2} → C2={cc2}")
    K_recovered = (np.array([cc1, cc2]).T % 26).astype(int)
    return K_recovered

print("=" * 60)
print("HILL CIPHER — KNOWN PLAINTEXT ATTACK")
print("=" * 60)

# Setup with hidden key
TRUE_KEY = np.array([[9, 4], [5, 7]])
print(f"\n(Hidden) True Key:\n{TRUE_KEY}")

# Generate known pairs from a chosen message
sample = "HELPME"
nums   = text_to_nums(sample)
pairs  = []
for i in range(0, min(len(nums), 4), 2):
    p = nums[i:i+2]
    c = list((np.dot(TRUE_KEY, np.array(p).reshape(2,1)) % 26).flatten().astype(int))
    pairs.append((p, c))
    print(f"Known pair: P={p} ({nums_to_text(p)})  C={c} ({nums_to_text(c)})")

print("\n--- KNOWN PLAINTEXT ATTACK ---")
recovered = known_plaintext_attack(pairs)
if recovered is not None:
    print(f"\n  Recovered Key:\n{recovered}")
    print(f"  Matches True Key: {np.array_equal(recovered, TRUE_KEY)}")

print("\n--- CHOSEN PLAINTEXT ATTACK ---")
cp_recovered = chosen_plaintext_attack(TRUE_KEY)
print(f"\n  Recovered Key:\n{cp_recovered}")
print(f"  Matches True Key: {np.array_equal(cp_recovered, TRUE_KEY)}")

print("""
=== ANALYSIS ===
Known Plaintext  : Need at least 2 linearly independent plaintext pairs.
                   Solve K = C × P⁻¹ (mod 26).
Chosen Plaintext : Even easier — choose P = Identity matrix.
                   Then K = C directly (columns of K are the ciphertexts).
Defense          : Use a larger block size (3×3 or 4×4) to require more pairs.
                   In practice, Hill cipher is still vulnerable regardless.
""")
