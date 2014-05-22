from django.conf import settings
from django.db.models import SubfieldBase, TextField
from django.utils.translation import ugettext_lazy as _

from .datastructures import TextPlusStuff

if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [], [r"^textplusstuff\.fields\.TextPlusStuffField"]
    )


class TextPlusStuffField(TextField):

    description = _("Rich Text")
    __metaclass__ = SubfieldBase

    def get_prep_value(self, value):
        if isinstance(value, TextPlusStuff):
            textplusstuff_instance = value
        else:
            textplusstuff_instance = TextPlusStuff(raw_text=value, field=self.attname)

        return textplusstuff_instance.raw_text

    def to_python(self, value):
        """
        Takes Markdown-flavored (and TextPlusStuffToken-laden text) and returns it
        as a TextPlusStuff instance.
        """
        if isinstance(value, TextPlusStuff):
            textplusstuff_instance = value
            textplusstuff_instance.field = self.attname
        else:
            textplusstuff_instance = TextPlusStuff(raw_text=value, field=self.attname)

        return textplusstuff_instance

__all__ = ('TextPlusStuffField')
