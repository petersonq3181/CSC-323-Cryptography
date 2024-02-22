import crypto
import os
from base64 import b64decode
from base64 import b64encode



def bitFlip(pos, bit, raw):
    list1 = list(raw)
    list1[pos] = list1[pos] ^ bit
    raw = bytes(list1)
    return bytes(raw)

# key = os.urandom(16)
key = b'\x8c\xec(\xcf\xde\x04\xb4\x8e\x93\xca\xbe\x89[\xeb\xfd\xc5'

# p1 = user=aaaa&uid=1&role=user 
c1 = crypto.create_crypto_cookie('aaaa', '1', 'user', key)
print(type(c1), type(c1.hex()))
print(c1.hex())
p1 = crypto.verify_crypto_cookie(c1, key)
print(p1)


c1 = bitFlip(5, 4, c1)
print('Message...      :', crypto.verify_crypto_cookie(c1, key)) 