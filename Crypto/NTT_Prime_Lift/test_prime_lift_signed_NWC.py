import random
import sys

sys.path.append("..")
sys.path.append("../PolyMul")
import helper
import poly

length = 256
q = 8192
low_value = -q // 2
high_value = q // 2 - 1
# q_Prime = 2**39 - 2**12 + 1
# tw_q_Prime = 2174960542
# tw_2n_q_Prime = 2455281570
# low_value1 = low_value
# high_value1 = high_value
q_Prime = 2**25 - 2**14 + 1
tw_q_Prime = 242917
tw_2n_q_Prime = 60094
low_value1 = -5
high_value1 = 5

poly_1 = [random.randint(low_value, high_value) for _ in range(length)]
poly_2 = [random.randint(low_value1, high_value1) for _ in range(length)]

# (1) NWC schoolbook method -------------------------------
out_poly_mul_NWC_schoolbook = poly.poly_mul_NWC_schoolbook_signed(
    poly_1, poly_2, length, q
)

# (2) signed NTT method -----------------------------------
out_poly_mul_q_Prime = poly.poly_mul_NWC_NTT_signed(
    poly_1, poly_2, length, q_Prime, tw_q_Prime, tw_2n_q_Prime
)
for i in range(length):
    out_poly_mul_q_Prime[i] = helper.mod_signed(out_poly_mul_q_Prime[i], q)

for i in range(length):
    if out_poly_mul_q_Prime[i] != out_poly_mul_NWC_schoolbook[i]:
        print(out_poly_mul_NWC_schoolbook)
        print(out_poly_mul_q_Prime)
        raise Exception("Incorrect poly mul result")


# (3) unsigned NTT with signed data
out_poly_mul_q_Prime_2 = poly.poly_mul_NWC_NTT_data_trans(
    poly_1, poly_2, length, q_Prime, tw_q_Prime, tw_2n_q_Prime
)
for i in range(length):
    out_poly_mul_q_Prime_2[i] = helper.mod_signed(out_poly_mul_q_Prime_2[i], q)

for i in range(length):
    if out_poly_mul_q_Prime_2[i] != out_poly_mul_NWC_schoolbook[i]:
        print(out_poly_mul_NWC_schoolbook)
        print(out_poly_mul_q_Prime_2)
        raise Exception("Incorrect poly mul result")
