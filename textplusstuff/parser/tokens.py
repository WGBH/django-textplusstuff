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
        return '<%s token: "%s...">' % (
            self.token_type,
            self.contents[:10].replace('\n', '')
        )
