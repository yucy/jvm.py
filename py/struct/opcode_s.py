# -*- coding:utf-8 -*-
'''
说明：此模块中的结构用于指令附属功能实现
'''
import sys,threading
sys.path.append('..')

from lang.myexceptions import *
from Queue import Queue


# 配合实现monitorenter指令
class Monitor(object):
	def __init__(self, count=0,owner=None):
		self.count = count
		self.owner = owner
		self.queue = Queue() # Queue(3) 这样可以指定queue的最大长度为3,不写参数表示最大长度为INT_MAX
		self.__thread_lock = threading.Lock() 

	# owner是线程
	def isOwner(self,_owner):
		return self.owner is _owner

	def isLock(self):
		return self.count > 0 or self.owner is not None

	def isUnLock(self):
		return not self.isLock()

	def __unLock(self,_owner):
		if self.owner is not _owner:
			raise IllegalMonitorStateException(_owner)
		self.owner=None
		self.count =0
		if not self.queue.empty():
			self.__lock()

	def unLock(self,_owner):
		if self.count == 0:
			raise IllegalMonitorStateException(-1)
		self.count -= 1
		# 如果减 1 后计数器值为 0,那线程退出 monitor,不再是这个 monitor 的拥有者
		if self.count == 0:
				self.__unLock(_owner)

	def lock(self,_owner):
		if _owner is None:
			return 'param[owner] is None'
		else:
			# 用队列来实现wait
			self.__lock(_owner)

	def __lock(self,_owner=None):
		# with self:字面意思呢就是通过自己返回一个上下文管理器对象,上下文管理器里面要有__enter__()和__exit__()方法
		# 其实python已经内建支持with语句来自动关闭文件和线程锁的自动获取和释放，用法为:with open(r'somefileName')和with threading.Lock()
		# 但是本人觉得每次来获取一个lock对象比较浪费，还是一个monitor分配一个threading_lock比较省空间。
		with self :
			print 'Lock:', self.isLock(),', _owner:', self.owner is _owner
			# 需要可重入，同一个owner是可以进入lock的
			if self.isUnLock() or self.owner is _owner:
				if _owner is None:
					_owner = self.queue.get()
				print '%s get lock' % _owner
				self.owner=_owner
				self.count += 1
			elif _owner is not None:
				self.queue.put(_owner)


	# __enter__和__exit__配合起来用于实现with,类似java中的AOP
	# 这样的过程其实等价于：
	# try:
	# 执行 __enter__的内容
	# 执行 with_block.
	# finally:
	# 执行 __exit__内容

	# 这个方法的返回值将被赋值给as后面的变量,example:with open("/tmp /foo.txt") as file
	def __enter__(self):
		# print '__enter__,cannotLock', self.isLock()
		self.__thread_lock.acquire()

	def __exit__(self,_type,value,traceback):
		self.__thread_lock.release()
		# print '__exit__'
		# print "type:", _type
        # print "value:", value
        # print "trace:", traceback