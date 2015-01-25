# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import logging
from plone import api


logger = logging.getLogger("userkeywordlist.py")


class UserKeywordList(BrowserView):

    template = ViewPageTemplateFile('templates/userkeywordlist.pt')

    def __call__(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        #取得plone預設的帳號型態
#-->先暫停：20150125
#-->        ploneUsers = api.user.get_users()
        #cs.auth.facebook產生的id，單獨存在acl_users.cs-facebook-users中，使用portal_membership找不出來
        #使用以下三行撈出facebook型態帳號
        acl_users = api.portal.get_tool(name='acl_users')
        cs_facebook_users = getattr(acl_users, 'cs-facebook-users', '')
        facebookUsers = cs_facebook_users.enumerateUsers()
#        import pdb; pdb.set_trace()

        #結合plone型態帳號與facebook型態帳號
        users = list()
        for fbUser in facebookUsers:
            users.append(fbUser['id'])
#-->        for ploneUser in ploneUsers:
#-->            users.append(unicode(ploneUser.id))

        self.users = []
        for userId in users:
            self.users.append(api.user.get(userid=userId))




        return self.template()
