from __future__ import unicode_literals

from textplusstuff import registry

from ..models import RegisteredModel
from ..serializers import RegisteredModelSerializer


class RegisteredModelStuff(registry.ModelStuff):
    queryset = RegisteredModel.objects.all()
    description = 'Add an Registration Test Model'
    serializer_class = RegisteredModelSerializer
    renditions = [
        registry.Rendition(
            short_name='foo',
            verbose_name='Foo Rendition',
            description='Displays a Foo Rendition rendered.',
            path_to_template='nonexistant.html',
            rendition_type='block'
        ),
        registry.Rendition(
            short_name='foo',
            verbose_name='Foo Rendition Duplicate',
            description='Displays a Foo Rendition rendered.',
            path_to_template='nonexistant-duplicate.html',
            rendition_type='block'
        )
    ]
    list_display = ('id', 'title')

registry.stuff_registry.add_modelstuff(
    RegisteredModel,
    RegisteredModelStuff,
    groups=['test_group']
)
