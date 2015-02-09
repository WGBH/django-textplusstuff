Using textplusstuff
===================

Registering Stuff
-----------------

To start using textplusstuff you have to register a model as Stuff. The examples below will use the creatively named `TestModel` which has one attribute, 'name' a `CharField`:

1. Create a file called `serializers.py` within the app that has the model you want to register as stuff:

    .. code-block:: bash

        someproject/
            someapp/
                models.py
                serializers.py # Like this!

2. Now open `serializers.py` to create your first serializer. For more information on serializing models `check out django REST frameworks fantastic docs <http://www.django-rest-framework.org/api-guide/serializers#modelserializer>`__.:

        .. code-block:: python

            # serializers.py

            from rest_framework.serializers import ModelSerializer

            from .models import TestModel

            class TestModelSerializer(ModelSerializer):

                class Meta:
                    model = TestModel
                    fields = (
                        'name',
                    )

3. OK, now that we've got a serializer when need to create a file called ``stuff.py`` within the app that has the model you want to register as Stuff:

    .. code-block:: bash

        someproject/
            someapp/
                models.py
                serializers.py
                stuff.py # Like this!

4. Now open the `stuff.py` file you just created and import the model you want to register and the serializer you just created:

    .. code-block:: python

        # someapp/stuff.py
        from textplusstuff import registry

        from .models import TestModel
        from .serializers import TestModelSerializer

        class TestModelStuff(registry.ModelStuff):
            # The queryset used to retrieve instances of TestModel
            # within the front-end interface. For instance, you could
            # exclude 'unpublished' instances or anything else you can
            # query the ORM against
            queryset = RoadshowTable.objects.all()

            # What humans see when they see this stuff
            verbose_name = 'Test Model'
            verbose_name_plural = 'Test Models'
            description = 'Add a Test Model'

            # The serializer we just defined, this is what provides the context/JSON
            # payload for this Stuff
            serializer_class = TestModelSerializer

            # All Stuff must have at least one rendition (specified in
            # the `renditions` attribute below) which basically
            # just points to a template and some human-readable metadata.
            # At present there are only two options for setting rendition_type:
            # either 'block' (the default) or inline. These will be used by
            # the front-end editor when placing tokens.
            renditions = [
                registry.Rendition(
                    short_name='sidebar_left',
                    verbose_name='Test Model Sidebar',
                    description='Displays a Test Model in the sidebar.',
                    path_to_template='someapp/templates/sidebar_left.html',
                    rendition_type='block'
                )
            ]
            # The attributes used in the list (table) display of the front-end
            # editing tool.
            list_display = ('id', 'name')

        # OK, now let's register our Model and its Stuff config:
        registry.stuff_registry.add_modelstuff(
            TestModel,
            TestModelStuff,
            groups=['image', 'media']
        )

    Once you've registered your Stuff you can test if it worked by firing up a webserver and visiting http://localhost:8000/textplusstuff/.

Using the TextPlusStuff field
-----------------------------

Using a TextPlusStuff field is easy just import it and set it to an attribute. Any options available to a django TextField (like blank=True) can be set on a TextPlusStuffField:

    .. code-block:: python

        # someapp/models.py

        from django.db import models

        from textplusstuff.fields import TextPlusStuffField

        class MyModel(models.Model):
            content = TextPlusStuffField()

TextPlusStuff fields store rich text as markdown and can serve it back as either raw markdown, plain text (formatting removed), or as HTML (markdown entities converted into HTML tags):

    .. code-block:: python

        >>> from someapp.models import MyModel
        >>> instance = MyModel(content='Oh _hello there_!')
        >>> instance.save()
        >>> instance.content.as_markdown()
        'Oh _hello there_!'
        >>> instance.content.as_plaintext()
        'Oh hello there!'
        >>> instance.content.as_html()
        'Oh <em>hello there</em>!'

Try pasting some tokens (that you find at /textplusstuff) into a TextPlusStuffField, saving the model instance associated with the field and then call the attributes above to see what happens.

Adding just-in-time extra context to .as_html() rendering
`````````````````````````````````````````````````````````

If you want to include extra context data beyond what is provided natively by a token just pass a dictionary to the `extra_context` keyword argument of the `as_html()` method:

    >>> instance.content.as_html(extra_context={'some_key': 'some_value'})

This dictionary will then be passed to the `context keyword argument of the serializer class <http://www.django-rest-framework.org/api-guide/serializers.html#including-extra-context>`__ associated with that token's Stuff config. `Click here <http://www.django-rest-framework.org/api-guide/serializers.html#including-extra-context>`__ for more information about how to access this data within your serializer.

Admin Integration
-----------------

There currently isn't a front-end interface for TextPlusStuff fields and this makes finding tokens unnecessarily difficult (unless you're a weirdo who likes groking JSON). To mitigate this, just swap the superclass of your admin configurations from ``django.contrib.admin.ModelAdmin`` with ``textplusstuff.admin.TextPlusStuffRegisteredModelAdmin`` like so:

    .. code-block:: python

        from django.contrib import admin

        from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

        # A model registered with textplusstuff.registry.stuff_registry
        from .models import SomeModel

        class SomeModelAdmin(TextPlusStuffRegisteredModelAdmin):
            # Configure like you would any admin.ModelAdmin class
            pass

        admin.site.register(SomeModel, SomeModelAdmin)

This will add an 'Available Renditions' sections beneath the change/edit form within the admin that contains a table that lists all the available renditions for that model (including their instance-associated tokens).
