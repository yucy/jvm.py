# -*- coding:utf-8 -*-
import sys
sys.path.append('..')

from common.accessFlags import checkFieldAccess
from common.base import Base
'''
说明：此模块中的结构用于java类加载、链接和初始化过程
'''

# class_info 构造 , 用于保存方法区信息
# 内容包括运行时常量池，类型信息，字段信息，方法信息，类加载器引用，Class实例引用,类变量和方法表
# XXX 为了方便，先做成充血模型吧
class ClassInfo(Base):

	# 结构定义和功能分开
	def __init__(self):
		# 运行时常量池
		self.cp_info = []
		# 类型信息
		# 1 ．类型的完全限定名
		# 2 ．类型直接超类的完全限定名 
		# 3 ．直接超接口的全限定名列表 
		# 4 ．该类型是类类型还是接口类型 
		# 5 ．类型的访问修饰符（如 public,abstract,final 等，对应 access_flags. )
		self.this_class = None
		self.super_class = None
		self.access_flags = 0
		self.interfaces = []
		
		# 字段信息
		self.field_info = []
		
		# 方法信息
		self.method_info = []

		# 类变量分为两种变量： (注意类变量和实例变量的区别)
		# 1 ．运行时变量，static,在准备阶段就赋予默认值.
		# 2 ．编译时变量，static+属性表中存在ContentValue属性，直接赋予ContentValue的值。（如果其他类引用了此变量，
		# 直接把变量的值写进其class文件流中，这在编译时处理）
		self.class_field = {}

		# 类加载器的引用
		# 一个类可以被启动类加载器或者自定义的类加载器加载，如果一个类被某个自定义类加载器的对象（实例）加载，
		# 则方法区中必须保存对该对象的引用。注意：如果是被JVM内部加载器加载，则此项为None
		self.classLoader = None

		# 指向 Class 实例的引用
		# 在加载过程中，虚拟机会创建一个代表该类型的 Class 对象，方法区中必须保存对该对象的引用
		# TODO execute Class.init()
		self.Class = None

		# 方法表
		# 为了提高访问效率，必须仔细的设计存储在方法区中的数据信息结构。除了以上讨论的结构，JVM 的实现者还可以添加一些其他
		# 的数据结构，如方法表。 jvm 对每个加载的非虚拟类的类型信息中都添加了一个方法表，方法表是一组对类实例方法的直接引用
		# （包括从父类继承的方法）。 jvm 可以通过方法表快速激活实例方法．
		# TODO
		self.methodTable = []

	def initBaseInfo(self,_classFile):
		# 运行时常量池
		self.cp_info = _classFile['cp_info']
		# 类型信息
		# 1 ．类型的完全限定名
		# 2 ．类型直接超类的完全限定名 
		# 3 ．直接超接口的全限定名列表 
		# 4 ．该类型是类类型还是接口类型 
		# 5 ．类型的访问修饰符（如 public,abstract,final 等，对应 access_flags. )
		self.this_class = _classFile['this_class']
		self.super_class = _classFile['super_class']
		self.access_flags = _classFile['access_flags']
		self.interfaces = _classFile['interfaces']
		# 字段信息
		self.field_info = [FieldInfo(i) for i in _classFile['field_info']]
		# 方法信息
		self.method_info = [MethodInfo(i) for i in _classFile['method_info']]

	# 初始化类变量，其实也是准备阶段要做的事情
	def initClassField(self,_classFile):
		for field in _classFile['field_info']:
			access_flags = field['access_flags']
			if checkFieldAccess('STATIC',access_flags):
				print field
				_type = arg['descriptor']
				tempValue = None
				for attr in field.attributes:
					# 'info': {'value': ['ss_67890']}, 'attribute_name': 'ConstantValue'
					if attr['attribute_name'] == 'ConstantValue':
						tempValue = attr['info']['value'][0] # TODO 取值太麻烦，需要优化
						break
				if tempValue is None:
					if _type in ['B','S','I','L']:
						tempValue = 0
					elif _type in ['D','F']:
						tempValue = 0.0
					elif _type == 'C':
						tempValue = b'0'
					elif _type == 'Z':
						tempValue = False
				self.class_field[field['name']] = tempValue


	# 返回方法信息 -> 方法表
	'''
	const char* szMethodName
	const char* szDescriptor
	bool bFindFromBaseClass=true
	'''
	def findMethodInfo(self):
		return "method_info"

	# 是否是接口
	def isInterface(self):
		return self.access_flags.__contains__('ACC_INTERFACE')

	# 是否是抽象类
	def isAbstract(self):
		return self.access_flags.__contains__('ACC_ABSTRACT')

