import base64
from itertools import cycle, combinations

def base64_decode(data):
    """Decode base64 data."""
    return base64.b64decode(data)

def xor_decrypt(ciphertext, key):
    """Decrypt the ciphertext by XORing with a key."""
    return bytes(c ^ k for c, k in zip(ciphertext, cycle(key)))

def score_text(text):
    """Score the text based on the frequency of common English characters."""
    # Frequencies of common English characters (including space)
    freqs = {'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 
             'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153, 
             'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507, 
             'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 
             'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 
             'z': 0.074, ' ': 13.000}

    return sum(freqs.get(chr(byte).lower(), 0) for byte in text)

def find_key_and_decrypt(encoded_data):
    """Find the key and decrypt the encoded data."""
    decoded_data = base64_decode(encoded_data)
    max_score = 0
    best_text = None
    best_key = None
    
    # Trying keys of different lengths (up to 64)
    for key_length in range(1, 3):
        for key in combinations(range(256), key_length):
            decrypted_text = xor_decrypt(decoded_data, key)
            current_score = score_text(decrypted_text)

            if current_score > max_score:
                max_score = current_score
                best_text = decrypted_text
                best_key = key

    return best_text, best_key

# The encoded message
encoded_message = ("LhfQy3oVDtrLehURx4I/QRjbg3oVFpWTMgRZ04h9ayrbiDURWfGIPQYAlaM1Bh6VhjQFWfGVdEE9"
                   "x4J6CAqVhi5BDd2CegUW2pVQMxzUgyNBDdrHNwAS0Mc7D1nQiS4TGNuEP0EK2sc4ABrexzUPWcCX"
                   "UEk61JIpBFnMiC9BEtuILUEO0MAoBFnUhTUUDZWTNUEL3Jd6Eg3AgTxBDMXOems+3JE/QRTQxy4J"
                   "HJWKMwIL2pcyDhfQxzwIC8aTehIWla56AhjbxzgUCsHHNggS0Mc7QRvAhTgNHL+kNQwJwYg0QRjb"
                   "g3otFtuAeiMc1IQyQQ3agD8VEdCVeg8WwscjDgyVjDQODpWeNRRZ3Il6FQvakjgNHL+mMw9ewcc0"
                   "Dg3djjQGWdeSLkEYlaB6FRHUiT1NWdeGOBhZv7MtDlnZiDlGHNHHNRQNlYMvBRzGxykOWcKCfRMc"
                   "lYQoAAPM7R4EGMGPejMWwsczElnBjz9BFdSFPw1ZwY87FVnFhiMSWdiCUDQX04Y+BBjXiz9BCtrH"
                   "Kg0c1JQ/QR3aiX0VWcGVI0EN2sc8AB3Qxy4JEMbt")

# Find the key and decrypt the message
decrypted_text, decryption_key = find_key_and_decrypt(encoded_message)

# Print the results
print(decrypted_text, decryption_key)
