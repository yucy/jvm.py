# -*- coding:utf-8 -*-
import sys,math
sys.path.append('..')
# sys.getrefcount(obj) # 引用计数

from lang.myexceptions import *
from lang.mycollections import *
from common.content import cmd

# 数据类型定义常量
# [FLOAT,DOUBLE,BYTE,CHAR,SHORT,INT,LONG,OBJECTREF] = ['float','double','byte','char','short','int','long','objectref']
[BOOLEAN,FLOAT,DOUBLE,BYTE,CHAR,SHORT,INT,LONG,OBJECTREF] = [bool,float,float,int,chr,int,int,long,object]

# §2.11.1 的表 2.3 中列出的分类一
dup_type1 = (BOOLEAN,BYTE,CHAR,SHORT,INT,FLOAT,OBJECTREF)# ,REFERENCE,RETURNADDRESS)
# §2.11.1 的表 2.3 中列出的分类二
dup_type2 = (LONG,DOUBLE)

# 指令的参数数量，默认0,[0xaa,0xab]->n个参数
param_d = {
	0x19:1, 0x18:1, 0x17:1, 0x15:1, 0x16:1, 0x3a:1, 0x39:1, 0x38:1, 0x36:1, 0x37:1, 0x12:1, 0x10:1, 0xbc:1, 0xa9:1,
	0x11:2, 0x13:2, 0x14:2, 0x84:2, 0x99:2, 0x9a:2, 0x9b:2, 0x9c:2, 0x9d:2, 0x9e:2, 0x9f:2, 0xa0:2, 0xa1:2, 0xa2:2, 0xa3:2, 0xa4:2, 0xa5:2, 0xa6:2, 0xa7:2, 0xa8:2, 0xb2:2, 0xb3:2, 0xb4:2, 0xb5:2, 0xb6:2, 0xb7:2, 0xb8:2, 0xbb:2, 0xbd:2, 0xc0:2, 0xc1:2, 0xc7:2, 0xc7:2,
	0xc4:3, 0xc5:3,
	0xb9:4, 0xba:4, 0xc8:4, 0xc9:4,
}
# 1 ['aload', 'dload', 'fload', 'iload', 'lload', 'astore', 'dstore', 'fstore', 'istore', 'lstore', 'ldc', 'bipush', 'newarray', 'ret']
# 2 ['sipush', 'ldc_w', 'ldc2_w', 'iinc', 'ifeq', 'ifne', 'iflt', 'ifge', 'ifgt', 'ifle', 'if_icmpeq', 'if_icmpne', 'if_icmplt', 'if_icmpge', 'if_icmpgt', 'if_icmple', 'if_acmpeq', 'if_acmpne', 'goto', 'jsr', 'getstatic', 'putstatic', 'getfield', 'putfield', 'invokevirtual', 'invokespecial', 'invokestatic', 'new', 'anewarray', 'checkcast', 'instanceof', 'ifnonnull', 'ifnonnull']
# 3 'wide','multianewarray',
# 4 ['invokeinterface', 'invokedynamic', 'goto_w', 'jsr_w']
# 5 0xc4 wide->若后面第一个参数是iinc指令，则总参数数量为5
# n 0xaa,0xab -> tableswitch,lookupswitch 指令后面第2-3个参数来确认参数数量

# atype 为要创建数组的元素类型,它将为以下值之一
atypes = {
	4:BOOLEAN,
	5:CHAR,
	6:FLOAT,
	7:DOUBLE,
	8:BYTE,
	9:SHORT,
	10:INT,
	11:LONG,
}

# 根据codes数组来执行方法
class ExecMethod(object):
	def __init__(self,_codes, _locals,_cpinfo):
		self.locals = _locals
		self.cpinfo = _cpinfo
		self.codes = _codes
		self.o = Opcode(Stack(3),_locals,_cpinfo)
		# codes 游标位置
		self.__offset = 0

	def __xswitch(self,offset,code):
		temp_code = 0x00
		print '__xswitch',offset,self.codes[offset]
		# pad_num = pad + switch_param_1
		pad_num,params_num = 0,0
		while temp_code is 0x00:
			temp_code = self.codes[offset]
			# print '===============temp_code,offset',temp_code,offset
			offset += 1
			pad_num+= 1
		print self.codes[offset],self.codes[offset+1],self.codes[offset+2],self.codes[offset+3]
		switch_param_2 = (self.codes[offset]<< 24)|(self.codes[offset+1] << 16)|(self.codes[offset+2] << 8)| self.codes[offset+3]
		# tableswitch, 指令后面第2-3个参数来确认参数数量
		if code is 0xaa:
			low = switch_param_2
			high = (self.codes[offset+4]<< 24)|(self.codes[offset+5] << 16)|(self.codes[offset+6] << 8)| self.codes[offset+7]
			params_num = pad_num+4+4+(high-low+1)*4
			print '===============low,high,params_num',low,high,params_num
		# lookupswitch 指令后面第2个参数来确认参数数量
		elif code is 0xab:
			num = switch_param_2
			params_num = pad_num+4+8*num
			print '===============num,params_num',num,params_num
		return params_num
	# 方法调用
	def execute(self):
		# TODO 方法调用的时候,一个新的栈帧将在 Java 虚拟机栈中被创建出来
		# 是否有返回值
		has_return = False
		# 返回值
		return_value = None
		# 解析并分割code里方法指令集
		_proxy = getattr(self.o,'_proxy')
		offset ,size= 0,len(self.codes)
		print 'offset ,size',offset ,size
		while offset < size:
			temp_code = self.codes[offset]
			offset += 1
			num_params = param_d.get(temp_code,0)
			# 0xc4 wide->若后面第一个参数是 iinc 指令，则总参数数量为5
			if temp_code is 0xc4: # wide
				next = self.codes[offset+1]
				if next is 0x84: # iinc 指令
					num_params = 5
			# tableswitch, lookupswitch 指令后面第2-3个参数来确认参数数量
			elif temp_code in [0xaa,0xab]:
				num_params = self.__xswitch(offset,temp_code)
			print cmd.get(temp_code),'num_params',num_params
			# 指令方法
			_instruction = _proxy(temp_code)
			
			# if num_params is 0:
			# 	_instruction()
			# elif num_params is 1:
			# 	_instruction(self.codes[offset])
			# elif num_params is 2:
			# 	_instruction(self.codes[offset],self.codes[offset+1])
			# elif num_params is 3:
			# 	_instruction(self.codes[offset],self.codes[offset+1],self.codes[offset+2])
			# elif num_params is 4:
			# 	_instruction(self.codes[offset],self.codes[offset+1],self.codes[offset+2],self.codes[offset+3])
			# elif num_params is 5:
			# 	_instruction(self.codes[offset],self.codes[offset+1],self.codes[offset+2],self.codes[offset+3],self.codes[offset+4])
			# elif num_params > 5:
			# 	_instruction(self.codes[offset,offset+num_params])
			offset += num_params
		# 
		# return has_return,return_value
		
