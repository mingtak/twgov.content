# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from ..config import PORTAL_DIR, SITE_URL
from ..config import SEND_GOV_NOTICE_LOG_FILE
from plone import api
from DateTime import DateTime
from email.mime.text import MIMEText
from Products.CMFCore.utils import getToolByName
from datetime import datetime
from collections import Counter
import logging


logger = logging.getLogger(".sendrelationitem.SendRelationItem")


#發送govnotice 給使用者
class SendRelationItem(BrowserView):
    def __call__(self):
        #找前1天
        start = DateTime() - 1
        now = DateTime()

        catalog = api.portal.get_tool(name='portal_catalog')
        #取得plone預設的帳號型態
#-->先暫停：20150125
#-->        ploneUsers = api.user.get_users()
        #cs.auth.facebook產生的id，單獨存在acl_users.cs-facebook-users中，使用portal_membership找不出來
        #使用以下三行撈出facebook型態帳號
        acl_users = api.portal.get_tool(name='acl_users')
        cs_facebook_users = getattr(acl_users, 'cs-facebook-users', '')
        facebookUsers = cs_facebook_users.enumerateUsers()

        #結合plone型態帳號與facebook型態的帳號
        users = list()
        for fbUser in facebookUsers:
            users.append(fbUser['id'])
#-->        for ploneUser in ploneUsers:
#-->            users.append(unicode(ploneUser.id))


        #將近期的relationNotice找出來，列出item.noticeRelation, list type
        dateRange = {'query':(start,now), 'range': 'min:max'}
        brains = catalog({'portal_type':'twgov.content.newrelationnotice', 'created':dateRange}, sort_on='created')
        noticeRelationList = []
        for brain in brains:
            item = brain.getObject()
            if item.noticeRelation != None:
                for noticeRelation in item.noticeRelation:
                    noticeRelationList.append(noticeRelation.to_object.id)

        #開始逐個user處理
        for userId in users:
            user = api.user.get(userid=userId)
            if not hasattr(user, 'traceDict'):
                continue
            if '@' not in user.emailaddress or user.checkedregister is False:
                continue
            matchList = []            
            for traceNoticeId in user.traceDict:
                if traceNoticeId in noticeRelationList:
                    matchList.append(traceNoticeId)
            if len(matchList) == 0:
                continue
            urlList = []
            for noticeId in matchList:
                brain = catalog(id=noticeId)
                if len(brain) == 0:
                    continue
                urlList.append((brain[0].getURL(), brain[0].Title))
            #編寫html
            htmlString = '''
                         <html>
                           <head>
                             <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                           </head>
                           <body>
                             <h2>標案追蹤報告-Play公社,政府採購報馬仔</h2>
                             <p>您設定追蹤的標案有最新狀態<p>
                             <ul>
                         '''
            for urlItem in urlList:
                htmlString += '<li><a href=%s>%s</a></li>' % (urlItem[0], urlItem[1])
            htmlString += '''
                             </ul>
                             <p>若您認為收到這封信件是錯誤的，請填寫
                               <a href="http://gov.playgroup.com.tw/system/6211898175338a34">申訴表單</a>，我們將儘速為您處理.
                             </p>
                           </body></html>
                          '''
            mimeBody = MIMEText(htmlString, 'html', 'utf-8')
            #寄發email
            api.portal.send_email(recipient=user.emailaddress,
                                  sender='service@mingtak.com.tw',
                                  subject='%s%s%s' % (str(user.getProperty("fullname")),
                                                    '您好，Play公社-標案追蹤報告：',
                                                    str(DateTime()).split()[0]),
                                  body='%s' % (mimeBody.as_string()))
            logger.info('已寄出標案追蹤報告：%s' % user.emailaddress)
