from Crypto.Cipher import AES 
import crypto
import os
from base64 import b64decode
from base64 import b64encode
import random
from enum import Enum




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

# c1 = bitFlip(5, 4, c1)
# print('Message...      :', crypto.verify_crypto_cookie(c1, key)) 


print()
print()
print()


def xor(a, b): 
    return bytes([a_byte ^ b_byte for a_byte, b_byte in zip(a, b)])

class BitFlipper:
    def __init__(self, ciphertext, plaintext, block_size=16):
        self._ciphertext = ciphertext
        self._block_size = block_size

        if len(ciphertext) % block_size != 0:
            raise Exception("Invalid ciphertext length or block size")

        self._plaintext = plaintext
        if len(self._plaintext) != len(ciphertext):
            raise Exception("Invalid plaintext length")

    def get_plaintext(self):
        return self._plaintext

    def get_ciphertext(self):
        return self._ciphertext

    def flip(self, a, b):
        if a not in self._plaintext:
            raise Exception("Unable to find occurence of %s in plaintext" % a)
        if len(a) != len(b):
            raise Exception("Data length mismatch")

        plaintextblock = [self._plaintext[i:i + self._block_size] for i in
                          range(0, len(self._plaintext), self._block_size)]

        offset = 0
        in_block = -1
        for i in range(len(plaintextblock)):
            if a in plaintextblock[i]:
                in_block = i
                offset = plaintextblock[i].find(a)
                break

        if in_block < 1 or len(a) > self._block_size:
            raise Exception("Bit Flipping attack cannot change consecutive blocks")

        modif = xor(a, b)
        pos = (in_block-1)*self._block_size + offset

        self._ciphertext = self._ciphertext[:pos] + xor(modif, self._ciphertext[pos:pos + len(a)]) + self._ciphertext[
                                                                                                     pos + len(a):]

        return self._ciphertext

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return "<%s plaintext=%s>" % (self.__class__.__name__, self.get_plaintext())
    
class Padding(Enum):
    No = 0
    Zero = 1
    ANSI_X923 = 2
    ISO_10126 = 3
    PKCS7 = 4
    PKCS5 = 5
    ISOIEC_78164 = 6

def pad(msg, block_size, padding=Padding.Zero):
    def __random_bytes(n):
        return "".join([chr(random.randint(0, 255)) for _ in range(n)])

    if padding == Padding.PKCS5:
        block_size = 8

    pad_size = block_size - (len(msg) % block_size)
    if pad_size == 16:
        pad_size = block_size

    if padding == Padding.Zero:
        return msg + "\0" * pad_size
    elif padding == Padding.ANSI_X923:
        return msg + "\0" * (pad_size - 1) + chr(pad_size)
    elif padding == Padding.ISO_10126:
        return msg + __random_bytes(pad_size - 1) + chr(pad_size)
    elif padding == Padding.ISOIEC_78164:
        return msg + chr(0x80) + "\x00" * (pad_size - 1)
    elif padding == Padding.PKCS7:
        return msg + chr(pad_size) * pad_size
    elif padding == Padding.PKCS5:
        return msg + chr(pad_size) * pad_size

    return msg


p = 'user=aaaa&uid=1&role=user'
iv = c1[:AES.block_size]
p = iv + pad(p, AES.block_size, Padding.Zero).encode('utf-8')
print(len(p))
print(len(c1))
dolphin = BitFlipper(c1, p, block_size=AES.block_size)
dolphin.flip(b"user", b"fuck")
flipped_ciphertext = dolphin.get_ciphertext()
print("New ciphertext  :", flipped_ciphertext)


# c1 = bitFlip(5, 4, c1)
print('Message...      :', crypto.verify_crypto_cookie(flipped_ciphertext, key)) 
