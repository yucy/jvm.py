# -*- coding:utf-8 -*-
import sys
sys.path.append('..')

import accessFlags
from common.utils import getDecimal
from common.content import constant_type,cmd

# 3405691582
_MAGIC = int('0XCAFEBABE',16)
# 保存常量池
constant_pool = [None]
# class 游标位置
offset = 0
# class 二进制文件数据
data = []

# class 全局游标
def cursor(step):
	global offset
	# print '------data',data
	result = data[offset:offset+step]
	offset += step
	return result

# 解析class文件
def javap(_data):
	global data
	data = _data
	# u4 magic;
	magic = ''.join(cursor(4)).replace('0x','')
	print 'magic:',magic
	if getDecimal(magic) != _MAGIC:
		print 'This is not a valid class file.'
		return
	# u2 minor_version;
	print 'minor_version:',getDecimal(cursor(2))
	# u2 major_version;
	print 'major_version:',getDecimal(cursor(2))
	# u2 constant_pool_count;
	constant_pool_count = getDecimal(cursor(2))-1
	print 'constant_pool_count:',constant_pool_count
	# cp_info constant_pool[constant_pool_count-1];
	constant_pool_index = 0
	while constant_pool_count > constant_pool_index:
		# print 'constant_pool_count:%d constant_pool_index:%d' % (constant_pool_count , constant_pool_index)
		constant_pool_index += 1
		tag = getDecimal(cursor(1))
		constant_name = constant_type.get(tag)
		# print 'tag:%d\tconstant_name:%s' % (tag,constant_name)
		_struct = getStruct(constant_name)
		ref_index,utf8_data = '',''
		up,down,is_longORdouble  = '','',False
		if tag == 7:# Class
			# u1 tag;
			# u2 name_index;
			ref_index=constant_2(2)
		elif tag in (9,10,11):# Fieldref,Methodref,InterfaceMethodref
			# u1 tag;
			# u2 class_index;
			# u2 name_and_type_index;
			ref_index=constant_3(2,2)
		elif tag == 8:# String
			# u1 tag;
			# u2 string_index;
			ref_index=constant_2(2)
		elif tag in (3,4):# Integer,Float
			# u1 tag;
			# u4 bytes;
			ref_index=constant_2(4)
		# 在 Class 文件的常量池中,所有的 8 字节的常量都占两个表成员(项)的空间。如果一个
		# CONSTANT_Long_info 或 CONSTANT_Double_info 结构的项在常量池中的索引为 n,则常量
		# 池中下一个有效的项的索引为 n+2,此时常量池中索引为 n+1 的项有效但必须被认为不可用
		elif tag in (5,6):# long , double
			constant_pool_index += 1
			# u1 tag;
			# u4 high_bytes;
			# u4 low_bytes;
			is_longORdouble = True
			up,down = cursor(4),cursor(4)
		elif tag == 12:# NameAndType
			# u1 tag;
			# u2 name_index;
			# u2 descriptor_index;
			ref_index=constant_3(2,2)
		elif tag == 1:# UTF8
			# u1 tag;
			# u2 length;
			# u1 bytes[length];
			bytes_len = getDecimal(cursor(2))
			utf8_data = ''.join([chr(int(b,16)) for b in cursor(bytes_len)])
			# print 'utf8_data:%s' % utf8_data
		elif tag == 15:# MethodHandler
			# u1 tag;
			# u1 reference_kind;
			# u2 reference_index;
			ref_index=constant_3(1,2)
		elif tag == 16:# MethodType
			# u1 tag;
			# u2 descriptor_index;
			ref_index=constant_2(2)
		elif tag == 18:# InvokeDynamic
			# u1 tag;
			# u2 bootstrap_method_attr_index;
			# u2 name_and_type_index;
			ref_index=constant_3(2,2)
		constant_info = ref_index+utf8_data
		if is_longORdouble:
			constant_pool.extend([up,down])
		else:
			constant_pool.append(constant_info)
		print '#%d %s\t\t%s' % (constant_pool_index,constant_name[9:-5],constant_info)
	# u2 access_flags;
	access_flag_class = accessFlags.getAccessFlag('class',getDecimal(cursor(2)))
	print 'access_flags:%s'% access_flag_class
	# u2 this_class;
	class_index = getDecimal(cursor(2))
	print 'this_class:',getConstant(class_index)
	# u2 super_class;
	print 'super_class:',getConstant(getDecimal(cursor(2)))
	# u2 interfaces_count;
	interfaces_count = getDecimal(cursor(2))
	print 'interfaces_count:',interfaces_count
	if interfaces_count > 0:
		# u2 interfaces[interfaces_count];
		interfaces = [getDecimal(cursor(2)) for i in xrange(interfaces_count)]
		print interfaces
	# u2 fields_count;
	fields_count = getDecimal(cursor(2))
	print 'fields_count:',fields_count
	# field_info fields[fields_count];
	if fields_count > 0:
		methodAndFieldHandler('field',fields_count)
	# u2 methods_count;
	methods_count = getDecimal(cursor(2))
	print 'methods_count:',methods_count
	# method_info methods[methods_count];
	if methods_count > 0:
		methodAndFieldHandler('method',methods_count)
	# u2 attributes_count;
	attributes_count = getDecimal(cursor(2))
	print 'attributes_count:',attributes_count
	# attribute_info attributes[attributes_count];
	if attributes_count > 0:
		attrHandler()

