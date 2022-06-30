import random
import sys

sys.path.append("../PolyMul")
import poly


def test(length, q, q_Prime, tw_q_Prime):
    poly_1 = [random.randint(0, q) for _ in range(length)]
    poly_2 = [random.randint(0, q) for _ in range(length)]

    # (1) PWC schoolbook method -------------------------------
    out_poly_mul_PWC_schoolbook = poly.poly_mul_PWC_schoolbook(
        poly_1, poly_2, length, q
    )

    # (2) shcoolbook with prime lift --------------------------
    out_poly_mul_schoolbook_lift = poly.poly_mul_schoolbook(
        poly_1, poly_2, length, q_Prime
    )
    for i in range(length):
        out_poly_mul_schoolbook_lift[i] = (
            out_poly_mul_schoolbook_lift[i] + out_poly_mul_schoolbook_lift[i + length]
        ) % q
    # compare
    for i in range(length):
        if out_poly_mul_schoolbook_lift[i] != out_poly_mul_PWC_schoolbook[i]:
            print(out_poly_mul_PWC_schoolbook)
            print(out_poly_mul_schoolbook_lift)
            raise Exception("Incorrect poly mul result")

    # (3) NTT with prime lift
    out_poly_mul_q_Prime = poly.poly_mul_PWC_NTT(
        poly_1, poly_2, length, q_Prime, tw_q_Prime
    )
    for i in range(length):
        out_poly_mul_q_Prime[i] = (out_poly_mul_q_Prime[i]) % q

    for i in range(length):
        if out_poly_mul_q_Prime[i] != out_poly_mul_PWC_schoolbook[i]:
            print(out_poly_mul_PWC_schoolbook)
            print(out_poly_mul_q_Prime)
            raise Exception("Incorrect poly mul result")


if __name__ == "__main__":
    length = 256
    q = 8192
    q_Prime = 2**39 - 2**12 + 1
    tw_q_Prime = 2174960542

    test(length, q, q_Prime, tw_q_Prime)
