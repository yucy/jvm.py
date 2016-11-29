# -*- coding:utf-8 -*-

access_flags_class = {
	# 0x0001
	0:'ACC_PUBLIC', #可以被包的类外访问。
	# 0x0010
	4:'ACC_FINAL', #不允许有子类。
	# 0x0020
	5:'ACC_SUPER', #当用到invokespecial指令时,需要特殊处理的父类方法。
	# 0x0200
	9:'ACC_INTERFACE', #标识定义的是接口而不是类。
	# 0x0400
	10:'ACC_ABSTRACT', #不能被实例化。
	# 0x1000
	12:'ACC_SYNTHETIC', #标识并非标识并非Java源码生成的代码。
	# 0x2000
	13:'ACC_ANNOTATION', #标识注解类型
	# 0x4000
	14:'ACC_ENUM', #标识枚举类型

}
'''
[
'0b1', 					0
'0b10,000', 			4
'0b100,000', 			5
'0b1,000,000,000', 		9
'0b10,000,000,000', 	10
'0b1,000,000,000,000', 	12
'0b10,000,000,000,000', 13
'0b100,000,000,000,000'	14

]
'''

access_flags_field = {
	# 0x0001
	0 :'ACC_PUBLIC', #public,表示字段可以从任何包访问。
	# 0x0002
	1 :'ACC_PRIVATE', #private,表示字段仅能该类自身调用。
	# 0x0004
	2 :'ACC_PROTECTED', #protected,表示字段可以被子类调用。
	# 0x0008
	3 :'ACC_STATIC', #static,表示静态字段。
	# 0x0010
	4 :'ACC_FINAL', #final,表示字段定义后值无法修改(JLS_§17.5)。
	# 0x0040
	6 :'ACC_VOLATILE', #volatile,表示字段是易变的。
	# 0x0080
	7 :'ACC_TRANSIENT', #transient,表示字段不会被序列化。
	# 0x1000
	12:'ACC_SYNTHETIC', #表示字段由编译器自动产生。
	# 0x4000
	14:'ACC_ENUM', #enum,表示字段为枚举类型。

}
'''
[
'0b1', 					0
'0b10', 				1
'0b100', 				2
'0b1000', 				3
'0b10000', 				4
'0b1000000', 			6
'0b10,000,000', 		7
'0b1,000,000,000,000', 	12
'0b100,000,000,000,000'	14
]
'''

access_flags_method = {
	# 0x0001
	0:'ACC_PUBLIC', #public,方法可以从包外访问
	# 0x0002
	1:'ACC_PRIVATE', #private,方法只能本类中访问
	# 0x0004
	2:'ACC_PROTECTED', #protected,方法在自身和子类可以访问
	# 0x0008
	3:'ACC_STATIC', #static,静态方法
	# 0x0010
	4:'ACC_FINAL', #final,方法不能被重写(覆盖)
	# 0x0020
	5:'ACC_SYNCHRONIZED', #synchronized,方法由管程同步
	# 0x0040
	6:'ACC_BRIDGE', #bridge,方法由编译器产生
	# 0x0080
	7:'ACC_VARARGS', #表示方法带有变长参数
	# 0x0100
	8:'ACC_NATIVE', #native,方法引用非java语言的本地方法
	# 0x0400
	10:'ACC_ABSTRACT', #abstract,方法没有具体实现
	# 0x0800
	11:'ACC_STRICT', #strictfp,方法使用FP-strict浮点格式
	# 0x1000
	12:'ACC_SYNTHETIC', #方法在源文件中不出现,由编译器产生
}

'''
[
'0b1', 					0
'0b10', 				1
'0b100', 				2	
'0b1,000', 				3	
'0b10,000', 			4		
'0b100,000', 			5		
'0b1,000,000', 			6		
'0b10,000,000', 		7			
'0b100,000,000', 		8			
'0b10,000,000,000', 	10				
'0b100,000,000,000', 	11				
'0b1,000,000,000,000'	12				
]
'''

access_flags = {
	'class':access_flags_class,
	'field':access_flags_field,
	'method':access_flags_method,
}

def getAccessFlag(_type,num):
	if _type not in ('method','field','class'):
		print 'the type can be [class,field,method] only,not %s' % _type
		return None
	_dict = access_flags.get(_type)
	s = reverse(bin(num).replace('0b',''))
	print s
	temp = [i for i in xrange(len(s)) if s[i] != '0']
	print temp
	return [_dict.get(i,None) for i in temp]

	return _dict.get(num)

def reverse(string):
	return string[::-1]


if __name__ == '__main__':
	temp = [bin(i) for i in access_flags_method.keys()]
	temp.sort()
	# print temp
	print bin(34)
	print getAccessFlag('class',34)
