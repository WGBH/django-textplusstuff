from __future__ import unicode_literals

from .nodes import (
    MarkdownFlavoredTextNode,
    ModelStuffNode
)

TOKEN_NODE_MAPPING = {
    'MARKDOWNTEXT': MarkdownFlavoredTextNode,
    'MODELSTUFF': ModelStuffNode
}


class TextPlusStuffToken(object):

    def __init__(self, token_type, contents):
        # token_type must be MARKDOWN_FLAVORED_TEXT_TOKEN
        # or RICHTEXT_TOKEN.
        self.token_type, self.contents = token_type, contents
        self.lineno = None

    def __str__(self):
        return '<{token_type} token: "{content}...">'.format(
            token_type=self.token_type,
            content=self.contents[:10].replace('\n', '')
        )
