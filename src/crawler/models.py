'''
Created on 2014-04-05

@author: liuminglu
'''
import multiprocessing

class CrawlWorker:
    '''
    crawle html worker 
    '''
    def __init__(self, stop_event, rabbit_mq_host, mongo_host, fdfs_conf):
        self.__rabbit_mq_host = rabbit_mq_host
        self.__mongo_host = mongo_host
        self.__fdfs_conf = fdfs_conf
        self.__stop_event = stop_event 

    def __init(self):
        '''
        initialize the crawl worker, make the connection to rabbitmq, fdfs, mongodb
        '''
        pass
    
    def stop(self):
        '''
        stop the connections, quit the phantonjs, exit the process
        '''
        pass
    
    def start(self):
        '''
        start the endless loop to process message
        '''
        pass
    
    def __save_file(self, html_buffer):
        '''
        save the html_buffer to fdfs
        '''
        pass

    def __download(self,  url):
        '''
        download the rendered html by url
        '''
        pass
    
    def __save_info(self, html_info):
        '''
        save the html info to mongodb
        '''
        pass

    def __get_message(self):
        '''
        get a message from rabbitmq
        '''
        pass
    
    def __process(self, msg):
        '''
        process the msg
        '''
        pass

class Crawler:
    '''
    crawl the html in multi processes
    '''
    def __init__(self, process_count, rabbit_mq_host, mongo_host, fdfs_conf):
        self.__rabbit_mq_host = rabbit_mq_host
        self.__mongo_host = mongo_host
        self.__fdfs_conf = fdfs_conf
        self.__process_count= process_count 
    
    def mp_start(self):
        pass
