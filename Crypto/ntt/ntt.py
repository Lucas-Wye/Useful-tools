#coding=utf-8
'''
Author: Lucas Wye<lucas.zw.ye@outlook.com>
Date: 2021-01-08 16:57:37
Description: 查看不同阶段ntt的输入输出
'''

from math import log
from generate_prime import *

def check_power_of_two(n):
    return (not (n & (n-1))) and n


def barrett_parameter(q):
    k = 2 * (int(log(q, 2))+1)
    m = int(2 ** k / q)
    return k, m

def barrett_reduction(z, q, k, m):
    t = (z * m) >> k
    z = z - (t * q)
    if z >= q:
        z = z - q
    if z < 0:
        z = z + q
    return z

def barrett_mut_reduction(x, y, q, k, m):
    return barrett_reduction(x * y, q, k, m)


# Cooley-Tukey Butterfly Structure
# A0,A1: input coefficients
# W: twiddle factor
# q: modulus
# B0,B1: output coefficients
def DIT_CT_Butterfly(A0, A1, W, q):
    """
    A0 -------\--|+|-- B0
               \/
               /\
    A1 --|x|--/--|-|-- B1
    """
    k, m = barrett_parameter(q)
    M = barrett_mut_reduction(A1, W, q, k, m)
    B0 = barrett_reduction(A0 + M, q, k, m)
    B1 = barrett_reduction(A0 - M, q, k, m)
    return B0, B1


# Bit-Reverse integer
def intReverse(a, n):
    b = ('{:0'+str(n)+'b}').format(a)
    return int(b[::-1],2)

# From paper: NTTU: An Area-Efficient Low-POwer NTT-Uncoupled Architecture for NTT-Based Multiplication
# Iterative Radix-2 Decimation-in-Time (DIT) (CT) NTT - NR
# A: input polynomial (standard order)
# W: twiddle factor
# q: modulus
# B: output polynomial (bit-reversed order)
def Radix2_DIT_Iterative_NTT_NR(A,W,q):
    N = len(A)
    B = [_ for _ in A]

    cindex_1 = [[] for _ in range(int(log(N, 2)))]
    cindex_2 = [[] for _ in range(int(log(N, 2)))]
    cnt = 0

    BF_count = 0 
    for s in range(int(log(N,2)),0,-1):
        m = 2**s
        for k in range(int(N/m)):
            TW = pow(W,\
                    intReverse(k,int(log(N,2))-s)*int(m/2),\
                    q)
            for j in range(int(m/2)):
                index_1 = k*m +j
                index_2 = k*m +j +int(m/2)
                B[index_1], B[index_2] = DIT_CT_Butterfly(B[index_1],B[index_2],TW, q) 
                BF_count += 1

                cindex_1[cnt].append(index_1)
                cindex_2[cnt].append(index_2)
        cnt += 1

            
    # bit reverse
    tmp_index_1 = []
    tmp_index_2 = []
    for i in range(len(cindex_1[-1])):
        tmp_1 = cindex_1[-1][i]
        tmp_2 = cindex_2[-1][i]
        tmp_1 = intReverse(tmp_1, int(log(N,2))) 
        tmp_2 = intReverse(tmp_2, int(log(N,2))) 
        tmp_index_1.append(tmp_1)
        tmp_index_2.append(tmp_2)
    cindex_1.append(tmp_index_1)
    cindex_2.append(tmp_index_2)

    print(BF_count)
    for i in range(len(cindex_1[0])):
        for j in range(len(cindex_1)):
            print(cindex_1[j][i], cindex_2[j][i],end="\t")
        print()

    return B


# Iterative Radix-2 Decimation-in-Time (DIT) (CT) NTT - RN
# A: input polynomial (bit-reversed order)
# W: twiddle factor
# q: modulus
# B: output polynomial (standard order)
def Radix2_DIT_Iterative_NTT_RN(A,W,q): 
    N = len(A) 
    B = [_ for _ in A]

    v = int(N/2)
    m = 1
    d = 1

    index_1 = [[] for _ in range(int(log(N, 2)))]
    index_2 = [[] for _ in range(int(log(N, 2)))]
    cnt = 0
    BF_count = 0 
    while m<N:
        np = 2*m
        lp = np*(v-1)
        for k in range(m):
            TW = pow(W,k*v,q)
            j = k
            while j < (k+lp+1):
                B[j], B[j+d] = DIT_CT_Butterfly(B[j],B[j+d],TW, q) 
                BF_count += 1
                index_1[cnt].append(j)
                index_2[cnt].append(j+d)
                j = j+np
        v = int(v/2)
        m = 2*m
        d = 2*d
        cnt += 1

    # bit reverse
    tmp_index_1 = []
    tmp_index_2 = []
    for i in range(len(index_1[0])):
        tmp_1 = index_1[0][i]
        tmp_2 = index_2[0][i]
        tmp_1 = intReverse(tmp_1, int(log(N,2))) 
        tmp_2 = intReverse(tmp_2, int(log(N,2))) 
        tmp_index_1.append(tmp_1)
        tmp_index_2.append(tmp_2)
    index_1.insert(0, tmp_index_1)
    index_2.insert(0, tmp_index_2)
    print(BF_count)
    for i in range(len(index_1[0])):
        for j in range(len(index_1)):
            print(index_1[j][i], index_2[j][i],end="\t")
        print()

    return B



