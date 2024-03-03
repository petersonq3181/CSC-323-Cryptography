import crypto
import requests

url = 'http://0.0.0.0:8080/'

curve = crypto.curve 
base_point = crypto.base_point
bp_order = crypto.bp_order

point = crypto.EccAlgPoint(curve=crypto.curve, x=16349894185180983439102154383611486412, y=224942997200586455214256137069604954919)

# ----- get unique set of points (8 total b/c it's order 8)
acc = []
for i in range(0, 1000):
    try:
        acc.append((crypto.EccPoint.__mul__(point, i).x, crypto.EccPoint.__mul__(point, i).y))
    except: 
        print(crypto.EccPoint.__mul__(point, i).__str__())

# note: prints 7 elements instead of 8 b/c missing the origin 
ps = set(acc)
unique_points = []
for i, p in enumerate(ps):
    print(i, p)
    unique_points.append(crypto.EccAlgPoint(curve=crypto.curve, x=p[0], y=p[1]))

# ----- talk to admin 
admin_public = (5857514870807797964012693241104587497, 193396171777314066986828010215107005104)
admin_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=admin_public[0], y=admin_public[1])

usr = 'Admin'
msg = 'hello admin!!' 

my_private, my_public = crypto.gen_keys()
# my_public = unique_points[0] # TODO 
print(f'my private and public:\n\t {my_private}\n\t {my_public}\n')

shared_key = crypto.get_shared_key(admin_public_point, my_private)
print(f'shared key:\n\t {shared_key}\n')

hmac = crypto.calculate_hmac(msg, shared_key)
print(f'hmac:\n\t {hmac.hexdigest()}')

# reply, gen_hmac = server.user_msg(usr, msg, 
#     given_hmac=hmac.hexdigest(), 
#     pub_key_x=str(my_public.x), 
#     pub_key_y=str(my_public.y))
# print(f'reply:\n\t{reply} \ngen_hmac:\n\t {gen_hmac}')

with requests.Session() as session:
    data = {
        'recipient': usr,
        'message': msg,
        'hmac': hmac.hexdigest(),
        'pkey_x': str(my_public.x),
        'pkey_y': str(my_public.y)
    }
    res = session.post(url + 'submit', data=data)
    print(res)
    print(res.text)
