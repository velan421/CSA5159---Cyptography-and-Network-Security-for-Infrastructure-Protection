# ============================================================
# EXPERIMENT 6 - BREAKING AN AFFINE CIPHER
# ============================================================

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(ciphertext, a, b):
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            c = ord(ch) - ord('A')
            p = (a_inv * (c - b)) % 26
            result += chr(p + ord('A'))
        else:
            result += ch
    return result

def break_affine_cipher(ciphertext, most_freq, second_freq):
    # In English: 'E' (4) is most frequent, 'T' (19) is second most frequent
    e_val = ord('E') - ord('A')   # 4
    t_val = ord('T') - ord('A')   # 19
    b1 = ord(most_freq.upper())   - ord('A')
    b2 = ord(second_freq.upper()) - ord('A')

    print(f"\nAssuming '{most_freq}' maps to 'E' (4) and '{second_freq}' maps to 'T' (19)")
    print(f"Solving: {most_freq}={b1}, {second_freq}={b2}")

    solutions_found = 0
    for a in range(1, 26):
        if gcd(a, 26) != 1:
            continue
        # a*e + b ≡ b1 (mod 26)
        # a*t + b ≡ b2 (mod 26)
        # => a*(e - t) ≡ b1 - b2 (mod 26)
        lhs = (a * (e_val - t_val)) % 26
        rhs = (b1 - b2) % 26
        if lhs == rhs:
            b = (b1 - a * e_val) % 26
            dec = affine_decrypt(ciphertext, a, b)
            if dec:
                print(f"\nPossible key found: a={a}, b={b}")
                print(f"Decrypted text    : {dec}")
                solutions_found += 1

    if solutions_found == 0:
        print("Could not break the cipher with given frequency assumptions.")

def get_top_frequencies(ciphertext):
    freq = {}
    for ch in ciphertext.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
    print("\nLetter Frequency in Ciphertext:")
    for ch, cnt in sorted_freq:
        print(f"  {ch} : {cnt}")
    return sorted_freq

ciphertext = input("Enter ciphertext: ")

sorted_freq = get_top_frequencies(ciphertext)

most_freq   = input("\nEnter most frequent letter (default B): ").strip() or 'B'
second_freq = input("Enter second most frequent letter (default U): ").strip() or 'U'

break_affine_cipher(ciphertext, most_freq, second_freq)
