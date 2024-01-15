import base64
from collections import Counter
from langdetect import detect



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
# attempted to write an IOC calculator for english -- ended up using detect from langdetect
alphabet = "abcdefghijklmnopqrstuvwxyz"

def countLetters(s):
    return sum(1 for c in s if c in alphabet)

def getIOC(s):
    s = s.lower()
    counts = Counter(s)
    total = 0
    for ni in counts.values():
        total += ni * (ni - 1)

    n = countLetters(s)
    total = float(total) / ((n * (n - 1)) / 26)
    return total






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

    print(detect("This is english"))
    print(detect("Also english ha used to put the speaker on the desk"))
    print(detect("df cjkdsij ri3bjkcnkj i nkni nli2 kd"))
    print(detect("asdff ksjdlvie 3 ind ij "))


  

    with open('Lab0.TaskII.B.txt', 'r') as file:
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

