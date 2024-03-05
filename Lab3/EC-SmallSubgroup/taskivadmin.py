import crypto

# paste in Bob's
other_public = (67962902483891606150910003455789427653, 228558958161179103215723740427538994859)
other_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=other_public[0], y=other_public[1])

# paste in Admin's, and Admin's private calculated from Chinese Remainder Theorem (in test.py; after taskiv.py)
my_public = (174631127780235583597992824516490167288, 88449913412994293846060964510401358900)
X = my_public[0]
Y = my_public[1]
# my_private, my_public = crypto.gen_keys()
my_private = 10358729598232529341521219605103477246

'''
-----
Alice (me) trying to send message to Other 
----- 
'''
msg = 'hello bob'



my_public = crypto.EccAlgPoint(curve=crypto.curve, x=X, y=Y)

print(f'my private and public:\n\t {my_private}\n\t {my_public}\n')

# calculate shared key 
shared_key = crypto.get_shared_key(other_public_point, my_private)
print(f'shared key:\n\t {shared_key}\n')

# sign w/ HMAC 
h = crypto.calculate_hmac(msg, shared_key)
print(f'hmac:\n\t {h.hexdigest()}\n\n\n')

