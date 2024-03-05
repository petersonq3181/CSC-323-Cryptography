from sympy.ntheory import factorint
from taskii import *
import crypto
from taskiiifunc import *
import requests
from bs4 import BeautifulSoup
import sys 

def factors_2_points(factors):
    total_product = 1
    for key, value in factors.items():
        total_product *= key**value

    fs_otherprods = {}
    for key in factors:
        if factors[key] > 1:
            new_value = total_product // (key ** factors[key])
        else:
            new_value = total_product // key
        fs_otherprods[key] = new_value

    points = {}
    for k, v in fs_otherprods.items():
        X, Y = find_random_point_on_curve(potential_curves[1][0], potential_curves[1][1], potential_curves[1][2])
        new_point_orig = crypto.EccAlgPoint(curve=crypto.curve, x=X, y=Y)
        new_point = new_point_orig * v
        points[k] = new_point

    return points

def test_point_order(point, expected_order):
    acc = []
    for i in range(0, expected_order * 11):
        mp = point * i 

        acc.append((i % expected_order, mp))

    unique_points = set(acc)
    return len(unique_points) == expected_order


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
print(factors_product > 29246302889428143187362802287225875743)

# turn each curve's factor dicts into {factor: point} dicts 
# TODO: at this point it might not be necessary to still keep track of 
# which points corr. to which curves, could just accumulate all the points 
f_points = []
for f in factors:
    f_points_dict = factors_2_points(f)
    f_points.append(f_points_dict)

# reconstruct to only save prime factors (stored per curve) that are unique 
# across all the curves 
curve_pfs = [[] for _ in range(len(factors))]
points = []
for i, fs in enumerate(f_points):
    for factor, point in fs.items():
        if factor in uniq_pf:
            uniq_pf.remove(factor)
            curve_pfs[i].append((factor, point))
            points.append((factor, point))


# # TODO for now just first point 
# print(points[1])
# point = points[1][1]
# factor = points[1][0]
# print(type(point), point)
# try:
#     print(point.x, point.y)
# except: 
#     print('origin')
#     pass 

# run(point.x, point.y, factor) 
# # match mod 0

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

    # TODO refactor to for all points 
    point = points[1][1]
    if isinstance(point, crypto.EccInfPoint):
        print('cur point is Origin')
        sys.exit(0) # maybe refactor to Continue 
    factor = points[1][0]


    given_hmac, x, y, hmacs = run(point.x, point.y, factor, admin_public)
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

    print('LFG')
    print(found_mod, point)

    # hmac_texts = [submit_msg(hmac, str(my_public.x), str(my_public.y))]