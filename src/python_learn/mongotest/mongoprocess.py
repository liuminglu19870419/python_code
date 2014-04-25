# coding: UTF-8
'''
Created on  2014-04-16

@author: mingliu
'''
import pymongo
import time
if __name__ == '__main__':
    host = '10.2.8.219'
#     host = 'localhost'
    conn = pymongo.Connection(host=host, port=27017)
    db = conn.weibo
#     infos = db['infos']
#     hour_startegy = {}
#     cate_strategy = {}
#     for info in db.infos.find({'cid':{'$exists':True}}, {'_id':1, 'cid':1}):
#          ltime = time.localtime(int(info['_id']) / 1000000)
#          category = info['cid']
#          hour_startegy[str(ltime.tm_hour)] = hour_startegy.get(str(ltime.tm_hour), 0) + 1
#          cate_strategy[str(category)] = cate_strategy.get(str(category), 0) + 1
#     for item in sorted(hour_startegy.items(), key=lambda x: int(x[0])):
#         print item
#     print cate_strategy
#     print hour_startegy
#     for item in cate_strategy.items():
#         print item
    key_word = []
    
    infos = db.infos.find({"news.content":{"$regex":"(马航)"}, "eid":{'$exists':True}})
    
    size = 0
    for info in infos:
        size += 1
        count = db.events.find_one({'_id':info['eid'], 'count':{'$exists':True}})
        if count != None:
            print '%s-%s-%s:%s, eid %s count %s' % (time.localtime(info['_id'] / 1000000).tm_year, \
            time.localtime(info['_id'] / 1000000).tm_mon, \
            time.localtime(info['_id'] / 1000000).tm_mday, \
            time.localtime(info['_id'] / 1000000).tm_hour, \
            info['eid'], \
            count['count']
           )
        print info['news']['title']
    print size

#    for u in db.infos.find({"did":{"$lt":1005}}).limit(10).sort([('cid', pymongo.ASCENDING), ('did', pymongo.ASCENDING)]):#select limit sort
#        print u
#
#    for u in db.infos.find({"did":677}):
#        print u
#    for i in range(1000):
#        db.test.save({"foo":True, "num":i})
#     results = db.test.find({"$or":[{"num":{"$in":[2,3,4], "$lt":4}}, {"num":{"$gte":990}}]}, {"num":1, "_id":0})
#     for result in results:
#         print result
   # start = time.time()
#    db.test.remove()
   # end = time.time() - start
   # print end
    conn.close()
