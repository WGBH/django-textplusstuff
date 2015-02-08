from __future__ import unicode_literals

from textplusstuff import registry

from ..models import RegisteredModel
from ..serializers import RegisteredModelSerializer


class RegisteredModelStuff(registry.ModelStuff):
    queryset = RegisteredModel.objects.all()
    description = 'Add an Registration Test Model'
    serializer_class = RegisteredModelSerializer
    renditions = [
        object()
    ]
    list_display = ('id', 'title')

registry.stuff_registry.add_modelstuff(
    RegisteredModel,
    RegisteredModelStuff,
    groups=['test_group']
)
