"""
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % m
"""


def modinv(R, p):
    t = 0
    r = p
    newt = 1
    newr = R
    while newr != 0:
        q = r // newr
        (t, newt) = (newt, t - q * newt)
        (r, newr) = (newr, r - q * newr)

    if r != 1:
        return 0
    if t < 0:
        return t + p
    return t


# Bit-Reverse integer
def intReverse(a, n):
    b = ("{:0" + str(n) + "b}").format(a)
    return int(b[::-1], 2)


# Bit-Reversed index
def indexReverse(a, r):
    n = len(a)
    b = [0] * n
    for i in range(n):
        rev_idx = intReverse(i, r)
        b[rev_idx] = a[i]
    return b


# Check if input is m-th (could be n or 2n) primitive root of unity of q
def isrootofunity(w, m, q):
    if pow(w, m, q) != 1:
        return False
    elif pow(w, m // 2, q) != (q - 1):
        return False
    else:
        v = w
        for i in range(1, m):
            if v == 1:
                return False
            else:
                v = (v * w) % q
        return True


def transform_to_unsigned(in1, length, q):
    out = [in1[i] for i in range(length)]
    for i in range(length):
        if in1[i] < 0:
            out[i] = q + in1[i]
    return out


def transform_to_signed(in1, length, q):
    mid = q // 2 - 1
    out = [in1[i] for i in range(length)]
    for i in range(length):
        if in1[i] > mid:
            out[i] = in1[i] - q
    return out


def mod_signed(x, q):
    mid = q // 2 - 1
    out = x % q
    if out > mid:
        out = out - q
    return out