# 处理常量类型结构里元素数量等于2的
def constant_2(second):
	ref_index = '#%d' % getDecimal(cursor(second))
	return ref_index

# 处理常量类型结构里元素数量等于3的
def constant_3(second,third):
	ref_index = '#%d,#%d' % (getDecimal(cursor(second)),getDecimal(cursor(third)))
	return ref_index

# 从常量池中获取值
def getConstant(num):
	source = constant_pool[num]
	if source.__contains__('#'):
		temp = source.replace('#','')
		pointers = temp.split(',')
		target = [constant_pool[int(i)-1] for i in pointers]
		return target
	return source


def methodAndFieldHandler(_type,count):
	if count <= 0:
		print 'count can not lower than zero.[methodAndFieldHandler]'
		return None
	for i in xrange(count):
		print '\t %s:%d' % (_type,i)
		# u2 access_flags;
		print '\t access_flags:' , accessFlags.getAccessFlag(_type,getDecimal(cursor(2)))
		# u2 name_index;
		print '\t name_index:',getConstant(getDecimal(cursor(2)))
		# u2 descriptor_index;
		print '\t descriptor_index:',getConstant(getDecimal(cursor(2)))
		# u2 attributes_count;
		attributes_count = getDecimal(cursor(2))
		print '\t attributes_count:',attributes_count
		# attribute_info attributes[attributes_count];
		if attributes_count > 0:
			attrHandler()
		print '\t---------------'

