from __future__ import unicode_literals

try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt  # Django 1.6.x
from django.forms.widgets import Textarea
from django.utils.encoding import force_text
from django.utils.html import format_html

from .datastructures import TextPlusStuff


class TextPlusStuffWidget(Textarea):

    def render(self, name, value, attrs=None):
        value = value or ''
        if isinstance(value, TextPlusStuff):
            value = value.raw_text
        final_attrs = self.build_attrs(attrs)
        final_attrs['rows'] = '10'
        final_attrs['name'] = name
        final_attrs['cols'] = '40'
        final_attrs['class'] = 'vLargeTextField textplusstuff'

        return format_html('<textarea{0}>\r\n{1}</textarea>',
                           flatatt(final_attrs),
                           force_text(value))
