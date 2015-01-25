# -*- coding: utf-8 -*-
#測試相關功能用
from bs4 import BeautifulSoup
from Products.Five.browser import BrowserView
import urllib2
from ..config import GOV_NOTICE_URL
from ..config import PCC_DOMAIN
from ..config import TEST_STRING
from ..config import NOTICE_KEYWORDS
from plone import api
from random import randrange, random, choice
from datetime import datetime


class CheckCode(BrowserView):
    def __call__(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(portal_type='twgov.content.govnotice')
        result = str()
        for brain in brains:
            item = brain.getObject()
            item.viewPoint = random() * 100
            if item.viewPoint < 35.0:
                item.viewPoint += 35.0
            item.budgetPoint = random() * 100
            if item.budgetPoint < 35.0:
                item.budgetPoint += 35.0
            item.hotPoint = item.viewPoint * 0.35 + item.budgetPoint * 0.65
            item.importantPoint = (item.viewPoint + item.budgetPoint + item.hotPoint) / 3
            result += '%s\t%s\t%s\t%s\t%s\n' % (brain.Title.decode('utf-8'),
                                        item.viewPoint,
                                        item.budgetPoint,
                                        item.hotPoint,
                                        item.importantPoint,)
        return result
        
#twgov.content.govnotice
