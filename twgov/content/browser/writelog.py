# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from ..config import PAGE_ACCESS_LOG_FILE
from DateTime import DateTime
from mmseg import seg_txt
import logging
from Products.CMFPlone.utils import safe_unicode

logger = logging.getLogger("Plone")


#write log data to log file
class WriteLog(BrowserView):
    def __call__(self):
        seg = list()
        for i in seg_txt("最主要的更动是：张无忌最后没有选定自己的配偶"):
            j = safe_unicode(i)
            seg.append([j, len(j)])
        logger.info(str(seg))
