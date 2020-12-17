#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: JimruEaster<295140325@qq.com>
# Created on 2017-09-12 09:33

from lib.euler import *


# Judge whether a is m's primitive root
# param int m: the mod num
# param int a: the candidate root
# return bool
def is_primitive_root(m, a):
    if m <= 0:
        raise Exception('m should be positive')
    m = int(m)
    a = int(a)
    result_set = {a**o % m for o in range(1,m)}
    if get_euler(m) == len(result_set):
        return True
    else:
        return False


# Get the list of primitive root
# param int m: the mod num
# return list
def get_primitive_root(m):
    primitive_list = []
    m = int(float(m))
    for a in range(m):
        if is_primitive_root(m, a):
            primitive_list.append(a)
    return primitive_list


# Get one of primitive root
# param int m: the mod num
# return int
def get_one_primitive_root(m):    
    m = int(float(m))
    for a in range(m):
        if is_primitive_root(m, a):
            return a
