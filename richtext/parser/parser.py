from .nodes import (
    MarkdownFlavoredTextNode,
    RichTextContentNode
)


class RichTextParser(object):
    def __init__(self, tokens):
        self.tokens = tokens

    def next_token(self):
        return self.tokens.pop(0)

    def extend_nodelist(self, nodelist, node, token):
        nodelist.append(node)

    def parse(self, rendition=None):
        nodelist = []

        while self.tokens:
            token = self.next_token()

            if token.token_type == 1:   # MARKDOWN_FLAVORED_TEXT_TOKEN
                node_class = MarkdownFlavoredTextNode
            elif token.token_type == 2:  # RICHTEXTNODE_TOKEN
                node_class = RichTextContentNode

            self.extend_nodelist(
                nodelist=nodelist,
                node=node_class(token.contents),
                token=token
            )

        return nodelist
