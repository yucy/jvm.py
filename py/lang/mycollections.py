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

	# 栈顶元素出栈，并将其返回
	def pop(self):
		isEmpty = self.queue.empty()
		if isEmpty:
			self.throw('this stack is null ')
		else:
			return self.queue.get()

	# 推送一个元素至栈顶
	def push(self,value):
		isFull = self.queue.full()
		if isFull:
			self.throw('this stack is full')
		else:
			self.queue.put(value)

	def throw(self,msg):
		raise BaseException(msg)

	# 获取queue的队列内容
	def list(self):
		return self.queue.queue

	# 清空队列
	def clear(self):
		isEmpty = self.queue.empty()
		if not isEmpty:
			self.queue.get()
			self.clear()

# ['__doc__', '__init__', '__module__', '_get', '_init', '_put', '_qsize', 
# 'all_tasks_done', 'empty', 'full', 'get', 'get_nowait', 'join', 'maxsize', 
# 'mutex', 'not_empty', 'not_full', 'put', 'put_nowait', 'qsize', 'queue', 
# 'task_done', 'unfinished_tasks']

# 类似于java里面的数组，限定元素类型和长度
class Array(object):
	def __init__(self, _size,_type=object):
		self.size = _size
		# if size <0, throw exception
		self.__verify_size()
		self.type = _type
		self._element = [None]*_size

	def __len__(self):
		return self.size

	def __getitem__(self,index):
		self.__verify_index(index)
		return self._element[index]

	def __setitem__(self,index,value):
		self.__verify_index(index)
		self.__verify_value(value)
		self._element[index] = value

	# 验证size，前面两个下划线说明是private方法
	def __verify_size(self):
		if self.size < 0:
			raise NegativeArraySizeException(self.size)

	# 验证index是否有效
	def __verify_index(self,index):
		if index is None:
			raise NullPointException()
		if index >= len(self) or index < 0:
			raise ArrayIndexOutOfBoundsException(index)

	# 验证value是否有效
	def __verify_value(self,value):
		# TODO 后续还需要判断接口实现和类继承的判断
		if value is not None and not isinstance(value,self.type):
			raise ArrayStoreException(value)

# TODO 类似于java里面的多维数组，限定元素类型,维数和长度
# 参考http://blog.csdn.net/linzhiqiang0316/article/details/51602433
# 在运行时常量池中确定的数组类型维度可能比操作数栈中 dimensions 所代表的维度更高,在这种情况下,multianewarray 指令只会创建数组的第一个维度。
class MultiArray(object):
	def __init__(self, _dimension,_type=object,*_size):
		# 一个新的多维数组将会被分配在 GC 堆中,如果任何一个 count 值为 0,那就
		# 不会分配维度。数组第一维的元素被初始化为第二维的子数组,后面每一维都
		# 依此类推。数组的最后一个维度的元素将会被分配为数组元素类型的初始值
		self.size = _size
		# if size <0, throw exception
		self.__verify_size()
		if _dimension <= 0:
			raise NegativeArraySizeException(_dimension)
		self.type = _type
		self.dimension = _dimension
		self._element = [None]*_size

	def __len__(self):
		return self.size

	def __getitem__(self,index):
		self.__verify_index(index)
		return self._element[index]

	def __setitem__(self,index,value):
		self.__verify_index(index)
		self.__verify_value(value)
		self._element[index] = value

	# 验证size，前面两个下划线说明是private方法
	def __verify_size(self):
		if self.size < 0:
			raise NegativeArraySizeException(self.size)

	# 验证index是否有效
	def __verify_index(self,index):
		if index is None:
			raise NullPointException()
		if index >= len(self) or index < 0:
			raise ArrayIndexOutOfBoundsException(index)

	# 验证value是否有效
	def __verify_value(self,value):
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

