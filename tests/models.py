from django.db import models

from textplusstuff.fields import TextPlusStuffField


class RegisteredModel(models.Model):
    """
    A simple model used to test textplusstuff.registry.StuffRegistry
    """
    title = models.CharField(
        max_length=90
    )


class TPSTestModel(models.Model):
    content = TextPlusStuffField()
