# -*- coding: utf-8 -*-
#from bs4 import BeautifulSoup
from Products.Five.browser import BrowserView
#from ..config import GOV_NOTICE_URL
#from ..config import PCC_DOMAIN
#from ..config import TEST_STRING
#from ..config import NOTICE_KEYWORDS
from ..config import PORTAL_DIR, SITE_URL
from ..config import SEND_GOV_NOTICE_LOG_FILE
from plone import api
#from random import randrange
#from datetime import datetime
from DateTime import DateTime
from email.mime.text import MIMEText
from Products.CMFCore.utils import getToolByName
from datetime import datetime
from Products.CMFPlone.utils import safe_unicode
import logging

logger = logging.getLogger(".sendgovnotice.SendGovNotice")


#發送govnotice 給使用者
class SendGovNotice(BrowserView):
    def __call__(self):
        #找前13小時
        start = DateTime() - 0.55
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

        #結合plone型態帳號與facebook型態帳號
        users = list()
        for fbUser in facebookUsers:
            users.append(fbUser['id'])
#-->        for ploneUser in ploneUsers:
#-->            users.append(unicode(ploneUser.id))

        for userId in users:
            user = api.user.get(userid=userId)
#            logger.info('%s\n%s\n%s' % (user.emailaddress, 'get user, ', str(hasattr(user,'emailaddress'))))
            if '@' in user.emailaddress and user.checkedregister is True:
                keywords = []
                userKeywords = getattr(user, 'keywords', '')
                for keyword in userKeywords.split('\n'):
                    if len(keyword.strip()) == 0:
                        continue
                    keywords.append(keyword.strip())
                htmlString = str()
                keywordsList = ''
                for keyword in keywords:
                    keywordsList += ' %s /' % keyword
                    dateRange = {'query':(start,now), 'range': 'min:max'}
                    try:
                        brains = catalog({'portal_type':'twgov.content.govnotice', 'Title':keyword, 'created':dateRange}, sort_on='created')
                    except:
                        continue
                    for brain in brains:
                        if safe_unicode(brain.noticeName) not in safe_unicode(htmlString):
                            url = brain.getPath().replace(PORTAL_DIR, SITE_URL)
                            htmlString += '%s%s%s%s%s%s%s' % (
                                '<li><a href="',
                                url,
                                '">',
                                brain.noticeName.encode('utf-8'),
                                '</a><span>：',
                                brain.govDepartment.encode('utf-8'),
                                '</span></li>',)
#                import pdb; pdb.set_trace()
                if htmlString == str():
                    mimeBody = MIMEText(
                        '''
                        <html><body><h2>今日最新-Play公社,政府採購報馬仔</h2><div>
                        很抱歉，目前沒有您關心的標案內容,<br /><br />
                        <p>
                        您也可以<a href="http://gov.playgroup.com.tw/keywords_setting">前往網站更改設定</a>
                        </p>
                        <p>若您認為收到這封信件是錯誤的，請填寫
                          <a href="http://gov.playgroup.com.tw/system/6211898175338a34">申訴表單</a>，我們將儘速為您處理.
                        </p>
                        </div></body></html>
                        '''
                        , 'html', 'utf-8')
                else:
                    mimeBody = MIMEText('%s%s%s%s%s' % (
                        '''
                        <html><body><h2>今日最新-Play公社,政府採購報馬仔</h2><div>
                          <p>您目前所設定的追蹤關鍵字為：<p><span>
                        '''
                        , keywordsList,
                        '</span></div><ul>',
                        htmlString,
                        '''
                        </ul>
                        <p>你也可以
                          <a href="http://gov.playgroup.com.tw/keywords_setting">前往網站修改設定</a>
                        </p>
                        <p>看到喜歡的廣告點一下，是我們提供服務的最大動力.--Play公社感謝您的支持--</p>
                        <p>若您認為收到這封信件是錯誤的，請填寫
                          <a href="http://gov.playgroup.com.tw/system/6211898175338a34">申訴表單</a>，我們將儘速為您處理.
                        </p></body></html>
                        ''',),
                        'html', 'utf-8')

                try:
                    api.portal.send_email(recipient=user.emailaddress,
                                          sender='service@mingtak.com.tw',
                                          subject='%s%s%s' % (str(user.getProperty("fullname")),
                                                            '您好，Play公社-政府採購公告：',
                                                            str(DateTime()).split()[0]),
                                          body='%s' % (mimeBody.as_string()))
                except:
                    logger.error('send email ERROR!!, %s' % user.emailaddress)
                    pass
                logger.info('send mail OK, to %s' % user.emailaddress)
                logger.info('keywords is => %s' % keywordsList)
            else:
                continue
