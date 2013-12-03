MARKDOWN_FLAVORED_TEXT_TOKEN = 1
RICHTEXTNODE_TOKEN = 2

TOKEN_TYPES = {
    MARKDOWN_FLAVORED_TEXT_TOKEN: 'MarkdownFlavoredText',
    RICHTEXTNODE_TOKEN: 'RichTextContentNode'
}

class RichTextToken(object):

    def __init__(self, token_type, contents):
        # token_type must be MARKDOWN_FLAVORED_TEXT_TOKEN
        # or RICHTEXT_TOKEN.
        self.token_type, self.contents = token_type, contents
        self.lineno = None

    def __str__(self):
        token_name = TOKEN_TYPES[self.token_type]
        return ('<%s token: "%s...">' %
                (token_name, self.contents[:50].replace('\n', '')))
