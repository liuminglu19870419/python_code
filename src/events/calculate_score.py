'''
Created on: Mar 14, 2014

@author: qwang

This module is for calculating score of events offline.
'''
import math
import pymongo
from datetime import datetime

_CALCULATE_INTERVAL = 24 * 60 * 60 * 1000 * 1000 # seconds
_LATEST_EVENT_INTERVAL = 1 * 24 * 60 * 60 * 1000 * 1000 # 1 day, in seconds

_EVENT_INFO_COUNT_THRESHOLD = 5

def _connect():
    con = pymongo.Connection('127.0.0.1')
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
    infos = db.infos.find({'eid': eid}, {'_id': 1}, sort=[('_id', pymongo.DESCENDING),], limit=1)
    info = infos[0]
    return info['_id']

def _get_event_valid_infos(time, event, db):
    '''
    Get infos dids in event before the given time
    '''
    infos = db.infos.find({'eid': event['_id'], '_id': {'$lte': time}}, {'_id': 1})
    return [info['_id'] for info in infos]

def _get_event_valid_mids(time, event, db):
    '''
    Get event milestones before the given time
    '''
    mids = []
    for mid in event['mids']:
        info = db.infos.find_one({'did': mid}, {'_id': 1})
        if info['_id'] <= time:
            mids.append(mid)
    return mids

def _valid_event(event, time, db):
    '''
    Is valid event:
    1. last modify in 24 hours
    2. infos count lager than threshold
    '''
    last_modify = _get_event_last_modify(event['_id'], db)
    if last_modify < time - _LATEST_EVENT_INTERVAL:
        return False
    # event news count in one day
    count = db.infos.find({'eid': event['_id'], '_id': {'$lte': time, '$gte': time - _LATEST_EVENT_INTERVAL}}).count()
    if count < _EVENT_INFO_COUNT_THRESHOLD:
        return False
    return True

def _get_events(time, max_did, db):
    '''
    Get events and infos in events of the given time by max did
    '''
    # find all events before the given time
    events = db.events.find({'_id': {'$lte': max_did}})
    valid_events = []
    for event in events:
        # get event last modify time
        if _valid_event(event, time, db):
            event['infos'] = _get_event_valid_infos(time, event, db)
            event['mids'] = _get_event_valid_mids(time, event, db)
            valid_events.append(event)
    return valid_events

def _calculate_event_score(event, time):
    '''
    Calculate event score
    '''
    P1 = 1
    P2 = 10
    P3 = 86400 * 1000 * 1000 * 5
    P4 = 10

    meta = {}

    # add score of infos count
    score = 0.0
    info_count = len(event['infos'])
    meta['count'] = info_count
    meta['count_score'] = math.log(info_count, P2)
    if info_count > 0:
        score += P1 * math.log(info_count, P2)
    else:
        raise Exception('Info count is 0 while calculating event score')
    # add score of latest update
    latest_id = max(event['infos'])
    delta = time - latest_id
    meta['delta'] = delta / 1000 / 1000 # detal in seconds
    meta['delta_score'] = P3 / delta
    if delta > 0:
        score += P3 / delta
    # add score of update frequency
    meta['update'] = {}
    for i in range(4):
        to_time = time - i * 6 * 60 * 60 * 1000 * 1000
        from_time = time - (i + 1) * 6 * 60 * 60 * 1000 * 1000
        count = len([info for info in event['infos'] if info <= to_time and info > from_time ])
        meta['update']['%s' % i] = {}
        meta['update']['%s' % i]['count'] = count
        meta['update']['%s' % i]['score'] = P4 * count * (4 - i)
        score += P4 * count * (4 - i)
    return score, meta

def _get_hot_event(events, time, db):
    '''
    Get hot event:
    1. calculate score for all events
    2. get event with highest score and score lager than threadhold
    '''
    hot_event = None
    max_score = 0.0
    for event in events:
        score, meta = _calculate_event_score(event, time)
        db.validEvents.save({
            'eid': event['_id'],
            'time': datetime.utcfromtimestamp(time / 1000 / 1000),
            'score': score,
            'meta': meta,
        })
        if score > max_score:
            max_score = score
            hot_event = event
    return hot_event, max_score

def _process_hot_event(event, score, time, db):
    '''
    Process hot event:
    1. print out hot event
    2. save into database
    '''
    if event is None:
        return
    info = db.infos.find_one({'did': event['_id']})
    print 'Got hot event: %s with score %s' % (event['_id'], score)
    print 'title: %s' % (info['news']['title'].encode('utf-8'))
    print 'count: %s' % len(event['infos'])
    print 'mids count: %s' % len(event['mids'])
    print '#' * 20
    db.hotEvents.save({'eid': event['_id'], '_id': datetime.utcfromtimestamp(time / 1000 / 1000), 'score': score, \
            'title': info['news']['title'], 'event': event, 'count': len(event['infos']), 'midsCount': len(event['mids'])})

def main():
    db = _connect()
    start_time, end_time = _get_start_end_time(db)
    # set start time, start from 2013/10/1
    start_time = 1380585600000000
    time = start_time + _CALCULATE_INTERVAL
    # calculate top events of specific time
    count = 0
    while time < end_time:
        # get max did of given time
        max_did = _get_top_did(time, db)
        # get all events and infos in events of the given time
        events = _get_events(time, max_did, db)
        print time
        print len(events)
        hot_event, score = _get_hot_event(events, time, db)
        _process_hot_event(hot_event, score, time, db)
        count += 1
        time += _CALCULATE_INTERVAL

if __name__ == '__main__':
    main()
