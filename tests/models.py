from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from textplusstuff.fields import TextPlusStuffField


@python_2_unicode_compatible
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

    def __str__(self):
        return "registeredmodel:{}".format(self.pk)


@python_2_unicode_compatible
class TPSTestModel(models.Model):
    content = TextPlusStuffField()

    def __str__(self):
        return "tpstestmodel:{}".format(self.pk)
