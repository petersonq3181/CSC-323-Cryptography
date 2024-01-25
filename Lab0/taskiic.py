from lab0 import base642bytes
import matplotlib.pyplot as plt


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

def index_of_coincidence(bytes_seq):
    counts = [0] * 256
    total = len(bytes_seq)

    if total <= 1:
        return 0

    for byte in bytes_seq:
        counts[byte] += 1

    numer = sum(count * (count - 1) for count in counts)
    return numer / (total * (total - 1))


# Task II. C. Multi-byte XOR
# plaintext --> plaintext ascii encoded --> XOR --> ciphertext --> base64 encoded --> ciphertext 
# ciphertext --> base64 decode --> ciphertext --> XOR --> plaintext ascii encoded --> ascii decode --> plaintext 
with open('Lab0.TaskII.C.txt', 'rb') as file:
    ciphertext = base642bytes(file.read().strip())

print(len(ciphertext))

key_lengths, avg_iocs = analyze_ciphertext_for_key_lengths(ciphertext, 30)

for i in range(len(key_lengths)):
    print('key_length: ', key_lengths[i], '\tavg_ioc: ', avg_iocs[i])

# Plotting
plt.bar(key_lengths, avg_iocs)
plt.xlabel('Key Length (Period)')
plt.ylabel('Average IOC')
plt.title('Average IOC vs Key Length')
plt.xticks(range(1, len(key_lengths) + 1))  # Set x-ticks to be every key length
plt.ylim(0, 2.5)  # Set the limits of y-axis
plt.grid(True)  # Enable gridlines
plt.show()
