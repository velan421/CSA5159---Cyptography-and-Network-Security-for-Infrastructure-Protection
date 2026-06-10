# ============================================================
# EXPERIMENT 13 - HILL CIPHER: KNOWN PLAINTEXT ATTACK
# ============================================================

import numpy as np

def mod_matrix_inverse(matrix, mod):
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = None
    for x in range(mod):
        if (det * x) % mod == 1:
            det_inv = x
            break
    if det_inv is None:
        return None
    adj = np.array([[matrix[1,1], -matrix[0,1]],
                    [-matrix[1,0],  matrix[0,0]]])
    return ((det_inv * adj) % mod).astype(int)

def text_to_nums(text):
    return [ord(ch) - ord('A') for ch in ''.join(filter(str.isalpha, text.upper()))]

def nums_to_text(nums):
    return ''.join(chr(int(n) % 26 + ord('A')) for n in nums)

def hill_encrypt_block(block_nums, key):
    vec = np.array(block_nums).reshape(-1, 1)
    return (np.dot(key, vec) % 26).flatten().astype(int)

def known_plaintext_attack(plaintext_pairs):
    """
    Given plaintext-ciphertext pairs, recover the 2x2 key matrix K.
    We know: C = K * P (mod 26)
    So:      K = C * P^(-1) (mod 26)
    """
    # Use first two pairs to build P and C matrices
    p1, c1 = plaintext_pairs[0]
    p2, c2 = plaintext_pairs[1]

    P = np.array([[p1[0], p2[0]],
                  [p1[1], p2[1]]])
    C = np.array([[c1[0], c2[0]],
                  [c1[1], c2[1]]])

    print(f"\nPlaintext matrix P:\n{P}")
    print(f"\nCiphertext matrix C:\n{C}")

    P_inv = mod_matrix_inverse(P, 26)
    if P_inv is None:
        print("Plaintext matrix is not invertible mod 26. Try different pairs.")
        return None

    print(f"\nP^(-1) mod 26:\n{P_inv}")

    K = (np.dot(C, P_inv) % 26).astype(int)
    print(f"\nRecovered Key Matrix K = C * P^(-1) mod 26:\n{K}")
    return K

# ---- Demo ----
# Use a known key to generate pairs, then attack
TRUE_KEY = np.array([[9, 4], [5, 7]])
plaintext = "HELP"
nums = text_to_nums(plaintext)

pair1_p = nums[0:2]
pair1_c = hill_encrypt_block(pair1_p, TRUE_KEY).tolist()
pair2_p = nums[2:4]
pair2_c = hill_encrypt_block(pair2_p, TRUE_KEY).tolist()

print("=" * 60)
print("HILL CIPHER - KNOWN PLAINTEXT ATTACK")
print("=" * 60)
print(f"\nTrue Key (hidden from attacker):\n{TRUE_KEY}")
print(f"\nKnown plaintext : {plaintext}")
print(f"Known ciphertext: {nums_to_text(pair1_c + pair2_c)}")
print(f"\nPair 1 -> Plain: {pair1_p} ({nums_to_text(pair1_p)})  Cipher: {pair1_c} ({nums_to_text(pair1_c)})")
print(f"Pair 2 -> Plain: {pair2_p} ({nums_to_text(pair2_p)})  Cipher: {pair2_c} ({nums_to_text(pair2_c)})")

print("\nMounting Known Plaintext Attack...")
recovered = known_plaintext_attack([(pair1_p, pair1_c), (pair2_p, pair2_c)])

if recovered is not None and np.array_equal(recovered, TRUE_KEY):
    print("\nAttack SUCCESSFUL! Recovered key matches true key.")
else:
    print("\nRecovered key differs — try more pairs.")

# Chosen plaintext attack
print("\n" + "-" * 60)
print("CHOSEN PLAINTEXT ATTACK")
print("-" * 60)
print("Choose identity-like plaintext pairs for easier recovery.")
identity_p1 = [1, 0]
identity_p2 = [0, 1]
id_c1 = hill_encrypt_block(identity_p1, TRUE_KEY).tolist()
id_c2 = hill_encrypt_block(identity_p2, TRUE_KEY).tolist()
print(f"Chosen P1={identity_p1} -> C1={id_c1}")
print(f"Chosen P2={identity_p2} -> C2={id_c2}")
K_chosen = (np.array([id_c1, id_c2]).T % 26).astype(int)
print(f"\nRecovered Key from chosen plaintext:\n{K_chosen}")
