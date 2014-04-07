'''
Created on 2014-04-05

@author: liuminglu
'''
import logging
from logging import config
import os

PHANTOMJS_PATH = '/home/mingliu/phantomjs'
LOG_PATH = '/home/mingliu/git/python_code/'
FASTDFS_CLIENT_CONF = ''
RABBITMQ_SERVER = 'localhost'
LOGGING = {
    'version': 1,
    'disable_existing_loggers':False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'detail': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'message_only': {
            'format': '%(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': LOG_PATH + '/crawler.log',
            'when': 'D',
            'backupCount' : 30
        },
        'perf':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'message_only',
            'filename': LOG_PATH + '/crawler_perf.log',
            'maxBytes': 30 * 1024 * 1024, # 30MB
            'backupCount' : 30
        },
        'err':{
            'level':'ERROR',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'detail',
            'filename': LOG_PATH + '/crawler.err',
            'when': 'D',
            'backupCount' : 30
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['file', 'err' ],
            'level': 'DEBUG',
        },
        'crawler_perf': {
            'handlers': ['perf'],
            'level': 'DEBUG',
        },
        'default' : {
            'handlers': ['file', 'err' ],
            'level': 'DEBUG',
        },
    }
}

config.dictConfig(LOGGING)
# log = logging.getLogger('crawler')
# log.debug('debug')
# log.info('info')
# log.error('error')
# log1 = logging.getLogger('crawler_perf')
# log1.debug('debug')
# log1.info('info')
# log1.error('error')