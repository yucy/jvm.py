# -*- coding:utf-8 -*-

from time import sleep, time  
import gc  
'''
结论：
当调用del时，其实Python并不会真正release内存，而是将其继续放在其内存池中；
只有在显式调用gc.collect()或者设置引用变量为None时，才会真正release内存
'''
def test_release(way=1):  
    print time()  
    for i in range(10000000):  
        if way == 1:  
            pass  
        elif way == 0:
            i = None
        else:  # way 2, 3  
            del i  
              
    print time()  
    if way == 1 or way == 2:  
        pass  
    else:  # way 3  
        gc.collect()  
    print time()  

def gc_test():
    a = '1'
    print sys.getrefcount('1')
    del a
    print gc.garbage
    print sys.getrefcount('1')

    b = 0
    print sys.getrefcount(b)

    c = 'kjfakjdncaoiduf'
    print sys.getrefcount(c)

    print(gc.get_threshold())

    gc.set_threshold(600,10,5)
    print gc.get_threshold()
    print gc.get_count()
    print gc.get_count()
    print gc.get_count()
    print gc.get_count()
    
          
if __name__ == "__main__":  
    print "Test way 1: just pass"  
    test_release(way=1)  
    sleep(20)  
    print "Test way 0: just None"  
    test_release(way=0)  
    sleep(20)  
    print "Test way 2: just del"  
    test_release(way=2)  
    sleep(20)  
    print "Test way 3: del, and then gc.collect()"  
    test_release(way=3)  
    sleep(20) 
