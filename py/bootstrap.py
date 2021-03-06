# -*- coding:utf-8 -*-
import os
# print sys.path

from classFileParser import ClassParser
from bean.clinitBean import ClassInfo
from common.accessFlags import printAccessFlag
from common.base import Base
from lang.myexceptions import ClassFileNotFoundError
from zipfile import ZipFile


'''
对于JVM级别的类加载器在启动时就会把默认的 JAVA_HOME/lib里的class文件加载到JVM中，
因为这些是系统常用的类，对于其他的第三方类，则采用用到时就去找，找到了就缓存起来的，
下次再用到这个类的时候就可以直接用缓存起来的类对象了

类加载，等class文件加载完成后，就开始类加载过程。类加载完成后放入方法区。
内容包括运行时常量池，类型信息，字段信息，方法信息，类加载器引用，Class实例引用
我们这里的类加载器引用都为None，因为都是用bootstrap 加载器加载的，而不是用户自定义类加载器加载
'''
class Bootstrap(Base):
	# _class_name:类路径
	def __init__(self, _class_name):
		self.class_name = _class_name
		self.is_basic = False
		if not Base.METHOD_AREA.has_key(self.class_name):
			self.do()
			

	def do(self):
		# print Base.METHOD_AREA
		# 最终放入方法区的内容
		self.classInfo = ClassInfo()
		# 放入方法区
		Base.METHOD_AREA[self.class_name] = self.classInfo
		self.__load()
		# 基础数据类型不加载
		if self.is_basic:
			return
		self.__verity()
		self.__preparation()
		# 解析和初始化的过程放在指令执行阶段
		# self.__resolution()
		# self.__clinit()
		# 移除指针，以便GC
		self.classInfo.clearTempData()

		# print '类变量:',self.classInfo.class_field

	# 装载阶段 - 查找并装载类型的二进制数据. 此阶段在 ClassFile 类中完成了
	def __load(self):
		if self.class_name.startswith('['):
			# 首先去除"["符号，多维数组会有多个"["符号
			self.class_name = self.class_name[self.class_name.rindex('[')+1:]
			# TODO 基本数据类型的数组暂时不解析
			if self.class_name[0] in ['B','C','D','F','I','J','Z','S']:
				self.is_basic = True
				return
			else: # 首位字符为'L'，代表引用类型
				self.class_name = self.class_name[1:-1]
		# 解析好的class二进制文件内容
		_c_file = ClassFile().loadClass(self.class_name)
		# _c_file.printClass()
		# 初始化方法区的一些基本属性
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
		self.classInfo.initClassField()

	# 解析阶段 - 把常量池中的符号引用转化为直接引用，可以在指令anewarray、checkcast、getfield、getstatic、instanceof等的触发下执行
	# 麻蛋，啪啪打脸啊，一步到位你妹啊 -> 说一句：在这里我们一步到位，加载过程直接到初始化阶段，不用等这些指令来触发。
	# 说两句：对于指向“类型”【Class对象】、类变量、类方法的直接引用可能是指向方法区的本地指针
	def __resolution(self):
		# 1.类或接口的解析
		# 2.字段的解析
		# 3.类方法的解析
		# 4.接口方法的解析
		self.classInfo.handlerCpinfo()


	# 初始化阶段 - 把类变量初始化为正确的初始值，执行类构造器<clinit>方法，如果有父类，则需要先执行父类的<clinit>方法
	# 注意接口的情况，只有当子接口或者实现类用到了父接口的静态变量时，才需要执行父接口的<clinit>方法，如果父接口有的话。
	def __clinit(self):
		pass

	# 类的实例化 - 执行类的实例构造函数<init>，由new等指令来触发
	def init(self):
		pass