# 指令集定义
class Opcode(object):
	"""docstring for Opcode"""
	# stack：操作数栈，local：局部变量表，cpinfo：常量池
	def __init__(self,_stack,_local,_cpinfo):
		self.stack = _stack
		self.local = _local
		self.cpinfo = _cpinfo
		self.__cmd = cmd

	# 根据code（hex数字）返回方法引用
	def _proxy(self,_code):
		return getattr(self,cmd.get(_code))

	def __pop(self):
		return self.stack.pop()

	def __push(self,value):
		self.stack.push(value)

	# 类型检查
	def __type_check(self,_type,*values):
		for value in values:
			if isinstance(value,list):
				for temp in value:
					self.__type_check(_type,temp)
			else:
				if value is not None and not isinstance(value,_type):
					raise ClassCastException(type(value),_type)

	# 判空
	def isNull(self,obj,msg='Null'):
		if obj is None:
			raise NullPointException(msg)

	# 废弃此方法的原因是参数不好设定进去，毕竟不是所有的方法都支持*args类型的元组参数,use ExecMethod.execute()
	# def do(self,code,*args):
	# 	func = getattr(self,code)
	# 	# execute operate code
	# 	func()
	# =============================================================
	# 结束方法,并返回一个 x 类型数据
	# TODO 后续需要考虑synchronized方法的IllegalMonitorStateException异常
	def xreturn(self,_type):
		# ...,value →
		# [empty] # 个人理解：方法操作结束的时候，操作数栈里最后一个元素就是objectref，它出栈以后，stack就empty了。
		value = self.__pop()
		# value 必须为 _type 类型
		self.__type_check(_type,value)
		return value

	# 从数组中加载一个 x 类型数据到操作数栈
	def xaload(self,_type):
		# ...,arrayref,index →
		# ...,value
		index = self.__pop()
		# index 必须为 int 类型
		self.__type_check(INT,index)
		arrayref = self.__pop()
		# judge this obj is null
		self.isNull(arrayref)
		value = arrayref[index]
		# value 必须为 _type 类型
		self.__type_check(_type,value)
		self.__push(value)

	# 从操作数栈读取一个 x 类型数据存入到数组中
	def xastore(self,_type):
		# ...,arrayref,index,value →
		# ...,
		value = self.__pop()
		# value 必须为 _type 类型
		self.__type_check(_type,value)
		# index 必须为 int 类型
		index = self.__pop()
		self.__type_check(INT,index)
		arrayref = self.__pop()
		# judge this obj is null
		self.isNull(arrayref)
		arrayref[index] = value

	# 从局部变量表加载一个x 类型值到操作数栈中
	def xload(self,index,_type):
		# ... →
		# ...,value #说明: value 是x 类型
		value = self.local[index]
		# value 是x 类型
		self.__type_check(_type,value)
		self.__push(value)

	# 将一个 x 类型数据保存到局部变量表中。
	def xstore(self,index,_type):
		# ...,value → #说明: value 是x 类型
		# ...
		value = self.__pop()
		# value 是x 类型
		self.__type_check(_type,value)
		self.local[index] = value

	# 数值计算---------------------------

	# x 类型数据相加
	def xadd(self,_type):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1,value2 是x 类型
		self.__type_check(_type,value2,value1)
		result = 0
		# value1 = value1 if value1 is not None else 0
		# value2 = value2 if value2 is not None else 0
		if math.isnan(value1) or math.isnan(value2):
			result = float(nan)
		else:
			result = value1+value2
		self.__push(result)

	# x 类型数据相减
	def xsub(self,_type):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1,value2 是x 类型
		self.__type_check(_type,value2,value1)
		result = 0
		# value1 = value1 if value1 is not None else 0
		# value2 = value2 if value2 is not None else 0
		if math.isnan(value1) or math.isnan(value2):
			result = float(nan)
		else:
			result = value1+value2
		self.__push(result)

	#  x 类型数据除法
	def xdiv(self,_type):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1,value2 是x 类型
		self.__type_check(_type,value2,value1)
		result = 0
		# value1 = value1 if value1 is not None else 0
		# value2 = value2 if value2 is not None else 0
		if math.isnan(value1) or math.isnan(value2) or value2 == 0:
			result = float(nan)
		else:
			result = value1/value2
		self.__push(result)

	# x 类型数据乘法
	def xmul(self,_type):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1,value2 是x 类型
		self.__type_check(_type,value2,value1)
		result = 0
		# value1 = value1 if value1 is not None else 0
		# value2 = value2 if value2 is not None else 0
		if math.isnan(value1) or math.isnan(value2):
			result = float(nan)
		else:
			result = value1*value2
		self.__push(result)

	# x 类型数据取负运算
	def xneg(self,_type):
		# ...,value →
		# ...,result
		value = self.__pop()
		# value 是x 类型
		self.__type_check(_type,value)
		if math.isnan(value):
			result = float(nan)
		else:
			result = 0-value
		self.__push(result)

	# x 类型数据求余
	def xrem(self,_type):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1,value2 是x 类型
		self.__type_check(_type,value2,value1)
		result = 0
		# value1 = value1 if value1 is not None else 0
		# value2 = value2 if value2 is not None else 0
		if math.isnan(value1) or math.isnan(value2):
			result = float(nan)
		# 如果被除数为零,而除数是有限值,那运算结果等于被除数
		elif value2 == 0:
			result == 0
		else:
			result = value1%value2
		self.__push(result)
	# -----------------------------------------

	# 'dcmpl',#比较栈顶两 x 型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将-1压入栈顶。
	# 'dcmpg',#比较栈顶两 x 型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将1压入栈顶。
	def xcmp(self,_type,_arg):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1,value2 是x 类型
		self.__type_check(_type,value2,value1)
		result = 0
		# value1 = value1 if value1 is not None else 0
		# value2 = value2 if value2 is not None else 0
		if math.isnan(value1) or math.isnan(value2):
			result = 1 if _arg is 'g' else -1
		elif value1 == value2:
			result = 0
		else:
			result = 1 if value1>value2 else -1
		self.__push(result)

	# -----------------------------------------
	# 类型转换
	# 将类型为x的数值转化成类型为y的数值
	def x2y(self,_x_type,_y_type):
		# ...,value →
		# ...,result
		value = self.__pop()
		self.__type_check(_x_type,value)
		self.__push(_y_type(value))

	# -----------------------------------------
	# 位运算
	# int 或者 long 类型数据进行按位与运算
	def xand(self,_type):
		# „,value1,value2 →
		# „,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1、value2 必须为 x 类型数据
		self.__type_check(_type,value1,value2)
		result = value1 & value2
		self.__push(result)

	# int 或者 long 类型数值的布尔或运算
	def xor(self,_type):
		# „,value1,value2 →
		# „,result
		# 指令执行时,它们从操作数栈中出栈
		value2 = self.__pop()
		value1 = self.__pop()
		# value1、value2 必须为 x 类型数据
		self.__type_check(_type,value1,value2)
		# 对这 2 个数进行按位或(Bitwise Inclusive OR)运算
		result = value2 | value1
		self.__push(result)

	# int 或者 long 数值左移运算
	def xshl(self,_type):
		# „,value1,value2 →
		# „,result
		# 指令执行时,它们从操作数栈中出栈
		value2 = self.__pop()
		value1 = self.__pop()
		# value1、value2 必须为 x 类型数据
		self.__type_check(_type,value1,value2)
		# 将 value1 左移 s 位,result = value1*2^s
		temp_bit = '11111' # int 类型数据,s 是 value2 低 5 位所表示的值
		if _type is LONG:
			# long 类型数据,s 是 value2 低 6 位所表示的值
			temp_bit = '111111'
		result = value1 << (value2 & int(temp_bit,2))
		self.__push(result)

	# int 或者 long 数值右移运算
	def xshr(self,_type):
		# „,value1,value2 →
		# „,result
		# 指令执行时,它们从操作数栈中出栈
		value2 = self.__pop()
		value1 = self.__pop()
		# value1、value2 必须为 x 类型数据
		self.__type_check(_type,value1,value2)
		# 将 value1 左移 s 位,result = value1÷2^s
		temp_bit = '11111' # int 类型数据,s 是 value2 低 5 位所表示的值
		if _type is LONG:
			# long 类型数据,s 是 value2 低 6 位所表示的值
			temp_bit = '111111'
		result = value1 >> (value2 & int(temp_bit,2))
		self.__push(result)

	# int 或者 long 数值逻辑右移运算
	def xushr(self,_type):
		# „,value1,value2 →
		# „,result
		# 指令执行时,它们从操作数栈中出栈
		self.xshr(_type)

	# int 或者 long 数值异或运算
	def xxor(self,_type):
		# „,value1,value2 →
		# „,result
		# 指令执行时,它们从操作数栈中出栈
		value2 = self.__pop()
		value1 = self.__pop()
		# value1、value2 必须为 x 类型数据
		self.__type_check(_type,value1,value2)
		result = value1 ^ value2
		self.__push(result)

	# =============================================================
	# 从数组中加载一个 reference 类型数据到操作数栈
	def aaload(self):
		self.xaload('array')
		
	# 从操作数栈读取一个 reference 类型数据存入到数组中
	def aastore(self):
		self.xastore('array')
		
	# 将一个 null 值压入到操作数栈中
	def aconst_null(self):
		# ...,→
		# ...,null
		self.__push(None)

	# 从局部变量表加载一个 reference 类型值到操作数栈中
	# TODO index 作为索引定位的局部变量必须为 reference 类型,称为objectref,不支持returnAddress类型
	def aload(self,index):
		# ...,→
		# ...,objectref
		self.xload(index,OBJECTREF)

	def aload_0(self):
		self.aload(0)

	def aload_1(self):
		self.aload(1)

	def aload_2(self):
		self.aload(2)

	def aload_3(self):
		self.aload(3)

	# 创建一个组件类型为 reference 类型的数组
	def anewarray(self,indexbyte1,indexbyte2):
		# ...,count →
		# ...,arrayref
		# 下面的位移和按位或操作，是为了组合出一个双字节数字，参考class文件定义中的【xxx_index】
		cpinfo_index = (indexbyte1 << 8)|indexbyte2
		count = self.__pop()
		# TODO _type 转换为可用类型，从常量表取出来的可能是一个类型描述符
		_type = self.cpinfo[cpinfo_index]
		arrayref = Array(count,_type)
		self.__push(arrayref)

	# 结束方法,并返回一个 reference 类型数据
	def areturn(self):
		# ...,objectref →
		# [empty] 
		return self.xreturn(OBJECTREF)

	# 取数组长度
	def arraylength(self):
		# ...,arrayref →
		# ...,length
		arrayref = self.__pop()
		# judge this obj is null
		self.isNull(arrayref)
		length = len(arrayref)
		self.__push(length)

	# 将一个 reference或returnAddress 类型数据保存到局部变量表中。
	# 注意：aload不能处理【returnAddress】类型，这种不对称的设计是有意为之。
	def astore(self,index):
		# ...,objectref →
		# ...
		self.xstore(self,index,OBJECTREF)

	def astore_0(self):
		self.astore(0)

	def astore_1(self):
		self.astore(1)

	def astore_2(self):
		self.astore(2)

	def astore_3(self):
		self.astore(3)

	# 抛出一个异常实例(exception 或者 error)
	# TODO 后续需要运行时，程序处理预定义异常抛出的问题
	def athrow(self):
		# ...,objectref →
		# objectref
		objectref = self.__pop()
		self.stack.clear()
		self.__push(objectref)

	# 从数组中读取 byte 或者 boolean 类型的数据
	def baload(self):
		self.xaload(BYTE)

	# 从操作数栈读取一个 byte 或 boolean 类型数据存入到数组中
	def bastore(self):
		self.xastore(BYTE)

	# 将一个 byte 类型数据入栈
	def bipush(self,value):
		# ..., →
		# ...,value
		self.__push(value)

	# 从操作数栈读取一个 char 类型数据存入到数组中
	def caload(self):
		self.xaload(CHAR)

	# castore
	def castore(self):
		self.xastore(CHAR)

	# 检查对象是否符合给定的类型
	def checkcast(self,indexbyte1,indexbyte2):
		# ...,objectref →
		# ...,objectref
		# 下面的位移和按位或操作，是为了组合出一个双字节数字，参考class文件定义中的【xxx_index】
		cpinfo_index = (indexbyte1 << 8)|indexbyte2
		objectref = self.__pop()
		# TODO _type 转换为可用类型，从常量表取出来的可能是一个类型描述符
		_type = self.cpinfo[cpinfo_index]
		# 如果 objectref 可以转换为_type指定的这个类、接口或者数组类型,那操作数栈就保持不变,否则 checkcast 指令将抛出一个 ClassCastException 异常
		objectref_type = type(objectref)
		if objectref is None or isinstance(objectref,_type):
			self.__push(arrayref)
		else:
			raise ClassCastException(type(objectref),_type)

	# 将 double 类型数据转换为 float 类型
	def d2f(self):
		# ...,value →
		# ...,result
		# TODO python里没有单精度的概念，java里的float和double都对应python里的float
		self.x2y(DOUBLE,FLOAT)

	# 将 double 类型数据转换为 int 类型
	def d2i(self):
		# ...,value →
		# ...,result
		# python里超过int范围的整数就自动当长整数(long)处理
		self.x2y(DOUBLE,INT)

	# 将 double 类型数据转换为 long 类型
	def d2l(self):
		# ...,value →
		# ...,result
		self.x2y(DOUBLE,LONG)

	# double 类型数据相加
	def dadd(self):
		# ...,value1,value2 →
		# ...,result
		self.xadd(DOUBLE)

	# 从数组中加载一个 double 类型数据到操作数栈
	def daload(self):
		self.xaload(DOUBLE)

	# 从操作数栈读取一个 double 类型数据存入到数组中
	def dastore(self):
		self.xastore(DOUBLE)

	def dcmpl(self):
		self.xcmp(DOUBLE,'l')

	def dcmpg(self):
		self.xcmp(DOUBLE,'g')

	# 将 double 类型数据 0 压入到操作数栈中
	def dconst_0(self):
		# ... →
		# ...,<d>
		self.__push(DOUBLE(0.0))

	# 将 double 类型数据 1 压入到操作数栈中
	def dconst_1(self):
		# ... →
		# ...,<d>
		self.__push(DOUBLE(1.0))

	# double 类型数据除法
	def ddiv(self):
		# ...,value1,value2 →
		# ...,result
		self.xdiv(DOUBLE)

	# 从局部变量表加载一个 double 类型值到操作数栈中
	def dload(self,index):
		# ..., →
		# ...,value
		# TODO index 作为索引定位的局部变量必须为 double 类型(占用 index和 index+1 两个位置)
		# ,记为 value。指令执行后,value 将会压入到操作数栈栈顶
		# 注意:dload 操作码可以与 wide 指令联合一起实现使用 2 个字节长度的无符号byte 型数值作为索引来访问局部变量表。
		self.xload(index,DOUBLE)

	def dload_0(self):
		self.dload(0)

	def dload_1(self):
		self.dload(1)

	def dload_2(self):
		self.dload(2)

	def dload_3(self):
		self.dload(3)

	# double 类型数据乘法
	def dmul(self):
		# „,value1,value2 →
		# „,result
		self.xmul(DOUBLE)
	
	# double 类型数据取负运算
	def dneg(self):
		# „,value →
		# „,result
		self.xneg(DOUBLE)
	
	# double 类型数据求余
	def drem(self):
		# „,value1,value2 →
		# „,result
		self.xrem(DOUBLE)

	# 结束方法,并返回一个 double 类型数据
	def dreturn(self):
		# „,value →
		# [empty]
		return self.xreturn(DOUBLE)

	# 将一个 double 类型数据保存到局部变量表中
	def dstore(self,index):
		# „,value →
		# „
		# TODO 保存到 index 和 index+1 所指向的局部变量表位置中
		# TODO 后面可能将局部变量表设计成操作数栈一样的存储结构，即：一个节点存放一个值，不管其占几个字节
		# TODO dstore 指令可以与 wide 指令联合使用,以实现使用 2 字节宽度的无符号整数作为索引来访问局部变量表
		self.xstore(index,DOUBLE)


	def dstore_0(self):
		self.dstore(0)

	def dstore_1(self):
		self.dstore(1)

	def dstore_2(self):
		self.dstore(2)

	def dstore_3(self):
		self.dstore(3)

	# double 类型数据相减
	def dsub(self):
		# „,value1,value2 →
		# „,result
		self.xsub(DOUBLE)

	# 复制操作数栈栈顶的值,并插入到栈顶
	def dup(self):
		# „,value →
		# „,value,value
		value = self.__pop()
		self.__push(value)

	# 复制操作数栈栈顶的值,并插入到栈顶以下 2 个值之后
	def dup_x1(self):
		# „,value2,value1 →
		# „,value1,value2,value1
		value1 = self.__pop()
		value2 = self.__pop()
		self.__push(value1)
		self.__push(value2)
		self.__push(value1)

	# 复制操作数栈栈顶的值,并插入到栈顶以下 2 个或 3 个值之后
	def dup_x2(self):
		# 结构 1: 当 value1、value2 和 value3 都是 dup_type1 中列出的分类一中的数据类型时
		# „,value3,value2,value1 →
		# „,value1,value3,value2,value1
		# 
		# 结构 2:当 value1 是 dup_type1 中的数据类型,而 value2是 dup_type2 的数据类型时
		# „,value2,value1 →
		# „,value1,value2,value1

		# TODO long和double当作了特殊类型，如果后面要该局部变量表，这里也是需要考虑的
		value1 = self.__pop()
		value2 = self.__pop()
		if isinstance(value2,dup_type2):
			# 结构 2
			self.__push(value1)
			self.__push(value2)
			self.__push(value1)
		else:
			# 结构 1
			value3 = self.__pop()
			self.__push(value1)
			self.__push(value3)
			self.__push(value2)
			self.__push(value1)

	# 复制操作数栈栈顶 1 个或 2 个值,并插入到栈顶
	def dup2(self):
		# 结构 1:
		# „,value2,value1 →
		# „,value2,value1,value2,value1
		# 当 value1 和 value2 都是§2.11.1 的表 2.3 中列出的分类一中的数据类型时满足结构 1。

		# 结构 2:
		# „,value →
		# „,value,value
		# 当 value 是§2.11.1 的表 2.3 中列出的分类二中的数据类型时满足结构 2。
		value1 = self.__pop()
		if isinstance(value1,dup_type2):
			# 结构 2
			self.__push(value1)
			self.__push(value1)
		else:
			# 结构 1
			value2 = self.__pop()
			self.__push(value2)
			self.__push(value1)
			self.__push(value2)
			self.__push(value1)

	# 复制操作数栈栈顶 1 个或 2 个值,并插入到栈顶以下 2 个或 3 个值之后
	def dup2_x1(self):
		# 结构 1:
		# „,value3,value2,value1 →
		# „,value2,value1,value3,value2,value1
		# 当 value1、value2 和 value3 都是§2.11.1 的表 2.3 中列出的分类一中的数据类型时满足结构 1。

		# 结构 2:
		# „,value2,value1 →
		# „,value1,value2,value1
		# 当 value1 是§2.11.1 的表 2.3 中列出的分类二中的数据类型,而 value2是分类一的数据类型时满足结构 2。
		value1 = self.__pop()
		value2 = self.__pop()
		if isinstance(value2,dup_type2):
			# 结构 2
			self.__push(value1)
			self.__push(value2)
			self.__push(value1)
		else:
			# 结构 1
			value3 = self.__pop()
			self.__push(value2)
			self.__push(value1)
			self.__push(value3)
			self.__push(value2)
			self.__push(value1)

	# 复制操作数栈栈顶 1 个或 2 个值,并插入到栈顶以下 2 个、3 个或者 3 个值之后
	def dup2_x2(self):
		# 结构 1:
		# „,value4,value3,value2,value1 →
		# „,value2,value1,value4,value3,value2,value1
		# 当 value1、value2 、value3 和 value4 全部都是§2.11.1 的表 2.3 中列出的分类一中的数据类型时满足结构 1。

		# 结构 2:
		# „,value3,value2,value1 →
		# „,value1,value3,value2,value1
		# 当 value1 是§2.11.1 的表 2.3 中列出的分类二中的数据类型,而 value2和 value3 是分类一的数据类型时满足结构 2。

		# 结构 3:
		# „,value3,value2,value1 →
		# „,value2,value1,value3,value2,value1
		# 当 value1 和 value2 是§2.11.1 的表 2.3 中列出的分类一中的数据类型,而 value3 是分类二的数据类型时满足结构 3。

		# 结构 4:
		# „,value2,value1 →
		# „,value1,value2,value1
		# 当 value1 和 value2 是§2.11.1 的表 2.3 中列出的分类二中的数据类型时满足结构 4。
		value1 = self.__pop()
		value2 = self.__pop()
		if isinstance(value1,dup_type2) and isinstance(value2,dup_type2):
			# 结构 4
			self.__push(value1)
			self.__push(value2)
			self.__push(value1)
			return

		value3 = self.__pop()
		if isinstance(value1,dup_type2):
			# 结构 2
			self.__push(value1)
			self.__push(value3)
			self.__push(value2)
			self.__push(value1)
		elif isinstance(value1,dup_type3):
			# 结构 3
			self.__push(value2)
			self.__push(value1)
			self.__push(value3)
			self.__push(value2)
			self.__push(value1)
		else:
			# 结构 1
			value4 = self.__pop()
			self.__push(value2)
			self.__push(value1)
			self.__push(value4)
			self.__push(value3)
			self.__push(value2)
			self.__push(value1)

	# 将 float 类型数据转换为 double 类型
	def f2d(self):
		# „,value →
		# „,result
		# TODO T_T,python has no type [double].
		self.x2y(FLOAT,DOUBLE)

	# 将 float 类型数据转换为 int 类型
	def f2i(self):
		# „,value →
		# „,result
		value = self.__pop()
		result = 0
		# 如果 value’是 NaN 值,那 result 的转换结果为 int 类型的零值
		if math.isnan(value):
			result = 0
		else:
			result = int(value)
		self.__push(result)

	# 将 float 类型数据转换为 long 类型
	def f2l(self):
		# „,value →
		# „,result
		value = self.__pop()
		result = 0
		# 如果 value’是 NaN 值,那 result 的转换结果为 long 类型的零值
		if math.isnan(value):
			result = 0L
		else:
			result = long(value)
		self.__push(result)

	# float 类型数据相加
	def fadd(self):
		# „,value1,value2 →
		# „,result
		self.xadd(FLOAT)

	# 从数组中加载一个 float 类型数据到操作数栈
	def faload(self):
		# „,arrayref,index →
		# „,value
		self.xaload(FLOAT)

	# 从操作数栈读取一个 float 类型数据存入到数组中
	def fastore(self):
		# „,arrayref,index,value →
		# „
		self.xastore(FLOAT)

	def fcmpl(self):
		# „,value1,value2 →
		# „,result
		self.xcmp(FLOAT,'l')

	def fcmpg(self):
		# „,value1,value2 →
		# „,result
		self.xcmp(FLOAT,'g')

	# 将 float 类型数据压入到操作数栈中
	def fconst_0(self):
		# „ →
		# „,<f>
		self.__push(FLOAT(0))

	def fconst_1(self):
		# „ →
		# „,<f>
		self.__push(FLOAT(1))

	def fconst_2(self):
		# „ →
		# „,<f>
		self.__push(FLOAT(2))

	# float 类型数据除法
	def fdiv(self):
		# „,value1,value2 →
		# „,result
		self.xdiv(FLOAT)

	# 从局部变量表加载一个 float 类型值到操作数栈中
	def fload(self,index):
		# „ →
		# „,value
		self.xload(index,FLOAT)

	def fload_0(self):
		self.fload(0)

	def fload_1(self):
		self.fload(1)

	def fload_2(self):
		self.fload(2)

	def fload_3(self):
		self.fload(3)

	# float 类型数据乘法
	def fmul(self):
		# „,value1,value2 →
		# „,result
		self.xmul(FLOAT)

	# float 类型数据取负运算
	def fneg(self):
		# „,value →
		# „,result
		self.xneg(FLOAT)

	# float 类型数据求余
	def frem(self):
		# „,value1,value2 →
		# „,result
		self.xrem(FLOAT)

	# 结束方法,并返回一个 float 类型数据
	def freturn(self):
		# „,value →
		# [empty]
		return xreturn(FLOAT)

	# 将一个 float 类型数据保存到局部变量表中
	def fstore(self,index):
		# „,value →
		# „
		self.xstore(index,FLOAT)

	def fstore_0(self):
		self.fstore(0)

	def fstore_1(self):
		self.fstore(1)

	def fstore_2(self):
		self.fstore(2)

	def fstore_3(self):
		self.fstore(3)

	# float 类型数据相减
	def fsub(self):
		# „,value1,value2 →
		# „,result
		self.xsub(FLOAT)

	# 获取对象的字段值
	def getfield(self,indexbyte1,indexbyte2):
		# „,objectref →
		# „,value
		cpinfo_index = (indexbyte1 << 8)|indexbyte2
		# 对象实例的引用
		objectref = self.__pop()
		# 判空
		self.isNull(objectref)
		# TODO _field 转换为可用类型，从常量表取出来的可能是一个类型描述符
		_field = self.cpinfo[cpinfo_index]
		# 获取对象的字段值
		value = getattr(objectref,_field)
		self.__push(value)

	# 获取对象的静态字段值
	def getstatic(self,indexbyte1,indexbyte2):
		# „, →
		# „,value
		cpinfo_index = (indexbyte1 << 8)|indexbyte2
		# TODO 在字段被成功解析之后，如果字段所在的类或者接口没有被初始化过（§5.5），那指令执行时将会触发其初始化过程
		# TODO 如何获取字段的值，1.需要正常初始化；2.需要从常量池中取出其正确的值
		value = self.cpinfo[cpinfo_index] # XXX 这里是错误的引用，后续做到了上面两点，再修正
		# TODO 如果已解析的字段是一个非静态（not static）字段，getstatic指令将会抛出一个IncompatibleClassChangeError异常
		self.__push(value)

	# 分支跳转
	def goto(self,branchbyte1,branchbyte2):
		# 操作数栈没有改变
		# 用于构建一个16位有符号的分支偏移量，此偏移量为code[]的下标
		code_index = (branchbyte1 << 8)|branchbyte2
		# 指令执行后，程序将会转到这个goto指令之后的，由上述偏移量确定的目标地址上继续执行
		return code_index

	# 分支跳转（宽范围）
	# 尽管goto_w指令拥有4字节宽度的分支偏移量，但是还受到方法最大字节码长度为65535字节（§4.11）的限制，这个限制值可能会在未来的Java虚拟机版本中增大
	def goto_w(self,branchbyte1,branchbyte2,branchbyte3,branchbyte4):
		# 操作数栈没有改变
		# 用于构建一个16位有符号的分支偏移量，此偏移量为code[]的下标
		code_index = (branchbyte1 << 24) | (branchbyte2 << 16) | (branchbyte3 << 8) | branchbyte4
		# 指令执行后，程序将会转到这个goto指令之后的，由上述偏移量确定的目标地址上继续执行
		return code_index

	# 将int类型数据转换为byte类型
	def i2b(self):
		# „，value →
		# „，result
		# TODO 后续可能会自定义byte，short,char和double类型，来弥补python版jvm的缺憾
		self.x2y(INT,BYTE)

	# 将int类型数据转换为char类型
	def i2c():
		# „，value →
		# „，result
		# 指令执行时，它将从操作数栈中出栈，转换成byte类型数据，然后零位扩展（Zero-Extended）回一个int的结果压入到操作数栈之中。
		# TODO 这里其实是转成了string类型
		self.x2y(INT,CHAR)

	# 将int类型数据转换为double类型
	def i2d(self):
		# „，value →
		# „，result
		self.x2y(INT,DOUBLE)

	# 将int类型数据转换为double类型
	def i2f(self):
		# „，value →
		# „，result
		self.x2y(INT,FLOAT)
	
	# 将int类型数据转换为 long 类型
	def i2l(self):
		# „，value →
		# „，result
		self.x2y(INT,LONG)

	# 将int类型数据转换为short类型
	def i2s(self):
		# „，value →
		# „，result
		self.x2y(INT,SHORT)

	# int 类型数据相加
	# 运算的结果使用低位在高地址（Low-Order Bites）的顺序、按照二进制补码形式存储在32位空间中
	def iadd(self):
		# „,value1,value2 →
		# „,result
		self.xadd(INT)

	# 从数组中加载一个 int 类型数据到操作数栈
	def iaload(self):
		# „,arrayref,index →
		# „,value
		self.xaload(INT)

	# 对int类型数据进行按位与运算
	def iand(self):
		# „,value1,value2 →
		# „,result
		self.xand(INT)

	# 从操作数栈读取一个 int 类型数据存入到数组中
	def iastore(self):
		# „,arrayref,index,value →
		# „
		self.xastore(INT)

	# def fcmpl(self):
	# 	# „,value1,value2 →
	# 	# „,result
	# 	self.xcmp(INT,'l')

	# def fcmpg(self):
	# 	# „,value1,value2 →
	# 	# „,result
	# 	self.xcmp(INT,'g')

	# 将int类型数据 -1 压入到操作数栈中
	def iconst_m1(self):
		# „ →
		# „,<i>
		self.__push(-1)

	# 将int类型数据 0 压入到操作数栈中
	def iconst_0(self):
		# „ →
		# „,<i>
		self.__push(0)
	# 将int类型数据 1 压入到操作数栈中
	def iconst_1(self):
		# „ →
		# „,<i>
		self.__push(1)
	# 将int类型数据 2 压入到操作数栈中
	def iconst_2(self):
		# „ →
		# „,<i>
		self.__push(2)
	# 将int类型数据 3 压入到操作数栈中
	def iconst_3(self):
		# „ →
		# „,<i>
		self.__push(3)
	# 将int类型数据 4 压入到操作数栈中
	def iconst_4(self):
		# „ →
		# „,<i>
		self.__push(4)
	# 将int类型数据 5 压入到操作数栈中
	def iconst_5(self):
		# „ →
		# „,<i>
		self.__push(5)

	# 将 float 类型数据压入到操作数栈中
	def fconst_0(self):
		# „ →
		# „,<i>
		self.__push(0)

	def fconst_1(self):
		# „ →
		# „,<i>
		self.__push(1)

	def fconst_2(self):
		# „ →
		# „,<i>
		self.__push(2)

	def fconst_3(self):
		# „ →
		# „,<i>
		self.__push(3)

	def fconst_4(self):
		# „ →
		# „,<i>
		self.__push(4)

	def fconst_5(self):
		# „ →
		# „,<i>
		self.__push(5)

	# int 类型数据除法
	def idiv(self):
		# „,value1,value2 →
		# „,result
		self.xdiv(INT)

	# 数据的条件分支判断,【x】:a,i 【y】:ne,eq,lt,gt,le,ge
	def if_xcmpy(self,branchbyte1,branchbyte2,_arg,_type):
		# „，value1，value2 →
		# „
		value2 = self.__pop()
		value1 = self.__pop()
		result = -1
		# 下面三组的后半部分为异异或，相同为 True ，不同为 False
		# lt 当且仅当 value1<value2 比较的结果为真。
		# gt 当且仅当 value1>value2 比较的结果为真。
		lt_flag = _arg in ['lt','gt'] and bool(value1 <  value2)  ==  bool('lt' == _arg)
		# le 当且仅当 value1≤value2 比较的结果为真。
		# ge 当且仅当 value1≥value2 比较的结果为真。
		le_flag = _arg in ['le','ge'] and bool(value1 <= value2)  ==  bool('le' == _arg)
		# eq 当且仅当value1=value2比较的结果为真。
		# ne 当且仅当value1≠value2比较的结果为真。
		eq_flag = _arg in ['eq','ne'] and bool(value1 == value2)  ==  bool('eq' == _arg)
		
		if lt_flag or le_flag or eq_flag:
			# 如果为真，则跳转
			# 用于构建一个16位有符号的分支偏移量，此偏移量为code[]的下标
			result = (branchbyte1 << 8)|branchbyte2
		# 如果比较结果为假，那程序将继续执行if_acmp<cond>指令后面的其他直接码指令
		return result

	# reference数据的条件分支判断
	def if_acmpeq(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'eq',OBJECTREF)

	def if_acmpne(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'ne',OBJECTREF)

	# int 数值的条件分支判断
	def if_icmpeq(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'eq',INT)

	def if_icmpne(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'ne',INT)

	def if_icmplt(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'lt',INT)

	def if_icmpgt(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'gt',INT)

	def if_icmple(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'le',INT)

	def if_icmpge(self,branchbyte1,branchbyte2):
		self.if_xcmpy(branchbyte1,branchbyte2,'ge',INT)

	# int 整数与零比较的条件分支判断,【x】:ne,eq,lt,gt,le,ge
	def ifx(self,branchbyte1,branchbyte2,_arg):
		# „，value →
		# „
		value = self.__pop()
		result = -1
		# 下面三组的后半部分为异异或，相同为 True ，不同为 False
		# lt 当且仅当 value1<0 比较的结果为真。
		# gt 当且仅当 value1>0 比较的结果为真。
		lt_flag = _arg in ['lt','gt'] and bool(value1 <  0)  ==  bool('lt' == _arg)
		# le 当且仅当 value1≤0 比较的结果为真。
		# ge 当且仅当 value1≥0 比较的结果为真。
		le_flag = _arg in ['le','ge'] and bool(value1 <= 0)  ==  bool('le' == _arg)
		# eq 当且仅当value1=0比较的结果为真。
		# ne 当且仅当value1≠0比较的结果为真。
		eq_flag = _arg in ['eq','ne'] and bool(value1 == 0)  ==  bool('eq' == _arg)
		
		if lt_flag or le_flag or eq_flag:
			# 如果为真，则跳转
			# 用于构建一个16位有符号的分支偏移量，此偏移量为code[]的下标
			result = (branchbyte1 << 8)|branchbyte2
		# 如果比较结果为假，那程序将继续执行if_acmp<cond>指令后面的其他直接码指令
		return result

	def ifne(self,branchbyte1,branchbyte2):
		self.ifx(branchbyte1,branchbyte2,'ne')

	def ifeq(self,branchbyte1,branchbyte2):
		self.ifx(branchbyte1,branchbyte2,'eq')

	def ifle(self,branchbyte1,branchbyte2):
		self.ifx(branchbyte1,branchbyte2,'le')

	def ifge(self,branchbyte1,branchbyte2):
		self.ifx(branchbyte1,branchbyte2,'ge')

	def iflt(self,branchbyte1,branchbyte2):
		self.ifx(branchbyte1,branchbyte2,'lt')

	def ifgt(self,branchbyte1,branchbyte2):
		self.ifx(branchbyte1,branchbyte2,'gt')

	# 引用不为空的条件分支判断
	def ifnonnull(self,branchbyte1,branchbyte2):
		# „，value →
		# „
		# value 必须为 reference 类型数据
		value = self.__pop()
		result = -1
		if value is not None:
			# 如果为真，则跳转
			# 用于构建一个16位有符号的分支偏移量，此偏移量为code[]的下标
			result = (branchbyte1 << 8)|branchbyte2
		# 如果比较结果为假，那程序将继续执行if_acmp<cond>指令后面的其他直接码指令
		return result

	# 引用为空的条件分支判断
	def ifnonnull(self,branchbyte1,branchbyte2):
		# „，value →
		# „
		# value 必须为 reference 类型数据
		value = self.__pop()
		result = -1
		if value is None:
			# 如果为真，则跳转
			# 用于构建一个16位有符号的分支偏移量，此偏移量为code[]的下标
			result = (branchbyte1 << 8)|branchbyte2
		# 如果比较结果为假，那程序将继续执行if_acmp<cond>指令后面的其他直接码指令
		return result

	# 局部变量自增
	def iinc(self,index,const):
		# 操作数栈 无改变
		current_value = self.local[index]
		# 由 index 定位到的局部变量必须是 int 类型
		self.__type_check(INT,current_value)
		# const 首先带符号扩展成一个 int 类型数值,然后加到由 index 定位到的局部变量中
		value = current_value+int(const)
		self.local[index] = value

	# 从局部变量表加载一个 int 类型值到操作数栈中
	def iload(self,index):
		# „ →
		# „,value
		self.xload(index,INT)

	def iload_0(self):
		self.iload(0)

	def iload_1(self):
		self.iload(1)

	def iload_2(self):
		self.iload(2)

	def iload_3(self):
		self.iload(3)

	# iloat 类型数据乘法
	def imul(self):
		# „,value1,value2 →
		# „,result
		self.xmul(INT)

	# int 类型数据取负运算
	def ineg(self):
		# „,value →
		# „,result
		self.xneg(INT)

	# 判断对象是否指定的类型
	def instanceof(self,indexbyte1,indexbyte2):
		# „,value →
		# „,result
		# objectref 必须是一个 reference 类型的数据
		value = self.__pop()
		# 如果 objectref 为 null 的话,那 instanceof 指令将会把 int 值 0 推入到操作数栈栈顶
		if value is None:
			self.__push(0)
		else:
			self.__type_check(OBJECTREF,value)
			# 下面的位移和按位或操作，是为了组合出一个双字节数字，参考class文件定义中的【xxx_index】
			# 该索引所指向的运行时常量池项应当是一个类、接口或者数组类型的符号引用
			cpinfo_index = (indexbyte1 << 8)|indexbyte2
			# TODO _type 转换为可用类型，从常量表取出来的可能是一个类型描述符
			_type = self.cpinfo[cpinfo_index]
			result = 0
			if isinstance(value,_type):
				result = 1
			self.__push(result)

	# 调用动态方法
	def invokedynamic(self,indexbyte1,indexbyte2):# ,0,0
		pass
		# „,[arg1, [arg2 ...]]→
		# „
		# continue

	# 调用接口方法
	def invokeinterface(self,indexbyte1,indexbyte2):# ,0,0
		pass
		# „,objectref,[arg1,[arg2 ...]] →
		# „
		# continue

	# 调用超类方法、私有方法和实例初始化方法
	def invokespecial(self,indexbyte1,indexbyte2):
		# „,objectref,[arg1,[arg2 ...]] →
		# „
		# 该索引所指向的运行时常量池项应当是一个方法(§5.1)的符号引用
		cpinfo_index = (indexbyte1 << 8)|indexbyte2
		# TODO _type 转换为可用类型，从常量表取出来的可能是一个类型描述符
		_method = self.cpinfo[cpinfo_index]
		args_count = _method.descriptor# TODO nedd to parse this
		args = [self.__pop() for i in xrange(args_count)].reverse()
		# objectref 所指向的对象的类型必须为当前类或者当前类的子类
		objectref = self.__pop()
		self.isNull(objectref)
		# 只有在下面所有的条件都成立的前提下,才会进行调用方法的搜索:
		# 1.当前类的 ACC_SUPER 标志为真(参见表 4-1,“类访问和属性修改”)。
		# 2.调用方法所在的类是当前类的超类。 TODO
		# 3.调用方法不是实例初始化方法(§2.9)。
		current_class = objectref.classref# TODO
		if 'ACC_STATIC' in _method.access_flags :
			raise IncompatibleClassChangeError(_method)
		elif 'ACC_SUPER' in current_class.accessFlag and _method.name != 'init':
			final_class,_method = self.__findSuperMethod(current_class,_method)
			# 方法调用的时候,一个新的栈帧将在 Java 虚拟机栈中被创建出来,
			# objectref 和连续的 n 个参数将存放到新栈帧的局部变量表中, objectref存为局部变量 0
			_local = [objectref].extend(args)
			has_return,return_value = execMethod(_method.code,_local,self.cpinfo)
			# 如果这个本地方法有返回值,那平台相关的代码返回的数据必须通过某种
			# 实现相关的方式转换成本地方法所定义的 Java 类型,并压入到操作数栈中
			if has_return:
				self.__push(return_value)
			
	# 第归查找父类方法
	def __findSuperMethod(self,current_class,_method):
		# 也可以在常量池中找
		if _method in current_class.method_info:
			return current_class,_method
		else:
			super_class = current_class.super_class
			self.__findSuperMethod(super_class,_method)

	# 调用静态方法
	def invokestatic(self,indexbyte1,indexbyte2):
		# „,[arg1,[arg2 ...]] →
		# „
		# 该索引所指向的运行时常量池项应当是一个方法(§5.1)的符号引用
		cpinfo_index = (indexbyte1 << 8)|indexbyte2
		# TODO _type 转换为可用类型，从常量表取出来的可能是一个类型描述符
		_method = self.cpinfo[cpinfo_index]
		args_count = _method.descriptor# TODO nedd to parse this
		args = [self.__pop() for i in xrange(args_count)].reverse()
		if 'ACC_STATIC' in _method.access_flags:
			has_return,return_value = execMethod(_method.code,_local,self.cpinfo)
			# 如果这个本地方法有返回值,那平台相关的代码返回的数据必须通过某种
			# 实现相关的方式转换成本地方法所定义的 Java 类型,并压入到操作数栈中
			if has_return:
				self.__push(return_value)

	# 调用实例方法,依据实例的类型进行分派
	def invokevirtual(self,indexbyte1,indexbyte2):
		# „,objectref,[arg1,[arg2 ...]] →
		# „
		# 该索引所指向的运行时常量池项应当是一个方法(§5.1)的符号引用
		cpinfo_index = (indexbyte1 << 8)|indexbyte2
		# TODO _type 转换为可用类型，从常量表取出来的可能是一个类型描述符
		_method = self.cpinfo[cpinfo_index]
		args_count = _method.descriptor# TODO nedd to parse this
		args = [self.__pop() for i in xrange(args_count)].reverse()
		# objectref 所指向的对象的类型必须为当前类或者当前类的子类
		objectref = self.__pop()
		self.isNull(objectref)
		# 只有在下面所有的条件都成立的前提下,才会进行调用方法的搜索:
		# 1.当前类的 ACC_SUPER 标志为真(参见表 4-1,“类访问和属性修改”)。
		# 2.调用方法所在的类是当前类的超类。 TODO
		# 3.调用方法不是实例初始化方法(§2.9)。
		current_class = objectref.classref# TODO
		# 如果被调用的方法是一个 static 方法,那 invokevirtual 指令将会抛出一个 IncompatibleClassChangeError 异常
		if 'ACC_STATIC' in _method.access_flags :
			raise IncompatibleClassChangeError(_method)
		elif 'ACC_SUPER' in current_class.accessFlag and _method.name != 'init':
			final_class,_method = self.__findSuperMethod(current_class,_method)
			# 方法调用的时候,一个新的栈帧将在 Java 虚拟机栈中被创建出来,
			# objectref 和连续的 n 个参数将存放到新栈帧的局部变量表中, objectref存为局部变量 0
			_local = [objectref].extend(args)
			has_return,return_value = execMethod(_method.code,_local,self.cpinfo)
			# 如果这个本地方法有返回值,那平台相关的代码返回的数据必须通过某种
			# 实现相关的方式转换成本地方法所定义的 Java 类型,并压入到操作数栈中
			if has_return:
				self.__push(return_value)

	# int 类型数值的布尔或运算
	def ior(self):
		# „,value1,value2 →
		# „,result
		self.xor(INT)
		
	# int 类型数据求余
	def irem(self):
		# „,value1,value2 →
		# „,result
		self.xrem(INT)

	# 结束方法,并返回一个 int 类型数据
	def ireturn(self):
		# „,value →
		# [empty]
		return xreturn(INT)

	# int 数值左移运算
	def ishl(self):
		# „,value1,value2 →
		# „,result
		self.xshl(INT)

	# int 数值右移运算
	def ishr(self):
		# „,value1,value2 →
		# „,result
		self.xshr(INT)

	# 将一个 int 类型数据保存到局部变量表中
	def istore(self,index):
		# „,value →
		# „
		self.xstore(index,INT)

	def istore_0(self):
		self.fstore(0)

	def istore_1(self):
		self.fstore(1)

	def istore_2(self):
		self.fstore(2)

	def istore_3(self):
		self.fstore(3)

	# int 类型数据相减
	def isub(self):
		# „,value1,value2 →
		# „,result
		self.xsub(INT)

	# int 数值逻辑右移运算,只有当value1 是负数时，才与ishr指令不一样-> (value1 >> s)+(2 << ~s)
	# 然而我们用的不是c语言，大python已经考虑到这层了，no care 正负数
	def iushr(self):
		# „,value1,value2 →
		# „,result
		self.ishr()

	# int 数值异或运算
	def ixor(self):
		# „,value1,value2 →
		# „,result
		self.xxor(INT)

	# 程序段落跳转
	def jsr(self,branchbyte1,branchbyte2):
		# „,→
		# „,address
		# 构建一个 16位有符号的分支偏移量,并压入到操作数栈中
		address = (branchbyte1 << 8) | branchbyte2
		# ret 指令从局部变量表中把它取出,这种不对称的操作是故意设计的
		self.__push(address)

	# 程序段落跳转
	def jsr_w(self,branchbyte1,branchbyte2,branchbyte3,branchbyte4):
		# „,→
		# „,address
		# 构建一个 32位有符号的分支偏移量,并压入到操作数栈中
		address = (branchbyte1 << 24) | (branchbyte2 << 16) | (branchbyte3 << 8) | branchbyte4
		return address

	# 将 long 类型数据转换为 double 类型
	def l2d(self):
		# „,value →
		# „,result
		self.x2y(LONG,DOUBLE)

	# 将 long 类型数据转换为 float 类型
	def l2f(self):
		# „,value →
		# „,result
		self.x2y(LONG,FLOAT)

	# 将 long 类型数据转换为 int 类型
	def l2i(self):
		# „,value →
		# „,result
		self.x2y(LONG,INT)

	# long 类型数据相加
	def ladd(self):
		# ...,value1,value2 →
		# ...,result
		self.xadd(LONG)

	# 从数组中加载一个 long 类型数据到操作数栈
	def laload(self):
		self.xaload(LONG)

	def land(self):
		# „,value1,value2 →
		# „,result
		self.xand(LONG)

	# 从操作数栈读取一个 long 类型数据存入到数组中
	def lastore(self):
		self.xastore(LONG)

	# 比较 2 个 long 类型数据的大小
	def lcmp(self):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
		# value1,value2 是long 类型
		self.__type_check(LONG,value2,value1)
		result = 1 if value1 > value2 else -1
		if value1 == value2:
			result = 0
		self.__push(result)

	# 将 long 类型数据 0 压入到操作数栈中
	def lconst_0(self):
		# ... →
		# ...,<d>
		self.__push(LONG(0))

	# 将 long 类型数据 1 压入到操作数栈中
	def lconst_1(self):
		# ... →
		# ...,<d>
		self.__push(LONG(1))

	# 从运行时常量池中提取数据推入操作数栈
	# 常量池中对应的值不是long和double
	def ldc(self,index):
		# „ →
		# „,value
		value = self.cpinfo[index]
		self.__push(value)

	# 从运行时常量池中提取数据推入操作数栈(宽索引)
	# 常量池中对应的值不是long和double
	def ldc_w(self,indexbyte1,indexbyte2):
		# „ →
		# „,value
		index = (indexbyte1 << 8) | indexbyte2
		value = self.cpinfo[index]
		self.__push(value)

	# 从运行时常量池中提取 long 或 double 数据推入操作数栈(宽索引)
	# long和double数据类型在常量池中占两个坑
	def ldc2_w(self,indexbyte1,indexbyte2):
		# „ →
		# „,value
		index = (indexbyte1 << 8) | indexbyte2
		up = self.cpinfo[index]
		down = self.cpinfo[index+1]
		value = (up << 8) | value
		self.__push(value)

	# long 类型数据除法
	def ldiv(self):
		# ...,value1,value2 →
		# ...,result
		self.xdiv(LONG)

	# 从局部变量表加载一个 long 类型值到操作数栈中
	def lload(self,index):
		# ..., →
		# ...,value
		# TODO index 作为索引定位的局部变量必须为 long 类型(占用 index和 index+1 两个位置)
		# ,记为 value。指令执行后,value 将会压入到操作数栈栈顶
		# 注意:lload 操作码可以与 wide 指令联合一起实现使用 2 个字节长度的无符号byte 型数值作为索引来访问局部变量表。
		self.xload(index,LONG)

	def lload_0(self):
		self.lload(0)

	def lload_1(self):
		self.lload(1)

	def lload_2(self):
		self.lload(2)

	def lload_3(self):
		self.lload(3)

	# long 类型数据乘法
	def lmul(self):
		# „,value1,value2 →
		# „,result
		self.xmul(LONG)
	
	# long 类型数据取负运算
	def lneg(self):
		# „,value →
		# „,result
		self.xneg(LONG)

	# 根据键值在跳转表中寻找配对的分支并进行跳转,如果case中的值是连续的，则用指令【tableswitch】
	# tableswitch和lookupswitch 是以 4 字节为界划分开的，所以这两条指令需要预留出相应的空位来实现对齐
	def lookupswitch(self,*args):
		# „,key →
		# „
		key = self.__pop()
		# <0-3 byte pad>：空白填充
		# defaultbyte1,defaultbyte2,defaultbyte3,defaultbyte4：默认跳转地址
		# npairs1,npairs2,npairs3,npairs4：分支数量，包含default
		# match-offset pairs：健值对,byte1,byte2,byte3,byte4:byte1,byte2,byte3,byte4，其中int是健，后面四位是offset值
		# 举例:
		# public void inc(int i){  
        # 	switch(i){
        #     case 13:i = 1;break;
        #     case 21:i = 2;break;
        #     default:i = 0;
        # 	}
        # }
		# 'codes': [27, 171, 0, 0, 0, 0, 0, 37, 0, 0, 0, 2, 0, 0, 0, 13, 0, 0, 0, 27, 0, 0, 0, 21, 0, 0, 0, 32, 4, 60, 167, 0, 10, 5, 60, 167, 0, 5, 3, 60, 177]
		# 27, iload_1
		# 171, lookupswitch
		# 0, 0, <0-3 byte pad>
		# 0, 0, 0, 37, defaultbyte1,defaultbyte2,defaultbyte3,defaultbyte4
		# 0, 0, 0, 2, npairs1,npairs2,npairs3,npairs4
		# 0, 0, 0, 13, 0, 0, 0, 27, match-offset
		# 0, 0, 0, 21, 0, 0, 0, 32, match-offset
		# 4, iconst_1
		# 60, istore_1
		# 167, 0, 10 , goto(branchbyte1,branchbyte2)
		# 5, iconst_2
		# 60, istore_1
		# 167, 0, 5, goto(branchbyte1,branchbyte2)
		# 3, iconst_0
		# 60, istore_1
		# 177 return

		count = len(args)
		# 空白填充
		pad = count%4
		# data_valid -> [4, 5, 6, 7, 8, 9, 10, 11]
		data_valid = [args[i] for i in xrange(pad,count)]
		# indexes -> [0,4]
		indexes = [i for i in xrange(len(data_valid)) if i%4 == 0]
		# data_4 -> [[4, 5, 6, 7], [8, 9, 10, 11]]
		data_4 = [data_valid[i:i+4] for i in indexes]
		default_offset = self.__byte4(data_4[0])
		pairs = self.__byte4(data_4[1])
		return_offset = None
		for x in xrange(2,2+pairs*2):
			if x%2 == 0: # 匹配健
				case_key = self.__byte4(data_4[x])
				if key == case_key: # 键值在跳转表中寻找配对的分支并进行跳转
					offset = self.__byte4(data_4[x+1])
					return offset
		# 若匹配不到，则返回默认offset
		if return_offset is None:
			return default_offset
			
	# 合成4位byte
	def __byte4(self,ls):
		return (ls[0]<< 24)|(ls[1] << 16)|(ls[2] << 8)| ls[3]
	
	# long 类型数值的布尔或运算
	def lor(self):
		# „,value1,value2 →
		# „,result
		return xor(LONG)
		
	# long 类型数据求余
	def lrem(self):
		# „,value1,value2 →
		# „,result
		self.xrem(LONG)

	# 结束方法,并返回一个 long 类型数据
	def lreturn(self):
		# „,value →
		# [empty]
		return self.xreturn(LONG)

	# long 数值左移运算
	def lshl(self):
		# „,value1,value2 →
		# „,result
		self.xshl(LONG)

	# long 数值右移运算
	def lshr(self):
		# „,value1,value2 →
		# „,result
		self.xshr(LONG)

	# 将一个 long 类型数据保存到局部变量表中
	def lstore(self,index):
		# „,value →
		# „
		# TODO 保存到 index 和 index+1 所指向的局部变量表位置中
		# TODO 后面可能将局部变量表设计成操作数栈一样的存储结构，即：一个节点存放一个值，不管其占几个字节
		# TODO dstore 指令可以与 wide 指令联合使用,以实现使用 2 字节宽度的无符号整数作为索引来访问局部变量表
		self.xstore(index,LONG)

	def lstore_0(self):
		self.dstore(0)

	def lstore_1(self):
		self.dstore(1)

	def lstore_2(self):
		self.dstore(2)

	def lstore_3(self):
		self.dstore(3)

	# long 类型数据相减
	def lsub(self):
		# „,value1,value2 →
		# „,result
		self.xsub(LONG)

	# long 数值逻辑右移运算
	def lushr(self):
		# „,value1,value2 →
		# „,result
		self.lshr()

	# long 数值异或运算
	def lxor(self):
		# „,value1,value2 →
		# „,result
		self.xxor(LONG)


	# 进入一个对象的 monitor
	def monitorenter(self):
		# „,objectref →
		# „
		# objectref 必须为 reference 类型数据
		objectref = self.__pop()
		self.isNull(objectref)
		self.__type_check(OBJECTREF,objectref)
		# 任何对象都有一个 monitor 与之关联
		# monitorenter并不用来实现synchronized语义；在此我把每个objectref对象都加上一个monitor属性，用来实现此条指令
		monitor = objectref.monitor
		# monitor计数器等于零或在拥有者为当前线程 TODO->当前线程
		if not monitor.isLock() : 
			# 在 monitor 里用队列来实现wait
			monitor.lock(self)
		elif monitor.isLock() and monitor.isOwner(self):
			monitor.incr()

	# 退出一个对象的 monitor
	def monitorexit(self):
		# „,objectref →
		# „
		# objectref 必须为 reference 类型数据
		objectref = self.__pop()
		self.isNull(objectref)
		self.__type_check(OBJECTREF,objectref)
		# 任何对象都有一个 monitor 与之关联
		# monitorenter并不用来实现synchronized语义；在此我把每个objectref对象都加上一个monitor属性，用来实现此条指令
		monitor = objectref.monitor
		# 执行 monitorexit 指令的线程必须是 objectref 对应的 monitor 的所有者
		if monitor.isOwner(self):
			monitor.reduce(self)
		else:
			# 执行 monitorexit 的线程原本并没有这个 monitor 的所有权
			raise IllegalMonitorStateException(_owner) 

	# 创建一个新的多维数组
	# dimensions 操作数是一个无符号 byte 类型数据,它必须大于或等于 1,代表创建数组的维度值
	def multianewarray(self,indexbyte1,indexbyte2,dimensions):
		# „,count1,[count2,...] →
		# „,arrayref
		# count1 描述第一个维度的长度,count2 描述第二个维度的长度,依此类推
		sizes = [self.__pop() for i in xrange(dimensions)].reverse()
		self.__type_check(sizes,INT)
		# 索引所指向的运行时常量池项应当是一个类、接口或者数组类型的符号引用
		cpinfo_index = (indexbyte1 << 8)| indexbyte2
		_type = self.cpinfo[cpinfo_index]
		arr = MultiArray(dimensions,_type,sizes)
		self.__push(arr)

	# 创建一个对象
	def new(self,indexbyte1,indexbyte2):
		# „ →
		# „,objectref
		# 索引所指向的运行时常量池项应当是一个类或接口的符号引用
		cpinfo_index = (indexbyte1 << 8)| indexbyte2
		_class = self.cpinfo[cpinfo_index]
		# 如果在类、接口或者数组的符号引用最终被解析为一个接口或抽象类,new 指令将抛出 InstantiationError 异常
		if 'ACC_ABSTRACT' in _class.access_flags or 'ACC_INTERFACE' in _class.access_flags:
			raise InstantiationError(_class.access_flags)
		# TODO 初始化一个类，并不是执行类的init方法
		# NOTE:new 指令执行后并没有完成一个对象实例创建的全部过程,只有实例初始化方法被执行并完成后,实例才算完全创建。
		objectref = None
		self.__push(objectref)

	# 创建一个数组
	def newarray(self,atype):
		# „,count →
		# „,arrayref
		count = self.__pop()
		self.__type_check(INT,count)
		if count < 0:
			raise NegativeArraySizeException(count)
		_type = atypes.get(atype)
		arrayref = Array(count,_type)
		self.__push(arrayref)

	# 什么事情都不做
	def nop(self):
		# 无变化
		pass


	# 将操作数栈的栈顶元素出栈
	def pop(self):
		# „,value →
		# „
		self.__pop()


	# 将操作数栈的栈顶一个或两个元素出栈
	def pop2(self):
		# value2,value1 →
		# „
		value1 = self.__pop()
		value2 = self.__pop()
		return value2,value1


	# 设置对象字段
	def putfield(self,indexbyte1,indexbyte2):
		# „,objectref,value →
		# „
		# 索引所指向的运行时常量池项应当是一个字段(§5.1)的符号引用
		cpinfo_index = (indexbyte1 << 8)| indexbyte2
		_field = self.cpinfo[cpinfo_index]
		value = self.__pop()
		objectref = self.__pop()
		self.isNull(objectref)
		self.__type_check(OBJECTREF,objectref)
		# TODO _field 需要转化为真实的field字段名称
		setattr(objectref,_field,value)

	# 设置对象的静态字段值
	def putstatic(self,indexbyte1,indexbyte2):
		# „,objectref,value →
		# „
		# 索引所指向的运行时常量池项应当是一个字段(§5.1)的符号引用
		cpinfo_index = (indexbyte1 << 8)| indexbyte2
		_field = self.cpinfo[cpinfo_index]
		# not-static
		if 'ACC_STATIC' not in _field.access_flags:
			raise IncompatibleClassChangeError(_field.access_flags)
		# final
		elif 'ACC_FINAL' in _field.access_flags:
			raise IllegalAccessError(_field)
		value = self.__pop()
		objectref = self.__pop()
		self.isNull(objectref)
		self.__type_check(OBJECTREF,objectref)
		# TODO _field 需要转化为真实的field字段名称
		setattr(objectref,_field,value)

	# 代码片段中返回
	def ret(self,index):
		# 无变化
		# index 是一个 0 至 255 之间的无符号数
		# ret 指令不应与 return 指令混为一谈,return 是在没有返回值的方法返回时使用
		value = self.locals[index]
		# 指令执行后,将该局部变量的值更新到 Java 虚拟机的 PC 寄存器中,令程序从修改后的位置继续执行
		# TODO pc_cache = value


	# 无返回值的方法返回
	def Return(self):
		# „ →
		# [empty]
		# 指令执行后,解释器会恢复调用者的栈帧,并且把程序控制权交回到调用者
		# TODO synchronized
		return

	# 从数组中加载一个 short 类型数据到操作数栈
	def saload(self):
		# „,arrayref,index →
		# „,value
		self.xaload(SHORT)

	# 从操作数栈读取一个 short 类型数据存入到数组中
	def sastore(self):
		# „,arrayref,index,value →
		# „
		self.xastore(SHORT)

	# 将一个 short 类型数据入栈
	def sipush(self,byte1,byte2):
		# „ →
		# „,value
		value = (byte1 << 8)| byte2
		self.__push(value)

	# 交换操作数栈顶的两个值
	def swap(self):
		# „,value2,value1 →
		# „,value1,value2
		value2,value1 = self.pop2()
		self.__push(value1)
		self.__push(value2)
		print '0x5f'

	# 根据索引值在跳转表中寻找配对的分支并进行跳转
	def tableswitch(self,*xargs):
		# „,index →
		# „
		# args 
		# <0-3 byte pad>
		# defaultbyte1
		# defaultbyte2
		# defaultbyte3
		# defaultbyte4
		# lowbyte1
		# lowbyte2
		# lowbyte3
		# lowbyte4
		# highbyte1
		# highbyte2
		# highbyte3
		# highbyte4
		# jump offsets...
		index = self.__pop()
		# <0-3 byte pad>：空白填充
		# defaultbyte1,defaultbyte2,defaultbyte3,defaultbyte4：默认跳转地址
		# lowbyte1,lowbyte2,lowbyte3,lowbyte4 ：
		# highbyte1,highbyte2,highbyte3,highbyte4 ：
		# jump offsets ：跳转地址,byte1,byte2,byte3,byte4
		# 举例:
		# public void inc(int i){  
        # 	switch(i){
        #     case 2:i = 1;break;
        #     case 3:i = 2;break;
        #     case 4:i = 2;break;
        #     default:i = 0;
        # 	}
        # }
		# 'codes': [27, 170, 0, 0, 0, 0, 0, 42, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 27, 0, 0, 0, 32, 0, 0, 0, 37, 4, 60, 167, 0, 15, 5, 60, 167, 0, 10, 5, 60, 167, 0, 5, 3, 60, 177]
		# 27, iload_1
		# 171, lookupswitch
		# 0, 0, <0-3 byte pad>
		# 0, 0, 0, 37, defaultbyte1,defaultbyte2,defaultbyte3,defaultbyte4
		# 0, 0, 0, 2, lowbyte1,lowbyte2,lowbyte3,lowbyte4
		# 0, 0, 0, 4, highbyte1,highbyte2,highbyte3,highbyte4
		# 0, 0, 0, 27, jump offset
		# 0, 0, 0, 32, jump offset
		# 0, 0, 0, 37, jump offset
		# 4, iconst_1
		# 60, istore_1
		# 167, 0, 15 , goto(branchbyte1,branchbyte2)
		# 5, iconst_2
		# 60, istore_1
		# 167, 0, 10, goto(branchbyte1,branchbyte2)
		# 5, iconst_2
		# 60, istore_1
		# 167, 0, 5, goto(branchbyte1,branchbyte2)
		# 3, iconst_0
		# 60, istore_1
		# 177 return
		count = len(args)
		# 空白填充
		pad = count%4
		# data_valid -> [4, 5, 6, 7, 8, 9, 10, 11]
		data_valid = [args[i] for i in xrange(pad,count)]
		# indexes -> [0,4]
		indexes = [i for i in xrange(len(data_valid)) if i%4 == 0]
		# data_4 -> [[4, 5, 6, 7], [8, 9, 10, 11]]
		data_4 = [data_valid[i:i+4] for i in indexes]
		default_offset = self.__byte4(data_4[0])
		low = self.__byte4(data_4[1])
		high = self.__byte4(data_4[2])
		
		if index in xrange(low,high+1):
			return self.__byte4(data_4[2+index-low+1])
		else:
			return default_offset

	# 扩展局部变量表索引
	# _opcode in [iload, fload, aload, lload, dload, istore, fstore,astore,lstore,dstore,ret]
	def wide(self,_opcode,indexbyte1,indexbyte2):
		# 操作数栈 与被扩展的指令一致
		index = (indexbyte1 << 8) | indexbyte2
		fun = getattr(self,_opcode)
		# 反射执行
		fun(index)

	# iinc 扩展局部变量表索引
	def wide(self,iinc,indexbyte1,indexbyte2,constbyte1,constbyte2):
		# 操作数栈 与被扩展的指令一致
		index = (indexbyte1 << 8) | indexbyte2
		const = (constbyte1 << 8) | constbyte2
		# 反射执行
		self.iinc(index,const)


