from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import SubfieldBase, TextField
from django.utils.translation import ugettext_lazy as _

from .datastructures import RichText
from .parser import RichTextContentNode

if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [],[r"^richtext\.fields\.RichTextField"]
    )

class RichTextField(TextField):

    description = _("Rich Text")
    __metaclass__ = SubfieldBase

    def get_prep_value(self, value):
        if isinstance(value, RichText):
            richtext_instance = value
        else:
            richtext_instance = RichText(raw_text=value, field=self.attname)

        return richtext_instance.raw_text

    def to_python(self, value):
        """
        Takes Markdown-flavored (and RichTextToken-laden text) and returns it
        as a RichText instance.
        """
        if isinstance(value, RichText):
            richtext_instance = value
            richtext_instance.field = self.attname
        else:
            richtext_instance = RichText(raw_text=value, field=self.attname)

        return richtext_instance

__all__ = ('RichTextField')
