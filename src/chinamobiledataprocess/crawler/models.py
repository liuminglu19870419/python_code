'''
Created on 2014-04-05

@author: liuminglu
'''
import multiprocessing
import pika
import logging
import traceback
import time
import json
from selenium.webdriver import PhantomJS
import os
from selenium.selenium import selenium
from chinamobiledataprocess.crawler.daemon import Daemon

_LOGGER = logging.getLogger('crawler')

def reliable_op(fun):
    '''
    auto process the reconnect to rabbitmq
    '''
    def reconnect(*args, **kwargs):
        while True:
            try:
                res = fun(*args, **kwargs)
                return res
            except Exception, err:
                _LOGGER.error('reconnect to rabbitmq')
                self = args[0]
                init_func = getattr(self, "_init")
                init_func()
                time.sleep(5)
    return reconnect

class RabbitmqClient(object):

    _QUEUE_NAME = 'test'

    def __init__(self, rabbit_mq_host):
        self.__rabbit_mq_host = rabbit_mq_host
        self._init()

    def _init(self):
        try:
            self.__rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(self.__rabbit_mq_host))
            self.__rabbitmq_channel = self.__rabbitmq_connection.channel()
            self.__rabbitmq_channel.queue_declare(queue=RabbitmqClient._QUEUE_NAME)
        except Exception, err:
            _LOGGER.error('rabbitmq init error: %s' % err)
            _LOGGER.error(traceback.format_exc())

    @reliable_op
    def get(self):
        method, properties, body = self.__rabbitmq_channel.basic_get(queue=RabbitmqClient._QUEUE_NAME, \
                                                        no_ack=False)
        if method is None or method.NAME == "Basic.GetEmpty":
            _LOGGER.info('empty  message')
            return None
        _LOGGER.debug('get msg %s' % body)
        body = json.loads(body)
        body["__delivery_tag"] = method.delivery_tag
        return body

    @reliable_op
    def ack(self, delivery_tag):
        self.__rabbitmq_channel.basic_ack(delivery_tag=delivery_tag)

    def close(self):
        self.__rabbitmq_connection.close()


def reliable_op_for_phant(fun):
    '''
    maintain the phantomjs process
    '''
    def restart_phantomjs(*args, **kwargs):
        while True:
            try:
                res = fun(*args, **kwargs)
                return res
            except Exception, err:
                _LOGGER.error(err)
                _LOGGER.error(traceback.format_exc())
                self = args[0]

                close_func = getattr(self, 'close')
                try:
                    close_func()
                except Exception, err:
                    _LOGGER.error('quit phantomjs error %s' % err)
                    _LOGGER.error(traceback.format_exc())

                init_func = getattr(self, "_init")
                try:
                    init_func()
                except Exception, err:
                    _LOGGER.error('init phantomjs error %s' % err)
                    _LOGGER.error(traceback.format_exc())
                time.sleep(5)
    return restart_phantomjs

class DownLoadUrl(object):
    '''
    download html by url
    '''
    def __init__(self, phantomjs, phant_port):
        self.__phantomjs = phantomjs
        self.__port = phant_port
        self._init()

    def _init(self):
        self._webdriver = PhantomJS(executable_path=self.__phantomjs, port=self.__port)

    @reliable_op_for_phant
    def get_html(self, url):
        self._webdriver.get(url)
        return self._webdriver.page_source

    def close(self):
        self._webdriver.quit()


class CrawlWorker(object):
    '''
    crawle html worker 
    '''
    def __init__(self, stop_event, rabbit_mq_host, mongo_host, fdfs_conf, phantomjs_path, phantomjs_port):
        selenium.set_timeout(10)
        self.__rabbit_mq_host = rabbit_mq_host
        self.__mongo_host = mongo_host
        self.__fdfs_conf = fdfs_conf
        self.__stop_event = stop_event 
        self.__phantomjs = phantomjs_path
        self.__phantomjs_port = phantomjs_port
        self._init()

    def _init(self):
        '''
        initialize the crawl worker, make the connection to rabbitmq, fdfs, mongodb
        '''
        self._rabbitmq_client = RabbitmqClient(self.__rabbitmq_host)
        self._crawler = DownLoadUrl(self.__phantomjs, port = self.__phantomjs_port)
        

    def stop(self):
        '''
        stop the connections, quit the phantonjs, exit the process
        '''
        self._rabbitmq_client.close()
        self._crawler.close()
    
    def start(self):
        '''
        start the endless loop to process message
        '''
        _LOGGER.info('start work at %s' % os.getpid())
        while True:
            msg = self._rabbitmq_client.get()
            if msg != None:
                self.__process(msg)
            else:
                time.sleep(5)
    
    def __process(self, msg):
        '''
        process the msg
        '''
        if 'url' not in msg:
            _LOGGER.error('un support msg type')
            return
        html = self.__download(msg['url'])
        if html != None:
            self.__save_file(html)
            self.__save_info(msg)
        self._rabbitmq_client.ack(msg['__delivery_tag'])
    
    def __save_file(self, html_buffer):
        '''
        save the html_buffer to fdfs
        '''
        pass

    def __download(self, url):
        '''
        download the rendered html by url
        '''
        html_buffer = self._crawler.get(url)
        if len(html_buffer) < 100:
            return None
        return html_buffer
    
    def __save_info(self, html_info):
        '''
        save the html info to mongodb
        '''
        pass
