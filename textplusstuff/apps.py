from django.apps import AppConfig


class TextPlusStuffAppConfig(AppConfig):
    name = 'textplusstuff'
    verbose_name = "Text Plus Stuff"

    def ready(self):
        self.module.autodiscover()
