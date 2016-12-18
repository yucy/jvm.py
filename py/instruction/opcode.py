# -*- coding:utf-8 -*-
import sys,math
sys.path.append('..')

from lang.myexceptions import *
from lang.mycollections import *

# §2.11.1 的表 2.3 中列出的分类一
dup_type1 = (boolean,byte,char,short,int,float,reference,returnAddress)
# §2.11.1 的表 2.3 中列出的分类二
dup_type2 = (long,double)

# 数据类型定义常量
[FLOAT,DOUBLE,BYTE,CHAR,SHORT,INT,LONG,OBJECTREF] = ['float','double','byte','char','short','int','long','objectref']

# sys.getrefcount(obj) # 引用计数

class Opcode(object):
	"""docstring for Opcode"""
	# stack：操作数栈，local：局部变量表，cpinfo：常量池
	def __init__(self,_stack,_local,_cpinfo):
		self.stack = _stack
		self.local = _local
		self.cpinfo = _cpinfo

	def __pop(self):
		return self.stack.pop()

	def __push(self,value):
		self.stack.push(value)

	def isNull(self,obj,msg='Null'):
		if obj is None:
			raise NullPointException(msg)
		
	def do(self,code,*args):
		func = getattr(self,code)
		# execute operate code
		func()
	# =============================================================
	# 结束方法,并返回一个 x 类型数据
	# TODO 后续需要考虑synchronized方法的IllegalMonitorStateException异常
	def xreturn(self,_type):
		# ...,value →
		# [empty] # 个人理解：方法操作结束的时候，操作数栈里最后一个元素就是objectref，它出栈以后，stack就empty了。
		value = self.__pop()
		return value

	# 从数组中加载一个 x 类型数据到操作数栈
	def xaload(self,_type):
		# ...,arrayref,index →
		# ...,value
		index = self.__pop()
		arrayref = self.__pop()
		# judge this obj is null
		self.isNull(arrayref)
		value = arrayref[index]
		self.__push(value)

	# 从操作数栈读取一个 x 类型数据存入到数组中
	def xastore(self,_type):
		# ...,arrayref,index,value →
		# ...,
		value = self.__pop()
		index = self.__pop()
		arrayref = self.__pop()
		# judge this obj is null
		self.isNull(arrayref)
		arrayref[index] = value

	# 从局部变量表加载一个x 类型值到操作数栈中
	def xload(self,index,_type):
		# ... →
		# ...,value #说明: value 是x 类型
		value = self.local[index]
		self.__push(value)

	# 将一个 x 类型数据保存到局部变量表中。
	def xstore(self,index,_type):
		# ...,value → #说明: value 是x 类型
		# ...
		value = self.__pop()
		self.local[index] = value

	# 数值计算---------------------------

	# x 类型数据相加
	def xadd(self,_type):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
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
		if math.isnan(value):
			result = float(nan)
		else:
			result = value*-1
		self.__push(result)

	# x 类型数据求余
	def xrem(self,_type):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
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

	# 'dcmpl',#比较栈顶两double型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将-1压入栈顶。
	# 'dcmpg',#比较栈顶两double型数值大小，并将结果（1，0，-1）压入栈顶；当其中一个数值为“NaN”时，将1压入栈顶。
	def xcmp(self,_type,_arg):
		# ...,value1,value2 →
		# ...,result
		value2 = self.__pop()
		value1 = self.__pop()
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
		value = self.__pop()
		# TODO python里没有单精度的概念，java里的float和double都对应python里的float
		self.__push(float(value))

	# 将 double 类型数据转换为 int 类型
	def d2i(self):
		# ...,value →
		# ...,result
		value = self.__pop()
		# python里超过int范围的整数就自动当长整数(long)处理
		self.__push(int(value))

	# 将 double 类型数据转换为 long 类型
	def d2l(self):
		# ...,value →
		# ...,result
		value = self.__pop()
		self.__push(long(value))

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

	# 将 double 类型数据压入到操作数栈中
	def dconst_x(self,value):
		# ... →
		# ...,<d>
		self.__push(value)

	# 将 double 类型数据 0 压入到操作数栈中
	def dconst_0(self):
		# ... →
		# ...,<d>
		self.dconst_x(float(0.0))

	# 将 double 类型数据 1 压入到操作数栈中
	def dconst_1(self):
		# ... →
		# ...,<d>
		self.dconst_x(float(1.0))

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
		value = self.__pop()
		# TODO T_T,python has no type [double].
		self.__push(float(value))

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
		self.__push(float(0))

	def fconst_1(self):
		# „ →
		# „,<f>
		self.__push(float(1))

	def fconst_2(self):
		# „ →
		# „,<f>
		self.__push(float(2))

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
		# continue


if __name__ == '__main__':
	q = Stack(3)
	arr = [11,22,33]
	q.push(arr)
	q.push(1)
	print q.list()
	o = Opcode(q,[],[])
	o.do('aaload')
	print q.list()
	_arg = 'l'
	print 1 if _arg is 'l' else -1