if __name__ == '__main__':
	q = Stack(3)
	# arr = [11,22,33]
	# q.push(arr)
	# q.push(1)
	# print q.list()
	# o = Opcode(q,[],[])
	# o.do('aaload')
	# print q.list()
	# _arg = 'l'
	# print 1 if _arg is 'l' else -1
	# o = Opcode(q,[],[])
	# _proxy = getattr(o,'_proxy')

	# _method1 = _proxy(1)
	# _method1()
	# print _method1
	# _method1 = _proxy(2)
	# print _method1
	# _method1()
	cpinfo = [None, '#7,#27', '#28,#29', '#30', '#31,#32', '#33', '#34', '#35', 'm', 'I', 'n', 'J', 'ConstantValue', ['0x00', '0x00', '0x00', '0x00'], ['0x00', '0x00', '0x00', '0x01'], '<init>', '()V', 'Code', 'LineNumberTable', 'inc', '(I)V', 'StackMapTable', 'tcc', 'main', '([Ljava/lang/String;)V', 'SourceFile', 'test.java', '#15,#16', '#36', '#37,#38', '11111111111111', '#39', '#40,#41', '', 'cls/test', 'java/lang/Object', 'java/lang/System', 'out', 'Ljava/io/PrintStream;', 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V']
	# main_code = [178, 0, 2, 18, 3, 182, 0, 4, 16, 10, 60, 18, 5, 77, 177]
	tableswitch_code = [27, 170, 0, 0, 0, 0, 0, 42, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 27, 0, 0, 0, 32, 0, 0, 0, 37, 4, 60, 167, 0, 15, 5, 60, 167, 0, 10, 5, 60, 167, 0, 5, 3, 60, 177]
	e = ExecMethod(tableswitch_code,[],cpinfo)
	e.execute()

