from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .signals import (
    construct_RichTextLink_attachments,
    delete_attached_RichTextLink_instances
)

class RichTextLink(models.Model):
    """
    Creates a polymorphic relationship between two model instances:
        1. `parent_content_object`: A model instance with
            a RichTextField (`field`)
        2. `content_object`: A model instance that 'powers'
            a rendition within a RichTextField
    """
    parent_content_type = models.ForeignKey(
        ContentType,
        related_name="richtextlink_parent_link"
    )
    parent_object_id = models.PositiveIntegerField()
    parent_content_object = generic.GenericForeignKey(
        'parent_content_type',
        'parent_object_id'
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(
        'content_type',
        'object_id'
    )
    field = models.CharField(
        _('Field'),
        max_length=50
    )

    class Meta:
        verbose_name = 'Rich Text Content Link'
        verbose_name = 'Rich Text Content Links'

    def __unicode__(self):
        doesnotexist_string = '<DoesNotExist>'
        if self.content_object:
            content_object_string = self.content_object.__str__()[:20]
        else:
            content_object_string = doesnotexist_string

        if self.parent_content_object:
            parent_content_object_string = self.parent_content_object.__str__()[:20]
        else:
            parent_content_object_string = doesnotexist_string

        return "%s -> %s" % (
            parent_content_object_string,
            content_object_string
        )
