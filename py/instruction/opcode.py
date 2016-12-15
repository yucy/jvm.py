# -*- coding:utf-8 -*-
# LIFO类似于堆,即先进后出
from Queue import LifoQueue

# stack[] operation set
class Stack(object):
	"""docstring for stack"""
	def __init__(self, maxsize):
		if maxsize > 65535:
			raise BaseException('StackOverflowError')
		self.queue = LifoQueue(maxsize)
	def pop(self):
		isEmpty = self.queue.empty()
		if isEmpty:
			raise BaseException('this stack is null ')
		else:
			return self.queue.get()

	def push(self,value):
		isFull = self.queue.full()
		if isFull:
			raise BaseException('this stack is full')
		else:
			self.queue.put(value)

	def list(self):
		return self.queue.queue
# ['__doc__', '__init__', '__module__', '_get', '_init', '_put', '_qsize', 
# 'all_tasks_done', 'empty', 'full', 'get', 'get_nowait', 'join', 'maxsize', 
# 'mutex', 'not_empty', 'not_full', 'put', 'put_nowait', 'qsize', 'queue', 
# 'task_done', 'unfinished_tasks']

class Opcode(object):
	"""docstring for Opcode"""
	def __init__(self,arg):
		self.stack = arg
		
	def do(self,code,*args):
		func = getattr(self,code)
		# execute operate code
		func()

	def aaload(self):
		# ...,arrayref,index →
		# ...,value
		index = self.stack.pop()
		arrayref = self.stack.pop()
		value = arrayref[index]
		self.stack.push(value)
		print 'aaload ----'

if __name__ == '__main__':
	q = Stack(3)
	arr = [11,22,33]
	q.push(arr)
	q.push(1)
	print q.list()
	o = Opcode(q)
	o.do('aaload')
	print q.list()
	# q = LifoQueue(3)
	# print dir(q)
	# q.put(1)
	# q.put(2)
	# print q.get()
	# stack = Stack(65536)
	# stack.push(1)
	# stack.push(2)
	# stack.push(3)
	# stack.push(4)
	# print stack.pop()
	# print stack.pop()
	# print stack.pop()
	# print stack.pop()
	# print stack.pop()