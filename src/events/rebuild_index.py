'''
Created on: Mar 12, 2014

@author: qwang
'''
import sys
sys.path.append('/home/qwang/workspace/DolphinNews/weibonews')

import logging
import pymongo
import simplejson

from weibonews.utils.format import clean_content

from serviceagent import index_doc

def set_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    sh = logging.StreamHandler()
    sh.setLevel(level)
    logger.addHandler(sh)
    return logger

def _process_index_result(info_id, result, db):
    '''
    process index result, save event related infos
    '''
    if not result.success or result.cid is None or result.eid is None or result.pid is None:
        return
    # update events related infos into infos
    db.infos.update({'_id': info_id}, {'$set': {'cid': result.cid, 'eid': result.eid, 'pid': result.pid}})
    # save events
    event = {
        'cid': result.cid,
        'mids': result.mids
    }
    db.events.update({'_id': result.eid}, {'$set': event, '$inc': {'count': 1}}, upsert=True)

def main():
    con = pymongo.Connection('127.0.0.1')
    db = con['weibo']

    set_logger('weibonews.dispatcher')
    f = open('infos.json', 'r')
    for line in f:
        try:
            info = simplejson.loads(line)
            if info['type'] != 0:
                continue
            if 'news' not in info or 'content' not in info['news'] or not info['news']['content']:
                continue
            content = clean_content(info['news']['content'])
            result = index_doc(info['did'], info['category'], info['pubDate'], info['news']['title'], content)
            if result.success:
                _process_index_result(info['_id'], result, db)
        except Exception, err:
            print 'Exception: %s, line: %s' % (err, line)

    f.close()

main()
