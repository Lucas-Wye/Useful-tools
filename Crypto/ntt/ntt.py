'''
Author: Lucas Wye<lucas.zw.ye@outlook.com>
Date: 2021-01-08 16:57:37
Description: 查看不同阶段ntt的输入输出
'''
n = 256
m = 2
while m <= n:
    
    
    count = 0
    j = 0
    while j <= m//2 -1:
        k = 0
        while k <= n-1:            
            print((k+j) % n, (k+j+m//2) % n)
            k += m
            count += 1
        j += 1   
    print("\nstage:", m, "count =", count)         
    m = 2*m
