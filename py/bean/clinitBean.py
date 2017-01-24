# -*- coding:utf-8 -*-
import sys
sys.path.append('..')

from common.accessFlags import checkFieldAccess
from common.base import Base
from common.content import constant_type

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
		self.classFile = _classFile
		# 运行时常量池
		self.cp_info = self.classFile.cp_info
		# 类型信息
		# 1 ．类型的完全限定名
		# 2 ．类型直接超类的完全限定名 
		# 3 ．直接超接口的全限定名列表 
		# 4 ．该类型是类类型还是接口类型 
		# 5 ．类型的访问修饰符（如 public,abstract,final 等，对应 access_flags. )
		self.this_class = self.classFile.this_class
		self.super_class = self.classFile.super_class
		self.access_flags = self.classFile.access_flags
		self.interfaces = self.classFile.interfaces
		# 字段信息
		self.field_info = [FieldInfo(i) for i in self.classFile.field_info]
		# 方法信息
		self.method_info = [MethodInfo(i) for i in self.classFile.method_info]

	# 初始化类变量，其实也是准备阶段要做的事情
	def initClassField(self):
		for field in self.classFile.field_info:
			access_flags = field.access_flags
			if checkFieldAccess('STATIC',access_flags):
				_type = field.descriptor
				tempValue = None
				for attr in field.attributes:
					# 'info': {'value': ['ss_67890']}, 'attribute_name': 'ConstantValue'
					if attr.attribute_name == 'ConstantValue':
						# print '===============',attr.info
						tempValue = attr.info
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
				self.class_field[field.name] = tempValue

	# 将常量池中的符号引用转换为直接引用，主要是针对常量池中的类，字段和方法
	# 对于指向“类型”【Class对象】、类变量、类方法的直接引用可能是指向方法区的本地指针
	# https://www.zhihu.com/question/30300585?sort=created
	def handlerCpinfo(self):
		
		# 导入放在这里是防止模块初始化时的导入循环，也可以放到方法体中
		from bootstrap import Bootstrap
		for index,tag in enumerate(self.classFile.cp_tag):
			# Class ,Fieldref ,Methodref ,InterfaceMethodref
			if tag not in [7,9,10,11]:
				continue	
			# print tag,constant_type.get(tag),self.classFile.cp_info[index]
			# TODO 其他模块的getContent方法可以删掉
			res = self.__searchContent(index)
			# print res
			# class eg:java/lang/System
			if tag == 7:
				# if not Base.methodArea.has_key(_class_path):
				# 	print '=======has Bootstrap========',_class_path
				# 	# TODO 处理class文件之后还需要加载class进方法区，bootstrap
				# print '+++++++++++++++++ClassInfo.handlerCpinfo+++++++++++++++%s' % res
				Bootstrap(res)
			# Fieldref eg:['java/lang/System', ['out', 'Ljava/io/PrintStream;']]
			# class name_and_type
			elif tag == 9:
				pass
			# Methodref eg: ['java/lang/Object', ['<init>', '()V']]
			# class name_and_type
			elif tag == 10:
				pass
			# InterfaceMethodref
			elif tag == 11:
				pass 


	# 递归深度优先来查找常量池,从常量池中获取值
	def __searchContent(self,index):
		source = self.classFile.cp_info[index]
		if isinstance(source,str) and source.__contains__('#'):
			temp = source.replace('#','')
			pointers = temp.split(',')
			target = [self.__searchContent(int(i)) for i in pointers]
			return target if len(target) > 1 else target[0]
		else:
			return source

	'''
	假设常量池项#2为一个 Methodref
	假设找到的methodblock*是0x45762300，那么常量池项#2的内容会变为：
	[00 23 76 45]
	（解析后字节序使用x86原生使用的低位在前字节序（little-endian），为了后续使用方便）
	这样，以后再查询到常量池项#2时，里面就不再是一个符号引用，而是一个能直接找到Java方法元数据
	的methodblock*了。这里的methodblock*就是一个“直接引用”。

	7:'CONSTANT_Class_info',
	9:'CONSTANT_Fieldref_info',
	10:'CONSTANT_Methodref_info',
	11:'CONSTANT_InterfaceMethodref_info',
	'''
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

	# 是否是给定class名的子类
	# const char* szBaseClassName
	def isDerivedClassOf(self,szBaseClassName):
		return False or True

	# 是否是给定class名的子类
	# CClassFile* pBaseClassFile
	def isDerivedClassOf(self,pBaseClassFile):
		return False or True

	# 是否是给定class名的父类
	# const char* szDerivedClassName
	def isBaseClassOf(self,szDerivedClassName):
		return False or True

	# 是否是给定class名的父类
	# CClassFile* pDerivedClassFile
	def isBaseClassOf(self,pDerivedClassFile):
		return False or True

	# 移除指针，以便后期的垃圾收集
	def clearTempData(self):
		self.classFile = None

