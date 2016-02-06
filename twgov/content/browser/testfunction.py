# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
#from ..config import PAGE_ACCESS_LOG_FILE
#from DateTime import DateTime
import logging
#from Products.CMFPlone.utils import safe_unicode
#from plone import api
#import os

logger = logging.getLogger("TESTFUNCTION")

#write log data to log file
class TestFunction(BrowserView):
    def __call__(self):
        import pdb; pdb.set_trace()
        return


        #cs.auth.facebook產生的id，單獨存在acl_users.cs-facebook-users中，使用portal_membership找不出來
        #使用以下三行撈出facebook型態帳號
#        acl_users = api.portal.get_tool(name='acl_users')
#        cs_facebook_users = getattr(acl_users, 'cs-facebook-users', '')
#        facebookUsers = cs_facebook_users.enumerateUsers()

# 用這行找到user object ==>   user = api.user.get(userid=userId)

        catalog = self.context.portal_catalog
        brain = catalog({'portal_type':['twgov.content.newrelationnotice']}, sort_on='id')
#        import pdb; pdb.set_trace()
        count = 0
#        idString = ""
        for item in brain[int(self.request['s']):int(self.request['e'])]:
            count += 1
            if count % 1000 == 0:
                logger.info(count)
            try:
                item.getObject().reindexObject()
            except:
                pass
        return 'start=%s, end=%s\n' % (self.request['s'], self.request['e'])
