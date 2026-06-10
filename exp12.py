# ============================================================
# EXPERIMENT 12 - HILL CIPHER
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
        raise ValueError(f"Matrix is not invertible mod {mod}")

    size = matrix.shape[0]
    if size == 2:
        adj = np.array([[matrix[1,1], -matrix[0,1]],
                        [-matrix[1,0], matrix[0,0]]])
    else:
        raise ValueError("Only 2x2 supported in this implementation")

    inv = (det_inv * adj) % mod
    return inv.astype(int)

def text_to_nums(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    return [ord(ch) - ord('A') for ch in text]

def nums_to_text(nums):
    return ''.join(chr(n % 26 + ord('A')) for n in nums)

def hill_encrypt(plaintext, key_matrix):
    nums = text_to_nums(plaintext)
    # Pad if needed
    while len(nums) % 2 != 0:
        nums.append(ord('X') - ord('A'))

    ciphertext = ""
    print(f"\n{'Block':<10} {'Vector':<15} {'Result':<15} {'Cipher'}")
    print("-" * 50)
    for i in range(0, len(nums), 2):
        vec = np.array([[nums[i]], [nums[i+1]]])
        result = np.dot(key_matrix, vec) % 26
        block_plain = nums_to_text([nums[i], nums[i+1]])
        block_cipher = nums_to_text(result.flatten().tolist())
        print(f"  {block_plain:<10} {str(vec.flatten().tolist()):<15} {str(result.flatten().tolist()):<15} {block_cipher}")
        ciphertext += block_cipher
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    inv_key = mod_matrix_inverse(key_matrix, 26)
    print(f"\nInverse Key Matrix (mod 26):\n{inv_key}")
    nums = text_to_nums(ciphertext)
    plaintext = ""
    print(f"\n{'Block':<10} {'Vector':<15} {'Result':<15} {'Plain'}")
    print("-" * 50)
    for i in range(0, len(nums), 2):
        vec = np.array([[nums[i]], [nums[i+1]]])
        result = np.dot(inv_key, vec) % 26
        block_cipher = nums_to_text([nums[i], nums[i+1]])
        block_plain  = nums_to_text(result.flatten().tolist())
        print(f"  {block_cipher:<10} {str(vec.flatten().tolist()):<15} {str(result.flatten().tolist()):<15} {block_plain}")
        plaintext += block_plain
    return plaintext

# Default key from problem
KEY = np.array([[9, 4], [5, 7]])
MESSAGE = "meet me at the usual place at ten rather than eight oclock"

print("=" * 60)
print("HILL CIPHER")
print("=" * 60)
print(f"\nKey Matrix:\n{KEY}")
print(f"\nPlaintext: {MESSAGE}")

print("\n--- ENCRYPTION ---")
encrypted = hill_encrypt(MESSAGE, KEY)
print(f"\nCiphertext: {encrypted}")

print("\n--- DECRYPTION ---")
decrypted = hill_decrypt(encrypted, KEY)
print(f"\nDecrypted : {decrypted}")

print("\n--- CUSTOM INPUT ---")
custom = input("\nEnter your own message (or press Enter to skip): ").strip()
if custom:
    enc = hill_encrypt(custom, KEY)
    print(f"Encrypted : {enc}")
    dec = hill_decrypt(enc, KEY)
    print(f"Decrypted : {dec}")
