from __future__ import unicode_literals

from rest_framework.serializers import CharField

from .datastructures import TextPlusStuff


class TextPlusStuffFieldSerializer(CharField):
    """
    Returns a dictionary of all available permutations of a TextPlusStuffField

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
                'as_html': value.as_html(),
                'as_html_no_tokens': value.as_html(
                    include_content_nodes=False
                ),
            }
