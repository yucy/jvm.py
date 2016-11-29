# -*- coding:utf-8 -*-
import struct,accessFlags

# 3405691582
_MAGIC = int('0XCAFEBABE',16)
# 保存常量池
constant_pool = []
offset = 0
data = []

def cursor(step):
	global offset
	# print '------data',data
	if step == 0:
		return None
	result = data[offset:offset+step]
	offset += step
	return result

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
	source = constant_pool[num-1]
	if source.__contains__('#'):
		temp = source.replace('#','')
		pointers = temp.split(',')
		target = [constant_pool[int(i)-1] for i in pointers]
		return target
	return source

def attrHandler():
	# u2 attribute_name_index;
	print '\t attribute_name_index:',getConstant(getDecimal(cursor(2)))
	# u4 attribute_length;
	attribute_length = getDecimal(cursor(4))
	print '\t attribute_length:',attribute_length
	# u1 info[attribute_length];
	# _attrInfo = ''.join([chr(int(b,16)) for b in cursor(attribute_length)])
	print '\t attribute_info:',cursor(attribute_length)

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


constant_type={
	1:'CONSTANT_Utf8_info',
	3:'CONSTANT_Integer_info',
	4:'CONSTANT_Float_info',
	5:'CONSTANT_Long_info',
	6:'CONSTANT_Double_info',
	7:'CONSTANT_Class_info',
	8:'CONSTANT_String_info',
	9:'CONSTANT_Fieldref_info',
	10:'CONSTANT_Methodref_info',
	11:'CONSTANT_InterfaceMethodref_info',
	12:'CONSTANT_NameAndType_info',
	15:'CONSTANT_MethodHandle_info',
	16:'CONSTANT_MethodType_info',
	18:'CONSTANT_InvokeDynamic_info',
}

