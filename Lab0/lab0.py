import base64


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
def score_english(s):
    freqs = {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
        'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
        'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
        'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
        'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
        'z': 0.074
    }

    s = ''.join(filter(str.isalpha, s.lower()))

    letter_counts = {letter: s.count(letter) for letter in freqs}
    letter_total = sum(letter_counts.values())

    score = sum((letter_counts[letter] / letter_total * 100 - freqs[letter]) ** 2 for letter in freqs) ** 0.5

    ioc = sum(letter_counts[letter] * (letter_counts[letter] - 1) for letter in letter_counts) / (letter_total * (letter_total - 1))

    ioc_expected = 0.0667

    ioc_score = abs(ioc - ioc_expected)

    return score + ioc_score







if __name__ == "__main__": 
    # ----- Task I. testing 
    byte_string = b"Hello, world!"
    hex_string = bytes2hex(byte_string)
    print("Hex Encoded:", hex_string)
    decoded_bytes = hex2bytes(hex_string)
    print("Decoded Bytes:", decoded_bytes)

    base64_str = bytes2base64(byte_string)
    print("Base64 Encoded:", base64_str)
    decoded_bytes = base642bytes(base64_str)
    print("Decoded Bytes:", decoded_bytes)

    # ----- Task II. testing 
    res = xor_strings(b'hello', b'key')
    print("xor_strings result:", res)


    # test encoding 
    mystr = b"This is definitely an English Plaintext"
    mystr = xor_strings(mystr, bytes([1]))
    mystr = bytes2hex(mystr)
    print(mystr)
    
    

  

    with open('testB.txt', 'r') as file:
        hex_strings = file.read().splitlines()

    top_scores = []

    for hex_str in hex_strings:
        byte_str = hex2bytes(hex_str)

        for key in range(256):
            key_byte = bytes([key])
            xored_result = xor_strings(byte_str, key_byte)
            xored_english = bytes2base64(xored_result)
            score = score_english(xored_english)

            # Add the score, plaintext, and key to the list
            top_scores.append((score, xored_english, key_byte))

            # Keep only the top 100 scores
            top_scores = sorted(top_scores, reverse=False, key=lambda x: x[0])[:512]

    # Print the top 100 scores and their associated plaintexts and keys
    for score, plaintext, key in top_scores:
        print(f"Score: {score}, Plaintext: {plaintext}, Key: {bytes2hex(key)}")

