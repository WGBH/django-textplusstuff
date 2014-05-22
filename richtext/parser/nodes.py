from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str

from BeautifulSoup import BeautifulSoup
from markdown2 import Markdown


class BaseNode(object):
    pass


class MarkdownFlavoredTextNode(BaseNode):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return force_str(
            "<MarkdownFlavoredTextNode: '%s'>" % self.s[:25],
            'ascii',
            errors='replace'
        )

    def render(self, render_as='html'):
        """
        `render_as` can be one of three values:
            * 'html': Returns a block of markdown flavored text as HTML
            * 'plain_text': Returns a block of text with markdown syntax
                            removed
            * 'markdown': Returns the text as is.
        """
        if render_as in ['html', 'plain_text']:
            markdowner = Markdown()
            markdown_as_html = markdowner.convert(self.s)
            if render_as == 'html':
                to_return = markdown_as_html
            else:
                to_return = ''.join(
                    BeautifulSoup(markdown_as_html).findAll(text=True)
                )
        elif render_as == 'markdown':
            to_return = self.s
        else:
            raise Exception(
                "`render_as` must be either 'html', 'plain_text' or 'markdown'"
            )
        return to_return


class RichTextContentNode(BaseNode):
    """
    {% richtext '%(app_label)s:%(model)s:%(pk)d:%(rendition_key)s:%(field)s' %}
    """
    node_args = (
        'content_type__app_label',
        'content_type__model',
        'object_id',
        'rendition_key',
        'field'
    )

    def __init__(self, node_id):
        """
        `node_id`: A colon-separated string of positional arguments
                   that corresponds to self.node_args
                   Example Value:
                   'carousel:carousel:4:main:content'
        """
        # Split `node_id` in preparation for building `self.node_mapping`
        node_id_split = node_id.split(':')

        # Initialize an empty dictionary
        node_mapping = {}
        # Iterate through each string in `node_id_split`...
        for index, node_segment in enumerate(node_id_split):
            try:
                # ...creating a key with a string from the same position
                # in `self.node_args` and a value `node_segment`
                node_mapping[self.node_args[index]] = node_segment
            except IndexError:
                # This exception will fire if we've already iterated through
                # every key in `self.node_args`. It can be safetly passed
                # since we wouldn't know how to deal with that value anyways.
                # This will allow any future subclasses to extend
                # `self.node_args` without having to rework this constructor.
                pass
        self.node_id = node_id
        self.node_mapping = node_mapping

    def __repr__(self):
        return force_str(
            "<RichTextContentNode: %s>" % self.node_id,
            'ascii',
            errors='replace'
        )

    def get_richtextlink_instance(self):
        from .models import RichTextLink
        try:
            ct = ContentType.objects.get(
                app_label=self.node_mapping.get('app_label'),
                model=self.node_mapping.get('model')
            )
        except ContentType.DoesNotExist:
            raise
        else:
            try:
                node_content = RichTextLink.objects.get(
                    content_type=ct,
                    object_id=self.node_mapping.get('instance_pk'),
                    field=self.node_mapping.get('field', '')
                )
            except RichTextLink.DoesNotExist:
                node_content = None

            return node_content

    def render(self):
        # TODO: Each RichTextContentNode will need to refer to the
        # soon-to-be-coded richtext.registry to retrieve its context
        # and template so a true rendering can be accomplished.
        return '|'.join([
            "%s=%s" % (key, str(value))
            for key, value in self.node_mapping.iteritems()
        ])

__all__ = ('MarkdownFlavoredTextNode', 'RichTextContentNode')
