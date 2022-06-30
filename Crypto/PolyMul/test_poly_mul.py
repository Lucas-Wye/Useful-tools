import random

import sys

sys.path.append("../")
import helper

import poly
import ntt


def test(q, length):
    poly_1 = [random.randint(0, q) for _ in range(length)]
    poly_2 = [random.randint(0, q) for _ in range(length)]

    tw_n = ntt.searchTiddleFactor(length, q)
    tw_2n = ntt.searchTiddleFactor(2 * length, q)

    out_poly_mul = poly.poly_mul_NWC_NTT(poly_1, poly_2, length, q, tw_n, tw_2n)
    out_poly_mul_schoolbook = poly.poly_mul_NWC_schoolbook(poly_1, poly_2, length, q)

    for i in range(length):
        if out_poly_mul[i] != out_poly_mul_schoolbook[i]:
            raise Exception("Incorrect poly mul result")

    out_poly_mul = poly.poly_mul_PWC_NTT(poly_1, poly_2, length, q, tw_n)
    out_poly_mul_schoolbook = poly.poly_mul_PWC_schoolbook(poly_1, poly_2, length, q)

    for i in range(length):
        if out_poly_mul[i] != out_poly_mul_schoolbook[i]:
            raise Exception("Incorrect poly mul result")


if __name__ == "__main__":
    test(7681, 256)  # Kyber
    test(8380417, 256)  # Dilithium
    # test(8192, 256) # Saber

    test(13 * 1024 + 1, 512)
