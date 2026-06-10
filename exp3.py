# ============================================================
# EXPERIMENT 3 - PLAYFAIR CIPHER
# ============================================================

import string

def build_matrix(keyword):
    keyword = keyword.upper().replace('J', 'I')
    seen = []
    for ch in keyword:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    for ch in string.ascii_uppercase.replace('J', ''):
        if ch not in seen:
            seen.append(ch)
    matrix = [seen[i*5:(i+1)*5] for i in range(5)]
    return matrix

def find_position(matrix, ch):
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
            b = text[i + 1]
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

def playfair_encrypt(plaintext, keyword):
    matrix = build_matrix(keyword)
    text = prepare_plaintext(plaintext)
    ciphertext = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            ciphertext += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            ciphertext += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            ciphertext += matrix[r1][c2] + matrix[r2][c1]
    return ciphertext

def playfair_decrypt(ciphertext, keyword):
    matrix = build_matrix(keyword)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            plaintext += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            plaintext += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            plaintext += matrix[r1][c2] + matrix[r2][c1]
    return plaintext

def print_matrix(matrix):
    print("\n5x5 Playfair Matrix:")
    for row in matrix:
        print(" ".join(row))

keyword  = input("Enter keyword: ")
plaintext = input("Enter plaintext: ")

matrix = build_matrix(keyword)
print_matrix(matrix)

encrypted = playfair_encrypt(plaintext, keyword)
decrypted = playfair_decrypt(encrypted, keyword)

print(f"\nPlaintext  : {plaintext.upper()}")
print(f"Prepared   : {prepare_plaintext(plaintext)}")
print(f"Encrypted  : {encrypted}")
print(f"Decrypted  : {decrypted}")
