import sys

sys.path.append("../")
import helper


def searchTiddleFactor(length, q):
    tw = -1
    for i in range(1, q):
        if helper.isrootofunity(i, length, q):
            tw = i
            break
    return tw


def ntt(input, length, q, tw):
    out = [0 for _ in range(length)]
    for k in range(length):
        tmp = 0
        for n in range(length):
            w = pow(tw, n * k, q)
            tmp += input[n] * w % q
        out[k] = tmp % q
    return out


def ntt_signed(input, length, q, tw):
    out = [0 for _ in range(length)]
    for k in range(length):
        tmp = 0
        for n in range(length):
            w = pow(tw, n * k, q)
            w = helper.mod_signed(w, q)
            tmp += helper.mod_signed(input[n] * w, q)
        out[k] = tmp % q
    return out
