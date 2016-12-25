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
		
# 转化类型异常
class ClassCastException(Exception):
	def __init__(self, source,target):
		self.source = source
		self.target = target
	def __str__(self):
		return '%s can not case to %s' % (self.source,self.target)

# getstatic时，如果已解析的字段是一个非静态（not static）字段，getstatic指令将会抛出一个IncompatibleClassChangeError异常
class IncompatibleClassChangeError(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)
		
# 1.没有找到任何名称和描述符都与要调用的接口方法一致的方法
# 2.被调用方法是 abstract 的
class AbstractMethodError(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)
		
# 如果搜索到的方法是 native 的话,当实现代码实现代码无法绑定到虚拟机中
class UnsatisfiedLinkError(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)
		
# 1.执行 monitorexit 的线程原本并没有这个 monitor 的所有权
# 2.出现线程 T 释放管程 M 的次数比 T 持有管程 M 次数多的情况
class IllegalMonitorStateException(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)
		
# 如果 dimensions 值小于 0 的话,multianewarray 指令将会抛出一个 NegativeArraySizeException 异常
class NegativeArraySizeException(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)

# 在类、接口或者数组的符号引用最终被解析为一个接口或抽象类,new 指令将抛出 InstantiationError 异常
class InstantiationError(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)
# 如果字段声明为 final,那就只有在当前类的实例初始化方法(<clinit>)中设置当前类的 final 字段才是合法的,否则将会抛出IllegalAccessError 异常。
class IllegalAccessError(Exception):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return repr(self.arg)
		

if __name__ == '__main__':
	print '-------------'
	e = NullPointException()
	print dir(e)
	# raise NegativeArraySizeException(-2)
	

