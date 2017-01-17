# -*- coding:utf-8 -*-

# 0,4,5,9,10,12,13,14
access_flags_class_print = {
	0x0001:'ACC_PUBLIC', #可以被包的类外访问。
	0x0010:'ACC_FINAL', #不允许有子类。
	0x0020:'ACC_SUPER', #当用到invokespecial指令时,需要特殊处理的父类方法。
	0x0200:'ACC_INTERFACE', #标识定义的是接口而不是类。
	0x0400:'ACC_ABSTRACT', #不能被实例化。
	0x1000:'ACC_SYNTHETIC', #标识并非标识并非Java源码生成的代码。
	0x2000:'ACC_ANNOTATION', #标识注解类型
	0x4000:'ACC_ENUM', #标识枚举类型
}

access_flags_class = {
	'PUBLIC':	0x0001, #可以被包的类外访问。
	'FINAL':	0x0010, #不允许有子类。
	'SUPER':	0x0020, #当用到invokespecial指令时,需要特殊处理的父类方法。
	'INTERFACE':0x0200, #标识定义的是接口而不是类。
	'ABSTRACT':	0x0400, #不能被实例化。
	'SYNTHETIC':0x1000, #标识并非标识并非Java源码生成的代码。
	'ANNOTATION':0x2000, #标识注解类型
	'ENUM':		0x4000, #标识枚举类型
}

'''
'1', 					0
'10,000', 				4
'100,000', 				5
'1,000,000,000', 		9
'10,000,000,000', 		10
'1,000,000,000,000', 	12
'10,000,000,000,000', 	13
'100,000,000,000,000'	14
'''
# 0,1,2,3,4,6,7,12,14
access_flags_field_print = {
	0x0001:'ACC_PUBLIC', #public,表示字段可以从任何包访问。
	0x0002:'ACC_PRIVATE', #private,表示字段仅能该类自身调用。
	0x0004:'ACC_PROTECTED', #protected,表示字段可以被子类调用。
	0x0008:'ACC_STATIC', #static,表示静态字段。
	0x0010:'ACC_FINAL', #final,表示字段定义后值无法修改(JLS_§17.5)。
	0x0040:'ACC_VOLATILE', #volatile,表示字段是易变的。
	0x0080:'ACC_TRANSIENT', #transient,表示字段不会被序列化。
	0x1000:'ACC_SYNTHETIC', #表示字段由编译器自动产生。
	0x4000:'ACC_ENUM', #enum,表示字段为枚举类型。
}

access_flags_field = {
	'PUBLIC':	0x0001, #public,表示字段可以从任何包访问。
	'PRIVATE':	0x0002, #private,表示字段仅能该类自身调用。
	'PROTECTED':0x0004, #protected,表示字段可以被子类调用。
	'STATIC':	0x0008, #static,表示静态字段。
	'FINAL':	0x0010, #final,表示字段定义后值无法修改(JLS_§17.5)。
	'VOLATILE':	0x0040, #volatile,表示字段是易变的。
	'TRANSIENT':0x0080, #transient,表示字段不会被序列化。
	'SYNTHETIC':0x1000, #表示字段由编译器自动产生。
	'ENUM':		0x4000, #enum,表示字段为枚举类型。
}
'''
'1', 					0
'10', 					1
'100', 					2
'1,000', 				3
'10,000', 				4
'1,000,000', 			6
'10,000,000', 			7
'1,000,000,000,000', 	12
'100,000,000,000,000'	14
'''

# 0,1,2,3,4,5,6,7,8,10,11,12
access_flags_method_print = {
	0x0001:'ACC_PUBLIC', #public,方法可以从包外访问
	0x0002:'ACC_PRIVATE', #private,方法只能本类中访问
	0x0004:'ACC_PROTECTED', #protected,方法在自身和子类可以访问
	0x0008:'ACC_STATIC', #static,静态方法
	0x0010:'ACC_FINAL', #final,方法不能被重写(覆盖)
	0x0020:'ACC_SYNCHRONIZED', #synchronized,方法由管程同步
	0x0040:'ACC_BRIDGE', #bridge,方法由编译器产生
	0x0080:'ACC_VARARGS', #表示方法带有变长参数
	0x0100:'ACC_NATIVE', #native,方法引用非java语言的本地方法
	0x0400:'ACC_ABSTRACT', #abstract,方法没有具体实现
	0x0800:'ACC_STRICT', #strictfp,方法使用FP-strict浮点格式
	0x1000:'ACC_SYNTHETIC', #方法在源文件中不出现,由编译器产生
}

