# -*- coding:utf-8 -*-
import sys,threading,time
sys.path.append('..')
from Queue import Queue
from parser.struct import *

def test_dict():
	attr = {'test':2}
	attr['test'] = 123
	print attr

def test_if():
	a = None
	print a if a is not None else '222'

def test_type():
	INT = int
	[DOUBLE,FLOAT] = ['double','float']
	print DOUBLE
	print FLOAT
	print INT(123.45)

def test_bit_move():
	# int 低 5 位所表示的值
	i = 15
	print i & int('11',2)
	print int('11111',2)
	print 2 << (i & int('11',2))
	print 32 >> (i & int('11',2))
	print -32 >> (i & int('11',2))

def test_up_down():
	ii = 171 # 1010 1011
	up = ii >> 4
	down = ii & int('00001111',2)
	source = (up << 4) | down
	print up,down,source
	# 11111111111111111111111111111111
	# double up:31(符号占一位),down:32
	# 00000000000000000000000000000000111111111111111111111111111111111

def test_char():
	print chr(12)
	print str(12)

def test_args(num,*args):
	print num
	print args[1]
	print dir(args)
	count = len(args)
	nop = count%4
	ll = [args[i] for i in xrange(nop,count)]
	print ll
	indexes = [i for i in xrange(len(ll)) if i%4 == 0]
	print [ll[i:i+4] for i in indexes]

	print args.count

def test_kwargs(num,**kwargs):
	print num
	print type(args)
	for i in args:
		print i 

def test_each4():
	ls = [0,1,2,3,4,5,6,7,8,9,10,11]
	pairs = 5
	for x in xrange(2,2+pairs*2):
		print '---------',x
		if x%2 == 0:
			print x,ls[x]
	print range(2,10)

def test_range():
	print 10 in xrange(9,10)

class test_invoke(object):
	def __init__(self):
		pass

	def m1(self):
		fun = getattr(self,'m2')
		fun('abc')

	def m2(self,_arg):
		print _arg
		
def test_queue():
	q = Queue()
	print dir(q)
	q.put('a')
	q.put('b')
	print q.queue
	print q.get()
	print q.queue
	print q.empty()
	print q.full()
	lock = threading.Lock()



if __name__ == '__main__':
	# test_dict()
	# test_if()
	# test_type()
	# test_bit_move()
	# test_up_down()
	# test_char()
	# test_args(2,1,2,3,4,5,6,7,8,9,10,11)
	# test_kwargs(2,a=1,b=2)
	# test_each4()
	# test_range()
	# t = test_invoke()
	# t.m1()
	# test_queue()
	mo = Monitor(2,'a')
	time.sleep(5)
	mo.lock('aa')
	mo.lock('ba')
