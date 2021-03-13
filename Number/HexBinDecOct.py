#coding=utf-8

format = int(input('The number format: '))
while True:
    i = int(input('The number: '), format)
    print(bin(i))
    print(i)
    print(hex(i))
    print()

