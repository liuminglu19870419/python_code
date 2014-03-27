'''
Created on Mar 27, 2014

@author: mlliu
'''
from PyQt4 import QtCore, QtGui, uic
import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from PyQt4.QtWebKit import *
import re
import signal
import sys


reload(sys)  
sys.setdefaultencoding('utf-8')  

class Baidu(QtCore.QObject):
  
    def __init__(self):
        QObject.__init__(self)
        
        self.page = QWebPage()
        #self.webview = QWebView()
        #self.page=self.webview.page()
        self.current = "http://www.yunfan.com/show/mo/3925499320903804626.html"
        self.logged = False 
        self.frame = self.page.mainFrame()     
        QtCore.QObject.connect(self.frame,QtCore.SIGNAL('loadFinished(bool)'),self.do_do)                      
        #self.webview.show()

    def start(self,username,password):
        self.frame.load(QUrl(self.current))

    def do_do(self,bool):
        url = self.frame.url()
        print self.frame.toPlainText()
        sys.exit(0)
#         size = self.page.mainFrame().contentsSize()
#         self.page.setViewportSize(QtCore.QSize(size.width()+16,size.height()))
#         img = QtGui.QImage(size, QtGui.QImage.Format_ARGB32)
#         painter = QtGui.QPainter(img)
#         self.page.mainFrame().render(painter)
#         painter.end()
#         fileName= "shot.png";
#         img.save(fileName)

        print url.toString()
#         print self.frame.
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    baidu = Baidu()
    baidu.start("username","password")
    sys.exit(app.exec_())
