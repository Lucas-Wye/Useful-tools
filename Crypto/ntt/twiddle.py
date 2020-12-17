'''
Author: Lucas Wye<lucas.zw.ye@outlook.com>
Date: 2020-12-03 20:24:28
Description: Generate twiddle factors
'''

import os, sys
path = os.path.join(sys.path[0], os.path.pardir, "bfv")
sys.path.append(path)

from helper import *
from lib import primitive, euler


'''
Description: generate twiddle factors by searching the primitive factor
param {*} N
param {*} P
'''
def generate_twiddle_factorS(N, P):
    for i in range(2, P-1):
            wfound = isrootofunity(i, 2*N, P)
            if wfound:
                psi = i
                psiv = modinv(psi, P)
                w = pow(psi, 2, P)
                wv = modinv(w, P)
                break

    # Generate tables
    w_table = [1]*N
    wv_table = [1]*N
    psi_table = [1]*N
    psiv_table = [1]*N
    for i in range(1, N):
        w_table[i] = ((w_table[i-1] * w) % P)
        wv_table[i] = ((wv_table[i-1] * wv) % P)
        psi_table[i] = ((psi_table[i-1] * psi) % P)
        psiv_table[i] = ((psiv_table[i-1]*psiv) % P)
    return w_table, wv_table, psi_table, psiv_table


'''
Description: calculate the twiddle factors
param {*} N
param {*} g
param {*} P
param {*} minus_enable 
    if minus_enable is `True`, then there will be negative number
'''
def getW(N, g, P, minus_enable):
    W = [0 for i in range(N)]
    for i in range(N):
        tmp = quick_mod(g, (P-1) * i // N, P)
        if minus_enable:            
            W[i] = tmp if ((P - tmp) > tmp) else (tmp - P)     
        else:
            W[i] = tmp  
    return W


def getWn(N, g, P):
    # for the matrix
    Wn = [[0 for i in range(N)] for j in range(N)]
    for n in range(N):
        for k in range(N):
            temp = quick_mod(g, (P-1) * n * k // N, P)
            for item in W:
                if temp == (P - item) and temp > item:
                    temp = -item
            Wn[n][k] = temp
    # print Wn[][] regularly
    for i in range(N):
        print("[", end="")
        for j in range(N):
            print('{:<10}'.format(Wn[i][j]), end=" ")
        print("\b\b]")


if __name__ == "__main__":
    P = 4177
    N = 8

    # (1)
    g = primitive.get_one_primitive_root(P) # very slow for some big primes
    W = getW(N, g, P, False)
    print(W)

    # (2)
    W, _, _, _ = generate_twiddle_factorS(N, P) # very slow
    print(W)
