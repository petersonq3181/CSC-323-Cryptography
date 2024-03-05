from sympy.ntheory import factorint
from taskii import *
import crypto
from taskiiifunc import *
import requests
from bs4 import BeautifulSoup
import sys 

server_order = 29246302889428143187362802287225875743

# potential curves (M = B (ie. B != server curve's B))
# (A, B, Field, Order)
potential_curves = [
    (-95051, 118, 233970423115425145524320034830162017933, 233970423115425145528637034783781621127),
    (-95051, 727, 233970423115425145524320034830162017933, 233970423115425145545378039958152057148),
    (-95051, 210, 233970423115425145524320034830162017933, 233970423115425145550826547352470124412),
    (-95051, 79, 233970423115425145524320034830162017933, 233970423115425145538546862144009931013),
    (-95051, 504, 233970423115425145524320034830162017933, 233970423115425145544350131142039591210),
]

# get prime factors of all curves' orders 
factors = []
for curve in potential_curves:
    fs = factorint(curve[3])
    print(fs)
    factors.append(fs)

# find all unique prime factors that are relatively small (< 2^16)
uniq_pf = {key for f in factors for key in f.keys() if key < 65536}

print(uniq_pf)
print(len(uniq_pf))

# make sure prod of all unique factors is greater than server's curve order 
factors_product = 1
for ele in uniq_pf:
    factors_product *= ele 
print('factors product', factors_product)
print(factors_product > server_order)


# curve_pfs = [[] for _ in range(len(factors))]
# for i, d in enumerate(factors):
#     for k, v in d.items():
#         if k in uniq_pf:
#             curve_pfs[i].append(k)
#             uniq_pf.remove(k)
# print(curve_pfs)

# hardcoded for 3 curves based on prev print statements 
fs_and_points = []
for curve_number in [1, 2, 4]:
    curve = potential_curves[curve_number]
    my_keys = [k for k in list(factors[curve_number].keys())[::-1]]

    for i, k in enumerate(my_keys):
        print(i, k)

        if k < 7:
            continue 
    
        fs_and_points.append((k, find_point_of_order(curve[0], curve[1], curve[2], curve[3], k)))

# at this point it might not be necessary to still keep track of 
# which points corr. to which curves, could just accumulate all the points and their factors 
uniq_fandp = []
for factor, point in fs_and_points:
    if factor in uniq_pf:
        uniq_fandp.append((factor, point))
        uniq_pf.remove(factor)
uniq_fandp = sorted(uniq_fandp)
print(uniq_fandp)
print(len(uniq_fandp))



def parse_admin_public(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if cols and cols[0].text.strip() == 'Admin':
            admin_public_key_str = cols[1].text.strip()
            admin_public_key = tuple(map(int, admin_public_key_str.strip('()').split(', ')))
            return admin_public_key
    return None


url = 'http://0.0.0.0:8080/'
usr = 'Admin'
msg = 'hello admin'
res_msg = 'Huh, it looks like your hmac does not match your public key. Would you like to double check that?'

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
        question_text = soup.find('font', string=lambda t: res_msg in t).text if soup.find('font', string=lambda t: res_msg in t) else None
        return hmac_text.split()[1], question_text.strip()

    # get admin public key 
    users_res = session.get(url + 'users')
    admin_public = parse_admin_public(users_res.text)
    if admin_public == None:
        print('Failed to get Admin Public')
        sys.exit(0)

    curprod = 1

    # --- s MOD m = f
    # s: admin secret key
    # m: found_mod 
    # f: factor of point used as our public_key in msg 
    # CRT_data contains tuples of (m, f)
    CRT_data = []
    for i, (factor, point) in enumerate(uniq_fandp): 
        # if isinstance(point, crypto.EccInfPoint):
        #     print('cur point is Origin')
        #     # sys.exit(0) # maybe refactor to Continue 
        #     continue
        
        curprod *= factor

        print(f'entered loop i: {i}, factor: {factor}')

        given_hmac, x, y, hmacs = run(point[0], point[1], factor, admin_public)
        # print(given_hmac)
        # print(x)
        # print(y)
        # for m, h in hmacs:
        #     print(m, h.hexdigest(), type(h.hexdigest()))
        
        admin_hmac, ret_msg = submit_msg(given_hmac, str(x), str(y))
        
        # search for which mod/hmac pair equals admin hmac 
        found_mod = -1
        for m, h in hmacs:
            if h.hexdigest() == admin_hmac:
                found_mod = m
                break 
        if found_mod == -1:
            print('no match found between admin_hmac and our hmacs')
            for m, h in hmacs:
                print(m, h.hexdigest(), type(h.hexdigest()))
            print(admin_hmac)
            sys.exit(0)

        print(f'i: {i}\t {(found_mod, factor)}\t curprod: {curprod}, curprod>curveorder? {curprod > server_order}\n')

        CRT_data.append((found_mod, factor))

        if curprod > server_order:
            break

    print('end of loop:')
    print(len(CRT_data))
    print(CRT_data)

'''
an example generated CRT_data for 15 points:
[(3, 7), (3, 11), (7, 23), (14, 31), (19, 37), (14, 61), (17, 67), (13, 89), (43, 607), (1557, 1979), (3449, 4999), (4029, 12157), (7785, 13327), (2225, 13799), (8816, 28411)]
'''
