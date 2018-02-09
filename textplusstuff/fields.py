from __future__ import unicode_literals
from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
try:
    from django.core.exceptions import FieldDoesNotExist
except ImportError:
    from django.db.models.fields import FieldDoesNotExist
from django.db.models import TextField
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from .datastructures import TextPlusStuff
from .registry import stuff_registry
from .serializers import TextPlusStuffFieldSerializer
from .widgets import TextPlusStuffWidget


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
        Prepare this field for serialization.
        """
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        if isinstance(value, TextPlusStuff):
            textplusstuff_instance = value
            textplusstuff_instance.field = self.attname
        else:
            textplusstuff_instance = TextPlusStuff(
                raw_text=value, field=self.attname
            )

        return textplusstuff_instance

    def to_python(self, value):
        """
        Take Markdown-flavored (and TextPlusStuffToken-laden text) and
        returns it as a TextPlusStuff instance.
        """
        if isinstance(value, TextPlusStuff):
            textplusstuff_instance = value
            textplusstuff_instance.field = self.attname
        else:
            textplusstuff_instance = TextPlusStuff(
                raw_text=value, field=self.attname
            )

        if value is None:
            textplusstuff_instance = TextPlusStuff(
                raw_text="", field=self.attname
            )

        return textplusstuff_instance

    def formfield(self, **kwargs):
        formfield = super(TextPlusStuffField, self).formfield(**kwargs)
        attrs = formfield.widget.attrs
        attrs.update({'class': 'vLargeTextField textplusstuff'})
        formfield.widget = TextPlusStuffWidget(
            attrs=attrs
        )
        return formfield

    def update_constructed_field(self, model_instance):
        """
        Update field's constructed field, if defined.

        This method is hooked up this field's pre_save method to update
        the constructed immediately before the model instance (`instance`)
        it is associated with is saved.
        """
        # Nothing to update if the field doesn't have have a constructed field
        if self.constructed_field:
            tps_field_value = getattr(model_instance, self.attname)
            if not isinstance(tps_field_value, TextPlusStuff):
                tps_field_value = self.to_python(tps_field_value)

            constructed_value = TextPlusStuffFieldSerializer(
            ).to_representation(
                tps_field_value
            )
            setattr(
                model_instance,
                self.constructed_field,
                constructed_value
            )

    def pre_save(self, model_instance, add):
        """Return the field's value just before saving."""
        value = super(TextPlusStuffField, self).pre_save(model_instance, add)
        if not isinstance(value, TextPlusStuff):
            value = TextPlusStuff(value)
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
        kwargs['editable'] = False
        super(TextPlusStuffConstructedField, self).__init__(*args, **kwargs)


@receiver(post_save)
def update_constructed_fields(sender, instance, **kwargs):
    """
    Rebuild any constructed fields on model instances with a
    TextPlusStuff field.
    """
    if type(instance) in stuff_registry._registry:
        from .models import TextPlusStuffLink
        instance_ct = ContentType.objects.get_for_model(instance)
        to_update_qs = TextPlusStuffLink.objects.filter(
            content_type=instance_ct,
            object_id=instance.pk
        )
        for link_instance in to_update_qs:
            parent_instance = link_instance.parent_content_object
            try:
                tps_field = parent_instance._meta.get_field(
                    link_instance.field
                )
            except FieldDoesNotExist:  # pragma: no cover
                pass
            else:
                if tps_field.constructed_field is not None:
                    parent_instance.save()


__all__ = ('TextPlusStuffField', 'TextPlusStuffConstructedField')
