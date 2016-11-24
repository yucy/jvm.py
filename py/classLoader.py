# -*- coding:utf-8 -*-
from sys import argv

# 根据java class名称读取相应java class文件的内容
def readClassFile(path):
	with open(path,'rb') as _file:
		printClassFile(_file)
	return False or True

# 打印读入的class文件内容
def printClassFile(_file):
	#for line in _file:
	#	print line
	#_file.seek(0,0) #定位到文件开头，offset->0
	data = []
	while True:
		t_byte = _file.read(1)
		if t_byte == '\n':
			#print 'this is line end.'
			data.append(t_byte)
		if len(t_byte) == 0:
			break
		else:
			data.append('%.2x' % ord(t_byte)) # "0x%.2X" % ord(t_byte)
			# data.append(ord(t_byte))
	for x in range(0,len(data)):
		print data[x],
	return data	



# 默认执行该class文件的main方法
def execute():
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
def executeMethod():
	return False or True

# 返回方法信息
'''
const char* szMethodName
const char* szDescriptor
bool bFindFromBaseClass=true
'''
def findMethodInfo():
	return "method_info"

# 是否是给定class名的子类
# const char* szBaseClassName
def isDerivedClassOf(szBaseClassName):
	return False or True

# 是否三给定class名的子类
# CClassFile* pBaseClassFile
def isDerivedClassOf(pBaseClassFile):
	return False or True

# 是否是给定class名的父类
# const char* szDerivedClassName
def isBaseClassOf(szDerivedClassName):
	return False or True

# 是否三给定class名的父类
# CClassFile* pDerivedClassFile
def isBaseClassOf(pDerivedClassFile):
	return False or True

# 是否是接口
def isInterface():
	return False or True

# 是否是抽象类
def isAbstractClass():
	return False or True

# 程序入口
if __name__=="__main__":
	# argv,第一个参数是python后面算起的，我们的启动命令是：python py/classLoader.py cls/demo.class
	# 很显然，我们要读取的是class文件，是第二个参数，故而我们用argv[1]
	path = argv[1]
	print "The class path is [%s]." % path
	if path:
		readClassFile(path)
