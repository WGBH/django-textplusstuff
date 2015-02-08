from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils import six

from .parser import (
    MarkdownFlavoredTextNode,
    ModelStuffNode,
    TextPlusStuffLexer,
    TextPlusStuffParser
)


class TextPlusStuff(object):

    def __init__(self, raw_text, field=None):
        raw_text = raw_text or ""
        if not isinstance(raw_text, six.string_types):
            raise UnicodeError(
                (
                    "TextPlusStuff can only be initialized with either "
                    "unicode or UTF-8 strings."
                )
            )
        else:
            raw_text_processed = force_text(raw_text, errors='replace')
        self.raw_text = raw_text_processed
        # Initialize lexer
        lexer = TextPlusStuffLexer(raw_val=raw_text_processed)
        # Use the lexer to create tokens
        tokens = lexer.tokenize()
        # Pass tokens to parser and parse
        self.nodelist = TextPlusStuffParser(tokens=tokens).parse()

    def render(self, render_markdown_as, **kwargs):
        """
        Renders a TextPlusStuffField
        `render_markdown_as`: The format that markdown-flavored text should
        be transformed in. Options: `html`, `markdown`, `plain_text`
        """
        final_output = ""
        include_content_nodes = kwargs.pop('include_content_nodes', True)
        extra_context = kwargs.pop('extra_context', None)
        for node in self.nodelist:
            if isinstance(node, MarkdownFlavoredTextNode):
                final_output += node.render(render_as=render_markdown_as)
            elif isinstance(node, ModelStuffNode):
                if include_content_nodes is False:
                    pass
                else:
                    final_output += node.render(extra_context=extra_context)
        return final_output

    def as_html(self, **kwargs):
        """
        Renders a TextPlusStuffField as HTML.
        Optional keyword arguments:
        * `include_content_nodes`: Boolean signifying whether or not to render
                                   content nodes (i.e. ModelStuff tokens).
                                   Defaults to `True`.
        """
        return mark_safe(
            self.render(
                'html',
                include_content_nodes=kwargs.pop(
                    'include_content_nodes', True
                ),
                extra_context=kwargs.pop('extra_context', None)
            )
        )

    def as_plaintext(self, **kwargs):
        """
        Renders a TextPlusStuffField as plain text (all markdown
        formatting removed).

        Content nodes (i.e. ModelStuff tokens) will not be rendered.
        """
        return self.render(
            'plain_text',
            include_content_nodes=False
        )

    def as_markdown(self, **kwargs):
        """
        Renders a TextPlusStuffField as markdown.

        Content nodes (i.e. ModelStuff tokens) will not be rendered.
        """
        return self.render(
            'markdown',
            include_content_nodes=False
        )

__all__ = ('TextPlusStuff')
