from __future__ import unicode_literals

from django.conf import settings
from django.db.models import SubfieldBase, TextField
from django.utils.six import add_metaclass
from django.utils.translation import ugettext_lazy as _

from .datastructures import TextPlusStuff
from .widgets import TextPlusStuffWidget

if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [], [r"^textplusstuff\.fields\.TextPlusStuffField"]
    )


@add_metaclass(SubfieldBase)
class TextPlusStuffField(TextField):

    description = _("Text Plus Stuff Field")

    def get_prep_value(self, value):
        if not isinstance(value, TextPlusStuff):
            value = TextPlusStuff(value)
        return value.raw_text

    def value_to_string(self, obj):
        """
        Prepares this field for serialization.
        """
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def to_python(self, value):
        """
        Takes Markdown-flavored (and TextPlusStuffToken-laden text) and
        returns it as a TextPlusStuff instance.
        """
        if isinstance(value, TextPlusStuff):
            textplusstuff_instance = value
            textplusstuff_instance.field = self.attname
        else:
            textplusstuff_instance = TextPlusStuff(
                raw_text=value, field=self.attname
            )

        return textplusstuff_instance

    def formfield(self, **kwargs):
        formfield = super(TextPlusStuffField, self).formfield(**kwargs)
        formfield.widget = TextPlusStuffWidget(
            attrs={'class': 'vLargeTextField textplusstuff'}
        )
        return formfield

__all__ = ('TextPlusStuffField')
