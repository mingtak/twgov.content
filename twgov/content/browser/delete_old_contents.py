# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from plone import api
#from plone.memoize import ram
#from time import time
import logging
from DateTime import DateTime
#import transaction


class DeleteOldContents(BrowserView):

#    template = ViewPageTemplateFile('templates/delete_old_contents.pt')

    def __call__(self):

        logger = logging.getLogger("Delete_Old_Contents")
        logger.info('Start Delete Old Contents')
        request = self.request
        catalog = self.context.portal_catalog
        if not request.has_key('type') or not request.has_key('date'):
            logger.info('End Delete Old Contents')
            return

        date_range = {
            'query':DateTime('%s 00:00:00' % request['date']),
            'range': 'max',
        }

        brain = catalog({'Type':request['type'],
                         'created':date_range})

        lenBrain = len(brain)
        logger.info('Brain amount: %s' % lenBrain)
        count = 0
        objectList = []
        for item in brain:
            count += 1
            objectList.append(item.id)

#            logger.info('(%s/%s) Delete Content id: %s' % (count, lenBrain, item.id))
#            api.content.delete(obj=item.getObject())
            if count // (int(request['count']) if request.has_key('count') else 1000):
#                logger.info('Finish! End Delete Old Contents.')
                logger.info('Creat List OK.')
                break
#                transaction.commit()
#        transaction.commit()
        folder = brain[0].getObject().aq_parent
        folder.manage_delObjects(objectList)
        logger.info('Finish! End Delete Old Contents.')
        return