# =======================================================================================================
# 字段信息,包括类级变量和实例变量，不包括局部变量
class FieldInfo(object):
	def __init__(self, arg):
		if arg is None:
			print '=======clinit FieldInfo arg is None========'
		# 1 ．字段名 
		# 2 ．字段的类型（可能是基本类型或引用类型）
		# 3 ．字段的修饰符（ pUblic 、 Static 、transient等）
		# 注意 : 字段的顺序也要保留
		self.name = arg['name']
		self.type = arg['descriptor']
		self.access_flags = arg['access_flags']
		

# =======================================================================================================
# 方法信息
class MethodInfo(object):
	def __init__(self, arg):
		if arg is None:
			print '=======clinit FieldInfo arg is None========'
		# 1 ．方法名
		# 2 ．方法返回类型 
		# 3 ．方法参数的个数、类型和顺序等 
		# 4 ．方法的修饰符 
		# 5 ．方法的字节码（ bytecodes 非本地方法具有） 
		# 6 ．操作数栈和该方法在栈帧中局部变量的大小等 
		# 7 ．异常表。
		self.name = arg['name']
		self.descriptor = arg['descriptor']
		# TODO 方法参数的个数、类型和顺序等 
		# 如果以一个L开头的描述符，就是类描述符，它后紧跟着类的字符串，然后分号“；”结束
		# int j,String s,List l,double[] d ==> ILjava/lang/String;Ljava/util/List;[D
		# ()V ==> no params and return void

		self.returnType,self.args = self.__parserDescriptor()

		self.args = []
		[test(x,self.args) for x in args_temp]

		self.access_flags = arg['access_flags']
		# method's Code Attribute
		Code = arg['Code']
		self.codes = Code['codes']
		#  'max_locals': 3, 'max_stack': 2, 'exception_table_length'
		self.max_locals = Code['max_locals']
		self.max_stack = Code['max_stack']
		# 'attribute_name': 'Exceptions' {'number_of_exceptions': 1, 'exception_index_table': [['java/lang/Exception']]}
		Exceptions = arg['Exceptions']
		self.exceptions = Exceptions['exception_index_table']

	# 方法参数的个数、类型和顺序等 
	# 如果以一个L开头的描述符，就是类描述符，它后紧跟着类的字符串，然后分号“；”结束
	# int j,String s,List l,double[] d ==> ILjava/lang/String;Ljava/util/List;[D
	# ()V ==> no params and return void
	# (I)Ljava/lang/String; ==> params:int and return string
	def __parserDescriptor(self):
		args_returnType = self.descriptor[1:].split(')')
		returnType = []
		[self.__parserArgs(x,returnType) for x in args_returnType[1].split(';')]

		args_temp = args_returnType[0].split(';')
		args = []
		[self.__parserArgs(x,args) for x in args_temp]
		return returnType[0],args


	def __parserType(self,temp,result):
		if len(temp) == 0:
			return
		head = temp[:1]

		if head == 'L':
			result.append(temp[1:])
		elif head == '[': # TODO 暂时只处理一维数组
			result.append(head + temp[1:2])
			self.__parserArgs(temp[1:],result)
		else:
			result.append(head)
			self.__parserArgs(temp[1:],result)

def test(args_temp,result):
	if len(args_temp) == 0:
		return
	head = args_temp[:1]

	if head == 'L':
		result.append(args_temp[1:])
	elif head == '[': # TODO 暂时只处理一维数组
		result.append(head + args_temp[1:2])
		test(args_temp[1:],result)
	else:
		result.append(head)
		test(args_temp[1:],result)

if __name__ == '__main__':
	descriptor = '(ILjava/lang/String;Ljava/util/List;[D[Ljava/lang/String;)Ljava/lang/String;'
	temp = descriptor[1:].split(')')
	print temp
	method = []
	print temp[1]
	[test(x,method) for x in temp[1].split(';')]
	print '============',method

	args_temp = temp[0].split(';')
	print args_temp
	args = []
	for x in args_temp:
		test(x,args)
	print args
	tt = []
	[test(x,tt) for x in args_temp]
	print tt
		

			




# =======================================================================================================
'''
method_argtype={
	'B': BYTE, # 有符号字节型数
	'C': CHAR, # Unicode 字符,UTF-16 编码
	'D': DOUBLE, # 双精度浮点数
	'F': FLOAT, # 单精度浮点数
	'I': INT, # 整型数
	'J': LONG, # 长整数
	'S': SHORT, # 有符号短整数
	'Z': BOOLEAN, # 布尔值 true/false
	'L': REFERENCE, #;  一个名为<Classname>的实例,e.g.: Ljava/lang/String;Ljava/util/List;
	'[': ARRAY, # 一个一维数组,e.g.:[D -> double[] 
}
'''