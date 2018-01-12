from django.apps import AppConfig
import logging

django_log = logging.getLogger('django.server')


class TextPlusStuffAppConfig(AppConfig):
    name = 'textplusstuff'
    verbose_name = "Text Plus Stuff"
