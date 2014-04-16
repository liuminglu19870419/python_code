'''
Created on: Mar 18, 2014

@author: qwang
'''
import pymongo
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response

con = pymongo.Connection('127.0.0.1')
db = con['weibo']

def index(request):
    hot_events = db.hotEvents.find(sort=[('_id', pymongo.ASCENDING)])
    events = []
    for event in hot_events:
        event['time_str'] = event['_id'].strftime('%Y-%m-%d')
        events.append(event)
    return render_to_response('index.html', {'hot_events': events})

def detail(request):
    query = request.GET
    time_str = query.get('time', None)
    if time_str is None:
        return HttpResponse('time not provided')
    time = datetime.strptime(time_str, '%Y-%m-%d')
    cursor = db.validEvents.find({'time': time}, sort=[('score', pymongo.DESCENDING)])
    events = []
    for event in cursor:
        info = db.infos.find_one({'did': event['eid']}, {'news.title': 1})
        event['title'] = info['news']['title']
        events.append(event)
    return render_to_response('events.html', {'events': events, 'time_str': time_str})
