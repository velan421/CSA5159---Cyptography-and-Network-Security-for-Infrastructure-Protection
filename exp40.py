# ============================================================
# EXPERIMENT 40 - FREQUENCY ATTACK ON MONOALPHABETIC CIPHER
# ============================================================

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
ENGLISH_FREQ = {
    'E':12.70,'T':9.06,'A':8.17,'O':7.51,'I':6.97,'N':6.75,
    'S':6.33,'H':6.09,'R':5.99,'D':4.25,'L':4.03,'C':2.78,
    'U':2.76,'M':2.41,'W':2.36,'F':2.23,'G':2.02,'Y':1.97,
    'P':1.93,'B':1.49,'V':0.98,'K':0.77,'J':0.15,'X':0.15,
    'Q':0.10,'Z':0.07
}
# English bigram frequencies (top common pairs)
BIGRAMS = {"TH","HE","IN","ER","AN","RE","ON","EN","AT","ND",
           "TI","ES","OR","TE","OF","ED","IS","IT","AL","AR"}

def get_freq(text):
    freq, total = {}, 0
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

def bigram_score(text):
    """Count matching English bigrams."""
    text = ''.join(filter(str.isalpha, text.upper()))
    count = sum(1 for i in range(len(text)-1) if text[i:i+2] in BIGRAMS)
    return count

def combined_score(text):
    return chi_squared(text) - bigram_score(text) * 2   # lower = better

def apply_mapping(text, mapping):
    return ''.join(mapping.get(ch, ch) if ch.isalpha() else ch
                   for ch in text.upper())

def attack(ciphertext, top_n=10):
    freq, total = get_freq(ciphertext)
    cipher_order = sorted(freq.keys(), key=lambda x: -freq[x])
    eng = list(ENGLISH_FREQ_ORDER)

    base = {c: eng[i] for i, c in enumerate(cipher_order) if i < len(eng)}
    candidates = []
    candidates.append((combined_score(apply_mapping(ciphertext, base)),
                        dict(base), apply_mapping(ciphertext, base)))

    # Generate permutations of top-N English letters
    for i in range(min(14, len(eng)-1)):
        for j in range(i+1, min(i+7, len(eng))):
            m = dict(base)
            keys = list(m.keys())
            if i < len(keys) and j < len(keys):
                m[keys[i]], m[keys[j]] = m[keys[j]], m[keys[i]]
                dec   = apply_mapping(ciphertext, m)
                score = combined_score(dec)
                candidates.append((score, m, dec))

    candidates.sort(key=lambda x: x[0])
    seen, unique = set(), []
    for item in candidates:
        key = item[2][:30]
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique[:top_n], cipher_order, freq, total

print("=" * 60)
print("FREQUENCY ATTACK ON MONOALPHABETIC SUBSTITUTION CIPHER")
print("=" * 60)

ciphertext = input("\nEnter monoalphabetic ciphertext: ").strip()
n_input    = input("Top N plaintexts to show? (default 10): ").strip()
top_n      = int(n_input) if n_input.isdigit() else 10

candidates, cipher_order, freq, total = attack(ciphertext, top_n)

print(f"\nFrequency analysis:")
print(f"  Cipher freq order : {' '.join(cipher_order[:13])}...")
print(f"  English freq order: {' '.join(ENGLISH_FREQ_ORDER[:13])}...")

print(f"\nTop {top_n} candidates (chi² adjusted for bigram bonus):")
print(f"\n  {'Rank':<6} {'Score':>8}   {'Candidate Plaintext'}")
print("  " + "-" * 70)
for rank, (score, mapping, decoded) in enumerate(candidates, 1):
    print(f"  {rank:<6} {score:>8.2f}   {decoded}")

print("\nManually refine best result? (yes/no)")
if input().strip().lower() == "yes":
    _, best_map, _ = candidates[0]
    while True:
        print(f"\nCurrent result: {apply_mapping(ciphertext, best_map)}")
        change = input("Change (e.g. X:E) or 'done': ").strip().upper()
        if change == "DONE":
            break
        if ":" in change:
            parts = change.split(":")
            if len(parts) == 2 and len(parts[0]) == 1 and len(parts[1]) == 1:
                best_map[parts[0]] = parts[1]
    print(f"\nFinal result: {apply_mapping(ciphertext, best_map)}")
