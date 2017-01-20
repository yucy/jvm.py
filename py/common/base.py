# -*- coding:utf-8 -*-

# JVM 全局基类
class Base(object):
	# JVM 全局类型定义
	[BOOLEAN,FLOAT,DOUBLE,BYTE,CHAR,SHORT,INT,LONG,OBJECTREF,ARRAY] = [bool,float,float,int,chr,int,int,long,object,list]
	# 方法区类型映射
	method_argtype={
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
		print self.atypes[4]

	def abc(self):
		print id(self.OBJECTREF)
		
if __name__ == '__main__':
	# test()
	# ll = [234,6456,533]
	# for i,e in enumerate(ll):
	# 	print i,e
	s = '[Ljava/lang/Object;'
	print s[2:-1]