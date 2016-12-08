# -*- coding:utf-8 -*-

# 将多个十六进制整合转化为十进制，并返回
def getDecimal(arr):
	if len(arr) == 0:
		return None
	else:
		return int('0x%s' % ''.join(arr).replace('0x',''),16)


if __name__ == '__main__':
	attr = {'test':2}
	attr['test'] = 123
	print attr