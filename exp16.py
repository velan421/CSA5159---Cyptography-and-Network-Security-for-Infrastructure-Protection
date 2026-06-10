# ============================================================
# EXPERIMENT 16 - FREQUENCY ATTACK ON MONOALPHABETIC CIPHER
# ============================================================

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.49,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}

def get_freq_order(ciphertext):
    freq = {}
    total = 0
    for ch in ciphertext.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
            total += 1
    sorted_chars = sorted(freq.keys(), key=lambda x: -freq[x])
    return sorted_chars, freq, total

def apply_mapping(ciphertext, mapping):
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += mapping.get(ch, '_')
        else:
            result += ch
    return result

def score_text(text):
    """Score how English-like the text is using chi-squared."""
    freq = {}
    total = 0
    for ch in text.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
            total += 1
    if total == 0:
        return float('inf')
    score = 0
    for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed = (freq.get(ch, 0) / total) * 100
        expected = ENGLISH_FREQ.get(ch, 0.01)
        score += ((observed - expected) ** 2) / expected
    return score

def generate_top_n_mappings(ciphertext, top_n=10):
    """
    Generate candidate mappings by mapping cipher freq order to
    English freq order with slight permutations for top candidates.
    """
    sorted_cipher, freq, total = get_freq_order(ciphertext)
    candidates = []

    # Base mapping: direct frequency order match
    base_mapping = {}
    for i, c in enumerate(sorted_cipher):
        if i < len(ENGLISH_FREQ_ORDER):
            base_mapping[c] = ENGLISH_FREQ_ORDER[i]

    base_decoded = apply_mapping(ciphertext, base_mapping)
    base_score   = score_text(base_decoded)
    candidates.append((base_score, base_mapping, base_decoded))

    # Generate variations by swapping adjacent frequency mappings
    eng_list = list(ENGLISH_FREQ_ORDER)
    for i in range(min(len(eng_list)-1, 15)):
        for j in range(i+1, min(i+5, len(eng_list))):
            new_eng = eng_list[:]
            new_eng[i], new_eng[j] = new_eng[j], new_eng[i]
            mapping = {}
            for k, c in enumerate(sorted_cipher):
                if k < len(new_eng):
                    mapping[c] = new_eng[k]
            decoded = apply_mapping(ciphertext, mapping)
            score   = score_text(decoded)
            candidates.append((score, mapping, decoded))

    candidates.sort(key=lambda x: x[0])
    return candidates[:top_n]

ciphertext = input("Enter monoalphabetic ciphertext: ").strip()
top_n_input = input("How many top plaintexts to show? (default 10): ").strip()
top_n = int(top_n_input) if top_n_input.isdigit() else 10

sorted_cipher, freq, total = get_freq_order(ciphertext)
print(f"\nCipher frequency order : {' '.join(sorted_cipher)}")
print(f"English frequency order: {' '.join(ENGLISH_FREQ_ORDER)}")

print(f"\nTop {top_n} possible plaintexts (ranked by chi-squared score):\n")
print(f"{'Rank':<6} {'Chi²':<10} {'Plaintext'}")
print("-" * 70)

candidates = generate_top_n_mappings(ciphertext, top_n)
for rank, (score, mapping, decoded) in enumerate(candidates, 1):
    print(f"  {rank:<6} {score:<10.2f} {decoded}")

print("\nNote: Lower chi² score = more English-like = more likely correct.")
