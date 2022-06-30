import random


def Barrett_Reduction(T, q, k, m):
    # calculate T % q
    z = T
    q1 = z >> (k - 1)
    t = (q1 * m) >> (k + 1)
    z = z - (t * q)
    if z >= q:
        z = z - q
    return z


if __name__ == "__main__":
    q = 3329
    k = len(bin(q)) - 2
    m = int((2 ** (2 * k)) / q)

    test_times = 100
    for _ in range(test_times):
        a = random.randint(0, q - 1)
        b = random.randint(0, q - 1)
        T = a * b

        res = Barrett_Reduction(T, q, k, m)
        ref = T % q
        if res != ref:
            raise Exception("Error")
