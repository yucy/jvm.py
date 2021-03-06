# -*- coding:utf-8 -*-

from common.utils import getDecimal
from common.content import constant_type,cmd
from bean.parserBean import FieldInfo,MethodInfo,AttributeInfo

# 3405691582
_MAGIC = int('0XCAFEBABE',16)

class ClassParser(object):
	
	def __init__(self, _data):
		# class 二进制文件数据
		self.data = _data
		# XXX 碰到个疑难杂症，如果把 constant_pool 等放在__init__函数外面做成类变量，则父 classfile
		# 的pool和子 classfile 的pool一致，而且id(self) 函数也只会执行一次
		# 保存常量池
		self.constant_pool = [None]
		# 常量池类型，后面转换直接引用时会用到
		self.cp_tag = [None]
		# 保存类中的方法信息
		self.methods = []
		# 保存类中的字段信息
		self.fields = []
		# class 游标位置
		self.offset = 0
		self._cls_args = {}
		# print self.constant_pool
		self.javap()
		# print '================id===============',id(self)
		
	# class 全局游标
	def cursor(self,step):
		# print '------data',self.data
		result = self.data[self.offset:self.offset+step]
		self.offset += step
		return result

	# 解析class文件
	def javap(self):
		
		# u4 magic;
		magic = ''.join(self.cursor(4)).replace('0x','')
		if getDecimal(magic) != _MAGIC:
			print 'This is not a valid class file.'
			return
		# u2 minor_version;
		minor_version=getDecimal(self.cursor(2))
		# u2 major_version;
		major_version=getDecimal(self.cursor(2))
		# u2 constant_pool_count;
		constant_pool_count = getDecimal(self.cursor(2))-1
		# print 'constant_pool_count:',constant_pool_count
		self._cls_args.update({
			'magic':magic,
			'minor_version':minor_version,
			'major_version':major_version,
			'constant_pool_count':constant_pool_count,
			'cp_info':self.constant_pool,
			'cp_tag':self.cp_tag
			})
		# cp_info constant_pool[constant_pool_count-1];
		constant_pool_index = 0
		while constant_pool_count > constant_pool_index:
			# print 'constant_pool_count:%d constant_pool_index:%d' % (constant_pool_count , constant_pool_index)
			constant_pool_index += 1
			tag = getDecimal(self.cursor(1))
			constant_name = constant_type.get(tag)
			# print 'tag:%d\tconstant_name:%s' % (tag,constant_name)
			# _struct = getStruct(constant_name)
			ref_index,utf8_data = None,''
			up,down,is_longORdouble  = '','',False
			if tag == 7:# Class
				# u1 tag;
				# u2 name_index;
				ref_index=self.constant_2(2)
			elif tag in (9,10,11):# Fieldref,Methodref,InterfaceMethodref
				# u1 tag;
				# u2 class_index;
				# u2 name_and_type_index;
				ref_index=self.constant_3(2,2)
			elif tag == 8:# String
				# u1 tag;
				# u2 string_index;
				ref_index=self.constant_2(2)
			elif tag in (3,4):# Integer,Float
				# u1 tag;
				# u4 bytes;
				ref_index=getDecimal(self.cursor(4))
			# 在 Class 文件的常量池中,所有的 8 字节的常量都占两个表成员(项)的空间。如果一个
			# CONSTANT_Long_info 或 CONSTANT_Double_info 结构的项在常量池中的索引为 n,则常量
			# 池中下一个有效的项的索引为 n+2,此时常量池中索引为 n+1 的项有效但必须被认为不可用
			elif tag in (5,6):# long , double
				constant_pool_index += 1
				# u1 tag;
				# u4 high_bytes;
				# u4 low_bytes;
				is_longORdouble = True
				up,down = self.cursor(4),self.cursor(4)
			elif tag == 12:# NameAndType
				# u1 tag;
				# u2 name_index;
				# u2 descriptor_index;
				ref_index=self.constant_3(2,2)
			elif tag == 1:# UTF8
				# u1 tag;
				# u2 length;
				# u1 bytes[length];
				bytes_len = getDecimal(self.cursor(2))
				utf8_data = ''.join([chr(int(b,16)) for b in self.cursor(bytes_len)])
				# print 'utf8_data:%s' % utf8_data
			elif tag == 15:# MethodHandler
				# u1 tag;
				# u1 reference_kind;
				# u2 reference_index;
				ref_index=self.constant_3(1,2)
			elif tag == 16:# MethodType
				# u1 tag;
				# u2 descriptor_index;
				ref_index=self.constant_2(2)
			elif tag == 18:# InvokeDynamic
				# u1 tag;
				# u2 bootstrap_method_attr_index;
				# u2 name_and_type_index;
				ref_index=self.constant_3(2,2)
			constant_info = ref_index if ref_index is not None else utf8_data
			# 常量池类型
			self.cp_tag.append(tag)
			if is_longORdouble:
				self.constant_pool.extend([up,down])
				self.cp_tag.append(0)
			else:
				self.constant_pool.append(constant_info)
			# print '#%d %s\t\t%s' % (constant_pool_index,constant_name[9:-5],constant_info)
		# =============常量池处理完毕==================================================
		# u2 access_flags;
		access_flags = getDecimal(self.cursor(2))
		# u2 this_class;
		this_class = self.getConstant(getDecimal(self.cursor(2)))
		# u2 super_class;
		super_class = self.getConstant(getDecimal(self.cursor(2)))
		# 如果当前类是Object，那么 _super_temp 是 None
		# u2 interfaces_count;
		interfaces_count = getDecimal(self.cursor(2))
		interfaces = []
		if interfaces_count > 0:
			# u2 interfaces[interfaces_count];
			interfaces = [getDecimal(self.cursor(2)) for i in xrange(interfaces_count)]
		# u2 fields_count;
		fields_count = getDecimal(self.cursor(2))
		# field_info fields[fields_count];
		if fields_count > 0:
			self.methodAndFieldHandler('field',fields_count)
		# u2 methods_count;
		methods_count = getDecimal(self.cursor(2))
		# method_info methods[methods_count];
		if methods_count > 0:
			self.methodAndFieldHandler('method',methods_count)
		# u2 attributes_count;
		attributes_count = getDecimal(self.cursor(2))
		# attribute_info attributes[attributes_count];
		# if attributes_count > 0:
		# 	attrHandler()
		self._cls_args.update({
			'access_flags':access_flags,
			'this_class':this_class,
			'super_class':super_class,
			'interfaces_count':interfaces_count,
			'interfaces':interfaces,
			'fields_count':fields_count,
			'field_info':self.fields,
			'methods_count':methods_count,
			'method_info':self.methods,
			'attributes_count':attributes_count,
			'attribute_info':self.handlerAttr(attributes_count)
			})
		# return CClassFile(_cls_args)
		# return _cls_args

	# 处理常量类型结构里元素数量等于2的
	def constant_2(self,second):
		ref_index = '#%d' % getDecimal(self.cursor(second))
		return ref_index

	# 处理常量类型结构里元素数量等于3的
	def constant_3(self,second,third):
		ref_index = '#%d,#%d' % (getDecimal(self.cursor(second)),getDecimal(self.cursor(third)))
		return ref_index

	# 从常量池中获取值
	def getConstant(self,num):
		try:
			source = self.constant_pool[num]
			if isinstance(source,str) and source.__contains__('#'):
				temp = source.replace('#','')
				pointers = temp.split(',')
				target = [self.constant_pool[int(i)] for i in pointers]
				return target if len(target) > 1 else target[0]
			return source
		except Exception, e:
			print '==========================',num,len(self.constant_pool)
		
	def methodAndFieldHandler(self,_type,count):
		# global methods,fields
		if count <= 0:
			print 'count can not lower than zero.[methodAndFieldHandler]'
			return None
		temp = []
		for i in xrange(count):
			# print '\t %s:%d' % (_type,i)
			# u2 access_flags;
			# u2 name_index;
			# u2 descriptor_index;
			# u2 attributes_count;
			args = {
				'access_flags':getDecimal(self.cursor(2)),
				'name':self.getConstant(getDecimal(self.cursor(2))),
				'descriptor':self.getConstant(getDecimal(self.cursor(2)))
			}
			attributes_count = getDecimal(self.cursor(2))
			# attribute_info attributes[attributes_count];
			# if attributes_count > 0:
			
			args.update({
				'attributes_count':attributes_count,
				'attributes':self.handlerAttr(attributes_count)
				})
			temp.append(args)
		if _type == 'field':
			# list[-1:]=[] 效果等同于 list.extend(..)
			self.fields[-1:] =  [FieldInfo(x) for x in temp]
		else:
			self.methods[-1:] =  [MethodInfo(x) for x in temp]

	def handlerAttr(self,count):
		attributes = []
		for x in xrange(count):
			attr_name = self.cursor(2)
			attr_length = self.cursor(4)
			attr_desc = self.cursor(getDecimal(attr_length))
			attr_arg = attr_name+attr_length+attr_desc
			attributes.append(AttributeInfo(attr_arg,self.constant_pool))
		return attributes

	# 获取常量类型结构定义
	# def getStruct(self,struct_name):
	# 	return getattr(struct,struct_name)

if __name__=="__main__":
	# demo
	# data =  ['0xca', '0xfe', '0xba', '0xbe',...]
	# _class = javap(data)
	# print '============================='
	# method_info = _class.method_info
	# for x in method_info:
	# 	print x.name
	# 	print x.code.__dict__

	print _MAGIC
	# print range(40,46)
	# print ''.join([chr(int(data[i],16)) for i in xrange(40,46)])
	# print getStruct(constant_type.get('1'))

	# self.constant_pool = [1,2,3,4,5,6]
	# pointers = [2,3]
	# print tuple([self.constant_pool[i-1] for i in pointers])
	# print '%s %s' % tuple([self.constant_pool[i-1] for i in pointers])
	# print 123
	# print ['this %s at %d' % ('self.getConstant(getDecimal(self.cursor(2)))',i) for i in xrange(2)]
	# print self.constant_pool[0]
	# print [x for x in xrange(10) if 0<x<8]
	# print hex(int('0x0f',16))

