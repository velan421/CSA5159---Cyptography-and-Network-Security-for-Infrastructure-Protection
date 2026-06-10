# ============================================================
# EXPERIMENT 37 - FREQUENCY ATTACK ON MONOALPHABETIC CIPHER
# ============================================================

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

ENGLISH_FREQ = {
    'E':12.70,'T':9.06,'A':8.17,'O':7.51,'I':6.97,'N':6.75,
    'S':6.33,'H':6.09,'R':5.99,'D':4.25,'L':4.03,'C':2.78,
    'U':2.76,'M':2.41,'W':2.36,'F':2.23,'G':2.02,'Y':1.97,
    'P':1.93,'B':1.49,'V':0.98,'K':0.77,'J':0.15,'X':0.15,
    'Q':0.10,'Z':0.07
}

def get_freq(text):
    freq  = {}
    total = 0
    for ch in text.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
            total += 1
    return freq, total

def chi_squared(text):
    freq, total = get_freq(text)
    if total == 0:
        return float('inf')
    score = 0
    for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        obs = (freq.get(ch, 0) / total) * 100
        exp = ENGLISH_FREQ.get(ch, 0.01)
        score += ((obs - exp) ** 2) / exp
    return score

def apply_mapping(text, mapping):
    return ''.join(mapping.get(ch, ch) if ch.isalpha() else ch
                   for ch in text.upper())

def frequency_attack(ciphertext, top_n=10):
    freq, total = get_freq(ciphertext)
    sorted_cipher = sorted(freq.keys(), key=lambda x: -freq[x])
    eng = list(ENGLISH_FREQ_ORDER)
    candidates = []

    # Base mapping
    base = {c: eng[i] for i, c in enumerate(sorted_cipher) if i < len(eng)}
    candidates.append((chi_squared(apply_mapping(ciphertext, base)), dict(base),
                        apply_mapping(ciphertext, base)))

    # Swap top 12 pairs to generate more candidates
    for i in range(min(12, len(eng)-1)):
        for j in range(i+1, min(i+6, len(eng))):
            m = dict(base)
            keys = list(m.keys())
            if i < len(keys) and j < len(keys):
                ki, kj = keys[i], keys[j]
                m[ki], m[kj] = m[kj], m[ki]
                dec   = apply_mapping(ciphertext, m)
                score = chi_squared(dec)
                candidates.append((score, m, dec))

    candidates.sort(key=lambda x: x[0])
    return candidates[:top_n], sorted_cipher, freq, total

ciphertext = input("Enter monoalphabetic ciphertext: ").strip()
n_input    = input("How many top plaintexts? (default 10): ").strip()
top_n      = int(n_input) if n_input.isdigit() else 10

candidates, sorted_cipher, freq, total = frequency_attack(ciphertext, top_n)

print(f"\nCharacter Frequencies:")
print(f"  {'Char':<5} {'Count':<7} {'Freq%':<8} {'Bar'}")
print("  " + "-"*40)
for ch in sorted_cipher:
    cnt = freq[ch]
    bar = "#" * int((cnt/total)*30)
    print(f"  {ch:<5} {cnt:<7} {cnt/total*100:5.2f}%   {bar}")

print(f"\nTop {top_n} decryption candidates (lower chi² = more English-like):")
print(f"\n{'Rank':<6} {'Chi²':>8}   {'Plaintext'}")
print("-" * 70)
for rank, (score, mapping, decoded) in enumerate(candidates, 1):
    print(f"  {rank:<6} {score:>8.2f}   {decoded}")

print("\nWould you like to manually refine the best mapping? (yes/no)")
if input().strip().lower() == "yes":
    _, best_map, _ = candidates[0]
    print("\nCurrent mapping (Cipher → Plain):")
    for k, v in sorted(best_map.items()):
        print(f"  {k} → {v}")
    while True:
        change = input("\nChange (e.g. B:E) or 'done': ").strip().upper()
        if change == "DONE":
            break
        if ":" in change:
            parts = change.split(":")
            if len(parts) == 2 and parts[0].isalpha() and parts[1].isalpha():
                best_map[parts[0]] = parts[1]
    refined = apply_mapping(ciphertext, best_map)
    print(f"\nRefined result: {refined}")
