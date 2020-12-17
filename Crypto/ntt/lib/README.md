<!--
 * @Author: Lucas Wye
 * @Date: 2020-12-17 10:46:54
 * @Description: 
-->
# Math-Functions
Some significant functions for Diffie–Hellman Key Exchange. Such as **Prime**, **Euler**, **Primitive_root** in Python3

Python-module List
-----------------
- [prime.py](#prime)
- [euler.py](#euler)
- [primitive.py](#primitive) 

-----------------
## <a name="prime"></a> prime.py
### get_prime(min_num, max_num, reverse=False)
```
$python3 
>>> import prime
>>> print(prime.get_prime(2, 12))
>>> [2, 3, 5, 7, 11]
```

## <a name="euler"></a> euler.py
### **get_euler(n)**
```
$python3 
>>> import euler
>>> print(euler.get_euler(11))
>>> 10
```

## <a name="primitive"></a> primitive.py
### **get_primitive_root(n)**
```
$python3 
>>> import primitive
>>> print(primitive.get_primitive_root(7))
>>> [3, 5]
```

fork from https://github.com/jimrueaster/Math-Functions