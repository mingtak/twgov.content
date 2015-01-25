# -*- coding: utf-8 -*-
from five import grok
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotatable, IAnnotations
from plone import api
import logging


logger = logging.getLogger(".keywordssetting.KeywordsSetting")
class KeywordsSetting(grok.View):
    """Keywords Setting View
    """

    grok.context(IAnnotatable)
    grok.require('zope2.View')
    grok.name('keywords_setting')

    def update(self):
        userItem = api.user.get_current()
        if hasattr(self.request, 'replyto'):
            isEmailString = self.request['replyto']
            if len(isEmailString.split('@')) != 2 or len(isEmailString.split()) != 1 or len(isEmailString.split('@')[1].split('.')) == 1:
                api.portal.show_message(message=u'Email 格式錯誤!!!', request=self.request, type='error')
            else:
                if self.request.has_key('checkedregister'):
                    userItem.checkedregister = True
                else:
                    userItem.checkedregister = False
                    return
                userItem.emailaddress = self.request['replyto']
                userItem.keywords = self.request['keywords']
                api.portal.show_message(message=u'您的設定已經更新', request=self.request)
                #logger.info(self.request['keywords'])
                #logger.info(userItem.keywords)
        return
