import random
from taski import scalar_multiplication

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

def find_random_point_on_curve(A, B, p):
    while True:
        x = random.randint(0, p-1)
        n = (x**3 + A*x + B) % p
        if is_quadratic_residue(n, p):
            y = tonelli_shanks(n, p)
            return (x, y)


A = 3
B = 8
p = 13

point = find_random_point_on_curve(A, B, p)
print(f"Random point on the curve: {point}")



def find_point_of_order(A, B, p, curve_order, desired_order):
    O = (None, None)

    max_attempts = 1000
    for _ in range(max_attempts):
        x = random.randint(0, p-1)
        y_squared = (x**3 + A*x + B) % p

        if not is_quadratic_residue(y_squared, p):
            continue
        y = tonelli_shanks(y_squared, p)

        for possible_y in [y, p-y]:
            P = (x, possible_y)
            Q = scalar_multiplication(curve_order // desired_order, P, A, B, p)
            if not (Q == O):
                if scalar_multiplication(desired_order, Q, A, B, p) == O:
                    return Q
    return None

# Example usage - define A, B, p, curve_order, and desired_order based on your specific curve and requirements
curve_order = 12  # This is just an example value; you'll need to compute or know the curve's order
desired_order = 3

point = find_point_of_order(A, B, p, curve_order, desired_order)
print(f"Point with order {desired_order}: {point}")

