import crypto
import server 

other_public = (177610206659405715089668382012774040984, 199646344175385570337654575447987532017)
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

print('alice private and public:')
print(alice_private, alice_public)

# calculate shared key 
shared_key = crypto.get_shared_key(other_public_point, alice_private)
print('shared key:')
print(shared_key)

# sign w/ HMAC 
h = crypto.calculate_hmac(msg, shared_key)
print('hmac:')
print(h.hexdigest())


# reply, hmac = server.user_msg('Admin', 'hello Amin!', h.hexdigest(), alice_public.x, alice_public.y)
# print(reply)
# print(hmac)
