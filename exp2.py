# ============================================================
# EXPERIMENT 2 - MONOALPHABETIC SUBSTITUTION CIPHER
# ============================================================

import random
import string

def generate_key():
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def mono_encrypt(plaintext, key):
    result = ""
    for ch in plaintext.upper():
        if ch.isalpha():
            result += key[ch]
        else:
            result += ch
    return result

def mono_decrypt(ciphertext, key):
    rev_key = {v: k for k, v in key.items()}
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += rev_key[ch]
        else:
            result += ch
    return result

plaintext = input("Enter plaintext: ")

key = generate_key()
print("\nGenerated Key Mapping:")
print("Plain :", " ".join(key.keys()))
print("Cipher:", " ".join(key.values()))

encrypted = mono_encrypt(plaintext, key)
decrypted = mono_decrypt(encrypted, key)

print(f"\nPlaintext  : {plaintext.upper()}")
print(f"Encrypted  : {encrypted}")
print(f"Decrypted  : {decrypted}")
