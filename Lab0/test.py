from collections import Counter
from math import log, sqrt
import matplotlib.pyplot as plt
from random import randrange
import string 

def xor_strings(s, key):
    repeated_key = (key * (len(s) // len(key) + 1))[:len(s)]
    return bytes([input_byte ^ key_byte for input_byte, key_byte in zip(s, repeated_key)])


# help from here: https://www.cipherchallenge.org/wp-content/uploads/2020/12/Five-ways-to-crack-a-Vigenere-cipher.pdf
# NOTE: states the stats-only attack t is only reliable for
# ciphertexts that are at least 100 times as long as the period
# (found period = 7, ciphertext length = 668 )

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
english_freqs = {'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'u': 2.8, 'w': 2.4, 'm': 2.4, 'f': 2.2, 'c': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5, 'k': 1.3, 'v': 1.0, 'j': 0.2, 'x': 0.2, 'q': 0.1, 'z': 0.1}
english_freqs_list = [english_freqs[char.lower()] for char in ALPHABET]

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
    key_lengths = []
    avg_iocs = [] 
    for key_length in range(1, max_key_length + 1):
        groups = [ciphertext[i::key_length] for i in range(key_length)]
        group_iocs = [index_of_coincidence(group) for group in groups]
        avg_ioc = sum(group_iocs) / len(group_iocs)

        key_lengths.append(key_length)
        avg_iocs.append(avg_ioc)
    return key_lengths, avg_iocs

def cosangle(x, y):
    numerator = sum(xi * yi for xi, yi in zip(x, y))
    lengthx2 = sum(xi ** 2 for xi in x)
    lengthy2 = sum(yi ** 2 for yi in y)
    return numerator / sqrt(lengthx2 * lengthy2)

def encrypt(plaintext,key):
    ciphertext = ''
    for i in range(len(plaintext)):
        p = ALPHABET.index(plaintext[i])
        k = ALPHABET.index(key[i%len(key)])
        c = (p + k) % 26
        ciphertext += ALPHABET[c]
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = ''
    for i in range(len(ciphertext)):
        p = ALPHABET.index(ciphertext[i])
        k = ALPHABET.index(key[i%len(key)])
        c = (p - k) % 26
        plaintext += ALPHABET[c]
    return plaintext

# # encrypted then ascii encoded, or ascii encoded then encrypted ? 

# # test in 
# with open('test.txt', 'rb') as file:
#     english_text = file.read().strip().decode('ascii')

# key = 'ydhxkxx'
# ciphertext = encrypt(english_text.upper(), key.upper())

# # print(ciphertext)






with open('Lab0.TaskII.D.txt', 'rb') as file:
    ciphertext = file.read().strip().decode('ascii')

print(len(ciphertext))
   
key_lengths, avg_iocs = analyze_ciphertext_for_key_lengths(ciphertext, 40)


# Plotting
plt.bar(key_lengths, avg_iocs)
plt.xlabel('Key Length (Period)')
plt.ylabel('Average IOC')
plt.title('Average IOC vs Key Length')
plt.xticks(range(1, len(key_lengths) + 1))  # Set x-ticks to be every key length
plt.ylim(0, 2.5)  # Set the limits of y-axis
plt.grid(True)  # Enable gridlines
plt.show()


period = 14

slices = [ciphertext[i::period] for i in range(period)]

frequencies = []
for i in range(period):
    frequencies.append([0]*26)
    for j in range(len(slices[i])):
        frequencies[i][ALPHABET.index(slices[i][j])] += 1
    for j in range(26):
        frequencies[i][j] = frequencies[i][j] / len(slices[i])
        
key = ['A']*period
for i in range(period):
    for j in range(26):
        testtable = frequencies[i][j:]+frequencies[i][:j]
        if cosangle(english_freqs_list, testtable) > 0.9:
            key[i] = ALPHABET[j]

plaintext = decrypt(ciphertext, key)
print(plaintext)
