from sympy.ntheory import factorint
from taskii import *
import crypto

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
f_points = []
for f in factors:
    f_points_dict = factors_2_points(f)
    f_points.append(f_points_dict)

# reconstruct to only save prime factors (stored per curve) that are unique 
# across all the curves 
curve_pfs = [[] for _ in range(len(factors))]
for i, fs in enumerate(f_points):
    for factor, point in fs.items():
        if factor in uniq_pf:
            uniq_pf.remove(factor)
            curve_pfs[i].append((factor, point))


# (hand-selected based on viewing print statements)
relevant_curves = [1, 2, 4]

