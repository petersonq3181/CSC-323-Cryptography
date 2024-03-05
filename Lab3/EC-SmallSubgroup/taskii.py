import random
import time
from taski import scalar_multiplication
from numpy import roots


# check if n is a quadratic residue modulo p using Euler's criterion
def is_quadratic_residue(n, p):
    return pow(n, (p-1)//2, p) == 1

# find a quadratic non-residue modulo p
def find_non_residue(p):
    for z in range(2, p):
        if not is_quadratic_residue(z, p):
            return z
    raise ValueError("quadratic non-residue not found")

# find a square root of n modulo p using the Tonelli-Shanks algorithm
def tonelli_shanks(n, p):
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    if S == 1:
        return pow(n, (p + 1) // 4, p)

    z = find_non_residue(p)
    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)

    while True:
        if t == 0:
            return 0
        if t == 1:
            return R

        i = 0
        for i in range(1, M):
            if pow(t, 2**i, p) == 1:
                break

        b = pow(c, 2**(M - i - 1), p)
        M = i
        c = pow(b, 2, p)
        t = (t * c) % p
        R = (R * b) % p

def efficient_find_y(x, A, B, p):
    y_squared = (x**3 + A*x + B) % p
    if is_quadratic_residue(y_squared, p):
        y = tonelli_shanks(y_squared, p)
        return y, p - y 
    return None, None 


def find_random_point_on_curve(A, B, p):
    while True:
        x = random.randint(0, p-1)
        n = (x**3 + A*x + B) % p
        if is_quadratic_residue(n, p):
            y = tonelli_shanks(n, p)
            return (x, y)

def find_point_of_order(A, B, p, curve_order, desired_order):
    O = (None, None)

    if desired_order == 2:
        for x in range(p):
            if (x**3 + A*x + B) % p == 0:
                return (x, 0)
        return None 

    for x in range(p):
        y, y_neg = efficient_find_y(x, A, B, p)
        if y is not None:
            for possible_y in [y, y_neg]:
                P = (x, possible_y)
                Q = scalar_multiplication(curve_order // desired_order, P, A, B, p)
                if Q != O: 
                    if scalar_multiplication(desired_order, Q, A, B, p) == O:
                        return Q 

    return None  


if __name__ == "__main__":
    A = 3
    B = 8
    p = 13

    point = find_random_point_on_curve(A, B, p)
    print(f"Random point on the curve: {point}")



    curve_order = 12 
    desired_order = 3

    point = find_point_of_order(A, B, p, curve_order, desired_order)
    print(f"point with order {desired_order}: {point}")

    '''
    finding a point with order 2 on an elliptic curve means finding a point that
    when added to itself, results in the identity element

    ie. P = -P 
    or same x and opposite y's (so y must equal 0)

    solve 0 = x^3 - Ax + B 
    '''
    def find_point_of_order_2(A, B):
        coefficients = [1, 0, A, B]
        return roots(coefficients)

    print(find_point_of_order_2(-95051, 11279326))
