# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from plone.memoize import ram
#from time import time


class SitemapRelatedNotice(BrowserView):

    template = ViewPageTemplateFile('templates/sitemap.pt')

#    @ram.cache(lambda *args: time() // (60 * 60 * 12))
    def __call__(self):
        request = self.request
        catalog = self.context.portal_catalog
        self.brain = catalog({'portal_type':['twgov.content.newrelationnotice',],
                              'review_state':'published'},
                              sort_on='modified',
                              sort_order='reverse')[:50000]
        return self.template()


class SitemapGovNotice(BrowserView):

    template = ViewPageTemplateFile('templates/sitemap.pt')

#    @ram.cache(lambda *args: time() // (60 * 60 * 12))
    def __call__(self):
        request = self.request
        catalog = self.context.portal_catalog
        self.brain = catalog({'portal_type':['twgov.content.govnotice',],
                              'review_state':'published'},
                              sort_on='modified',
                              sort_order='reverse')[:50000]
        return self.template()


class SitemapDocAndNews(BrowserView):

    template = ViewPageTemplateFile('templates/sitemap.pt')

#    @ram.cache(lambda *args: time() // (60 * 60 * 12))
    def __call__(self):
        request = self.request
        catalog = self.context.portal_catalog
        self.brain = catalog({'portal_type':['Document', 'News Item', 'Event'],
                              'review_state':'published'},
                              sort_on='modified',
                              sort_order='reverse')[:50000]
        return self.template()
