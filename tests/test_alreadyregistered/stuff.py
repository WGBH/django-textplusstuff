from __future__ import unicode_literals

from textplusstuff import registry
from ..models import RegisteredModel


class DummyModelStuff(registry.ModelStuff):
    renditions = [
        registry.Rendition(
            short_name='foo',
            verbose_name='foo',
            description='foo',
            path_to_template='foo.html')
    ]

registry.stuff_registry.add_modelstuff(
    RegisteredModel,
    DummyModelStuff,
    groups=['test_group']
)

registry.stuff_registry.add_modelstuff(
    RegisteredModel,
    object,
    groups=['test_group']
)
