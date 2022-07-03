from math import log2
import random
import sys

# local library
sys.path.append("..")
import helper


def Mont_Mod_Red(T, R, q, qPrime):
    # calculate T * R^{-1} % q
    new_T = T % R  # optimze here
    m = new_T * qPrime % R
    t = (T + q * m) // R
    if t > q:
        t = t - q
    return t


def signed_mod(input, q):
    output = input % q
    if output >= (q // 2 + 1):
        output = output - q
    return output


def signed_Mont_Red(T, R, q, qInv):
    # from paper "Faster AVX2 optimized NTT multiplication for Ring-LWE lattice cryptography"
    new_T = signed_mod(T, R)
    shift = int(log2(R))
    new_Th = T >> shift
    tmp = new_T * qInv
    m = signed_mod(tmp, R)
    t = m * q >> shift
    r = new_Th - t
    # print(
    #     "T = {}, new_T = {}, new_Th = {}".format(
    #         T, new_T, new_Th
    #     )
    # )
    # if shift == 32:
    #     print(
    #         "    T = {}, \nnew_T = {}, \nnew_Th = {}".format(
    #             bin(T & 0xFFFFFFFF),
    #             bin(new_T & 0xFFFFFFFF),
    #             bin(new_Th & 0xFFFFFFFF),
    #         )
    #     )
    # else:
    #     print(
    #         "    T = {}, \nnew_T = {}, \nnew_Th = {}".format(
    #             bin(T & 0xFFFFFFFF),
    #             bin(new_T & 0xFFFF),
    #             bin(new_Th & 0xFFFF),
    #         )
    #     )
    return r


def test_unsigned_Mont(q, test_times):
    R = 2**32
    if q < 2**16:
        R = 2**16
    R_inv = helper.modinv(R, q)
    qPrime = (R * R_inv - 1) // q
    print("""q = {},q' = {},R = {},R^-1 = {}""".format(q, qPrime, R, R_inv))

    for _ in range(test_times):
        a = random.randint(0, q - 1)
        b = random.randint(0, q - 1)
        T = a * b

        res = Mont_Mod_Red(T, R, q, qPrime)
        ref = T * R_inv % q

        if res != ref:
            print(
                "a = {}, b = {}, res = {}, ref = {}, res % q = {}".format(
                    a, b, res, ref, res % q
                )
            )
            raise Exception("Error!")


def test_signed_Mont(q, test_times):
    R = 2**32
    if q < 2**16:
        R = 2**16
    R_inv = helper.modinv(R, q)
    qInv = helper.modinv(q, R)
    print("""q = {},q^-1 = {},R = {},R^-1 = {}""".format(q, qInv, R, R_inv))

    for _ in range(test_times):
        a = random.randint(-(q - 1) // 2, q // 2)
        b = random.randint(-(q - 1) // 2, q // 2)
        T = a * b

        res = signed_Mont_Red(T, R, q, qInv)
        ref = T * R_inv % q

        if res < 0:
            res = res + q
        if res != ref:
            print(
                "a = {}, b = {}, res = {}, ref = {}, res % q = {}".format(
                    a, b, res, ref, res % q
                )
            )
            raise Exception("Error!")


if __name__ == "__main__":
    q_list = [
        3329,  # Kyber
        8380417,  # Dilithium
        2**25 - 2**14 + 1,  # Saber
    ]
    test_times = 10
    for q in q_list:
        test_unsigned_Mont(q, test_times)
        test_signed_Mont(q, test_times)