def attrHandler():
	# u2 attribute_name_index;
	attribute_name = getConstant(cursor(2))
	print '\t attribute_name_index:',attribute_name
	# u4 attribute_length;
	attribute_length = getDecimal(cursor(4))
	print '\t attribute_length:',attribute_length
	# u1 info[attribute_length];
	# _attrInfo = ''.join([chr(int(b,16)) for b in cursor(attribute_length)])
	print '\t attribute_info:',
	if attribute_name == 'Code':#方法表，Java代码编译成的字节码指令
		# u2 max_stack; 
		# u2 max_locals; 
		# u4 code_length; 
		# u1 code[code_length]; 
		# u2 exception_table_length; 
		# { 
		# 	u2 start_pc; 
		# 	u2 end_pc; 
		# 	u2 handler_pc; 
		# 	u2 catch_type; 
		# } exception_table[exception_table_length]; 
		# u2 attributes_count; 
		# attribute_info attributes[attributes_count];

		print 'max_stack:',getDecimal(cursor(2))
		print 'max_locals:',getDecimal(cursor(2))
		code_length = getDecimal(cursor(4))
		print 'code_length:',code_length
		codes = [cmd.get('0x%.2x' % ord(cursor(x))) for x in xrange(code_length)]
		print codes
		exception_table_length = getDecimal(cursor(2))
		print 'exception_table_length:',exception_table_length
		if exception_table_length > 0:
			exceptions = []
			for x in xrange(exception_table_length):
				temp = {}
				temp['start_pc'] = getDecimal(cursor(2))
				temp['end_pc'] = getDecimal(cursor(2))
				temp['handler_pc'] = getDecimal(cursor(2))
				temp['catch_type'] = getDecimal(cursor(2))
				exceptions.append(temp)
			print 'exceptions:',exceptions
		attributes_count = getDecimal(cursor(2))
		for x in xrange(attributes_count):
			attrHandler()
	elif attribute_name == 'ConstantValue':#字段表，field定义的常量池
		# 结构：u2 constantvalue_index , attribute_length === 2
		print getConstant(cursor(attribute_length))
	elif attribute_name == 'StackMapTable':#Code属性 ，JDK1.6中新增的属性，供新的类型检查检验器检查和处理目标方法的局部变量和操作数有所需要的类是否匹配 
		# u2 number_of_entries; 
		# stack_map_frame entries[number_of_entries];
		# union stack_map_frame { 
		# 	same_frame; 
		# 	same_locals_1_stack_item_frame; 
		# 	same_locals_1_stack_item_frame_extended; 
		# 	chop_frame; 
		# 	same_frame_extended; 
		# 	append_frame; 
		# 	full_frame; 
		# }
		number_of_entries = getDecimal(cursor(2))
		'''XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''
	elif attribute_name == 'Exceptions':#方法表 ，方法抛出的异常
		# u2 number_of_exceptions;
		# u2 exception_index_table[number_of_exceptions];
		number_of_exceptions = getDecimal(cursor(2))
		print [getConstant(cursor(2)) for i in xrange(number_of_exceptions)] 
	elif attribute_name == 'InnerClass':#类文件 ，内部类列表 
		# u2 number_of_classes;
		# {
		# 	u2 inner_class_info_index;
		# 	u2 outer_class_info_index;
		# 	u2 inner_name_index;
		# 	u2 inner_class_access_flags;
		# } classes[number_of_classes];
		number_of_classes = getDecimal(cursor(2))
		print ['inner_class_info:%s,outer_class_info:%s,inner_name:%s,inner_class_access:%s\n\t' % (getConstant(cursor(2))\
			,getConstant(cursor(2)),getConstant(cursor(2)),accessFlags.getAccessFlag('class',getDecimal(cursor(2)))) \
			for i in xrange(number_of_exceptions)] 
	elif attribute_name == 'EnclosingMethod':#类文件 ，仅当一个类为局部类或者匿名类是才能拥有这个属性，这个属性用于标识这个类所在的外围方法 
		# u2 class_index
		# u2 method_index;
		print 'class:%s , method:%s' % (getConstant(cursor(2)),getConstant(cursor(2)))
	elif attribute_name == 'Synthetic':#类，方法表，字段表 ，标志方法或字段为编译器自动生成的 
		# ACC_SYNTHETIC ,attribute_length === 0
		print 'ACC_SYNTHETIC'
	elif attribute_name == 'Signature':#类，方法表，字段表 ，用于支持泛型情况下的方法签名
		# u2 signature_index;
		print 'signature:',getConstant(cursor(2))
	elif attribute_name == 'SourceFile':#类文件 ，记录源文件名称 
		# u2 sourcefile_index;
		print 'sourcefile:',getConstant(cursor(2))
	elif attribute_name == 'SourceDebugExtension':#类文件 ，用于存储额外的调试信息 
		# u1 debug_extension[attribute_length];
		print ''.join([chr(getDecimal(cursor(1))) for i in xrange(attribute_length)])
	elif attribute_name == 'LineNumberTable':#Code属性 ，Java源码的行号与字节码指令的对应关系 
		# u2 line_number_table_length;
		# {
		# 	u2 start_pc;
		# 	u2 line_number;
		# } line_number_table[line_number_table_length];
		line_number_table_length = getDecimal(cursor(2))
		print ['start_pc:%d,line_number:%d\n\t' % (getDecimal(cursor(2)),getDecimal(cursor(2))) \
			for i in xrange(number_of_exceptions)] 
	elif attribute_name == 'LocalVariableTable':#Code属性 ，方法的局部变量描述 
		# u2 local_variable_table_length;
		# {
		# 	u2 start_pc;
		# 	u2 length;
		# 	u2 name_index;
		# 	u2 descriptor_index;
		# 	u2 index;
		# } local_variable_table[local_variable_table_length];
		local_variable_table_length = getDecimal(cursor(2))
		'''XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''
		# print ['start_pc:%s,length:%s,name:%s,descriptor:%s,index:%s\n\t' % (getDecimal(cursor(2))\
		# 	,getDecimal(cursor(2)),getConstant(cursor(2)),getConstant(cursor(2)),getDecimal(cursor(2))) \
		# 	for i in xrange(number_of_exceptions)] 
	elif attribute_name == 'LocalVariableTypeTable':#类 ，使用特征签名代替描述符，是为了引入泛型语法之后能描述泛型参数化类型而添加 
		pass
	elif attribute_name == 'Deprecated':#类，方法，字段表，被声明为deprecated的方法和字段
		# attribute_length === 0
		print 'Deprecated'
	elif attribute_name == 'RuntimeVisibleAnnotations':#类，方法表，字段表 ，为动态注解提供支持 
		# u2 num_annotations;
		# annotation annotations[num_annotations];
		num_annotations = getDecimal(cursor(2))
		print [handlerAnnotation() for x in xrange(num_annotations)]

	elif attribute_name == 'RuntimeInvisibleAnnotations':#表，方法表，字段表 ，用于指明哪些注解是运行时不可见的 
		# u2 num_annotations;
		# annotation annotations[num_annotations];
		num_annotations = getDecimal(cursor(2))
		print [handlerAnnotation() for x in xrange(num_annotations)]
	# 数组中每个成员的值表示一个的参数的所有的运行时可见注解。它们的顺序和方法描述符表示的参数的顺序一致
	elif attribute_name == 'RuntimeVisibleParameterAnnotation':#方法表 ，作用与RuntimeVisibleAnnotations属性类似，只不过作用对象为方法
		# u1 num_parameters;
		# {
		# 	u2 num_annotations;
		# 	annotation annotations[num_annotations];
		# } parameter_annotations[num_parameters];
		num_parameters = getDecimal(cursor(1))
		for x in xrange(num_parameters):
			num_annotations = getDecimal(cursor(2))
			print [handlerAnnotation() for x in xrange(num_annotations)]
	elif attribute_name == 'RuntimeInvisibleParameterAnnotation ':#方法表，作用与RuntimeInvisibleAnnotations属性类似，作用对象为方法参数
		# u1 num_parameters;
		# {
		# 	u2 num_annotations;
		# 	annotation annotations[num_annotations];
		# } parameter_annotations[num_parameters];
		num_parameters = getDecimal(cursor(1))
		for x in xrange(num_parameters):
			num_annotations = getDecimal(cursor(2))
			print [handlerAnnotation() for x in xrange(num_annotations)]
	elif attribute_name == 'AnnotationDefault':#方法表，用于记录注解类元素的默认值 
		# element_value default_value;
		hadlerAnnotation_element()
	elif attribute_name == 'BootstrapMethods':#类文件 ，用于保存invokeddynamic指令引用的引导方式限定符  
		# u2 num_bootstrap_methods;
		# {
		# 	u2 bootstrap_method_ref;
		# 	u2 num_bootstrap_arguments;
		# 	u2 bootstrap_arguments[num_bootstrap_arguments];
		# } bootstrap_methods[num_bootstrap_methods];
		num_bootstrap_methods = getDecimal(cursor(2))
		for x in xrange(num_bootstrap_methods):
			'''
			bootstrap_method_ref 项的值必须是一个对常量池的有效索引。常量池在该索引处的值必须是一个 CONSTANT_MethodHandle_info 结构。
			注意:此 CONSTANT_MethodHandle_info 结构的 reference_kind 项应为值 6	(REF_invokeStatic)或 8(REF_newInvokeSpecial)
			(§5.4.3.5),否则在 invokedynamic 指令解析调用点限定符时,引导方法会执行失败。
			'''
			bootstrap_method = getConstant(cursor(2))
			print 'bootstrap_method:',bootstrap_method
			num_bootstrap_arguments = getDecimal(cursor(2))
			print [getConstant(cursor(2)) for x in xrange(num_bootstrap_arguments)]
	else:
		print 'ERROR:cannot parse this attribute %s' % attribute_name ,\
		 '\t attribute_info:',cursor(attribute_length)
		
