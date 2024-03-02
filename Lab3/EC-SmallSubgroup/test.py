import crypto


# hmac = crypto.calculate_hmac('asdf', (159317589597603284839581010503845834343, 201768302101518577742048492751200300103))
# print(hmac.hexdigest())



bob_public = (59615353590406748135717578710548358608, 122413972788214489652428834752089502199)
bob_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=bob_public[0], y=bob_public[1])


'''
-----
Alice (me) trying to send message to Bob 
----- 
'''
msg = 'hello BOB!'

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
shared_key = crypto.get_shared_key(bob_public_point, alice_private)
print('shared key:')
print(shared_key)

# sign w/ HMAC 
h = crypto.calculate_hmac(msg, shared_key)
