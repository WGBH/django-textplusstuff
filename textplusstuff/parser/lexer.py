from __future__ import unicode_literals

import re

from ..exceptions import MalformedToken
from .tokens import TextPlusStuffToken

# The below compiled regex (`textplusstuff_re`) matches the following pattern:
# {% textplusstuff '%(content_type__app_label)s'
#             ':%(content_type__model)s:%(pk)d'
#             ':%(rendition_key)s:%(field)s' %}
# Example:
# {% textplusstuff 'carousel:carousel:4:full_width:content' %}

textplusstuff_re = re.compile(
    "\{\%\s*textplusstuff\s*.*?"
    "(?P<textplusstuff_token>[a-z-A-Z-0-9:_]+).*?\s*\%\}"
)


class TextPlusStuffLexer(object):

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
        for chunk in textplusstuff_re.split(self.raw_val):
            # Ensures empty, non-new-line values (i.e. '') won't
            # create unnecessary tokens
            if chunk:
                result.append(self.create_token(chunk, in_tag))
            # Since `textplusstuff_re.split(self.raw_val)` will return
            # alternating token types `in_tag` must switch between
            # `True` and `False` during each iteration.
            in_tag = not in_tag
        return result

    def create_token(self, token_string, in_tag):
        """
        Convert the given token string into a new Token object and return it.
        If `in_tag` is `True`, we are processing a 'chunk' that matched the
        pattern in `textplusstuff_re`, otherwise it should be treated as a
        markdown-flavored string.
        """
        if in_tag:
            try:
                token_type, token_string = token_string.split('__')
            except ValueError:
                raise MalformedToken(
                    "{} is a malformed token string!".format(token_string)
                )
            else:
                token = TextPlusStuffToken(
                    token_type=token_type,
                    contents=token_string
                )
        else:
            token = TextPlusStuffToken(
                token_type='MARKDOWNTEXT',
                contents=token_string
            )
        token.lineno = self.lineno
        self.lineno += token.contents.count('\n')
        return token
