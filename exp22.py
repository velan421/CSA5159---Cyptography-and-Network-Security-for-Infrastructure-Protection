# ============================================================
# EXPERIMENT 22 - S-DES IN CBC MODE
# ============================================================

# S-DES Tables
P10  = [3,5,2,7,4,10,1,9,8,6]
P8   = [6,3,7,4,8,5,10,9]
IP   = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]
EP   = [4,1,2,3,2,3,4,1]
P4   = [2,4,3,1]

S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

def permute(bits, table):
    return [bits[i-1] for i in table]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def sbox_lookup(bits4, sbox):
    row = (bits4[0] << 1) | bits4[3]
    col = (bits4[1] << 1) | bits4[2]
    val = sbox[row][col]
    return [(val >> 1) & 1, val & 1]

def generate_subkeys(key10):
    p10 = permute(key10, P10)
    left, right = p10[:5], p10[5:]
    left, right = left_shift(left, 1), left_shift(right, 1)
    k1 = permute(left + right, P8)
    left, right = left_shift(left, 2), left_shift(right, 2)
    k2 = permute(left + right, P8)
    return k1, k2

def fk(bits8, subkey):
    left, right = bits8[:4], bits8[4:]
    ep = permute(right, EP)
    xored = xor(ep, subkey)
    s0_out = sbox_lookup(xored[:4], S0)
    s1_out = sbox_lookup(xored[4:], S1)
    p4 = permute(s0_out + s1_out, P4)
    return xor(left, p4) + right

def sdes_encrypt_block(plain8, k1, k2):
    ip = permute(plain8, IP)
    fk1 = fk(ip, k1)
    sw  = fk1[4:] + fk1[:4]
    fk2 = fk(sw, k2)
    return permute(fk2, IP_INV)

def sdes_decrypt_block(cipher8, k1, k2):
    ip = permute(cipher8, IP)
    fk1 = fk(ip, k2)
    sw  = fk1[4:] + fk1[:4]
    fk2 = fk(sw, k1)
    return permute(fk2, IP_INV)

def bits_to_str(bits):
    return ''.join(map(str, bits))

def str_to_bits(s):
    return [int(c) for c in s if c in '01']

def cbc_sdes_encrypt(plaintext_bits, key10, iv8):
    k1, k2 = generate_subkeys(key10)
    ciphertext = []
    prev = iv8[:]
    for i in range(0, len(plaintext_bits), 8):
        block = plaintext_bits[i:i+8]
        xored = xor(block, prev)
        enc   = sdes_encrypt_block(xored, k1, k2)
        ciphertext.extend(enc)
        prev = enc
    return ciphertext

def cbc_sdes_decrypt(cipher_bits, key10, iv8):
    k1, k2 = generate_subkeys(key10)
    plaintext = []
    prev = iv8[:]
    for i in range(0, len(cipher_bits), 8):
        block = cipher_bits[i:i+8]
        dec   = sdes_decrypt_block(block, k1, k2)
        plain = xor(dec, prev)
        plaintext.extend(plain)
        prev = block
    return plaintext

# Test vectors from problem
print("=" * 60)
print("S-DES IN CBC MODE")
print("=" * 60)

iv_bits  = str_to_bits("10101010")
key_bits = str_to_bits("0111111101")

# Test vector: plaintext 0000000100100011, key 0111111101, IV 1010 1010
# Expected ciphertext: 1111010000001011

plain_test = str_to_bits("0000000100100011")
print(f"\nTest Vector:")
print(f"  Key       : {bits_to_str(key_bits)}")
print(f"  IV        : {bits_to_str(iv_bits)}")
print(f"  Plaintext : {bits_to_str(plain_test)}")

cipher = cbc_sdes_encrypt(plain_test, key_bits, iv_bits)
print(f"  Ciphertext: {bits_to_str(cipher)}")
print(f"  Expected  : 1111010000001011")
print(f"  Match     : {bits_to_str(cipher) == '1111010000001011'}")

decrypted = cbc_sdes_decrypt(cipher, key_bits, iv_bits)
print(f"  Decrypted : {bits_to_str(decrypted)}")
print(f"  Match orig: {bits_to_str(decrypted) == bits_to_str(plain_test)}")

print("\n--- CUSTOM INPUT ---")
pt_in  = input("Enter plaintext bits (multiples of 8, e.g. 00000001): ").strip()
key_in = input("Enter 10-bit key (e.g. 0111111101): ").strip()
iv_in  = input("Enter 8-bit IV  (e.g. 10101010): ").strip()

if pt_in and key_in and iv_in:
    pt  = str_to_bits(pt_in)
    k   = str_to_bits(key_in)
    iv  = str_to_bits(iv_in)
    ct  = cbc_sdes_encrypt(pt, k, iv)
    dt  = cbc_sdes_decrypt(ct, k, iv)
    print(f"Encrypted : {bits_to_str(ct)}")
    print(f"Decrypted : {bits_to_str(dt)}")
