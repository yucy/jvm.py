# -*- coding:utf-8 -*-
# 之所以模块名称前面加上了下划线，是因为python标准库里已经有了此模块，如果不稍加改动，就会报错：ImportError: cannot import name XXX

# LIFO类似于堆,即先进后出
from Queue import LifoQueue
from myexceptions import *


# stack[] operation set
class Stack(object):
	"""docstring for stack"""
	def __init__(self, maxsize):
		if maxsize > 65535:
			self.throw('StackOverflowError')
		self.queue = LifoQueue(maxsize)
	def pop(self):
		isEmpty = self.queue.empty()
		if isEmpty:
			self.throw('this stack is null ')
		else:
			return self.queue.get()

	def push(self,value):
		isFull = self.queue.full()
		if isFull:
			self.throw('this stack is full')
		else:
			self.queue.put(value)

	def throw(self,msg):
		raise BaseException(msg)

	def list(self):
		return self.queue.queue

	def clear(self):
		isEmpty = self.queue.empty()
		if not isEmpty:
			self.queue.get()
			self.clear()

# ['__doc__', '__init__', '__module__', '_get', '_init', '_put', '_qsize', 
# 'all_tasks_done', 'empty', 'full', 'get', 'get_nowait', 'join', 'maxsize', 
# 'mutex', 'not_empty', 'not_full', 'put', 'put_nowait', 'qsize', 'queue', 
# 'task_done', 'unfinished_tasks']


class Array(object):
	def __init__(self, _size,_type=object):
		self.size = _size
		# if size <0, throw exception
		self.__size()
		self.type = _type
		self._element = [None]*_size

	def __len__(self):
		return self.size

	def __getitem__(self,index):
		self.__index(index)
		return self._element[index]

	def __setitem__(self,index,value):
		self.__index(index)
		self.__value(value)
		self._element[index] = value

	def __size(self):
		if self.size < 0:
			raise NegativeArraySizeException(self.size)

	def __index(self,index):
		if index is None:
			raise NullPointException()
		if index >= len(self) or index < 0:
			raise ArrayIndexOutOfBoundsException(index)

	def __value(self,value):
		# TODO 后续还需要判断接口实现和类继承的判断
		if value is not None and not isinstance(value,self.type):
			raise ArrayStoreException(value)

		
def test(msg='aaaa'):
	print msg

if __name__ == '__main__':
	l = Array(2,int)
	l[0] = 1
	l[1] = None
	print l.__dict__
	# l.__setitem__(2,11)
	# print dir(l)
	# test()

	q = Stack(3)
	arr = [11,22,33]
	q.push(arr)
	q.push(1)
	print q.list()
	q.clear()
	print q.list()

