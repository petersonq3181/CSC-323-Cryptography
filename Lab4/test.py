from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib, json
from Crypto import Random

DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

prev =  {
  "type": 0,
  "id": "e6f5b54ff5d56bd84ba6a73e7427bd301a00b5ddc617decb447c45e2f2c7ecf9",
  "nonce": "d4d08f2f264f782a1abf392ef4c5dc1e",
  "pow": "000000799651c0623c467b4082884ba80f696691977e568610fcb1b94b6720d4",
  "prev": "180d003f7cb67fa87f1cf7584b3430378543154ab973d1e3814d1814e353184f",
  "tx": {
   "type": 1,
   "input": {
    "id": "78dc1cc5b48296b1bef9aa362ea8314a1794b3630015171431d709a827115f17",
    "n": 0
   },
   "sig": "86bb3ca7e1fe7659a64c9bc26ce0a1ce6e721497dd8542f8f9ac00396a45e939d0df050f1a772b920043a05e31e4a436",
   "output": [
    {
     "value": 5,
     "pub_key": "2a3332b42e28499bcc8283fa55648a1679c0b2793ca1005139c321bd0e0d82c144180435b24afff61754b8ab32afadc2"
    },
    {
     "value": 45,
     "pub_key": "9e46b03be11b4e64aefb3b26a85bb77105614a56c77a026a7d469de01f13d29426adf2946f1d58171b16c86eff37a3fe"
    },
    {
     "value": 50,
     "pub_key": "9e46b03be11b4e64aefb3b26a85bb77105614a56c77a026a7d469de01f13d29426adf2946f1d58171b16c86eff37a3fe"
    }
   ]
  }
}

block = {'type': 0, 'id': '91a0aa419952c57a6565ca541624e32c42c094af14250341e4678fbfc511d73a', 'nonce': '0553a308632631c0f06791530c86f809', 'pow': '0000003ad9682742eb55cffca80157345b2f2ce966c8cb33923c4dc71fba2692', 'prev': 'e6f5b54ff5d56bd84ba6a73e7427bd301a00b5ddc617decb447c45e2f2c7ecf9', 'tx': {'type': 1, 'input': {'id': 'e6f5b54ff5d56bd84ba6a73e7427bd301a00b5ddc617decb447c45e2f2c7ecf9', 'n': 2}, 'sig': 'f20ffed21d5a2782c11009e2bbc74c30d27db32a9c3c896779fccc7623eefb6f6939903995fde7e0ece074a2d7b6ef0d', 'output': [{'value': '50', 'pub_key': '75fa6f7d6263203194ed9c9111ec07c643fcdd9643507c0fdc39e2fdea6b17dd760cc9822f35688a8fdcdd1bc6c0f6a0'}, {'value': 50, 'pub_key': '75fa6f7d6263203194ed9c9111ec07c643fcdd9643507c0fdc39e2fdea6b17dd760cc9822f35688a8fdcdd1bc6c0f6a0'}]}}


def mine_transaction(utx, prev):
    nonce = Random.new().read(AES.block_size).hex()
    i = 0
    while( int( hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') +
    prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest(), 16) > DIFFICULTY):

        i += 1
        if i % 100000 == 0:
            print('still mining')
        nonce = Random.new().read(AES.block_size).hex()
    pow = hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') +
    prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest()
    return pow, nonce

print(type(prev))
print(type(block['tx']))


gg = json.dumps(prev, sort_keys=True)
print(type(gg), gg)

print(type(json.dumps(block['tx'], sort_keys=True)), json.dumps(block['tx'], sort_keys=True))

pow, nonce = mine_transaction(json.dumps(block['tx'], sort_keys=True), json.dumps(prev, sort_keys=True))
print(pow, nonce)

