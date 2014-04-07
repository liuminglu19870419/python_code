#coding: UTF-8
'''

@author: mingliu
'''
from selenium import webdriver
if __name__ == '__main__':
    driver = webdriver.PhantomJS('/home/mingliu/phantomjs')
    driver.get('http://www.baidu.com')
    data = driver.title
    print data
    elem = driver.page_source
    print elem

    driver.quit()