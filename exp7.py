# ============================================================
# EXPERIMENT 7 - SIMPLE SUBSTITUTION CIPHER (FREQUENCY ANALYSIS)
# ============================================================

def frequency_analysis(ciphertext):
    freq = {}
    total = 0
    for ch in ciphertext.upper():
        if ch.isalpha():
            freq[ch] = freq.get(ch, 0) + 1
            total += 1

    if total == 0:
        print("No alphabetic characters found in ciphertext.")
        return []

    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])

    print("\nCharacter Frequency Analysis:")
    print(f"  {'Char':<6} {'Count':<8} {'Frequency'}")
    print("  " + "-" * 28)
    for ch, cnt in sorted_freq:
        bar = "#" * int((cnt / total) * 40)
        print(f"  {ch:<6} {cnt:<8} {cnt/total*100:5.2f}%  {bar}")

    return sorted_freq

def build_mapping(sorted_freq, english_order):
    cipher_letters = [ch for ch, _ in sorted_freq]
    mapping = {}
    for i, c in enumerate(cipher_letters):
        if i < len(english_order):
            mapping[c] = english_order[i]
    return mapping

def apply_mapping(ciphertext, mapping):
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            result += mapping.get(ch, '_')
        else:
            result += ch
    return result

def update_mapping_interactive(mapping):
    print("\nCurrent Mapping (Cipher -> Plain):")
    for k, v in sorted(mapping.items()):
        print(f"  {k} -> {v}")

    while True:
        change = input("\nChange a mapping? Enter 'cipher:plain' (e.g. B:E) or 'done': ").strip()
        if change.lower() == 'done':
            break
        if ':' in change:
            parts = change.upper().split(':')
            if len(parts) == 2 and parts[0].isalpha() and parts[1].isalpha():
                mapping[parts[0]] = parts[1]
                print(f"  Mapped {parts[0]} -> {parts[1]}")
            else:
                print("  Invalid format. Use 'X:Y' where X and Y are single letters.")
        else:
            print("  Invalid input.")
    return mapping

# The famous Poe cipher from the problem
default_cipher = (
    "53 305))6 4826)4 .)4 );806 ;48 8 60))85;;]8 ;: 8 83"
    "(88)5 46(;88 96 ?;8)* (;485);5 2: (;4956 2(5 4)8 8"
    ";4069285);)6 8)4 ;1( 9;48081;8:8 1;48 85;4)485 528806"
    "81(9;48;(88;4( ?34;48)4 ;161;:188; ?;"
)

print("Default ciphertext (Poe cipher) loaded.")
print("Press Enter to use it, or type your own ciphertext.")
user_input = input("Ciphertext: ").strip()
ciphertext = user_input if user_input else default_cipher

sorted_freq = frequency_analysis(ciphertext)

# Standard English letter frequency order
english_freq = list("ETAOINSHRDLCUMWFGYPBVKJXQZ")

mapping = build_mapping(sorted_freq, english_freq)

decoded = apply_mapping(ciphertext, mapping)
print(f"\nAuto-decoded Text (frequency mapping):")
print(decoded)

# Allow manual refinement
refine = input("\nWould you like to manually refine the mapping? (yes/no): ").strip().lower()
if refine == 'yes':
    mapping = update_mapping_interactive(mapping)
    decoded = apply_mapping(ciphertext, mapping)
    print(f"\nRefined Decoded Text:")
    print(decoded)

print("\nNote: Frequency analysis is a starting point.")
print("For short texts, manual refinement is needed for full decryption.")
