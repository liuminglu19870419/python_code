'''
Created on: Mar 14, 2014

@author: qwang

This module is for calculating score of events offline.
'''
import math
import pymongo
import time as timer
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import temp
import logging

_EVENT_INFO_COUNT_THRESHOLD = 5
_EVENT_MODIFY_COUNT = 5
_OUT_EVENTS_COUNT = 10
_EVENT_TIME_LINE = 12 * 60 * 60  # only the event modified after this time line will be calc
_TRAIN_INFO_TIME_LINE = 5 * 24 * 60 * 60  # only the info happened after this time line will be calc
_TRAIN_MID_TIME_LINE = 14 * 24 * 60 * 60  # only the mid happened after this time line will be calc
mails = ['mlliu@bainainfo.com', 'fli@bainainfo.com', 'qwang@bainainfo.com', 'jzheng@bainainfo.com', \
          'jwang@bainainfo.com', 'lzhang@bainainfo.com', 'prong@bainainfo.com', 'yyu@bainainfo.com', \
          'yfjiang@bainainfo.com', 'zxzhang@bainainfo.com']
_LOGGER = logging.getLogger("test")
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.addHandler(logging.StreamHandler())

def _connect(host):
    con = pymongo.Connection(host)
    return con['weibo']

def _get_start_end_time(db):
    '''
    Get start calculate time, return value in seconds
    '''
    # get start time
    infos = db.infos.find({}, {'_id': 1}, sort=[('_id', pymongo.ASCENDING)], limit=1)
    info = infos[0]
    start_time = info['_id']
    # get end time
    infos = db.infos.find({}, {'_id': 1}, sort=[('_id', pymongo.DESCENDING)], limit=1)
    info = infos[0]
    end_time = info['_id']
    return start_time, end_time

def _get_top_did(time, db):
    '''
    Get max did of the given time
    '''
    infos = db.infos.find({'_id': {'$lte': time}}, {'did': 1}, sort=[('_id', pymongo.DESCENDING)], limit=1)
    max_did = infos[0]['did']
    return max_did

def _get_event_last_modify(eid, db):
    '''
    Get last modify time of the given event
    '''
    infos = db.infos.find({'eid': eid}, {'_id': 1}, sort=[('_id', pymongo.DESCENDING), ], limit=1)
    info = infos[0]
    return info['_id']

def _get_event_valid_infos(time, event, db):
    '''
    Get infos dids in event before the given time
    '''
    infos = db.infos.find({'eid': event['_id'], '_id': {'$gte': time}}, {'_id': 1})
    return [info['_id'] for info in infos]

def _get_event_valid_mids(time, event, db):
    '''
    Get event milestones before the given time
    '''
    mids = []
    for mid in event['mids']:
        info = db.infos.find_one({'did': mid}, {'_id': 1})
        if info['_id'] >= time:
            mids.append(mid)
    return mids

def _get_event_duration_time(event, db):
    info = db.infos.find_one({'eid':event['_id']}, sort=[('_id', pymongo.ASCENDING)])
    return timer.time() - info['_id'] / 1000000

def _get_train_modified_events(start_time, db):
    end_time = start_time - _EVENT_TIME_LINE
    start_time = start_time * 1000 * 1000
    end_time = int(end_time * 1000 * 1000)
    infos = db.infos.find({'_id':{'$gte': end_time, '$lte':start_time}, 'eid':{'$exists':True}})
    events = []
    for info in infos:
        events.append(info['eid'])
    events = set(events)
    _LOGGER.debug(events)
    valid_event = []
    for key in events:
        event = {}
        event['_id'] = key
        event['count'] = _get_event_count_train(start_time, event, db)
        if event['count'] < _EVENT_INFO_COUNT_THRESHOLD:
            continue
        end_time = start_time - _TRAIN_INFO_TIME_LINE * 1000 * 1000
        event['infos'] = _get_event_valid_infos_train(start_time, end_time, event, db)
        _LOGGER.debug(len(event['infos']))
        event['cid'] = db.infos.find_one({'eid':key})['cid']
        end_time = start_time - _TRAIN_MID_TIME_LINE * 1000 * 1000
        event['mids'] = _get_event_valid_mids_train(start_time, end_time, event, db)
        event['duration_time'] = _get_event_duration_time_train(start_time, event, db)
        valid_event.append(event)
    return valid_event

def _get_event_valid_infos_train(start_time, end_time, event, db):
    infos = db.infos.find({'_id':{'$gte': end_time, '$lte': start_time}, 'eid':event['_id']})
    return [info['_id'] for info in infos]

