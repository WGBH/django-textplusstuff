from __future__ import unicode_literals

from django.contrib import admin

from .models import TextPlusStuffDraft
from .registry import get_modelstuff_renditions


class TextPlusStuffRegisteredModelAdmin(admin.ModelAdmin):
    change_form_template = 'textplusstuff/change_form_with_renditions.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, admin.utils.unquote(object_id))
        rendition_dict = get_modelstuff_renditions(obj) or {}
        rendition_list = [
            rendition
            for short_name, rendition in rendition_dict.items()
        ]
        extra_context = extra_context or {}
        if rendition_dict:
            extra_context.update({
                'textplusstuff_rendition_list': rendition_list
            })
        return super(TextPlusStuffRegisteredModelAdmin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context
        )


admin.site.register(TextPlusStuffDraft)
