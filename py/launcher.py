# -*- coding:utf-8 -*-
import os,time
from sys import argv
from common.base import Base
from bootstrap import Bootstrap
from zipfile import ZipFile
		
# 启动JVM类
class Laucher(Base):
	def __init__(self,_class_path,_main_class):
		# 初始化Base
		super(Laucher, self).__init__()
		# 启动class路径
		self.class_path = _class_path
		# 启动class
		Base.MAIN_CLASS = _main_class.replace('.','/')
		# class path
		self.initClassPath()
		# JRE
		self.__scanJRE()
		
	def start(self):
		# 加载初始类
		Bootstrap(Base.MAIN_CLASS)

	# 加载启动类，初始加载需要指定路径来初始化APP_PATH，而loadClassFile()方法只需指定class就行
	def initClassPath(self):
		# 包路径外的绝对路径,只执行一次，因为要根据 this_class 的包路径来切割绝对路径，所以放在这里进行初始化
		# if APP_HOME is None:
		# print '===abspath:',os.path.abspath(path)
		# print self.this_class
		# self.__load(path)
		# print '===isLinux:',Base.ISLINUX
		abspath = os.path.abspath(self.class_path)
		# print '===abspath:',abspath
		# 判断是否linux系统
		if not Base.ISLINUX:
			# linux和windows的文件路径分隔符不一样，这里统一为linux的分隔符【/】
			abspath = abspath.replace('\\','/')
		Base.APP_CLASS_PATH = abspath+'/%s.class'
		print Base.MAIN_CLASS,Base.APP_CLASS_PATH

	# 缓存jre里的类名集合
	def __scanJRE(self):
		# JRE jar文件
		self.__getJvmClass(Base.JRE_HOME)
		# ext jar文件，不需要加载
		# self.__getJvmClass(Base.JRE_HOME+'ext/')

		# print Base.JRE_JARS
		# print Base.JRE_CLASSES.get('java/lang/annotation/Annotation',-1)

	# 将class文件和jar路径关联起来
	def __getJvmClass(self,_jar_path):
		if not Base.ISLINUX:
			# linux和windows的文件路径分隔符不一样，这里统一为linux的分隔符【/】
			_jar_path = _jar_path.replace('\\','/')
		# print '====================',_jar_path
		# 遍历目录下的文件/文件夹
		for jar in os.listdir(_jar_path):
			if jar in Base.BOOTSTRAP_JARS:
				_index = len(Base.JRE_JARS)
				_absolute_jar_path = _jar_path+jar
				# print '++++++++++++++++++++++++',_absolute_jar_path
				_zip_handle = ZipFile(_absolute_jar_path)
				# 保存jar文件句柄
				Base.JRE_JARS.append(_zip_handle)
				# 保存class文件和jar路径在_jars集合中的下标
				Base.JRE_CLASSES.update([(_c[:_c.index('.class')],_index) for _c in _zip_handle.namelist() if _c.endswith('class')])
				# _zip.close() # close 或者 del 并不能立即释放内存，可以用gc.collect()

	# 执行该 APP启动类的main方法
	def executeMethod(self):
		print 234
		return False or True

	

# JVM 启动入口
if __name__ == '__main__':
	# argv,第一个参数是python后面算起的，我们的启动命令是：python py/classLoader.py cls/demo.class
	# 很显然，我们要读取的是class文件，是第二个参数，故而我们用argv[1]
	# path = argv[1]
	# 加载APP启动类 , 参考java -cp 命令，cp后面跟的就是CLASS_PATH
	class_path = '../'
	main_class = 'cls.test'
	lau = Laucher(class_path,main_class)
	# lau.jre()
	# lau.getExtJar()
	lau.start()