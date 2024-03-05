import crypto


# note: must be run in conjunction with looking at and 
# modifying the server's page in a browser 
# - set other_public as the admin's public key 

def run(X, Y, factor):
    other_public = (178701865528500695111421931078682459602, 97278987132914619892488911365753380408)
    other_public_point = crypto.EccAlgPoint(curve=crypto.curve, x=other_public[0], y=other_public[1])

    '''
    -----
    Alice (me) trying to send message to Other 
    ----- 
    '''
    msg = 'hello admin'

    alice_private, alice_public = crypto.gen_keys()

    alice_public = crypto.EccAlgPoint(curve=crypto.curve, x=X, y=Y)

    print(f'my private and public:\n\t {alice_private}\n\t {alice_public}\n')

    # calculate shared key 
    shared_key = crypto.get_shared_key(other_public_point, alice_private)
    print(f'shared key:\n\t {shared_key}\n')

    # sign w/ HMAC 
    h = crypto.calculate_hmac(msg, shared_key)
    print(f'hmac:\n\t {h.hexdigest()}\n\n\n')

    point = crypto.EccAlgPoint(curve=crypto.curve, x=X, y=Y)

    msg = 'Huh, it looks like your hmac does not match your public key. Would you like to double check that?'

    # get unique set of points (8 total b/c it's order 8)
    acc = []
    for i in range(0, factor * 10):
        mp = point * i 

        acc.append((i % factor, mp))

    unique_points = set(acc)
    hmacs = []
    for i, p in enumerate(unique_points):
        # print(f'mod: {p[0]}\npoint: {p[1]}\n')

        h = crypto.calculate_hmac(msg, p[1])
        hmacs.append((p[0], h))

    for mod, h in hmacs:
        print(f'mod: {mod}, h: {h.hexdigest()}')
