# -*- coding:utf-8 -*-

# JVM 全局基类
class Base(object):
	# JVM 全局类型定义
	[BOOLEAN,FLOAT,DOUBLE,BYTE,CHAR,SHORT,INT,LONG,OBJECTREF,ARRAY] = [bool,float,float,int,chr,int,int,long,object,list]
	def __init__(self):
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

	def abc(self):
		print id(self.OBJECTREF)
		
if __name__ == '__main__':
	test()