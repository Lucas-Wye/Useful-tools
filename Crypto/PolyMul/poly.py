import sys

sys.path.append("../")
import helper

import ntt


def poly_mul_PWC_NTT(in1, in2, length, q, tw_n):
    n_inv = helper.modinv(length, q)
    tw_n_inv = helper.modinv(tw_n, q)

    # NTT
    res1 = ntt.ntt(in1, length, q, tw_n)
    res2 = ntt.ntt(in2, length, q, tw_n)

    # Point-Wise Mul
    point_wise_res = [res1[i] * res2[i] % q for i in range(length)]

    # INTT
    res_intt = ntt.ntt(point_wise_res, length, q, tw_n_inv)
    for i in range(length):
        res_intt[i] = res_intt[i] * n_inv % q

    return res_intt


def poly_mul_NWC_NTT(in1, in2, length, q, tw_n, tw_2n):
    n_inv = helper.modinv(length, q)
    tw_n_inv = helper.modinv(tw_n, q)
    tw_2n_inv = helper.modinv(tw_2n, q)

    # pre-processing
    in1_preprocessing = [0 for _ in range(length)]
    in2_preprocessing = [0 for _ in range(length)]
    for i in range(length):
        tmp = pow(tw_2n, i, q)
        in1_preprocessing[i] = in1[i] * tmp % q
        in2_preprocessing[i] = in2[i] * tmp % q

    # NTT
    res1 = ntt.ntt(in1_preprocessing, length, q, tw_n)
    res2 = ntt.ntt(in2_preprocessing, length, q, tw_n)

    # Point-Wise Mul
    point_wise_res = [res1[i] * res2[i] % q for i in range(length)]

    # INTT
    res_intt = ntt.ntt(point_wise_res, length, q, tw_n_inv)
    for i in range(length):
        res_intt[i] = res_intt[i] * n_inv % q

    # post-processing
    out_postprocessing = [0 for _ in range(length)]
    for i in range(length):
        tmp = pow(tw_2n_inv, i, q)
        out_postprocessing[i] = res_intt[i] * tmp % q
    return out_postprocessing


def poly_mul_NTT(in1, in2, length, q, tw_n):
    # by padding zeros
    n_inv = helper.modinv(length, q)
    tw_n_inv = helper.modinv(tw_n, q)

    # NTT
    res1 = ntt.ntt(in1, length, q, tw_n)
    res2 = ntt.ntt(in2, length, q, tw_n)

    # Point-Wise Mul
    point_wise_res = [res1[i] * res2[i] % q for i in range(length)]

    # INTT
    res_intt = ntt.ntt(point_wise_res, length, q, tw_n_inv)
    for i in range(length):
        res_intt[i] = res_intt[i] * n_inv % q
    return res_intt


def poly_mul_schoolbook(in1, in2, length, q):
    # out length is 2 * length
    mul = [0 for _ in range(2 * length)]
    for i in range(length):
        for j in range(length):
            index = i + j
            mul[index] = (mul[index] + in1[i] * in2[j] % q) % q
    return mul


def poly_mul_NWC_schoolbook(in1, in2, length, q):
    mul = poly_mul_schoolbook(in1, in2, length, q)
    for i in range(length):
        mul[i] = (mul[i] - mul[i + length]) % q

    out = [item for item in mul[:length]]
    return out


def poly_mul_PWC_schoolbook(in1, in2, length, q):
    mul = poly_mul_schoolbook(in1, in2, length, q)
    for i in range(length):
        mul[i] = (mul[i] + mul[i + length]) % q

    out = [item for item in mul[:length]]
    return out


def poly_mul_NWC_schoolbook_signed(in1, in2, length, q):
    in1_unsigned = helper.transform_to_unsigned(in1, length, q)
    in2_unsigned = helper.transform_to_unsigned(in2, length, q)
    out = poly_mul_NWC_schoolbook(in1_unsigned, in2_unsigned, length, q)
    return helper.transform_to_signed(out, length, q)


def poly_mul_NWC_NTT_signed(in1, in2, length, q, tw_n, tw_2n):
    n_inv = helper.modinv(length, q)
    tw_n_inv = helper.modinv(tw_n, q)
    tw_2n_inv = helper.modinv(tw_2n, q)

    n_inv = helper.mod_signed(n_inv, q)
    tw_n_inv = helper.mod_signed(tw_n_inv, q)
    tw_2n_inv = helper.mod_signed(tw_2n_inv, q)
    tw_n = helper.mod_signed(tw_n, q)
    tw_2n = helper.mod_signed(tw_2n, q)

    # pre-processing
    in1_preprocessing = [0 for _ in range(length)]
    in2_preprocessing = [0 for _ in range(length)]
    for i in range(length):
        tmp = pow(tw_2n, i, q)
        in1_preprocessing[i] = helper.mod_signed(in1[i] * tmp, q)
        in2_preprocessing[i] = helper.mod_signed(in2[i] * tmp, q)

    # NTT
    res1 = ntt.ntt_signed(in1_preprocessing, length, q, tw_n)
    res2 = ntt.ntt_signed(in2_preprocessing, length, q, tw_n)

    # Point-Wise Mul
    point_wise_res = [helper.mod_signed(res1[i] * res2[i], q) for i in range(length)]

    # INTT
    res_intt = ntt.ntt_signed(point_wise_res, length, q, tw_n_inv)
    for i in range(length):
        res_intt[i] = helper.mod_signed(res_intt[i] * n_inv, q)

    # post-processing
    out_postprocessing = [0 for _ in range(length)]
    for i in range(length):
        tmp = pow(tw_2n_inv, i, q)
        tmp = helper.mod_signed(tmp, q)
        out_postprocessing[i] = helper.mod_signed(res_intt[i] * tmp, q)
    return out_postprocessing


def poly_mul_NWC_NTT_data_trans(in1, in2, length, q, tw_n, tw_2n):
    in1_unsigned = helper.transform_to_unsigned(in1, length, q)
    in2_unsigned = helper.transform_to_unsigned(in2, length, q)
    out = poly_mul_NWC_NTT(in1, in2, length, q, tw_n, tw_2n)
    return helper.transform_to_signed(out, length, q)
