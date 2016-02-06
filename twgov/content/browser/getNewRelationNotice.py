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


GET_HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://web.pcc.gov.tw",
    "Connection": "keep-alive"
}


class GetNewRelationNotice(BrowserView):
    def __call__(self):
        logger = logging.getLogger("getNewRelationNotice.GetNewRelationNotice")
        portal = api.portal.get()
        catalog = api.portal.get_tool(name='portal_catalog')
        #取得公告BDM網址
        dateString = os.popen('date +%Y%m%d').read().strip()
        try:
            getBdmUrl = '%s%s%s' % (GET_BDM_URL_HEAD, dateString, GET_BDM_URL_TAIL)
            execString = 'elinks --dump %s | grep BDM' % getBdmUrl
            getBDM_Urls = os.popen(execString).read()
########
#            logger.info('1111111111111111')
        except:
            raise IOError('web site NO Response')
        #取得所有網址
        urlList = list()
        for url in getBDM_Urls.split('\n'):
            if url.split('/')[-1].strip() == '':
                continue
            bdmUrl = '%s%s%s' % (BDM_URL_HEAD, dateString, BDM_URL_TAIL)
            urlList.append(bdmUrl+url.split('/')[-1])
######## 
#            logger.info('2222222222222222222')
        #處理個別頁面
        intIds = component.getUtility(IIntIds)
        addCount = 0
#############
#        import pdb; pdb.set_trace()
        for pageUrl in urlList:
            try:
                os.system('sleep 1s')
                if len(catalog(noticeUrl=pageUrl)) > 0:
                    logger.info('noticeUrl: %s' % pageUrl)
                    continue

                try:
                    request = urllib2.Request(pageUrl, headers=GET_HEADERS)        
                    pageHtml =  urllib2.urlopen(request).read()
                except:
                    api.portal.send_email(recipient=LOG_MAIL_RECIPIENT,
                        sender=LOG_MAIL_SENDER,
                        subject="Play公社getNewRelationNotice錯誤回報",
                        body="網站無回應或被擋了",)
                    raise IOError('web site NO Response')

                logger.info('date: %s, count: %s, len: %s' % (dateString, addCount, len(pageHtml)))
                soup = BeautifulSoup(pageHtml)
                find_All_T11b = soup.find_all('td', attrs={'class':'T11b', 'align':'left'})
                contentDict = []
                for item in find_All_T11b:
                    attrName = safe_unicode(item.contents[0]).strip()
                    attrValue = safe_unicode(item.find_next_sibling('td').contents[0]).strip()
                    contentDict.append({attrName:attrValue})
                noticeDetail = ''
                noAwardCompaniesName = ''
                noticePublishedDate = datetime(2000,1,1)
                noticeMethod = ''
                authorityName = ''
                noticeBudget = ''
                awardCategories = ''
                awardMethod = ''
                winningTenderer = ''
                awardAmount = ''
                tenderCompanies = ''
                for contentItem in contentDict:
                    item = contentItem.popitem()
                    if item[0] == u'標案名稱':
                        title = item[1]
                    if item[0] == u'標案案號':
                        noticeId = item[1]
                    if item[0] == u'原公告日期':
                        try:
                            year, month, day = item[1].split('/')
                            year = int(year) + 1911
                            month, day = int(month), int(day.split()[0])
                            noticePublishedDate = datetime(year, month, day)
                        except:
                            pass
                    if item[0] == u'招標方式':
                        noticeMethod = item[1]
                    if item[0] == u'機關名稱':
                        authorityName = item[1]
                    if item[0] == u'預算金額':
                        noticeBudget = item[1]
                    if item[0] == u'決標資料類別':
                        awardCategories = item[1]
                    if item[0] == u'決標方式':
                        awardMethod = item[1]
                    if item[0] == u'得標廠商名稱':
                        winningTenderer = item[1]
                    if item[0] == u'決標金額':
                        awardAmount = item[1]
                    if item[0] == u'投標廠商家數':
                        tenderCompanies = item[1]
                    if item[0] == u'未得標廠商名稱':
                        if noAwardCompaniesName == '':
                            noAwardCompaniesName = item[1]
                        elif item[1] not in noAwardCompaniesName:
                            noAwardCompaniesName += ',%s' % item[1]
                    noticeDetail += '<p><strong>%s%s</strong><span>%s</span></p>' % (item[0], safe_unicode('：'), item[1])
                contentId = '%s%s' % (str(datetime.now().strftime('%Y%m%d%H%M')), str(randrange(10000000,100000000)))
                #確認資料庫中有關聯項目
                relatedItems = catalog({'portal_type':'twgov.content.govnotice', 'noticeName':title, 'noticeId':noticeId})
#                if len(relatedItems) == 0:
#                    continue
                api.content.create(container=portal['relation_notice'],
                                   type='twgov.content.newrelationnotice',
                                   title=safe_unicode(u'[決標]:'+title),
                                   id=contentId,
                                   noticeId=noticeId,
                                   noticePublishedDate = noticePublishedDate,
                                   noticeMethod = noticeMethod,
                                   authorityName = authorityName,
                                   noticeBudget = noticeBudget,
                                   awardCategories = awardCategories,
                                   awardMethod = awardMethod,
                                   winningTenderer = winningTenderer,
                                   awardAmount = awardAmount,
                                   tenderCompanies = tenderCompanies,
                                   noAwardCompaniesName = noAwardCompaniesName,
                                   noticeUrl=pageUrl,
                                   noticeDetail = RichTextValue(noticeDetail, 'text/html', 'text/html'),)
                #找關聯
                getSelfBrain = catalog(id=contentId)
                getSelfObject = getSelfBrain[0].getObject()
                getSelfObject.setDescription(u'標案名稱: %s, 招標單位: %s, 得標廠商: %s, 決標金額:%s' %
                                (title, getSelfObject.authorityName, getSelfObject.winningTenderer, getSelfObject.awardAmount))
                try:
                    if len(relatedItems) > 0:
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
                            subjectList = list(relatedItem_Object.Subject()) + list([winningTenderer]) + list(noAwardCompaniesName.split(','))
                            getSelfObject.setSubject(subjectList)
#                            getSelfObject.setSubject(list(relatedItem_Object.Subject()))
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
                              subject="Play公社回報, %s, New-relationnotice 取得:%s" % (dateString, addCount),
                              body='Done, %s' % dateString,)

        return logger.info('新增關聯公告完成，筆數: %s' % addCount)
