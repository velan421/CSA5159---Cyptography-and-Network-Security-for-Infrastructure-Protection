# ============================================================
# EXPERIMENT 14 - ONE-TIME PAD VERSION OF VIGENERE CIPHER
# ============================================================

def otp_encrypt(plaintext, key_stream):
    text = ''.join(filter(str.isalpha, plaintext.upper()))
    if len(key_stream) < len(text):
        print("Warning: Key stream shorter than plaintext!")
        return None
    ciphertext = ""
    print(f"\n{'Plain':<8} {'Num':<6} {'Key':<6} {'(p+k)%26':<10} {'Cipher'}")
    print("-" * 45)
    for i, ch in enumerate(text):
        p = ord(ch) - ord('A')
        k = key_stream[i]
        c = (p + k) % 26
        cipher_ch = chr(c + ord('A'))
        print(f"  {ch:<8} {p:<6} {k:<6} {c:<10} {cipher_ch}")
        ciphertext += cipher_ch
    return ciphertext

def otp_decrypt(ciphertext, key_stream):
    text = ''.join(filter(str.isalpha, ciphertext.upper()))
    plaintext = ""
    for i, ch in enumerate(text):
        c = ord(ch) - ord('A')
        k = key_stream[i]
        p = (c - k) % 26
        plaintext += chr(p + ord('A'))
    return plaintext

def find_key_for_target(ciphertext, target_plaintext):
    """Find a key stream so that ciphertext decrypts to target_plaintext."""
    c_text = ''.join(filter(str.isalpha, ciphertext.upper()))
    p_text = ''.join(filter(str.isalpha, target_plaintext.upper()))
    if len(c_text) != len(p_text):
        print("Lengths don't match!")
        return None
    key = []
    for c_ch, p_ch in zip(c_text, p_text):
        c = ord(c_ch) - ord('A')
        p = ord(p_ch) - ord('A')
        k = (c - p) % 26
        key.append(k)
    return key

# ---- Part (a): Encrypt "send more money" ----
print("=" * 60)
print("ONE-TIME PAD VIGENERE CIPHER")
print("=" * 60)

plaintext_a = "send more money"
key_a = [9, 0, 1, 7, 23, 15, 21, 14, 11, 11, 2, 8, 9]

print(f"\n(a) Plaintext  : {plaintext_a.upper()}")
print(f"    Key stream  : {key_a}")
ciphertext_a = otp_encrypt(plaintext_a, key_a)
print(f"\n    Ciphertext : {ciphertext_a}")

# ---- Part (b): Find key so ciphertext decrypts to "cash not needed" ----
print("\n" + "-" * 60)
print("(b) Find key so ciphertext decrypts to 'cash not needed'")
print("-" * 60)

target = "cash not needed"
target_clean = ''.join(filter(str.isalpha, target.upper()))
cipher_clean  = ''.join(filter(str.isalpha, ciphertext_a))

# Pad target if needed
if len(target_clean) < len(cipher_clean):
    target_clean = target_clean.ljust(len(cipher_clean), 'X')

key_b = find_key_for_target(cipher_clean, target_clean)
print(f"\n    Target plaintext : {target.upper()}")
print(f"    New key stream   : {key_b}")

# Verify
verified = otp_decrypt(cipher_clean, key_b)
print(f"    Verification     : {verified}")
print("\nThis demonstrates the 'perfect secrecy' property of OTP:")
print("The same ciphertext can decode to ANY plaintext given the right key!")
