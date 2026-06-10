# ============================================================
# EXPERIMENT 4 - VIGENERE CIPHER (Polyalphabetic Substitution)
# ============================================================

def vigenere_encrypt(plaintext, key):
    key = key.upper()
    result = ""
    j = 0
    for ch in plaintext.upper():
        if ch.isalpha():
            shift = ord(key[j % len(key)]) - ord('A')
            result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            j += 1
        else:
            result += ch
    return result

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    result = ""
    j = 0
    for ch in ciphertext.upper():
        if ch.isalpha():
            shift = ord(key[j % len(key)]) - ord('A')
            result += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
            j += 1
        else:
            result += ch
    return result

def show_vigenere_table(plaintext, key):
    key = key.upper()
    plaintext = plaintext.upper()
    print(f"\n{'Plaintext':<12} {'Key':<6} {'Shift':<8} {'Ciphertext'}")
    print("-" * 40)
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            k = key[j % len(key)]
            shift = ord(k) - ord('A')
            c = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            print(f"  {ch:<12} {k:<6} {shift:<8} {c}")
            j += 1

plaintext = input("Enter plaintext: ")
key       = input("Enter key: ")

show_vigenere_table(plaintext, key)

encrypted = vigenere_encrypt(plaintext, key)
decrypted = vigenere_decrypt(encrypted, key)

print(f"\nPlaintext  : {plaintext.upper()}")
print(f"Key        : {key.upper()}")
print(f"Encrypted  : {encrypted}")
print(f"Decrypted  : {decrypted}")
