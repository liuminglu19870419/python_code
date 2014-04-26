'''
Created on Apr 7, 2014

@author: mlliu
'''
import time

if __name__ == '__main__':
#     dic = {
#            'key1':'value1',
#            'key2':'value2',
#            'key3':'value3',
#            'key4':'value4',
#            }
#     print len(dic)
#     for key in dic:
#         print key
#     print dic.keys()
#     print dic.values()
#     print dic.items()
# 
#     for key in dic.keys():
#         print key
# 
#     del dic
#     dic = dict(x=1,y=2,z='test')
#     print dic
    
#     event = {u'count': 28, u'lastModify': 1398412967, u'cid': 104, 'duration_time': 578360.5955629349, u'lastId': 504290L, 'infos': [1398412966386297L, 1398317850929234L, 1398303806191769L, 1398293117058273L, 1398249409186684L, 1398249399168037L, 1398248462595075L, 1398236545494963L, 1398154082187414L, 1398084974330560L, 1398067504268002L, 1398064056649188L, 1398050346354681L, 1398048288893342L, 1398040277732488L, 1398037181041408L, 1398036984430357L, 1398033413777442L, 1398033112227581L], u'_id': 487269, u'mids': [487269, 487273, 487279, 489302, 491278, 491300, 492225, 493371, 494079, 495150, 498731]}
#     print time.localtime(1398416562759002 / 1000000)
#     print '****************************************************************************'
#     t = 1398416562759002
#     P_UPDATE_FREQUENCE_BASE = 2
#     for info in event['infos']:
#         print time.localtime(info / 1000000)
#         if info < t:
#             continue
#         else:
#             print info
#     print '****************************************************************************'
#     for i in range(P_UPDATE_FREQUENCE_BASE):
#         to_time = t - i * 60 * 60 * 1000 * 1000
#         from_time = t - (i + 1) * 60 * 60 * 1000 * 1000
#         print time.localtime(to_time / 1000000)
#         print time.localtime(from_time / 1000000)
#         count = 0
#         for info in event['infos']:
#             if info < to_time and info >= from_time:
#                 count += 1
#         print count
#         count = len([info for info in event['infos'] if info <= to_time and info >= from_time])
#         print count
    infos = [1398452962577717L, 1398423738758857L, 1398417784706052L, 1398416154266666L, 1398414370016603L, 1398414214373474L, 1398411225452056L, 1398408116555952L]
    from_time = 1398485210000000    
    to_time = 1398492410000000    
    time = to_time
    P_UPDATE_FREQUENCE_BASE = 1000
    P_UPDATE_TIME_DELTA = 1
    for i in range(P_UPDATE_FREQUENCE_BASE):
        to_time = time - i * 60 * 60 * 1000 * 1000 * P_UPDATE_TIME_DELTA
        from_time = time - (i + 1) * 60 * 60 * 1000 * 1000 * P_UPDATE_TIME_DELTA
        count = len([info for info in infos if info <= to_time and info > from_time ])
        print '%s:%s' % (i, count)
#     for info in infos:
#         print(time.localtime(info/ 1000000))


