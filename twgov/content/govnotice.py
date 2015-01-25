# -*- coding: utf-8 -*-
import logging
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from twgov.content import MessageFactory as _

from plone.indexer import indexer
from collective import dexteritytextindexer

from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog


def back_references(source_object, attribute_name):
    """ Return back references from source object on specified attribute_name """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                            dict(to_id=intids.getId(aq_inner(source_object)),
                                 from_attribute=attribute_name)
                            ):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result


class IgovNotice(form.Schema, IImageScaleTraversable):
    """
    govNotice conttent type
    """
    form.model("models/govnotice.xml")

    govDepartment = schema.TextLine(
        title=_(u'government departments'),
        required=False,
    )

    govBranch = schema.TextLine(
        title=_(u'government branch unit'),
        required=False,
    )

    govAddress = schema.TextLine(
        title=_(u'government branch unit address'),
        required=False,
    )

    contact = schema.TextLine(
        title=_(u'this notice contact'),
        required=False,
    )

    telNo = schema.TextLine(
        title=_(u'telephone number'),
        required=False,
    )

    faxNo = schema.TextLine(
        title=_(u'fax number'),
        required=False,
    )

    emailAddress = schema.TextLine(
        title=_(u'contact email address'),
        required=False,
    )

    noticeId = schema.TextLine(
        title=_(u'notice ID'),
        required=False,
    )

    noticeName = schema.TextLine(
        title=_(u'notice name'),
        required=False,
    )

    budget = schema.TextLine(
        title=_(u'notice budget'),
        required=False,
    )

    bidWay = schema.TextLine(
        title=_(u'bid way'),
        required=False,
    )

    decideWay = schema.TextLine(
        title=_(u'decide way'),
        required=False,
    )

    noticeTimes = schema.TextLine(
        title=_(u'number of notice times'),
        required=False,
    )

    noticeState = schema.TextLine(
        title=_(u'notice state'),
        required=False,
    )

    startDate = schema.Datetime(
        title=_(u'notice start date'),
        required=False,
    )

    endDate = schema.Datetime(
        title=_(u'notice end date'),
        required=True,
    )

    bidDate = schema.Datetime(
        title=_(u'notice bid date'),
        required=False,
    )

    bidAddress = schema.TextLine(
        title=_(u'notice bid address'),
        required=False,
    )

    bidDeposit = schema.TextLine(
        title=_(u'bid deposit'),
        required=False,
    )

    documentSendTo = schema.TextLine(
        title=_(u'bid document send to'),
        required=False,
    )

    companyQualification = schema.Text(
        title=_(u'company qualification'),
        required=False,
    )

    companyAbility = schema.Text(
        title=_(u'company ability to basic qualifications'),
        required=False,
    )

    noticeUrl = schema.TextLine(
        title=_(u'notice url address'),
        required=False,
    )

#    form.mode(organizationCode='hidden')
    organizationCode = schema.TextLine(
        title=_(u"organization Code"),
        required=False,
    )

    form.mode(hotPoint='hidden')
    hotPoint = schema.Float(
        title=_(u"hot point"),
        required=False,
    )

    form.mode(viewPoint='hidden')
    viewPoint = schema.Float(
        title=_(u"view point"),
        required=False,
    )

    form.mode(budgetPoint='hidden')
    budgetPoint = schema.Float(
        title=_(u"budget point"),
        required=False,
    )

    form.mode(importantPoint='hidden')
    importantPoint = schema.Float(
        title=_(u"important point"),
        required=False,
    )

    qrCodeImage = NamedBlobImage(
        title=_(u"QR Code Image"),
        required=False,
    )

    #setting full text search field
    dexteritytextindexer.searchable('govDepartment')


class govNotice(Container):
    grok.implements(IgovNotice)

    # Add your class methods and properties here


class SampleView(grok.View):
    grok.context(IgovNotice)
    grok.require('zope2.View')
    grok.name('view')
    '''
    def findBackReferences(self):
        backReferences = list()
        if self.context.noticeRelation is None:
            return backReferences
        for i in range(len(self.context.noticeRelation)):
            backReferences += back_references(self.context.noticeRelation[i].to_object, 'noticeRelation')
        backReferences = list(set(backReferences))
        for i in range(len(backReferences)-1, -1, -1):
            if self.context == backReferences[i]:
                backReferences.pop(i)
        return backReferences
    '''
    def findBackReferences(self):
        logger = logging.getLogger("findBackReferences")
        backReferences = back_references(self.context, 'noticeRelation')
        return backReferences


@indexer(IgovNotice)
def noticeUrl_indexer(obj):
     return obj.noticeUrl
grok.global_adapter(noticeUrl_indexer, name='noticeUrl')

@indexer(IgovNotice)
def noticeId_indexer(obj):
     return obj.noticeId
grok.global_adapter(noticeId_indexer, name='noticeId')

@indexer(IgovNotice)
def noticeName_indexer(obj):
     return obj.noticeName
grok.global_adapter(noticeName_indexer, name='noticeName')

@indexer(IgovNotice)
def govDepartment_indexer(obj):
     return obj.govDepartment
grok.global_adapter(govDepartment_indexer, name='govDepartment')

@indexer(IgovNotice)
def budget_indexer(obj):
     return obj.budget
grok.global_adapter(budget_indexer, name='budget')

@indexer(IgovNotice)
def bidWay_indexer(obj):
     return obj.bidWay
grok.global_adapter(bidWay_indexer, name='bidWay')

@indexer(IgovNotice)
def endDate_indexer(obj):
     return obj.endDate
grok.global_adapter(endDate_indexer, name='endDate')

@indexer(IgovNotice)
def hotPoint_indexer(obj):
     return obj.hotPoint
grok.global_adapter(hotPoint_indexer, name='hotPoint')

@indexer(IgovNotice)
def viewPoint_indexer(obj):
     return obj.viewPoint
grok.global_adapter(viewPoint_indexer, name='viewPoint')

@indexer(IgovNotice)
def budgetPoint_indexer(obj):
     return obj.budgetPoint
grok.global_adapter(budgetPoint_indexer, name='budgetPoint')






