from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from .parser import (
    MarkdownFlavoredTextNode,
    RichTextContentNode,
    RichTextLexer,
    RichTextParser
)


class RichText(object):

    def __init__(self, raw_text, field=None):
        if raw_text is None:
            raw_text = ""
        try:
            raw_text_processed = force_text(raw_text)
        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                "RichText can only be initialized with either "
                "unicode or UTF-8 strings."
            )
        else:
            self.raw_text = raw_text_processed
        # Initialize lexer
        lexer = RichTextLexer(raw_val=raw_text_processed)
        # Use the lexer to create tokens
        tokens = lexer.tokenize()
        # Pass tokens to parser and parse
        self.nodelist = RichTextParser(tokens=tokens).parse()

    def render(self, text_output_format='html', include_content_nodes=True):
        """"""
        final_output = ""
        for node in self.nodelist:
            if isinstance(node, MarkdownFlavoredTextNode):
                final_output += node.render(render_as=text_output_format)
            elif isinstance(node, RichTextContentNode):
                if (not include_content_nodes) or (
                    text_output_format in ['plain_text', 'markdown']
                ):
                    pass
                else:
                    final_output += node.render()
        return final_output

    @property
    def as_html(self):
        return mark_safe(
            self.render(
                text_output_format='html',
                include_content_nodes=True
            )
        )

    @property
    def as_plaintext(self):
        return self.render(
            text_output_format='plain_text',
            include_content_nodes=False
        )

    @property
    def as_markdown(self):
        return self.render(
            text_output_format='markdown',
            include_content_nodes=False
        )

__all__ = ('RichText')
