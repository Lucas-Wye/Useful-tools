import random


def bit_cut(z, tmp, shift):
    z = z % (2 ** (shift))
    tmp = tmp % (2 ** (shift))
    return z, tmp


def Barrett_Reduction(T, q, k, m):
    # calculate T % q
    z = T
    q1 = z >> (k - 1)
    t = (q1 * m) >> (k + 1)
    tmp = t * q
    shift = k + 1
    # print(hex(z), hex(tmp), shift, z - tmp)
    z, tmp = bit_cut(z, tmp, shift)
    r = z - tmp
    # optimization
    r = r + 2 ** (30)
    r = r % (2 ** (shift))
    # if r < 0:
    #     r = r + 2 ** (shift)
    if r >= 2 * q:
        r = r - 2 * q
    if r >= q:
        r = r - q
    # print(hex(z), hex(tmp), r)
    return r


if __name__ == "__main__":
    q_list = [
        3329,  # Kyber
        8380417,  # Dilithium
        2**25 - 2**14 + 1,  # Saber
        2048,  # NTRU
        4096,  # NTRU
        8192,  # NTRU
    ]
    for q in q_list:
        k = len(bin(q)) - 2
        m = int((2 ** (2 * k)) / q)

        test_times = 500000
        for _ in range(test_times):
            a = random.randint(0, q - 1)
            b = random.randint(0, q - 1)
            T = a * b

            res = Barrett_Reduction(T, q, k, m)
            ref = T % q
            if res != ref:
                raise Exception("Error", q, a, b, k, m)
