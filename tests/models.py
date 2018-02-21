from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from textplusstuff.fields import (
    TextPlusStuffField,
    TextPlusStuffConstructedField
)


class RegisteredModel(models.Model):
    """
    A simple model used to test textplusstuff.registry.StuffRegistry
    """
    title = models.CharField(
        max_length=90
    )

    class Meta:
        verbose_name = _('Registered Model')
        verbose_name_plural = _('Registered Models')

    def __unicode__(self):
        return "registeredmodel:{}".format(self.pk)


class TPSTestModel(models.Model):
    content = TextPlusStuffField(
        constructed_field='content_constructed'
    )
    content_constructed = TextPlusStuffConstructedField()

    def __unicode__(self):
        return "tpstestmodel:{}".format(self.pk)
