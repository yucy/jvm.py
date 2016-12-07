# -*- coding:utf-8 -*-

import sys
sys.path.append('..')
import accessFlags
from common.utils import getDecimal


class CClassFile(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		self.magic = arg.get('magic',None)# u4 
		self.minor_version = arg.get('minor_version',0)# u2 
		self.major_version = arg.get('major_version',None)# u2 
		self.constant_pool_count = arg.get('constant_pool_count',0)# u2 
		self.cp_info = arg.get('cp_info',[])
		self.access_flags = arg.get('access_flags',None)# u2 
		self.this_class = arg.get('this_class',None)# u2 
		self.super_class = arg.get('super_class',None)# u2 
		self.interfaces_count = arg.get('interfaces_count',0)# u2 
		self.interfaces = arg.get('interfaces',[]) # u2 
		self.fields_count = arg.get('fields_count',0)# u2 
		self.field_info = arg.get('field_info',[])
		self.methods_count = arg.get('methods_count',0)# u2 
		self.method_info = arg.get('method_info',[])
		self.attributes_count = arg.get('attributes_count',0)# u2 
		self.attribute_info = arg.get('attribute_info',[])
	def setFieldInfo(self,fields):
		self.field_info = fields
		self.aaa = 1
		self.toString()

	def toString(self):
		print self.magic,self.minor_version,self.major_version,self.constant_pool_count

# =================================================================
class FieldInfo(object):
	"""docstring for FieldInfo"""
	def __init__(self, arg):
		self.access_flags = arg.get('access_flags',None) # u2 
		self.name = arg.get('name',None) # u2 
		self.descriptor = arg.get('descriptor',None) # u2 
		self.attributes_count = arg.get('attributes_count',0) # u2 
		self.attributes = arg.get('attributes',[])

# =================================================================
class MethodInfo(object):
	"""docstring for MethodInfo"""
	def __init__(self, arg):
		self.access_flags = arg.get('access_flags',None) # u2 
		self.name = arg.get('name',None) # u2 
		self.descriptor = arg.get('descriptor',None) # u2 
		self.attributes_count = arg.get('attributes_count',0) # u2 
		self.attributes = arg.get('attributes',[])
		self.code = arg.get('code',None)

# =================================================================
class AttributeInfo(object):
	"""docstring for AttributeInfo"""
	def __init__(self, arg,pool=[]):
		self.__offset = 0
		self.code = {}
		if isinstance(arg,dict):
			self.init(arg)
		else:
			self.__data = arg
			self.__constant_pool = pool
			self.__attrHandler()

	def __cursor(self,step):
		# print '------__data',__data
		result = self.__data[self.__offset:self.__offset+step]
		self.__offset += step
		return result

	def init(self,arg):
		self.attribute_name = arg.get('attribute_name',None) # u2 
		self.attribute_length = arg.get('attribute_length',0) # u4 
		self.info = arg.get('info',{}) # u1 

	# 从常量池中获取值
	def __getConstant(self,num):
		try:
			source = self.__constant_pool[num]
			if source.__contains__('#'):
				temp = source.replace('#','')
				pointers = temp.split(',')
				target = [self.__constant_pool[int(i)-1] for i in pointers]
				return target
			return source
		except Exception, e:
			print '==========================',num,len(self.__constant_pool)

	def __attrHandler(self):
		# u2 self.attribute_name_index;
		self.attribute_name = self.__getConstant(getDecimal(self.__cursor(2)))
		# u4 self.attribute_length;
		self.attribute_length = getDecimal(self.__cursor(4))
		print '\t self.attribute_length:',self.attribute_length
		# u1 info[self.attribute_length];
		# _attrInfo = ''.join([chr(int(b,16)) for b in self.__cursor(self.attribute_length)])
		if self.attribute_name == 'Code':#方法表，Java代码编译成的字节码指令
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
			
			self.code['max_stack']= getDecimal(self.__cursor(2))
			self.code['max_locals']= getDecimal(self.__cursor(2))
			code_length = getDecimal(self.__cursor(4))
			self.code['code_length']= code_length
			codes = [cmd.get(toInt(self.__cursor(1))) for x in xrange(code_length)]
			print codes
			exception_table_length = getDecimal(self.__cursor(2))
			self.code['exception_table_length']= exception_table_length
			if exception_table_length > 0:
				exceptions = []
				for x in xrange(exception_table_length):
					temp = {}
					temp['start_pc'] = getDecimal(self.__cursor(2))
					temp['end_pc'] = getDecimal(self.__cursor(2))
					temp['handler_pc'] = getDecimal(self.__cursor(2))
					temp['catch_type'] = getDecimal(self.__cursor(2))
					exceptions.append(temp)
				self.code['exceptions:']= exceptions
			attributes_count = getDecimal(self.__cursor(2))
			for x in xrange(attributes_count):
				self.__attrHandler()
		elif self.attribute_name == 'ConstantValue':#字段表，field定义的常量池
			# 结构：u2 constantvalue_index , self.attribute_length === 2
			self.ConstantValue = self.__getConstant(getDecimal(self.__cursor(self.attribute_length)))
		# 一个方法的 Code 属性最多只能有一个 StackMapTable 属性,否则将抛出 ClassFormatError 异常
		elif self.attribute_name == 'StackMapTable':#Code属性 ，JDK1.6中新增的属性，供新的类型检验器检查和处理目标方法的局部变量和操作数有所需要的类是否匹配 
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
			number_of_entries = getDecimal(self.__cursor(2))
			self.info['number_of_entries'] = number_of_entries
			'''
			使用时帧的字节偏移量计算方法为:前一帧的字节码偏移量(Bytecode Offset)加上 offset_delta 的值再加 1,如果前一个帧是方法的初始帧
			(Initial Frame),那这时候字节码偏移量就是 offset_delta。
			方法的初始帧是隐式的,它通过方法描述符计算得出
			'''
			entries = []
			self.info['entries'] = entries
			for x in xrange(number_of_entries):
				entry = {}
				frame_type = getDecimal(self.__cursor(1))
				entry['type'] = frame_type
				# same_frame {
				# u1 frame_type = SAME; /* 0-63 */
				# }
				# 当前帧拥有和前一个栈映射帧完全相同的 locals[]数组,并且对应的 stack 项的成员个数为 0。
				# 当前帧的 offset_delta 值就使用 frame_type 项的值来表示
				if 0<=frame_type<64:
					# print 'SAME,offset_delta:%d' % frame_type
					pass
				# same_locals_1_stack_item_frame {
				# u1 frame_type = SAME_LOCALS_1_STACK_ITEM;/* 64-127 */
				# self.__verification_type_info stack[1];
				# }
				# 前帧拥有和前一个栈映射帧完全相同的 locals[]数组,同时对应的 stack[]数组的成员个数为 1。当前帧的 offset_delta 值为 frame_type-64。
				# 并且有一个 self.__verification_type_info 项跟随在此帧类型之后,用于表示那一个 stack 项的成员。
				elif 64<=frame_type<128:
					# print 'SAME_LOCALS_1_STACK_ITEM,offset_delta:%d' % frame_type-64
					entry['type_info'] = self.__verification_type_info()
				# same_locals_1_stack_item_frame_extended {
				# 	u1 frame_type = SAME_LOCALS_1_STACK_ITEM_EXTENDED;/* 247 */
				# 	u2 offset_delta;
				# 	self.__verification_type_info stack[1];
				# }
				# 当前帧拥有和前一个栈映射帧完全相同的 locals[]数组,同时对应的 stack[]数组的成员个数为 1。
				# 当前帧的 offset_delta 的值需要由 offset_delta 项明确指定。有一个 stack[]数组的成员跟随在 offset_delta 项之后。
				elif frame_type == 247:
					entry['offset_delta'] = getDecimal(self.__cursor(2))
					entry['type_info'] = self.__verification_type_info()
					# print 'SAME_LOCALS_1_STACK_ITEM_EXTENDED,offset_delta:%d' % offset_delta
				# chop_frame {
				# u1 frame_type = CHOP; /* 248-250 */
				# u2 offset_delta;
				# }
				# 对应的操作数栈为空,并且拥有和前一个栈映射帧相同的 locals[]数组,不过其中的第 k 个之后的 locals 项是不存在的。
				# k 的值由 251-frame_type 确定
				elif 248<=frame_type<251:
					entry['offset_delta'] = getDecimal(self.__cursor(2))
					entry['k'] = 251-frame_type
					# print 'chop_frame,k:%d,offset_delta:%d' % (k,offset_delta)
				# same_frame_extended {
				# 	u1 frame_type = SAME_FRAME_EXTENDED; /* 251 */
				# 	u2 offset_delta;
				# }
				# 当前帧有拥有和前一个栈映射帧的完全相同的locals[]数组,同时对应的 stack[]数组的成员数量为 0。
				elif frame_type == 251:
					entry['offset_delta'] = getDecimal(self.__cursor(2))
					# print 'same_frame_extended,offset_delta:%d' % offset_delta
				
				# append_frame {
				# 	u1 frame_type = APPEND; /* 252-254 */
				# 	u2 offset_delta;
				# 	self.__verification_type_info locals[frame_type - 251];
				# }
				# 对应操作数栈为空,并且包含和前一个栈映射帧相同的 locals[]数组,不过还额外附加 k 个的 locals 项。k 值为 frame_type-251。
				elif 252<=frame_type<255:
					entry['offset_delta'] = getDecimal(self.__cursor(2))
					entry['k'] = frame_type-251
					entry['type_info'] = self.__verification_type_info()
					# print 'append_frame,k:%d,offset_delta:%d' % (k,offset_delta)
				entries.append(entry)

		elif self.attribute_name == 'Exceptions':#方法表 ，方法抛出的异常
			# u2 number_of_exceptions;
			# u2 exception_index_table[number_of_exceptions];
			number_of_exceptions = getDecimal(self.__cursor(2))
			self.info = {
				'number_of_exceptions': number_of_exceptions,
				'exception_index_table':  [self.__getConstant(getDecimal(self.__cursor(2))) \
					for i in xrange(number_of_exceptions)]
			}

		elif self.attribute_name == 'InnerClass':#类文件 ，内部类列表 
			# u2 number_of_classes;
			# {
			# 	u2 inner_class_info_index;
			# 	u2 outer_class_info_index;
			# 	u2 inner_name_index;
			# 	u2 inner_class_access_flags;
			# } classes[number_of_classes];

			number_of_classes = getDecimal(self.__cursor(2))
			self.info['number_of_classes'] = number_of_classes
			classes = []
			self.info['classes'] = classes
			for i in xrange(number_of_classes):
				inner_class = {
					'inner_class_info': self.__getConstant(getDecimal(self.__cursor(2))),
					'outer_class_info': self.__getConstant(getDecimal(self.__cursor(2))),
					'inner_name': self.__getConstant(getDecimal(self.__cursor(2))),
					'inner_class_access': accessFlags.getAccessFlag('class',getDecimal(self.__cursor(2)))
				}
				classes.append(inner_class)
				
			# print ['inner_class_info:%s,outer_class_info:%s,inner_name:%s,inner_class_access:%s' % (\
			# 	,self.__getConstant(getDecimal(self.__cursor(2))),self.__getConstant(getDecimal(self.__cursor(2))),accessFlags.getAccessFlag('class',getDecimal(self.__cursor(2)))) \
			# 	for i in xrange(number_of_classes)] 
		elif self.attribute_name == 'EnclosingMethod':#类文件 ，仅当一个类为局部类或者匿名类是才能拥有这个属性，这个属性用于标识这个类所在的外围方法 
			# u2 class_index
			# u2 method_index;
			self.info = {
				'class':self.__getConstant(getDecimal(self.__cursor(2))),
				'method':self.__getConstant(getDecimal(self.__cursor(2)))
			}
			# print 'class:%s , method:%s' % (self.__getConstant(getDecimal(self.__cursor(2))),self.__getConstant(getDecimal(self.__cursor(2))))
		elif self.attribute_name == 'Synthetic':#类，方法表，字段表 ，标志方法或字段为编译器自动生成的 
			# ACC_SYNTHETIC ,self.attribute_length === 0
			self.info['Synthetic'] = 1
			print 'ACC_SYNTHETIC'
		elif self.attribute_name == 'Signature':#类，方法表，字段表 ，用于支持泛型情况下的方法签名
			# u2 signature_index;
			self.info['signature'] = self.__getConstant(getDecimal(self.__cursor(2)))
		elif self.attribute_name == 'SourceFile':#类文件 ，记录源文件名称 
			# u2 sourcefile_index;
			self.info['sourcefile'] =  self.__getConstant(getDecimal(self.__cursor(2)))
		elif self.attribute_name == 'SourceDebugExtension':#类文件 ，用于存储额外的调试信息 
			# u1 debug_extension[self.attribute_length];
			self.info['debug_extension'] = ''.join([chr(getDecimal(self.__cursor(1))) for i in xrange(self.attribute_length)])
		elif self.attribute_name == 'LineNumberTable':#Code属性 ，Java源码的行号与字节码指令的对应关系 
			# u2 line_number_table_length;
			# {
			# 	u2 start_pc;
			# 	u2 line_number;
			# } line_number_table[line_number_table_length];
			line_number_table_length = getDecimal(self.__cursor(2))
			self.info['line_number_table_length'] = line_number_table_length
			line_number_table = []
			self.info['line_number_table'] = line_number_table
			for i in xrange(line_number_table_length):
				_table = {
					'start_pc':getDecimal(self.__cursor(2)),
					'line_number':getDecimal(self.__cursor(2))
				}
				line_number_table.append(_table)
			# print ['start_pc:%d,line_number:%d' % (getDecimal(self.__cursor(2)),getDecimal(self.__cursor(2))) \
			# 	for i in xrange(line_number_table_length)] 
		# Code 属性中的每个局部变量最多只能有一个 LocalVariableTable 属性
		elif self.attribute_name == 'LocalVariableTable':#Code属性 ，方法的局部变量描述 
			# u2 local_variable_table_length;
			# {
			# 	u2 start_pc;
			# 	u2 length;
			# 	u2 name_index;
			# 	u2 descriptor_index;
			# 	u2 index;
			# } local_variable_table[local_variable_table_length];
			local_variable_table_length = getDecimal(self.__cursor(2))
			self.info['local_variable_table_length'] = local_variable_table_length
			local_variable_table = []
			self.info['local_variable_table'] = local_variable_table
			for i in xrange(local_variable_table_length):
				_table = {
					'start_pc':getDecimal(self.__cursor(2)),
					'length':getDecimal(self.__cursor(2)),
					'name':self.__getConstant(getDecimal(self.__cursor(2))),
					'descriptor':self.__getConstant(getDecimal(self.__cursor(2))),
					'index':getDecimal(self.__cursor(2))
				}
				local_variable_table.append(_table)
			# print ['start_pc:%s,length:%s,name:%s,descriptor:%s,index:%s' % (getDecimal(self.__cursor(2))\
			# 	,getDecimal(self.__cursor(2)),self.__getConstant(getDecimal(self.__cursor(2))),self.__getConstant(getDecimal(self.__cursor(2))),getDecimal(self.__cursor(2))) \
			# 	for i in xrange(local_variable_table_length)] 
		elif self.attribute_name == 'LocalVariableTypeTable':#类 ，使用特征签名代替描述符，是为了引入泛型语法之后能描述泛型参数化类型而添加 
			# u2 local_variable_type_table_length;
			# {
			# 	u2 start_pc;
			# 	u2 length;
			# 	u2 name_index;
			# 	u2 signature_index;
			# 	u2 index;
			# 	}local_variable_type_table[local_variable_type_table_length
			# }
			local_variable_type_table_length = getDecimal(self.__cursor(2))
			self.info['local_variable_type_table_length'] = local_variable_type_table_length
			local_variable_type_table = []
			self.info['local_variable_type_table'] = local_variable_type_table
			for i in xrange(local_variable_type_table_length):
				_table = {
					'start_pc':getDecimal(self.__cursor(2)),
					'length':getDecimal(self.__cursor(2)),
					'name':self.__getConstant(getDecimal(self.__cursor(2))),
					'descriptor':self.__getConstant(getDecimal(self.__cursor(2))),
					'index':getDecimal(self.__cursor(2))
				}
				local_variable_type_table.append(_table)
			# print ['start_pc:%s,length:%s,name:%s,signature:%s,index:%s' % (getDecimal(self.__cursor(2))\
			# 	,getDecimal(self.__cursor(2)),self.__getConstant(getDecimal(self.__cursor(2))),self.__getConstant(getDecimal(self.__cursor(2))),getDecimal(self.__cursor(2))) \
			# 	for i in xrange(local_variable_type_table_length)] 
		elif self.attribute_name == 'Deprecated':#类，方法，字段表，被声明为deprecated的方法和字段
			# self.attribute_length === 0
			self.info['Deprecated'] = 1
		# #类，方法表，字段表 ，为动态注解提供支持 ,RuntimeInvisibleAnnotations用于指明哪些注解是运行时不可见的 
		elif self.attribute_name in ['RuntimeVisibleAnnotations','RuntimeInvisibleAnnotations']:#类，方法表，字段表 ，为动态注解提供支持 
			# u2 num_annotations;
			# annotation annotations[num_annotations];
			num_annotations = getDecimal(self.__cursor(2))
			self.info['num_annotations'] = num_annotations
			annotations = []
			self.info['annotations'] = annotations
			for i in xrange(num_annotations):
				annotations.append(self.__handlerAnnotation())
			# print [self.__handlerAnnotation() for x in xrange(num_annotations)]
		# 数组中每个成员的值表示一个的参数的所有的运行时可见注解。它们的顺序和方法描述符表示的参数的顺序一致
		elif self.attribute_name in ['RuntimeVisibleParameterAnnotation','RuntimeInvisibleParameterAnnotation']:#方法表 ，作用与RuntimeVisibleAnnotations属性类似，只不过作用对象为方法
			# u1 num_parameters;
			# {
			# 	u2 num_annotations;
			# 	annotation annotations[num_annotations];
			# } parameter_annotations[num_parameters];
			num_parameters = getDecimal(self.__cursor(1))
			self.info['num_parameters'] = num_parameters
			parameter_annotations = []
			self.info['parameter_annotations'] = parameter_annotations
			for x in xrange(num_parameters):
				num_annotations = getDecimal(self.__cursor(2))
				annotations = []
				self.info['annotations'] = annotations
				for i in xrange(num_annotations):
					annotations.append(self.__handlerAnnotation())
				# print [self.__handlerAnnotation() for x in xrange(num_annotations)]
		elif self.attribute_name == 'AnnotationDefault':#方法表，用于记录注解类元素的默认值 
			# element_value default_value;
			self.info = self.__hadlerAnnotation_element()
		elif self.attribute_name == 'BootstrapMethods':#类文件 ，用于保存invokeddynamic指令引用的引导方式限定符  
			# u2 num_bootstrap_methods;
			# {
			# 	u2 bootstrap_method_ref;
			# 	u2 num_bootstrap_arguments;
			# 	u2 bootstrap_arguments[num_bootstrap_arguments];
			# } bootstrap_methods[num_bootstrap_methods];
			num_bootstrap_methods = getDecimal(self.__cursor(2))
			self.info['num_bootstrap_methods'] = num_bootstrap_methods
			bootstrap_methods = []
			self.info['bootstrap_methods'] = bootstrap_methods

			for x in xrange(num_bootstrap_methods):
				'''
				bootstrap_method_ref 项的值必须是一个对常量池的有效索引。常量池在该索引处的值必须是一个 CONSTANT_MethodHandle_info 结构。
				注意:此 CONSTANT_MethodHandle_info 结构的 reference_kind 项应为值 6	(REF_invokeStatic)或 8(REF_newInvokeSpecial)
				(§5.4.3.5),否则在 invokedynamic 指令解析调用点限定符时,引导方法会执行失败。
				'''
				_method = {
					'bootstrap_method' : self.__getConstant(getDecimal(self.__cursor(2))),
					'num_bootstrap_arguments' : getDecimal(self.__cursor(2)),
					'bootstrap_arguments' : [self.__getConstant(getDecimal(self.__cursor(2))) for x in xrange(num_bootstrap_arguments)]
				}
				bootstrap_methods.append(_method)
		else:
			self.info = {
				'error':'ERROR:cannot parse this attribute %s' % self.attribute_name,
				'attribute_info':self.__cursor(self.attribute_length)
			}
			# print 'ERROR:cannot parse this attribute %s' % self.attribute_name ,\
			#  '\t attribute_info:',self.__cursor(self.attribute_length)
			
	# 结构的第一个字节 tag 作为类型标记,之后跟随 0 至多个字节表示由 tag 类型所决定的信息
	def __verification_type_info(self):
		type_info = {}
		tag = getDecimal(self.__cursor(1))
		type_info['tag'] = tag
		# Top_variable_info 类型说明这个局部变量拥有验证类型 top(ᴛ)。
		# Top_variable_info {
		# u1 tag = ITEM_Top; /* 0 */
		# }
		if tag == 0:
			# print 'ITEM_Top'
			pass
		# Integer_variable_info 类型说明这个局部变量包含验证类型 int
		# Integer_variable_info {
		# u1 tag = ITEM_Integer; /* 1 */
		# }
		elif tag == 1:
			# print 'ITEM_Integer'
			pass
		# Float_variable_info 类型说明局部变量包含验证类型 float
		# Float_variable_info {
		# u1 tag = ITEM_Float; /* 2 */
		# }
		elif tag == 2:
			# print 'ITEM_Float'
			pass
		# Long_variable_info 类型说明存储单元包含验证类型 long,如果存储单元是局部变量,
		# 则要求:
		# 1. 不能是最大索引值的局部变量。
		# 2. 按顺序计数的下一个局部变量包含验证类型 ᴛ
		# 如果单元存储是操作数栈成员,则要求:
		# 1. 当前的存储单元不能在栈顶。
		# 2. 靠近栈顶方向的下一个存储单元包含验证类型 ᴛ。
		# Long_variable_info 结构在局部变量表或操作数栈中占用 2 个存储单元。
		# Long_variable_info {
		# u1 tag = ITEM_Long; /* 4 */
		# }
		elif tag == 4:
			# print 'ITEM_Long'
			pass
		# Double_variable_info 类型说明存储单元包含验证类型 double。如果存储单元是局部
		# 变量,则要求:
		#  1.不能是最大索引值的局部变量。
		#  2.按顺序计数的下一个局部变量包含验证类型 ᴛ
		# 如果单元存储是操作数栈成员,则要求:
		# 1.当前的存储单元不能在栈顶。
		# 2.靠近栈顶方向的下一个存储单元包含验证类型 ᴛ。
		# Double_variable_info 结构在局部变量表或操作数栈中占用 2 个存储单元。
		# Double_variable_info {
		# u1 tag = ITEM_Double; /* 3 */
		# }
		elif tag == 3:
			# print 'ITEM_Double'
			pass
		# Null_variable_info 类型说明存储单元包含验证类型 null。
		# Null_variable_info {
		# u1 tag = ITEM_Null; /* 5 */
		# }
		elif tag == 5:
			# print 'ITEM_Null'
			pass
		# UninitializedThis_variable_info 类型说明存储单元包含验证类型
		# uninitializedThis。
		# UninitializedThis_variable_info {
		# u1 tag = ITEM_UninitializedThis; /* 6 */
		# }
		elif tag == 6:
			# print 'ITEM_UninitializedThis'
			pass
		# Object_variable_info 类型说明存储单元包含某个 Class 的实例。由常量池在
		# cpool_index 给出的索引处的 CONSTANT_CLASS_Info(§4.4.1)结构表示。
		# Object_variable_info {
		# u1 tag = ITEM_Object; /* 7 */
		# u2 cpool_index;
		# }
		elif tag == 7:
			cpool = self.__getConstant(getDecimal(self.__cursor(2)))
			type_info['cpool'] = cpool
		# Uninitialized_variable_info 说明存储单元包含验证类型
		# uninitialized(offset)。offset 项给出了一个偏移量,表示在包含此 StackMapTable 属
		# 性的 Code 属性中,new 指令创建的对象所存储的位置。
		# Uninitialized_variable_info {
		# u1 tag = ITEM_Uninitialized /* 8 */
		# u2 offset;
		# }
		elif tag == 8:
			offset = getDecimal(self.__cursor(2))
			type_info['offset'] = offset
			# print 'Uninitialized_variable_info,_offset:',_offset
		return type_info
		
	def __handlerAnnotation(self):
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
		annotation['type_index'] = self.__getConstant(getDecimal(self.__cursor(2)))
		num_element_value_pairs = getDecimal(self.__cursor(2))
		annotation['num_element_value_pairs'] = num_element_value_pairs
		pairs = {}
		for x in xrange(num_element_value_pairs):
			pairs['element_name_index'] = self.__getConstant(getDecimal(self.__cursor(2)))
			pairs['element_value'] = self.__hadlerAnnotation_element()
		return annotation

	def __hadlerAnnotation_element(self):
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
		tag = chr(getDecimal(self.__cursor(1)))
		element['tag'] = tag
		element['const_value'] = self.__getConstant(getDecimal(self.__cursor(2)))
		if 'e' == tag:
			element['type_name'] = self.__getConstant(getDecimal(self.__cursor(2)))
			element['const_name'] = self.__getConstant(getDecimal(self.__cursor(2)))
		elif 'c' == tag:
			element['class_info'] = self.__getConstant(getDecimal(self.__cursor(2)))
		elif '@' == tag:
			element['annotation'] = self.__handlerAnnotation()
		elif '[' == tag:
			num_values = getDecimal(self.__cursor(2))
			child_element = []
			for x in xrange(num_values):
				child_element.append(self.__hadlerAnnotation_element())
			element['array_value'] = child_element
		return element


# =================================================================
if __name__ == '__main__':
	attr = ['0x00','0x0a','0x00','0x00','0x00','0x57','0x00','0x02','0x00','0x03','0x00','0x00','0x00','0x1d','0x04','0x3c','0x05','0x3d','0x1b','0x1c','0xa4','0x00','0x0e','0xb2','0x00','0x02','0x12','0x03','0xb6','0x00','0x04','0xa7','0x00','0x0b','0xb2','0x00','0x02','0x12','0x05','0xb6','0x00','0x04','0xb1','0x00','0x00','0x00','0x02','0x00','0x0b','0x00','0x00','0x00','0x1a','0x00','0x06','0x00','0x00','0x00','0x06','0x00','0x02','0x00','0x07','0x00','0x04','0x00','0x08','0x00','0x09','0x00','0x09','0x00','0x14','0x00','0x0b','0x00','0x1c','0x00','0x0d','0x00','0x0e','0x00','0x00','0x00','0x08','0x00','0x02','0xfd','0x00','0x14','0x01','0x01','0x07']
	c = AttributeInfo(attr)
	print c.__dict__