def handlerAnnotation():
	annotation = {}
	'''
	annotation {
		u2 type_index;
		u2 num_element_value_pairs;
		{
			u2 element_name_index;
			element_value value;
		} element_value_pairs[num_element_value_pairs]
	}
	------------------------------------------------
	'''
	annotation['type_index'] = getConstant(cursor(2))
	num_element_value_pairs = getDecimal(cursor(2))
	annotation['num_element_value_pairs'] = num_element_value_pairs
	pairs = {}
	for x in xrange(num_element_value_pairs):
		pairs['element_name_index'] = getConstant(cursor(2))
		pairs['element_value'] = hadlerAnnotation_element()
	return annotation

def hadlerAnnotation_element():
	element = {}
	'''
	element_value {
		u1 tag;
		union {
			u2 const_value_index;
			{
				u2 type_name_index;
				u2 const_name_index;
			} enum_const_value;
			u2 class_info_index;
			annotation annotation_value;
			{
				u2 num_values;
				element_value values[num_values];
			} array_value;
		} value;
	}

	------------------------------------------------
	tag:
	B byte 有符号字节型数
	C char Unicode 字符,UTF-16 编码
	D double 双精度浮点数
	F float 单精度浮点数
	I int 整型数
	J long 长整数
	S short 有符号短整数
	Z boolean 布尔值 true/false
	s String
	e enum constant
	c class
	@ annotation type
	[ array
	------------------------------------------------
	当 tag 项为'e'时,enum_const_value 项才会被使用。
	当 tag 项为'c'时,class_info_index 项才会被使用。
	当 tag 项为'@'时,annotation_value 项才会被使用。
	当 tag 项为'['时, array_value 项才会被使用
	'''
	tag = chr(getDecimal(cursor(1)))
	element['tag'] = tag
	element['const_value'] = getConstant(cursor(2))
	if 'e' == tag:
		element['type_name'] = getConstant(cursor(2))
		element['const_name'] = getConstant(cursor(2))
	elif 'c' == tag:
		element['class_info'] = getConstant(cursor(2))
	elif '@' == tag:
		element['annotation'] = handlerAnnotation()
	elif '[' == tag:
		num_values = getDecimal(cursor(2))
		child_element = []
		for x in xrange(num_values):
			child_element.append(hadlerAnnotation_element())
		element['array_value'] = child_element
	return element


