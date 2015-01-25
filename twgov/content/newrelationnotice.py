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
from twgov.content.govnotice import IgovNotice
from plone.indexer import indexer
from collective import dexteritytextindexer
from Products.CMFPlone.utils import safe_unicode

class INewRelationNotice(form.Schema, IImageScaleTraversable):

    noticeId = schema.TextLine(
        title=_(u'Notice ID'),
        required=True,
    )

    noticePublishedDate = schema.Datetime(
        title=_(u'Notice publish date'),
        required=False,
    )

    noticeMethod = schema.TextLine(
        title=_(u'Notice Method'),
        required=False,
    )

    authorityName = schema.TextLine(
        title=_(u'Authority Name'),
        required=False,
    )

    noticeBudget = schema.TextLine(
        title=_(u'Notice Budget'),
        required=False,
    )

    awardCategories = schema.TextLine(
        title=_(u'Award categories'),
        required=False,
    )

    awardMethod = schema.TextLine(
        title=_(u'Award Method'),
        required=False,
    )

    winningTenderer = schema.TextLine(
        title=_(u'Winning Tenderer Company Name'),
        required=False,
    )

    awardAmount = schema.TextLine(
        title=_(u'Award Amount'),
        required=False,
    )

    tenderCompanies = schema.TextLine(
        title=_(u'Tender Companies count'),
        required=False,
    )

    noAwardCompaniesName = schema.TextLine(
        title=_(u'No Award Companies Name'),
        required=False,
    )

    noticeUrl = schema.TextLine(
        title=_(u'Notice URL'),
        required=True,
    )

    dexteritytextindexer.searchable('noticeDetail')
    noticeDetail = RichText(
        title=_(u'Notice Detail Information'),
        required=True,
    )


#    form.widget(noticeRelation=AutocompleteMultiFieldWidget)
    noticeRelation = RelationList(
        title=_(u"relation notice"),
        value_type=RelationChoice(
            source=ObjPathSourceBinder(
                object_provides=IgovNotice.__identifier__,
            ),
        ),
        required=False,
    )


class NewRelationNotice(Container):
    grok.implements(INewRelationNotice)


class SampleView(grok.View):
    """ sample view class """

    grok.context(INewRelationNotice)
    grok.require('zope2.View')
    grok.name('view')


@indexer(INewRelationNotice)
def noticePublishedDate_indexer(obj):
     return obj.noticePublishedDate
grok.global_adapter(noticePublishedDate_indexer, name='noticePublishedDate')

@indexer(INewRelationNotice)
def authorityName_indexer(obj):
     return obj.authorityName
grok.global_adapter(authorityName_indexer, name='authorityName')

@indexer(INewRelationNotice)
def winningTenderer_indexer(obj):
     return obj.winningTenderer 
grok.global_adapter(winningTenderer_indexer, name='winningTenderer')

@indexer(INewRelationNotice)
def noAwardCompaniesName_indexer(obj):
     return obj.noAwardCompaniesName
grok.global_adapter(noAwardCompaniesName_indexer, name='noAwardCompaniesName')

@indexer(INewRelationNotice)
def noticeUrl_indexer(obj):
     return obj.noticeUrl
grok.global_adapter(noticeUrl_indexer, name='noticeUrl')

@indexer(INewRelationNotice)
def biddingCompaniesName_indexer(obj):
     if obj.noAwardCompaniesName == u'':
         resultString = safe_unicode(obj.winningTenderer)
     else:
         resultString = safe_unicode(obj.noAwardCompaniesName) + u',' + safe_unicode(obj.winningTenderer)
     return resultString
grok.global_adapter(biddingCompaniesName_indexer, name='biddingCompaniesName')
