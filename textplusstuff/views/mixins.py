from django.utils.functional import Promise

from rest_framework.response import Response
from rest_framework.utils import formatting


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
        model_verbose_name = self.model._meta.verbose_name._proxy____cast()
        if isinstance(model_verbose_name, Promise):
            # Catching ugettext_lazy marked text
            model_name = model_verbose_name._proxy____cast()
        elif isinstance(
            model_verbose_name, str
        ) or isinstance(model_verbose_name, unicode):
            model_name = model_verbose_name
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
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        renditions = dict(
            (
                rendition.short_name,
                {
                    'verbose_name': rendition.verbose_name,
                    'description': rendition.description,
                    'token': "{%% textplusstuff '%(app)s:%(model)s:%(pk)s:%(rend)s' %%}" % {
                        'app': self.model._meta.app_label,
                        'model': self.model._meta.model_name,
                        'pk': unicode(self.object.pk),
                        'rend': rendition.short_name
                    },
                    'path_to_template': rendition.path_to_template
                }
            )
            for rendition in self.renditions
        )
        template = {
            'context': serializer.data,
            'renditions': renditions
        }
        return Response(template)
