# -*- coding:utf-8 -*-

# 将多个十六进制整合转化为十进制，并返回
def getDecimal(arr):
	if len(arr) == 0:
		return None
	else:
		return int('0x%s' % ''.join(arr).replace('0x',''),16)


if __name__ == '__main__':
	d = {'a':getDecimal('0x0f')
	,'b':[i for i in xrange(10)]
	}
	print d['a']
	b = d
	print b
	d.update({'c':123})
	print d
	print isinstance(d,dict)
