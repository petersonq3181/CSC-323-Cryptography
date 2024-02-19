from Crypto.Cipher import AES
import base64
from taski import pad, unpad

def cbc_encrypt(plaintext, key, iv):
    assert len(iv) == AES.block_size

    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(plaintext, AES.block_size)
    
    prev_block = iv
    ciphertext = b''

    for i in range(0, len(padded), AES.block_size):
        block = padded[i:i+AES.block_size]
        block = bytes([x ^ y for x, y in zip(block, prev_block)])
        encrypted_block = cipher.encrypt(block)
        ciphertext += encrypted_block
        prev_block = encrypted_block

    return ciphertext

def cbc_decrypt(ciphertext, key, iv):
    assert len(iv) == AES.block_size

    if len(ciphertext) % AES.block_size != 0:
        raise ValueError('ciphertext is not a multiple of the block size')

    cipher = AES.new(key, AES.MODE_ECB)
    prev_block = iv
    padded = b''

    for i in range(0, len(ciphertext), AES.block_size):
        block = ciphertext[i:i+AES.block_size]
        decrypted_block = cipher.decrypt(block)
        padded += bytes([x ^ y for x, y in zip(decrypted_block, prev_block)])
        prev_block = block

    return unpad(padded, AES.block_size)

with open('Lab2.TaskIII.A.txt', 'r') as file:
    encrypted_data_base64 = file.read()

encrypted_data = base64.b64decode(encrypted_data_base64)

key = b'MIND ON MY MONEY'
iv = b'MONEY ON MY MIND'

decrypted_data = cbc_decrypt(encrypted_data, key, iv)

print(decrypted_data)
