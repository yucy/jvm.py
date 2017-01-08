# -*- coding:utf-8 -*-
import os
from sys import argv
from bootstrap import Bootstrap

def main(start_path):
	boot = Bootstrap(start_path)
	

# 执行该 APP启动类的main方法
def execute():
	print 234
	return False or True

# JVM 启动入口
if __name__ == '__main__':
	# argv,第一个参数是python后面算起的，我们的启动命令是：python py/classLoader.py cls/demo.class
	# 很显然，我们要读取的是class文件，是第二个参数，故而我们用argv[1]
	# path = argv[1]
	# 加载APP启动类
	path = '../cls/test.class'
	main()