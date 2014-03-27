'''

@author: xiaoluBambi
'''
import Queue
import hashlib
import os
from os.path import isdir
import random
import threading
import time
import traceback

from api import get_file_list, save_file, get_html


FILE_PATH = '/home/mlliu/git/python_code/testdata/'
HTML_FILE_PATH = '/home/mlliu/git/python_code/html'
EMPTY_LINE = ['', '\r\n', '\r', '\n']
THREAD_COUNT = 20
queue = Queue.Queue(THREAD_COUNT)
count=0
finish_count=0

def fun(path, file_name, url):
    url = "http://" + url
    file_name = path + '/' + file_name + '.html'
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

def main():
    file_list = get_file_list(FILE_PATH)

    thread_list = []
    for file in file_list: 
        dir = HTML_FILE_PATH + '/' + file
        if not isdir(dir):
            os.mkdir(dir)
        file = FILE_PATH + '/' + file
        with open(file, 'r') as fp:
            for url in fp.readlines():
                url = url.strip()
                if url in EMPTY_LINE:
                    continue

                file_name = str(abs(hash(url + str(time.clock())))) + str(random.random())      
                thread_item = threading.Thread(target=fun, args=(dir, file_name , url))
                queue.put(thread_item)
                global count
                count += 1
                print "read", count
                thread_list.append(thread_item) 
                thread_item.start()
    print "finished"
    for t in thread_list:
        t.join()


if __name__ == '__main__':
    main()
