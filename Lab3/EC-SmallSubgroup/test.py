import crypto
import requests
from bs4 import BeautifulSoup

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
        # print(crypto.EccPoint.__mul__(point, i).__str__())
        pass 

# note: prints 7 elements instead of 8 b/c missing the origin 
ps = set(acc)
unique_points = []
for i, p in enumerate(ps):
    # print(i, p)
    unique_points.append(crypto.EccAlgPoint(curve=crypto.curve, x=p[0], y=p[1]))

# ----- talk to admin 
admin_public = (228586928728760623489332690628331395579, 80025156566348652611156132435508764067)
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

with requests.Session() as session:

    def submit_msg(hmac, x, y):
        data = {
            'recipient': usr,
            'message': msg,
            'hmac': hmac.hexdigest(),
            'pkey_x': x,
            'pkey_y': y
        }
        res = session.post(url + 'submit', data=data)

        soup = BeautifulSoup(res.text, 'html.parser')
        hmac_text = soup.find('font', string=lambda t: "HMAC" in t).text if soup.find('font', string=lambda t: "HMAC" in t) else None
        question_text = soup.find('font', string=lambda t: "What do you want?" in t).text if soup.find('font', string=lambda t: "What do you want?" in t) else None
        return hmac_text, question_text

    hmac_texts = [submit_msg(hmac, str(my_public.x), str(my_public.y))]

    for my_public in unique_points: 
        # print(f'my private and public:\n\t {my_private}\n\t {my_public}\n')

        shared_key = crypto.get_shared_key(admin_public_point, my_private)
        # print(f'shared key:\n\t {shared_key}\n')

        hmac = crypto.calculate_hmac(msg, shared_key)
        # print(f'hmac:\n\t {hmac.hexdigest()}')

        hmac_texts.append(submit_msg(hmac, str(my_public.x), str(my_public.y)))

    for ele in hmac_texts:
        print(ele)