# ============================================================================================================================
# 类文件，并非Class实例
class ClassFile(Base):

	def __init__(self):
		# 父类class文件的指针（一个ClassFile实例指针）
		self.super_class_file = None

	# 类文件内容Code
	def __init(self,class_args):
		self.magic = class_args.get('magic',None)# u4 
		self.minor_version = class_args.get('minor_version',0)# u2 
		self.major_version = class_args.get('major_version',None)# u2 
		self.constant_pool_count = class_args.get('constant_pool_count',0)# u2 
		self.cp_info = class_args.get('cp_info',[])
		self.cp_tag = class_args.get('cp_tag',[])
		self.access_flags = class_args.get('access_flags',0)# u2 
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
		
	# 加载类，根据java class名称读取相应java class文件的内容
	def loadClass(self,_class):
		if Base.CLASS_FILES.has_key(_class):
			# print '================has loaded class==============:',_class
			return Base.CLASS_FILES[_class]
		print 'load class :',_class
		# 存放class文件二进制内容
		class_content = []
		# 如果class在JRE中
		if Base.JRE_CLASSES.__contains__(_class):
			self.__loadJreClass(_class,class_content)
		else:
			self.__loadAppClass(_class,class_content)
		# print class_content
		class_args = ClassParser(class_content)._cls_args
		# print 'class_args:',class_args
		self.__init(class_args)
		# 每个被装载的类文件
		Base.CLASS_FILES[self.this_class]=self
		# 处理父类:当父类不为空，并且还未被加载
		if self.super_class is not None and not Base.CLASS_FILES.has_key(self.super_class):
			# 做一次第归
			_super = ClassFile()
			_super.loadClass(self.super_class)
			self.super_class_file = _super
		return self

	# 加载JRE的class文件
	def __loadJreClass(self,_class,class_content):
		_temp_index = Base.JRE_CLASSES[_class]
		_zip_handle = Base.JRE_JARS[_temp_index]
		# print _zip_handle.printdir()
		# 读取文件内容
		# _class名称后面加上.class，是因为在JRE_CLASSES集合中和class二进制文件中保存的都是不加后缀的
		# 但是_zip_handle句柄中映射的文件却是要带后缀名的，故而如此。
		# 此处如果用【with _zip_handle.open(_class+'.class','r') as _file:】，在linux环境下会报错：
		# AttributeError: ZipExtFile instance has no attribute '__exit__'
		_file = _zip_handle.open(_class+'.class','r')
		self.__readFile(_file,class_content)
		_file.close()
		
	# 加载应用的class文件 - 根据绝对路径查找并装载类型的二进制数据
	def __loadAppClass(self,_class,class_content):
		_absolute_path = Base.APP_CLASS_PATH % _class
		# print '============_absolute_path:',_absolute_path
		# 如果文件不存在，则抛出异常
		if not os.path.exists(_absolute_path):
			raise ClassFileNotFoundError(_absolute_path)
		# 读取文件内容
		with open(_absolute_path,'rb') as _file:
			self.__readFile(_file,class_content)
		
	# 读取二进制文件
	def __readFile(self,_file,_file_content):
		while True:
			b = _file.read(1)
			# 到达文件结尾，直接跳出
			if len(b) == 0:
				break
			# 回车符直接打印，不需要转码【被自己坑，class里面就没有一个多余的字符】
			# elif b == '\n':
			# 	print 'line is end'
			# 	_file_content.append(b)
			#将编码转化为16进制数据添加进data数组
			else:
				_file_content.append('%.2x' % ord(b)) # "0x%.2X" % ord(b)
				# data.append('%.2d' % ord(b))

	# pirnt class with accessFlags
	def printClass(self):
		# print '===============following is class================'
		# print c.this_class
		# print c.__dict__
		# print '----is or not a interface:',c.isInterface()
		# print 'cp_info:',self.cp_info
		# print 'cp_tag:',self.cp_tag
		print '===============following is field_info================'
		for x in self.field_info:
			print printAccessFlag('field',x.access_flags),x.__dict__
			for y in x.attributes:
				print y.__dict__
		# print '===============following is method_info================'
		# for x in self.method_info:
		# 	print x.name
		#	print printAccessFlag('method',x.access_flags),x.__dict__
		# 	print x.__dict__
		# 	if x.Code:
		# 		print x.Code.__dict__
		# 	if x.Exceptions:
		# 		print x.Exceptions.__dict__
		# print '===============following is _super method_info================'
		# _super = self.super_class_file
		# for x in _super.method_info:
		# 	print x.name
		# 	if x.Code is not None:
		# 		print x.Code.__dict__
		print '===============following is Base.CLASS_FILES================'
		print len(Base.CLASS_FILES)
		for k,v in Base.CLASS_FILES.items():
			print k#,v.__dict__


if __name__ == '__main__':
	# 加载APP启动类
	path = 'cls/test'
	# path = 'java/io/IOException'
	# Bootstrap(path)
	c = ClassFile()
	c.loadClass(path)
	c.printClass()
	# print c.__dict__