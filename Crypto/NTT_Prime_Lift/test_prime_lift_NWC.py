import random
import sys

sys.path.append("../PolyMul")
import poly


length = 256
q = 8192
q_Prime = 2**39 - 2**12 + 1
tw_q_Prime = 2174960542
tw_2n_q_Prime = 2455281570


poly_1 = [random.randint(0, q) for _ in range(length)]
poly_2 = [random.randint(0, q) for _ in range(length)]

# (1) NWC schoolbook method -------------------------------
out_poly_mul_NWC_schoolbook = poly.poly_mul_NWC_schoolbook(poly_1, poly_2, length, q)

# (2) shcoolbook with prime lift --------------------------
out_poly_mul_schoolbook_lift = poly.poly_mul_schoolbook(poly_1, poly_2, length, q_Prime)
for i in range(length):
    out_poly_mul_schoolbook_lift[i] = (
        out_poly_mul_schoolbook_lift[i] - out_poly_mul_schoolbook_lift[i + length]
    ) % q
# compare
for i in range(length):
    if out_poly_mul_schoolbook_lift[i] != out_poly_mul_NWC_schoolbook[i]:
        print(out_poly_mul_NWC_schoolbook)
        print(out_poly_mul_schoolbook_lift)
        raise Exception("Incorrect poly mul result")

# (3) 2n-point NTT with prime lift ------------------------
poly_zeros = [0 for _ in range(length * 2)]
poly_1_padding = poly_1 + poly_zeros
poly_2_padding = poly_2 + poly_zeros

out_poly_mul_2n_q_Prime = poly.poly_mul_NTT(
    poly_1_padding, poly_2_padding, length * 2, q_Prime, tw_2n_q_Prime
)
for i in range(length):
    out_poly_mul_2n_q_Prime[i] = (
        out_poly_mul_2n_q_Prime[i] - out_poly_mul_2n_q_Prime[i + length]
    ) % q
# compare
for i in range(length):
    if out_poly_mul_2n_q_Prime[i] != out_poly_mul_NWC_schoolbook[i]:
        print(out_poly_mul_NWC_schoolbook)
        print(out_poly_mul_2n_q_Prime)
        raise Exception("Incorrect poly mul result")

# (4) n-point NTT with prime lift (NWC) -------------------
out_poly_mul_q_Prime = poly.poly_mul_NWC_NTT(
    poly_1, poly_2, length, q_Prime, tw_q_Prime, tw_2n_q_Prime
)
for i in range(length):
    out_poly_mul_q_Prime[i] = (out_poly_mul_q_Prime[i] - q_Prime) % q
# compare
err = 0
for i in range(length):
    if out_poly_mul_q_Prime[i] != out_poly_mul_NWC_schoolbook[i]:
        out_poly_mul_q_Prime[i] = (out_poly_mul_q_Prime[i] + q_Prime) % q
        if out_poly_mul_q_Prime[i] != out_poly_mul_NWC_schoolbook[i]:
            raise Exception(
                "Incorrect poly mul result"
            )  # a negligible error probability
