#! /usr/bin/env python
#coding=utf-8
import time
def deco(arg):
    print arg
    def _deco(fun):
        def __deco(*args, **kwargs):
            print 'before'
            ret = fun(*args, **kwargs)
            print 'after'
            return ret
        return __deco
    return _deco

@deco('test')
def fun(a, b):
    print 'a + b:',a + b
    return (a + b)
def fun3(a, b, c):
    print 'a + b + c:',a + b + c
    return (a + b + c)
time.sleep(10)
fun(1,3)
fun3(1,2,3)
