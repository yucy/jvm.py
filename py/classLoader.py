# -*- coding:utf-8 -*-
from sys import argv
import parser.javaParser as jp

# 每个被装载的类，虚拟机都会为它创建一个java.lang.Class类的实例
classes = {}
_self_class = None

# 根据java class名称读取相应java class文件的内容
def readClassFile(path):
	global _self_class
	data = []
	with open(path,'rb') as _file:
		data = printClassFile(_file)
	_self_class = jp.javap(data)
	# 每个被装载的类，虚拟机都会为它创建一个java.lang.Class类的实例
	classes[_self_class.this_class]=_self_class
	# return data

# 打印读入的class文件内容
def printClassFile(_file):
	#for line in _file:
	#	print line
	#_file.seek(0,0) #定位到文件开头，offset->0
	data = []
	while True:
		b = _file.read(1)
		# 到达文件结尾，直接跳出
		if len(b) == 0:
			break
		# 回车符直接打印，不需要转码【被自己坑，class里面就没有一个多余的字符】
		# elif b == '\n':
		# 	print 'line is end'
		# 	data.append(b)
		#将编码转化为16进制数据添加进data数组
		else:
			data.append('0x%.2x' % ord(b)) # "0x%.2X" % ord(b)
			# data.append('%.2d' % ord(b))
	# 此处不用range，是因为range直接返回一个list，如果class文件很大的话，需要分配很多内存空间，性能不佳；
	# 而xrange只是返回一个生成器【每请求一次就返回+1的数字】，list(xrange(5)) 效果等同于 range(5)
	# print data
	# for x in xrange(0,len(data)):
	# 	#为了格式整齐，每十六个输出一个换行
	# 	if x%16 == 0:
	# 		print
	# 	# 尾部加上逗号，是为了打印不换行
	# 	print data[x],
		
		# temp = jp.inner_cmd.get(data[x],data[x])
		# if temp == 'nop':
		# 	continue
		# print temp
	return data	


# 默认执行该class文件的main方法
def execute():
	print 234
	return False or True

# 执行该class文件中指定方法名和方法描述符的方法
'''
bool bMustFindMethod
const char* szMethodName
const char* szDescriptor
bool bFromBaseClass=true
word objref=null
'''
def executeMethod():
	return False or True

# 返回方法信息
'''
const char* szMethodName
const char* szDescriptor
bool bFindFromBaseClass=true
'''
def findMethodInfo():
	return "method_info"

# 是否是给定class名的子类
# const char* szBaseClassName
def isDerivedClassOf(szBaseClassName):
	return False or True

# 是否是给定class名的子类
# CClassFile* pBaseClassFile
def isDerivedClassOf(pBaseClassFile):
	return False or True

# 是否是给定class名的父类
# const char* szDerivedClassName
def isBaseClassOf(szDerivedClassName):
	return False or True

# 是否是给定class名的父类
# CClassFile* pDerivedClassFile
def isBaseClassOf(pDerivedClassFile):
	return False or True

# 是否是接口
def isInterface():
	return _self_class.access_flags.__contains__('ACC_INTERFACE')

# 是否是抽象类
def isAbstractClass():
	return _self_class.access_flags.__contains__('ACC_ABSTRACT')

# 程序入口
if __name__=="__main__":
	# argv,第一个参数是python后面算起的，我们的启动命令是：python py/classLoader.py cls/demo.class
	# 很显然，我们要读取的是class文件，是第二个参数，故而我们用argv[1]
	# path = argv[1]
	# path = '/home/yucy/git/jvm.py/cls/demo.class'
	# path = 'e:/git/github/jvm.py/cls/demo.class'
	path = '../cls/test.class'
	print "The class path is [%s]." % path
	# 如果path不为空
	if path:
		readClassFile(path)
		# _class = jp.javap(data)
		print '============================='
		print _self_class.this_class
		print _self_class.__dict__
		print isInterface()
		method_info = _self_class.method_info
		for x in method_info:
			print x.name
			print x.code.__dict__