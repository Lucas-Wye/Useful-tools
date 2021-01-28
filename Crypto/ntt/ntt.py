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
def intReverse(a,n):
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

    for s in range(int(log(N,2)),0,-1):
        m = 2**s
        for k in range(int(N/m)):
            TW = pow(W,intReverse(k,int(log(N,2))-s)*int(m/2),q)
            for j in range(int(m/2)):
                u = B[k*m+j]
                t = (TW*B[k*m+j+int(m/2)]) % q
                
                B[k*m+j]          = (u+t) % q
                B[k*m+j+int(m/2)] = (u-t) % q

    return B

def my_Radix2_DIT_Iterative_NTT_NR(A,W,q):
    N = len(A)
    B = [_ for _ in A]

    index = [[] for _ in range(int(log(N, 2)))]

    for s in range(int(log(N,2)),0,-1):
        m = 2**s
        for k in range(int(N/m)):
            TW = pow(W,intReverse(k,int(log(N,2))-s)*int(m/2),q)
            for j in range(int(m/2)):
                index_1 = k*m +j
                index_2 = k*m +j +int(m/2)

                B[index_1],B[index_2] = DIT_CT_Butterfly(B[index_1],B[index_2],TW, q) 
                index[s-1].append(str(index_1)+' '+str(index_2)) 

    for i in range(len(index[0])):
        for j in range(len(index)):
            print(index[len(index) - 1 - j][i],end="\t")
        print()
            
    return B

def test_ntt_nr():
    import random
    for _ in range(1):
        q_bit = random.randint(10, 32)
        q = generate_large_prime(q_bit)
        A = [random.randint(1,q) for _ in range(16)]
        B = random.randint(1,q)
        r1 = Radix2_DIT_Iterative_NTT_NR(A, B, q)
        r2 = my_Radix2_DIT_Iterative_NTT_NR(A,B,q)
        for i in range(len(r1)): 
            if r1[i] != r2[i]: 
                print(i, r1[i], r2[i], " fail")
                break
test_ntt_nr()        
