from __future__ import unicode_literals

from textplusstuff import registry
from ..models import RegisteredModel

dupe_rendition = registry.Rendition(
    short_name='test_rendition',
    verbose_name='Test Rendition',
    description='Displays a Test Rendition rendered.',
    path_to_template='RegisteredModel_test_rendition.html',
    rendition_type='block'
)

registry.stuff_registry.add_noncore_modelstuff_rendition(
    RegisteredModel,
    dupe_rendition
)
