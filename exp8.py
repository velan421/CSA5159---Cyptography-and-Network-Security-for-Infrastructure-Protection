# ============================================================
# EXPERIMENT 8 - MONOALPHABETIC CIPHER WITH KEYWORD
# ============================================================

import string

def generate_cipher_alphabet(keyword):
    keyword = keyword.upper()
    seen = []
    for ch in keyword:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    for ch in string.ascii_uppercase:
        if ch not in seen:
            seen.append(ch)
    return seen

def build_mapping(keyword):
    cipher_alpha = generate_cipher_alphabet(keyword)
    plain_to_cipher = dict(zip(string.ascii_uppercase, cipher_alpha))
    cipher_to_plain = {v: k for k, v in plain_to_cipher.items()}
    return plain_to_cipher, cipher_to_plain

def encrypt(plaintext, plain_to_cipher):
    result = ""
    for ch in plaintext.upper():
        if ch.isalpha():
            result += plain_to_cipher[ch]
        else:
            result += ch
    return result

def decrypt(ciphertext, cipher_to_plain):
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += cipher_to_plain[ch]
        else:
            result += ch
    return result

keyword   = input("Enter keyword (e.g. CIPHER): ").strip()
plaintext = input("Enter plaintext: ").strip()

plain_to_cipher, cipher_to_plain = build_mapping(keyword)
cipher_alpha = generate_cipher_alphabet(keyword)

print("\nPlain  : " + " ".join(string.ascii_uppercase))
print("Cipher : " + " ".join(cipher_alpha))

encrypted = encrypt(plaintext, plain_to_cipher)
decrypted = decrypt(encrypted, cipher_to_plain)

print(f"\nPlaintext  : {plaintext.upper()}")
print(f"Encrypted  : {encrypted}")
print(f"Decrypted  : {decrypted}")
