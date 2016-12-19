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
		value1 = 76
		value2 = 34

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

if __name__ == '__main__':
	attr = {'test':2}
	attr['test'] = 123
	print attr
	a = None
	print a if a is not None else '222'
	[DOUBLE,FLOAT] = ['double','float']
	print DOUBLE
	print FLOAT
	result = if_xcmpy(4,0,'ne')
	print '==========:',result
	print Null
