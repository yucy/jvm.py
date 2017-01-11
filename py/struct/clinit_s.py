# -*- coding:utf-8 -*-
'''
说明：此模块中的结构用于java类加载、链接和初始化过程
'''

# class_info 构造 , 用于保存方法区信息
# 内容包括运行时常量池，类型信息，字段信息，方法信息，类加载器引用，Class实例引用,类变量和方法表
class ClassInfo(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		# 运行时常量池
		self.cp_info = arg.get('cp_info',[])
		# 类型信息
		# 1 ．类型的完全限定名
		# 2 ．类型直接超类的完全限定名 
		# 3 ．直接超接口的全限定名列表 
		# 4 ．该类型是类类型还是接口类型 
		# 5 ．类型的访问修饰符（如 public,abstract,final 等，对应 access_flags. )
		self.this_class = arg.get('this_class',None)# u2 
		self.super_class = arg.get('super_class',None)# u2 
		self.access_flags = arg.get('access_flags',None)# u2 
		self.interfaces = arg.get('interfaces',[]) # u2 
		
		# 字段信息
		self.field_info = [FieldInfo(i) for i in arg.get('field_info',[])]
		
		# 方法信息
		self.method_info = [MethodInfo(i) for i in arg.get('method_info',[])]
		# 类变量分为两种变量： 
		# 1 ．运行时变量，在准备阶段就赋予默认值.
		# 2 ．编译时变量，static+属性表中存在ContentValue属性，直接赋予ContentValue的值。（如果其他类引用了此变量，
		# 直接把变量的值写进其class文件流中，这在编译时处理）
		# TODO

		# 类加载器的引用
		# 一个类可以被启动类加载器或者自定义的类加载器加载，如果一个类被某个自定义类加载器的对象（实例）加载，
		# 则方法区中必须保存对该对象的引用。注意：如果是被JVM内部加载器加载，则此项为None
		self.classLoader = None

		# 指向 Class 实例的引用
		# 在加载过程中，虚拟机会创建一个代表该类型的 Class 对象，方法区中必须保存对该对象的引用
		# TODO execute Class.init()

		# 方法表
		# 为了提高访问效率，必须仔细的设计存储在方法区中的数据信息结构。除了以上讨论的结构，JVM 的实现者还可以添加一些其他
		# 的数据结构，如方法表。 jvm 对每个加载的非虚拟类的类型信息中都添加了一个方法表，方法表是一组对类实例方法的直接引用
		# （包括从父类继承的方法）。 jvm 可以通过方法表快速激活实例方法．
		# TODO

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
		self.name = arg.get('name')
		self.type = arg.get('descriptor')
		self.access_flags = arg.get('access_flags')
		

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
		self.name = arg.get('name')
		self.returnType = arg.get('descriptor')
		# TODO 方法参数的个数、类型和顺序等 
		self.access_flags = arg.get('access_flags')
		# method's Code Attribute
		Code = arg.get('Code')
		self.codes = Code.get('codes')
		#  'max_locals': 3, 'max_stack': 2, 'exception_table_length'
		self.max_locals = Code.get('max_locals')
		self.max_stack = Code.get('max_stack')
		# 'attribute_name': 'Exceptions' {'number_of_exceptions': 1, 'exception_index_table': [['java/lang/Exception']]}
		Exceptions = arg.get('Exceptions')
		self.exceptions = Exceptions.get('exception_index_table')



# =======================================================================================================