inner_cmd = {
	'0x00':'nop',#什么都不做。
	'0x01':'aconst_null',#将null推送至栈顶。
	'0x02':'iconst_m1',#将int型-1推送至栈顶。
	'0x03':'iconst_0',#将int型0推送至栈顶。
	'0x04':'iconst_1',#将int型1推送至栈顶。
	'0x05':'iconst_2',#将int型2推送至栈顶。
	'0x06':'iconst_3',#将int型3推送至栈顶。
	'0x07':'iconst_4',#将int型4推送至栈顶。
	'0x08':'iconst_5',#将int型5推送至栈顶。
	'0x09':'lconst_0',#将long型0推送至栈顶。
	'0x0a':'lconst_1',#将long型1推送至栈顶。
	'0x0b':'fconst_0',#将float型0推送至栈顶。
	'0x0c':'fconst_1',#将float型1推送至栈顶。
	'0x0d':'fconst_2',#将float型2推送至栈顶。
	'0x0e':'dconst_0',#将double型0推送至栈顶。
	'0x0f':'dconst_1',#将double型1推送至栈顶。
	'0x10':'bipush',#将单字节的常量值（-128~127）推送至栈顶。
	'0x11':'sipush',#将一个短整型常量值（-32768~32767）推送至栈顶。
	'0x12':'ldc',#将int，float或String型常量值从常量池中推送至栈顶。
	'0x13':'ldc_w',#将int，float或String型常量值从常量池中推送至栈顶（宽索引）。
	'0x14':'ldc2_w',#将long或double型常量值从常量池中推送至栈顶（宽索引）。
	'0x15':'iload',#将指定的int型局部变量推送至栈顶。
	'0x16':'lload',#将指定的long型局部变量推送至栈顶。
	'0x17':'fload',#将指定的float型局部变量推送至栈顶。
	'0x18':'dload',#将指定的double型局部变量推送至栈顶。
	'0x19':'aload',#将指定的引用类型局部变量推送至栈顶。
	'0x1a':'iload_0',#将第一个int型局部变量推送至栈顶。
	'0x1b':'iload_1',#将第二个int型局部变量推送至栈顶。
	'0x1c':'iload_2',#将第三个int型局部变量推送至栈顶。
	'0x1d':'iload_3',#将第四个int型局部变量推送至栈顶。
	'0x1e':'lload_0',#将第一个long型局部变量推送至栈顶。
	'0x1f':'lload_1',#将第二个long型局部变量推送至栈顶。
	'0x20':'lload_2',#将第三个long型局部变量推送至栈顶。
	'0x21':'lload_3',#将第四个long型局部变量推送至栈顶。
	'0x22':'fload_0',#将第一个float型局部变量推送至栈顶。
	'0x23':'fload_1',#将第二个float型局部变量推送至栈顶。
	'0x24':'fload_2',#将第三个float型局部变量推送至栈顶
	'0x25':'fload_3',#将第四个float型局部变量推送至栈顶。
	'0x26':'dload_0',#将第一个double型局部变量推送至栈顶。
	'0x27':'dload_1',#将第二个double型局部变量推送至栈顶。
	'0x28':'dload_2',#将第三个double型局部变量推送至栈顶。
	'0x29':'dload_3',#将第四个double型局部变量推送至栈顶。
	'0x2a':'aload_0',#将第一个引用类型局部变量推送至栈顶。
	'0x2b':'aload_1',#将第二个引用类型局部变量推送至栈顶。
	'0x2c':'aload_2',#将第三个引用类型局部变量推送至栈顶。
	'0x2d':'aload_3',#将第四个引用类型局部变量推送至栈顶。
	'0x2e':'iaload',#将int型数组指定索引的值推送至栈顶。
	'0x2f':'laload',#将long型数组指定索引的值推送至栈顶。
	'0x30':'faload',#将float型数组指定索引的值推送至栈顶。
	'0x31':'daload',#将double型数组指定索引的值推送至栈顶。
	'0x32':'aaload',#将引用型数组指定索引的值推送至栈顶。
	'0x33':'baload',#将boolean或byte型数组指定索引的值推送至栈顶。
	'0x34':'caload',#将char型数组指定索引的值推送至栈顶。
	'0x35':'saload',#将short型数组指定索引的值推送至栈顶。
	'0x36':'istore',#将栈顶int型数值存入指定局部变量。
	'0x37':'lstore',#将栈顶long型数值存入指定局部变量。
	'0x38':'fstore',#将栈顶float型数值存入指定局部变量。
	'0x39':'dstore',#将栈顶double型数值存入指定局部变量。
	'0x3a':'astore',#将栈顶引用型数值存入指定局部变量。
	'0x3b':'istore_0',#将栈顶int型数值存入第一个局部变量。
	'0x3c':'istore_1',#将栈顶int型数值存入第二个局部变量。
	'0x3d':'istore_2',#将栈顶int型数值存入第三个局部变量。
	'0x3e':'istore_3',#将栈顶int型数值存入第四个局部变量。
	'0x3f':'lstore_0',#将栈顶long型数值存入第一个局部变量。
	'0x40':'lstore_1',#将栈顶long型数值存入第二个局部变量。
	'0x41':'lstore_2',#将栈顶long型数值存入第三个局部变量。
	'0x42':'lstore_3',#将栈顶long型数值存入第四个局部变量。
	'0x43':'fstore_0',#将栈顶float型数值存入第一个局部变量。
	'0x44':'fstore_1',#将栈顶float型数值存入第二个局部变量。
	'0x45':'fstore_2',#将栈顶float型数值存入第三个局部变量。
	'0x46':'fstore_3',#将栈顶float型数值存入第四个局部变量。
	'0x47':'dstore_0',#将栈顶double型数值存入第一个局部变量。
	'0x48':'dstore_1',#将栈顶double型数值存入第二个局部变量。
	'0x49':'dstore_2',#将栈顶double型数值存入第三个局部变量。
	'0x4a':'dstore_3',#将栈顶double型数值存入第四个局部变量。
	'0x4b':'astore_0',#将栈顶引用型数值存入第一个局部变量。
	'0x4c':'astore_1',#将栈顶引用型数值存入第二个局部变量。
	'0x4d':'astore_2',#将栈顶引用型数值存入第三个局部变量
	'0x4e':'astore_3',#将栈顶引用型数值存入第四个局部变量。
	'0x4f':'iastore',#将栈顶int型数值存入指定数组的指定索引位置
	'0x50':'lastore',#将栈顶long型数值存入指定数组的指定索引位置。
	'0x51':'fastore',#将栈顶float型数值存入指定数组的指定索引位置。
	'0x52':'dastore',#将栈顶double型数值存入指定数组的指定索引位置。
	'0x53':'aastore',#将栈顶引用型数值存入指定数组的指定索引位置。
	'0x54':'bastore',#将栈顶boolean或byte型数值存入指定数组的指定索引位置。
	'0x55':'castore',#将栈顶char型数值存入指定数组的指定索引位置
	'0x56':'sastore',#将栈顶short型数值存入指定数组的指定索引位置。
	'0x57':'pop',#将栈顶数值弹出（数值不能是long或double类型的）。
	'0x58':'pop2',#将栈顶的一个（long或double类型的）或两个数值弹出（其它）。
	'0x59':'dup',#复制栈顶数值并将复制值压入栈顶。
	'0x5a':'dup_x1',#复制栈顶数值并将两个复制值压入栈顶。
	'0x5b':'dup_x2',#复制栈顶数值并将三个（或两个）复制值压入栈顶。
	'0x5c':'dup2',#复制栈顶一个（long或double类型的)或两个（其它）数值并将复制值压入栈顶。
	'0x5d':'dup2_x1',#dup_x1指令的双倍版本。
	'0x5e':'dup2_x2',#dup_x2指令的双倍版本。
	'0x5f':'swap',#将栈最顶端的两个数值互换（数值不能是long或double类型的）。
	'0x60':'iadd',#将栈顶两int型数值相加并将结果压入栈顶。
	'0x61':'ladd',#将栈顶两long型数值相加并将结果压入栈顶。
	'0x62':'fadd',#将栈顶两float型数值相加并将结果压入栈顶。
	'0x63':'dadd',#将栈顶两double型数值相加并将结果压入栈顶。
	'0x64':'isub',#将栈顶两int型数值相减并将结果压入栈顶。
	'0x65':'lsub',#将栈顶两long型数值相减并将结果压入栈顶。
	'0x66':'fsub',#将栈顶两float型数值相减并将结果压入栈顶。
	'0x67':'dsub',#将栈顶两double型数值相减并将结果压入栈顶。
	'0x68':'imul',#将栈顶两int型数值相乘并将结果压入栈顶。。
	'0x69':'lmul',#将栈顶两long型数值相乘并将结果压入栈顶。
	'0x6a':'fmul',#将栈顶两float型数值相乘并将结果压入栈顶。
	'0x6b':'dmul',#将栈顶两double型数值相乘并将结果压入栈顶。
	'0x6c':'idiv',#将栈顶两int型数值相除并将结果压入栈顶。
	'0x6d':'ldiv',#将栈顶两long型数值相除并将结果压入栈顶。
	'0x6e':'fdiv',#将栈顶两float型数值相除并将结果压入栈顶。
	'0x6f':'ddiv',#将栈顶两double型数值相除并将结果压入栈顶。
	'0x70':'irem',#将栈顶两int型数值作取模运算并将结果压入栈顶。
	'0x71':'lrem',#将栈顶两long型数值作取模运算并将结果压入栈顶。
	'0x72':'frem',#将栈顶两float型数值作取模运算并将结果压入栈顶。
	'0x73':'drem',#将栈顶两double型数值作取模运算并将结果压入栈顶。
	'0x74':'ineg',#将栈顶int型数值取负并将结果压入栈顶。
	'0x75':'lneg',#将栈顶long型数值取负并将结果压入栈顶。
	'0x76':'fneg',#将栈顶float型数值取负并将结果压入栈顶。
	'0x77':'dneg',#将栈顶double型数值取负并将结果压入栈顶。
	'0x78':'ishl',#将int型数值左移位指定位数并将结果压入栈顶。
	'0x79':'lshl',#将long型数值左移位指定位数并将结果压入栈顶。
	'0x7a':'ishr',#将int型数值右（有符号）移位指定位数并将结果压入栈顶。
	'0x7b':'lshr',#将long型数值右（有符号）移位指定位数并将结果压入栈顶。
	'0x7c':'iushr',#将int型数值右（无符号）移位指定位数并将结果压入栈顶。
	'0x7d':'lushr',#将long型数值右（无符号）移位指定位数并将结果压入栈顶。
	'0x7e':'iand',#将栈顶两int型数值作“按位与”并将结果压入栈顶。
	'0x7f':'land',#将栈顶两long型数值作“按位与”并将结果压入栈顶。
	'0x80':'ior',#将栈顶两int型数值作“按位或”并将结果压入栈顶。
	'0x81':'lor',#将栈顶两long型数值作“按位或”并将结果压入栈顶。
	'0x82':'ixor',#将栈顶两int型数值作“按位异或”并将结果压入栈顶。
	'0x83':'lxor',#将栈顶两long型数值作“按位异或”并将结果压入栈顶。
	'0x84':'iinc',#将指定int型变量增加指定值。
	'0x85':'i2l',#将栈顶int型数值强制转换成long型数值并将结果压入栈顶。
	'0x86':'i2f',#将栈顶int型数值强制转换成float型数值并将结果压入栈顶。
	'0x87':'i2d',#将栈顶int型数值强制转换成double型数值并将结果压入栈顶。
	'0x88':'l2i',#将栈顶long型数值强制转换成int型数值并将结果压入栈顶。
	'0x89':'l2f',#将栈顶long型数值强制转换成float型数值并将结果压入栈顶。
	'0x8a':'l2d',#将栈顶long型数值强制转换成double型数值并将结果压入栈顶。
	'0x8b':'f2i',#将栈顶float型数值强制转换成int型数值并将结果压入栈顶。
	'0x8c':'f2l',#将栈顶float型数值强制转换成long型数值并将结果压入栈顶。
	'0x8d':'f2d',#将栈顶float型数值强制转换成double型数值并将结果压入栈顶。
	'0x8e':'d2i',#将栈顶double型数值强制转换成int型数值并将结果压入栈顶。
	'0x8f':'d2l',#将栈顶double型数值强制转换成long型数值并将结果压入栈顶。
	'0x90':'d2f',#将栈顶double型数值强制转换成float型数值并将结果压入栈顶。
	'0x91':'i2b',#将栈顶int型数值强制转换成byte型数值并将结果压入栈顶。
	'0x92':'i2c',#将栈顶int型数值强制转换成char型数值并将结果压入栈顶。
	'0x93':'i2s',#将栈顶int型数值强制转换成short型数值并将结果压入栈顶。
	'0x94':'lcmp',#比较栈顶两long型数值大小，并将结果（1，0，-1）压入栈顶。
	'0x95':'fcmpl',#比较栈顶两float型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将-1压入栈顶。
	'0x96':'fcmpg',#比较栈顶两float型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将1压入栈顶。
	'0x97':'dcmpl',#比较栈顶两double型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将-1压入栈顶。
	'0x98':'dcmpg',#比较栈顶两double型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将1压入栈顶。
	'0x99':'ifeq',#当栈顶int型数值等于0时跳转。
	'0x9a':'ifne',#当栈顶int型数值不等于0时跳转。
	'0x9b':'iflt',#当栈顶int型数值小于0时跳转。
	'0x9c':'ifge',#当栈顶int型数值大于等于0时跳转。
	'0x9d':'ifgt',#当栈顶int型数值大于0时跳转。
	'0x9e':'ifle',#当栈顶int型数值小于等于0时跳转。
	'0x9f':'if_icmpeq',#比较栈顶两int型数值大小，当结果等于0时跳转。
	'0xa0':'if_icmpne',#比较栈顶两int型数值大小，当结果不等于0时跳转。
	'0xa1':'if_icmplt',#比较栈顶两int型数值大小，当结果小于0时跳转。
	'0xa2':'if_icmpge',#比较栈顶两int型数值大小，当结果大于等于0时跳转。
	'0xa3':'if_icmpgt',#比较栈顶两int型数值大小，当结果大于0时跳转
	'0xa4':'if_icmple',#比较栈顶两int型数值大小，当结果小于等于0时跳转。
	'0xa5':'if_acmpeq',#比较栈顶两引用型数值，当结果相等时跳转。
	'0xa6':'if_acmpne',#比较栈顶两引用型数值，当结果不相等时跳转。
	'0xa7':'goto',#无条件跳转。
	'0xa8':'jsr',#跳转至指定16位offset位置，并将jsr下一条指令地址压入栈顶。
	'0xa9':'ret',#返回至局部变量指定的index的指令位置（一般与jsr，jsr_w联合使用）。
	'0xaa':'tableswitch',#用于switch条件跳转，case值连续（可变长度指令）。
	'0xab':'lookupswitch',#用于switch条件跳转，case值不连续（可变长度指令）。
	'0xac':'ireturn',#从当前方法返回int。
	'0xad':'lreturn',#从当前方法返回long。
	'0xae':'freturn',#从当前方法返回float。
	'0xaf':'dreturn',#从当前方法返回double。
	'0xb0':'areturn',#从当前方法返回对象引用。
	'0xb1':'return',#从当前方法返回void。
	'0xb2':'getstatic',#获取指定类的静态域，并将其值压入栈顶。
	'0xb3':'putstatic',#为指定的类的静态域赋值。
	'0xb4':'getfield',#获取指定类的实例域，并将其值压入栈顶。
	'0xb5':'putfield',#为指定的类的实例域赋值。
	'0xb6':'invokevirtual',#调用实例方法。
	'0xb7':'invokespecial',#调用超类构造方法，实例初始化方法，私有方法。
	'0xb8':'invokestatic',#调用静态方法。
	'0xb9':'invokeinterface',#调用接口方法。
	'0xba':'invokedynamic',#调用动态链接方法，注：操作码为186（0xba）的invokedynamic指令是Java SE 7中新加入的。
	'0xbb':'new',#创建一个对象，并将其引用值压入栈顶。
	'0xbc':'newarray',#创建一个指定原始类型（如int、float、char„„）的数组，并将其引用值压入栈顶。
	'0xbd':'anewarray',#创建一个引用型（如类，接口，数组）的数组，并将其引用值压入栈顶。
	'0xbe':'arraylength',#获得数组的长度值并压入栈顶。
	'0xbf':'athrow',#将栈顶的异常抛出。
	'0xc0':'checkcast',#检验类型转换，检验未通过将抛出ClassCastException。
	'0xc1':'instanceof',#检验对象是否是指定的类的实例，如果是将1压入栈顶，否则将0压入栈顶。
	'0xc2':'monitorenter',#获得对象的monitor，用于同步方法或同步块。
	'0xc3':'monitorexit',#释放对象的monitor，用于同步方法或同步块。
	'0xc4':'wide',#扩展访问局部变量表的索引宽度。
	'0xc5':'multianewarray',#创建指定类型和指定维度的多维数组（执行该指令时，操作栈中必须包含各维度的长度值），并将其引用值压入栈顶。
	'0xc6':'ifnull',#为null时跳转。
	'0xc7':'ifnonnull',#不为null时跳转。
	'0xc8':'goto_w',#无条件跳转（宽索引）。
	'0xc9':'jsr_w',#跳转至指定32位地址偏移量位置，并将jsr_w下一条指令地址压入栈顶。（保留指令）
	'0xca':'breakpoint',#调试时的断点标志。
	'0xfe':'impdep1',#用于在特定硬件中使用的语言后门。
	'0xff':'impdep1',#用于在特定硬件中使用的语言后门。
}

