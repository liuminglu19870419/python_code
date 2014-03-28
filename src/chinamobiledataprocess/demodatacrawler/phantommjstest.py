#coding: UTF-8
'''

@author: mingliu
'''
from selenium import webdriver
if __name__ == '__main__':
    driver = webdriver.PhantomJS()
    driver.get('http://www.newsmth.net/bbstcon.php?board=Divorce&gid=203828')
    data = driver.title
    print data
    elem = driver.page_source
    print elem

    driver.quit()