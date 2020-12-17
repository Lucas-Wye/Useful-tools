'''
Author: Lucas Wye
Date: 2020-12-17 10:46:54
Description: 
'''
#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: JimruEaster<295140325@qq.com>
# Created on 2017-09-11 16:59

from lib.prime import *


# Get Euler Func
# param int n: an integer
# return int
def get_euler(n):
    if is_prime(n):
        return n-1
    else:
        cnt = 0
        for i in range(n):
            if is_co_prime(i, n):
                cnt += 1
        return cnt
