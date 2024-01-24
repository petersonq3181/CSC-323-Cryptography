from lab0 import base642bytes, xor_strings, getIOC
from matplotlib import plt

# Task II. C. Multi-byte XOR
# plaintext --> plaintext ascii encoded --> XOR --> ciphertext --> base64 encoded --> ciphertext 
# ciphertext --> base64 decode --> ciphertext --> XOR --> plaintext ascii encoded --> ascii decode --> plaintext 
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

potentials.sort(key=lambda x: abs(x[1] - 1.7))
potentials = potentials[:20]

for text, ioc, key in potentials:
    print(f"Decrypted text: {text}, Key: {key}, IOC: {ioc}")


