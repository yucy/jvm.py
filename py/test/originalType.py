# -*- coding:utf-8 -*-
import sys
from ctypes import *

class PyObject(Structure):
	_fields_ = [
		('refcnt',c_size_t),
		('typeid',c_voidp)
	]

class PyByte(PyObject):
	_fields_ = [('val',c_byte)]

class PyChar(PyObject):
	_fields_ = [('val',c_char)]

class PyShort(PyObject):
	_fields_ = [('val',c_short)]

class PyInt(PyObject):
	_fields_ = [('val',c_int32)]

		
if __name__ == '__main__':
	a = 'this is a string'
	# PyObject.from_address()可以将指定的内存地址的内容转换为一个 PyObject 对象。通过此 PyObject 对象obj_a 可以访问对象 a 的结构体中的内容
	obj_a = PyObject.from_address(id(a))
	obj_str = PyObject.from_address(id(str))
	print obj_a.refcnt
	print obj_str.refcnt
	b = [a]*10
	print b 
	print obj_a.refcnt
	print obj_a.typeid
	# print type(a)
	# print str
	# print id(type(a))
	# print id(str)
	# print id(type(str))
	# print isinstance(a,str)
	# print dir(a)
	# print dir(obj_a)
	print '=========================================='
	b = 127
	bb = c_byte(127)
	obj_b = PyByte.from_address(id(b))
	print obj_b.val
	obj_bb = PyByte(12)
	print obj_bb.val
	print 'bb.value:',bb.value
	print 'bb.size:',bb.__sizeof__()
	print dir(c_byte)
	print sys.getsizeof(b)
	print sys.getsizeof(bb)
	print sys.getsizeof(obj_str)