# 将多个十六进制整合转化为十进制，并返回
def getDecimal(arr):
	if len(arr) == 0:
		return None
	else:
		return int('0x%s' % ''.join(arr).replace('0x',''),16)

# 获取常量类型结构定义
def getStruct(struct_name):
	return getattr(struct,struct_name)

# 程序入口
if __name__=="__main__":
	data = ['0xca', '0xfe', '0xba', '0xbe', '0x00', '0x00', '0x00', '0x33', '0x00', '0x20', '0x0a', '0x00', '0x07', '0x00', '0x11', '0x09', '0x00', '0x12', '0x00', '0x13', '0x08', '0x00', '0x14', '0x0a', '0x00', '0x15', '0x00', '0x16', '0x08', '0x00', '0x17', '0x07', '0x00', '0x18', '0x07', '0x00', '0x19', '0x01', '0x00', '0x06', '0x3c', '0x69', '0x6e', '0x69', '0x74', '0x3e', '0x01', '0x00', '0x03', '0x28', '0x29', '0x56', '0x01', '0x00', '0x04', '0x43', '0x6f', '0x64', '0x65', '0x01', '0x00', '0x0f', '0x4c', '0x69', '0x6e', '0x65', '0x4e', '0x75', '0x6d', '0x62', '0x65', '0x72', '0x54', '0x61', '0x62', '0x6c', '0x65', '0x01', '0x00', '0x04', '0x6d', '0x61', '0x69', '0x6e', '0x01', '0x00', '0x16', '0x28', '0x5b', '0x4c', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x53', '0x74', '0x72', '0x69', '0x6e', '0x67', '0x3b', '0x29', '0x56', '0x01', '0x00', '0x0d', '0x53', '0x74', '0x61', '0x63', '0x6b', '0x4d', '0x61', '0x70', '0x54', '0x61', '0x62', '0x6c', '0x65', '0x01', '0x00', '0x0a', '0x53', '0x6f', '0x75', '0x72', '0x63', '0x65', '0x46', '0x69', '0x6c', '0x65', '0x01', '0x00', '0x09', '0x64', '0x65', '0x6d', '0x6f', '0x2e', '0x6a', '0x61', '0x76', '0x61', '0x0c', '0x00', '0x08', '0x00', '0x09', '0x07', '0x00', '0x1a', '0x0c', '0x00', '0x1b', '0x00', '0x1c', '0x01', '0x00', '0x06', '0x62', '0x69', '0x67', '0x67', '0x65', '0x72', '0x07', '0x00', '0x1d', '0x0c', '0x00', '0x1e', '0x00', '0x1f', '0x01', '0x00', '0x07', '0x73', '0x6d', '0x61', '0x6c', '0x6c', '0x65', '0x72', '0x01', '0x00', '0x08', '0x63', '0x6c', '0x73', '0x2f', '0x64', '0x65', '0x6d', '0x6f', '0x01', '0x00', '0x10', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x4f', '0x62', '0x6a', '0x65', '0x63', '0x74', '0x01', '0x00', '0x10', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x53', '0x79', '0x73', '0x74', '0x65', '0x6d', '0x01', '0x00', '0x03', '0x6f', '0x75', '0x74', '0x01', '0x00', '0x15', '0x4c', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x69', '0x6f', '0x2f', '0x50', '0x72', '0x69', '0x6e', '0x74', '0x53', '0x74', '0x72', '0x65', '0x61', '0x6d', '0x3b', '0x01', '0x00', '0x13', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x69', '0x6f', '0x2f', '0x50', '0x72', '0x69', '0x6e', '0x74', '0x53', '0x74', '0x72', '0x65', '0x61', '0x6d', '0x01', '0x00', '0x07', '0x70', '0x72', '0x69', '0x6e', '0x74', '0x6c', '0x6e', '0x01', '0x00', '0x15', '0x28', '0x4c', '0x6a', '0x61', '0x76', '0x61', '0x2f', '0x6c', '0x61', '0x6e', '0x67', '0x2f', '0x53', '0x74', '0x72', '0x69', '0x6e', '0x67', '0x3b', '0x29', '0x56', '0x00', '0x21', '0x00', '0x06', '0x00', '0x07', '0x00', '0x00', '0x00', '0x00', '0x00', '0x02', '0x00', '0x01', '0x00', '0x08', '0x00', '0x09', '0x00', '0x01', '0x00', '0x0a', '0x00', '0x00', '0x00', '0x1d', '0x00', '0x01', '0x00', '0x01', '0x00', '0x00', '0x00', '0x05', '0x2a', '0xb7', '0x00', '0x01', '0xb1', '0x00', '0x00', '0x00', '0x01', '0x00', '0x0b', '0x00', '0x00', '0x00', '0x06', '0x00', '0x01', '0x00', '0x00', '0x00', '0x03', '0x00', '0x09', '0x00', '0x0c', '0x00', '0x0d', '0x00', '0x01', '0x00', '0x0a', '0x00', '0x00', '0x00', '0x57', '0x00', '0x02', '0x00', '0x03', '0x00', '0x00', '0x00', '0x1d', '0x04', '0x3c', '0x05', '0x3d', '0x1b', '0x1c', '0xa4', '0x00', '0x0e', '0xb2', '0x00', '0x02', '0x12', '0x03', '0xb6', '0x00', '0x04', '0xa7', '0x00', '0x0b', '0xb2', '0x00', '0x02', '0x12', '0x05', '0xb6', '0x00', '0x04', '0xb1', '0x00', '0x00', '0x00', '0x02', '0x00', '0x0b', '0x00', '0x00', '0x00', '0x1a', '0x00', '0x06', '0x00', '0x00', '0x00', '0x06', '0x00', '0x02', '0x00', '0x07', '0x00', '0x04', '0x00', '0x08', '0x00', '0x09', '0x00', '0x09', '0x00', '0x14', '0x00', '0x0b', '0x00', '0x1c', '0x00', '0x0d', '0x00', '0x0e', '0x00', '0x00', '0x00', '0x08', '0x00', '0x02', '0xfd', '0x00', '0x14', '0x01', '0x01', '0x07', '0x00', '0x01', '0x00', '0x0f', '0x00', '0x00', '0x00', '0x02', '0x00', '0x10']
	javap(data)
	# print _MAGIC
	# print range(40,46)
	# print ''.join([chr(int(data[i],16)) for i in xrange(40,46)])
	# print getStruct(constant_type.get('1'))

	# constant_pool = [1,2,3,4,5,6]
	# pointers = [2,3]
	# print tuple([constant_pool[i-1] for i in pointers])
	# print '%s %s' % tuple([constant_pool[i-1] for i in pointers])
	