access_flags_method = {
	'PUBLIC':		0x0001, #public,方法可以从包外访问
	'PRIVATE':		0x0002, #private,方法只能本类中访问
	'PROTECTED':	0x0004, #protected,方法在自身和子类可以访问
	'STATIC':		0x0008, #static,静态方法
	'FINAL':		0x0010, #final,方法不能被重写(覆盖)
	'SYNCHRONIZED':	0x0020, #synchronized,方法由管程同步
	'BRIDGE':		0x0040, #bridge,方法由编译器产生
	'VARARGS':		0x0080, #表示方法带有变长参数
	'NATIVE':		0x0100, #native,方法引用非java语言的本地方法
	'ABSTRACT':		0x0400, #abstract,方法没有具体实现
	'STRICT':		0x0800, #strictfp,方法使用FP-strict浮点格式
	'SYNTHETIC':	0x1000, #方法在源文件中不出现,由编译器产生
}

'''
'1', 				0
'10', 				1
'100', 				2
'1,000', 			3
'10,000', 			4
'100,000', 			5
'1,000,000', 		6
'10,000,000', 		7
'100,000,000', 		8
'10,000,000,000', 	10
'100,000,000,000', 	11
'1,000,000,000,000'	12
'''


access_flags = {
	'class':access_flags_class_print,
	'field':access_flags_field_print,
	'method':access_flags_method_print,
}

# 访问标识 _type : class,field,method
def printAccessFlag(_type,num):
	if _type not in ('method','field','class'):
		print 'the type can be [class,field,method] only,not %s' % _type
		return None
	_dict = access_flags.get(_type)
	# 将十进制的数据转换成2进制，去掉头标识【0b】后反置
	s = reverse(bin(num).replace('0b',''))
	# 检索出非零字符的位置下标
	_index = [i for i in xrange(len(s)) if s[i] != '0']
	# 根据位置下标来取2的N次方，并根据此值来返回访问标识字符串
	return [_dict.get(pow(2,i),None) for i in _index]


# 是否指定访问标识字段 ,_access:PUBLIC,PRIVATE...
def checkFieldAccess(_access,num):
	accessValue = access_flags_field.get(_access,None)
	if accessValue is None:
		print 'checkFieldAccess, access:%s not found' % _access
		return False
	return checkAccess(accessValue,num)


# 是否指定访问标识方法 
def checkMethodAccess(_access,num):
	accessValue = access_flags_method.get(_access,None)
	if accessValue is None:
		print 'checkMethodAccess, access:%s not found' % _access
		return False
	return checkAccess(accessValue,num)

# 是否指定访问标识类
def checkClassAccess(_access,num):
	accessValue = access_flags_class.get(_access,None)
	if accessValue is None:
		print 'checkClassAccess, access:%s not found' % _access
		return False
	return checkAccess(accessValue,num)

def checkAccess(accessValue,num):
	# 将十进制的数据转换成2进制，去掉头标识【0b】后反置
	s = reverse(bin(num).replace('0b',''))
	# 检索出非零字符的位置下标,并根据位置下标来取2的N次方
	_index = [pow(2,i) for i in xrange(len(s)) if s[i] != '0']
	if _index.__contains__(accessValue):
		return True
	return False




# 反置字符串
def reverse(string):
	return string[::-1]

if __name__ == '__main__':
	# temp = [bin(i) for i in access_flags_method.keys()]
	# temp.sort()
	# print temp
	# print bin(34)
	print printAccessFlag('method',15)
	flag = checkMethodAccess('STATIC',15)
	print flag

