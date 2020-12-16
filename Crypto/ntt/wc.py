# convolution and wrapped convolution

n = 5

# convolution
len_conv = 2*n-1
conv_str = ["" for _ in range(len_conv)]
for i in range(len_conv):
    tmp = "c[" + str(i) + "] =   "
    for j in range(n):
        if i-j >= 0:
            tmp += "a[" + str(j) + "]b[" + str(i-j) + "] + "
    conv_str[i] = tmp[:-3]


# negative wrapped convolution
len_nwc = n
nwc_str = ["" for _ in range(len_nwc)]
for i in range(n):
    tmp = "c[" + str(i) + "] =   "
    for j in range(i):
        if i-j >= 0:
            tmp += "a[" + str(j) + "]b[" + str(i-j) + "] + "
    tmp = tmp[:-2] + "- "
    for j in range(i+1, n):
        if n+i-j >= 0:
            tmp += "a[" + str(j) + "]b[" + str(n+i-j) + "] - "
    nwc_str[i] = tmp[:-3]

# positive wrapped convolution
len_pwc = n
pwc_str = ["" for _ in range(len_pwc)]
for i in range(n):
    tmp = "c[" + str(i) + "] =   "
    for j in range(i):
        if i-j >= 0:
            tmp += "a[" + str(j) + "]b[" + str(i-j) + "] + "
    for j in range(i+1, n):
        if n+i-j >= 0:
            tmp += "a[" + str(j) + "]b[" + str(n+i-j) + "] + "
    pwc_str[i] = tmp[:-3]

# compare
for i in range(len_nwc):
    print(conv_str[i])
    print(nwc_str[i])
    print(pwc_str[i])
    print()
