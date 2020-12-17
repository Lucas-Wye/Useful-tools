'''
Author: Lucas Wye
Date: 2020-10-16 14:07:32
Description: 
    J. Wolkerstorfer, E. Oswald, and M. Lamberger, “An ASIC Implementation of the AES SBoxes,” 
    in Topics in Cryptology — CT-RSA 2002, Berlin, Heidelberg, 2002, pp. 67–78, doi: 10.1007/3-540-45760-7_6.

    https://doi.org/10.1007/3-540-45760-7_6
'''

def get_bit_val(byte, index):
    """
    得到某个字节中某一位（Bit）的值

    :param byte: 待取值的字节值
    :param index: 待读取位的序号，从右向左0开始，0-7为一个完整字节的8个位
    :returns: 返回读取该位的值，0或1
    """
    if byte & (1 << index):
        return 1
    else:
        return 0

def restore_from_bits(bits):
    res = 0    
    for index in range(len(bits)):
        bit = bits[index]
        if bit == 0:            
            pass
        elif bit == 1:
            res += 2**index
    return res

def bit_not(a):    
    return a ^ 1

def aff_trans(a):    
    a_A = a[0] ^ a[1]
    a_B = a[2] ^ a[3]
    a_C = a[4] ^ a[5]
    a_D = a[6] ^ a[7]    
    q = [0 for index in range(8)]    
    
    q[0] = bit_not(a[0]) ^ a_C ^ a_D    
    q[1] = bit_not(a[5]) ^ a_A ^ a_D    
    q[2] =  a[2] ^ a_A ^ a_D
    q[3] =  a[7] ^ a_A ^ a_B
    q[4] =  a[4] ^ a_A ^ a_B
    q[5] = bit_not(a[1]) ^ a_B ^ a_C
    q[6] = bit_not(a[6]) ^ a_B ^ a_C
    q[7] =  a[3] ^ a_C ^ a_D

    return q

def true_aff_trans(a, c):   
    q = [0 for index in range(8)]
    for i in range(len(a)):
        q[i] = a[i] ^ a[(i+4) % 8] ^ a[(i+5) % 8] ^ a[(i+6) % 8] ^ a[(i+7) % 8] ^ c[i]
    return q        


a = 0x1c # input
c = 0x63 # constant
binary_a = [get_bit_val(a, index) for index in range(8)]
binary_c = [get_bit_val(c, index) for index in range(8)]

binary_res = aff_trans(binary_a)
res = restore_from_bits(binary_res)

binary_res_true = true_aff_trans(binary_a, binary_c)
res_true = restore_from_bits(binary_res_true)

if res == res_true:
    print("test pass")
