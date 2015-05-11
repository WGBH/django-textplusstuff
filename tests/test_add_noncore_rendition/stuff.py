from __future__ import unicode_literals

from textplusstuff import registry
from ..models import RegisteredModel

rendition = registry.Rendition(
    short_name='baz',
    verbose_name='baz',
    description='baz',
    path_to_template='baz.html'
)

registry.stuff_registry.add_noncore_modelstuff_rendition(
    RegisteredModel,
    rendition
)