# Iterative Radix-2 Decimation-in-Time (DIT) (CT) NTT - NN
# A: input polynomial (standard order)
# W: twiddle factor
# q: modulus
# B: output polynomial (standard order)
def Radix2_DIT_Iterative_NTT_NN(A,W,q):
    N = len(A)
    B = [_ for _ in A]
    C = [_ for _ in A]
    # C = [0]*N

    v = int(N/2)
    m = 1
    d = int(N/2)

    if int(log(v))%2 == 0:
        nsi = True
    else:
        nsi = False

    index_1 = [[] for _ in range(int(log(N, 2)))]
    index_2 = [[] for _ in range(int(log(N, 2)))]
    cnt = 0
    BF_count = 0

    while m<N:
        l = 0
        for k in range(m):
            jf = 2*k*v
            jl = jf + v - 1
            jt = k*v

            TW = pow(W,jt,q)

            for j in range(jf,jl+1):
                if nsi:
                    C[l], C[l+int(N/2)] = DIT_CT_Butterfly(B[j],B[j+d],TW, q) 
                else:
                    B[l], B[l+int(N/2)] = DIT_CT_Butterfly(C[j],C[j+d],TW, q) 
                BF_count += 1
                index_1[cnt].append(j)
                index_2[cnt].append(j+d)

                l = l+1
        nsi = (not nsi) 
        cnt += 1
        v = int(v/2)
        m = 2*m
        d = int(d/2)

    print(BF_count)
    for i in range(len(index_1[0])):
        for j in range(len(index_1)):
            print(index_1[j][i], index_2[j][i],end="\t")
        print()
    return C

def another_DIT(n):
    # https://zjueducn-my.sharepoint.com/personal/lucas_zw_ye_zju_edu_cn/_layouts/OneNote.aspx?id=%2Fpersonal%2Flucas_zw_ye_zju_edu_cn%2FDocuments%2FNotebooks%2FMy%20Notebook%20%40%20zju.edu.cn&wd=target%28PQC.one%7CCC5317AE-695E-4D9C-BD2C-8B2061C79D76%2FNTT%7C185E72CC-68F7-4A21-B61E-B9EA439524F3%2F%29 onenote:https://zjueducn-my.sharepoint.com/personal/lucas_zw_ye_zju_edu_cn/Documents/Notebooks/My%20Notebook%20@%20zju.edu.cn/PQC.one#NTT&section-id={CC5317AE-695E-4D9C-BD2C-8B2061C79D76}&page-id={185E72CC-68F7-4A21-B61E-B9EA439524F3}&object-id={6888E231-8200-0EE5-2E9F-87107CBAED78}&45
    a = [i for i in range(n)]
    #for i in range(n):
    #    a[i]=intReverse(i, int(log(n,2)))
    #    print('a[', i ,'] =',a[i])
    index = [[] for _ in range(int(log(n,2)))]
    cnt = 0 
    m = 2 
    while m <= n:
        j = 0
        for j in range(int(m/2)):
            k = 0
            while k <= n-1:
                index[cnt].append(str(a[k+j])+' ' + str(a[k+j+int(m/2)]))
                k = k + m
        m = 2 * m
        cnt = cnt + 1
    for i in range(len(index[0])):
        for j in range(len(index)):
            print(index[j][i],end="\t")
        print()


def test_ntt(point):
    import random
    for _ in range(1):
        q_bit = random.randint(10, 32)
        q = generate_large_prime(q_bit)
        A = [random.randint(1,q) for _ in range(point)]
        B = random.randint(1,q)
        print('NR')
        r1 = Radix2_DIT_Iterative_NTT_NR(A, B, q)
        print('\nRN')
        r2 = Radix2_DIT_Iterative_NTT_RN(A, B, q)
        print('\nNN')
        r3 = Radix2_DIT_Iterative_NTT_NN(A, B, q)
        print('\nanother')
        another_DIT(16)
        #for i in range(len(r1)):
        #    if r1[i] != r2[i]:
        #        print('fail')
        #        break
test_ntt(16)        
