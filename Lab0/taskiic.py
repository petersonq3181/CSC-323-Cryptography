from lab0 import base642bytes, xor_strings
import matplotlib.pyplot as plt

# avg ioc for each group of ciphertext, when split for various repeating key lengths 
def analyze_ciphertext_for_key_lengths(ciphertext, max_key_length):
    key_lengths = []
    avg_iocs = [] 
    for key_length in range(1, max_key_length + 1):
        groups = [ciphertext[i::key_length] for i in range(key_length)]
        group_iocs = [bytes_index_of_coincidence(group) for group in groups]
        avg_ioc = sum(group_iocs) / len(group_iocs)

        key_lengths.append(key_length)
        avg_iocs.append(avg_ioc)
    return key_lengths, avg_iocs

# IOC for each possible byte out of the 256 possibilities 
def bytes_index_of_coincidence(bytes_seq):
    counts = [0] * 256
    total = len(bytes_seq)

    if total <= 1:
        return 0

    for byte in bytes_seq:
        counts[byte] += 1

    numer = sum(count * (count - 1) for count in counts)
    return numer / (total * (total - 1))

# to get key_length-number of ciphertexts, of the original divided and concatenated 
def transpose_blocks(ciphertext, key_length):
    blocks = [ciphertext[i:i + key_length] for i in range(0, len(ciphertext), key_length)]

    transposed_blocks = [[] for _ in range(key_length)]
    for block in blocks:
        for i in range(len(block)):
            transposed_blocks[i].append(block[i])

    return transposed_blocks

def score_text(text):
    english_letter_freq = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228, 
                           'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025, 
                           'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 
                           's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 
                           'y': 0.01974, 'z': 0.00074, ' ': 0.13000} 

    return sum([english_letter_freq.get(chr(byte), 0) for byte in text.lower()])

# Task II. C. Multi-byte XOR
# plaintext --> plaintext ascii encoded --> XOR --> ciphertext --> base64 encoded --> ciphertext 
# ciphertext --> base64 decode --> ciphertext --> XOR --> plaintext ascii encoded --> ascii decode --> plaintext 
with open('Lab0.TaskII.C.txt', 'rb') as file:
    ciphertext = base642bytes(file.read().strip())

print(len(ciphertext))

key_lengths, avg_iocs = analyze_ciphertext_for_key_lengths(ciphertext, 30)

# # Plotted for the purpose of finding the likely key length; found to be 5 
# # Plotting
# plt.bar(key_lengths, avg_iocs)
# plt.xlabel('Key Length (Period)')
# plt.ylabel('Average IOC')
# plt.title('Average IOC vs Key Length')
# plt.xticks(range(1, len(key_lengths) + 1))  # Set x-ticks to be every key length
# plt.ylim(0, 2.5)  # Set the limits of y-axis
# plt.grid(True)  # Enable gridlines
# plt.show()
    
# or likely multiple of 5 
key_length = 5 

transposed_blocks = transpose_blocks(ciphertext, key_length)
transposed_blocks = [bytes(block) for block in transposed_blocks]

# does single-byte xor decryption testing on each transposed block 
# keeps track of best score of text (close to english) and keeps key w/ best score 
key = []
for block in transposed_blocks:
    best_score = 0
    best_key = None
    for potential_key in range(256):
        decrypted_block = xor_strings(block, bytes([potential_key]))
        score = score_text(decrypted_block)
        if score > best_score:
            best_score = score
            best_key = potential_key
    key.append(best_key)

key = bytes(key)
decrypted = xor_strings(ciphertext, key)

try:
    plaintext = decrypted.decode('ascii')
    print(f"Decrypted text: {plaintext}")
    print("Key: ", key)
except UnicodeDecodeError:
    print("Decryption resulted in non-ASCII characters")

'''
Decrypted text: One, two, three and to the fo'
Snoop Doggy Dogg and Dr. Dre is at the door
Ready to make an entrance so back on up
(Cause you know we're about to rip stuff up) 
Give me the microphone first so I can bust like a bubble
Compton and Long Beach together now you know you in trouble
Ain't nothing but a G thang, baby 
Two loc'ed out dudes so we're crazy
Death Row is the label that pays me
Unfadeable so please don't try to fade this

Key:  b'ayÑxb5Ñxe7Z'
'''