def _get_event_valid_mids_train(start_time, end_time, event, db):
    return []

def _get_event_duration_time_train(start_time, event, db):
    info = db.infos.find_one({'eid': event['_id']}, sort=[('_id', pymongo.ASCENDING)])
    _LOGGER.debug(timer.localtime(info['_id'] / 1000000))
    return int(start_time - info['_id'])

def _get_event_count_train(start_time, event, db):
    count = db.infos.find({'_id':{'$lte': start_time}, 'eid':event['_id']}).count()
    _LOGGER.debug(count)
    return count

def _get_modified_events(start_time, db):
    '''
    Get events which changed during the start_time and end_time
    '''
    events = db.events.find({'lastModify': {'$gte': start_time}})
    time = start_time * 1000 * 1000
    valid_events = []
    for event in events:
        event['duration_time'] = _get_event_duration_time(event, db)
        event['infos'] = _get_event_valid_infos(time - _TRAIN_INFO_TIME_LINE * 1000 * 1000, event, db)
        event['mids'] = _get_event_valid_mids(time - _TRAIN_MID_TIME_LINE * 1000 * 1000, event, db)
#         if event['cid'] == 103 or event['cid'] == 104 or event['cid'] == 108:
#             continue
        if len(event['infos']) >= _EVENT_INFO_COUNT_THRESHOLD:
            valid_events.append(event)
    return valid_events

def _calculate_event_score(event, time):
    '''
    Calculate event score
    '''

    time = time * 1000 * 1000
    P_UPDATE_FREQUENCE_WEIGHT_ALPHA = 1.1
    P_UPDATE_FREQUENCE_BASE = 6
    P_UPDATE_TIME_DELTA = 2
    meta = {}

    score = 0.0

    # add score of infos count
    info_count = len(event['infos'])
    total_info_count = event['count']
#     mid_count = len(event['mids'])
    meta['count'] = info_count
    if info_count > 0:
        coffecient = info_count * total_info_count / (event['duration_time'] / 1000000.0)
    else:
        raise Exception('Info count is 0 while calculating event score')

    # add score of update frequency
    meta['update'] = {}
    P_UPDATE_FREQUENCE_BASE = int(_EVENT_TIME_LINE / 60 / 60) * P_UPDATE_FREQUENCE_BASE
    for i in range(P_UPDATE_FREQUENCE_BASE):
        to_time = time - i * 60 * 60 * 1000 * 1000 * P_UPDATE_TIME_DELTA
        from_time = time - (i + 1) * 60 * 60 * 1000 * 1000 * P_UPDATE_TIME_DELTA
        count = len([info for info in event['infos'] if info <= to_time and info > from_time ])
        meta['update']['%s' % i] = {}
        meta['update']['%s' % i]['count'] = count
#         meta['update']['%s' % i]['score'] = count * (P_UPDATE_FREQUENCE_WEIGHT_ALPHA ** (P_UPDATE_FREQUENCE_BASE - i))
        meta['update']['%s' % i]['score'] = count * ((P_UPDATE_FREQUENCE_BASE - i) ** 2)
        score += meta['update']['%s' % i]['score']
    score = coffecient * score
    return score, meta

def _key_cmp(key1, key2):
    if key1[0]['cid'] == key2[0]['cid']:
        if key1[1] > key2[1]:
            return 1
        if key1[1] == key2[1]:
            return 0
        if key1[1] < key2[1]:
            return -1
    if key1[0]['cid'] > key2[0]['cid']:
        return 1
    if key1[0]['cid'] < key2[0]['cid']:
        return -1

def _key_cmp1(key1, key2):
    if key1[0]['cid'] == key2[0]['cid']:
        #####################################################
        if key1[1] > key2[1]:
            return 1
        if key1[1] == key2[1]:
            if key1[0]['count'] > key2[0]['count']:
                return 1
            if key1[0]['count'] < key2[0]['count']:
                return -1
            if key1[0]['count'] == key2[0]['count']:
                return 0
        if key1[1] < key2[1]:
            return -1
        ####################################################
    if temp.category_weight[str(key1[0]['cid'])] > temp.category_weight[str(key2[0]['cid'])]:
        return 1
    if temp.category_weight[str(key1[0]['cid'])] < temp.category_weight[str(key2[0]['cid'])]:
        return -1

def _get_hot_event(events, time):
    '''
    Get hot event:
    1. calculate score for all events
    2. get event with highest score and score lager than threadhold
    '''
    event_list = []
    for event in events:
        score, meta = _calculate_event_score(event, time)
        event_list.append([event, score, meta])
