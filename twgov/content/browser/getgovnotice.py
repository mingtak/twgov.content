# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from Products.Five.browser import BrowserView
import urllib2
from ..config import GOV_NOTICE_URL
from ..config import PCC_DOMAIN
from ..config import TEST_STRING
from ..config import NOTICE_KEYWORDS
from ..config import GET_GOV_NOTICE_LOG_FILE
from ..config import WEB_SITE_URL
from ..config import LOG_MAIL_RECIPIENT
from ..config import LOG_MAIL_SENDER
from ..config import MY_DICT
from ..config import METADATA_KEYWORD_LIST
from plone import api
from random import random, choice, randrange
from datetime import datetime
from mmseg import seg_txt
from Products.CMFPlone.utils import safe_unicode
from plone import namedfile
from plone.namedfile.field import NamedBlobImage
import qrcode
import os
import logging
#import scseg

from jieba.analyse import extract_tags
from jieba import load_userdict
load_userdict(MY_DICT)

import re


class GetGovNotice(BrowserView):
    def __call__(self):
        logger = logging.getLogger(".getgovnotice.GetGovNotice")
        titleLogger = logging.getLogger("分詞案名")
        segLogger = logging.getLogger("分詞結果")
        #取得公告首頁
        try:
            getHtml = urllib2.urlopen(GOV_NOTICE_URL)
        except:
            raise IOError('web site NO Response')
        hrefList = list()
        for line in getHtml:
            if TEST_STRING in line:
                href = line.split('href="')[1].split('">')[0]
                hrefList.append('%s%s' % (PCC_DOMAIN, href))
        hrefList.reverse()

        #依連結取得各頁面
        portal = api.portal.get()
        catalog = api.portal.get_tool(name='portal_catalog')
        add_count = 0
        for link in hrefList:
            # 比對 link,或已存在catalog，continue
            if len(catalog(noticeUrl=link)) > 0:
                continue

            try:
                getNoticeHtml = urllib2.urlopen(link)
            except:
                continue
            doc = getNoticeHtml.read()
            soup = BeautifulSoup(doc.decode('utf-8'))

            findT11bTags = soup.findAll('th','T11b')
            #get value
            teststring=list()
            for T11b in findT11bTags:
                if hasattr(T11b.string, 'strip'):
                    T11bString = T11b.string.strip()
                else:
                    T11bString == 'no string in here'
#                teststring.append(T11bString)
#            return str(teststring)
#            if True:
                if T11bString == NOTICE_KEYWORDS[0]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    govDepartment = text
                elif T11bString == NOTICE_KEYWORDS[1]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    govBranch = text
                elif T11bString == NOTICE_KEYWORDS[2]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    govAddress = text
                elif T11bString == NOTICE_KEYWORDS[3]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    contact = text
                elif T11bString == NOTICE_KEYWORDS[4]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    telNo = text
                elif T11bString == NOTICE_KEYWORDS[5]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    faxNo = text
                elif T11bString == NOTICE_KEYWORDS[6]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    emailAddress = text
                elif T11bString == NOTICE_KEYWORDS[7]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    noticeId = text
                elif T11bString == NOTICE_KEYWORDS[8]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    noticeName = text
                elif T11bString == NOTICE_KEYWORDS[9]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    budget = text
                elif T11bString == NOTICE_KEYWORDS[10]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    bidWay = text
                elif T11bString == NOTICE_KEYWORDS[11]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    decideWay = text
                elif T11bString == NOTICE_KEYWORDS[12]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    noticeTimes = text
                elif T11bString == NOTICE_KEYWORDS[13]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    noticeState = text
                elif T11bString == NOTICE_KEYWORDS[14]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    splitText = text.split('/')
                    startDate = (int(splitText[0])+1911,
                                 int(splitText[1]),
                                 int(splitText[2]),)
                elif T11bString == NOTICE_KEYWORDS[15]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    splitText = text.split()
                    splitTextToDate = splitText[0].split('/')
                    splitTextToTime = splitText[1].split(':')
                    endDate = (int(splitTextToDate[0])+1911,
                               int(splitTextToDate[1]),
                               int(splitTextToDate[2]),
                               int(splitTextToTime[0]),
                               int(splitTextToTime[1]),)
                elif T11bString == NOTICE_KEYWORDS[16]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    splitText = text.split()
                    splitTextToDate = splitText[0].split('/')
                    splitTextToTime = splitText[1].split(':')
                    bidDate = (int(splitTextToDate[0])+1911,
                               int(splitTextToDate[1]),
                               int(splitTextToDate[2]),
                               int(splitTextToTime[0]),
                               int(splitTextToTime[1]),)
                elif T11bString == NOTICE_KEYWORDS[17]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    bidAddress = text
                elif T11bString == NOTICE_KEYWORDS[18]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    bidDeposit = text
                elif T11bString == NOTICE_KEYWORDS[19]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    documentSendTo = text
                elif T11bString == NOTICE_KEYWORDS[20]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    companyQualification = text
                elif T11bString == NOTICE_KEYWORDS[21]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    companyAbility = text
                elif T11bString == NOTICE_KEYWORDS[22]:
                    [text for text in T11b.find_next_siblings("td")[0].stripped_strings]
                    organizationCode = text
