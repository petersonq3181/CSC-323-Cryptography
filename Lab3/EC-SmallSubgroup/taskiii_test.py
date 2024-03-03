import crypto

other_public = (26575165156548798546746147025597271043, 233202251361428332102415566383165517691)
other_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=other_public[0], y=other_public[1])


'''
-----
Alice (me) trying to send message to Other 
----- 
'''
msg = 'hello Amin!'

'''
- Each user generates a secret key by picking a random number (mod base_point_order,
aka 1 < X < order of the base point)
- Each user then generates a public key by multiplying the base point by their secret key.
These public keys are then published

encapsulated in the gen_keys() function 
'''
alice_private, alice_public = crypto.gen_keys()
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
