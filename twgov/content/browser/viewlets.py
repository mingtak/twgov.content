#-*- coding:utf-8 -*-
from zope.interface import Interface
from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContentTitle, IBelowContentBody

#設定viewlet介面、pt檔目錄
grok.context(Interface)
grok.templatedir('templates')


class GoogleAdAboveTitle(grok.Viewlet):

    grok.viewletmanager(IAboveContentTitle)

    def available(self):
        return True


class GoogleAdBelowContentBody(grok.Viewlet):

    grok.viewletmanager(IBelowContentBody)

    def available(self):
        return True


#下列可再新增viewlet, 可用的interface可查詢 plone.app.layout
