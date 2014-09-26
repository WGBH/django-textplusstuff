from .tokens import TOKEN_NODE_MAPPING


class TextPlusStuffParser(object):
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

            node_class = TOKEN_NODE_MAPPING[token.token_type]

            self.extend_nodelist(
                nodelist=nodelist,
                node=node_class(token.contents),
                token=token
            )

        return nodelist
