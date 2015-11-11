from __future__ import unicode_literals
from collections import OrderedDict

from django.conf import settings
from django.db.models import SubfieldBase, TextField
from django.utils.six import add_metaclass
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

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

    def __init__(self, *args, **kwargs):
        self.constructed_field = kwargs.pop('constructed_field', None)

        super(TextPlusStuffField, self).__init__(*args, **kwargs)

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

    def update_constructed_field(self, model_instance):
        """
        Updates field's ppoi field, if defined.

        This method is hooked up this field's pre_save method to update
        the constructed immediately before the model instance (`instance`)
        it is associated with is saved.
        """
        # Nothing to update if the field doesn't have have a constructed field
        if self.constructed_field:
            tps_field_value = getattr(model_instance, self.attname)
            setattr(
                model_instance,
                self.constructed_field,
                tps_field_value.as_json()
            )

    def pre_save(self, model_instance, add):
        "Returns field's value just before saving."
        value = super(TextPlusStuffField, self).pre_save(model_instance, add)
        self.update_constructed_field(model_instance)
        return value


class TextPlusStuffConstructedField(JSONField):
    description = _("Constructed Text Plus Stuff Field")

    def __init__(self, *args, **kwargs):
        load_kwargs = kwargs.pop('load_kwargs', {})
        if 'object_pairs_hook' not in load_kwargs:
            load_kwargs.update({'object_pairs_hook': OrderedDict})
        kwargs['load_kwargs'] = load_kwargs
        default = kwargs.get('default', {})
        kwargs['default'] = default
        super(TextPlusStuffConstructedField, self).__init__(*args, **kwargs)

__all__ = ('TextPlusStuffField', 'TextPlusStuffConstructedField')
