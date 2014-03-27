'''
Created on 2014-03-27

@author: mlliu
'''
from PyQt4 import QtCore
from PyQt4.QtWebKit import QWebFrame, QWebPage
from PyQt4.QtCore import QUrl
import PyQt4
from PyQt4.QtGui import QApplication
import sys
import Queue
from checkbox.properties import Time
import time
import threading

THREAD_COUNT = 20
queue = Queue.Queue(THREAD_COUNT)

HTML_FILE_PATH = '/home/mlliu/Desktop/html/'

class Crawler(QtCore.QObject):
    '''
    classdocs
    '''
    def __init__(self, url, file_name):
        '''
        Constructor
        '''
        QtCore.QObject.__init__(self)
        self.url = url
        self.file_name = file_name

    def get_html(self):
        self.page = QWebPage()
        self.frame = self.page.mainFrame()
        self.connect(self.frame, QtCore.SIGNAL('loadFinished(bool)'), self.save)
        self.frame.load(QUrl(self.url))
        print self.file_name

    def save(self, bool):
        cur_url = self.frame.url()
        html = self.frame.toHtml()
        fp = open(self.file_name, 'w')
        fp.write(str(html))
        fp.flush()
        fp.close()
        sys.exit(0)

app = QApplication(sys.argv)

def terminate():
    time.sleep(15)
    app.exit()
    sys.exit(0)

def main():
    crawler = Crawler(sys.argv[1] ,sys.argv[2])
    crawler.get_html()
    threading.Thread(target=terminate).start()
    app.exec_()
    
if __name__ == '__main__':
    main()
        
        
    