# -*- coding:utf-8 -*-
import sys,time,gc
sys.path.append('..')

from common.base import Base
from classFileParser import ClassParser
from zipfile import ZipFile


# _zip = ZipFile('C:/Program Files/Java/jdk1.7.0_51/jre/lib/rt.jar')

# 加载jre class
class JreClass(Base):
	
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
		return self.__loadJreClass(_class)

	def gc_(self,_zip):
		del _zip
		gc.collect()

	# 加载
	def __loadJreClass(self,_class):
		# ZipFile(_jar_path)
		print 111111
		time.sleep(10)
		# self.parser(_zip,_class)
		with ZipFile('C:/Program Files/Java/jdk1.7.0_51/jre/lib/rt.jar') as _zip:
			self.parser(_zip,_class)
			self.gc_(_zip)
		# print 2222222
		# time.sleep(10)
		# # _zip1 = ZipFile('C:/Program Files/Java/jdk1.7.0_51/jre/lib/rt.jar')
		
		print 2525252525
		time.sleep(10)
		# _zip.close()
		# print 3333333
		# time.sleep(10)
		# # _zip.__exit__()
		# # print 444444
		# # time.sleep(10)
		# del(_zip)
		# print 555555
		# time.sleep(10)
		# # 到这一步会回收内存
		# gc.collect()
		# print 66666
		# time.sleep(10)

	def parser(self,_zip,_class):
		data = []
		with _zip.open(_class) as _file:# 不能释放内存
			print dir(_file)
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
			# _file.close()
		# print data
		class_args = ClassParser(data)._cls_args
		# print 'class_args:',class_args
		self.__init(class_args)
		# 每个被装载的类文件
		Base.classFiles[self.this_class]=self
		
			
	# pirnt class with accessFlags
	def printClass(self):
		print 3333333
		time.sleep(10)
		# print '===============following is class================'
		# print c.this_class
		# print c.__dict__
		# print '----is or not a interface:',c.isInterface()
		print 'cp_info:',self.cp_info
		# print 'cp_tag:',self.cp_tag
		print '===============following is field_info================'
		for x in self.field_info:
			# x.access_flags = printAccessFlag('field',x.access_flags)
			print x.__dict__
			for y in x.attributes:
				print y.__dict__
		# print '===============following is method_info================'
		# for x in self.method_info:
		# 	print x.name
		# 	# x.access_flags = printAccessFlag('method',x.access_flags)
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
		print '===============following is Base.classFiles================'
		print len(Base.classFiles)
		for k,v in Base.classFiles.items():
			print k#,v.__dict__
		

if __name__ == '__main__':
	c = JreClass()
	_class = 'java/lang/Object.class'
	c.loadClass(_class)
	c.printClass()

	# d = JreClass()
	# _class = 'java/lang/String.class'
	# d.loadClass(_class)
	# d.printClass()