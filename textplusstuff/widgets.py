from __future__ import unicode_literals

from django.forms.util import flatatt
from django.forms.widgets import Textarea
from django.utils.encoding import force_text
from django.utils.html import format_html

from .datastructures import TextPlusStuff


class TextPlusStuffWidget(Textarea):

    def render(self, name, value, attrs=None):
        value = value or ''
        if isinstance(value, TextPlusStuff):
            value = value.raw_text
        final_attrs = self.build_attrs(attrs, name=name)
        return format_html('<textarea{0}>\r\n{1}</textarea>',
                           flatatt(final_attrs),
                           force_text(value))
