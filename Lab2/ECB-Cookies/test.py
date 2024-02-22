from Crypto.Cipher import AES
import web
from web import form
import crypto, hashlib, os

def ansix923_unpad(data):
    padding_len = data[-1]
    if padding_len < 1 or padding_len > AES.block_size:
        raise ValueError("invalid padding length")
    for byte in data[-padding_len:-1]:
        if byte != 0:
            raise ValueError("invalid padding")
    return data[:-padding_len]

def decrypt_cookie(encrypted_cookie, key):
    aes_obj = AES.new(key, AES.MODE_ECB)
    decrypted_cookie = aes_obj.decrypt(encrypted_cookie)
    unpadded_cookie = ansix923_unpad(decrypted_cookie)
    return unpadded_cookie




# master_key = os.urandom(16)
# set master_key as constant for my own testing purposes 
master_key = b'\xc9\xa3\xb6\xa1mE\xca\xfa\x82\xac\x1e\x17hL\x99\xec'


# role will always be 'user' b/c based on server logic, can't change this directly to admin 
role = 'user'

c1 = crypto.create_crypto_cookie('123456789012345', 1, role, master_key)
print('gg', c1, type(c1))
print('c1: ', type(c1.hex()), c1.hex())
print('c1 decrypted: ', decrypt_cookie(c1, master_key))

# properly set so 'admin' is at the beginning of block 1 (0 indexing)
c2 = crypto.create_crypto_cookie('12345678901admin', 2, role, master_key)
print('c2: ', c2.hex())
print('c2 decrypted: ', decrypt_cookie(bytes.fromhex(c2.hex()), master_key))


print(type(c1), c1)

combined_cookie_hex = c1.hex()[:64] + c2.hex()[32:]
combined_cookie = bytes.fromhex(combined_cookie_hex)
print('Combined Cookie Decrypted: ', decrypt_cookie(combined_cookie, master_key))

print(crypto.verify_crypto_cookie(bytes.fromhex(c2.hex()), master_key))
print(crypto.verify_crypto_cookie(combined_cookie, master_key))
