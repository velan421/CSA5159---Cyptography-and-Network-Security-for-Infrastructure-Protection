# ============================================================
# EXPERIMENT 39 - FREQUENCY ATTACK ON ADDITIVE (CAESAR) CIPHER
# ============================================================

ENGLISH_FREQ = {
    'A':8.17,'B':1.49,'C':2.78,'D':4.25,'E':12.70,'F':2.23,
    'G':2.02,'H':6.09,'I':6.97,'J':0.15,'K':0.77,'L':4.03,
    'M':2.41,'N':6.75,'O':7.51,'P':1.93,'Q':0.10,'R':5.99,
    'S':6.33,'T':9.06,'U':2.76,'V':0.98,'W':2.36,'X':0.15,
    'Y':1.97,'Z':0.07
}

def decrypt_additive(ciphertext, key):
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
        else:
            result += ch
    return result

def chi_squared_score(text):
    freq  = {}
    total = 0
    for ch in text.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
            total += 1
    if total == 0:
        return float('inf')
    score = 0
    for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        obs = (freq.get(ch, 0) / total) * 100
        exp = ENGLISH_FREQ[ch]
        score += ((obs - exp) ** 2) / exp
    return score

def frequency_attack_additive(ciphertext, top_n=10):
    results = []
    for key in range(26):
        decrypted = decrypt_additive(ciphertext, key)
        score     = chi_squared_score(decrypted)
        results.append((score, key, decrypted))
    results.sort(key=lambda x: x[0])
    return results[:top_n]

def show_cipher_freq(ciphertext):
    freq  = {}
    total = 0
    for ch in ciphertext.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
            total += 1
    sorted_f = sorted(freq.items(), key=lambda x: -x[1])
    print(f"\n  {'Char':<5} {'Count':<7} {'Freq%':<8} {'Bar'}")
    print("  " + "-"*35)
    for ch, cnt in sorted_f:
        bar = "#" * int((cnt/total)*25)
        print(f"  {ch:<5} {cnt:<7} {cnt/total*100:5.2f}%   {bar}")

print("=" * 60)
print("FREQUENCY ATTACK ON ADDITIVE (CAESAR) CIPHER")
print("=" * 60)

ciphertext = input("\nEnter ciphertext: ").strip()
n_input    = input("How many top plaintexts to show? (default 10): ").strip()
top_n      = int(n_input) if n_input.isdigit() else 10

show_cipher_freq(ciphertext)

results = frequency_attack_additive(ciphertext, top_n)

print(f"\nTop {top_n} possible plaintexts (sorted by chi-squared score):")
print(f"\n  {'Rank':<6} {'Key':<6} {'Chi²':>10}   {'Plaintext'}")
print("  " + "-" * 65)
for rank, (score, key, text) in enumerate(results, 1):
    print(f"  {rank:<6} {key:<6} {score:>10.2f}   {text}")

print("\nNote: Rank 1 is the most likely English plaintext.")
print("      Lower chi-squared = better match to English letter frequencies.")
