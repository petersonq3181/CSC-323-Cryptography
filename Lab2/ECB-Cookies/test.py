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
print('c1: ', c1.hex())
print('c1 decrypted: ', decrypt_cookie(c1, master_key))

# properly set so 'admin' is at the beginning of block 1 (0 indexing)
c2 = crypto.create_crypto_cookie('12345678901admin', 2, role, master_key)
print('c2: ', c2.hex())
print('c2 decrypted: ', decrypt_cookie(bytes.fromhex(c2.hex()), master_key))



combined_cookie_hex = c1.hex()[:64] + c2.hex()[32:]
combined_cookie = bytes.fromhex(combined_cookie_hex)
print('Combined Cookie Decrypted: ', decrypt_cookie(combined_cookie, master_key))

print(type(bytes.fromhex(c1.hex())))
print(type(c1))

def gg(c, key):
    try:

        return crypto.verify_crypto_cookie(bytes.fromhex(c.hex()), key)
    except:
        print('fuck')
        return "","",""

a, b, c = gg(c1, master_key)
print(a, b, c)

'''
c1
b4a6532ef5db31e17b2834aa48f8b2b850dab3dadb27f5a50ad88768e51ae48e
block 0: b4a6532ef5db31e17b2834aa48f8b2b8

c2
1b5f72d2324695b3dc0edb8118c091a1410d2a8676427a1d5f862c4c42d9be6e01858a7459b743385d2c0cd40cd8eefc
0: 1b5f72d2324695b3dc0edb8118c091a1
1: 410d2a8676427a1d5f862c4c42d9be6e
2: 01858a7459b743385d2c0cd40cd8eefc

c1[0] + c2[1] = b4a6532ef5db31e17b2834aa48f8b2b8410d2a8676427a1d5f862c4c42d9be6e
'''