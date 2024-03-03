import crypto

curve = crypto.Curve(a=-95051, b=11279326, field=233970423115425145524320034830162017933)
base_point = crypto.EccAlgPoint(curve=curve, x=182, y=85518893674295321206118380980485522083)
bp_order = 29246302889428143187362802287225875743

point = crypto.EccAlgPoint(curve=crypto.curve, x=16349894185180983439102154383611486412, y=224942997200586455214256137069604954919)

acc = []
for i in range(1, 1000):
    try:
        acc.append((crypto.EccPoint.__mul__(point, i).x, crypto.EccPoint.__mul__(point, i).y))
    except: 
        pass 

uniq_points = set(acc)
for i, p in enumerate(uniq_points):
    print(i, p)
