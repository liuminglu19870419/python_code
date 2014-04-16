'''
Created on Apr 7, 2014

@author: mlliu
'''

if __name__ == '__main__':
    dic = {
           'key1':'value1',
           'key2':'value2',
           'key3':'value3',
           'key4':'value4',
           }
    print len(dic)
    for key in dic:
        print key
    print dic.keys()
    print dic.values()
    print dic.items()

    for key in dic.keys():
        print key

    del dic
    dic = dict(x=1,y=2,z='test')
    print dic