#     sorteditem = sorted(event_list, key=lambda a: a[1], reverse=True)
    cids = {}
    for event in events:
        cid = cids.get(event['cid'], None)
        if cid == None:
            cids[event['cid']] = 1.
        else:
            cids[event['cid']] += 1.
    event_len = len(events)

    for cid in cids.keys():
        weight = math.ceil(_OUT_EVENTS_COUNT * cids[cid] / event_len)
        cids[cid] = weight
        _LOGGER.debug(weight)
    for event in event_list:
        event[1] = event[1] / cids[event[0]['cid']]

    result_event = []
    sorteditem = sorted(event_list, cmp=_key_cmp1, reverse=True)
    current_cid = 0
    for event in sorteditem:
        if event[0]['cid'] != current_cid:
            current_cid = event[0]['cid']
            event_count = 0
        if event_count < cids[current_cid]:
            result_event.append(event)
            event_count += 1
#     result_event = sorted(result_event, key=lambda result:result[1], reverse=True)
    result_event = sorted(result_event, cmp=_key_cmp1, reverse=True)
    _LOGGER.debug('result events count: %s' % len(result_event))
    return result_event

def _process_hot_event(event, score, score_detail, time, db):
    '''
    Process hot event:
    1. print out hot event
    2. save into database
    '''
    if event is None:
        return
    info = db.infos.find_one({'did': event['_id']})
    final_result = 'Got hot event: %s with score %s\n<br>' % (event['_id'], score)
    if score_detail != None:
#         final_result += 'delta_score %s' % (score_detail['delta_score']) + '\tcount score%s \n<br>' % (score_detail['count_score'])
        items = score_detail['update'].items()
        items = sorted(items, key=lambda a: int(a[0]))
        result = ''
        k = 0
#         for item in items:
#             k += 1
#             result += 'timeline level %s, count %s score %s \t' % (item[0], item[1]['count'], item[1]['score'])
#             if k % 2 == 0:
#                 final_result += result + '\n<br>'
#                 result = ''
    new_info = db.infos.find_one({'eid':event['_id']}, sort=[('_id', pymongo.DESCENDING)])
    final_result += 'init title: %s \n<br>' % (info['news']['title'].encode('utf-8'))
    final_result += 'latest title: %s \n<br>' % (new_info['news']['title'].encode('utf-8'))
    final_result += 'count: %s \n<br>' % len(event['infos'])
    final_result += 'mids count: %s\n<br>' % len(event['mids'])
    final_result += 'cid %s ' % event['cid']
    final_result += 'duration time: %s\t total count: %s\n<br>' % (event['duration_time'], event['count'])
    final_result += '#' * 20
    final_result += '\n<br>\r'
    return final_result

def _send_mail(text):
    user = 'reporst@gmail.com'
    passwd = 'reporstP@55'
    for to in mails:
#         to = ';'.join(mails)
        msg = MIMEMultipart('alternative')
        msg['To'] = to
        msg['From'] = 'mlliu<' + user + '>'
        msg[ 'Subject'] = 'host event in %s' % timer.strftime('%Y-%m-%d %H:%M:%S', timer.localtime(timer.time()))
        part = MIMEText(text, 'html', 'utf-8')
        msg.attach(part)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.ehlo()
        s.login(user, passwd)
        s.sendmail(msg['From'], to, msg.as_string())
        s.quit()
   

def main():
    db = _connect(host='10.2.8.219')
    global _EVENT_TIME_LINE
    hour = timer.localtime(timer.time()).tm_hour
    _EVENT_TIME_LINE = _EVENT_TIME_LINE * temp.hour_strategy[str(hour)]
    start_time = int(timer.time())
    while True:
        events = _get_train_modified_events(start_time, db)
        if len(events) <= _EVENT_MODIFY_COUNT:
            _EVENT_TIME_LINE += 60 * 60
            continue
        else:
            break

    for event in events:
        for info in event['infos']:
            _LOGGER.debug(timer.localtime(info / 1000000))
    _LOGGER.debug(start_time)
    sorted_events = _get_hot_event(events, start_time)
    result = ''
    current_cid = 0
    for event in sorted_events:
        if event[0]['cid'] != current_cid:
                current_cid = event[0]['cid']
                result += '*' * 100 + '\n<br>'
        result += _process_hot_event(event[0], event[1], event[2], start_time, db)
        result += '\n<br>'
    print result

    _send_mail(result)

if __name__ == '__main__':
    start = timer.time()
    db = _connect(host='10.2.8.219')
#     _get_train_modified_events(int(start), db)
    main()
    end = timer.time() - start 
    print 'process time: %s' % end
