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
for i in range(0, 100):
    mp = point * i 

    acc.append((i % 8, mp))

unique_points = set(acc)
for i, p in enumerate(unique_points):
    print(i, p)

# ----- talk to admin 
admin_public = (8406619959067174887612185901056420613, 20101476828203913063003426095829121743)
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

    # normal admin msg submit with my public x and y
    orig_hmac, question_text = submit_msg(hmac, str(my_public.x), str(my_public.y))
    print(f'orig hmac: {orig_hmac}\nreturned text: {question_text}\n')
    
    hmacs = []
    for mod_mult, my_public in unique_points: 
        # print(f'my private and public:\n\t {my_private}\n\t {my_public}\n')

        shared_key = crypto.get_shared_key(admin_public_point, my_private)
        print(f'shared key:\n\t {shared_key}\n')
        # NOTE: shouldn't be the same everytime, maybe need to change my_private 
        # accordingly for each change of my_public ? 

        hmac = crypto.calculate_hmac(msg, shared_key)
        # print(f'hmac:\n\t {hmac.hexdigest()}')

        try:
            res = submit_msg(hmac, str(my_public.x), str(my_public.y))
        except:
            res = submit_msg(hmac, None, None)

        hmacs.append((mod_mult, res))

    for ele in hmacs: 
        if ele[1][0] == None: 
            continue
        # print(ele[1])

        print(f'mod: {ele[0]},\t hmac: {ele[1][0].split(":")[1].strip()}\n')
