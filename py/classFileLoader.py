# -*- coding:utf-8 -*-
import os
from sys import argv
from common.accessFlags import getAccessFlag
from parser.classParser import ClassParser

# 被装载的类文件
classFiles = {}

JAVA_HOME = '/home/yucy/git/jvm.py/rt/%s.class'
APP_HOME = None

# 类文件，并非Class实例
class ClassFile(object):

	def __init__(self, path):
		print 'load class file :',path
		self.path = path
		# 父类class文件的指针（一个ClassFile实例指针）
		self.super_class_file = None
		self.loadFile()

	# 类文件内容
	def __init(self,class_args):
		self.magic = class_args.get('magic',None)# u4 
		self.minor_version = class_args.get('minor_version',0)# u2 
		self.major_version = class_args.get('major_version',None)# u2 
		self.constant_pool_count = class_args.get('constant_pool_count',0)# u2 
		self.cp_info = class_args.get('cp_info',[])
		self.access_flags = class_args.get('access_flags',None)# u2 
		self.this_class = class_args.get('this_class',None)# u2 
		self.super_class = class_args.get('super_class',None)# u2 
		self.interfaces_count = class_args.get('interfaces_count',0)# u2 
		self.interfaces = class_args.get('interfaces',[]) # u2 
		self.fields_count = class_args.get('fields_count',0)# u2 
		self.field_info = class_args.get('field_info',[])
		self.methods_count = class_args.get('methods_count',0)# u2 
		self.method_info = class_args.get('method_info',[])
		self.attributes_count = class_args.get('attributes_count',0)# u2 
		self.attribute_info = class_args.get('attribute_info',[])
		
	# 装载阶段 - 查找并装载类型的二进制数据
	# 根据java class名称读取相应java class文件的内容
	def loadFile(self):
		global APP_HOME
		data = []
		with open(self.path,'rb') as _file:
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
		# print data
		class_args = ClassParser(data)._cls_args
		# print 'class_args:',class_args
		self.__init(class_args)
		# 包路径外的绝对路径,只执行一次，因为要根据 this_class 的包路径来切割绝对路径，所以放在这里进行初始化
		if APP_HOME is None:
			# print '===abspath:',os.path.abspath(path)
			# print self.this_class
			abspath = os.path.abspath(self.path)
			APP_HOME = abspath[:abspath.find(self.this_class)]+'%s.class'
		# 每个被装载的类文件
		classFiles[self.this_class]=self
		# 处理父类:当父类不为空，并且还未被加载
		if self.super_class is not None and not classFiles.has_key(self.super_class):
			# 先到 JAVA_HOME 里面查找，找不到再根据父类路径查找
			_super_path = JAVA_HOME % self.super_class
			if not os.path.exists(_super_path):
				_super_path = APP_HOME % self.super_class
			print '_super_path:',_super_path
			# 做一次第归
			self.super_class_file = ClassFile(_super_path)
			
	# 默认执行该class文件的main方法
	def execute(self):
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
	def executeMethod(self):
		return False or True

	# 返回方法信息
	'''
	const char* szMethodName
	const char* szDescriptor
	bool bFindFromBaseClass=true
	'''
	def findMethodInfo(self):
		return "method_info"

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

	# 是否是接口
	def isInterface(self):
		return self.access_flags.__contains__('ACC_INTERFACE')

	# 是否是抽象类
	def isAbstractClass(self):
		return self.access_flags.__contains__('ACC_ABSTRACT')

	# pirnt class with accessFlags
	def printClass(self):
		# print '===============following is class================'
		# print c.this_class
		# print c.__dict__
		# print '----is or not a interface:',c.isInterface()
		print self.cp_info
		print '===============following is field_info================'
		for x in self.field_info:
			x.access_flags = getAccessFlag('field',x.access_flags)
			print x.__dict__
			for y in x.attributes:
				print y.__dict__
		print '===============following is method_info================'
		for x in self.method_info:
			print x.name
			x.access_flags = getAccessFlag('method',x.access_flags)
			print x.__dict__
			if x.Code:
				print x.Code.__dict__
			if x.Exceptions:
				print x.Exceptions.__dict__
		# print '===============following is _super method_info================'
		# _super = self.super_class_file
		# for x in _super.method_info:
		# 	print x.name
		# 	if x.code:
		# 		print x.code.__dict__
		print '===============following is classFiles================'
		print len(classFiles)
		for k,v in classFiles.items():
			print k,v,v.__dict__

# 程序入口
if __name__=="__main__":
	# argv,第一个参数是python后面算起的，我们的启动命令是：python py/classLoader.py cls/demo.class
	# 很显然，我们要读取的是class文件，是第二个参数，故而我们用argv[1]
	# path = argv[1]
	# path = '/home/yucy/git/jvm.py/cls/demo.class'
	# path = 'e:/git/github/jvm.py/cls/demo.class'
	path = '../cls/test.class'
	# path = '../rt/java/lang/Object.class'
	# path = '../rt/java/lang/Class.class'
	# path = '../cls/test_extends.class'
	# print "The class path is [%s]." % path
	# 如果path不为空
	if path:
		c = ClassFile(path)
		c.printClass()
		
		
