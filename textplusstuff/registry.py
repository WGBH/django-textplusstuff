from __future__ import unicode_literals

import collections
import copy

from django.conf import settings
from django.conf.urls import url, include
from django.template.loader import get_template
from django.utils import six
from django.utils.encoding import force_text
from django.utils.text import slugify

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy as reverse
from rest_framework.serializers import ModelSerializer, \
    HyperlinkedIdentityField

from .exceptions import (
    AlreadyRegistered,
    AlreadyRegisteredRendition,
    NotRegistered,
    NonExistentGroup,
    InvalidRenditionType,
    InvalidRendition,
    ImproperlyConfigured,
    ImproperlyConfiguredStuff
)
from .views import (
    ListStuffView,
    RetrieveStuffView,
    TextPlusStuffAPIViewMixIn
)


class Rendition(object):

    def __init__(self, short_name, verbose_name, description,
                 path_to_template, rendition_type='block'):
        if six.PY2:
            short_name = force_text(short_name)

        self.short_name = slugify(short_name)
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

    def get_context_data(self, **context):
        return context

    def render_as_html(self, context):
        template = get_template(self.path_to_template)
        context = self.get_context_data(context=context)
        return template.render(context)


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
        self._renditions = self._verify_and_build_initial_rendition_dict()
        self.model = model

    def _verify_rendition(self, rendition):
        if not isinstance(rendition, Rendition):
            raise InvalidRendition(
                "{} is an invalid Rendition. All Renditions must "
                "be a subclass of textplusstuff.registry.Rendition".format(
                    rendition
                )
            )

    def _verify_rendition_list_uniqueness(self, rendition_list):
        non_unique_renditions = [
            x
            for x, y in collections.Counter([
                rendition.short_name
                for rendition in rendition_list
            ]).items()
            if y > 1
        ]
        if non_unique_renditions:
            raise InvalidRendition(
                "{} has multiple renditions associated it that use the "
                "'short_name' {}. 'short_name' values must be unique across "
                "all renditions associated with a Stuff subclass.".format(
                    self.__class__.__name__,
                    non_unique_renditions[0]
                )
            )

    def _verify_and_build_initial_rendition_dict(self):
        for rendition in self.renditions:
            self._verify_rendition(rendition)
        self._verify_rendition_list_uniqueness(self.renditions)
        return dict(
            (rendition.short_name, rendition)
            for rendition in self.renditions
        )

    def register_non_core_rendition(self, rendition):
        """
        Register a 'non-core' rendition with this Stuff Config
        """
        self._verify_rendition(rendition)
        if rendition.short_name in self._renditions:
            raise AlreadyRegisteredRendition(
                "A rendition with a short_name of '{}' has already been "
                "registered to {} (for model: {}).".format(
                    rendition.short_name,
                    self.__class__.__name__,
                    self.model
                )
            )
        else:
            self._renditions[rendition.short_name] = rendition

    def get_list_serializer(self):
        """"""
        class ListSerializer(ModelSerializer):
            url = HyperlinkedIdentityField(
                view_name='textplusstuff:{}-detail'.format(
                    self.get_url_name_key()
                ),
                lookup_field='pk'
            )

            class Meta:
                model = self.model
                fields = self.list_display + ('url',)

        return ListSerializer

    def list_view(self):
        """
        Return a view that lists out all instances of self.model
        """
        return ListStuffView.as_view(
            model=self.model,
            queryset=self.queryset,
            serializer_class=self.get_list_serializer()
        )

    def detail_view(self):
        """
        Return a view that returns a single instance of self.model

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
            queryset=self.queryset,
            serializer_class=self.serializer_class,
            renditions=self._renditions
        )

    def get_url_name_key(self):
        return "{app}-{model}".format(
            app=self.model._meta.app_label,
            model=self.model._meta.model_name
        )

    def get_urls(self):
        url_name_key = self.get_url_name_key()
        urlpatterns = [
            url(
                r'^list/$',
                self.list_view(),
                name='{}-list'.format(url_name_key)
            ),
            url(
                r'^detail/(?P<pk>\w+)/$',
                self.detail_view(),
                name='{}-detail'.format(url_name_key)
            ),
        ]
        return urlpatterns


class StuffRegistry(object):
    """
    A StuffRegistry object allows Stuff to be registered on an app-by-app
    basis.
    """

    def __init__(self, name='stuff_registry'):
        self._registry = {}
        self.name = name

    def verify_stuff_cls(self, stuff_cls):
        """
        Verify that a Stuff class is properly configured.
        """
        invalid_stuff_msg = ''
        if not stuff_cls.renditions:
            invalid_stuff_msg = (
                "{} does not have any renditions! (All Stuff must have at "
                "least one rendition)."
            ).format(stuff_cls.__name__)
        if invalid_stuff_msg:
            raise ImproperlyConfiguredStuff(invalid_stuff_msg)

    def verify_groups(self, groups, stuff_cls):
        """
        Verify that Stuff Groups are properly configured.
        """
        stuffgroups = getattr(
            settings, 'TEXTPLUSSTUFF_STUFFGROUPS', {}
        )
        for group in groups:
            if group not in stuffgroups:
                raise NonExistentGroup(
                    "You tried registering {} with a group ({}) that is not "
                    "defined in settings.TEXTPLUSSTUFF_STUFFGROUPS.".format(
                        stuff_cls.__name__,
                        group
                    )
                )

    def add_modelstuff(self, model, stuff_cls, groups=[]):
        """
        Register the given model(s) with the given Stuff class.
        """
        if model in self._registry:
            raise AlreadyRegistered(
                'The model {} is already registered with the TextPlusStuff '
                'registry.'.format(model.__name__)
            )
        else:
            self.verify_stuff_cls(stuff_cls)
            self.verify_groups(groups, stuff_cls)
            self._registry[model] = (stuff_cls(model), groups)

    def add_noncore_modelstuff_rendition(self, model, rendition):
        """
        Register a 'non-core' rendition (`rendition`) with `model`.

        Raises `NotRegistered` if `model` isn't registered.
        """
        if self._registry.get(model, None) is not None:
            stuff_cls = self._registry.get(model)[0]
            stuff_cls.register_non_core_rendition(rendition)
        else:
            raise NotRegistered(
                'The model {} is not registered with the TextPlusStuff '
                'registry.'.format(model.__name__)
            )

    def remove_modelstuff(self, model):
        """
        Unregister the given model.

        If a model isn't already registered, this will raise NotRegistered.
        """
        if model not in self._registry:
            raise NotRegistered(
                'The model {} is not registered with the TextPlusStuff '
                'registry.'.format(model.__name__)
            )
        else:
            del self._registry[model]

    def index(self):
        """
        Return the 'front page' response of the TextPlusStuff builder.
        """
        stuff_registry = self._registry

        class ListStuffGroups(TextPlusStuffAPIViewMixIn, APIView):
            """
            View to list all StuffGroups for this project.
            """
            registered_stuff = stuff_registry

            def prepare_stuffgroups(self):
                stuffgroups = getattr(
                    settings, 'TEXTPLUSSTUFF_STUFFGROUPS', {}
                )
                if stuffgroups:
                    stuffgroups_copy = copy.copy(
                        getattr(settings, 'TEXTPLUSSTUFF_STUFFGROUPS', {})
                    )
                    # Verifying the StuffGroups listed in settings
                    for short_name, config in six.iteritems(stuffgroups):
                        if 'name' not in config or 'description' not in config:
                            raise ImproperlyConfigured(
                                "The %s group is configured incorrectly. Each "
                                "group listed in "
                                "settings.TEXTPLUSSTUFF_STUFFGROUPS must "
                                "provide both a 'name' & a 'description' key."
                                % short_name
                            )
                        else:
                            # OK, this config passed, give it a 'stuff' key
                            # to hold Stuff that is associated with it.
                            stuffgroup = collections.OrderedDict([
                                ('name', stuffgroups_copy[short_name]['name']),
                                ('short_name', short_name),
                                (
                                    'description',
                                    stuffgroups_copy[short_name]['description']
                                ),
                                ('stuff', [])
                            ])
                            stuffgroups_copy[short_name] = stuffgroup
                    return stuffgroups_copy
                else:
                    return None

            def get_generated_stuffgroups(self):
                stuffgroups = self.prepare_stuffgroups()
                if not stuffgroups:
                    raise ImproperlyConfigured(
                        'To use textplustuff the TEXTPLUSSTUFF_STUFFGROUPS '
                        'must be set in your settings file.'
                    )
                else:
                    for model, tup in six.iteritems(self.registered_stuff):
                        stuff_cls, groups = tup
                        for group in groups:
                            stuffgroups[group][
                                'stuff'
                            ].append(collections.OrderedDict([
                                ('name', stuff_cls.verbose_name),
                                ('description', stuff_cls.description or ''),
                                ('instance_list', reverse(
                                    'textplusstuff:{}-list'.format(
                                        stuff_cls.get_url_name_key()
                                    ),
                                    request=self.request
                                )),
                                ('renditions', [
                                    {
                                        'name': rendition.verbose_name,
                                        'description': rendition.description,
                                        'type': rendition.rendition_type,
                                        'short_name': rendition.short_name
                                    }
                                    for short_name, rendition in six.iteritems(
                                        stuff_cls._renditions
                                    )
                                ])
                            ]))
                    return [
                        stuffgroup
                        for short_name, stuffgroup in six.iteritems(
                            stuffgroups
                        )
                    ]

            def get(self, request, format=None):
                """
                Return a list of all StuffGroups.
                """
                return Response(self.get_generated_stuffgroups())

        return ListStuffGroups.as_view()

    def get_urls(self):
        urlpatterns = [
            url(
                r'^$',
                self.index(),
                name='index'
            ),
        ]

        for model, tup in six.iteritems(self._registry):
            stuff_config, groups = tup
            urlpatterns += [
                url(
                    r'^{app}/{model}/'.format(
                        app=model._meta.app_label,
                        model=model._meta.model_name
                    ),
                    include(stuff_config.get_urls())
                )
            ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'textplusstuff', 'textplusstuff'


stuff_registry = StuffRegistry()


def get_modelstuff_renditions(model_instance):
    """
    Build out a dict of the available MODELSTUFF renditions
    for a particular model instance
    """
    stuff_config, groups = stuff_registry._registry.get(
        model_instance._meta.model, (None, None)
    )
    if stuff_config is not None:
        return dict(
            (
                short_name,
                {
                    'verbose_name': rendition.verbose_name,
                    'description': rendition.description,
                    'token': (
                        "{{% textplusstuff 'MODELSTUFF__{app}:{model}:"
                        "{pk}:{rend}' %}}"
                    ).format(
                        app=model_instance._meta.app_label,
                        model=model_instance._meta.model_name,
                        pk=model_instance.pk,
                        rend=short_name
                    ),
                    'path_to_template': rendition.path_to_template,
                    'type': rendition.rendition_type

                }
            )
            for short_name, rendition in six.iteritems(
                stuff_config._renditions
            )
        )
