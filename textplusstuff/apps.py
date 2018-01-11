from django.apps import AppConfig


class TextPlusStuffAppConfig(AppConfig):
    name = 'textplusstuff'
    verbose_name = "Text Plus Stuff"

    def ready(self):
        from .registry import findstuff, stuff_registry
        findstuff()
