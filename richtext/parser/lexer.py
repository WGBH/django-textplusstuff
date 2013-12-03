import re

from .tokens import (
    MARKDOWN_FLAVORED_TEXT_TOKEN,
    RICHTEXTNODE_TOKEN,
    RichTextToken
)

# The below compiled regex (`richtext_re`) matches the following pattern:
# {% richtext '%(content_type__app_label)s'
#             ':%(content_type__model)s:%(pk)d'
#             ':%(rendition_key)s:%(field)s' %}
# Example:
# {% richtext 'carousel:carousel:4:full_width:content' %}

richtext_re = re.compile("""\{\%\s*richtext\s*.*?(?P<richtext_token>[a-z-0-9:]+).*?\s*\%\}""")

class RichTextLexer(object):

    def __init__(self, raw_val):
        self.raw_val = raw_val
        self.lineno = 1

    def tokenize(self):
        """
        Return a list of tokens from self.raw_val
        """
        # `in_tag` is initially set to `False` since it will
        # always encounter a non-token first. Even if the token
        # is at the beginning of `self.raw_val` the first value
        # returned will be an empty string.
        in_tag = False
        result = []
        for chunk in richtext_re.split(self.raw_val):
            # Ensures empty, non-new-line values (i.e. '') won't
            # create unnecessary tokens
            if chunk:
                result.append(self.create_token(chunk, in_tag))
            # Since `richtext_re.split(self.raw_val)` will return
            # alternating token types `in_tag` must switch between
            # `True` and `False` during each iteration.
            in_tag = not in_tag
        return result

    def create_token(self, token_string, in_tag):
        """
        Convert the given token string into a new Token object and return it.
        If `in_tag` is `True`, we are processing a 'chunk' that matched the
        pattern in `richtext_re`, otherwise it should be treated as a
        markdown-flavored string.
        """
        if in_tag:
            token = RichTextToken(
                        token_type=RICHTEXTNODE_TOKEN,
                        contents=token_string
                    )
        else:
            token = RichTextToken(
                        token_type=MARKDOWN_FLAVORED_TEXT_TOKEN,
                        contents=token_string
                    )
        token.lineno = self.lineno
        self.lineno += token.contents.count('\n')
        return token
