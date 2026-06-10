# ============================================================
# EXPERIMENT 9 - PLAYFAIR CIPHER: PT-109 MESSAGE DECRYPTION
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
    return [seen[i*5:(i+1)*5] for i in range(5)]

def find_pos(matrix, ch):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c

def playfair_decrypt(ciphertext, keyword):
    matrix = build_matrix(keyword)
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

def print_matrix(matrix):
    print("\nPlayfair Matrix:")
    for row in matrix:
        print("  " + " ".join(row))

# PT-109 ciphertext
pt109_cipher = "KXJEY UREBE ZWEHE WRYTU HEYFS KREHE GOYFI WTTTU OLKSY CAJPO BOTEI ZONTX BYBNT GONEY CUZWR GDSON SXBOU YWRHE BAAHY USEDQ"

print("PT-109 Ciphertext:")
print(pt109_cipher)

keyword = input("\nEnter Playfair keyword (try 'ROYAL'): ").strip()

matrix = build_matrix(keyword)
print_matrix(matrix)

decrypted = playfair_decrypt(pt109_cipher, keyword)
print(f"\nDecrypted : {decrypted}")
print("\nNote: Remove padding X's and split words to read the message.")
print("Known answer with key 'ROYAL': ATTACK AT DAWN (historical PT-109 message)")
