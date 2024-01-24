import base64
import binascii
from collections import Counter
import itertools
from langdetect import detect
import matplotlib.pyplot as plt
import numpy as np



# Task I. A. Implement Common Encoders & Decoders
def bytes2hex(byte_string):
    return byte_string.hex()

def hex2bytes(hex_string):
    return bytes.fromhex(hex_string)

def base642bytes(base64_encoded):
    return base64.b64decode(base64_encoded)

def bytes2base64(s):
    return base64.b64encode(s)


# Task II. A. Implement XOR
def xor_strings(s, key):
    repeated_key = (key * (len(s) // len(key) + 1))[:len(s)]
    return bytes([input_byte ^ key_byte for input_byte, key_byte in zip(s, repeated_key)])


# Task II. B. Single-byte XOR
# Decrypted text: Out on bail, fresh out of jail, California dreaming
# Soon as I step on the scene, I'm hearing ladies screaming, Key: 127, IOC: 1.0292218824328916

# IC expected for English is 1.73
# English typically falls in range 1.5 to 2.0
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

def taskIIB():
    with open('Lab0.TaskII.B.txt', 'r') as file:
        hex_strings = file.readlines()

    potentials = []

    for hex_str in hex_strings:
        byte_data = binascii.unhexlify(hex_str.strip())

        for key in range(256):  
            decrypted = xor_strings(byte_data, bytes([key]))
            try:
                plaintext = decrypted.decode('utf-8')
                print('ayoo: ', type(plaintext), plaintext)
                ioc = getIOC(plaintext)
                if ioc > 0:  
                    potentials.append((plaintext, ioc, key))
            except UnicodeDecodeError:
                continue

    potentials.sort(key=lambda x: abs(x[1] - ioc_expected))
    top_plaintexts = potentials[:5]

    for text, ioc, key in top_plaintexts:
        print(f"Decrypted text: {text}, Key: {key}, IOC: {ioc}")

# Task II. C. Multi-byte XOR
# plaintext --> plaintext ascii encoded --> XOR --> ciphertext --> base64 encoded --> ciphertext 
# ciphertext --> base64 decode --> ciphertext --> XOR --> plaintext ascii encoded --> ascii decode --> plaintext 
def taskIIC():
    with open('Lab0.TaskII.C.txt', 'rb') as file:
        encrypted_data = base642bytes(file.read().strip())
   
    keys = []
    for byte1 in range(256):
        key1 = bytes([byte1])
        keys.append(key1)

        for byte2 in range(256):
            key2 = bytes([byte1, byte2])
            keys.append(key2)

            # for byte3 in range(256):
            #     key3 = bytes([byte1, byte2, byte3])
            #     keys.append(key3)

    potentials = []
    scores = []

    for key in keys: 
        decrypted = xor_strings(encrypted_data, key)

        try:
            # plaintext = bytes2base64(decrypted)
            plaintext = decrypted.decode('ascii', errors='ignore')
            
            score = getIOC(plaintext)
            scores.append(score)

            if score > 0.5:
                potentials.append((plaintext, score, key))
        except UnicodeDecodeError:
            continue 

    print(len(potentials))
    plt.hist(scores, bins=50, alpha=0.75, color='b')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title('Distribution of Scores')
    plt.grid(True)
    plt.show()

    potentials.sort(key=lambda x: abs(x[1] - ioc_expected))
    potentials = potentials[:20]

    for text, ioc, key in potentials:
        print(f"Decrypted text: {text}, Key: {key}, IOC: {ioc}")

# Task II. D. Vigenère Cipher
def temp():
    return 


if __name__ == "__main__": 
    # # ----- Task I. testing 
    # byte_string = b"Hello, world!"
    # hex_string = bytes2hex(byte_string)
    # print("Hex Encoded:", hex_string)
    # decoded_bytes = hex2bytes(hex_string)
    # print("Decoded Bytes:", decoded_bytes)

    # base64_str = bytes2base64(byte_string)
    # print("Base64 Encoded:", base64_str)
    # decoded_bytes = base642bytes(base64_str)
    # print("Decoded Bytes:", decoded_bytes)

    # # ----- Task II. testing 
    # res = xor_strings(b'hello', b'key')
    # print("xor_strings result:", res)

    taskIIC()
