# coding: UTF-8
'''
Created on  2014-04-16

@author: mingliu
'''
import pymongo
import time
if __name__ == '__main__':
    host = '10.2.8.219'
    host = 'localhost'
    conn = pymongo.Connection(host=host, port=27017)
    db = conn.weibo
    infos = db['infos']
#    for u in db.infos.find({"did":{"$lt":1005}}).limit(10).sort([('cid', pymongo.ASCENDING), ('did', pymongo.ASCENDING)]):#select limit sort
#        print u
#
#    for u in db.infos.find({"did":677}):
#        print u
#    for i in range(1000):
#        db.test.save({"foo":True, "num":i})
    results = db.test.find({"$or":[{"num":{"$in":[2,3,4], "$lt":4}}, {"num":{"$gte":990}}]}, {"num":1, "_id":0})
    for result in results:
        print result
   # start = time.time()
#    db.test.remove()
   # end = time.time() - start
   # print end
    conn.close()
