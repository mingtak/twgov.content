# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import safe_unicode


class GetBiddingCompaniesName(BrowserView):

    def __call__(self):
        request = self.request
        context = self.context
        p = int(getattr(request, 'p', 0))
        start=p*100000
        catalog = context.portal_catalog
        brains = catalog({'portal_type':'twgov.content.newrelationnotice'})

        with open('/tmp/GetBiddingCompaniesName.%s' % p, 'w') as file:
            for object in brains[start:start+100000]:
                item = object.biddingCompaniesName.replace(',', ' Facebook\n')
                file.write('%s Facebook\n' % item.encode('UTF-8'))
        return 'OK, Finish!'

