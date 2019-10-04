#coding=utf-8
'''
Author: Lucas Wye
Date: 2019-03-20 14:05:35
Description: read csv file and plot data
'''

import csv
import sys
import matplotlib.pyplot as plt

if(len(sys.argv)<2):
  print('usage: python plot.py csv_filename')
  exit()

# file_processing
csv_reader = csv.reader(open(sys.argv[1],'r'))
data_x = []
data_y = []
for element in csv_reader:
  data_x.append((float)(element[1]))
  data_y.append((float)(element[3])*1e12)

# plot data
#plt.plot(data_x,data_y,'c--',label='first line')
plt.plot(data_x,data_y,'b-.',label='second line')
plt.xlabel('Plot Number')
plt.ylabel('Important var')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()

'''
	1）控制颜色
	颜色之间的对应关系为
	b---blue   c---cyan  g---green    k----black
	m---magenta r---red  w---white    y----yellow
	
	2)控制线型
	符号和线型之间的对应关系
	-      实线
	--     短线
	-.     短点相间线
	：     虚点线

	3）控制标记风格
	标记风格有多种：
	.  Point marker
	,  Pixel marker
	o  Circle marker
	v  Triangle down marker 
	^  Triangle up marker 
	<  Triangle left marker 
	>  Triangle right marker 
	1  Tripod down marker
	2  Tripod up marker
	3  Tripod left marker
	4  Tripod right marker
	s  Square marker
	p  Pentagon marker
	*  Star marker
	h  Hexagon marker
	H  Rotated hexagon D Diamond marker
	d  Thin diamond marker
	| Vertical line (vlinesymbol) marker
	_  Horizontal line (hline symbol) marker
	+  Plus marker

	plt.plot(y, 'cx--', y+1, 'mo:', y+2, 'kp-.');
	plt.show()
'''
