#coding: UTF-8
'''
Created on  2014-03-28

@author: mingliu
'''
import subprocess
import threading
import time
import signal
import os

pi = subprocess.Popen('python /home/mingliu/deco.py', stdout=None, shell=True)

def term():
    time.sleep(2)
    print 'kill thread start'
    print pi.pid
    os.kill(pi.pid, signal.SIGKILL)
    print 'kill thread finished'

if __name__ == '__main__':
    print 'start'
    threading.Thread(target=term).start()
    pi.wait()
    print 'all finished'
