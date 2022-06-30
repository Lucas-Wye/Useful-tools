import random

# local library
import helper


def Mont_Mod_Red(T, R, q, qPrime):
    # calculate T * R^{-1} % q
    m = T * qPrime % R
    t = (T + q * m) // R
    if t > q:
        return t - q
    return t


if __name__ == "__main__":
    q = 3329
    R = 2**32
    R_inv = helper.modinv(R, q)
    qPrime = (R * R_inv - 1) // q
    print("""q = {},\nq' = {},\nR = {},\nR^-1 = {}""".format(q, qPrime, R, R_inv))

    test_times = 1
    for _ in range(test_times):
        a = random.randint(0, q - 1)
        b = random.randint(0, q - 1)
        T = a * b

        res = Mont_Mod_Red(T, R, q, qPrime)
        ref = T * R_inv % q

        if res != ref:
            raise Exception("Error!")
        print("a = {}, b = {}, res = {}".format(a, b, res))
