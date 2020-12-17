#!/usr/bin/python3
# -#- coding:utf-8 -#-
# Author: JimruEaster<295140325@qq.com>
# Created on 2017-09-11 16:36:56

from math import sqrt


# Whether the number is prime or not
# param int n: the num waiting to be checked
# return bool
def is_prime(n):
    n = int(n)
    if 0 not in [n % i for i in range(2, int(sqrt(n))+1)]:
        return True
    else:
        return False


# Get greatest common divisor through Euclidean algorithm
# param int a: an integer
# param int b: another integer
# return int
def gcd(a, b):
    if a < b:
        a, b = b, a

    while b != 0:
        a, b = b, a % b
    return a


# Judge the two params are co_prime or not
# param int m: an integer
# param int n: another integer
# return bool
def is_co_prime(m, n):
    return gcd(m, n) == 1


# Get a list of prime numbers
# param int min_num: from where
# param int max_num: to where(include)
# param bool reverse: if True to reverse
# return list
def get_prime(min_num, max_num, reverse=False):
    lst = []
    min_num = int(min_num)
    max_num = int(max_num)+1
    candidate_range = range(min_num, max_num)

    if reverse is True:
        candidate_range = range(max_num, min_num, -1)

    for n in candidate_range:
        if n == 1:
            continue
        elif n == 2:
            lst.append(2)
        else:
            if is_prime(n):
                lst.append(n)
    return lst
