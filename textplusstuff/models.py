from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .fields import TextPlusStuffField
# Importing signals into models.py so they'll be
# 'seen' by django.contrib.messages
from .signals import (
    construct_TextPlusStuffLink_attachments,
    delete_attached_TextPlusStuffLink_instances
)


class TextPlusStuffDraft(models.Model):
    """
    A simple model used to hold 'drafts' of TextPlusStuffField
    content.
    """
    title = models.CharField(
        _('Draft Title'),
        max_length=100
    )
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        help_text=_(
            'The user who created this draft.'
        )
    )
    date_created = models.DateTimeField(
        _('Date Created'),
        auto_now_add=True,
        help_text=_('The date this draft was originally created.')
    )
    date_modified = models.DateTimeField(
        _('Date Modified'),
        auto_now=True,
        help_text=_('The date this draft was updated.')
    )
    content = TextPlusStuffField(
        _('Content'),
        blank=True
    )
    content_ported = models.BooleanField(
        _('Content Ported'),
        default=False,
        help_text=_(
            'Signifies whether or not this draft has been used to populate '
            'a TextPlusStuffField on another model.'
        )
    )

    class Meta:
        verbose_name = _('Text Plus Stuff Draft')
        verbose_name_plural = _('Text Plus Stuff Drafts')


@python_2_unicode_compatible
class TextPlusStuffLink(models.Model):
    """
    Creates a polymorphic relationship between two model instances:
        1. `parent_content_object`: A model instance with
            a TextPlusStuffField (`field`)
        2. `content_object`: A model instance that 'powers'
            a rendition within a TextPlusStuffField
    """
    parent_content_type = models.ForeignKey(
        ContentType,
        related_name="textplusstufflink_parent_link"
    )
    parent_object_id = models.PositiveIntegerField()
    parent_content_object = generic.GenericForeignKey(
        'parent_content_type',
        'parent_object_id'
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=25)
    content_object = generic.GenericForeignKey(
        'content_type',
        'object_id'
    )
    field = models.CharField(
        _('Field'),
        max_length=50
    )

    class Meta:
        verbose_name = 'Text Plus Stuff Link'
        verbose_name = 'Text Plus Stuff Links'

    def __str__(self):
        doesnotexist_string = '<DoesNotExist>'
        if self.content_object:
            content_object_string = self.content_object.__str__()[:20]
        else:
            content_object_string = doesnotexist_string

        if self.parent_content_object:
            parent_content_object_string = self.parent_content_object.__str__(
            )[:20]
        else:
            parent_content_object_string = doesnotexist_string

        return "{} -> {}".format(
            parent_content_object_string,
            content_object_string
        )

__all__ = [
    'construct_TextPlusStuffLink_attachments',
    'delete_attached_TextPlusStuffLink_instances',
    'TextPlusStuffDraft',
    'TextPlusStuffLink'
]
