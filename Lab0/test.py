from collections import Counter
from math import log

# help from here: https://www.cipherchallenge.org/wp-content/uploads/2020/12/Five-ways-to-crack-a-Vigenere-cipher.pdf

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
english_freqs = {'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'u': 2.8, 'w': 2.4, 'm': 2.4, 'f': 2.2, 'c': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5, 'k': 1.3, 'v': 1.0, 'j': 0.2, 'x': 0.2, 'q': 0.1, 'z': 0.1}

def index_of_coincidence(text):
    counts = [0]*26
    for char in text:
        counts[ALPHABET.index(char)] += 1
    numer = 0
    total = 0
    for i in range(26):
        numer += counts[i]*(counts[i]-1)
        total += counts[i]
    return 26*numer / (total*(total-1))

ioc_expected = 1.73  
def getIOC(s):
    N = len(s)
    if N <= 1: 
        return 0
    c = 26 

    s = ''.join([c for c in s if c.isalpha()])
    s = s.lower()

    counts = Counter(s)
    total = sum(ni * (ni - 1) for ni in counts.values())

    IOC = float(total) / ((N * (N - 1)) / c)
    return IOC

english_text = "THIS IS A SAMPLE ENGLISH TEXT TO TEST INDEX OF COINCIDENCE"
non_english_text = "Ceci est un texte en français pour tester l'indice de coïncidence"
mixed_text = "This text3 has nuM8bers and punctuation! It's a mix3d bag."

def process_for_index_of_coincidence(text):
    # Filter only alphabetic characters and convert to uppercase
    return ''.join([char.upper() for char in text if char.upper() in ALPHABET])


# Compare IOCs
def compare_iocs(text):
    text_upper = process_for_index_of_coincidence(text)
    ioc1 = index_of_coincidence(text_upper)
    ioc2 = getIOC(text)
    return ioc1, ioc2

# Testing and comparing IOCs
english_iocs = compare_iocs(english_text)
non_english_iocs = compare_iocs(non_english_text)
mixed_iocs = compare_iocs(mixed_text)

print("English Text IOCs:", english_iocs)
print("Non-English Text IOCs:", non_english_iocs)
print("Mixed Text IOCs:", mixed_iocs)

# Example usage
with open('Lab0.TaskII.D.txt', 'rb') as file:
    ciphertext_bytes = file.read().strip()


