import binascii
import base64
from collections import Counter
import itertools

# Task II. A. Implement XOR
def xor_strings(s, key):
    repeated_key = (key * (len(s) // len(key) + 1))[:len(s)]
    return bytes([input_byte ^ key_byte for input_byte, key_byte in zip(s, repeated_key)])

# Scoring function (you can reuse this)
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

# Task II. C. Decrypt XOR'd and base64 encoded message
def taskIIC():
    with open('Lab0.TaskII.C.txt', 'r') as file:
        base64_encoded = file.read().strip()

    encrypted_data = base64.b64decode(base64_encoded)

    potentials = []

    for key_len in range(1, 2):  # Try different key lengths
        for key_candidate in itertools.product(range(256), repeat=key_len):
            key = bytes(key_candidate)
            decrypted = xor_strings(encrypted_data, key)
            
            try:
                plaintext = decrypted.decode('utf-16')
                ioc = getIOC(plaintext)
                print(ioc)
                if ioc > 1.5 and ioc < 2.0:  # You can adjust the IOC range as needed
                    potentials.append((plaintext, ioc, key))
            except UnicodeDecodeError:
                continue

    potentials.sort(key=lambda x: abs(x[1] - 1.73))
    top_plaintexts = potentials[:5]

    for text, ioc, key in top_plaintexts:
        print(f"Decrypted text: {text}, Key: {key}, IOC: {ioc}")

# Call the function to decrypt the message
taskIIC()
