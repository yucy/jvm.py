# -*- coding:utf-8 -*-

# 将多个十六进制整合转化为十进制，并返回
def getDecimal(arr):
	if len(arr) == 0:
		return None
	else:
		return int('0x%s' % ''.join(arr).replace('0x',''),16)

def if_xcmpy(branchbyte1,branchbyte2,_arg):
		# „，value1，value2 →
		# „
		value1 = 2
		value2 = 1
		result = -1
		# eq 当且仅当value1=value2比较的结果为真。
		# ne 当且仅当value1≠value2比较的结果为真。
		print '=====',bool(value1 < value2)  !=  bool('lt' == _arg)
		print bool(value1 == value2)  ==  bool('eq' == _arg)
		# 异异或，相同为 True ，不同为 False
		if     bool(value1 == value2)  ==  bool('eq' == _arg) \
			or bool(value1 < value2)  !=  bool('lt' == _arg) \
			or bool(value1 <= value2)  !=  bool('le' == _arg):
			# 如果为真，则跳转
			# 用于构建一个16位有符号的分支偏移量，此偏移量为code[]的下标
			result = (branchbyte1 << 8)|branchbyte2
		# 如果比较结果为假，那程序将继续执行if_acmp<cond>指令后面的其他直接码指令
		return result

if __name__ == '__main__':
	attr = {'test':2}
	attr['test'] = 123
	print attr
	a = None
	print a if a is not None else '222'
	[DOUBLE,FLOAT] = ['double','float']
	print DOUBLE
	print FLOAT
	result = if_xcmpy(4,0,'gt')
	print '==========:',result
