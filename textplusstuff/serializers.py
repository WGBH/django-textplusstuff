from __future__ import unicode_literals

import copy

from rest_framework import VERSION as REST_FRAMEWORK_VERSION
from rest_framework.serializers import CharField

from .datastructures import TextPlusStuff


class ExtraContextSerializerMixIn(object):
    """
    A serializer mixin that conveniently adds the entirety of self.context to
    the 'extra_context' key of `to_representation`.
    """

    def to_native(self, instance):
        """For backwards compatibility with djangorestframework 2.X.X"""
        return self.to_representation(instance)

    def to_representation(self, instance):
        """
        Add self.context to the 'extra_context' key of a
        serializers output.
        """
        if REST_FRAMEWORK_VERSION.startswith('2.'):
            payload = super(
                ExtraContextSerializerMixIn, self
            ).to_native(instance)
        else:
            payload = super(
                ExtraContextSerializerMixIn, self
            ).to_representation(instance)
        extra_context = copy.copy(self.context) or {}
        extra_context.pop('view', None)
        extra_context.pop('request', None)
        extra_context.pop('format', None)
        payload.update({
            'extra_context': extra_context
        })
        return payload


class TextPlusStuffFieldSerializer(CharField):
    """
    Return a dictionary of all available permutations of a TextPlusStuffField

    Example:
    {
        'raw_text': <Raw value of the field>,
        'as_plaintext': <As plaintext, no tokens rendered>,
        'as_markdown': <As markdown, no tokens rendered>,
        'as_html': <As HTML markup with tokens rendered>,
        'as_html_no_tokens': <As HTML markup no tokens rendered>,
    }
    """

    read_only = True

    def to_native(self, value):
        """For djangorestframework>=2.4.x"""
        return self.to_representation(value)

    def to_representation(self, value):
        if not isinstance(value, TextPlusStuff):
            raise ValueError(
                "Only TextPlusStuffFields can be rendered by "
                "the TextPlusStuffFieldSerializer"
            )
        else:
            return {
                'raw_text': value.raw_text,
                'as_plaintext': value.as_plaintext(),
                'as_markdown': value.as_markdown(),
                'as_html': value.as_html(extra_context=getattr(
                    self, 'context', {}
                )),
                'as_html_no_tokens': value.as_html(
                    include_content_nodes=False
                ),
                'as_json': value.as_json(convert_to_json_string=False)
            }
