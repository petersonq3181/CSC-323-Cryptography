import crypto
import requests
from bs4 import BeautifulSoup

url = 'http://0.0.0.0:8080/'

curve = crypto.curve 
base_point = crypto.base_point
bp_order = crypto.bp_order

X = 16349894185180983439102154383611486412
Y = 224942997200586455214256137069604954919
point = crypto.EccAlgPoint(curve=crypto.curve, x=X, y=Y)

# origin = crypto.EccInfPoint(curve=curve)

# ----- get unique set of points (8 total b/c it's order 8)
acc = []
for i in range(1, 100):
    gg = crypto.EccPoint.__mul__(point, i)
    acc.append(gg)

unique_points = set(acc)
for i, p in enumerate(unique_points):
    print(i, p)

# # ----- talk to admin 
# admin_public = (121827448578773748305120722784972190963, 112548776019462441772570757329996227364)
# admin_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=admin_public[0], y=admin_public[1])

# usr = 'Admin'
# msg = 'hello admin!!' 

# my_private, my_public = crypto.gen_keys()
# # my_public = unique_points[0] # TODO 
# print(f'my private and public:\n\t {my_private}\n\t {my_public}\n')

# shared_key = crypto.get_shared_key(admin_public_point, my_private)
# print(f'shared key:\n\t {shared_key}\n')

# hmac = crypto.calculate_hmac(msg, shared_key)
# print(f'hmac:\n\t {hmac.hexdigest()}')

# with requests.Session() as session:

#     def submit_msg(hmac, x, y):
#         data = {
#             'recipient': usr,
#             'message': msg,
#             'hmac': hmac.hexdigest(),
#             'pkey_x': x,
#             'pkey_y': y
#         }
#         res = session.post(url + 'submit', data=data)

#         soup = BeautifulSoup(res.text, 'html.parser')
#         hmac_text = soup.find('font', string=lambda t: "HMAC" in t).text if soup.find('font', string=lambda t: "HMAC" in t) else None
#         question_text = soup.find('font', string=lambda t: "What do you want?" in t).text if soup.find('font', string=lambda t: "What do you want?" in t) else None
#         return hmac_text, question_text

#     hmac_texts = [submit_msg(hmac, str(my_public.x), str(my_public.y))]
#     hmacs = []

#     for my_public in unique_points: 
#         # print(f'my private and public:\n\t {my_private}\n\t {my_public}\n')

#         shared_key = crypto.get_shared_key(admin_public_point, my_private)
#         # print(f'shared key:\n\t {shared_key}\n')

#         hmac = crypto.calculate_hmac(msg, shared_key)
#         # print(f'hmac:\n\t {hmac.hexdigest()}')

#         res = submit_msg(hmac, str(my_public.x), str(my_public.y))
#         hmac_texts.append(res)
#         hmacs.append(res[0].split(":")[1].strip())

#     for ele in hmac_texts:
#         print(ele)
#     for ele in hmacs: 
#         print(ele)
