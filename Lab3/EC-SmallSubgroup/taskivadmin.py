import crypto

# paste in Bob's
other_public = (197081780250990887425827005688240856386, 66852806643506563351917301897024861017)
other_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=other_public[0], y=other_public[1])

# paste in Admin's 
my_public = (183461775136947200127959946100322523072, 37682483540134556834827127697165390887)
X = my_public[0]
Y = my_public[1]
# my_private, my_public = crypto.gen_keys()
my_private = 4524555557526241377017376195840685006

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

