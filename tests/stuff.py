from __future__ import unicode_literals

from textplusstuff import registry

from .models import RegisteredModel
from .serializers import RegisteredModelSerializer


class RegisteredModelStuff(registry.ModelStuff):
    # The queryset used to retrieve instances of TestModel
    # within the front-end interface. For instance, you could
    # exclude 'unpublished' instances or anything else you can
    # query the ORM against
    queryset = RegisteredModel.objects.all()

    # What humans see when they see this stuff
    # verbose_name = 'Registration Test Model'
    # verbose_name_plural = 'Registration Test Models'
    description = 'Add an Registration Test Model'

    # The serializer we just defined, this is what provides the context/JSON
    # payload for this Stuff
    serializer_class = RegisteredModelSerializer

    # All Stuff must have at least one rendition (specified in
    # the `renditions` attribute below) which basically
    # just points to a template and some human-readable metadata.
    # At present there are only two options for setting rendition_type:
    # either 'block' (the default) or inline. These will be used by
    # the front-end editor when placing tokens.
    renditions = [
        registry.Rendition(
            short_name='test_rendition',
            verbose_name='Test Rendition',
            description='Displays a Test Rendition rendered.',
            path_to_template='RegisteredModel_test_rendition.html',
            rendition_type='block'
        )
    ]
    # The attributes used in the list (table) display of the front-end
    # editing tool.
    list_display = ('id', 'title')

# OK, now let's register our Model and its Stuff config:
registry.stuff_registry.add_modelstuff(
    RegisteredModel,
    RegisteredModelStuff,
    groups=['test_group']
)

# Testing stuff_registry.remove_modelstuff
registry.stuff_registry.remove_modelstuff(RegisteredModel)

# Re-registering for remaining tests
registry.stuff_registry.add_modelstuff(
    RegisteredModel,
    RegisteredModelStuff,
    groups=['test_group']
)
