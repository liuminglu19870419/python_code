'''

@author: xiaoluBambi
'''
from PyQt4.QtGui import QApplication
import Queue
from configglue.app.base import App
import os
from os.path import isdir
import random
import sys
import threading
import time
import traceback

from api import get_file_list, save_file, get_html
from utils import Crawler
from PyQt4 import QtCore


FILE_PATH = '/home/mlliu/Desktop/newdata/'
HTML_FILE_PATH = '/home/mlliu/Desktop/html/'
EMPTY_LINE = ['', '\r\n', '\r', '\n']
THREAD_COUNT = 20
queue = Queue.Queue(THREAD_COUNT)
count=0
finish_count=0

def fun(path, file_name, url):
#     print file_name
#     print url
    try:
        save_file(file_name, get_html(url))
    except Exception, e:
        print e
    finally:
        print queue.qsize()
        queue.get()
        global finish_count
        finish_count += 1
        print "finished",finish_count

SCRIPT_FILE = 'python /home/mlliu/git/python_code/src/chinamobiledataprocess/demodatacrawler/utils.py'

def sub_process(url, file_name):
    print file_name
    output = os.popen(SCRIPT_FILE + " " + url + " " + file_name)
    output.read()
    queue.get()
    print 'finished: ' + url

def main_loop():
    file_list = get_file_list(FILE_PATH)
    thread_list = []
    for file in file_list: 
        dir = HTML_FILE_PATH + file
        if not isdir(dir):
            os.mkdir(dir)
        file = FILE_PATH + '/' + file
        with open(file, 'r') as fp:
            for url in fp.readlines():
                url = url.strip()
                if url in EMPTY_LINE:
                    continue
                url = url[1:-1]
                url = "http://" + url
                url = "\"" + url + "\""
                file_name = str(abs(hash(url + str(time.clock())))) + str(random.random())      
                file_name = dir + '/' + file_name + '.txt'
                file_name= "\"" + file_name + "\""
                thread_item = threading.Thread(target=sub_process, args=(url, file_name))
                thread_list.append(thread_item)
                queue.put(url)
                thread_item.start()
                global count
                count += 1
                print count
    for item in thread_list:
        item.join()
    print "finished"

def main():
#     main_loop()
    url = '\"http://qidian.cn/wap2/book/book.do?order=&page=4&cpage=1&categoryid=70&bookid=1294670&sid=;;;;0\"'
    file_name = '/home/mlliu/Desktop/html/select_qidian/60632595253433675700.22381903979.txt'
    sub_process(url, file_name)


if __name__ == '__main__':
    main()
