# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from Products.Five.browser import BrowserView
import urllib2
from plone import api
from random import random, choice, randrange
from datetime import datetime
#from mmseg import seg_txt
from Products.CMFPlone.utils import safe_unicode
import logging
import os
from ..config import GET_BDM_URL_HEAD, GET_BDM_URL_TAIL
from ..config import BDM_URL_HEAD, BDM_URL_TAIL
from ..config import LOG_MAIL_RECIPIENT, LOG_MAIL_SENDER
from zope import component
from zope.app.intid.interfaces import IIntIds
from plone.app.textfield.value import RichTextValue
#以下3個import，做關聯用
from z3c.relationfield import RelationValue
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class GetRelationNotice(BrowserView):
    def __call__(self):
        logger = logging.getLogger(".getRelationNotice.GetRelationNotice")
        portal = api.portal.get()
        catalog = api.portal.get_tool(name='portal_catalog')
        #取得公告BDM網址
        dateString = os.popen('date +%Y%m%d').read().strip()
        try:
            getBdmUrl = '%s%s%s' % (GET_BDM_URL_HEAD, dateString, GET_BDM_URL_TAIL)
            execString = 'elinks --dump %s | grep BDM' % getBdmUrl
            getBDM_Urls = os.popen(execString).read()
        except:
            raise IOError('web site NO Response')
        #取得所有網址
        urlList = list()
        for url in getBDM_Urls.split('\n'):
            if url.split('/')[-1].strip() == '':
                continue
            bdmUrl = '%s%s%s' % (BDM_URL_HEAD, dateString, BDM_URL_TAIL)
            urlList.append(bdmUrl+url.split('/')[-1])
        #處理個別頁面
        intIds = component.getUtility(IIntIds)
        addCount = 0
        for pageUrl in urlList:
            try:
#                os.system('sleep 1s')
                if len(catalog(noticeUrl=pageUrl)) > 0:
                    continue                
                pageHtml =  urllib2.urlopen(pageUrl).read()
                logger.info(len(pageHtml))
                soup = BeautifulSoup(pageHtml)
                find_All_T11b = soup.find_all('td', attrs={'class':'T11b', 'align':'left'})
                contentDict = []
                for item in find_All_T11b:
                    attrName = safe_unicode(item.contents[0]).strip()
                    attrValue = safe_unicode(item.find_next_sibling('td').contents[0]).strip()
                    contentDict.append({attrName:attrValue})
                noticeDetail = ''
                for contentItem in contentDict:
                    item = contentItem.popitem()
                    if item[0] == u'標案名稱':
                        title = item[1]
                    if item[0] == u'標案案號':
                        noticeId = item[1]
                    noticeDetail += '<p><strong>%s%s</strong><span>%s</span></p>' % (item[0], safe_unicode('：'), item[1])
                contentId = '%s%s' % (str(datetime.now().strftime('%Y%m%d%H%M')), str(randrange(10000000,100000000)))
                #確認資料庫中有關聯項目
                relatedItems = catalog({'portal_type':'twgov.content.govnotice', 'noticeName':title, 'noticeId':noticeId})
                if len(relatedItems) == 0:
                    continue



                api.content.create(container=portal['relation_notice'],
                                   type='twgov.content.relationnotice',
                                   title=safe_unicode(u'[決標]:'+title),
                                   id=contentId,
                                   noticeId=noticeId,
                                   noticeUrl=pageUrl,
                                   noticeDetail = RichTextValue(noticeDetail, 'text/html', 'text/html'),)
                #找關聯
                getSelfBrain = catalog(id=contentId)
                getSelfObject = getSelfBrain[0].getObject()
                try:
                    for relatedItem in relatedItems:
                        relatedItem_Object = relatedItem.getObject()
                        if hasattr(getSelfObject, 'append'):
                            getSelfObject.noticeRelation.append(RelationValue(intIds.getId(relatedItem_Object)))
                            logger.info(pageUrl)
                        else:
                            getSelfObject.noticeRelation = [RelationValue(intIds.getId(relatedItem_Object))]
                        #通知系統，建立反向關聯
                        notify(ObjectModifiedEvent(getSelfObject))
                        #設定subject
                        getSelfObject.setSubject(list(relatedItem_Object.Subject()))
                except:
                    logger.error(pageUrl)
                    pass
                getSelfObject.exclude_from_nav = True
                getSelfObject.reindexObject()
                addCount += 1
            except:
                logger.error('error: %s' % pageUrl)
                pass

        api.portal.send_email(recipient=LOG_MAIL_RECIPIENT,
                              sender=LOG_MAIL_SENDER,
                              subject="Play公社回報, relationnotice 取得:%s" % addCount,
                              body="Done!",)

        return logger.info('新增關聯公告完成，筆數: %s' % addCount)
