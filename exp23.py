# ============================================================
# EXPERIMENT 23 - S-DES IN COUNTER (CTR) MODE
# ============================================================

P10  = [3,5,2,7,4,10,1,9,8,6]
P8   = [6,3,7,4,8,5,10,9]
IP   = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]
EP   = [4,1,2,3,2,3,4,1]
P4   = [2,4,3,1]
S0   = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1   = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

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
    l, r = p10[:5], p10[5:]
    l, r = left_shift(l, 1), left_shift(r, 1)
    k1 = permute(l + r, P8)
    l, r = left_shift(l, 2), left_shift(r, 2)
    k2 = permute(l + r, P8)
    return k1, k2

def fk(bits8, subkey):
    left, right = bits8[:4], bits8[4:]
    ep    = permute(right, EP)
    xored = xor(ep, subkey)
    p4    = permute(sbox_lookup(xored[:4], S0) + sbox_lookup(xored[4:], S1), P4)
    return xor(left, p4) + right

def sdes_encrypt_block(plain8, k1, k2):
    ip  = permute(plain8, IP)
    fk1 = fk(ip, k1)
    sw  = fk1[4:] + fk1[:4]
    fk2 = fk(sw, k2)
    return permute(fk2, IP_INV)

def int_to_bits8(n):
    return [(n >> (7 - i)) & 1 for i in range(8)]

def bits_to_str(bits):
    return ''.join(map(str, bits))

def str_to_bits(s):
    return [int(c) for c in s if c in '01']

def ctr_sdes(data_bits, key10, counter_start=0):
    """CTR mode: same function for encrypt and decrypt."""
    k1, k2 = generate_subkeys(key10)
    result = []
    counter = counter_start
    print(f"\n{'Block':<8} {'Counter':<12} {'Keystream':<12} {'Data':<12} {'Output'}")
    print("-" * 60)
    for i in range(0, len(data_bits), 8):
        block      = data_bits[i:i+8]
        ctr_bits   = int_to_bits8(counter)
        keystream  = sdes_encrypt_block(ctr_bits, k1, k2)
        out        = xor(block, keystream)
        print(f"  {i//8+1:<6} {bits_to_str(ctr_bits):<12} {bits_to_str(keystream):<12} "
              f"{bits_to_str(block):<12} {bits_to_str(out)}")
        result.extend(out)
        counter += 1
    return result

# ---- Test Vector ----
print("=" * 60)
print("S-DES IN COUNTER (CTR) MODE")
print("=" * 60)

key_bits   = str_to_bits("0111111101")
plain_test = str_to_bits("000000010000001000000100")
expected   = "001110000100111100110010"

print(f"\nTest Vector:")
print(f"  Key       : {bits_to_str(key_bits)}")
print(f"  Counter   : starts at 00000000")
print(f"  Plaintext : {bits_to_str(plain_test)}")

print("\nEncryption:")
cipher = ctr_sdes(plain_test, key_bits, counter_start=0)
print(f"\n  Ciphertext: {bits_to_str(cipher)}")
print(f"  Expected  : {expected}")
print(f"  Match     : {bits_to_str(cipher) == expected}")

print("\nDecryption (CTR is symmetric — same operation):")
decrypted = ctr_sdes(cipher, key_bits, counter_start=0)
print(f"\n  Decrypted : {bits_to_str(decrypted)}")
print(f"  Match orig: {bits_to_str(decrypted) == bits_to_str(plain_test)}")

print("\n--- CUSTOM INPUT ---")
pt_in  = input("\nEnter plaintext bits (multiples of 8): ").strip()
key_in = input("Enter 10-bit key (e.g. 0111111101): ").strip()
ctr_in = input("Enter counter start (integer, default 0): ").strip()

if pt_in and key_in:
    pt  = str_to_bits(pt_in)
    k   = str_to_bits(key_in)
    ctr = int(ctr_in) if ctr_in.isdigit() else 0
    print("\nEncrypting:")
    ct = ctr_sdes(pt, k, ctr)
    print(f"Ciphertext: {bits_to_str(ct)}")
    print("\nDecrypting:")
    dt = ctr_sdes(ct, k, ctr)
    print(f"Decrypted : {bits_to_str(dt)}")
