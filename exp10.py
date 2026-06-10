# ============================================================
# EXPERIMENT 10 - PLAYFAIR CIPHER WITH GIVEN MATRIX
# ============================================================
# Given matrix:
# M F H I/J K
# U N O P Q
# Z V W X Y
# E L A R G
# D S T B C

import string

FIXED_MATRIX = [
    ['M', 'F', 'H', 'I', 'K'],
    ['U', 'N', 'O', 'P', 'Q'],
    ['Z', 'V', 'W', 'X', 'Y'],
    ['E', 'L', 'A', 'R', 'G'],
    ['D', 'S', 'T', 'B', 'C']
]

def find_pos(matrix, ch):
    ch = 'I' if ch == 'J' else ch
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c

def prepare_plaintext(text):
    text = text.upper().replace('J', 'I')
    text = ''.join(filter(str.isalpha, text))
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i+1]
            if a == b:
                result += a + 'X'
                i += 1
            else:
                result += a + b
                i += 2
        else:
            result += a + 'X'
            i += 1
    return result

def playfair_encrypt(plaintext, matrix):
    text = prepare_plaintext(plaintext)
    ciphertext = ""
    print(f"\n{'Pair':<6} {'Rule':<20} {'Cipher Pair'}")
    print("-" * 40)
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)
        if r1 == r2:
            ca = matrix[r1][(c1+1)%5]
            cb = matrix[r2][(c2+1)%5]
            rule = "Same Row"
        elif c1 == c2:
            ca = matrix[(r1+1)%5][c1]
            cb = matrix[(r2+1)%5][c2]
            rule = "Same Col"
        else:
            ca = matrix[r1][c2]
            cb = matrix[r2][c1]
            rule = "Rectangle"
        print(f"  {a+b:<6} {rule:<20} {ca+cb}")
        ciphertext += ca + cb
    return ciphertext

def playfair_decrypt(ciphertext, matrix):
    text = ''.join(filter(str.isalpha, ciphertext.upper()))
    plaintext = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)
        if r1 == r2:
            plaintext += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            plaintext += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            plaintext += matrix[r1][c2] + matrix[r2][c1]
    return plaintext

print("Given Playfair Matrix:")
for row in FIXED_MATRIX:
    print("  " + " ".join(row))

message = "Must see you over Cadogan West. Coming at once."
print(f"\nOriginal Message : {message}")
print(f"Prepared Pairs   : {prepare_plaintext(message)}")

print("\nEncryption Steps:")
encrypted = playfair_encrypt(message, FIXED_MATRIX)
decrypted = playfair_decrypt(encrypted, FIXED_MATRIX)

print(f"\nPlaintext  : {message.upper()}")
print(f"Encrypted  : {encrypted}")
print(f"Decrypted  : {decrypted}")

custom = input("\nEnter your own message to encrypt (or press Enter to skip): ").strip()
if custom:
    enc = playfair_encrypt(custom, FIXED_MATRIX)
    print(f"Encrypted: {enc}")
