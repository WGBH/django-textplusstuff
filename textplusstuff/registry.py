import copy

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url, include
from django.utils import six
from django.utils.text import slugify

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy as reverse
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from .exceptions import (
    AlreadyRegistered,
    NotRegistered,
    NonExistantGroup,
    InvalidRenditionType,
    ImproperlyConfiguredStuff
)
from .views import (
    ListStuffView,
    RetrieveStuffView
)

STUFFGROUPS = getattr(settings, 'TEXTPLUSSTUFF_STUFFGROUPS', {})


class Rendition(object):

    def __init__(self, short_name, verbose_name, description,
                 path_to_template, rendition_type='block'):
        self.short_name = slugify(unicode(short_name))
        self.verbose_name = verbose_name
        self.description = description
        self.path_to_template = path_to_template
        if rendition_type not in ['block', 'inline']:
            raise InvalidRenditionType(
                "%s is an invalid rendition_type. Only 'block' "
                "and 'inline' are supported at this time."
            )
        else:
            self.rendition_type = rendition_type

    def render(self, context):
        pass


class Stuff(object):
    pass


class ModelStuff(Stuff):
    """
    {app_name}/{model_name}/
        list/
        detail/{pk}/
    """
    verbose_name = None
    verbose_name_plural = None
    description = ""
    serializer_class = None
    renditions = []

    def __init__(self, model):
        if self.verbose_name is None:
            self.verbose_name = model._meta.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = model._meta.verbose_name_plural
        self.model = model

    def get_list_serializer(self):
        """"""
        class ListSerializer(ModelSerializer):
            url = HyperlinkedIdentityField(
                view_name='textplusstuff:%s-detail' % self.get_url_name_key(),
                lookup_field='pk'
            )

            class Meta:
                model = self.model
                fields = self.list_display + ('url',)

        return ListSerializer

    def list_view(self):
        """
        Returns a view that lists out all instances of self.model
        """
        return ListStuffView.as_view(
            model=self.model,
            serializer_class=self.get_list_serializer()
        )

    def detail_view(self):
        """
        Returns a view that returns a single instance of self.model

        Proposed response template:
        {
            'context': {context_here},
            'renditions': {
                {short_name}: {
                    'verbose_name':,
                    'description':,
                    'token':{% token_hurr %},
                }
            }
        }
        """
        return RetrieveStuffView.as_view(
            model=self.model,
            serializer_class=self.serializer_class,
            renditions=self.renditions
        )

    def get_url_name_key(self):
        return "%s-%s" % (
            self.model._meta.app_label,
            self.model._meta.model_name
        )

    def get_urls(self):
        url_name_key = self.get_url_name_key()
        urlpatterns = patterns(
            '',
            url(
                r'^list/$',
                self.list_view(),
                name='%s-list' % url_name_key
            ),
            url(
                r'^detail/(?P<pk>\w+)/$',
                self.detail_view(),
                name='%s-detail' % url_name_key
            ),
        )
        return urlpatterns