#            return '%s\n%s\n' % (noticeName,str(endDate))
            #assign value
            contentId = '%s%s' % (str(datetime.now().strftime('%Y%m%d%H%M')), str(randrange(10000000,100000000)))
            try:
                api.content.create(container=portal['gov_notice'],
                                   type='twgov.content.govnotice',
                                   title=noticeName,
                                   id=contentId,
                                   endDate=datetime(endDate[0], endDate[1], endDate[2], endDate[3], endDate[4]))
            except:
                logger.error(' : create content fail, %s' % link)
                continue
#                raise TypeError('endDate is %s ' % str(endDate))
            brain = catalog(id=contentId)
            item = brain[0].getObject()
            try:
                item.govDepartment = govDepartment
                item.govBranch = govBranch
                item.govAddress = govAddress
                item.contact = contact
                item.telNo = telNo
                item.faxNo = faxNo
                item.emailAddress = emailAddress
                item.noticeId = noticeId
                item.noticeName = noticeName
                item.budget = budget
                item.bidWay = bidWay
                item.decideWay = decideWay
                item.noticeTimes = noticeTimes
                item.noticeState = noticeState
                item.startDate = datetime(startDate[0], startDate[1], startDate[2])
                item.bidDate = datetime(bidDate[0], bidDate[1], bidDate[2], bidDate[3], bidDate[4])
                item.bidAddress = bidAddress
                item.bidDeposit = bidDeposit
                item.documentSendTo = documentSendTo
                item.companyQualification = companyQualification
                item.companyAbility = companyAbility
                item.organizationCode = organizationCode
                item.noticeUrl = link
            except:
                logger.error(' url: %s' % link)
                api.content.delete(item)
                continue

            # setting hotPoint, viewPoint, budgetPoint and importantPoint
            if len(organizationCode.split('.')) == 1 and len(organizationCode) < 3:
                item.viewPoint = 90 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(organizationCode.split('.')) == 2:
                item.viewPoint = 75 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(organizationCode.split('.')) == 3:
                item.viewPoint = 60 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(organizationCode.split('.')) == 4:
                item.viewPoint = 52 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(organizationCode.split('.')) >= 5:
                item.viewPoint = 45 + (10 * random() * int(choice(['-1' ,'1'])))
            else:
                item.viewPoint = 45 + (10 * random() * int(choice(['-1' ,'1'])))

            if len(budget) >= 16:
                item.budgetPoint = 45 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(budget) > 12 and len(budget) < 16:
                item.budgetPoint = 90 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(budget) == 12 and int(budget[0]) > 2:
                item.budgetPoint = 80 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(budget) == 12 and int(budget[0]) <= 2:
                item.budgetPoint = 70 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(budget) == 11 and int(budget[0]) > 5:
                item.budgetPoint = 60 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(budget) == 11 and int(budget[0]) <= 5:
                item.budgetPoint = 52 + (10 * random() * int(choice(['-1' ,'1'])))
            elif len(budget) <= 10:
                item.budgetPoint = 45 + (10 * random() * int(choice(['-1' ,'1'])))
            else:
                item.budgetPoint = 45 + (10 * random() * int(choice(['-1' ,'1'])))

            item.hotPoint = (item.viewPoint * 0.5) + (item.budgetPoint * 0.5)
            item.importantPoint = (item.viewPoint + item.budgetPoint + item.hotPoint) / 3

            # setup metadate
            resultsFromNoticeName, subjectFromNoticeName = str(), list()
#            for seg in scseg.seg_keywords(safe_unicode(item.noticeName)):
            for seg in extract_tags(safe_unicode(item.noticeName), 5):
                #去除含數字的seg
                if re.search('\d', seg):
                    continue
                resultsFromNoticeName += "'%s'," % seg
                if len(safe_unicode(seg)) > 2:
                    subjectFromNoticeName.append(seg)
            #輸出分詞結果，供人工分析
            titleLogger.info(item.noticeName.encode('utf-8'))
            segLogger.info(resultsFromNoticeName.encode('utf-8'))
            randomKeyword = choice(METADATA_KEYWORD_LIST)

            item.setSubject([item.noticeName, randomKeyword] + subjectFromNoticeName)
            item.setDescription(u'%s公告，本案採購名稱：「%s」，招標方式為%s，並以%s決標' %
                                (item.govDepartment, item.noticeName, item.bidWay, item.decideWay))

            #設定QR Code
            itemPhysicalPath = item.getPhysicalPath()
            qrCodeContent = '%s, %s/%s/%s' % (item.noticeName, WEB_SITE_URL, itemPhysicalPath[-2], itemPhysicalPath[-1])
            qrCodeImage = qrcode.make(qrCodeContent)
            qrCodeImage.save('/tmp/tmpQrCodeImage.png')
            with open('/tmp/tmpQrCodeImage.png') as tmpQrCodeImage:
                qrCodeImage = tmpQrCodeImage.read()
            item.qrCodeImage = namedfile.NamedBlobImage(data=qrCodeImage, filename=safe_unicode('%s.png' % item.id))

            # exclude from nav and reindex object
            item.exclude_from_nav = True
            item.reindexObject()
            add_count += 1

        api.portal.send_email(recipient=LOG_MAIL_RECIPIENT,
                              sender=LOG_MAIL_SENDER,
                              subject="Play公社回報, govnotice 取得:%s" % add_count,
                              body="Done!",)

        return logger.info(' : OK,this time additional content: %s' % add_count)
