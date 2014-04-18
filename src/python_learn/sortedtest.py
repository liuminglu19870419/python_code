#coding: UTF-8
'''
Created on  2014-04-16

@author: mingliu
'''

if __name__ == '__main__':
    dict = {'key1':3, 'key2':1, 'key3':1}
    items = dict.items()
    print sorted(dict.items(), key=lambda a: a[1]) 