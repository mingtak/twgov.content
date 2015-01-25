# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
import logging


logger = logging.getLogger(".tracenotice.TraceNotice")


#前端點擊「我要追蹤」或「取消追蹤」，處理後端同步
class TraceNotice(BrowserView):
    def __call__(self):
        contentId = self.request.form['id']
        userItem = api.user.get_current()
        if not hasattr(userItem, 'traceDict'):
            userItem.traceDict = {}
        traceDict = getattr(userItem, 'traceDict')
        if traceDict.has_key(contentId):
            userItem.traceDict.pop(contentId)
            userItem.traceDict = userItem.traceDict
#            import pdb; pdb.set_trace()
            return '我要追蹤'
        else:
            userItem.traceDict[contentId] = contentId
            userItem.traceDict = userItem.traceDict
#            import pdb; pdb.set_trace()
            return '取消追蹤'
        return


#頁面一開始要秀追蹤或取消追蹤，這裏給答案
class CheckTraced(BrowserView):
    def __call__(self):
        userItem = api.user.get_current()
        traceDict = getattr(userItem, 'traceDict', {})
        if traceDict.has_key(self.context.id):
            return '取消追蹤'
        else:
            return '我要追蹤'
