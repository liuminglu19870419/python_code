'''
Created on Nov 26, 2013

@author: fli
'''
import logging
import simplejson
from weibonews.utils.uploader import upload
from weibonews.utils.decorators import perf_logging

_LOGGER  = logging.getLogger("weibonews.dispatcher")

INDEX_SERVER = '10.2.8.170:8081'
_INDEX_URL = "http://%s/relevance/add" % INDEX_SERVER

class IndexResult(object):
    '''
    Index result
    '''

    def __init__(self, response, did):
        # init fields
        self.success = False
        self.duplicated = False
        self.cid = None
        self.eid = None
        self.pid = None
        self.mids = None
        self.nes = None
        # process response
        if response is None or response.status != 200:
            _LOGGER.error("[ServiceAgent] Failed to index doc %s. reponse %s" % (did, response))
            return
        result = simplejson.loads(response.body)
        if result['sta'] == 0:
            _LOGGER.info("[ServiceAgent] index doc %s." % did)
            self.success = True
            self.cid = int(result['cid'])
            self.eid = int(result['eid'])
            self.pid = int(result['pid'])
            mids = result.get('mids', '').split(':')
            self.mids = [int(mid) for mid in mids if len(mid) > 0]
            self.nes = result.get('nes', None)
        elif result['sta'] == 99:
            _LOGGER.info("[ServiceAgent] Failed to index doc, doc %s duplicated with %s." % (did, result['err']))
            self.success = False
            self.duplicated = True
        else:
            _LOGGER.info("[ServiceAgent] Failed to index doc %s. sta: %s. err: %s" % (did, result['sta'], result['err']))

@perf_logging
def index_doc(did, cid, pub_date, title, content):
    '''
    Request remote service to index a document
    Parameters:
        did: id of document to be indexed
        cid: id of category this document belongs
        pub_date: millisecond timestamp when this document published
        title: title of document to be indexed
        content: content of document to be indexed
    Returns:
        success: if this document is indexed
        duplicated: whether or not this document is duplicated with others
        cid: id of category of this document
        eid: if of event this document belongs
        pid: id of parent doc in this event tree
        mids: id list of milestones of this event.
        nes: named entities of this document
    '''
    if isinstance(title, unicode):
        title = title.encode('utf8')
    if isinstance(content, unicode):
        content = content.encode('utf8')
    request_data = {'did':did, 'cid':cid, 'pubDate':pub_date, 'title':title, 'content':content}
    response = upload(_INDEX_URL, request_data)
    return IndexResult(response, did)
