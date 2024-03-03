import crypto

curve = crypto.curve 
base_point = crypto.base_point
bp_order = crypto.bp_order

point = crypto.EccAlgPoint(curve=crypto.curve, x=16349894185180983439102154383611486412, y=224942997200586455214256137069604954919)

acc = []
for i in range(0, 1000):
    try:
        acc.append((crypto.EccPoint.__mul__(point, i).x, crypto.EccPoint.__mul__(point, i).y))
    except: 
        pass 

# note: prints 7 elements instead of 8 b/c missing the origin 
uniq_points = set(acc)
for i, p in enumerate(uniq_points):
    print(i, p)
