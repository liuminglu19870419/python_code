#coding: UTF-8
'''
Created on  2014-04-18

@author: mingliu
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def email(address, subject, content):
    user = 'reporst@gmail.com'
    passwd = 'reporstP@55'
    to = ';'.join(address)
    msg = MIMEMultipart('alternative')
    msg['To'] = to
    msg['From'] = 'Push Monitor<'+user+'>'
    msg['Subject'] = subject
    part = MIMEText(content, 'html', 'utf-8')
    msg.attach(part)
    print 'send email 1'
    s = smtplib.SMTP('smtp.gmail.com',587)
    print 'send email 2'
    s.starttls()
    print 'send email 3'
    s.ehlo()
    print 'send email 4'
    s.login(user, passwd)
    print 'send email 5'
    s.sendmail(user, address, msg.as_string())
    print 'send email 6'
    s.quit()
    print 'send email 7'

if __name__ == '__main__':
    email('mlliu@bainainfo.com','test', 'test')