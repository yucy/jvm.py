# -*- coding:utf-8 -*-

rt_path = '../rt'
rt_jar_path = '/opt/jdk1.7.0_67/jre/lib/rt.jar'

# 类加载，等class文件加载完成后，就开始类加载过程。类加载完成后放入方法区。
# 内容包括运行时常量池，类型信息，字段信息，方法信息，类加载器引用，Class实例引用
# 我们这里的类加载器引用都为None，因为都是用bootstrap 加载器加载的，而不是用户自定义类加载器加载
class Bootstrap(object):
	# _class参数可以从classLoader.py里的映射hash表得到
	def __init__(self, _class):
		self.arg = _class

	# 装载阶段 - 查找并装载类型的二进制数据. 此阶段在classFileLoader.py中完成了
	def load(self):
		pass

		# 验证阶段 - 确保被导入类型的正确性
	def __verity(self):
		# 1.文件格式验证：是否以魔数开头、版本号是否在正确范围、常量池中是否有不支持的常量类型等
		# 2.元数据验证：子类是否继承了final方法、是否实现了父类或接口必要的方法、子类与父类是否有字段或方法冲突等
		# 3.字节码验证：字段类型是否匹配、方法体中的代码是否会跳转越界、方法体中的类型转换是否有效等
		# 4.符号引用验证：全限定名是否能对应到具体类、类，字段和方法访问权限等
		pass

	# 准备阶段 - 为类或接口的静态字段分配空间,并用默认值初始化这些字段
	# 数值类型 -> 0，boolean类型 -> False，char -> '\u0000'，reference类型 -> None
	def __preparation(self):
		# 1.非final的静态字段 : 正常赋予静态变量初始值
		# 2.final+static字段 : 直接从其ContentValue属性中取出值来做初始化
		pass

	# 解析阶段 - 把类型中的符号引用转化为直接引用，可以在指令anewarray、checkcast、getfield、getstatic、instanceof等的触发下执行
	# 说一句：在这里我们一步到位，加载过程直接到初始化阶段，不用指令这些指令来触发。
	def __resolution(self):
		# 1.类或接口的解析
		# 2.字段的解析
		# 3.类方法的解析
		# 4.接口方法的解析
		pass

	# 初始化阶段 - 把类变量初始化为正确的初始值，执行类构造器<clinit>方法，如果有父类，则需要先执行父类的<clinit>方法
	# 注意接口的情况，只有当子接口或者实现类用到了父接口的静态变量时，才需要执行父接口的<clinit>方法，如果父接口有的话。
	def __clinit(self):
		pass

	# 类的实例化 - 执行类的实例构造函数<init>，由new等指令来触发
	def init(self):
		pass

		

if __name__ == '__main__':
	main()