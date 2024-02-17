from Crypto.Cipher import AES
import base64
from taski import pad, unpad

def ecb_encrypt(key, plaintext):
    if len(key) != 16:
        raise ValueError("key must be 128 bits (16 bytes)")

    padded = pad(plaintext, AES.block_size)

    cipher = AES.new(key, AES.MODE_ECB)

    ciphertext = cipher.encrypt(padded)
    return ciphertext

def ecb_decrypt(key, ciphertext):
    if len(key) != 16:
        raise ValueError("key must be 128 bits (16 bytes)")

    if len(ciphertext) % AES.block_size != 0:
        raise ValueError("ciphertext is not a multiple of the block size")

    cipher = AES.new(key, AES.MODE_ECB)

    decrypted_padded = cipher.decrypt(ciphertext)

    try:
        plaintext = unpad(decrypted_padded, AES.block_size)
    except ValueError as e:
        raise ValueError("padding is incorrect or corrupted")

    return plaintext

def read_and_decode(fn):
    with open(fn, 'r') as file:
        encoded = file.read()
        decoded = base64.b64decode(encoded)
        return decoded

# --- Implement ECB Mode
key = b"CALIFORNIA LOVE!"
encoded = read_and_decode('Lab2.TaskII.A.txt')
decrypted = ecb_decrypt(key, encoded)
print(decrypted.decode('utf-8'))



def detect_ecb(ciphertext, block):
    blocks = [ciphertext[i:i + block] for i in range(0, len(ciphertext), block)]
    num_unique = len(set(blocks))
    return len(blocks) != num_unique

def find_ecb(fn):
    with open(fn, 'r') as file:
        lines = file.readlines()

    # ignoring the first 54 bytes which are the BMP header
    for i, line in enumerate(lines):
        ciphertext = bytes.fromhex(line.strip())[54:]

        # with open(f"ecb_encrypted_{i}.bmp", 'wb') as image_file:
        #     image_file.write(bytes.fromhex(line.strip()))

        if detect_ecb(ciphertext, AES.block_size):
            return i, line.strip()
    return None, None

# --- Identify ECB Mode
ecb_idx, ecb_line = find_ecb('Lab2.TaskII.B.txt')

if ecb_line is not None:
    print(f"ECB encrypted line is at index {ecb_idx}")
    with open('ecb_encrypted_image.bmp', 'wb') as image_file:
        image_file.write(bytes.fromhex(ecb_line))
else:
    print("No ECB encrypted image found")

