'''
Created on Apr 7, 2014

@author: mlliu
'''
from multiprocessing import Process
import os
import sys

from chinamobiledataprocess.crawler import settings
from chinamobiledataprocess.crawler.daemon import Daemon, daemon_main
from chinamobiledataprocess.crawler.models import CrawlWorker


class Crawler(Daemon):
    '''
    crawl the html in multi processes
    '''
    def __init__(self, pidfile, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull):
        super(Crawler, self).__init__(pidfile, stdin, stdout, stderr)

        self.__rabbit_mq_host = settings.RABBITMQ_SERVER 
        self.__mongo_host = settings.MONGO_HOST 
        self.__mongo_port = settings.MONGO_PORT
        self.__fdfs_conf =  settings.FASTDFS_CLIENT_CONF
        self.__process_count = settings.PROCESS_COUNT 
        self.__phantomjs = settings.PHANTOMJS_PATH
    
    def run(self):
        crawler_workers = [] 
        for i in range(self.__process_count):
            crawle_worker = CrawlWorker(stop_event=None, rabbit_mq_host=self.__rabbit_mq_host, mongo_host=self.__mongo_host, \
                                        fdfs_conf=self.__fdfs_conf, phantomjs_path=self.__phantomjs, phantomjs_port= 9090 + i)
            process_item = Process(target=crawle_worker.start)
            crawler_workers.append(process_item)

        for item in crawler_workers:
            item.start() 
        
        for item in crawler_workers:
            item.join()

if __name__ == '__main__':
    daemon_main(Crawler,settings.PID_PATH, sys.argv)