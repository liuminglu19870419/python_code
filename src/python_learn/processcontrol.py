#coding: UTF-8
'''
Created on  2014-04-07

@author: mingliu
'''
import time
import multiprocessing
import os

def f(arg):
    while True:
        print '%s %s' %(os.getpid(), time.clock())
        time.sleep(1)

if __name__ == '__main__':
    pool = multiprocessing.Pool(5)
    rel = pool.map(f, (None, None))
    time.sleep(4)
    print 'close'
    pool.close()
    print 'terminate'
    pool.terminate()
    