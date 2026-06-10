# ============================================================
# EXPERIMENT 1 - CAESAR CIPHER
# ============================================================

def caesar_encrypt(plaintext, k):
    result = ""
    for ch in plaintext.upper():
        if ch.isalpha():
            result += chr((ord(ch) - ord('A') + k) % 26 + ord('A'))
        else:
            result += ch
    return result

def caesar_decrypt(ciphertext, k):
    return caesar_encrypt(ciphertext, 26 - k)

plaintext = input("Enter plaintext: ")
k = int(input("Enter key (1-25): "))

encrypted = caesar_encrypt(plaintext, k)
decrypted = caesar_decrypt(encrypted, k)

print(f"\nPlaintext  : {plaintext.upper()}")
print(f"Key (k)    : {k}")
print(f"Encrypted  : {encrypted}")
print(f"Decrypted  : {decrypted}")
