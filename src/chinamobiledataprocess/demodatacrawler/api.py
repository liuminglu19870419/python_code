'''
Created on 2014-03-25
@author: xiaoluBambi
'''
import os
import sys
import urllib2
import urlparse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding('utf8')


def get_file_list(file_path):
    file_list = []
    for filepath in os.walk(file_path):
        for file in filepath[2]:
#             file = filepath[0] + '/' + file
            file_list.append(file)
    return  file_list


USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17"

def get_html(url):
    u = urlparse.urlparse(url)
    referer = u.scheme + '://' + u.netloc
    headers = {"User-Agent": USER_AGENT, "Referer": referer}
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    if response.code < 300:
        result = ''
        for line in response.readlines():
            line = line.encode('utf-8')
#             print line
            result += line
        return url, response.url, response.msg, result
    else:
        return None, None, None

    
def save_file(file_name, *args):
    fp = open(file_name, 'w')
    for arg in args[0]:
        fp.writelines(arg)
        fp.write("\n")
    fp.flush()
    fp.close()


_DYNAMIC_SCRIPT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download.js')
_TIMEOUT = 30

if __name__ == '__main__':
#     browser = webdriver.Firefox()
    browser = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())
    url = 'http://list.mp3.baidu.com/top/top100.html'
    u = urlparse.urlparse(url)
    try:
        browser.get(url)
        print browser.capabilities
        print browser.find_element_by_tag_name('body').text
        print browser.title
    except Exception, e:
        print e
    finally:
        browser.quit()
    
    
#     f = get_html(url)
