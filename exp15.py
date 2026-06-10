# ============================================================
# EXPERIMENT 15 - FREQUENCY ATTACK ON ADDITIVE (CAESAR) CIPHER
# ============================================================

# English letter frequencies (%)
ENGLISH_FREQ = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70,
    'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15,
    'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51,
    'P': 1.93, 'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
    'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
    'Z': 0.07
}

def get_cipher_freq(ciphertext):
    freq = {}
    total = 0
    for ch in ciphertext.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
            total += 1
    return {k: (v / total) * 100 for k, v in freq.items()} if total else {}

def chi_squared(text_freq):
    score = 0
    for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed = text_freq.get(ch, 0)
        expected = ENGLISH_FREQ[ch]
        score += ((observed - expected) ** 2) / expected
    return score

def decrypt_additive(ciphertext, key):
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
        else:
            result += ch
    return result

def frequency_attack_additive(ciphertext, top_n=10):
    results = []
    for key in range(26):
        decrypted = decrypt_additive(ciphertext, key)
        freq = get_cipher_freq(decrypted)
        score = chi_squared(freq)
        results.append((score, key, decrypted))
    results.sort(key=lambda x: x[0])
    return results[:top_n]

ciphertext = input("Enter ciphertext (additive/Caesar cipher): ").strip()
top_n_input = input("How many top plaintexts to show? (default 10): ").strip()
top_n = int(top_n_input) if top_n_input.isdigit() else 10

print(f"\nTop {top_n} possible plaintexts (ranked by likelihood):")
print(f"\n{'Rank':<6} {'Key':<6} {'Chi²':<12} {'Plaintext'}")
print("-" * 70)

results = frequency_attack_additive(ciphertext, top_n)
for rank, (score, key, text) in enumerate(results, 1):
    print(f"  {rank:<6} {key:<6} {score:<12.2f} {text}")
