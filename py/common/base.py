# -*- coding:utf-8 -*-
import platform,os,sys

# JVM 全局基类
class Base(object):
	# 设置递归调用深度为一百万
	# sys.setrecursionlimit(1000000) 

	# JVM 全局类型定义
	[BOOLEAN,FLOAT,DOUBLE,BYTE,CHAR,SHORT,INT,LONG,OBJECTREF,ARRAY] = [bool,float,float,int,chr,int,int,long,object,list]
	# 方法区类型映射
	METHOD_ARGTYPE={
		'B': BYTE, # 有符号字节型数
		'C': CHAR, # Unicode 字符,UTF-16 编码
		'D': DOUBLE, # 双精度浮点数
		'F': FLOAT, # 单精度浮点数
		'I': INT, # 整型数
		'J': LONG, # 长整数
		'S': SHORT, # 有符号短整数
		'Z': BOOLEAN, # 布尔值 true/false
		'L': OBJECTREF, #;  一个名为<Classname>的实例,e.g.: Ljava/lang/String;Ljava/util/List;
		'[': ARRAY, # 一个一维数组,e.g.:[D -> double[] 
	}
	# 判断是否linux系统
	ISLINUX = 'Linux' in platform.system()
	# 被装载的类文件
	CLASS_FILES = {}
	# 临时方法区，存放cinit_s.ClassInfo信息
	METHOD_AREA = {}
	# 临时堆，存放类实例
	HEAP_AREA = {}
	# JRE 类路径，读取环境变量【JAVA_HOME】
	JRE_HOME = os.getenv('JAVA_HOME')+'/jre/lib/'
	# 应用类路径
	APP_CLASS_PATH = None
	# 应用启动类
	MAIN_CLASS = None
	# jre的jar文件句柄集合
	JRE_JARS = []
	# jre中包含的class和包含class的jar文件在_jars集合中的下标，eg:{'sun/security/mscapi/PRNG': 6}
	JRE_CLASSES = {}

	def __init__(self):
		print '***************Base.init()***************'
		pass
		
	# 类方法，参数位类本身，只有类可以调用
	@classmethod
	def initJvm(c):
		# JAVA_HOME = 'E:/jar/rt/%s.class'
		# APP_CLASS_PATH = None
		pass

	# 静态方法，无参数，类和实例均可调用
	@staticmethod
	def initJVM():
		# JAVA_HOME = 'E:/jar/rt/%s.class'
		# APP_CLASS_PATH = None
		pass

class test(Base):
	atypes = {
		4:Base.BOOLEAN,
		5:Base.CHAR,
		6:Base.FLOAT,
		7:Base.DOUBLE,
		8:Base.BYTE,
		9:Base.SHORT,
	}
	def __init__(self):
		print id(Base.BOOLEAN)
		print id(self.BOOLEAN)
		self.abc()
		print self.atypes[4]

	def abc(self):
		print id(self.OBJECTREF)
		
		
if __name__ == '__main__':
	# test()
	# ll = [234,6456,533]
	# for i,e in enumerate(ll):
	# 	print i,e
	# s = '[[[Ljava/lang/annotation/Annotation;'
	# b = Base()
	print 123