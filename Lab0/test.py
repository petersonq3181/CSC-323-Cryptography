import base64
import string
import matplotlib.pyplot as plt


# Define expected English letter frequencies
expected_frequencies = {
    'a': 0.0817, 'b': 0.0149, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270, 'f': 0.0223,
    'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015, 'k': 0.0077, 'l': 0.0403,
    'm': 0.0241, 'n': 0.0675, 'o': 0.0751, 'p': 0.0193, 'q': 0.0010, 'r': 0.0599,
    's': 0.0633, 't': 0.0906, 'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
    'y': 0.0197, 'z': 0.0007,
}

def score_text(text):
    """
    Calculate a score for the likelihood that the given text is English plaintext.
    """
    text = text.lower()
    score = 0
    total_chars = len(text)
    
    for letter in string.ascii_lowercase:
        observed_frequency = text.count(letter) / total_chars
        expected_frequency = expected_frequencies[letter]
        score += abs(observed_frequency - expected_frequency)
    
    return score

def xor_bytes(input_bytes, key_bytes):
    """
    Perform XOR operation between input bytes and a key, repeating the key if necessary.
    """
    key_length = len(key_bytes)
    return bytes([input_bytes[i] ^ key_bytes[i % key_length] for i in range(len(input_bytes))])

# Load the base64-encoded ciphertext from the file
with open('Lab0.TaskII.C.txt', 'rb') as file:
    base64_ciphertext = file.read()

# Decode the base64 ciphertext to obtain the actual ciphertext
ciphertext = base64.b64decode(base64_ciphertext)

# Initialize variables to store the best key and plaintext
potentials = []

for key_length in range(1, 256):
    for key_value in range(256):
        key = bytes([key_value] * key_length) 
        decrypted_text = xor_bytes(ciphertext, key)
        score = score_text(decrypted_text.decode('utf-8', errors='ignore'))
        
        # if score < 0.75:
        plaintext = decrypted_text.decode('utf-8', errors='ignore')
        potentials.append((score, key, plaintext))


# # Plot the distribution of scores
# scores = [score for score, _, _ in potentials]
# plt.hist(scores, bins=50, alpha=0.75, color='b')
# plt.xlabel('Score')
# plt.ylabel('Frequency')
# plt.title('Distribution of Scores')
# plt.grid(True)
# plt.show()

# Print the potential decryptions
potentials.sort(key=lambda x: abs(x[0] - 0))
top_plaintexts = potentials[:30]
for ioc, key, text in top_plaintexts:
    print(f"Decrypted text: {text}, Key: {key}, IOC: {ioc}")

print(len(potentials))