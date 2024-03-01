def point_addition(P, Q, A, B, p):
    O = (None, None)
    
    if P == O:
        return Q
    if Q == O:
        return P
    
    x1, y1 = P
    x2, y2 = Q
    
    if x1 == x2 and y1 != y2:
        return O
    
    if P != Q:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p
    else:
        m = (3 * x1**2 + A) * pow(2 * y1, -1, p) % p
    
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    
    return (x3, y3)

A = 3
B = 8   
p = 13 

P = (9, 7) 
Q = (1, 8) 

result = point_addition(P, Q, A, B, p)
print(f"resulting point: {result}")

P = (9, 7) 
Q = (9, 7)

result = point_addition(P, Q, A, B, p)
print(f"resulting point: {result}")

P = (12, 11) 
Q = (12, 2)

result = point_addition(P, Q, A, B, p)
print(f"resulting point: {result}")
