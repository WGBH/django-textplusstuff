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
            * 'html' : Default, will return a block of markdown flavored text as HTML
            * 'plain_text' : Returns a block of text with markdown syntax removed
            * 'markdown' : Returns the text as is.
        """
        if render_as in ['html', 'plain_text']:
            markdowner = Markdown()
            markdown_as_html = markdowner.convert(self.s)
            if render_as == 'html':
                to_return = markdown_as_html
            else:
                to_return = ''.join(BeautifulSoup(markdown_as_html).findAll(text=True))
        elif render_as == 'markdown':
            to_return = self.s
        else:
            raise Exception("`render_as` must be either 'html', 'plain_text' or 'markdown'")
        return to_return

class RichTextContentNode(BaseNode):
    """
    {% richtext '%(app_label)s:%(model)s:%(pk)d:%(rendition_key)s:%(field)s' %}
    """

    def __init__(self, node_id):
        node_id_split = node_id.split(':')
        self.node_mapping = {
            'content_type__app_label':node_id_split[0],
            'content_type__model':node_id_split[1],
            'object_id':node_id_split[2],
            'rendition_key':node_id_split[3],
            'field':node_id_split[4]
        }

    def __repr__(self):
        return force_str(
            "<RichTextContentNode: %s>" % (
                '|'.join([
                    "%s:%s" % (key, str(value))
                    for key, value in self.node_mapping.iteritems()
                ])
            ),
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
                    rendition_key=self.node_mapping.get('rendition_key'),
                    field=self.node_mapping.get('field')
                )
            except RichTextLink.DoesNotExist:
                node_content = None

            return node_content

    def render(self):
        # TODO: Each RichTextContentNode will need to refer to the soon-to-be-coded
        # richtext.registry to retrieve its context and template so a true rendering
        # can be accomplished.
        return '|'.join(["%s=%s" % (key,str(value)) for key, value in self.node_mapping.iteritems()])

__all__ = ('MarkdownFlavoredTextNode', 'RichTextContentNode')