# 获取常量类型结构定义
# def getStruct(struct_name):
# 	return getattr(struct,struct_name)

# 程序入口
if __name__=="__main__":
	# data = ['0xca', '0xfe', '0xba', '0xbe', '0x00', '0x00', '0x00', '0x33', '0x00', '0x20', '0x0a', '0x00', '0x07', '0x00', '0x11', '0x09', '0x00', '0x12', '0x00', '0x13', '0x08', '0x00', '0x14', '0x0a', '0x00', '0x15', '0x00', '0x16', '0x08', '0x00', '0x17', '0x07', '0x00', '0x18', '0x07', '0x00', '0x19', '0x01', '0x00', '0x06', '0x3c', '0x69', '0x6e', '0x69', '0x74', '0x3e', '0x01', '0x00', '0x03', '0x28', '0x29', '0x56', '0x01', '0x00', '0x04', '0x43', '0x6f', '0x64', '0x65', '0x01', '0x00', '0x0f', '0x4c', '0x69', '0x6e', '0x65', '0x4e', '0x75', '0x6d', '0x62', '0x65', '0x72', '0x54', '0x61', '0x62', '0x6c', '0x65', '0x01', '0x00', '0x04', '0x6d', '0x61', '0x69', '0x6e', '0x01', '0x00', '0x16', '0x28', '0x5b', '0x4c', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x53', '0x74', '0x72', '0x69', '0x6e', '0x67', '0x3b', '0x29', '0x56', '0x01', '0x00', '0x0d', '0x53', '0x74', '0x61', '0x63', '0x6b', '0x4d', '0x61', '0x70', '0x54', '0x61', '0x62', '0x6c', '0x65', '0x01', '0x00', '0x0a', '0x53', '0x6f', '0x75', '0x72', '0x63', '0x65', '0x46', '0x69', '0x6c', '0x65', '0x01', '0x00', '0x09', '0x64', '0x65', '0x6d', '0x6f', '0x2e', '0x6a', '0x61', '0x76', '0x61', '0x0c', '0x00', '0x08', '0x00', '0x09', '0x07', '0x00', '0x1a', '0x0c', '0x00', '0x1b', '0x00', '0x1c', '0x01', '0x00', '0x06', '0x62', '0x69', '0x67', '0x67', '0x65', '0x72', '0x07', '0x00', '0x1d', '0x0c', '0x00', '0x1e', '0x00', '0x1f', '0x01', '0x00', '0x07', '0x73', '0x6d', '0x61', '0x6c', '0x6c', '0x65', '0x72', '0x01', '0x00', '0x08', '0x63', '0x6c', '0x73', '0x2f', '0x64', '0x65', '0x6d', '0x6f', '0x01', '0x00', '0x10', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x4f', '0x62', '0x6a', '0x65', '0x63', '0x74', '0x01', '0x00', '0x10', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x53', '0x79', '0x73', '0x74', '0x65', '0x6d', '0x01', '0x00', '0x03', '0x6f', '0x75', '0x74', '0x01', '0x00', '0x15', '0x4c', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x69', '0x6f', '0x2f', '0x50', '0x72', '0x69', '0x6e', '0x74', '0x53', '0x74', '0x72', '0x65', '0x61', '0x6d', '0x3b', '0x01', '0x00', '0x13', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x69', '0x6f', '0x2f', '0x50', '0x72', '0x69', '0x6e', '0x74', '0x53', '0x74', '0x72', '0x65', '0x61', '0x6d', '0x01', '0x00', '0x07', '0x70', '0x72', '0x69', '0x6e', '0x74', '0x6c', '0x6e', '0x01', '0x00', '0x15', '0x28', '0x4c', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x53', '0x74', '0x72', '0x69', '0x6e', '0x67', '0x3b', '0x29', '0x56', '0x00', '0x21', '0x00', '0x06', '0x00', '0x07', '0x00', '0x00', '0x00', '0x00', '0x00', '0x02', '0x00', '0x01', '0x00', '0x08', '0x00', '0x09', '0x00', '0x01', '0x00', '0x0a', '0x00', '0x00', '0x00', '0x1d', '0x00', '0x01', '0x00', '0x01', '0x00', '0x00', '0x00', '0x05', '0x2a', '0xb7', '0x00', '0x01', '0xb1', '0x00', '0x00', '0x00', '0x01', '0x00', '0x0b', '0x00', '0x00', '0x00', '0x06', '0x00', '0x01', '0x00', '0x00', '0x00', '0x03', '0x00', '0x09', '0x00', '0x0c', '0x00', '0x0d', '0x00', '0x01', '0x00', '0x0a', '0x00', '0x00', '0x00', '0x57', '0x00', '0x02', '0x00', '0x03', '0x00', '0x00', '0x00', '0x1d', '0x04', '0x3c', '0x05', '0x3d', '0x1b', '0x1c', '0xa4', '0x00', '0x0e', '0xb2', '0x00', '0x02', '0x12', '0x03', '0xb6', '0x00', '0x04', '0xa7', '0x00', '0x0b', '0xb2', '0x00', '0x02', '0x12', '0x05', '0xb6', '0x00', '0x04', '0xb1', '0x00', '0x00', '0x00', '0x02', '0x00', '0x0b', '0x00', '0x00', '0x00', '0x1a', '0x00', '0x06', '0x00', '0x00', '0x00', '0x06', '0x00', '0x02', '0x00', '0x07', '0x00', '0x04', '0x00', '0x08', '0x00', '0x09', '0x00', '0x09', '0x00', '0x14', '0x00', '0x0b', '0x00', '0x1c', '0x00', '0x0d', '0x00', '0x0e', '0x00', '0x00', '0x00', '0x08', '0x00', '0x02', '0xfd', '0x00', '0x14', '0x01', '0x01', '0x07', '0x00', '0x01', '0x00', '0x0f', '0x00', '0x00', '0x00', '0x02', '0x00', '0x10']
	# javap(data)
	# print _MAGIC
	# print range(40,46)
	# print ''.join([chr(int(data[i],16)) for i in xrange(40,46)])
	# print getStruct(constant_type.get('1'))

	# constant_pool = [1,2,3,4,5,6]
	# pointers = [2,3]
	# print tuple([constant_pool[i-1] for i in pointers])
	# print '%s %s' % tuple([constant_pool[i-1] for i in pointers])
	print 123
	print ['this %s at %d' % ('getConstant(cursor(2))',i) for i in xrange(2)]
	print constant_pool[0]
	print 

