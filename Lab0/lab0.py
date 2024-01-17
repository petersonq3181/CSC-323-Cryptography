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
# TODO detect() is too slow, need to flush out my own scoring funtion 
alphabet = "abcdefghijklmnopqrstuvwxyz"

def countLetters(s):
    return sum(1 for c in s if c in alphabet)

# IC expected for English is 1.73
# English typically falls in range 1.5 to 2.0
def getIOC(s):
    N = len(s)
    c = 26 

    s = ''.join([c for c in s if c.isalpha()])
    s = s.lower()

    counts = Counter(s)
    total = sum(ni * (ni - 1) for ni in counts.values())

    IOC = float(total) / ((N * (N - 1)) / c)
    return IOC






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

    print(getIOC("This is english"))
    print(getIOC("Also english used to put the speaker on the desk"))
    print(getIOC("df cjkdsij ri3bjkcnkj i nkni nli2 kd"))
    print(getIOC("asdff ksjdlvie 3 ind ij "))


  

    # with open('Lab0.TaskII.B.txt', 'r') as file:
    #     hex_strings = file.read().splitlines()

    # top_scores = []

    # gg = 0
    # for hex_str in hex_strings:
    #     byte_str = hex2bytes(hex_str)

    #     for key in range(256):
    #         gg += 1 
    #         print('gg: ', gg)

    #         key_byte = bytes([key])
    #         xored_result = xor_strings(byte_str, key_byte)

    #         plaintext = xored_result.decode('ASCII', errors='ignore')
    #         if detect(plaintext) == 'en': 
    #             top_scores.append((plaintext, key_byte))

    # for plaintext, key in top_scores:
    #     print(f"Plaintext: {plaintext}, Key: {bytes2hex(key)}")

