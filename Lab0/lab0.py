import base64
import binascii
from collections import Counter
import matplotlib.pyplot as plt


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
''' 
Decrypted text: Out on bail, fresh out of jail, California dreaming
Soon as I step on the scene, I'm hearing ladies screaming, Key: 127, IOC: 1.0292218824328916
'''

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


if __name__ == "__main__":
    with open('Lab0.TaskII.B.txt', 'r') as file:
        hex_strings = file.readlines()

    potentials = []

    for hex_str in hex_strings:
        byte_data = binascii.unhexlify(hex_str.strip())

        for key in range(256):  
            decrypted = xor_strings(byte_data, bytes([key]))
            try:
                plaintext = decrypted.decode('utf-8')
                ioc = getIOC(plaintext)
                if ioc > 0:  
                    potentials.append((plaintext, ioc, key))
            except UnicodeDecodeError:
                continue

    potentials.sort(key=lambda x: abs(x[1] - ioc_expected))
    top_plaintexts = potentials[:5]

    for text, ioc, key in top_plaintexts:
        print(f"Decrypted text: {text}, Key: {key}, IOC: {ioc}")
