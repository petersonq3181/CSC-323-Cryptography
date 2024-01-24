from collections import Counter
from math import log
import matplotlib.pyplot as plt


# help from here: https://www.cipherchallenge.org/wp-content/uploads/2020/12/Five-ways-to-crack-a-Vigenere-cipher.pdf

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
english_freqs = {'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'u': 2.8, 'w': 2.4, 'm': 2.4, 'f': 2.2, 'c': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5, 'k': 1.3, 'v': 1.0, 'j': 0.2, 'x': 0.2, 'q': 0.1, 'z': 0.1}

def index_of_coincidence(text):
    text = ''.join([char.upper() for char in text if char.upper() in ALPHABET])
    counts = [0]*26
    for char in text:
        counts[ALPHABET.index(char)] += 1
    numer = 0
    total = 0
    for i in range(26):
        numer += counts[i]*(counts[i]-1)
        total += counts[i]
    return 26*numer / (total*(total-1))


def analyze_ciphertext_for_key_lengths(ciphertext, max_key_length):
    ioc_data = []
    for key_length in range(1, max_key_length + 1):
        groups = [ciphertext[i::key_length] for i in range(key_length)]
        group_iocs = [index_of_coincidence(group) for group in groups]
        avg_ioc = sum(group_iocs) / len(group_iocs)
        ioc_data.append((key_length, avg_ioc))
    return ioc_data

with open('Lab0.TaskII.D.txt', 'rb') as file:
    ciphertext = file.read().strip().decode('ascii')
   
ioc_data = analyze_ciphertext_for_key_lengths(ciphertext, 40)

# Unzip the data
key_lengths, avg_iocs = zip(*ioc_data)

# Plotting
plt.bar(key_lengths, avg_iocs)
plt.xlabel('Key Length (Period)')
plt.ylabel('Average IOC')
plt.title('Average IOC vs Key Length')
plt.xticks(range(1, len(key_lengths) + 1))  # Set x-ticks to be every key length
plt.ylim(0, 2.5)  # Set the limits of y-axis
plt.grid(True)  # Enable gridlines
plt.show()
