# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import logging
from plone import api


logger = logging.getLogger(".noticeanalytics.ComAnalytics")

class ComAnalytics(BrowserView):

    template = ViewPageTemplateFile('templates/comanalytics.pt')

    def __call__(self):
        return self.template()


logger = logging.getLogger(".noticeanalytics.GovAnalytics")

class GovAnalytics(BrowserView):

    template = ViewPageTemplateFile('templates/govanalytics.pt')

    def __call__(self):
        return self.template()
