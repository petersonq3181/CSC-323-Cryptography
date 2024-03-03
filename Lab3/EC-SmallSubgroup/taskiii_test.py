import crypto
import server 

other_public = (78765447383511211333636960546902742062, 47558240522898893543186101077255029345)
other_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=other_public[0], y=other_public[1])


'''
-----
Alice (me) trying to send message to Other 
----- 
'''
msg = 'hello admin'

'''
- Each user generates a secret key by picking a random number (mod base_point_order,
aka 1 < X < order of the base point)
- Each user then generates a public key by multiplying the base point by their secret key.
These public keys are then published

encapsulated in the gen_keys() function 
'''
alice_private, alice_public = crypto.gen_keys()

alice_public = crypto.EccAlgPoint(curve=crypto.curve, x=16349894185180983439102154383611486412, y=224942997200586455214256137069604954919)

# alice_public = crypto.EccPoint.__mul__(alice_public, 4)

print('alice private and public:')
print(alice_private, alice_public)



'''
307635a904ea742cc5221bb35dc013566e2f243913e7fface7377f9307b59fcb

46a4b6cca4e558a936c17bd02dcae93e9a6ceaec83e7e3da6612201c1d4bb2a2

mul0: 
ba6e39e4c1b824bf865acb8a1a8293428d16048ac680ce5f94fa76a843368652

mul1:
46a4b6cca4e558a936c17bd02dcae93e9a6ceaec83e7e3da6612201c1d4bb2a2

mul2: 
ba6e39e4c1b824bf865acb8a1a8293428d16048ac680ce5f94fa76a843368652

mul3: 
46a4b6cca4e558a936c17bd02dcae93e9a6ceaec83e7e3da6612201c1d4bb2a2

mul4: 
ba6e39e4c1b824bf865acb8a1a8293428d16048ac680ce5f94fa76a843368652

'''

# calculate shared key 
shared_key = crypto.get_shared_key(other_public_point, alice_private)
print('shared key:')
print(shared_key)

# sign w/ HMAC 
h = crypto.calculate_hmac(msg, shared_key)
print('hmac:')
print(h.hexdigest())


reply, hmac = server.user_msg('Admin', 'hello Amin!', h.hexdigest(), alice_public.x, alice_public.y)
print(reply)
print(hmac)
