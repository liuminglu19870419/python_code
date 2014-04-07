'''
Created on 201447

@author: mingliu
'''
import unittest
import pika
import json
from chinamobiledataprocess.crawler import settings
from chinamobiledataprocess.crawler.models import RabbitmqClient, DownLoadUrl
import time
import traceback


class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_SERVER))
        channel = connection.channel()
        channel.queue_declare(queue='test')
 
        for i in range(2):
            msg = {'key1': 'value1',
                   'url': 'http://www.baidu.com'}
            msg = json.dumps(msg)
            channel.basic_publish(exchange='',
            routing_key='test',
            body=msg)
            print msg
        connection.close()

    def testRabbitmqClient(self):
        client = RabbitmqClient(settings.RABBITMQ_SERVER)
        crawler = DownLoadUrl(settings.PHANTOMJS_PATH, 22222)
        while True:
            msg = client.get()
            print msg
            if msg != None:
                url = str(msg['url'])
                print url
                print crawler.get_html(url)
                client.ack(msg['__delivery_tag'])
            time.sleep(0)
            if msg == None:
                break
        client.close()
        crawler.close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()