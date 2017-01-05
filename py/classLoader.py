# -*- coding:utf-8 -*-
from sys import argv
import parser.javaParser as jp

# 每个被装载的类，虚拟机都会为它创建一个java.lang.Class类的实例
classes = {}
_self_class = None

# 装载阶段 - 查找并装载类型的二进制数据
# 根据java class名称读取相应java class文件的内容
def load(path):
	global _self_class
	data = []
	with open(path,'rb') as _file:
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
	_self_class = jp.javap(data)
	# 每个被装载的类，虚拟机都会为它创建一个java.lang.Class类的实例
	classes[_self_class.this_class]=_self_class
	# return data

# 验证阶段 - 确保被导入类型的正确性
def verity():
	# 1.文件格式验证：是否以魔数开头、版本号是否在正确范围、常量池中是否有不支持的常量类型等
	# 2.元数据验证：子类是否继承了final方法、是否实现了父类或接口必要的方法、子类与父类是否有字段或方法冲突等
	# 3.字节码验证：字段类型是否匹配、方法体中的代码是否会跳转越界、方法体中的类型转换是否有效等
	# 4.符号引用验证：全限定名是否能对应到具体类、类，字段和方法访问权限等
	pass

# 准备阶段 - 为类或接口的静态字段分配空间,并用默认值初始化这些字段
# 数值类型 -> 0，boolean类型 -> False，char -> '\u0000'，reference类型 -> None
def preparation():
	# 1.非final的静态字段 : 正常赋予静态变量初始值
	# 2.final+static字段 : 直接从其ContentValue属性中取出值来做初始化
	pass

# 解析阶段 - 把类型中的符号引用转化为直接引用，可以在指令anewarray、checkcast、getfield、getstatic、instanceof等的触发下执行
# 说一句：在这里我们一步到位，加载过程直接到初始化阶段，不用指令这些指令来触发。
def resolution():
	# 1.类或接口的解析
	# 2.字段的解析
	# 3.类方法的解析
	# 4.接口方法的解析
	pass

# 初始化阶段 - 把类变量初始化为正确的初始值，执行类构造器<clinit>方法，如果有父类，则需要先执行父类的<clinit>方法
# 注意接口的情况，只有当子接口或者实现类用到了父接口的静态变量时，才需要执行父接口的<clinit>方法，如果父接口有的话。
def clinit():
	pass

# 类的实例化 - 执行类的实例构造函数<init>，由new等指令来触发
def init():
	pass

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
	path = '../cls/test_no_clinit.class'
	print "The class path is [%s]." % path
	# 如果path不为空
	if path:
		load(path)
		# _class = jp.javap(data)
		print '===============following is class================'
		print _self_class.this_class
		print _self_class.__dict__
		print isInterface()
		print _self_class.cp_info
		method_info = _self_class.method_info
		for x in _self_class.field_info:
			print x.__dict__
			for y in x.attributes:
				print y.__dict__
		print '===============following is method================'
		for x in method_info:
			print x.name
			print x.code.__dict__
