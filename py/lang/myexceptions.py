# -*- coding:utf-8 -*-
# 之所以模块名称前面加上了下划线，是因为python标准库里已经有了此模块，如果不稍加改动，就会报错：ImportError: cannot import name XXX

# 引用为空的异常
class NullPointException(Exception):
	# arg is error msg
	def __init__(self, arg="Null"):
		self.arg = arg

	def __str__(self):
		return repr(self.arg)

# 数组越界
class ArrayIndexOutOfBoundsException(Exception):
	# arg is array's index
	def __init__(self, arg=0):
		self.arg = arg

	def __str__(self):
		return repr(self.arg)

# 数组类型不匹配
class ArrayStoreException(Exception):
	# arg is array's index
	def __init__(self, arg):
		self.arg = type(arg)

	def __str__(self):
		return repr(self.arg)


# 数组初始化长度小于零
class NegativeArraySizeException(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)

# 如果虚拟机实现没有严格执行在§2.11.10 中规定的结构化锁定规则,导致当前方法是一个同步方法,但当前线程在调用方法时没有成功持有(Enter)
# 或重入(Reentered)相应的管程,那 areturn 指令将会抛出IllegalMonitorStateException 异常。这是可能出现的,譬如一个同步
# 方法只包含了对方法同步对象的 monitorexit 指令,但是未包含配对的monitorenter 指令
class IllegalMonitorStateException(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)
		
# checkcast
class ClassCastException(Exception):
	def __init__(self, source,target):
		self.source = source
		self.target = target
	def __str__(self):
		return '%s can not case to %s' % (self.source,self.target)

if __name__ == '__main__':
	print '-------------'
	e = NullPointException()
	print dir(e)
	raise NegativeArraySizeException(-2)

