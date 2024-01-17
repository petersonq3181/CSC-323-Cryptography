import base64
import binascii
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
# Decrypted text: Out on bail, fresh out of jail, California dreaming
# Soon as I step on the scene, I'm hearing ladies screaming, Key: 127, IOC: 1.0292218824328916
alphabet = "abcdefghijklmnopqrstuvwxyz"

def countLetters(s):
    return sum(1 for c in s if c in alphabet)

# IC expected for English is 1.73
# English typically falls in range 1.5 to 2.0
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

def closestScores(scores, target, n):
    scores = sorted(scores, key=lambda x: abs(x - target))    
    return scores[:n]

def xor_with_key(byte_data, key):
    return bytes([b ^ key for b in byte_data])




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


  

    with open('Lab0.TaskII.B.txt', 'r') as file:
        hex_strings = file.read().splitlines()


    # # testing 
    # byte_str = hex2bytes(hex_strings[0])
    # print('here:')
    # print(byte_str)
    # key_byte = bytes([0])
    # print(key_byte)
    # xored_result = xor_strings(byte_str, key_byte)
    # print(xored_result)
    # plaintext = xored_result.decode('utf-8') #.decode('ASCII')
    # print(plaintext)
    # score = getIOC(plaintext)
    # print(score)



    

    with open('Lab0.TaskII.B.txt', 'r') as file:
        hex_strings = file.readlines()

    typical_english_ioc = 1.73  # Approximate IOC value for English text
    possible_plaintexts = []

    for hex_str in hex_strings:
        byte_data = binascii.unhexlify(hex_str.strip())

        for key in range(256):  # Trying all possible single-byte keys
            decrypted = xor_with_key(byte_data, key)
            try:
                decoded = decrypted.decode('utf-8')
                ioc = getIOC(decoded)
                if ioc > 0:  # Filtering non-zero IOC values
                    possible_plaintexts.append((decoded, ioc, key))
            except UnicodeDecodeError:
                continue

    # Sort the possible plaintexts by their IOC score, closer to typical English IOC
    possible_plaintexts.sort(key=lambda x: abs(x[1] - typical_english_ioc))

    # Select the top 10 plaintexts
    top_plaintexts = possible_plaintexts[:10]

    # Print the top 10 plaintexts along with their keys
    for text, ioc, key in top_plaintexts:
        print(f"Decrypted text: {text}, Key: {key}, IOC: {ioc}")
