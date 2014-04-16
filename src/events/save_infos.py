import simplejson
import pymongo

con = pymongo.Connection('127.0.0.1')
db = con['weibo']

f = open('infos.json', 'r')

count = 0
for line in f:
    try:
        info = simplejson.loads(line)
        db.infos.save(info)
        count += 1
        if count % 100 == 0:
            print count
    except Exception, err:
        print err
