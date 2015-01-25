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
from plone.formwidget.contenttree import PathSourceBinder
from plone.formwidget.contenttree import ObjPathSourceBinder

from twgov.content import MessageFactory as _

from twgov.content.govnotice import IgovNotice
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget


class IRelationNotice(form.Schema, IImageScaleTraversable):
    noticeId = schema.TextLine(
        title=_(u'Notice ID'),
        required=True,
    )

    noticeDetail = RichText(
        title=_(u'Notice Detail'),
        required=True,
    )

    noticeUrl = schema.TextLine(
        title=_(u'Notice URL'),
        required=True,
    )

    form.widget(noticeRelation=AutocompleteMultiFieldWidget)
    noticeRelation = RelationList(
        title=_(u"relation notice"),
        value_type=RelationChoice(
            source=ObjPathSourceBinder(
                object_provides=IgovNotice.__identifier__,
            ),
        ),
        required=False,
    )


class RelationNotice(Container):
    grok.implements(IRelationNotice)


class SampleView(grok.View):
    grok.context(IRelationNotice)
    grok.require('zope2.View')
    grok.name('view')
