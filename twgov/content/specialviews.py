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

from plone.memoize import ram
from time import time

from twgov.content import MessageFactory as _


# Interface class; used to define content-type schema.

class ISpecialViews(form.Schema, IImageScaleTraversable):
    """
    special views, include several page views
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/specialviews.xml to define the content type.

    form.model("models/specialviews.xml")


class SpecialViews(Container):
    grok.implements(ISpecialViews)


class IndexView(grok.View):
    """ sample view class """

    grok.context(ISpecialViews)
    grok.require('zope2.View')
    grok.name('indexview')


class GovNoticeView(grok.View):
    """ sample view class """

    grok.context(ISpecialViews)
    grok.require('zope2.View')
    grok.name('govnoticeview')

    @ram.cache(lambda *args: time() // (60 * 60 * 12))
    def getNoticeList(self):
        context = self.context
        catalog = context.portal_catalog;
        results = catalog(portal_type='twgov.content.govnotice', sort_on='created', sort_order='descending')[:5000]
        return results


class NewsView(grok.View):
    """ sample view class """

    grok.context(ISpecialViews)
    grok.require('zope2.View')
    grok.name('newsview')