# =======================================================================================================
# 字段信息,包括类级变量和实例变量，不包括局部变量
class FieldInfo(object):
	def __init__(self, field):
		if field is None:
			print '=======clinit FieldInfo field is None========'
		# 1 ．字段名 
		# 2 ．字段的类型（可能是基本类型或引用类型）
		# 3 ．字段的修饰符（ pUblic 、 Static 、transient等）
		# 注意 : 字段的顺序也要保留
		self.name = field.name
		self.type = field.descriptor
		self.access_flags = field.access_flags
		

# =======================================================================================================
# 方法信息
class MethodInfo(object):
	def __init__(self, method):
		if method is None:
			print '=======clinit FieldInfo method is None========'
		# 1 ．方法名
		# 2 ．方法返回类型 
		# 3 ．方法参数的个数、类型和顺序等 
		# 4 ．方法的修饰符 
		# 5 ．方法的字节码（ bytecodes 非本地方法具有） 
		# 6 ．操作数栈和该方法在栈帧中局部变量的大小等 
		# 7 ．异常表。
		self.name = method.name
		self.descriptor = method.descriptor
		# TODO 方法参数的个数、类型和顺序等 
		# 如果以一个L开头的描述符，就是类描述符，它后紧跟着类的字符串，然后分号“；”结束
		# int j,String s,List l,double[] d ==> ILjava/lang/String;Ljava/util/List;[D
		# ()V ==> no params and return void

		self.returnType,self.args = self.__parserDescriptor()

		self.access_flags = method.access_flags
		self.codes = []
		self.max_locals,self.max_stack = 0,0
		# method's Code Attribute
		if method.Code is not None:
			CodeInfo = method.Code.info
			# print Code.info
			self.codes = CodeInfo['codes']
			#  'max_locals': 3, 'max_stack': 2, 'exception_table_length'
			self.max_locals = CodeInfo['max_locals']
			self.max_stack = CodeInfo['max_stack']
		# 'attribute_name': 'Exceptions' {'number_of_exceptions': 1, 'exception_index_table': [['java/lang/Exception']]}
		self.exceptions = method.Exceptions.info['exception_index_table'] \
				if method.Exceptions is not None else []

	# 方法参数的个数、类型和顺序等 
	# 如果以一个L开头的描述符，就是类描述符，它后紧跟着类的字符串，然后分号“；”结束
	# int j,String s,List l,double[] d ==> ILjava/lang/String;Ljava/util/List;[D
	# ()V ==> no params and return void
	# (I)Ljava/lang/String; ==> params:int and return string
	def __parserDescriptor(self):
		args_returnType = self.descriptor[1:].split(')')
		returnType = []
		[self.__parserType(x,returnType) for x in args_returnType[1].split(';')]

		args_temp = args_returnType[0].split(';')
		args = []
		[self.__parserType(x,args) for x in args_temp]
		return returnType[0],args

	# 递归解析方法参数类型
	def __parserType(self,temp,result):
		if len(temp) == 0:
			return
		head = temp[:1]

		if head == 'L':
			result.append(temp[1:])
		elif head == '[': # TODO 暂时只处理一维数组
			result.append(head + temp[1:2])
			self.__parserType(temp[1:],result)
		else:
			result.append(head)
			self.__parserType(temp[1:],result)

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