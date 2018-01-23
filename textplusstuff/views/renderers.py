from __future__ import unicode_literals

from rest_framework.renderers import BrowsableAPIRenderer

from textplusstuff.__version__ import __version__ as VERSION

version_as_string = [
    str(segment)
    for segment in VERSION
]


class TextPlusStuffBrowsableAPIRenderer(BrowsableAPIRenderer):
    template = 'textplusstuff/api.html'

    def get_context(self, data, accepted_media_type, renderer_context):
        """
        Returns the context used to render.
        """
        context = super(TextPlusStuffBrowsableAPIRenderer, self).get_context(
            data, accepted_media_type, renderer_context
        )
        rest_framework_version = context['version']
        context.update({
            'rest_framework_version': rest_framework_version,
            'version': '.'.join(version_as_string)
        })
        return context
