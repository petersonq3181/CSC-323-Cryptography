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

# testing w/ TaskII.A.txt 
key = b"CALIFORNIA LOVE!"
encoded = read_and_decode('Lab2.TaskII.A.txt')
decrypted = ecb_decrypt(key, encoded)
print(decrypted.decode('utf-8'))
