# -*- coding:utf-8 -*-
import os
from parser.classParser import ClassParser
from struct.clinit_s import ClassInfo

# 被装载的类文件
classFiles = {}
# 临时方法区，存放cinit_s.ClassInfo信息
methodArea = {}
# 临时堆，存放类实例
heap = {}

# JRE 类路径
JAVA_HOME = '/home/yucy/git/jvm.py/rt/%s.class'
# 应用类路径
APP_HOME = None
# 应用启动类
MAIN_CLASS = None

# 类加载，等class文件加载完成后，就开始类加载过程。类加载完成后放入方法区。
# 内容包括运行时常量池，类型信息，字段信息，方法信息，类加载器引用，Class实例引用
# 我们这里的类加载器引用都为None，因为都是用bootstrap 加载器加载的，而不是用户自定义类加载器加载
class Bootstrap(object):
	# _class_path:类路径
	def __init__(self, _class_path):
		self.class_path = _class_path
		# 最终放入方法区的内容
		self.classInfo = ClassInfo()
		self.__load()
		self.__verity()
		self.__preparation()
		self.__resolution()
		self.__clinit()
		# 放入方法区
		methodArea[self.classInfo.this_class] = self.classInfo

	# 装载阶段 - 查找并装载类型的二进制数据. 此阶段在 ClassFile 类中完成了
	def __load(self):
		# 解析好的class二进制文件内容
		_c_file = ClassFile(self.class_path)
		self.classInfo.initBaseInfo(_c_file)


		# 验证阶段 - 确保被导入类型的正确性
	def __verity(self):
		# 1.文件格式验证：是否以魔数开头、版本号是否在正确范围、常量池中是否有不支持的常量类型等
		# 2.元数据验证：子类是否继承了final方法、是否实现了父类或接口必要的方法、子类与父类是否有字段或方法冲突等
		# 3.字节码验证：字段类型是否匹配、方法体中的代码是否会跳转越界、方法体中的类型转换是否有效等
		# 4.符号引用验证：全限定名是否能对应到具体类、类，字段和方法访问权限等
		pass

	# 准备阶段 - 为类或接口的静态字段分配空间,并用默认值初始化这些字段
	# 数值类型 -> 0，boolean类型 -> False，char -> '\u0000'，reference类型 -> None
	def __preparation(self):
		# 1.非final的静态字段 : 正常赋予静态变量初始值
		# 2.final+static字段 : 直接从其ContentValue属性中取出值来做初始化
		pass

	# 解析阶段 - 把常量池中的符号引用转化为直接引用，可以在指令anewarray、checkcast、getfield、getstatic、instanceof等的触发下执行
	# 说一句：在这里我们一步到位，加载过程直接到初始化阶段，不用指令这些指令来触发。
	def __resolution(self):
		# 1.类或接口的解析
		# 2.字段的解析
		# 3.类方法的解析
		# 4.接口方法的解析
		pass

	# 初始化阶段 - 把类变量初始化为正确的初始值，执行类构造器<clinit>方法，如果有父类，则需要先执行父类的<clinit>方法
	# 注意接口的情况，只有当子接口或者实现类用到了父接口的静态变量时，才需要执行父接口的<clinit>方法，如果父接口有的话。
	def __clinit(self):
		pass

	# 类的实例化 - 执行类的实例构造函数<init>，由new等指令来触发
	def init(self):
		pass

		
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
		global APP_HOME,MAIN_CLASS
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
		if MAIN_CLASS is None:
			MAIN_CLASS = self.this_class
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
			

if __name__ == '__main__':
	# 加载APP启动类
	path = '../cls/test.class'
	c = ClassFile(path)
	print 'MAIN_CLASS:',MAIN_CLASS
	print len(classFiles)
	for k,v in classFiles.items():
		print k,v,v.__dict__