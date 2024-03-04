from sympy.ntheory import factorint

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
    # print(fs)
    factors.append(fs)

# find all unique prime factors that are relatively small (< 2^16)
uniq_pf = set()
max_key = 65536
for f in factors:
    for key, value in f.items():
        if key < max_key:
            uniq_pf.add(key)

print(uniq_pf)
print(len(uniq_pf))