class StuffRegistry(object):
    """
    A StuffRegistry object allows Stuff to be registered on an app-by-app
    basis.
    """

    def __init__(self, name='stuff_registry'):
        self._stuff_registry = {}
        self.name = name

    def verify_stuff_cls(self, stuff_cls):
        invalid_stuff_msg = ''
        if not hasattr(stuff_cls, 'renditions'):
            invalid_stuff_msg = (
                "%s does not have any renditions! (All Stuff must have at "
                "least one renditiom)."
            ) % stuff_cls.__name__
        if invalid_stuff_msg:
            raise ImproperlyConfiguredStuff(invalid_stuff_msg)

    def verify_groups(self, groups, stuff_cls):
        """

        """
        for group in groups:
            if group not in STUFFGROUPS:
                raise NonExistantGroup(
                    "You tried registering %s with a group (%s) that is "
                    "not defined in settings.TEXTPLUSSTUFF_STUFFGROUPS." % (
                        stuff_cls.__name__,
                        group
                    )
                )

    def add(self, model, stuff_cls, groups=[]):
        """
        Registers the given model(s) with the given Stuff class.
        """
        if model in self._stuff_registry:
            raise AlreadyRegistered(
                'The model %s is already registered with the TextPlusStuff '
                'registry.' % model.__name__
            )
        else:
            self.verify_stuff_cls(stuff_cls)
            self.verify_groups(groups, stuff_cls)
            self._stuff_registry[model] = (stuff_cls(model), groups)

    def remove(self, model):
        """
        Unregisters the given model.

        If a model isn't already registered, this will raise NotRegistered.
        """
        if model not in self._stuff_registry:
            raise NotRegistered(
                'The model %s is not registered with the TextPlusStuff '
                'registry.' % model.__name__)
        else:
            del self._stuff_registry[model]

    def index(self):
        """
        Returns the 'front page' response of the TextPlusStuff builder.
        """
        STUFF_REGISTRY = self._stuff_registry

        class ListStuffGroups(APIView):
            """
            View to list all StuffGroups for this project.
            """
            registered_stuff = STUFF_REGISTRY

            def prepare_stuffgroups(self):
                if STUFFGROUPS:
                    stuffgroups = copy.copy(STUFFGROUPS)
                    # Verifying the StuffGroups listed in settings
                    for short_name, config in STUFFGROUPS.iteritems():
                        if 'name' not in config or 'description' not in config:
                            raise ImproperlyConfigured(
                                "The %s group is configured incorrectly. Each "
                                "group listed in "
                                "settings.TEXTPLUSSTUFF_STUFFGROUPS must "
                                "provide both a 'name' & a 'description' key."
                            )
                        else:
                            # OK, this config passed, give it a 'stuff' key
                            # to hold Stuff that is associated with it.
                            stuffgroups[short_name].update({
                                'stuff': []
                            })
                    return stuffgroups
                else:
                    return None

            def get_generated_stuffgroups(self):
                stuffgroups = self.prepare_stuffgroups()
                for model, tup in self.registered_stuff.iteritems():
                    stuff_cls, groups = tup
                    for group in groups:
                        stuffgroups[group]['stuff'].append({
                            'name': stuff_cls.verbose_name,
                            'description': stuff_cls.description or '',
                            'renditions': [
                                {
                                    'name': rendition.verbose_name,
                                    'description': rendition.description,
                                    'type': rendition.rendition_type,
                                    'short_name': rendition.short_name
                                }
                                for rendition in stuff_cls.renditions
                                if isinstance(rendition, Rendition)
                            ],
                            'instance_list': reverse(
                                'textplusstuff:%s-list' % (
                                    stuff_cls.get_url_name_key()
                                ),
                                request=self.request
                            )
                        })
                return stuffgroups

            def get(self, request, format=None):
                """
                Return a list of all StuffGroups.
                """
                return Response(self.get_generated_stuffgroups())

        return ListStuffGroups.as_view()

    def get_urls(self):
        urlpatterns = patterns(
            '',
            url(
                r'^$',
                self.index(),
                name='index'
            ),
        )

        for model, tup in six.iteritems(self._stuff_registry):
            stuff_config, groups = tup
            urlpatterns += patterns(
                '',
                url(
                    r'^%s/%s/' % (
                        model._meta.app_label,
                        model._meta.model_name
                    ),
                    include(stuff_config.get_urls())
                )
            )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'textplusstuff', 'textplusstuff'

stuff_registry = StuffRegistry()


def findstuff():
    """
    Auto-discover INSTALLED_APPS stuff.py modules and fail silently when
    not present. This forces an import on them (thereby registering their
    Stuff)

    This is a near 1-to-1 copy of how django's admin application registers
    models.
    """
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's sizedimage module.
        try:
            before_import_stuff_registry = copy.copy(
                stuff_registry._stuff_registry
            )
            import_module('%s.stuff' % app)
        except:
            # Reset the stuff_registry to the state before the last
            # import as this import will have to reoccur on the next request
            # and this could raise NotRegistered and AlreadyRegistered
            # exceptions (see django ticket #8245).
            stuff_registry._stuff_registry = before_import_stuff_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have a stuff module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'stuff'):
                raise