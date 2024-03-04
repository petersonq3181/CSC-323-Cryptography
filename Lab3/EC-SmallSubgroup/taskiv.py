from sympy.ntheory import factorint
from taskii import *
import crypto

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

factors_product = 1
for ele in uniq_pf:
    factors_product *= ele 
print('factors product', factors_product)
print(factors_product > 29246302889428143187362802287225875743)

# reconstruct the prime factors (stored per curve) that are unique 
curve_pfs = [[] for _ in range(len(factors))]
for i, fs in enumerate(factors):
    for ks in fs.keys():
        if ks in uniq_pf:
            curve_pfs[i].append(ks)
            uniq_pf.remove(ks)

print(curve_pfs)

# # (hand-selected based on viewing print statements)
# relevant_curves = [1, 2, 4]


# testing :
# take one prime factor of one curve, and also find product 
# of all other factors 
# pick random point on the curve 
# multiply by number above 
# see if point truly has order equal to the orig prime factor 
curve2_gg = {2: 2, 7: 1, 23: 1, 37: 1, 67: 1, 607: 1, 1979: 1, 13327: 1, 13799: 1, 663413139201923717: 1}
prime = 7 
other_prod = 1
for k, v in curve2_gg.items():
    if k != prime: 
        other_prod *= k * v 
print(f'curve 2:\n\torder: {potential_curves[3]}\n\tprime: {prime}\n\tother_prod: {other_prod}\n\tprod: {other_prod * prime}')

X, Y = find_random_point_on_curve(potential_curves[1][0], potential_curves[1][1], potential_curves[1][2])
print(X, Y)

test_point_orig = crypto.EccAlgPoint(curve=crypto.curve, x=X, y=Y)
test_point = test_point_orig * other_prod
print(test_point)


acc = []
for i in range(0, 100):
    mp = test_point * i 

    acc.append((i % prime, mp))

unique_points = set(acc)
for i, p in enumerate(unique_points):
    print(i, p)
