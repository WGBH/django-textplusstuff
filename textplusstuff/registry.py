class TextPlusStuffModelConfig(object):
    model = None

    def __init__(self, model):
        self.model = model

    rendition_template_config = [
        'name': {
            'template': None,
            'context_method': 'build_context',

        }
    ]

    def get_rendition_list(self):
        pass

    def validate_rendition(self, rendition):
        pass

    def build_context(self, instance, rendition):
        raise NotImplementedError

    def bloom(self, context, template):
        pass
