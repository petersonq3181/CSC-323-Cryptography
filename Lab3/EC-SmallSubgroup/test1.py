import crypto 

curve = crypto.curve 
base_point = crypto.base_point
bp_order = crypto.bp_order

X = 16349894185180983439102154383611486412
Y = 224942997200586455214256137069604954919
point = crypto.EccAlgPoint(curve=crypto.curve, x=X, y=Y)

msg = 'Huh, it looks like your hmac does not match your public key. Would you like to double check that?'

# origin = crypto.EccInfPoint(curve=curve)

# ----- get unique set of points (8 total b/c it's order 8)
acc = []
for i in range(0, 100):
    mp = point * i 

    acc.append((i % 8, mp))

unique_points = set(acc)
hmacs = []
for i, p in enumerate(unique_points):
    print(f'mod: {p[0]}\npoint: {p[1]}\n')

    h = crypto.calculate_hmac(msg, p[1])
    hmacs.append((p[0], h))

for mod, h in hmacs:
    # print(ele.hexdigest())
    print(f'mod: {mod}, h: {h.hexdigest()}')
