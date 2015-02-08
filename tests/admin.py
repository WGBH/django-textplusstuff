from __future__ import unicode_literals

from django.contrib import admin

from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

from .models import RegisteredModel, TPSTestModel

admin.site.register(RegisteredModel, TextPlusStuffRegisteredModelAdmin)
admin.site.register(TPSTestModel)
