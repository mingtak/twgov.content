#-*- coding:utf-8 -*-
from zope.interface import Interface
from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContentTitle, IBelowContentBody, IHtmlHeadLinks
#from plone import api
#from random import choice
#from plone.memoize import ram
#from time import time

#設定viewlet介面、pt檔目錄
grok.context(Interface)
grok.templatedir('templates')


class AdditionalMetaData(grok.Viewlet):

    grok.viewletmanager(IHtmlHeadLinks)

    def available(self):
        return True

    """
    @ram.cache(lambda *args: time() // (60 * 60))
    def getRandomImage(self):
        context = self.context
        catalog = self.portal_catalog
        brain = catalog({'Type':'Image', 'path':'twGovBidding/system/social_images'})
        import pdb; pdb.set_trace()
        if brain:
            item = choice(brain)
            return item.getURL()
        else:
            return ''
    """


class GoogleAdAboveTitle(grok.Viewlet):

    grok.viewletmanager(IAboveContentTitle)

    def available(self):
        return True


class GoogleAdBelowContentBody(grok.Viewlet):

    grok.viewletmanager(IBelowContentBody)

    def available(self):
        return True


#下列可再新增viewlet, 可用的interface可查詢 plone.app.layout
