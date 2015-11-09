from __future__ import unicode_literals
from collections import OrderedDict

from django.utils.functional import Promise

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import formatting

from .renderers import TextPlusStuffBrowsableAPIRenderer


class TextPlusStuffAPIViewMixIn(object):
    renderer_classes = (
        JSONRenderer,
        TextPlusStuffBrowsableAPIRenderer
    )


class TextPlusStuffViewNameMixIn(object):

    def get_view_name(self):
        """
        Return the view name, as used in OPTIONS responses and in the
        browsable API.
        """
        name = self.__class__.__name__
        name = formatting.remove_trailing_string(name, 'View')
        name = formatting.camelcase_to_spaces(name)
        name = name.split(' ')
        model_name = self.model._meta.verbose_name
        if isinstance(model_name, Promise):
            # Catching ugettext_lazy marked text
            model_name = model_name._proxy____cast()
        new_name = [
            name[0],
            model_name,
            name[1]
        ]
        return ' '.join(new_name)


class TextPlusStuffRetrieveModelMixin(object):
    """
    Retrieve a model instance and return a Response 'wrapped'
    in the proper TextPlusStuff response template.
    """

    def retrieve(self, request, *args, **kwargs):
        from ..registry import get_modelstuff_renditions
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        renditions = get_modelstuff_renditions(self.object)
        template = OrderedDict([
            ('context', serializer.data),
            ('renditions', renditions)
        ])
        return Response(template)
