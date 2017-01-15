# -*- coding:utf-8 -*-

from ctypes import *

# 参考 : http://www.cnblogs.com/super119/archive/2011/04/05/2005621.html
'''
测试union结构特性
结论：因为union共享内存，而且所分配的内存根据结构体里最大字段类型长度而定。所以如果此结构体有
int字段和byte字段，那么此结构体所占用的内存为4字节(int)。改变byte字段的值，就相当于是改变
int字段低8位的值，无论有几个byte字段，无论改变的是哪个byte字段的值，都只能修改int字段低8位
的值。如果有short字段，则能修改int字段低16位的值。

但是，如果union里面套一层structure，则可以完美的实现int高地位分离，甚至ip自动分割，甚屌
'''
class PyObject(Structure):
	_fields_ = [
		('ll',c_ushort),
		('l',c_ushort),
		('h',c_ushort)
	]

class PyIp(Union):
	_fields_ = [
		('ip',c_uint32),
		('ah',c_ushort),
		('al',c_ushort),
		('o',PyObject) # union里面套一层structure
	]



# 返回32位整数，高16位和低16位的值
def high_low(i32):
	high = i32 >> 16
	low = i32 & int('00000000000000001111111111111111',2)
	source = (high << 16) | low
	print 'source:%d , high:%d , low:%d' % (source,high,low)

if __name__ == '__main__':
	p = PyIp()
	p.ip = 31895430
	print 'p.ip:',p.ip
	print 'p.au:',p.ah
	print 'p.al:',p.al
	print 'p.o.h:%d , p.o.l:%d, p.o.ll:%d' % (p.o.h,p.o.l,p.o.ll)
	high_low(p.ip)
	# print dir(p)
	p.ah = 123
	print 'p.ip:',p.ip
	print 'p.au:',p.ah
	print 'p.al:',p.al
	print 'p.o.h:%d , p.o.l:%d' % (p.o.h,p.o.l)
	high_low(p.ip)
	p.al = 321
	print 'p.ip:',p.ip
	print 'p.au:',p.ah
	print 'p.al:',p.al
	print 'p.o.h:%d , p.o.l:%d' % (p.o.h,p.o.l)
	high_low(p.ip)

