'''
Created on: Mar 18, 2014

@author: qwang
'''
from django.http import HttpResponse

def index(request):
    return HttpResponse('hello')
